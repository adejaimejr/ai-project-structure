# Specs: Ativar Modulo E Criar Spec

## Ativar O Modulo Em Projeto Existente

1. Confirme que o projeto usa a estrutura (tem `AGENTS.md` com marcadores; se for v1, ofereca primeiro o fluxo de `atualizacao.md`).
2. Copie `assets/docs/specs/README.md` desta skill para `docs/specs/README.md` (nao sobrescreva se ja existir).
3. Insira o conteudo de `assets/partials/AGENTS-specs-block.md` em `AGENTS.md`, logo apos `<!-- ai-project-structure:core:end -->` e antes de "## Regras Do Projeto". Se o bloco `specs` ja existir, nao duplique.
4. Registre: entrada em `docs/SESSION.md` e linha em `docs/CHANGELOG.md` do projeto.

## Criar Uma Spec

1. **Numero**: proximo `NNNN` livre em `docs/specs/` (comece em `0001`). Nunca reutilize.
2. **Entrevista curta**, com perguntas numeradas e opcoes numeradas (mesmo contrato do scaffold): titulo/slug, problema e resultado esperado, escopo (incluido / fora), criterios de aceite. Aplique a regra **Nunca Inferir**: lacuna sem resposta → pergunte; "Avançar" → registre em "Perguntas Abertas" da spec, nunca invente.
3. **Crie o arquivo** `docs/specs/NNNN-slug.md` usando o "Modelo De Spec" de `docs/specs/README.md`. Status inicial: `Rascunho` (ou `Definida`, se criterios de aceite ja fecharam sem perguntas abertas bloqueantes).
4. **Tarefas**: crie as tarefas em `docs/TASKS.md` com os proximos `T-NNN` livres e o sufixo `(spec: NNNN-slug)`. Na spec, liste apenas os T-IDs na secao "Tarefas" - status vive so em `TASKS.md`.
5. **Registre** em `docs/SESSION.md` se o trabalho foi relevante.

## Mudanca De Requisito Apos `Definida`

Reabra **apenas as secoes afetadas** da spec (nao recrie a spec):

1. Registre a mudanca em "Decisoes" com o proximo `DEC-NNN` (o que mudou, por que, trade-off).
2. Ajuste criterios de aceite/escopo afetados.
3. Reflita em `TASKS.md`: novas tarefas ganham novos `T-NNN`; tarefas obsoletas sao movidas para Concluidas com nota `(cancelada)` ou removidas apenas se nunca iniciadas.
4. Se a decisao tiver impacto alem da spec, copie para `docs/DECISIONS.md`.

## Concluir Uma Spec

1. Todas as tarefas da spec em "Concluidas" no `TASKS.md` (ou arquivadas).
2. Preencha "Evidencia De Conclusao": verificacao executada (comando ou checagem manual) + resultado.
3. Mude `**Status:**` para `Concluida`. Sem evidencia preenchida, nao conclua.
