# Expansion plan

This is a planning document, not a commitment to build everything listed here.
Every item stays inside the boundary set by #43 (Research track, Kuhn/Leduc
only, no new games, no live bot/UI) — expansion means more rigor on the games
we already have, not broader scope.

## Player-count axis (committed — tracked as issues)

Considered and rejected: full Texas Hold'em, as a "go bigger" move — this is
the exact thing #43 (and the professor's feedback it quotes) scoped out, so
reopening it would just re-trigger that concern. A "4-card game" variant was
also floated and dropped without further scoping.

Instead: **multiplayer Leduc**, N = 2..6 players. This is the axis that
actually made Pluribus notable — its headline result was 6-player Hold'em,
and the significance wasn't the bigger deck, it was the player count. CFR's
Nash-equilibrium convergence guarantee is only *proven* for 2-player
zero-sum games; at 3+ players there's no such proof, yet Pluribus worked
anyway. This project measures exactly where and how badly that theoretical
gap shows up — on a game small enough to also compute an exact best response
at every player count, which is impossible for real Hold'em.

Still Leduc, just parameterized by seat count (same precedent as OpenSpiel's
own Leduc implementation) — reuses the existing engine, CFR/CFR+/DCFR
algorithms, and exploitability harness, so it doesn't reopen the "new game"
scope conversation.

- Risk & Szafron. *Using Counterfactual Regret Minimization to Create Competitive Multiplayer Poker Agents*. AAMAS 2010.
- *Successful Nash Equilibrium Agent for a 3-Player Imperfect-Information Game*.
- Bowling et al. *Heads-up Limit Hold'em Poker is Solved*. Science, 2015 — cited only as an external data point (900 core-years, 3.19×10¹⁴ information sets) to put our measured small-scale growth rate in context, not something we attempt to reproduce.

Issues: #50 (generalize the Leduc environment to N players), #51 (the
scaling study itself — NashConv vs. player count, compute-to-convergence
growth curve). Related, already-tracked, simpler precedent: #27 (Kuhn at 3
players specifically).

## Core study (committed — tracked as issues)

One experiment design, cut into two issues for ticket-tracking, but run as a
single results matrix: every algorithm variant × every condition, reporting
exploitability-vs-iterations *and* exploitability-vs-wall-clock for each cell.

- **Algorithm axis** — Monte Carlo CFR (outcome sampling) and Discounted CFR
  (DCFR), alongside the vanilla CFR / CFR+ already planned.
- **Condition axis** — Leduc bet-sizing/raise-cap sensitivity, and
  compute-budget (wall-clock vs. iteration count) trade-offs across all
  algorithms.

Nobody builds a second harness for this — it's the same environment and
training loop, swap the update rule / raise-cap config and re-run.

Issues: see tracker, cross-linked to each other and to #8 (Leduc env needs a
configurable raise cap) and #26 (convergence plots this extends).

## Embedded, not a separate issue

**Visualization** (regret trajectories, information-set strategy heatmaps —
e.g. watching Kuhn's bluffing frequency settle toward its known equilibrium
value over iterations) is the instrument the core study is read with, not an
independent deliverable. It's a required acceptance-criterion of the core
study issues, and grows into the final report (#13) alongside the
experiments — not bolted on after.

## Gated stretch (do not start yet)

**Robust counter-strategies / opponent modeling.** Generalizes #32
(exploit one fixed opponent) into a restricted-Nash-response solver: trace
the exploitation-vs-exploitability frontier by sweeping how far a strategy is
allowed to deviate from equilibrium toward exploiting a modeled opponent
pool.

- Johanson, Zinkevich, Bowling. *Computing Robust Counter-Strategies*. NeurIPS 2007.
- *Safe Opponent Exploitation*. ACM EC 2012.
- *Safe Opponent-Exploitation Subgame Refinement*. NeurIPS 2022.

This needs real new state (a belief over opponent types, a fixed-opponent
pool, a restricted-Nash-response solver) — not an afternoon's extension.
**Gate:** only start once the core study's results matrix is actually
landing and there is verified, comfortable margin before the final
deadline. Note: the final deadline isn't recorded in the tracker yet — this
gate can't honestly be called "satisfied" until that's confirmed.

## Backlog — candidates, not yet issues

Cheap and reuse the existing harness, grouped by what kind of rigor they buy.
Pending a triage pass before any of these become tracked issues.

**Ground-truth / exact-solution**
- Sequence-form LP as a second, independent Nash oracle (Koller, Megiddo, von Stengel 1996) — verifies exploitability numbers two ways instead of one.
- Track convergence to Kuhn's known continuum of equilibria (parameterized by bluffing probability α ∈ [0, 1/3], Kuhn 1950) — does CFR lock onto one α or drift along the manifold?

**Algorithmic ablations**
- Isolate the local update rule alone: Regret Matching vs. RM+ vs. Hedge, holding the CFR decomposition fixed.
- Chance-sampled CFR as a third point between full vanilla CFR and full outcome-sampling MCCFR.
- DCFR hyperparameter (α, β, γ) sensitivity sweep, reported as a heatmap.
- Deep CFR as a deliberate overkill test on a game small enough to solve exactly — does function approximation cost anything here?

**Comparative game theory**
- CFR vs. Fictitious Self-Play (Heinrich, Lanctot, Silver, ICML 2015) — two
  distinct no-regret-adjacent dynamics, compare rate/stability. **Correction:**
  the paper's Nash-convergence guarantee applies to full-width fictitious
  play; the sampled/learned variant it introduces (FSP) is a distinct
  algorithm with its own, more limited theoretical treatment — don't claim
  both variants inherit the same guarantee without checking which one is
  actually being compared against CFR.
- Regret decomposition by information set — which decision points take longest to converge.

**Theory-practice gap**
- CFR+ empirically outruns its own unimproved O(1/√T) bound — plot both on log-log axes.
- Last-iterate vs. average-strategy convergence (current iterate can cycle even as the average converges).
- Simultaneous vs. alternating updates, isolated as its own ablation from CFR+'s regret-matching+ rule.
- Verify Brown & Sandholm's DCFR unification (AAAI 2019): does setting DCFR's parameters to the paper's stated values reproduce vanilla CFR's and CFR+'s measured curves?

**Libratus/Pluribus techniques**
- Regret-based pruning (Brown & Sandholm, NIPS 2015) — validate on a game small enough to check by brute force.
- Strategy-based warm-starting (Brown & Sandholm, AAAI 2016). **Caveat:**
  "warm-start Leduc from the exact Kuhn equilibrium" is an unvalidated idea,
  not a described method — the cited technique needs a strategy already
  defined on the *target* game. A Kuhn-to-Leduc information-set mapping
  would have to be designed and justified first; that's real design work,
  not a given.

**Closed as out of scope**
- Three-player Kuhn Poker (#27, closed) and a Limit Hold'em subset (#37,
  closed) — both new game variants, which #43 explicitly scoped out. The
  multiplayer research question is covered instead by #51 (multiplayer
  Leduc), which stays within the existing Leduc engine.

## Next step

Pick which backlog items (if any) are worth promoting to real tracked issues
— flag them and issues get created and assigned then, rather than ticketing
all ~15 up front.
