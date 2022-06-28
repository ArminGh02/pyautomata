from typing import NamedTuple, Any


class Grammar(NamedTuple):
    rules: list[list[str]]
    nonterminals: set[str]
    terminals: set[str]
    start_symbol: str

    @staticmethod
    def from_dict(d: dict[str, Any]) -> 'Grammar':
        return Grammar(
            rules=list(map(lambda rule: rule.split("->"), d["rules"])),
            nonterminals=set(d["nonterminals"]),
            terminals=set(d["terminals"]),
            start_symbol=d["start_symbol"],
        )
