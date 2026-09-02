# TASKS

Backlog vivo do projeto. Fonte unica de verdade do que esta em aberto.

Formato de tarefa:

- ID `T-NNN` sequencial e unico. Nunca reutilize um ID, nem apos concluir.
- Novo ID = maior ID ja usado + 1 (confira tambem `docs/archive/TASKS-*.md`, se existir).
- O status da tarefa e a secao onde ela esta (Em Andamento / Proximas Tarefas / Aguardando Usuario / Concluidas). Nao use campo de status na linha.
- Marcadores opcionais no fim da linha: `(prioridade: alta | media | baixa)`, `(spec: NNNN-slug)` quando a tarefa pertence a uma spec de `docs/specs/`, `(verifica: <comando>)` quando ja se sabe como a tarefa sera verificada, e `(bloqueada: AAAA-MM-DD)` nas tarefas de "Aguardando Usuario".
- Toda tarefa movida para "Concluidas" carrega uma sub-linha `Evidencia:`. A regra completa esta em "Evidencia De Fechamento", no `AGENTS.md`.
- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-02)`. Linha concluida antes dessa data nao e cobrada: registro historico nao vira alegacao sem evidencia.

Modelo de linha:

```md
- T-001: Descricao curta e acionavel. (prioridade: alta) (spec: 0001-login-social) (verifica: pytest -q)
```

Modelo de linha concluida:

```md
- AAAA-MM-DD T-001: Descricao curta e acionavel. (spec: 0001-login-social)
  - Evidencia: tipo=comando; procedimento=pytest -q; resultado=42 passed, exit 0
```

## Em Andamento

- (Vazio.)

## Proximas Tarefas

- T-014: Exercitar na mao os tres criterios de aceite da spec 0003 que nao tem runner: scaffold minimal e scaffold completa com os templates 2.2.0, e atualizacao de um projeto 2.1.0 pelo fluxo de `references/atualizacao.md` (com tarefas concluidas, tarefa aguardando e consenso existente), conferindo que nenhum registro historico vira alegacao sem evidencia. (prioridade: media) (spec: 0003-tasks-verificaveis)


## Aguardando Usuario

- (Vazio. Tarefa que travou por falta de resposta do usuario vem para ca, com `**Pergunta:**` e `**Resposta:** (A preencher.)`.)

## Concluidas

- 2026-09-02 T-012: Fixture `aguardando-project`, evals atualizados para 2.2.0, dogfood do meta-projeto e reinstalacao com paridade nos tres destinos. (verifica: python3 docs/skills/ai-project-structure/evals/verify_repository.py) (spec: 0003-tasks-verificaveis)
  - Evidencia: tipo=comando; procedimento=fixture nova com os dois casos, eval 9, `SKILL.md` e marcadores em 2.2.0, CHANGELOG da skill e do repositorio, passo 7b em `references/atualizacao.md`, comando registrado em `QUALITY.md`, `./install.sh` nos tres destinos globais e depois `python3 docs/skills/ai-project-structure/evals/verify_repository.py`; resultado=exit 0 com 26 de 26 verificacoes, os tres destinos em version 2.2.0 e identicos entre si por `diff -rq`, divergindo da fonte canonica apenas em `CHANGELOG.md`, `README.md`, `evals/` e `install.sh`, que nao sao distribuidos
- 2026-09-02 T-011: Criado `evals/verify_repository.py` (raiz, fixtures, paridade de blocos e templates, `evals.json`, install em destino temporario) e corrigidos os 4 headings ausentes em `SESSION.md`. (verifica: python3 docs/skills/ai-project-structure/evals/verify_repository.py) (spec: 0003-tasks-verificaveis)
  - Evidencia: tipo=comando; procedimento=verificador escrito com 26 checagens, os 4 headings de 2026-04-25 corrigidos com nota de que nada foi promovido retroativamente, e `python3 docs/skills/ai-project-structure/evals/verify_repository.py` rodado no estado limpo, com divergencia induzida no bloco core da raiz e com ela desfeita; resultado=exit 0 no estado limpo (26 de 26) e exit 1 com a divergencia, apontando `bloco core identico entre AGENTS.md e assets/AGENTS.md: 11390 bytes`; validador voltou a 0 avisos em `SESSION.md`
- 2026-09-02 T-010: Checks novos no validador: evidencia, `(verifica:)` sem resultado, `Aguardando Usuario` sem pergunta, marcador com valor desconhecido, campos de consenso e teto de rodadas. (verifica: python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict) (spec: 0003-tasks-verificaveis)
  - Evidencia: tipo=comando; procedimento=matriz de 17 casos em projeto descartavel (um por regra nova, mais os casos que devem ficar silenciosos por nao retroatividade) e depois `python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict` no meta-projeto; resultado=17/17 casos conforme esperado e exit 0 com 0 erros e 0 avisos; fixtures inalteradas (broken-project 2 erros exit 1, v1-project exit 0)
- 2026-09-02 T-013: Rotacionadas as entradas antigas de `CONSENSUS.md` e de `SESSION.md` para `docs/archive/CONSENSUS-2026.md` e `docs/archive/SESSIONS-2026.md`, com o indice do archive atualizado. (verifica: python3 docs/skills/ai-project-structure/scripts/validate_structure.py .) (spec: 0003-tasks-verificaveis)
  - Evidencia: tipo=comando; procedimento=10 entradas de SESSION.md (2026-04-25 a 2026-05-26) e os 2 debates de 2026-04-25 movidos para `docs/archive/`, ponteiros deixados nos arquivos principais, indice preenchido, e `python3 docs/skills/ai-project-structure/scripts/validate_structure.py .` rodado depois; resultado=exit 0 sem aviso de rotacao; SESSION.md de 33KB para 19KB (7 entradas), CONSENSUS.md de 32KB para 11KB (1 entrada), nenhuma entrada perdida (17 = 7 + 10 e 3 = 1 + 2)
- 2026-09-02 T-009: Bloco core v2.2.0 e templates de `TASKS.md` e `CONSENSUS.md` com evidencia obrigatoria, `(verifica:)`, secao `Aguardando Usuario` e campos declarativos de consenso. (spec: 0003-tasks-verificaveis)
  - Evidencia: tipo=conferencia; procedimento=bloco core reescrito em `assets/AGENTS.md` e propagado para a raiz por script, marcadores `core` e `specs` para v2.2.0, templates de `TASKS.md` e `CONSENSUS.md` atualizados, e comparacao dos dois blocos core byte a byte; resultado=blocos identicos (11373 bytes), quatro marcadores em v2.2.0, "Regras Do Projeto" preservada, validador exit 0 sem erro novo (6 avisos preexistentes)
- 2026-08-20 T-008: Inicializado git (a pedido do usuario) e publicado o projeto em `github.com/adejaimejr/ai-project-structure` (publico, branch main).
- 2026-08-20 T-005: Criado o template `STACK.md` (tecnologias, pacotes, documentacao oficial) e integrado ao bloco core e ao scaffold "completa"; skill 2.1.0. (spec: 0002-stack-e-progresso)
- 2026-08-20 T-006: Implementada a flag `--progress` no validador (projecao somente-leitura de tarefas e specs). (spec: 0002-stack-e-progresso)
- 2026-08-20 T-007: Evals atualizados (eval 2 com STACK, eval 8 novo de progresso), skill reinstalada com paridade nos tres destinos e bateria de validacao aprovada. (spec: 0002-stack-e-progresso)
- 2026-08-20 T-002: Rodados os 7 evals de `skills/ai-project-structure/evals/evals.json` no Claude Code, Codex CLI e Gemini CLI; as tres ferramentas aprovaram 7 de 7 cenarios. (spec: 0001-skill-v2)
- 2026-08-20 T-003: Testado o fluxo de atualizacao v1 para v2 (`references/atualizacao.md`) de ponta a ponta em projeto simulado fora do repositorio; 8 invariantes aprovados e validador exit 0. (spec: 0001-skill-v2)
- 2026-08-20 T-004: Reinstalada a skill v2 com `./install.sh` e conferida a paridade dos tres destinos. (spec: 0001-skill-v2)
- 2026-08-20 T-001: Preenchido `PROJECT_CONTEXT.md` com o contexto real do projeto.
- 2026-05-26: Skill `ai-project-structure` empacotada no Agent Skills Open Standard e instalada globalmente nas tres ferramentas (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`), com `install.sh`, `README.md` e `agents/openai.yaml`.
- 2026-05-26: Revisada a parte Codex da skill contra a documentacao oficial atual; corrigidos `agents/openai.yaml` e `README.md` na fonte canonica.
- 2026-05-26: Propagados os ajustes Codex via `install.sh`; verificado que `agents/openai.yaml` ficou identico nos tres destinos (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`).
- 2026-04-25: Criada a estrutura Markdown multiagente com sessoes e consenso.
- 2026-04-25: Validada a estrutura via tri-consenso (Claude + Gemini + Codex) em `CONSENSUS.md`.
- 2026-04-25: Aplicadas oito melhorias: `MEMORY.md`, `archive/`, revisao de `AGENTS.md`, templates de `SESSION.md` e `CONSENSUS.md`, `QUALITY.md` revisado, skill sincronizada.
- 2026-04-25: ~~Instalada a skill `ai-project-structure` globalmente em `~/.claude/skills/` e `~/.codex/skills/`.~~ **(substituido em 2026-05-26: a instalacao nao persistiu e `~/.codex/skills/` nao e o caminho lido pelo Codex.)**

## Ideias

- Criar versoes especificas desta estrutura para projetos de software, conteudo, automacao e produto.
- Avaliar emprestimos futuros do specsfy: entrevista com lentes de categorias (MCR-10 simplificado), campo Esforco nas specs como padrao.
