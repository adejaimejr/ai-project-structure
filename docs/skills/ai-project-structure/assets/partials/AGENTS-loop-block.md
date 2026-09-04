<!-- ai-project-structure:loop:start v2.7.0 -->
## Loop (Modulo Opcional Ativo)

Este projeto pode executar uma tarefa sem supervisao, pelo `loop.sh` da skill. O ciclo e sempre o mesmo: pega **uma** tarefa que declarou `(verifica: <comando>)`, trabalha, roda o comando declarado e usa a saida da falha como contexto da tentativa seguinte. Ate 3 tentativas.

### O Que O Loop Pode Escrever

Na memoria do projeto, o loop escreve **apenas o que um comando comprova**:

- Move a tarefa para "## Concluidas" e escreve `Evidencia: tipo=comando` **somente** quando o comando declarado sai 0. O campo `resultado` recebe a saida real, nao um resumo dela.
- Nunca escreve evidencia de `tipo=revisao-manual` nem `tipo=conferencia`. Esses dois tipos afirmam que uma pessoa conferiu, e o loop nao e uma pessoa.
- Portao falhou em todas as tentativas: nao move a tarefa, nao escreve evidencia, reporta e sai com codigo diferente de zero.

Excecao unica: **falta de contexto obrigatorio**. Nesse caso o loop move a tarefa para "## Aguardando Usuario", escreve `**Pergunta:**` com a duvida, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)`, e para. Registrar duvida e o oposto de alegar conclusao, por isso e a unica escrita sem comando por tras.

### Como Pedir Ajuda No Meio De Uma Rodada

Faltou contexto obrigatorio? Escreva a pergunta, em uma frase, no arquivo `.loop-pergunta` na raiz do projeto e **pare**. O loop registra a pergunta na tarefa e encerra a rodada. Nao escolha por inferencia plausivel para nao interromper o ciclo: uma rodada a menos custa pouco, e um palpite escrito como se fosse decisao custa caro.

### Nao Apague O Que Falha

O portao mede o que sobrou, nao o que voce fez. Entao apagar a coisa que falha sempre funciona: o teste que quebra, a secao que nao passa no lint, o link que nao resolve. **Nao faca isso.**

Quando a saida obvia for remover conteudo, informacao ou cobertura para o portao ficar verde, **pare e pergunte** pelo `.loop-pergunta`. Perder informacao e uma decisao do usuario, nunca sua, e ela nao aparece no portao: o verde fica igual nos dois casos.

### Limites

- Uma tarefa por rodada, indicada no comando. O loop nunca escolhe sozinho no que trabalhar.
- Tarefa sem `(verifica:)` nao e elegivel: o loop recusa antes de chamar o agente.
- O loop nao escreve em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `CONSENSUS.md`, `AGENTS.md` nem em specs. O relatorio da rodada da o material; quem registra e voce. `CONSENSUS.md` e caso especial: uma entrada la declara metodo, exposicao previa e rodada, e uma rodada de loop tem um agente so. Consenso de um modelo so e o que esses campos existem para denunciar.
- O aviso de parada e o exit code mais o relatorio em stdout. Som, notificacao ou webhook se compoem por fora.

O fluxo completo e o uso estao em `references/loop.md` da skill `ai-project-structure`.
<!-- ai-project-structure:loop:end -->
