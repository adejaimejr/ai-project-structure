# TASKS

Backlog vivo do projeto. Fonte unica de verdade do que esta em aberto.

Formato de tarefa:

- ID `T-NNN` sequencial e unico. Nunca reutilize um ID, nem apos concluir.
- Novo ID = maior ID ja usado + 1 (confira tambem `docs/archive/TASKS-*.md`, se existir).
- O status da tarefa e a secao onde ela esta (Em Andamento / Proximas Tarefas / Concluidas). Nao use campo de status na linha.
- Marcadores opcionais no fim da linha: `(prioridade: alta | media | baixa)` e `(spec: NNNN-slug)` quando a tarefa pertence a uma spec de `docs/specs/`.

Modelo de linha:

```md
- T-001: Descricao curta e acionavel. (prioridade: alta) (spec: 0001-login-social)
```

## Em Andamento

- (Vazio.)

## Proximas Tarefas

- T-009: Bloco core v2.2.0 e templates de `TASKS.md` e `CONSENSUS.md` com evidencia obrigatoria, `(verifica:)`, secao `Aguardando Usuario` e campos declarativos de consenso. (prioridade: alta) (spec: 0003-tasks-verificaveis)
- T-010: Checks novos no validador: evidencia, `(verifica:)` sem resultado, `Aguardando Usuario` sem pergunta, marcador com valor desconhecido, campos de consenso e teto de rodadas. (prioridade: alta) (verifica: python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict) (spec: 0003-tasks-verificaveis)
- T-011: Criar `evals/verify_repository.py` (raiz, fixtures, paridade de blocos e templates, `evals.json`, install em destino temporario) e corrigir os 4 headings ausentes em `SESSION.md`. (prioridade: alta) (verifica: python3 docs/skills/ai-project-structure/evals/verify_repository.py) (spec: 0003-tasks-verificaveis)
- T-012: Fixture `aguardando-project`, evals atualizados para 2.2.0, dogfood do meta-projeto e reinstalacao com paridade nos tres destinos. (prioridade: media) (verifica: python3 docs/skills/ai-project-structure/evals/verify_repository.py) (spec: 0003-tasks-verificaveis)
- T-013: Rotacionar as entradas antigas de `CONSENSUS.md` e de `SESSION.md` para `docs/archive/CONSENSUS-2026.md` e `docs/archive/SESSIONS-2026.md`, e atualizar o indice do archive. Os dois arquivos passaram de 30KB e o validador ja avisa nos dois. (prioridade: baixa) (verifica: python3 docs/skills/ai-project-structure/scripts/validate_structure.py .)

## Concluidas

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
