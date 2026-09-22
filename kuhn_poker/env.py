"""2-player Kuhn Poker: 3-card deck, single ante, single betting round.

Actions are uniform pass/bet ('p'/'b'), matching the standard CFR literature
convention: 'p' means check (if no bet is outstanding) or fold (if one is),
'b' means bet (if no bet is outstanding) or call (if one is).

Terminal histories and payoffs (pot always split 1-for-1 ante, +1 per bet):
    pp   -> showdown, pot 2  (winner +1 / loser -1)
    bp   -> player 0 bet, player 1 folded (p0 +1 / p1 -1)
    bb   -> showdown, pot 4  (winner +2 / loser -2)
    pbp  -> player 0 checked, player 1 bet, player 0 folded (p1 +1 / p0 -1)
    pbb  -> showdown, pot 4  (winner +2 / loser -2)
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from enum import IntEnum
from fractions import Fraction

_TERMINAL_HISTORIES = {"pp", "bp", "bb", "pbp", "pbb"}


class Card(IntEnum):
    JACK = 0
    QUEEN = 1
    KING = 2


def deal(seed: int | None = None) -> "KuhnPokerState":
    """Deal 2 of the 3 cards to the 2 players. Deterministic given a seed."""
    rng = random.Random(seed)
    p0_card, p1_card = rng.sample(list(Card), 2)
    return KuhnPokerState(cards=(p0_card, p1_card))


def deal_outcomes() -> list[tuple["KuhnPokerState", Fraction]]:
    """Every chance outcome (ordered deal) with its probability, for exact
    full-tree traversal (e.g. vanilla CFR) instead of sampling one deal."""
    ordered_deals = list(itertools.permutations(Card, 2))
    prob = Fraction(1, len(ordered_deals))
    return [(KuhnPokerState(cards=cards), prob) for cards in ordered_deals]


@dataclass(frozen=True)
class KuhnPokerState:
    cards: tuple[Card, Card]
    history: str = ""

    def current_player(self) -> int:
        return len(self.history) % 2

    def legal_actions(self) -> list[str]:
        if self.is_terminal():
            return []
        return ["p", "b"]

    def apply_action(self, action: str) -> "KuhnPokerState":
        if self.is_terminal():
            raise ValueError(f"cannot apply action {action!r} to terminal history {self.history!r}")
        if action not in ("p", "b"):
            raise ValueError(f"illegal action: {action!r}")
        return KuhnPokerState(self.cards, self.history + action)

    def is_terminal(self) -> bool:
        return self.history in _TERMINAL_HISTORIES

    def utility(self, player: int) -> int:
        """Payoff for `player` (0 or 1) at a terminal state."""
        if not self.is_terminal():
            raise ValueError("utility() called on a non-terminal state")
        h = self.history
        winner = 0 if self.cards[0] > self.cards[1] else 1

        if h == "bp":
            return 1 if player == 0 else -1
        if h == "pbp":
            return 1 if player == 1 else -1
        pot = 1 if h == "pp" else 2
        return pot if player == winner else -pot

    def information_set_key(self, player: int) -> str:
        return f"{self.cards[player].name[0]}{self.history}"
