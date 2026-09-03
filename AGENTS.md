# AGENTS.md

<!-- ai-project-structure:core:start v2.3.0 -->
<!-- Bloco gerenciado pela skill ai-project-structure. Nao edite dentro dos
     marcadores: atualizacoes da skill podem substituir este bloco (sempre com
     confirmacao). Regras especificas deste projeto vao na secao
     "Regras Do Projeto", no fim do arquivo. -->

Este e o arquivo central de instrucao para qualquer agente de IA neste projeto.

Claude Code deve entrar por `CLAUDE.md`.
Gemini deve entrar por `GEMINI.md`.
Codex e outros agentes devem ler este arquivo diretamente.

Se houver conflito entre arquivos, siga esta prioridade:

1. Instrucoes diretas do usuario na conversa atual.
2. Este arquivo, `AGENTS.md`.
3. Arquivos em `docs/`.
4. Padroes inferidos do projeto.

## Arquivos-Ponte Sao Imutaveis

`CLAUDE.md` e `GEMINI.md` sao apenas redirecionamentos para `AGENTS.md`. Eles nao podem conter regras de produto, arquitetura, processo, estilo ou qualquer logica. Quando uma regra precisar mudar, mude aqui.

## Ordem De Leitura

A profundidade de leitura depende do tipo de mudanca.

### Mudanca Trivial

Para typos, ajustes de comentario, formatacao ou rename estritamente local **sem impacto em comportamento, contrato, arquitetura, regras de IA ou estrutura de arquivos**, leia apenas:

1. `docs/SESSION.md`
2. `docs/TASKS.md`

Em duvida, trate como relevante.

### Mudanca Relevante

Para qualquer outra mudanca, leia:

1. `docs/README.md`
2. `docs/PROJECT_CONTEXT.md`
3. `docs/SESSION.md`
4. `docs/MEMORY.md`
5. `docs/TASKS.md`
6. `docs/ARCHITECTURE.md`
7. `docs/QUALITY.md`

Leia tambem quando necessario:

- `docs/DECISIONS.md` para entender decisoes ja tomadas.
- `docs/CONSENSUS.md` quando existir duvida, conflito ou decisao importante.
- `docs/PROMPTS.md` para reaproveitar prompts do projeto.
- `docs/GLOSSARY.md` para termos, siglas e nomes internos.
- `docs/API.md` e `docs/DATA_MODEL.md` quando a tarefa envolver contratos, dados ou integracoes.

## Como Trabalhar

- Responda em portugues claro, salvo pedido diferente do usuario.
- Nunca use o caractere travessao (em dash, U+2014) em textos deste projeto, nem isolado nem com espacos ao redor. Separe frases com dois-pontos, ponto-e-virgula, virgula, parenteses ou hifen simples. O validador da skill acusa qualquer ocorrencia.
- Antes de editar, entenda o objetivo, o contexto e o estado atual.
- Prefira mudancas pequenas, focadas e faceis de revisar.
- Nao refatore fora do escopo da tarefa.
- Nao sobrescreva conteudo existente sem preservar, mesclar ou pedir confirmacao.
- Quando houver ambiguidade importante, registre a duvida e proponha uma decisao.
- Quando concluir trabalho relevante, atualize a memoria do projeto conforme a regra de gatilho abaixo.

## Nunca Inferir

IA nao alucina por capricho: ela preenche vazio. Quando faltar contexto obrigatorio para a tarefa:

- **Pergunte.** Nao preencha por inferencia plausivel.
- Resposta adiada ("Avançar") adia a pergunta; **nunca autoriza inventar** a resposta.
- Registre perguntas abertas explicitamente: como tarefa em `TASKS.md` ou na secao "Perguntas Abertas" da spec correspondente (quando o modulo de specs estiver ativo).
- Pergunta que **trava a tarefa** move a tarefa para a secao "## Aguardando Usuario" de `TASKS.md`, com `**Pergunta:**`, `**Resposta:** (A preencher.)` e o marcador `(bloqueada: AAAA-MM-DD)`. Enquanto a resposta nao chegar, a tarefa nao volta para "Proximas Tarefas" e ninguem preenche a lacuna por inferencia.
- Placeholder honesto ("(A preencher.)") e melhor que conteudo inventado.

## Onde Escrever Cada Coisa

- **`SESSION.md`**: o que **aconteceu** em data X. Cronologico. Inclui pendencias daquela sessao.
- **`MEMORY.md`**: o que o projeto **aprendeu**. Fatos persistentes nao-decididos (preferencias, licoes, refs externas).
- **`DECISIONS.md`**: o que foi **decidido** formalmente, com motivo e impacto.
- **`PROJECT_CONTEXT.md`**: o que o projeto **e**. Estrutura permanente; raramente muda.
- **`TASKS.md`**: o que esta **em aberto**. Fonte unica de verdade do backlog vivo. Tarefas usam ID `T-NNN`; o modelo esta no proprio arquivo. Tarefa concluida carrega evidencia de fechamento; tarefa parada por pergunta ao usuario fica em "Aguardando Usuario".
- **`CONSENSUS.md`**: debate entre modelos para chegar a um consenso. Apenas para duvidas reais.
- **`CHANGELOG.md`**: historico de mudancas relevantes na estrutura ou no produto.
- **`STACK.md`**: com o que o projeto e **construido** e onde consultar cada tecnologia (opcional; crie quando o projeto tiver codigo). Antes de resolver problema de stack, consulte a documentacao apontada la.
- **`specs/`**: o que **sera construido** em trabalho tamanho-feature (apenas quando o modulo de specs estiver ativo).

## Atualizacao Por Gatilho

Atualize apenas o arquivo cuja funcao foi acionada na sessao. Atualizar tudo a cada turno gera baixa adocao.

- Houve trabalho cronologico relevante? Atualize `SESSION.md`.
- Surgiu aprendizado persistente? Atualize `MEMORY.md`.
- Foi tomada decisao formal? Atualize `DECISIONS.md` (e copie do `CONSENSUS.md` se aplicavel).
- Tarefa entrou ou saiu do backlog? Atualize `TASKS.md`.
- Mudou estrutura ou contrato? Atualize `ARCHITECTURE.md`, `API.md` ou `DATA_MODEL.md`.
- Entrou, saiu ou mudou de versao alguma tecnologia ou pacote? Atualize `STACK.md` (se existir).
- Mudou o que o projeto e? Atualize `PROJECT_CONTEXT.md`.
- Mudanca relevante na estrutura ou no produto? Registre em `CHANGELOG.md`.
- Trabalho de uma feature avancou? Atualize o `Status` da spec em `docs/specs/` e mova as tarefas dela em `TASKS.md` (quando o modulo de specs estiver ativo).

Pendencias de sessao que sejam acionaveis devem virar tarefa em `TASKS.md` antes de fechar a sessao. `TASKS.md` e canonico; "Pendencias" em `SESSION.md` e snapshot historico daquela sessao.

## Evidencia De Fechamento

Tarefa concluida e afirmacao. Sem evidencia, e afirmacao sem lastro. Toda tarefa movida para "## Concluidas" em `TASKS.md` carrega uma sub-linha:

```md
- AAAA-MM-DD T-001: Descricao curta e acionavel. (spec: 0001-login-social)
  - Evidencia: tipo=comando; procedimento=<o que foi feito>; resultado=<o que saiu>
```

- `tipo` aceita `comando`, `revisao-manual` ou `conferencia`. Tarefa de conteudo, pesquisa ou decisao usa `revisao-manual` ou `conferencia`. Nunca invente um comando inexistente so para preencher o campo.
- Tarefa aberta pode declarar de antemao como pretende ser verificada, com `(verifica: <comando>)` no fim da linha. O marcador e opcional; declarado, vira contrato: a evidencia da tarefa concluida precisa registrar o resultado daquele comando.
- A exigencia nao e retroativa. A data em que ela passa a valer fica declarada uma vez em `TASKS.md`, no marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)`. Linha concluida antes dessa data fica como esta: registro historico nao vira alegacao sem evidencia.

O validador confere a forma da evidencia, nunca o conteudo. Evidencia colada sem conferencia real passa no script e falha no proposito.

## Memoria Da Sessao

`docs/SESSION.md` da continuidade entre sessoes de IA.

Antes de comecar trabalho relevante:

- leia a sessao mais recente;
- identifique o que foi feito;
- confira pendencias e proximo passo recomendado.

Ao finalizar trabalho relevante, adicione uma nova entrada no topo de `docs/SESSION.md` com:

- data;
- agente usado;
- objetivo;
- resumo do que foi feito;
- arquivos criados ou alterados;
- decisoes tomadas;
- pendencias (refletidas em `TASKS.md` se acionaveis);
- proximo passo recomendado, no formato: agente sugerido + motivo + nota de "qualquer agente serve se tiver contexto suficiente" quando aplicavel.

## Memoria Persistente

`docs/MEMORY.md` guarda fatos consolidados que valem "a partir de agora, sempre". O proprio arquivo descreve as regras detalhadas. Resumo:

- promova de `SESSION.md` para `MEMORY.md` apenas o que for util para sessoes futuras, reutilizavel e ja consolidado;
- fatos obsoletos devem ser marcados como substituidos, nao apagados;
- nao registre dados sensiveis;
- se um fato virar estrutural permanente, promova para `PROJECT_CONTEXT.md`.

## Consenso Entre Modelos

Use `docs/CONSENSUS.md` quando:

- modelos diferentes discordarem;
- houver decisao arquitetural ou de produto relevante;
- a tarefa tiver risco alto;
- o usuario pedir opiniao de outro modelo;
- a melhor solucao nao estiver clara.

Nao use para microdecisoes. Consenso por teatro deixa o fluxo lento e perde valor.

O registro deve separar:

- contexto da duvida;
- posicao de cada modelo;
- pontos de acordo;
- riscos;
- consenso final;
- decisao que deve ser copiada para `docs/DECISIONS.md`, se for relevante.

Cada entrada deve ter `**Status:** aberto | resolvido | arquivado`. Quando o status estiver aberto, inclua tambem `**Proximo passo:**` com dono claro, para evitar consenso parado sem responsavel.

### Independencia Declarada

Consenso so vale como segunda opiniao se as posicoes forem independentes. Modelo que le a posicao do outro antes de escrever produz concordancia por cortesia, e consenso fraco fica indistinguivel de consenso forte. Cada entrada declara como foi produzida:

- `**Metodo:** pareceres-independentes | debate-aberto`
- `**Exposicao previa a outras posicoes:** sim | nao`
- `**Rodada:** N de 3`

Na rodada 1, cada modelo preenche apenas a propria secao, sem ler as demais. Da rodada 2 em diante a exposicao previa e esperada e deve ser declarada como `sim`. Tres rodadas sem convergencia e o teto: escale para o usuario em vez de abrir a quarta.

Os tres campos sao autodeclarados. O validador checa presenca e valor permitido, **nunca veracidade**: nenhum script prova que um modelo nao leu a posicao do outro. O ganho e rastreabilidade, nao garantia.

### Regra De Desempate

Quando os modelos nao convergem:

1. **Usuario decide** sempre que estiver disponivel.
2. Na ausencia do usuario, prevalece a opcao de **menor risco reversivel**.
3. Se nenhuma opcao for facilmente reversivel, **pare e peca confirmacao humana**. Nunca tome sozinho um caminho irreversivel, caro, sensivel ou estrutural.

## Decisoes E Historico

- Registre decisoes importantes em `docs/DECISIONS.md`.
- Registre mudancas relevantes em `docs/CHANGELOG.md`.
- Mantenha `docs/TASKS.md` atualizado quando tarefas forem iniciadas, concluidas ou descobertas.

## Rotacao De Arquivos

`SESSION.md` e `CONSENSUS.md` crescem indefinidamente. Quando passarem de aproximadamente 20 entradas (ou ~30KB):

- mova as mais antigas para `docs/archive/SESSIONS-AAAA.md` ou `docs/archive/CONSENSUS-AAAA.md`;
- mantenha as 5 a 10 mais recentes no arquivo principal;
- atualize o indice em `docs/archive/README.md` com resumo curto do que cada arquivo arquivado cobre.

Opcional: se a secao "Concluidas" de `TASKS.md` ficar longa, mova as mais antigas para `docs/archive/TASKS-AAAA.md` seguindo a mesma logica.

## Validacao

Antes de finalizar, confira:

- se a tarefa pedida foi realmente atendida;
- se toda tarefa concluida nesta sessao carrega evidencia de fechamento;
- se os arquivos de memoria afetados pela funcao acionada foram atualizados;
- se pendencias acionaveis viraram tarefas em `TASKS.md`;
- se houve aprendizado promovido para `MEMORY.md` quando aplicavel;
- se nao houve mudanca fora de escopo;
- se testes, revisao manual ou validacao foram executados quando aplicavel;
- se ha pendencias que precisam ser comunicadas.

<!-- ai-project-structure:core:end -->

<!-- ai-project-structure:specs:start v2.3.0 -->
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

<!-- ai-project-structure:loop:start v2.3.0 -->
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

### Limites

- Uma tarefa por rodada, indicada no comando. O loop nunca escolhe sozinho no que trabalhar.
- Tarefa sem `(verifica:)` nao e elegivel: o loop recusa antes de chamar o agente.
- O loop nao escreve em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` nem em specs. O relatorio da rodada da o material; quem registra e voce.
- O aviso de parada e o exit code mais o relatorio em stdout. Som, notificacao ou webhook se compoem por fora.

O fluxo completo e o uso estao em `references/loop.md` da skill `ai-project-structure`.
<!-- ai-project-structure:loop:end -->

## Regras Do Projeto

- Excecao a regra de raiz minima: `README.md`, `LICENSE` e `.gitignore` sao permitidos na raiz porque este repositorio e publicado no GitHub (`github.com/adejaimejr/ai-project-structure`). O `README.md` da raiz e apresentacao para visitantes; regras de agente continuam apenas neste arquivo.
