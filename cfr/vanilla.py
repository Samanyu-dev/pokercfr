"""Vanilla CFR (Zinkevich et al., 2007): full-tree traversal with simultaneous
updates, regret matching at every information set, reach-weighted strategy
averaging. The *average* strategy is what converges to Nash in 2-player
zero-sum games; for 3+ players there is no such guarantee (that gap is part
of what the ladder measures).

Works with any state exposing current_player / legal_actions / apply_action /
is_terminal / utilities / information_set_key, plus a chance enumeration
returning [(state, probability), ...].
"""
from __future__ import annotations

import math
from collections import defaultdict


def _regret_matching(regrets: dict[str, float], actions: list[str]) -> dict[str, float]:
    positive = {a: max(regrets[a], 0.0) for a in actions}
    total = sum(positive.values())
    if total > 0:
        return {a: positive[a] / total for a in actions}
    return {a: 1.0 / len(actions) for a in actions}


class VanillaCFR:
    def __init__(self, outcomes):
        # ponytail: float probs, not Fraction — exact arithmetic would blow up over many iterations
        self.outcomes = [(s, float(p)) for s, p in outcomes]
        self.players = len(self.outcomes[0][0].hands)
        self.regret_sum: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.strategy_sum: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.iterations = 0

    def train(self, iterations: int) -> None:
        for _ in range(iterations):
            for state, p in self.outcomes:
                self._cfr(state, [1.0] * self.players, p)
            self.iterations += 1

    def _cfr(self, state, reach: list[float], chance_reach: float) -> list[float]:
        """Returns the expected utility vector (one entry per player) from `state`."""
        if state.is_terminal():
            return state.utilities()

        player = state.current_player()
        actions = state.legal_actions()
        key = state.information_set_key(player)
        strategy = _regret_matching(self.regret_sum[key], actions)

        action_values = {}
        for a in actions:
            child_reach = reach.copy()
            child_reach[player] *= strategy[a]
            action_values[a] = self._cfr(state.apply_action(a), child_reach, chance_reach)
        node_value = [sum(strategy[a] * action_values[a][i] for a in actions) for i in range(self.players)]

        opp_reach = chance_reach * math.prod(r for i, r in enumerate(reach) if i != player)
        for a in actions:
            self.regret_sum[key][a] += opp_reach * (action_values[a][player] - node_value[player])
            self.strategy_sum[key][a] += reach[player] * strategy[a]
        return node_value

    def average_strategy(self) -> dict[str, dict[str, float]]:
        avg = {}
        for key, sums in self.strategy_sum.items():
            total = sum(sums.values())
            avg[key] = {a: s / total for a, s in sums.items()} if total > 0 else {
                a: 1.0 / len(sums) for a in sums
            }
        return avg


def expected_values(policy: dict[str, dict[str, float]], outcomes) -> list[float]:
    """Each player's expected payoff when everyone follows `policy`."""

    def walk(state) -> list[float]:
        if state.is_terminal():
            return state.utilities()
        probs = policy[state.information_set_key(state.current_player())]
        children = [(probs[a], walk(state.apply_action(a))) for a in state.legal_actions()]
        return [sum(p * v[i] for p, v in children) for i in range(len(children[0][1]))]

    total = None
    for state, p in outcomes:
        v = walk(state)
        total = [float(p) * x for x in v] if total is None else [t + float(p) * x for t, x in zip(total, v)]
    return total
