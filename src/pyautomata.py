from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass

from consts import LAMBDA
from grammar import Grammar
import grammar


class Automata(ABC):
    @abstractmethod
    def accepts(self, string: str) -> bool:
        pass


class FA(Automata, ABC):
    """Abstract base class for NFA and DFA"""


@dataclass
class NFA(FA):
    states: set[str]
    input_symbols: set[str]
    # a dict from current state to a dict from input symbol to the set of end states
    transitions: dict[str, dict[str, set[str]]]
    initial_state: str
    final_states: set[str]

    def accepts(self, string: str) -> bool:
        raise Exception("Not implemented yet")

    def get_lambda_closure(self, start_state: str) -> set[str]:
        encountered_states = set()
        stack = []
        stack.append(start_state)
        while stack:
            state = stack.pop()
            if state not in encountered_states:
                encountered_states.add(state)
                if LAMBDA in self.transitions[state]:
                    stack.extend(self.transitions[state][LAMBDA])

        return encountered_states

    def get_next_states(self, current_states, input_symbol):
        """Used in converting DFA to NFA"""
        next_states = set()

        for current_state in current_states:
            symbol_end_states = self.transitions[current_state].get(input_symbol)
            if symbol_end_states:
                for end_state in symbol_end_states:
                    next_states.update(self.get_lambda_closure(end_state))

        return next_states

    @staticmethod
    def from_grammar(rg: Grammar) -> 'NFA':
        if grammar.is_llg(rg):
            return NFA._from_llg(rg)

        if grammar.is_rlg(rg):
            return NFA._from_rlg(rg)

        raise ValueError("input grammar is not regular")

    @staticmethod
    def _from_rlg(rlg: Grammar) -> 'NFA':
        states = rlg.nonterminals.copy()
        states.add('F')

        return NFA(
            states=states,
            input_symbols=rlg.terminals,
            transitions=NFA._transitions_from_rules(rlg),
            initial_state=rlg.start_symbol,
            final_states={'F'}
        )

    @staticmethod
    def _from_llg(llg: Grammar) -> 'NFA':
        reversed_grammar = Grammar(
            rules=[[left_side, right_side[::-1]] for left_side, right_side in llg.rules],
            nonterminals=llg.nonterminals,
            terminals=llg.terminals,
            start_symbol=llg.start_symbol,
        )
        nfa = NFA._from_rlg(reversed_grammar)
        return nfa.reverse()

    def reverse(self):
        new_states = self.states.copy()
        new_initial_state = 0
        while new_initial_state in self.states:
            new_initial_state += 1
        new_states.add(str(new_initial_state))

        new_transitions = {state: {} for state in new_states}
        for state1, transitions in self.transitions.items():
            for symbol, states in transitions.items():
                for state2 in states:
                    new_transitions[state2].setdefault(symbol, set()).add(state1)

        new_transitions[new_initial_state][LAMBDA] = self.final_states.copy()

        return NFA(
            states=new_states,
            input_symbols=self.input_symbols,
            transitions=new_transitions,
            initial_state=new_initial_state,
            final_states={self.initial_state}
        )


    @staticmethod
    def _transitions_from_rules(rlg: Grammar) -> dict[str, dict[str, set[str]]]:
        # {'q0': {'a': {'q1', 'q2'}}} indicates a transition from q0 to q1 or q2 by reading 'a'
        transitions = {'F': {}}
        i = 0
        for left_side, right_side in rlg.rules:
            if right_side[-1] in rlg.nonterminals:
                if len(right_side) == 2:
                    transitions.setdefault(left_side, {}).setdefault(right_side[0], set()).add(right_side[1])
                else:
                    transitions.setdefault(left_side, {}).setdefault(right_side[0], set()).add(f'W{i}')
                    for terminal in right_side[1:-2]:
                        transitions[f'W{i}'] = {terminal: {f'W{i + 1}'}}
                        i += 1
                    transitions[f'W{i}'] = {right_side[-2]: {right_side[-1]}}
                    i += 1
            else:
                if len(right_side) == 1:
                    transitions.setdefault(left_side, {}).setdefault(right_side, set()).add('F')
                else:
                    transitions.setdefault(left_side, {}).setdefault(right_side[0], set()).add(f'W{i}')
                    for terminal in right_side[1:-1]:
                        transitions[f'W{i}'] = {terminal: {f'W{i + 1}'}}
                        i += 1
                    transitions[f'W{i}'] = {right_side[-2]: {'F'}}
                    i += 1

        return transitions


@dataclass
class DFA(FA):
    states: set[str]
    input_symbols: set[str]
    # a dict from current state to a dict from input symbol to the end state
    transitions: dict[str, dict[str, str]]
    initial_state: str
    final_states: set[str]

    def accepts(self, string: str) -> bool:
        if not set(string).issubset(self.input_symbols):
            return False

        cur_state = self.initial_state
        for symbol in string:
            cur_state = self.transitions[cur_state][symbol]
        return cur_state in self.final_states

    @staticmethod
    def from_nfa(nfa: NFA):
        def stringify_states(states: set[str]) -> str:
            return f"[{','.join(sorted(states))}]"

        states = set()
        transitions = {}
        nfa_initial_states = nfa.get_lambda_closure(nfa.initial_state)
        initial_state = stringify_states(nfa_initial_states)
        final_states = set()

        state_queue = deque()
        state_queue.append(nfa_initial_states)
        while state_queue:
            current_states = state_queue.popleft()

            current_state_name = stringify_states(current_states)
            if current_state_name in states:
                continue

            states.add(current_state_name)
            transitions[current_state_name] = {}
            if current_states & nfa.final_states:
                final_states.add(current_state_name)

            for input_symbol in nfa.input_symbols:
                next_states = nfa.get_next_states(current_states, input_symbol)
                transitions[current_state_name][input_symbol] = stringify_states(next_states)
                state_queue.append(next_states)

        return DFA(
            states=states,
            input_symbols=nfa.input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )


class PDA(Automata, ABC):
    pass


@dataclass
class DPDA(PDA):
    states: set[str]
    final_states: set[str]
    initial_state: str
    input_symbols: set[str]
    stack_symbols: set[str]
    transitions: dict[str, dict[str, tuple[str, str, str]]]
    stack_start_symbol: str

    def accepts(self, string: str) -> bool:
        """Acceptance by final state"""
        if not set(string).issubset(self.input_symbols):
            return False

        cur_state = self.initial_state
        stack = ['Z']
        for i, symbol in enumerate(string):
            next_state, to_pop, to_push = self.transitions[cur_state][symbol]
            stack.pop(to_pop)
            if to_push != LAMBDA:
                stack.append(to_push)

            if not stack:
                return i == len(string) - 1 and cur_state in self.final_states

            cur_state = next_state

        return cur_state in self.final_states
