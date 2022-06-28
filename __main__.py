import json

from visual_automata.fa.nfa import VisualNFA
from visual_automata.fa.dfa import VisualDFA

import cfl
import rl
from grammar import Grammar


def main() -> None:
    with open("grammar_input.json", "r") as f:
        input_grammar = Grammar.from_dict(json.load(f))

    if rl.is_rg(input_grammar):
        nfa = rl.NFA.from_grammar(input_grammar)
        visual_nfa = VisualNFA(
            initial_state=nfa.initial_state,
            states=nfa.states,
            final_states=nfa.final_states,
            input_symbols=nfa.input_symbols,
            transitions=nfa.transitions,
        )
        visual_nfa.show_diagram(filename="NFA")
        print("NFA graph is saved in NFA.png file")

        dfa = rl.DFA.from_nfa(nfa)
        visual_dfa = VisualDFA(
            states=dfa.states,
            input_symbols=dfa.input_symbols,
            transitions=dfa.transitions,
            initial_state=dfa.initial_state,
            final_states=dfa.final_states,
        )
        visual_dfa.show_diagram(filename="DFA")
        print("DFA graph is saved in DFA.png file.")

        print("You can now input strings to see if the DFA accepts them:")
        while True:
            print("> ")
            input_str = input()
            if dfa.accepts(input_str):
                print(f"Accepted '{input_str}'")
            else:
                print(f"Rejected '{input_str}'")
    elif cfl.is_cfg(input_grammar):
        # print Greibach normal form
        # visualize PDA
        pass


if __name__ == "__main__":
    main()
