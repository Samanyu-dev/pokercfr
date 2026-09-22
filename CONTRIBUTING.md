# Contributing

This repo backs a course project, so commit history is graded for accountability —
follow these conventions so contributions are traceable to issues and reviewable.

## Branch naming

`<type>/<issue-number>-<short-description>`, all lowercase, words hyphenated.

- `type` is one of: `feat`, `fix`, `test`, `docs`, `infra`, `research`
- Examples: `feat/19-kuhn-poker-env`, `docs/18-contributing-guide`, `fix/24-leduc-showdown-ties`

Branch off `main`. One issue per branch.

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/) style:

```
<type>: <short summary>

<optional body explaining why, not what>
```

- Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`
- Reference the issue in the body or footer (`Refs #19`) when the commit addresses one
- Summary in imperative mood ("add", not "added"), under 72 chars

## Pull requests

- One issue per PR. Title mirrors the branch's intent.
- Description must state: what changed, why, and how it was verified (test output,
  example run, plot, etc.)
- Link the issue it closes (`Closes #19`)
- Every PR gets at least a self-review comment before merge — call out any known
  gaps or follow-up issues filed
- **Request review from `@Samanyu-dev` or `@mrlegendary25` and get an approval
  before merging.** This is enforced by branch protection on `main` — a PR
  can't be merged without at least one approving review from a code owner.
- Squash-merge into `main` once approved, keeping the PR title as the merge commit
  summary

## Full workflow

1. Pick up (or get assigned) an issue. If the work doesn't map to an existing
   issue, open one first — no unowned or untracked work.
2. Branch off `main` using the naming convention above.
3. Implement, with a test per non-trivial piece of logic (see existing
   `tests/` for the pattern — plain `unittest`/`pytest`, no framework beyond
   that unless a task genuinely needs one).
4. Open a PR against `main`: description states what/why/how-verified, links
   `Closes #N`, includes a short self-review comment.
5. Request review from `@Samanyu-dev` or `@mrlegendary25`. Address feedback.
6. Once approved, squash-merge. Don't delete the branch (kept for the
   course's commit-history accountability record).

## Team and ownership

Work is split into three tracks (mirrors the project's own architecture: an
environment layer, an algorithm layer, and an evaluation layer):

| Track | Owners | Scope |
|---|---|---|
| **Game engine & abstraction** | [@Aarush-Kanipakam](https://github.com/Aarush-Kanipakam), [@SaiAashishJ](https://github.com/SaiAashishJ) | Kuhn/Leduc environments, the shared Game/State interface, environment unit tests, reproducibility/config, 3-player extension |
| **CFR engine** | [@mrlegendary25](https://github.com/mrlegendary25), Vik217 (pending invite) | Vanilla CFR, CFR+, Deep CFR (networks, replay buffer, hyperparameter sweep, ablations), exploitation-of-a-fixed-opponent study |
| **Evaluation & process** | [@Samanyu-dev](https://github.com/Samanyu-dev), hippiegeneral (pending invite) | Exploitability/best-response, baselines, plotting, bluff/bet-size analysis, multi-seed rigor, reproducibility checks, proposal/ethics/scope writeup |

`@Samanyu-dev` and `@mrlegendary25` are the two required reviewers (see
Pull requests above) and also track owners — review load is split the same
way work is: each mainly reviews PRs adjacent to their own track, but either
can review any PR.

Issues are assigned on GitHub per this table. `Vik217` and `hippiegeneral`
have pending repo invites — they'll be added as GitHub assignees on their
existing issues once they accept; ownership is already final per this table.
