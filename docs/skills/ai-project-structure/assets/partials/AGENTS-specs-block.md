<!-- ai-project-structure:specs:start v2.5.0 -->
## Specs (Modulo Opcional Ativo)

Crie uma spec em `docs/specs/` quando o trabalho for tamanho-feature:

- atravessa mais de uma sessao, ou gera mais de ~3 tarefas;
- muda contrato, arquitetura ou modelo de dados;
- tem ambiguidade que precisa de criterios de aceite explicitos.

Va direto para `TASKS.md`, sem spec, quando for mudanca pequena, correcao ou ajuste.

Regras:

- Nome do arquivo: `NNNN-slug.md` (sequencial, ex: `0001-login-social.md`).
- Status no arquivo: `Rascunho → Definida → Em andamento → Concluida` (ou `Cancelada`).
- `TASKS.md` e a unica fonte de status das tarefas. A spec so lista os T-IDs; nunca marque andamento de tarefa dentro da spec.
- Criterios de aceite nao podem ser inventados: se faltar contexto, pergunte (regra "Nunca Inferir") e registre em "Perguntas Abertas".
- Mudou o requisito depois de `Definida`? Reabra apenas as secoes afetadas e registre a mudanca em "Decisoes" (`DEC-NNN`).
- Spec so vira `Concluida` com "Evidencia De Conclusao" preenchida (comando + resultado).

O modelo de spec esta em `docs/specs/README.md`.
<!-- ai-project-structure:specs:end -->
