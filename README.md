[Leia em portugues](README.pt-BR.md)

# AI Project Structure

A multi-agent Markdown structure for projects touched by several AIs, plus an installable skill that creates it in any project.

[![Release](https://img.shields.io/github/v/release/adejaimejr/ai-project-structure)](https://github.com/adejaimejr/ai-project-structure/releases/latest) [![CI](https://github.com/adejaimejr/ai-project-structure/actions/workflows/ci.yml/badge.svg)](https://github.com/adejaimejr/ai-project-structure/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/adejaimejr/ai-project-structure)](LICENSE)

## Why

The structure answers one question: **what does the next model need to know so it does not repeat the previous one's work?**

- One source of rules (`AGENTS.md`) works for Claude Code, Codex CLI and Gemini CLI. No three-way drift.
- Project memory lives in plain Markdown in `docs/`, split by function: what happened, what was learned, what was decided, what is open.
- When context is missing, the agent asks. It never fills the gap with a plausible guess.

## Supported tools

The skill follows the Agent Skills Open Standard: one `SKILL.md`, installed in three places.

| Tool | Global install path | Per-project path | Entry file |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `<repo>/.claude/skills/` | `CLAUDE.md` (imports `AGENTS.md`) |
| Codex CLI | `~/.agents/skills/` | `<repo>/.agents/skills/` | `AGENTS.md` directly |
| Gemini CLI | `~/.gemini/skills/` | `<repo>/.gemini/skills/` | `GEMINI.md` (imports `AGENTS.md`) |

## Quick start

You need bash and Python 3 (standard library only).

```bash
git clone https://github.com/adejaimejr/ai-project-structure.git
cd ai-project-structure/docs/skills/ai-project-structure
./install.sh
```

Then, in any project, ask your agent in Portuguese (the skill is written in pt-BR):

> Cria a estrutura multiagente aqui

The skill runs a short interview with numbered options (answering "1 2 3" is enough) and creates the files. It never runs `git init` and never overwrites anything without asking.

Validate a project:

```bash
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <project>
```

Add `--strict` to make warnings fail, or `--progress` for a read-only view of tasks and specs.

## How it works

`AGENTS.md` holds the rules. `CLAUDE.md` and `GEMINI.md` are immutable bridges that point to it. Memory is split by function:

| File in `docs/` | Function |
| --- | --- |
| `PROJECT_CONTEXT.md` | What the project **is** |
| `SESSION.md` | What **happened**, in order, for continuity between sessions |
| `MEMORY.md` | What the project **learned** |
| `DECISIONS.md` | What was formally **decided** |
| `TASKS.md` | What is **open**: IDs `T-NNN`, the single source of status |
| `CONSENSUS.md` | Debate between models, with status and a tie-break rule |
| `STACK.md` | What the project is **built with** and where to read about it |
| `specs/` | What **will be built** (optional module, one light spec per feature) |

Operating rules: update only the file whose function was triggered, two reading depths (trivial or relevant change), rotation into `docs/archive/`, and evidence required to close a task.

## Docs

The skill, the generated structure and the project memory in `docs/` are in Brazilian Portuguese. This README, the contributing guide and the GitHub layer are in English.

For users:

| Document | What it covers |
| --- | --- |
| [Skill README](docs/skills/ai-project-structure/README.md) | Install flags, paths, validator, repository verifier |
| [Skill CHANGELOG](docs/skills/ai-project-structure/CHANGELOG.md) | Version history of the skill |
| [SECURITY](docs/SECURITY.md) | Scope, supported versions, how to report |

For contributors:

| Document | What it covers |
| --- | --- |
| [CONTRIBUTING](docs/CONTRIBUTING.md) | Setup, gates, pull request flow |
| [AGENTS](AGENTS.md) | The rules every agent follows here |
| [QUALITY](docs/QUALITY.md) | Quality bar and checks |
| [DECISIONS](docs/DECISIONS.md) | Formal decisions, with reasons |
| [TASKS](docs/TASKS.md) | The live backlog |
| [SESSION](docs/SESSION.md) | Chronological log of agent sessions |
| [specs](docs/specs/) | Feature specs |

This repository uses the structure it ships (dogfood). The canonical skill source is [docs/skills/ai-project-structure/](docs/skills/ai-project-structure/).

## Inspirations

Skill v2 was inspired by [Specsfy](https://github.com/promovaweb/specsfy), a spec-driven method in pt-BR. We adapted its numbered interview, managed blocks, script validation and single-file specs, without the full ceremony. The comparison with [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) is what led to the GitHub layer of this repository; see [docs/DECISIONS.md](docs/DECISIONS.md).

## Security

Report vulnerabilities as described in [docs/SECURITY.md](docs/SECURITY.md).

## License

[MIT](LICENSE).
