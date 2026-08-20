# AI Project Structure

Estrutura Markdown multiagente para projetos tocados por várias IAs, mais a skill instalável que cria essa estrutura em qualquer projeto novo. Uma única fonte funciona em **Claude Code**, **Codex CLI** e **Gemini CLI** (Agent Skills Open Standard).

A pergunta que a estrutura responde: **o que o próximo modelo precisa saber para não repetir o trabalho do anterior?**

## Como Funciona

- `AGENTS.md` é a fonte central de regras; `CLAUDE.md` e `GEMINI.md` são pontes imutáveis que apontam para ele.
- A memória do projeto vive em `docs/`, separada por função:

| Arquivo | Função |
| --- | --- |
| `PROJECT_CONTEXT.md` | O que o projeto **é** |
| `SESSION.md` | O que **aconteceu** (cronológico, continuidade entre sessões) |
| `MEMORY.md` | O que o projeto **aprendeu** (User / Feedback / Project / Reference) |
| `DECISIONS.md` | O que foi **decidido** formalmente |
| `TASKS.md` | O que está **em aberto** (IDs `T-NNN`, fonte única de status) |
| `CONSENSUS.md` | Debate entre modelos, com status e regra de desempate |
| `STACK.md` | Com o que o projeto é **construído** e onde consultar cada tecnologia |
| `specs/` | O que **será construído** (módulo opcional, uma spec leve por feature) |

- Regras operacionais: atualização por gatilho (só o arquivo cuja função foi acionada), dois níveis de leitura (trivial vs relevante), rotação para `docs/archive/`, e a regra **Nunca Inferir** (faltou contexto, o agente pergunta; nunca preenche por inferência).

## Instalação Da Skill

Requisitos: bash e Python 3 (somente biblioteca padrão).

```bash
git clone https://github.com/adejaimejr/ai-project-structure.git
cd ai-project-structure/docs/skills/ai-project-structure
./install.sh
```

Instala nas três ferramentas (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`). Flags: `--project`, `--claude`, `--codex`, `--gemini`, `--uninstall`. Detalhes em [docs/skills/ai-project-structure/README.md](docs/skills/ai-project-structure/README.md).

## Uso

A skill dispara por linguagem natural:

- "Inicia um projeto novo aqui chamado minha-loja, objetivo X. Estrutura minimal."
- "Atualiza este projeto para a versão mais nova da estrutura."
- "Valida a estrutura deste projeto."
- "Ativa o módulo de specs aqui."

Ela faz uma entrevista com perguntas e opções numeradas (responder "1 2 3" basta) e cria os arquivos de fato. Nunca inicializa git nem sobrescreve nada sem confirmação.

Validador e progresso:

```bash
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <projeto>
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <projeto> --progress
```

O modo padrão valida a estrutura com exit code (bom para gate); `--progress` mostra uma projeção somente-leitura de tarefas e specs.

## Este Repositório

O próprio repositório usa a estrutura que distribui (dogfood): as regras estão em [AGENTS.md](AGENTS.md), o histórico em [docs/SESSION.md](docs/SESSION.md) e [docs/CHANGELOG.md](docs/CHANGELOG.md), as specs reais em [docs/specs/](docs/specs/). A fonte canônica da skill fica em [docs/skills/ai-project-structure/](docs/skills/ai-project-structure/), com versão no frontmatter do `SKILL.md` e changelog próprio.

## Inspirações

A v2 da skill foi inspirada na análise do [Specsfy](https://github.com/promovaweb/specsfy) (metodologia SDD em pt-BR), de onde adaptamos entrevista numerada, blocos gerenciados, validação por script e specs de arquivo único, sem importar a cerimônia completa. O que foi importado e o que foi descartado está registrado em [docs/DECISIONS.md](docs/DECISIONS.md).

## Licença

[MIT](LICENSE).
