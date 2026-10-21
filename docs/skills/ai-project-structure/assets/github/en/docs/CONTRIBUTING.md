# Contributing

Thanks for helping. This file explains how to propose a change to the project.

## Languages

- The GitHub layer (README, this file, `SECURITY.md`, the code of conduct, issue and PR templates, workflows and releases) is written in English.
- `AGENTS.md`, `docs/` and the project memory follow the language set in `AGENTS.md`.

## Gates

Run the commands listed in the "Testes E Validacao" section of `docs/QUALITY.md` before you open a pull request. That section is the single definition of "passes" for this project, and CI runs the same commands.

CI also validates the Markdown structure of the project (`AGENTS.md` and `docs/`) in strict mode.

## No em dash

The em dash character (U+2014) is forbidden in Markdown files. Use a colon, comma, semicolon, parentheses or a plain hyphen instead.

## Commits

Follow the commit format recorded in `AGENTS.md`. Cite the task as `(T-NNN)` when there is one.

## Pull requests

- A code change goes into `main` through a pull request with the `ci` check green.
- Never force push to `main` and never delete it.
- Fill in the pull request template: what changed, why, and how you verified it.

## Releases

A version bump needs all of these:

1. Update the version and the CHANGELOG section.
2. Create an annotated tag `vX.Y.Z` on the bump commit: `git tag -a vX.Y.Z`.
3. Push the tag: `git push origin vX.Y.Z`.
4. Publish a GitHub Release for the tag.

A tag without a bump, or a bump without a tag, is an error.

## Repository settings

Repository settings (description, topics, rulesets, labels) are done with the `gh` CLI, never by an agent on its own. The checklist is in `references/github.md` of the structure skill.

## Where things are recorded

Project rules live in `AGENTS.md`. Work is recorded in `docs/TASKS.md`, `docs/SESSION.md`, `docs/DECISIONS.md` and `docs/CHANGELOG.md`; see `AGENTS.md` for what goes where.
