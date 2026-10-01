# Game-size ladder

Scope: start at Kuhn and climb to the biggest poker game our hardware can
solve — 6 laptops (M-series, 24 GB), Kaggle notebooks, AWS SageMaker. Each rung
reuses the same engine (`poker/`) and solvers (`cfr/`); a rung is a config,
not a new codebase. Every rung reports exploitability / NashConv, so moving up
is measured, not just claimed.

## Tier 1 — one betting round, configurable deck (`poker.LADDER`)

Measured with tabular vanilla CFR in pure Python, one M-series core
(`python -m poker.game` prints sizes).

| Rung | Players | Info sets | Deals | Time / CFR iteration |
|---|---|---|---|---|
| kuhn (J Q K) | 2 | 12 | 6 | 0.3 ms |
| 4rank (J Q K A) | 2 | 16 | 12 | 0.5 ms |
| 4rank-2dealt | 2 | 24 | 6 | 0.4 ms |
| 4rank-2suit | 2 | 32 | 56 | 2 ms |
| 4rank-2suit-2dealt | 2 | 112 | 420 | 16 ms |
| kuhn-3p | 3 | 48 | 24 | 3 ms |
| 4rank-2suit-3p | 3 | 96 | 336 | 37 ms |
| 4rank-2suit-2dealt-3p | 3 | 336 | 2,520 | 0.3 s |
| 4rank-2suit-4p | 4 | 256 | 1,680 | 0.5 s |
| 13rank-4suit-2dealt (full deck) | 2 | 5,304 | 1.6 M | ~65 s (projected) |
| 6rank-4suit-2dealt-4p | 4 | 8,832 | 1.9 B | ~7 days (projected) |

Takeaway: with one betting round the number of info sets stays tiny even with
a full deck. Cost comes from enumerating deals, and two fixes remove it:
chance-sampled MCCFR (#46), and vectorizing over hands with numpy. Tier 1 runs
entirely on laptops.

## Tier 2 — multiple rounds + public cards

Game size really grows with betting rounds, raises, and community cards. Next
rungs: Leduc (#8), then Leduc at N = 3..6 players (#50/#51), then larger decks
and raise caps. Still tabular; needs MCCFR plus a compiled inner loop (numba)
to stay under a day per run.

## Tier 3 — the top rung: Heads-up Limit Texas Hold'em, abstracted

HULHE has ~3.2×10¹⁴ info sets. Solving it exactly took 900 core-years
(Bowling et al. 2015), so we won't. The feasible top rung is:

- **Card abstraction + MCCFR**: bucket hands down to ~10⁷–10⁸ info sets, which
  fits in 24 GB. Report exploitability inside the abstraction plus head-to-head
  results.
- **Deep CFR on GPU (Kaggle)**: no abstraction table at all, so it's the natural
  fit for this size (#28).

Not feasible: 6-player no-limit à la Pluribus. Its blueprint used ~12,400
core-hours in optimized C++ and up to 512 GB RAM on one machine, and our
laptops can't pool memory.

## How the hardware gets used

- **Laptops**: one independent run per machine (a rung × algorithm × seed cell
  of the results matrix). We don't attempt a distributed solve; CFR tables need
  shared memory.
- **Kaggle**: GPU runs for Deep CFR. Sessions cap at 12 h, so training must
  checkpoint and resume.
- **AWS**: only for a run that needs more RAM than 24 GB (large abstractions).
  It's billed, so price the instance before launching.
