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


def is_rg(g: Grammar) -> bool:
    return is_rlg(g) or is_llg(g)


def is_rlg(g: Grammar) -> bool:
    # left side most consist only of one nonterminal
    if not all(len(left_side) == 1 and left_side in g.nonterminals for left_side, _ in g.rules):
        return False
    return all(
        set(right_side).issubset(g.terminals) or
        (right_side[-1] in g.nonterminals and set(right_side[:-1]).issubset(g.terminals))
        for _, right_side in g.rules
    )


def is_llg(g: Grammar) -> bool:
    if not all(len(left_side) == 1 and left_side in g.nonterminals for left_side, _ in g.rules):
        return False
    return all(
        set(right_side).issubset(g.terminals) or
        (right_side[1] in g.nonterminals and set(right_side[1:]).issubset(g.terminals))
        for _, right_side in g.rules
    )


def is_cfg(g: Grammar) -> bool:
    return all(left_side in g.nonterminals for left_side, _ in g.rules)
