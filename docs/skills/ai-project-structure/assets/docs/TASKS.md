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

- T-001: Preencher `PROJECT_CONTEXT.md` com o contexto real do projeto (publico, estado atual, restricoes, fora de escopo).

## Concluidas

- (Vazio. Ao concluir, mova a linha para ca prefixando a data: `- AAAA-MM-DD T-001: ...`.)

## Ideias

- (Vazio. Ideias nao precisam de ID; ao virarem tarefa, ganham o proximo T-NNN.)
