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
│   ├── partials/       # blocos de insercao specs e loop (nunca copiados ao projeto)
│   └── docs/...        # inclui docs/specs/README.md (modulo opcional)
├── references/         # fluxos detalhados: atualizacao.md, specs.md, loop.md
├── scripts/
│   ├── validate_structure.py   # validador (Python 3, so stdlib)
│   ├── loop.sh                 # modulo de loop: orquestra uma rodada
│   └── loop_task.py            # modulo de loop: edicoes em TASKS.md
├── agents/
│   └── openai.yaml     # metadado OPCIONAL do Codex (UI + politica de invocacao)
├── evals/
│   ├── evals.json      # suite local de teste da skill (nao vai para a instalacao)
│   ├── verify_repository.py    # prova a integridade deste repositorio
│   ├── test_loop.py    # bateria do modulo de loop, com agente falso
│   ├── portao_t065.py  # portao da T-065: prova que o verificador cobre os 39 codigos
│   └── fixtures/       # projetos de teste (v1-project, broken-project, aguardando-project, achado-project, debate-project, cobertura-*)
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

### Por Que So Duas Pontes

`CLAUDE.md` e `GEMINI.md` existem porque Claude Code e Gemini CLI entram por
arquivo proprio. Codex, Grok e opencode leem `AGENTS.md` direto, entao ponte
para eles seria arquivo morto: nenhum dos binarios procura `GROK.md` ou
`OPENCODE.md`. Conferido em 2026-09-03 contando as referencias dentro dos
proprios executaveis.

### Instalacao manual (sem o script)

```bash
# exemplo para Codex global
mkdir -p ~/.agents/skills/ai-project-structure
cp -R SKILL.md assets agents scripts references ~/.agents/skills/ai-project-structure/
find ~/.agents/skills/ai-project-structure -type d -name __pycache__ -prune -exec rm -rf {} +
```

Troque o destino pelo da tabela acima para Claude (`~/.claude/skills`) ou Gemini (`~/.gemini/skills`). Sem `scripts/` e `references/` a skill instala, mas validador, atualizacao, specs e loop nao funcionam: ate 2026-09-03 este exemplo copiava so tres itens (REVAL-7).

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
python3 scripts/validate_structure.py <caminho-do-projeto> --codigos  # uma linha por diagnostico, legivel por maquina
```

Da versao 2.5.0 em diante todo diagnostico carrega um **codigo estavel**
(`ACHADO-SEM-ESCAPOU`, `TASK-ID-DUPLICADO`, ...), mostrado no relatorio como
`[AVISO] [CODIGO] mensagem`. O codigo e contrato publico: a redacao da mensagem
pode mudar quando melhorar, o codigo so muda em mudanca de versao. `--codigos`
troca o relatorio por `NIVEL|CODIGO|ARQUIVO|SUJEITO`, uma linha por
diagnostico, que e o que usar para montar portao.

Checa: arquivos do nucleo, pontes, marcadores do bloco gerenciado, formato das
entradas de SESSION/CONSENSUS, limites de rotacao, IDs `T-NNN`, coerencia do
modulo de specs (nomes, Status, tarefas referenciadas) e ausencia de travessao
(em dash, U+2014), que e proibido nos textos do projeto.

Da versao 2.2.0 em diante checa tambem: evidencia de fechamento em tarefa
concluida (AVISO), tarefa que declarou `(verifica:)` e concluiu sem o resultado
do comando (ERRO), tarefa em `Aguardando Usuario` sem `**Pergunta:**` (ERRO),
valor desconhecido em marcador conhecido, idade do bloqueio e os campos
declarativos de `CONSENSUS.md`. A cobranca de evidencia depende do marcador
`(convencoes-2-2-0-desde: AAAA-MM-DD)` no `TASKS.md` do projeto: sem ele, nada e
cobrado, e nenhuma linha anterior a essa data e cobrada.

Da versao 2.4.0 em diante checa tambem o formato de achado em `CONSENSUS.md`
(AVISO): entrada que declara `**Achado:**` sem identificador, sem
`**Escapou de verificacao:**` ou com valor fora de `sim | nao`, e achado que
declarou `sim` sem a secao "Por Que Nada Pegou Antes". A partir da quarta
rodada, a entrada precisa de `**Pendente da rodada anterior:**`. Entrada de
debate nao e afetada: os checks novos so valem para quem declarar `**Achado:**`.

## Verificador do repositorio

```bash
python3 evals/verify_repository.py            # exit 0 se o repositorio esta integro
python3 evals/verify_repository.py --verbose  # mostra a saida do que falhar
```

So existe no repositorio-fonte (`evals/` nao e distribuido). Roda o validador na
raiz com `--strict`, os fixtures com os exit codes esperados, a paridade dos
blocos gerenciados e das pontes, as convencoes nos templates e no dogfood, a
coerencia de versao entre `SKILL.md`, marcadores e `CHANGELOG.md`, a estrutura de
`evals.json`, a ausencia de travessao em arquivo versionado e a paridade dos tres
destinos, instalando em pasta temporaria. Nao toca nas instalacoes reais.

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
