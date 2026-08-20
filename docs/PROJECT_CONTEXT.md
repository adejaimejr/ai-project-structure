# PROJECT_CONTEXT

**Nome do projeto:** ai-project-structure

## Objetivo Do Projeto

Manter a estrutura Markdown multiagente (AGENTS.md + pontes + memoria em `docs/`) e a skill instalavel que replica essa estrutura em novos projetos. A skill segue o Agent Skills Open Standard e funciona em Claude Code, Codex CLI e Gemini CLI a partir de uma unica fonte.

## Publico Ou Usuario Final

- O mantenedor do projeto e os agentes de IA (Claude, Codex, Gemini) que trabalham nos projetos dele.
- Qualquer pessoa que instale a skill para criar projetos com memoria multiagente.

## Estado Atual

- Estrutura v1 validada por tri-consenso (Claude + Gemini + Codex) em 2026-04-25.
- Skill empacotada no Agent Skills Open Standard e instalada nas tres ferramentas em 2026-05-26.
- v2 desenvolvida em 2026-08-20, inspirada na analise da metodologia specsfy: entrevista numerada, regra "Nunca Inferir", IDs T-NNN, blocos gerenciados com versao, validador Python, modulo opcional de specs e proibicao de travessao.

## Preferencias

- Idioma padrao: portugues.
- Manter instrucoes de IA centralizadas em `AGENTS.md`.
- Manter historico de sessoes em `SESSION.md`.
- Registrar consenso entre modelos em `CONSENSUS.md` quando necessario.
- Templates sem acentos; docs vivos podem usar acentos.
- Nunca usar o caractere travessao (em dash, U+2014) em textos do projeto.

## Fora De Escopo

- Pipeline SDD completo estilo specsfy (multi-skills numeradas, gates pesados).
- Matematica de cobertura (minimo de N criterios/testes por requisito) e sistema de attestation.
- CLI propria ou TUI.
- Dividir a skill em multiplas skills.
- Inicializar git pelo scaffold.

## Restricoes

- Todo conteudo user-facing da skill em pt-BR.
- Uma unica skill com um unico `SKILL.md` (fluxos pesados em `references/`).
- Validador apenas com biblioteca padrao do Python 3.
- Nenhum arquivo do usuario e sobrescrito sem confirmacao explicita.

## Links Internos

- Regras de IA: `../AGENTS.md`
- Tarefas: `TASKS.md`
- Sessoes: `SESSION.md`
- Memoria persistente: `MEMORY.md`
- Decisoes: `DECISIONS.md`
- Qualidade: `QUALITY.md`
- Specs: `specs/`
- Fonte da skill: `skills/ai-project-structure/`
