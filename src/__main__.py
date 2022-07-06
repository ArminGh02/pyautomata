import json

# used only for visualizing DFA and NFA
from visual_automata.fa.nfa import VisualNFA
from visual_automata.fa.dfa import VisualDFA

import grammar
from grammar import Grammar
import pyautomata
import image


def main() -> None:
    with open("grammar_input.json", "r") as f:
        input_grammar = Grammar.from_dict(json.load(f))

    if grammar.is_rg(input_grammar):
        nfa = pyautomata.NFA.from_grammar(input_grammar)
        dfa = pyautomata.DFA.from_nfa(nfa)

        create_dfa_and_nfa_images(dfa, nfa)
        image.open("DFA.png")
        image.open("NFA.png")

        accept_strings(dfa)

    elif grammar.is_cfg(input_grammar):
        # TODO print Greibach normal form
        # TODO visualize PDA
        pass


def create_dfa_and_nfa_images(dfa: pyautomata.DFA, nfa: pyautomata.NFA) -> None:
    visual_nfa = VisualNFA(
        initial_state=nfa.initial_state,
        states=nfa.states,
        final_states=nfa.final_states,
        input_symbols=nfa.input_symbols,
        transitions=nfa.transitions,
    )
    visual_nfa.show_diagram(filename="NFA")
    print("NFA graph is saved in NFA.png file")

    visual_dfa = VisualDFA(
        states=dfa.states,
        input_symbols=dfa.input_symbols,
        transitions=dfa.transitions,
        initial_state=dfa.initial_state,
        final_states=dfa.final_states,
    )
    visual_dfa.show_diagram(filename="DFA")
    print("DFA graph is saved in DFA.png file.")


def accept_strings(automata: pyautomata.Automata) -> None:
    print("You can now input strings to see if the DFA accepts them: (type 'exit' to quit)")
    while True:
        input_str = input("> ")

        if input_str == "exit":
            break

        if automata.accepts(input_str):
            print(f"Accepted '{input_str}'")
        else:
            print(f"Rejected '{input_str}'")


if __name__ == "__main__":
    main()
