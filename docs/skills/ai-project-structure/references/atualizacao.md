# Fluxo De Atualizacao

Use este fluxo quando o destino ja usa a estrutura (tem `AGENTS.md` e `docs/SESSION.md` com entradas reais) e o usuario quer atualiza-la para a versao atual da skill.

Sequencia:

```text
DETECTAR → (ja atualizado? → RELATAR + VALIDAR) → PLANEJAR → APLICAR POR BLOCO
→ PONTES → NOVOS ARQUIVOS → MIGRAR TASKS → REGISTRAR → VALIDAR
```

## Invariantes (valem em todos os passos)

- **Nada e sobrescrito sem confirmacao por item.** Sem resposta do usuario, nada muda.
- Nunca toque conteudo fora dos marcadores em `AGENTS.md` (excecao: o resgate v1, com consentimento explicito).
- Conteudo abaixo de "## Regras Do Projeto" e intocavel.
- Nunca inicialize repositorio git.

## 1. DETECTAR

Leia o `AGENTS.md` do destino e procure `<!-- ai-project-structure:core:start vX.Y.Z -->`.

- Marcador presente → versao do projeto = `X.Y.Z`.
- Marcador ausente, mas estrutura reconhecivel (`AGENTS.md` + `docs/SESSION.md`) → **v1**.

Compare com a versao no frontmatter do `SKILL.md` desta skill.

## 2. JA ATUALIZADO?

Versoes iguais: informe o usuario, ofereca rodar o validador (`scripts/validate_structure.py`) e encerre.

## 3. PLANEJAR

Monte a lista de acoes e **mostre ao usuario antes de tocar qualquer arquivo**:

- blocos de `AGENTS.md` a atualizar (core; specs, se existir);
- pontes (`CLAUDE.md`/`GEMINI.md`) divergentes do template atual;
- arquivos novos disponiveis (ex: `docs/specs/README.md`, se for ativar o modulo);
- migracao de `TASKS.md` para IDs `T-NNN` (se ainda nao usa).

## 4. APLICAR POR BLOCO (`AGENTS.md`)

### v1 → v2 (sem marcadores)

Mostre o diff entre o `AGENTS.md` atual do projeto e o bloco `core` do template v2. Pergunte:

- **(a) substituir pelo bloco v2** - secoes que existem no arquivo do usuario mas nao no template sao preservadas: mova-as para "## Regras Do Projeto", abaixo do bloco. Avise o usuario para revisar o resultado.
- **(b) manter como esta** - o projeto continua v1; registre a pendencia como tarefa em `TASKS.md`.

### v2 → v2.x (com marcadores)

Para cada bloco (`core`; `specs`, se existir no projeto):

- conteudo identico ao template atual → pule em silencio;
- conteudo diferente → mostre o diff **so do bloco** e pergunte: aplicar / pular / decidir depois. Bloco pulado vira tarefa em `TASKS.md`.

Bloco `specs` ausente e usuario nao usa specs → nao ofereca a insercao; apenas mencione que o modulo existe.

## 5. PONTES

`CLAUDE.md` ou `GEMINI.md` diferentes do template atual: mostre o diff e pergunte substituir/manter (lembre a regra: pontes sao imutaveis e nao carregam regras proprias).

## 6. NOVOS ARQUIVOS

Ofereca apenas arquivos que **nao existem** no destino. **Nunca** toque no conteudo de `docs/*.md` com dados do usuario (SESSION, MEMORY, TASKS, etc.).

## 7. MIGRAR TASKS

Se `docs/TASKS.md` nao usa IDs `T-NNN`, ofereca atribuir `T-001, T-002, ...` as tarefas existentes na ordem em que aparecem (Em Andamento primeiro, depois Proximas, depois Concluidas). Recusado → siga em frente; o validador emitira apenas um INFO "formato v1".

## 8. REGISTRAR

- Atualize `vX.Y.Z` nos marcadores aplicados.
- Nova entrada em `docs/SESSION.md` do destino: o que foi aplicado e o que foi pulado.
- Linha em `docs/CHANGELOG.md` do destino.
- Blocos/itens pulados → tarefas em `docs/TASKS.md`.

## 9. VALIDAR

Rode `python3 <dir-desta-skill>/scripts/validate_structure.py <destino>` e reporte o resultado ao usuario.
