<!-- ai-project-structure:loop:start v2.3.0 -->
## Loop (Modulo Opcional Ativo)

Este projeto pode executar uma tarefa sem supervisao, pelo `loop.sh` da skill. O ciclo e sempre o mesmo: pega **uma** tarefa que declarou `(verifica: <comando>)`, trabalha, roda o comando declarado e usa a saida da falha como contexto da tentativa seguinte. Ate 3 tentativas.

### O Que O Loop Pode Escrever

Na memoria do projeto, o loop escreve **apenas o que um comando comprova**:

- Move a tarefa para "## Concluidas" e escreve `Evidencia: tipo=comando` **somente** quando o comando declarado sai 0. O campo `resultado` recebe a saida real, nao um resumo dela.
- Nunca escreve evidencia de `tipo=revisao-manual` nem `tipo=conferencia`. Esses dois tipos afirmam que uma pessoa conferiu, e o loop nao e uma pessoa.
- Portao falhou em todas as tentativas: nao move a tarefa, nao escreve evidencia, reporta e sai com codigo diferente de zero.

Excecao unica: **falta de contexto obrigatorio**. Nesse caso o loop move a tarefa para "## Aguardando Usuario", escreve `**Pergunta:**` com a duvida, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)`, e para. Registrar duvida e o oposto de alegar conclusao, por isso e a unica escrita sem comando por tras.

### Limites

- Uma tarefa por rodada, indicada no comando. O loop nunca escolhe sozinho no que trabalhar.
- Tarefa sem `(verifica:)` nao e elegivel: o loop recusa antes de chamar o agente.
- O loop nao escreve em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` nem em specs. O relatorio da rodada da o material; quem registra e voce.
- O aviso de parada e o exit code mais o relatorio em stdout. Som, notificacao ou webhook se compoem por fora.

O fluxo completo e o uso estao em `references/loop.md` da skill `ai-project-structure`.
<!-- ai-project-structure:loop:end -->
