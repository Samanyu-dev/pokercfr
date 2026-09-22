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
- Squash-merge into `main` once approved, keeping the PR title as the merge commit
  summary
