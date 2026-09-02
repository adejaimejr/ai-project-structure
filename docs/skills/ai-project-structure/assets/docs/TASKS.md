# TASKS

Backlog vivo do projeto. Fonte unica de verdade do que esta em aberto.

Formato de tarefa:

- ID `T-NNN` sequencial e unico. Nunca reutilize um ID, nem apos concluir.
- Novo ID = maior ID ja usado + 1 (confira tambem `docs/archive/TASKS-*.md`, se existir).
- O status da tarefa e a secao onde ela esta (Em Andamento / Proximas Tarefas / Aguardando Usuario / Concluidas). Nao use campo de status na linha.
- Marcadores opcionais no fim da linha: `(prioridade: alta | media | baixa)`, `(spec: NNNN-slug)` quando a tarefa pertence a uma spec de `docs/specs/`, `(verifica: <comando>)` quando ja se sabe como a tarefa sera verificada, e `(bloqueada: AAAA-MM-DD)` nas tarefas de "Aguardando Usuario".
- Toda tarefa movida para "Concluidas" carrega uma sub-linha `Evidencia:`. A regra completa esta em "Evidencia De Fechamento", no `AGENTS.md`.
- Data de adocao das convencoes: `(convencoes-2-2-0-desde: AAAA-MM-DD)`. Troque `AAAA-MM-DD` pela data em que este projeto adotou a versao 2.2.0 da estrutura. Linha concluida antes dessa data nao e cobrada: registro historico nao vira alegacao sem evidencia.

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

- T-001: Preencher `PROJECT_CONTEXT.md` com o contexto real do projeto (publico, estado atual, restricoes, fora de escopo).

## Aguardando Usuario

- (Vazio. Tarefa que travou por falta de resposta do usuario vem para ca, com a pergunta registrada e o campo de resposta em aberto. Respondida, volta para "Em Andamento" ou "Proximas Tarefas".)

Modelo de tarefa aguardando:

```md
- T-002: Descricao curta e acionavel. (bloqueada: AAAA-MM-DD)
  - **Pergunta:** o que precisa ser respondido para a tarefa andar.
  - **Resposta:** (A preencher.)
```

## Concluidas

- (Vazio. Ao concluir, mova a linha para ca prefixando a data e adicione a sub-linha de evidencia: `- AAAA-MM-DD T-001: ...`.)

## Ideias

- (Vazio. Ideias nao precisam de ID; ao virarem tarefa, ganham o proximo T-NNN.)
