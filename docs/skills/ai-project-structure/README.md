# Skill: ai-project-structure

Skill instalavel que cria a **estrutura Markdown multiagente** (`AGENTS.md`, `CLAUDE.md`,
`GEMINI.md` + memoria em `docs/`) em um projeto novo ou existente.

Ela segue o **Agent Skills Open Standard**: o mesmo `SKILL.md` (frontmatter YAML com
`name` + `description`) e lido nativamente por **Claude Code**, **Codex CLI** e **Gemini CLI**.
Nao existem tres formatos diferentes - existe um pacote, instalado em tres lugares.

## Conteudo do pacote

```
ai-project-structure/
├── SKILL.md            # instrucoes da skill (formato padrao, cross-tool; version no frontmatter)
├── assets/             # templates copiados para o projeto-alvo
│   ├── AGENTS.md  CLAUDE.md  GEMINI.md
│   ├── partials/       # blocos de insercao (nunca copiados ao projeto)
│   └── docs/...        # inclui docs/specs/README.md (modulo opcional)
├── references/         # fluxos detalhados: atualizacao.md, specs.md
├── scripts/
│   └── validate_structure.py   # validador (Python 3, so stdlib)
├── agents/
│   └── openai.yaml     # metadado OPCIONAL do Codex (UI + politica de invocacao)
├── evals/
│   ├── evals.json      # suite local de teste da skill (nao vai para a instalacao)
│   └── fixtures/       # projetos de teste (v1-project, broken-project)
├── CHANGELOG.md        # historico de versoes da skill
├── install.sh          # instalador para as tres ferramentas
└── README.md           # este arquivo
```

`install.sh` copia para a instalacao `SKILL.md`, `assets/`, `agents/`, `scripts/` e `references/`.
`evals/`, `CHANGELOG.md`, `install.sh` e `README.md` ficam so no repositorio-fonte.

## Instalacao rapida

```bash
cd docs/skills/ai-project-structure
./install.sh            # global, nas tres ferramentas
```

Opcoes:

```bash
./install.sh --project          # instala neste repo (.claude / .agents / .gemini)
./install.sh --gemini           # so uma ferramenta
./install.sh --claude --codex   # subconjunto
./install.sh --uninstall        # remove dos destinos escolhidos
```

## Onde cada ferramenta le a skill

| Ferramenta  | Global (todos os projetos) | Por-projeto              |
|-------------|----------------------------|--------------------------|
| Claude Code | `~/.claude/skills/`        | `<repo>/.claude/skills/` |
| Codex CLI   | `~/.agents/skills/`        | `<repo>/.agents/skills/` |
| Gemini CLI  | `~/.gemini/skills/`        | `<repo>/.gemini/skills/` |

> Nota: o caminho oficial do Codex e `~/.agents/skills/` (padrao Agent Skills),
> **nao** `~/.codex/skills/`.

### Instalacao manual (sem o script)

```bash
# exemplo para Codex global
mkdir -p ~/.agents/skills/ai-project-structure
cp -R SKILL.md assets agents ~/.agents/skills/ai-project-structure/
```

Troque o destino pelo da tabela acima para Claude (`~/.claude/skills`) ou Gemini (`~/.gemini/skills`).

## Como usar depois de instalada

A skill dispara por linguagem natural (graças a `description` do `SKILL.md`) em qualquer
das tres ferramentas. Exemplos:

- "Inicia um projeto novo aqui chamado `minha-loja`, objetivo X. Estrutura minimal."
- "Cria a base multiagente completa neste diretorio."
- "Atualiza este projeto para a versao mais nova da estrutura."
- "Valida a estrutura deste projeto."
- "Ativa o modulo de specs aqui." / "Cria uma spec para a feature X."

Invocacao explicita:

- **Codex CLI / IDE**: rode `/skills` ou digite `$ai-project-structure`.
- **Claude Code**: use o seletor de skills/comandos da ferramenta.
- **Gemini CLI**: peca a tarefa que a skill cobre; ela ativa pela `description`.

## Nota sobre evals no Codex

O arquivo `evals/evals.json` e uma suite local simples. Para automacao com Codex, a
convencao recomendada pela documentacao oficial e manter um conjunto pequeno de prompts
em `evals/<skill>.prompts.csv`, executar `codex exec --json` e gravar traces JSONL em
`evals/artifacts/` para checks deterministas e rubricas estruturadas.

## Validador

```bash
python3 scripts/validate_structure.py <caminho-do-projeto>            # relatorio + exit code
python3 scripts/validate_structure.py <caminho-do-projeto> --strict   # avisos tambem falham
python3 scripts/validate_structure.py <caminho-do-projeto> --progress # projecao read-only de tarefas e specs
```

Checa: arquivos do nucleo, pontes, marcadores do bloco gerenciado, formato das
entradas de SESSION/CONSENSUS, limites de rotacao, IDs `T-NNN`, coerencia do
modulo de specs (nomes, Status, tarefas referenciadas) e ausencia de travessao
(em dash, U+2014), que e proibido nos textos do projeto.

## Atualizar um projeto existente

A skill faz isso (nao e mais "edite na mao"): peca "atualiza este projeto para a
versao mais nova da estrutura". O fluxo (`references/atualizacao.md`) detecta a
versao pelos marcadores `ai-project-structure:core:start vX.Y.Z` em `AGENTS.md`,
mostra diff por bloco e nunca sobrescreve sem confirmacao por item.

## Versionamento

A versao canonica da skill fica no frontmatter do `SKILL.md` (`version`); cada
release ganha entrada no `CHANGELOG.md` desta pasta. O projeto-alvo carrega a
versao aplicada nos marcadores do `AGENTS.md`.

## Atualizar a skill

A fonte canonica e esta pasta no repositorio. Edite `SKILL.md` / `assets/` /
`scripts/` / `references/` aqui e rode `./install.sh` de novo para propagar para
as tres ferramentas (a copia sobrescreve).
