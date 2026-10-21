[Read in English](README.md)

# AI Project Structure

Estrutura Markdown multiagente para projetos tocados por várias IAs, mais uma skill instalável que cria essa estrutura em qualquer projeto.

[![Release](https://img.shields.io/github/v/release/adejaimejr/ai-project-structure)](https://github.com/adejaimejr/ai-project-structure/releases/latest) [![CI](https://github.com/adejaimejr/ai-project-structure/actions/workflows/ci.yml/badge.svg)](https://github.com/adejaimejr/ai-project-structure/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/adejaimejr/ai-project-structure)](LICENSE)

## Por Quê

A estrutura responde uma pergunta: **o que o próximo modelo precisa saber para não repetir o trabalho do anterior?**

- Uma única fonte de regras (`AGENTS.md`) serve Claude Code, Codex CLI e Gemini CLI. Sem divergência entre três arquivos.
- A memória do projeto vive em Markdown simples em `docs/`, separada por função: o que aconteceu, o que foi aprendido, o que foi decidido, o que está em aberto.
- Quando falta contexto, o agente pergunta. Nunca preenche a lacuna com um palpite plausível.

## Ferramentas Suportadas

A skill segue o Agent Skills Open Standard: um único `SKILL.md`, instalado em três lugares.

| Ferramenta | Caminho global | Caminho por projeto | Arquivo de entrada |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `<repo>/.claude/skills/` | `CLAUDE.md` (importa `AGENTS.md`) |
| Codex CLI | `~/.agents/skills/` | `<repo>/.agents/skills/` | `AGENTS.md` direto |
| Gemini CLI | `~/.gemini/skills/` | `<repo>/.gemini/skills/` | `GEMINI.md` (importa `AGENTS.md`) |

## Início Rápido

Requisitos: bash e Python 3 (somente biblioteca padrão).

```bash
git clone https://github.com/adejaimejr/ai-project-structure.git
cd ai-project-structure/docs/skills/ai-project-structure
./install.sh
```

Depois, em qualquer projeto, peça ao agente:

> Cria a estrutura multiagente aqui

A skill faz uma entrevista curta com opções numeradas (responder "1 2 3" basta) e cria os arquivos. Nunca roda `git init` e nunca sobrescreve nada sem perguntar.

Validar um projeto:

```bash
python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py <projeto>
```

Use `--strict` para avisos também falharem, ou `--progress` para uma projeção somente-leitura de tarefas e specs.

## Como Funciona

`AGENTS.md` guarda as regras. `CLAUDE.md` e `GEMINI.md` são pontes imutáveis que apontam para ele. A memória é separada por função:

| Arquivo em `docs/` | Função |
| --- | --- |
| `PROJECT_CONTEXT.md` | O que o projeto **é** |
| `SESSION.md` | O que **aconteceu**, em ordem, para dar continuidade entre sessões |
| `MEMORY.md` | O que o projeto **aprendeu** |
| `DECISIONS.md` | O que foi **decidido** formalmente |
| `TASKS.md` | O que está **em aberto**: IDs `T-NNN`, fonte única de status |
| `CONSENSUS.md` | Debate entre modelos, com status e regra de desempate |
| `STACK.md` | Com o que o projeto é **construído** e onde consultar cada tecnologia |
| `specs/` | O que **será construído** (módulo opcional, uma spec leve por feature) |

Regras operacionais: atualizar só o arquivo cuja função foi acionada, dois níveis de leitura (mudança trivial ou relevante), rotação para `docs/archive/` e evidência obrigatória para fechar tarefa.

## Documentação

A skill, a estrutura gerada e a memória do projeto em `docs/` estão em português do Brasil. O README da raiz, o guia de contribuição e a camada GitHub estão em inglês; este arquivo é a versão em português do README.

Para usuários:

| Documento | O que cobre |
| --- | --- |
| [README da skill](docs/skills/ai-project-structure/README.md) | Flags de instalação, caminhos, validador, verificador do repositório |
| [CHANGELOG da skill](docs/skills/ai-project-structure/CHANGELOG.md) | Histórico de versões da skill |
| [SECURITY](docs/SECURITY.md) | Escopo, versões suportadas, como reportar (em inglês) |

Para contribuidores:

| Documento | O que cobre |
| --- | --- |
| [CONTRIBUTING](docs/CONTRIBUTING.md) | Preparação, portões, fluxo de pull request (em inglês) |
| [AGENTS](AGENTS.md) | As regras que todo agente segue aqui |
| [QUALITY](docs/QUALITY.md) | Régua de qualidade e checagens |
| [DECISIONS](docs/DECISIONS.md) | Decisões formais, com motivo |
| [TASKS](docs/TASKS.md) | O backlog vivo |
| [SESSION](docs/SESSION.md) | Registro cronológico das sessões de agente |
| [specs](docs/specs/) | Specs de feature |

Este repositório usa a estrutura que distribui (dogfood). A fonte canônica da skill fica em [docs/skills/ai-project-structure/](docs/skills/ai-project-structure/).

## Inspirações

A v2 da skill foi inspirada no [Specsfy](https://github.com/promovaweb/specsfy), método orientado a specs em pt-BR. Adaptamos a entrevista numerada, os blocos gerenciados, a validação por script e as specs de arquivo único, sem a cerimônia completa. A comparação com [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) originou a camada GitHub deste repositório; veja [docs/DECISIONS.md](docs/DECISIONS.md).

## Segurança

Reporte vulnerabilidades como descrito em [docs/SECURITY.md](docs/SECURITY.md).

## Licença

[MIT](LICENSE).
