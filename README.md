# pokercfr

A CFR (Counterfactual Regret Minimization) poker research project. We implement
and study equilibrium-finding algorithms — vanilla CFR, CFR+, and Deep CFR —
on Kuhn Poker and Leduc Hold'em, measure their exploitability and convergence,
and compare the resulting strategies against baselines and published
poker-theory results (Pluribus, historical hand data).

## Why this project

CFR-family algorithms are the backbone of every strong computer poker agent to
date, from Libratus to Pluribus. This project reproduces that line of work at
small scale — games simple enough to solve exactly and reason about by hand —
so results can be checked against closed-form/published equilibria instead of
taken on faith, then extended toward the harder questions (multiplayer play,
exploiting weak opponents, scaling to bigger trees with function
approximation).

## Games and algorithms

| | Kuhn Poker | Leduc Hold'em |
|---|---|---|
| Size | 3-card deck, 1 betting round, tiny tree (closed-form Nash known) | 6-card deck (2 suits × 3 ranks), 2 betting rounds, public card, much larger tree |
| Vanilla CFR | ✅ planned | ✅ planned |
| CFR+ | ✅ planned | ✅ planned |
| Deep CFR | — | ✅ planned |

**Vanilla CFR** ([Zinkevich et al., 2007](https://papers.nips.cc/paper/2007)) —
regret matching at every information set, self-play traversal of the full game
tree, average strategy converges to a Nash equilibrium.

**CFR+** ([Tammelin, 2014](https://arxiv.org/abs/1407.5042)) — regret-matching+
(negative regrets clamped to zero) with linear averaging; converges
dramatically faster in practice than vanilla CFR.

**Deep CFR** ([Brown et al., 2019](https://arxiv.org/abs/1811.00164)) — replaces
tabular regret/strategy storage with neural network function approximators
trained on a reservoir-sampled replay buffer, so it scales to game trees too
large to enumerate.

We also look at multiplayer dynamics (à la
[Pluribus](https://www.science.org/doi/10.1126/science.aay2400)) and the
equilibrium-vs-exploitation trade-off: computing a Nash strategy is not the
same as maximally exploiting a specific weak opponent.

## Repository layout

```
pokercfr/
├── kuhn_poker/          # Kuhn Poker environment (game tree, info sets, payoffs)
│   ├── __init__.py
│   └── env.py
├── tests/                # unit tests
│   └── test_kuhn_poker.py
├── CONTRIBUTING.md        # branch/commit/PR conventions
└── README.md
```

More packages (`leduc/`, `cfr/`, `deep_cfr/`, `eval/`) land as their
corresponding issues are implemented — see [Roadmap](#roadmap) below.

## Setup

Requires Python 3.10+ (uses `X | None` type hints and `list[str]`). No
third-party dependencies yet — everything so far is standard library.

```bash
git clone https://github.com/Samanyu-dev/pokercfr.git
cd pokercfr
```

## Quickstart

```python
from kuhn_poker.env import Card, KuhnPokerState, deal

# Deterministic chance node — same seed always deals the same two cards.
state = deal(seed=42)
state.cards                    # e.g. (Card.KING, Card.JACK)

# Play out a hand: player 0 checks, player 1 bets, player 0 calls.
state = state.apply_action("p")
state = state.apply_action("b")
state.legal_actions()          # ['p', 'b'] -> fold or call, facing a bet
state = state.apply_action("b")

state.is_terminal()            # True  (history "pbb")
state.utility(0), state.utility(1)  # zero-sum payoff, e.g. (2, -2)

state.information_set_key(0)   # e.g. "Kpb" — card + full public history,
                                # the key a CFR training loop looks up regrets by
```

Actions use the standard CFR-literature convention: `'p'` means check (no bet
outstanding) or fold (facing a bet); `'b'` means bet or call. See
`kuhn_poker/env.py` for the full terminal-history/payoff table.

## Running tests

```bash
python3 -m unittest discover -s tests -v
```

## Roadmap

Tracked as GitHub issues, grouped by epic. Rough dependency order. See
[`EXPANSION.md`](EXPANSION.md) for the planned algorithm/condition-axis
study ([#46](https://github.com/Samanyu-dev/pokercfr/issues/46),
[#47](https://github.com/Samanyu-dev/pokercfr/issues/47)) and gated/backlog
stretch work beyond the milestones below.

**M1 — Tabular CFR pipeline for Kuhn Poker** ([#1](https://github.com/Samanyu-dev/pokercfr/issues/1))
- [x] Kuhn Poker game tree + information sets ([#19](https://github.com/Samanyu-dev/pokercfr/issues/19), [#3](https://github.com/Samanyu-dev/pokercfr/issues/3))
- [ ] Vanilla CFR training loop ([#20](https://github.com/Samanyu-dev/pokercfr/issues/20), [#4](https://github.com/Samanyu-dev/pokercfr/issues/4))
- [ ] Exploitability / best-response calculator ([#22](https://github.com/Samanyu-dev/pokercfr/issues/22), [#5](https://github.com/Samanyu-dev/pokercfr/issues/5))
- [ ] Unit tests against closed-form Kuhn equilibrium ([#21](https://github.com/Samanyu-dev/pokercfr/issues/21))

**M2 — CFR+ and Leduc scaling study** ([#6](https://github.com/Samanyu-dev/pokercfr/issues/6))
- [ ] Leduc Hold'em environment ([#8](https://github.com/Samanyu-dev/pokercfr/issues/8))
- [ ] CFR+ / regret-matching+ ([#7](https://github.com/Samanyu-dev/pokercfr/issues/7))
- [ ] Convergence plots, CFR vs CFR+ ([#26](https://github.com/Samanyu-dev/pokercfr/issues/26))

**M3 — Deep CFR extension** ([#10](https://github.com/Samanyu-dev/pokercfr/issues/10))
- [ ] Replay buffer + advantage/strategy networks ([#28](https://github.com/Samanyu-dev/pokercfr/issues/28))
- [ ] Hyperparameter sweep for stability ([#29](https://github.com/Samanyu-dev/pokercfr/issues/29))
- [ ] Baseline agents + bluff/bet-sizing analysis vs. published hands ([#30](https://github.com/Samanyu-dev/pokercfr/issues/30), [#31](https://github.com/Samanyu-dev/pokercfr/issues/31))

**M4 — Robustness and scaling study** ([#33](https://github.com/Samanyu-dev/pokercfr/issues/33))
- [ ] Multi-seed variance on all headline results ([#34](https://github.com/Samanyu-dev/pokercfr/issues/34))
- [ ] Ablations, fresh-clone reproducibility check ([#35](https://github.com/Samanyu-dev/pokercfr/issues/35), [#36](https://github.com/Samanyu-dev/pokercfr/issues/36))

**Also tracked, not yet scheduled to a milestone above:** abstract Game/State
interface ([#15](https://github.com/Samanyu-dev/pokercfr/issues/15)), CI
pipeline ([#16](https://github.com/Samanyu-dev/pokercfr/issues/16)), config /
seeding system ([#17](https://github.com/Samanyu-dev/pokercfr/issues/17)),
3-player Kuhn extension ([#27](https://github.com/Samanyu-dev/pokercfr/issues/27)),
exploiting a fixed suboptimal opponent ([#32](https://github.com/Samanyu-dev/pokercfr/issues/32)),
literature review ([#23](https://github.com/Samanyu-dev/pokercfr/issues/23)).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for branch naming, commit message
style, and PR review expectations.

## References

- Zinkevich, Johanson, Bowling, Piccione. [Regret Minimization in Games with Incomplete Information](https://papers.nips.cc/paper/2007). NeurIPS 2007.
- Tammelin. [Solving Large Imperfect Information Games Using CFR+](https://arxiv.org/abs/1407.5042). 2014.
- Brown, Lerer, Gross, Sandholm. [Deep Counterfactual Regret Minimization](https://arxiv.org/abs/1811.00164). ICML 2019.
- Brown, Sandholm. [Superhuman AI for multiplayer poker](https://www.science.org/doi/10.1126/science.aay2400). Science, 2019.
