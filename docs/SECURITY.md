# Security Policy

## Scope

The skill runs locally, using only bash and the Python 3 standard library. It makes no network calls, needs no credentials and sends no telemetry. The only command that touches the network is the `git clone` used to install it.

Security issues in scope include scripts that run unexpected commands, write outside the target project, or read or leak local data.

## Supported versions

Only the latest published version (the most recent tag) receives fixes.

| Version         | Supported |
| --------------- | --------- |
| Latest release  | Yes       |
| Older releases  | No        |

## Reporting a vulnerability

Please do not open a public issue. Report it privately through a Private Security Advisory:

https://github.com/adejaimejr/ai-project-structure/security/advisories/new

Include the skill version, the operating system, the steps to reproduce and the impact you see.
