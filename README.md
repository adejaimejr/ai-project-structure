# AI Project Structure

Estrutura Markdown multiagente para projetos tocados por varias IAs, mais a skill instalavel que cria essa estrutura em qualquer projeto novo. Uma unica fonte funciona em **Claude Code**, **Codex CLI** e **Gemini CLI** (Agent Skills Open Standard).

A pergunta que a estrutura responde: **o que o proximo modelo precisa saber para nao repetir o trabalho do anterior?**

## Como Funciona

- `AGENTS.md` e a fonte central de regras; `CLAUDE.md` e `GEMINI.md` sao pontes imutaveis que apontam para ele.
- A memoria do projeto vive em `docs/`, separada por funcao:

| Arquivo | Funcao |
| --- | --- |
| `PROJECT_CONTEXT.md` | O que o projeto **e** |
| `SESSION.md` | O que **aconteceu** (cronologico, continuidade entre sessoes) |
| `MEMORY.md` | O que o projeto **aprendeu** (User / Feedback / Project / Reference) |
| `DECISIONS.md` | O que foi **decidido** formalmente |
| `TASKS.md` | O que esta **em aberto** (IDs `T-NNN`, fonte unica de status) |
| `CONSENSUS.md` | Debate entre modelos, com status e regra de desempate |
| `STACK.md` | Com o que o projeto e **construido** e onde consultar cada tecnologia |
| `specs/` | O que **sera construido** (modulo opcional, uma spec leve por feature) |

- Regras operacionais: atualizacao por gatilho (so o arquivo cuja funcao foi acionada), dois niveis de leitura (trivial vs relevante), rotacao para `docs/archive/`, e a regra **Nunca Inferir** (faltou contexto, o agente pergunta; nunca preenche por inferencia).

## Instalacao Da Skill

Requisitos: bash e Python 3 (somente biblioteca padrao).

```bash
git clone https://github.com/adejaimejr/ai-project-structure.git
cd ai-project-structure/docs/skills/ai-project-structure
./install.sh
```

Instala nas tres ferramentas (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`). Flags: `--project`, `--claude`, `--codex`, `--gemini`, `--uninstall`. Detalhes em [docs/skills/ai-project-structure/README.md](docs/skills/ai-project-structure/README.md).

## Uso

A skill dispara por linguagem natural:

- "Inicia um projeto novo aqui chamado minha-loja, objetivo X. Estrutura minimal."
- "Atualiza este projeto para a versao mais nova da estrutura."
- "Valida a estrutura deste projeto."
- "Ativa o modulo de specs aqui."

Ela faz uma entrevista com perguntas e opcoes numeradas (responder "1 2 3" basta) e cria os arquivos de fato. Nunca inicializa git nem sobrescreve nada sem confirmacao.

Validador e progresso:

```bash
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <projeto>
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <projeto> --progress
```

O modo padrao valida a estrutura com exit code (bom para gate); `--progress` mostra uma projecao somente-leitura de tarefas e specs.

## Este Repositorio

O proprio repositorio usa a estrutura que distribui (dogfood): as regras estao em [AGENTS.md](AGENTS.md), o historico em [docs/SESSION.md](docs/SESSION.md) e [docs/CHANGELOG.md](docs/CHANGELOG.md), as specs reais em [docs/specs/](docs/specs/). A fonte canonica da skill fica em [docs/skills/ai-project-structure/](docs/skills/ai-project-structure/), com versao no frontmatter do `SKILL.md` e changelog proprio.

## Inspiracoes

A v2 da skill foi inspirada na analise do [Specsfy](https://github.com/promovaweb/specsfy) (metodologia SDD em pt-BR), de onde adaptamos entrevista numerada, blocos gerenciados, validacao por script e specs de arquivo unico, sem importar a cerimonia completa. O que foi importado e o que foi descartado esta registrado em [docs/DECISIONS.md](docs/DECISIONS.md).

## Licenca

[MIT](LICENSE).
