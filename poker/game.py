"""Configurable one-round poker: Kuhn generalized along deck size, cards dealt,
and player count, so every rung of the game-size ladder is one config.

Rules (N-player Kuhn, Abou Risk & Szafron 2010): everyone antes 1. Players act
in seat order with 'p' (check) / 'b' (bet 1). Once someone bets, each other
player responds exactly once, in order after the bettor: 'p' fold / 'b' call.
No raises. Showdown among players still in; ties split the pot.

Hand strength (no community cards): pairs/trips/quads and two pair beat high
cards, compared by rank-count pattern then ranks.
# ponytail: no straights/flushes — add when a rung deals 5 cards
"""
from __future__ import annotations

import itertools
import math
import random
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

RANK_NAMES = "23456789TJQKA"
SUIT_NAMES = "shdc"


@dataclass(frozen=True)
class GameConfig:
    ranks: int = 3  # 3 -> J Q K (Kuhn), 4 -> J Q K A, more extend downward: 6 -> 9 T J Q K A
    suits: int = 1
    cards_dealt: int = 1
    players: int = 2

    @property
    def deck(self) -> list[int]:
        """Cards as ints: rank * suits + suit."""
        return list(range(self.ranks * self.suits))

    def card_name(self, card: int) -> str:
        names = "JQKA"[: self.ranks] if self.ranks <= 4 else RANK_NAMES[-self.ranks:]
        rank = names[card // self.suits]
        return rank + (SUIT_NAMES[card % self.suits] if self.suits > 1 else "")

    def num_deals(self) -> int:
        n, k = len(self.deck), self.cards_dealt
        return math.perm(n, k * self.players) // math.factorial(k) ** self.players

    def num_info_sets(self) -> int:
        return math.comb(len(self.deck), self.cards_dealt) * len(_decision_histories(self.players))


KUHN = GameConfig()

# The game-size ladder, smallest first. Sizes: `python -m poker.game`.
LADDER = {
    "kuhn": KUHN,
    "4rank": GameConfig(ranks=4),
    "4rank-2dealt": GameConfig(ranks=4, cards_dealt=2),
    "4rank-2suit": GameConfig(ranks=4, suits=2),
    "4rank-2suit-2dealt": GameConfig(ranks=4, suits=2, cards_dealt=2),
    "kuhn-3p": GameConfig(players=3, ranks=4),
    "4rank-2suit-3p": GameConfig(ranks=4, suits=2, players=3),
    "4rank-2suit-2dealt-3p": GameConfig(ranks=4, suits=2, cards_dealt=2, players=3),
    "4rank-2suit-4p": GameConfig(ranks=4, suits=2, players=4),
    "6rank-4suit-2dealt-4p": GameConfig(ranks=6, suits=4, cards_dealt=2, players=4),
    "13rank-4suit-2dealt-2p": GameConfig(ranks=13, suits=4, cards_dealt=2),
}


def _hand_strength(cards: tuple[int, ...], suits: int) -> tuple:
    counts = Counter(c // suits for c in cards)
    groups = sorted(counts.items(), key=lambda rc: (rc[1], rc[0]), reverse=True)
    return tuple(c for _, c in groups), tuple(r for r, _ in groups)


def _decision_histories(players: int) -> list[str]:
    """Every non-terminal betting history."""
    out, frontier = [], [""]
    while frontier:
        h = frontier.pop()
        if PokerState(GameConfig(players=players), ((),) * players, h).is_terminal():
            continue
        out.append(h)
        frontier += [h + "p", h + "b"]
    return out


@dataclass(frozen=True)
class PokerState:
    config: GameConfig
    hands: tuple[tuple[int, ...], ...]
    history: str = ""

    def _bet_index(self) -> int:
        return self.history.find("b")

    def current_player(self) -> int:
        return len(self.history) % self.config.players  # seats act in strict rotation

    def legal_actions(self) -> list[str]:
        return [] if self.is_terminal() else ["p", "b"]

    def apply_action(self, action: str) -> PokerState:
        if self.is_terminal():
            raise ValueError("apply_action() called on a terminal state")
        if action not in ("p", "b"):
            raise ValueError(f"illegal action: {action!r}")
        return PokerState(self.config, self.hands, self.history + action)

    def is_terminal(self) -> bool:
        n, i = self.config.players, self._bet_index()
        if i < 0:
            return len(self.history) == n
        return len(self.history) - i - 1 == n - 1

    def utilities(self) -> list[float]:
        if not self.is_terminal():
            raise ValueError("utilities() called on a non-terminal state")
        n, h, i = self.config.players, self.history, self._bet_index()
        contrib = [1] * n
        if i < 0:
            live = list(range(n))
        else:
            live = [i % n]
            contrib[i % n] += 1
            for offset, a in enumerate(h[i + 1:], start=1):
                if a == "b":
                    p = (i + offset) % n
                    live.append(p)
                    contrib[p] += 1
        strength = {p: _hand_strength(self.hands[p], self.config.suits) for p in live}
        best = max(strength.values())
        winners = [p for p in live if strength[p] == best]
        pot = sum(contrib)
        return [(pot / len(winners) if p in winners else 0) - contrib[p] for p in range(n)]

    def utility(self, player: int) -> float:
        return self.utilities()[player]

    def information_set_key(self, player: int) -> str:
        cards = "".join(self.config.card_name(c) for c in sorted(self.hands[player], reverse=True))
        return f"{cards}{self.history}"


def deal_outcomes(config: GameConfig = KUHN) -> list[tuple[PokerState, Fraction]]:
    """Every deal (ordered by seat, unordered within a hand) at exact probability."""
    k = config.cards_dealt

    def deals(remaining: frozenset[int], seats: int):
        if seats == 0:
            yield ()
            return
        for hand in itertools.combinations(sorted(remaining), k):
            for rest in deals(remaining - set(hand), seats - 1):
                yield (hand, *rest)

    all_deals = list(deals(frozenset(config.deck), config.players))
    prob = Fraction(1, len(all_deals))
    return [(PokerState(config, d), prob) for d in all_deals]


def sample_deal(config: GameConfig, rng: random.Random) -> PokerState:
    cards = rng.sample(config.deck, config.cards_dealt * config.players)
    k = config.cards_dealt
    return PokerState(config, tuple(tuple(cards[p * k:(p + 1) * k]) for p in range(config.players)))


if __name__ == "__main__":
    print(f"{'rung':26} {'players':>7} {'info sets':>12} {'deals':>16}")
    for name, cfg in LADDER.items():
        print(f"{name:26} {cfg.players:>7} {cfg.num_info_sets():>12,} {cfg.num_deals():>16,}")
