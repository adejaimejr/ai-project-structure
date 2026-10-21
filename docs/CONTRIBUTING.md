# Contributing

Thanks for helping. This project is a Markdown structure for AI agents plus a skill that creates and validates it.

## Languages

- English for the GitHub layer: the root README, this file, `SECURITY.md`, the code of conduct, issue and PR templates, workflows and releases.
- Portuguese (pt-BR) for `AGENTS.md`, `docs/`, the skill and everything it generates.

## Setup

```bash
git clone https://github.com/adejaimejr/ai-project-structure.git
cd ai-project-structure
```

You need bash and Python 3 with its standard library. There is nothing to install.

## Gates

Two checks must pass before a change is merged:

```bash
python3 docs/skills/ai-project-structure/evals/verify_repository.py
python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict
```

Expected output, in the last line of each:

```text
Resumo: 78/78 verificacoes passaram.
Resumo: 0 erros, 0 avisos.
```

CI runs both on Ubuntu and macOS. Scripts and fixtures must work on Linux, macOS and Windows (Git Bash).

## No em dash

The em dash character (U+2014) is forbidden in all Markdown files, including this one. The verifier flags every occurrence. Use a colon, comma, semicolon, parentheses or a plain hyphen instead.

## Commits

Format: `type: short subject in pt-BR`, where type is one of `feat`, `fix`, `docs`, `test` or `evals`. Cite the task as `(T-NNN)` when there is one.

A skill version bump uses `feat: skill X.Y.Z, <summary> (T-NNN)`, or `fix:` for a patch.

## Pull requests

- A change under `docs/skills/ai-project-structure/` (outside `evals/`) goes into `main` through a pull request with the `ci` check green.
- A change only in the root `docs/` may go straight to `main`.
- Never force push to `main` and never delete it.

## Releases

A skill version bump needs all of these:

1. Update `version` in `docs/skills/ai-project-structure/SKILL.md` and the version markers.
2. Add a `## X.Y.Z - YYYY-MM-DD` section to the skill CHANGELOG.
3. Create an annotated tag `vX.Y.Z` on the bump commit: `git tag -a vX.Y.Z`.
4. Push the tag: `git push origin vX.Y.Z`.

The release workflow publishes the GitHub Release from that CHANGELOG section. A tag without a bump, or a bump without a tag, is an error.

## Repository settings checklist

Repository settings are done with the `gh` CLI, never by the skill. The full checklist lives in `docs/skills/ai-project-structure/references/github.md`; the list below is the short version.

- Description and topics.
- Ruleset for `main`: block force push and deletion, require the `ci` check.
- Labels.
- Wiki and Projects turned off.

## Where things are recorded

Project rules live in `AGENTS.md`. Work is recorded in `docs/TASKS.md`, `docs/SESSION.md`, `docs/DECISIONS.md` and `docs/CHANGELOG.md`; see `AGENTS.md` for what goes where.
