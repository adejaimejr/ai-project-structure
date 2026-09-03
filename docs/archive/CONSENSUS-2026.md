# CONSENSUS 2026

Debates antigos de `docs/CONSENSUS.md`, rotacionados em 2026-09-02 e de novo em 2026-09-03, pela regra de "Rotacao De Arquivos" do `AGENTS.md`.

Cobre os dois debates de 2026-04-25, a revisao da spec 0003 de 2026-09-02, e do dia 2026-09-03 o achado `0005-A1` e a rodada das seis perguntas da spec 0006, todos `resolvido`, mais as rodadas de P-7/P-8 e P-9 da spec 0006, que continuam `aberto` (calibragem com o usuario, T-053) e foram rotacionadas por tamanho. Os de 2026-04-25 sao anteriores a versao 2.2.0 e nao trazem os campos declarativos de metodo, exposicao previa e rodada; o de 2026-09-02 e a primeira entrada do repositorio que os traz.

<!-- REVAL-5, resolvida sem defeito, rotacionada em 2026-09-03 por tamanho do CONSENSUS.md; as outras seis entradas REVAL-* continuam la. -->

## 2026-09-03 - REVAL-5: os tres fluxos funcionam contra a copia instalada; o que sobra e texto

**Achado:** REVAL-5

**Status:** resolvido

**Proximo passo:** nenhum; o residuo esta em REVAL-1 (data em Concluidas) e REVAL-6 (ARCHITECTURE.md).

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** nao

### Contexto

- Superficie 5, executada de verdade e nao lida: `claude -p --permission-mode bypassPermissions --model opus --effort high` em diretorios descartaveis, com a skill disparando implicitamente pela copia em `~/.claude/skills/ai-project-structure` (2.5.1). Quatro rodadas: scaffold minimal com specs, atualizacao de `evals/fixtures/v1-project`, criacao de spec com todas as respostas em "Avançar", e pedido de ativar o loop em projeto sem portao.

### O Que Foi Encontrado

- Scaffold: bloco core e bloco specs byte a byte iguais aos assets, `PROJECT_CONTEXT.md` com nome e objetivo, data de adocao preenchida, primeira entrada de sessao, nada de `partials/` copiado, `--strict` exit 0.
- Atualizacao v1: core aplicado, pontes trocadas, IDs `T-001` a `T-004`, secao Aguardando e marcador de adocao com a data da atualizacao, entrada antiga de consenso preservada sem campos retroativos, `--strict` exit 0. Duas arestas: "Regra Local Do Time" virou secao `##` irma de "Regras Do Projeto" (o texto do fluxo diz "mova para Regras Do Projeto", ambiguo entre dentro e abaixo); e `T-004` migrada para Concluidas ficou sem data, que e o furo de REVAL-1.
- Spec com "Avançar": quatro perguntas em "Aguardando Usuario" com `Pergunta`, `Resposta` e `(bloqueada:)`, spec em `Rascunho` com placeholders honestos, `--progress` contando 4 perguntas.
- Loop em projeto sem portao: recusado com o motivo certo, `AGENTS.md` intocado, pergunta registrada em Aguardando.

### Disposicao

- Nenhum defeito de fluxo. Dois ajustes de texto entram em T-062: `references/atualizacao.md` dizer se secao resgatada vira item **dentro** de "Regras Do Projeto" ou secao abaixo, e o passo 7 de migracao mandar prefixar data nas concluidas quando ela for conhecida, ou deixar sem data e dizer que a linha nao e cobrada.

### Revalidacao

- Grok e Codex ficaram para a verificacao dos achados; como nao houve achado de fluxo, o que se pede e a leitura das duas arestas por outra familia na proxima rodada.

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma.

<!-- Rotacionadas em 2026-09-03 (revalidacao adversarial). As duas entradas abaixo continuam com Status aberto: a calibragem esta com o usuario em T-053 de docs/TASKS.md. Foram movidas por tamanho, nao por conclusao. -->

## 2026-09-03 - P-9 da spec 0006: quando a minuta e escrita

**Status:** aberto

**Proximo passo:** o usuario ratifica o desenho, que teve 3 de 3, e decide as duas divergencias: se a retomada apos interrupcao e automatica ou exige palavra humana, e onde o bruto mora **durante** a rodada.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

### Contexto

P-9 nao e pergunta de desenho novo: e **conflito entre duas decisoes ja ratificadas** no mesmo dia. A DEC-003 manda o agente nao ver posicoes contemporaneas; a DEC-006 manda o da rodada 2 ver as anteriores na integra; e nenhuma das duas escolheu o instante da gravacao.

Duas ressalvas de independencia, as duas contra a forca desta rodada:

- **Quem descobriu o conflito foi o Grok**, na rodada anterior. Reter aquela entrada fez ele responder sem lembrar do proprio argumento, o que preserva a cegueira do raciocinio, mas a spec que ele leu credita o achado a ele por nome. Ele sabia que a pergunta era dele.
- **O enunciado e a transcricao que o Claude fez do achado do Grok.** Os tres responderam a versao de um dos tres. Se a transcricao estreitou o problema, os tres herdaram o estreitamento e nenhum tinha como perceber. E o Problema 3 da spec, agora na formulacao da pergunta em vez de na transcricao da resposta.

Posicao do Claude selada antes dos dois rodarem. Codex em `codex exec -s read-only -m gpt-5.6-sol`, esforco `high`. Grok em `cursor-agent -p --mode ask --force --model cursor-grok-4.6-xhigh`. Copia do repositorio com o corpo da entrada de P-7 e P-8 retido, pela DEC-003.

### Pergunta Ou Decisao

Quando a minuta e escrita no `CONSENSUS.md`, e o que acontece com o material da rodada em caso de interrupcao e de colisao entre duas execucoes.

### Posicao Do Claude

Selada antes das demais.

- **Tres artefatos, tres momentos.** Bruto de cada agente escrito assim que aquele agente termina, em diretorio nao visivel aos demais; manifesto incremental no mesmo lugar; minuta no `CONSENSUS.md` escrita **uma vez so**, no fim.
- **O ponto que levantei:** o vazamento nao vem do momento, vem do lugar. Tratar "quando escrever" sem tratar "onde" leva a resposta cara e errada, que e segurar tudo em memoria ate o fim.
- **Interrupcao:** repositorio fica intacto, diretorio de execucao fica com os brutos pagos. A proxima execucao **nao retoma sozinha**: reporta e para, com o precedente do `loop.sh`, que nao retoma rodada.
- **Resolve ou adia:** admiti que **adia parcialmente**. Se o diretorio de execucao estiver dentro do projeto e o agente tiver leitura do repositorio, que a DEC-003 permite, ele pode ler o bruto de quem terminou antes. Ou o diretorio fica fora do projeto durante a rodada, ou a DEC-003 passa a excluir explicitamente o diretorio corrente. Preferi a primeira, porque depender de o agente respeitar pasta proibida e voltar a confiar no prompt.
- **Decisao que muda:** nenhuma de valor; a **DEC-003 fica incompleta**, porque diz o que isolar e nao diz onde as posicoes moram durante a rodada. Isso e omissao, nao contradicao com a DEC-006.

### Posicao Do Codex

- **Barreira de rodada, em tres fases.** Antes de comecar: lock exclusivo por projeto, `run-id`, pacote de entrada imutavel por agente, e manifesto inicial numa **area persistente do orquestrador, fora do repositorio e inacessivel aos agentes**. Durante: nada em `CONSENSUS.md`, nada com posicao contemporanea em caminho visivel, e cada agente que termina tem stdout, stderr, exit code e metadados salvos na hora com arquivo temporario, `fsync` e rename atomico. No fim: manifesto selado, minuta gerada pela primeira vez, e publicacao.
- **Ordem de publicacao, que so ele argumentou:** o bundle (`docs/consensus/runs/<run-id>/`) e publicado **antes** da entrada. Assim, interrupcao entre as duas deixa bundle sem entrada, que da para finalizar, e **nunca** deixa entrada apontando para evidencia inexistente.
- **Interrupcao com retomada condicional:** se pergunta, modo, rodada, participantes, comandos e hashes dos insumos forem identicos, retoma o mesmo `run-id`, reusa as respostas completas e chama so quem falta. Se qualquer insumo diferir, recusa a retomada automatica. Saida parcial nunca vira posicao por inferencia.
- **Colisao:** lock exclusivo por projeto durante **toda** a rodada, e nao so na escrita final. Segunda execucao falha rapido informando qual run esta ativo. Lock por arquivo nao pode ser recuperado so por idade: tem de conferir identidade do processo.
- **Licoes que tirou do `loop.sh`, as tres conferidas aqui:** ele so muda o estado canonico depois do portao; o `TMP` com `trap 'rm -rf' EXIT` (linhas 86-87) serve para dado descartavel e nao para parecer ja pago; e o `.loop-pergunta` de nome global mostra por que arquivo temporario sem `run-id` nao serve para execucao concorrente.
- **Risco novo, e e o mais grave da rodada:** o bruto pode conter segredo, credencial ou dado pessoal encontrado no repositorio. Como a DEC-001 exige preservacao literal e a P-8 aponta para artefato versionado, **redacao automatica alteraria justamente a evidencia que deveria ser conferivel**. Sem politica de dados sensiveis, consenso automatizado vira "mecanismo permanente de exfiltracao para o historico Git".

### Posicao Do Grok

- **Tres artefatos, tres momentos**, com a mesma estrutura, e uma frase que os outros dois nao escreveram: "a minuta em `CONSENSUS.md` nao e o unico arquivo que vaza".
- **O corte que resolve o conflito:** **publicado = anterior; nao publicado = contemporaneo.** A DEC-003 e a DEC-006 falavam de momentos diferentes, e nenhuma tinha escolhido o instante da gravacao. Com esse criterio, enquanto a minuta desta rodada nao foi gravada, o contemporaneo ainda nao e anterior.
- **Argumento que sozinho ja proibe publicar cedo, e que veio de uma decisao ratificada:** a DEC-005 tornou `N=1` valido. Entao **minuta a meio, com 1 de 3 posicoes, e indistinguivel de uma corrida `N=1` concluida**. Nao e so vazamento: e ambiguidade de leitura.
- **Onde o bruto mora:** in-repo desde a volta de cada agente, fora do `.gitignore` como a P-8 exige, mas **fora da arvore em que os agentes da rodada corrente executam**. Ele nomeia o triangulo: P-8 manda o bruto sobreviver a sessao, a DEC-003 manda o colega nao ve-lo agora, e bruto so em `/tmp` perde trabalho na interrupcao, "o que ja aconteceu na rodada das seis perguntas".
- **Interrupcao sem retomada automatica e sem descarte automatico:** cadeado presente faz a proxima execucao recusar e pedir `--retomar` ou `--descartar`. "`--descartar` e decisao humana: joga fora trabalho pago; o script nao infere isso." Se o sidecar ja tem os brutos e a minuta nao saiu, a retomada **monta a minuta a partir do bruto, sem nova chamada**.
- **Sobre o `loop.sh`:** apontou que o paralelo certo e o `TASKS.md` so mudar no fecho, e o errado e a politica de leftover, porque "apagar leftover e perder trabalho" quando o leftover e parecer pago. E notou que o `loop.sh` **nao tem** protecao de colisao, entao dois loops na mesma tarefa correm em `TASKS.md`: "nao copiar o buraco".
- **Risco novo, conferido aqui:** `loop_task.py` grava `TASKS.md` com `write_text` direto (linha 147), que nao e atomico, e crash no meio pode **rasgar o arquivo de memoria**. A spec nao lista arquivo de memoria partido.
- **Alerta sobre o proprio check:** tratar diretorio de corrida incompleto como ERRO puniria interrupcao e vazaria cobranca para quem so teve uma corrida morta. Tem de ser AVISO, e so com o marcador de automacao.

### Pontos De Acordo

**3 de 3 no desenho.** As tres posicoes chegaram, separadamente, a mesma arquitetura:

- **Tres artefatos com momentos diferentes**, e a minuta escrita **uma vez so, no fim**, por substituicao atomica do arquivo inteiro e nunca por append no meio do Markdown.
- **Nada com posicao contemporanea em caminho que um agente ainda em curso consiga listar.** Os tres disseram, com palavras diferentes, que isolamento pedido no prompt nao fecha vazamento por filesystem.
- **Interrupcao deixa o `CONSENSUS.md` byte a byte como estava.** Nunca meia rodada no repositorio.
- **O bruto de quem ja respondeu nao pode ser descartado.** Chamada paga.
- **Nenhuma das seis decisoes precisa ser revertida.** Os tres classificaram o conflito como **lacuna**, e nao contradicao: falta uma DEC nova sobre o instante da gravacao.
- **Nenhum check de forma prova o momento da escrita.** Isso e teste de orquestrador, com agente falso, e os tres desenharam variacoes do mesmo teste: plantar token unico no bruto de um agente e conferir que o artefato do outro nao o contem.

Convergencia 2 de 3, com o Claude fora: **lock exclusivo por projeto durante toda a rodada**. Codex e Grok pediram; o Claude so propos nome de diretorio a prova de colisao, que e mais fraco.

### Riscos E Tradeoffs

- **Divergencia 1, retomada.** Codex aceita retomada **automatica** quando pergunta, modo, rodada, participantes, comandos e hashes forem identicos. Claude e Grok exigem **palavra humana** (`--retomar` ou `--descartar`), com o Grok sendo explicito: descartar trabalho pago e decisao de pessoa. E 2 a 1 pela palavra humana, e a posicao do Codex e a que preserva mais trabalho automaticamente.
- **Divergencia 2, onde o bruto mora durante a rodada.** Codex e Claude o mantem **fora do repositorio** ate o fim, e publicam no fecho. Grok o quer **in-repo desde o inicio**, fora da arvore de execucao, argumentando que a P-8 exige que ele sobreviva a sessao e que `/tmp` ja perdeu material nesta propria spec. As duas atendem a durabilidade; elas diferem em quanto confiam na separacao de arvore.
- **O risco de segredo no bruto nao tem solucao proposta por ninguem.** O Codex mostrou a armadilha inteira: a DEC-001 exige literal, a P-8 exige versionado, e redigir automaticamente destruiria a evidencia. As tres posicoes juntas nao produziram saida para isso.
- **A rodada tem n=3 e um enquadramento so**, e desta vez com agravante: o enunciado e a transcricao, feita por um dos tres, do achado de outro dos tres.
- Dois defeitos de codigo ja publicado apareceram como efeito colateral: escrita nao atomica em `TASKS.md`, e ausencia de protecao de colisao no `loop.sh`. Nenhum dos dois e da spec 0006.

### Consenso Final

**O desenho tem 3 de 3 e esta pronto para virar DEC**, com o criterio operacional do Grok como o coracao dela: **publicado e anterior, nao publicado e contemporaneo**. A DEC-003 e a DEC-006 nunca se contradisseram; elas falavam de momentos diferentes, e faltava alguem escolher o instante da gravacao.

Concretamente: lock exclusivo por projeto na abertura; bruto e manifesto gravados assim que cada agente encerra, em lugar que os agentes da rodada corrente nao alcancam; minuta escrita uma vez so, no fim, por substituicao atomica do arquivo inteiro; interrupcao deixando o repositorio intacto e o material pago preservado; e teste de orquestrador com token plantado, porque nenhum check de forma alcanca o momento da escrita.

**Duas calibragens para o usuario:** retomada automatica com insumos identicos (Codex) ou palavra humana sempre (Claude e Grok, 2 a 1); e bruto fora do repositorio ate o fecho (Codex e Claude) ou in-repo fora da arvore de execucao (Grok).

**Uma coisa que a rodada nao resolveu e ninguem deve fingir que resolveu:** o bruto pode conter segredo do repositorio, e a combinacao de "preservar literal" com "versionar" cria caminho de exfiltracao permanente para o historico. Isso precisa de decisao propria antes de qualquer linha de codigo.

### Decisao Para Registrar Em DECISIONS.md

Nada ainda. Quando o usuario ratificar, isto vira DEC-007 na spec 0006. **Uma parte deve subir para `docs/DECISIONS.md`**: a regra de que arquivo de memoria do projeto se escreve por substituicao atomica, e nunca por escrita direta, porque ela vale para o `loop_task.py` que ja esta publicado e para qualquer automacao futura, e nao so para esta operacao.

## 2026-09-03 - P-7 e P-8 da spec 0006: forma da entrada e proveniencia

**Status:** aberto

**Proximo passo:** o usuario ratifica ou vira as duas. As tres posicoes convergiram no **o que** e divergiram no **quanto**, entao nao ha empate a desfazer, ha calibragem a escolher.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

### Contexto

Rodada 1 cega sobre duas perguntas **novas**: P-7 nasceu da rodada anterior e P-8 foi registrada depois dela. Ninguem tinha opinado sobre nenhuma das duas.

Primeiro uso da DEC-003, ratificada horas antes. Os agentes rodaram numa copia do repositorio em que o corpo da entrada da rodada anterior foi **retido**, com uma nota no lugar dizendo que a omissao era proposital. Reter sem avisar teria feito os dois concluirem que nenhuma rodada havia acontecido, que e falso. O modelo de debate e o de achado ficaram na copia, porque **sao o objeto de P-7**.

A posicao do Claude foi selada antes dos dois rodarem. Codex em `codex exec -s read-only -m gpt-5.6-sol`, esforco `high`. Grok em `cursor-agent -p --mode ask --force --model cursor-grok-4.6-xhigh`, read-only por construcao.

### Pergunta Ou Decisao

**P-7:** a forma da entrada de `CONSENSUS.md` fica fora do escopo da spec 0006, sendo que nem o modelo de debate nem o de achado representam N agentes, falha individual ou hash de insumo? **P-8:** proveniencia (comando, exit code, caminho do artefato) entra no escopo?

### Posicao Do Claude

Selada antes das demais.

- **P-7: a forma muda nesta spec.** Mudei de ideia em relacao ao que eu mesmo escrevi no "Fora Do Escopo": a DEC-004 tornou aquilo insustentavel, porque com debate e achado dentro sao duas formas a acomodar. Proposta: trocar os headings fixos por um por participante, `### Posicao De <rotulo>`, com o rotulo vindo da chamada. Aceito perder: entradas antigas ficam com a forma velha e o validador aceita as duas por um tempo, que e divida e nao elegancia.
- **P-8: entra, e e o que faz a DEC-002 valer alguma coisa.** Sem proveniencia gravada, "a execucao comprova" e frase falsa, porque nada distingue campo escrito pela execucao de campo digitado. Mora num sidecar ao lado do bruto que a DEC-001 ja manda preservar, e nao dentro do `CONSENSUS.md`, que ja bate na rotacao com duas entradas.
- **Buraco que declarei nao saber resolver:** o validador nao tem como saber se uma entrada foi escrita por automacao ou na mao. Ou a entrada declara isso num campo, e ai a verificacao volta a depender de autodeclaracao, ou o check so vale para quem ja tem o ponteiro.
- Conflito que apontei entre as ratificadas: DEC-001 manda preservar o bruto e nao diz onde; DEC-002 manda escrever no `CONSENSUS.md`; P-8 pergunta onde mora a proveniencia. As tres esbarram na mesma lacuna, e talvez a pergunta certa nao fosse P-8 e sim "onde mora o material da rodada".

### Posicao Do Codex

- **P-7: a forma entra no escopo**, com esquema **versionado** e ativado por `**Origem:** automacao-consenso/v1`, sem invalidar entradas manuais antigas. Cada invocacao vira entrada propria com `**Tipo:** debate | achado`, `**Execucao:** <run-id>`, participantes por id arbitrario, um bloco por participante com resultado `sucesso | falha`, debate com `N>=2`, achado com `N>=1` e blocos repetiveis, vinculo entre revalidacoes sucessivas pelo identificador do achado e pelo `run-id` anterior, e secoes de julgamento vazias.
- **P-8: entra**, com pasta canonica por execucao (`docs/consensus/runs/<run-id>/`) contendo `manifest.json`, os insumos efetivamente fornecidos a cada agente, stdout, stderr e registros de falha. A entrada **repete** por participante o comando (como vetor JSON de argumentos), o diretorio, o exit code, o caminho do bruto, o SHA-256 do insumo e da saida, e o caminho do manifesto. O manifesto e a fonte canonica; os campos da entrada sao projecao deterministica conferivel. Argumento: um sidecar **sem** esses campos na entrada contrariaria a DEC-002, que ja autorizou escrever os comandos.
- Propos treze codigos de diagnostico, e defendeu que para entrada automatizada eles sejam **ERRO** e nao aviso, "pois ali a forma e contrato da operacao".
- **Achados de codigo, os tres conferidos aqui antes de aceitos:** `check_consensus_declaration` nao diagnostica `Rodada` **ausente**, porque retorna calado; o formato usa `re.match` e nao `fullmatch`, entao `1 de 1` seguido de lixo passa; e o `Modelo De Debate` do `docs/CONSENSUS.md` da raiz **nao tem** `Metodo`, `Exposicao previa` nem `Rodada`, que o `AGENTS.md` exige e o asset da skill ja traz.
- Correcoes a criterios de aceite da spec: "N artefatos de posicao" esta errado, o certo e **N artefatos de execucao**, dos quais so os sucessos contem posicao; e "o artefato nao contem texto das outras posicoes" e inadequado para rodada 2, porque ali as posicoes anteriores sao **exigidas** pela DEC-006, e o que se proibe sao as **contemporaneas**.
- Conflito que apontou entre ratificadas: a DEC-001 exige posicao **sem resumo**, e copia literal em Markdown e insegura, porque a saida pode trazer heading, cerca ou o travessao que o projeto proibe. Falta definir um escape reversivel e deterministico.

### Posicao Do Grok

- **P-7: a pergunta esta mal posta como binario.** Partiu "forma" em tres camadas que hoje ja nao coincidem: os campos declarativos da 2.2.0, os headings de posicao, e o que o validador de fato cobra. Recomendacao: os campos da 2.2.0 **ficam fora**, os headings **entram** nas duas formas, e o validador so ganha check novo em entrada produzida pela automacao. Concretamente: `### Posicao De <id>` no debate, `### Revalidacao De <id>` no achado, e `### Falha De <id>` quando o agente nao produziu posicao.
- **O achado que mais muda a pergunta, conferido aqui:** o validador **nao cobra heading nomeado nenhum**. Nao existe codigo exigindo `Posicao Do Codex` nem uma `Revalidacao` unica. As unicas exigencias de heading no script inteiro sao as de `SESSION.md` e a de "Por Que Nada Pegou Antes". "O gargalo e o template, nao o contrato do script."
- **P-8: entra, e nao e um terceiro pacote**, e o que impede DEC-001 e DEC-002 de nascerem autodeclaracao do script. Sidecar por rodada com bruto e manifesto, mais **ponte** na minuta: `### Proveniencia` com o caminho do sidecar e, por agente, id, exit code e caminho. O comando integral fica no manifesto. Justificativa para nao engolir o transcript: colocar o bruto dentro do `CONSENSUS.md` quebra a rotacao de ~20 entradas ou ~30KB.
- Propos oito codigos, todos **AVISO**, cobrados so com `Origem: automacao`. Entre eles, um que os outros dois nao propuseram: `CONSENSO-CAMPOS-INCOERENTES`, cruzando manifesto e campos da 2.2.0 nos pontos que a DEC-006 torna deterministicos (modo cego implica `Exposicao previa: nao`; rodada `>=2` implica `sim`). Argumento: **essa fatia e veracidade de processo**, e e a unica que o script passa a poder cobrar sem contrariar o comentario de `check_consensus_declaration`, que promete nunca checar veracidade.
- **Conflito entre duas ratificadas, que ninguem mais viu:** DEC-003 versus DEC-006 no **momento da escrita**. Na rodada 2 o agente **deve** ver as posicoes anteriores e **nao pode** ver as contemporaneas. Se o orquestrador gravar a minuta no repositorio no meio da rodada, o repositorio visivel vaza o contemporaneo. As seis decisoes nao escolhem quando escrever.
- Risco de rotacao que so ele levantou: o sidecar nao e o `CONSENSUS.md`. Arquivar a entrada e deixar o bruto para tras quebra o teste da DEC-001, que e conferir o campo olhando o bruto **ao lado**.
- Recusa explicita: nao aceita `gitignore` no bruto, "senao o teste ao lado morre na sessao seguinte".

### Pontos De Acordo

**As tres convergem no que fazer, e divergem em quanto.** Nao ha empate a desfazer.

- **P-7: 3 de 3, a forma entra no escopo.** Os tres recusaram encolher o requisito. Os tres chegaram, separadamente, a secao repetivel por participante com id arbitrario: o Claude escreveu `### Posicao De <rotulo>`, o Grok `### Posicao De <id>`, e o Codex "participantes identificados por IDs arbitrarios, sem secoes fixas".
- **P-7: 2 de 3 no gatilho opt-in, e o terceiro nao contradiz.** Codex e Grok propuseram, sem combinar, um marcador `**Origem:**` que faz o check novo valer so para entrada automatizada, preservando o criterio de que projeto que nao automatiza nao ganha cobranca. O Claude tinha declarado esse exato problema como "buraco que nao sei resolver". Os outros dois resolveram.
- **P-8: 3 de 3, proveniencia entra.** Sidecar com bruto e manifesto, fora do `CONSENSUS.md`, com ponte dentro. Os tres deram o mesmo motivo de fundo: sem isso, os campos escritos pela automacao voltam a ser autodeclaracao, so que do script.
- **Fora do que foi perguntado, 2 de 3:** Codex e Grok apontaram que a linha do "Fora Do Escopo" sobre nao mexer na forma virou **letra morta** depois da DEC-004, e que ela hoje se anula com a linha do "Incluido".

### Riscos E Tradeoffs

- **A divergencia real esta no quanto a entrada repete do manifesto.** Codex quer comando, hashes de insumo e saida, e diretorio **dentro** da entrada, argumentando que a DEC-002 autorizou escrever comandos e que sidecar sem isso a contraria. Grok quer o comando integral so no manifesto e uma ponte curta na entrada, argumentando rotacao e leitura humana. O Claude ficou no meio, sem tratar do ponto. **E escolha de calibragem, e as duas leituras da DEC-002 sao defensaveis.**
- **Segunda divergencia: nivel dos diagnosticos.** Codex quer ERRO para entrada automatizada, porque ali a forma e contrato da operacao. Grok quer AVISO, por simetria com todo o resto de consenso. O projeto tem precedente dos dois lados.
- **O conflito DEC-003 versus DEC-006 nao tem dono.** O momento da escrita nao foi decidido por nenhuma das seis, e nenhuma tarefa cobre isso hoje.
- **Rodada com n=3 e um enquadramento so**, de novo: as duas perguntas foram redigidas pelo Claude, e a de P-7 foi redigida como binario, que o Grok recusou.
- **A transcricao continua sendo do modelo criticado.** O risco registrado na rodada anterior nao foi resolvido por esta: quem leu as tres posicoes e escreveu este resumo foi um dos tres.

### Consenso Final

**As duas perguntas tem resposta convergente, e o que falta e voce escolher a calibragem.**

**P-7, com 3 de 3:** a forma entra no escopo desta spec, com secao repetivel por participante e id arbitrario nas duas formas, secao propria para agente que falhou, e check novo valendo **so** para entrada automatizada, por marcador opt-in. O que barateia a decisao: o validador nunca exigiu heading nomeado, entao o congelamento em Codex, Claude e Gemini esta no template e nao no contrato, e mudar custa menos do que a spec supunha.

**P-8, com 3 de 3:** proveniencia entra no escopo, com sidecar por rodada guardando bruto e manifesto, e ponte na entrada. O bruto nao pode ser ignorado pelo git, senao o teste da DEC-001, conferir o campo olhando o bruto ao lado, morre na sessao seguinte.

**Duas calibragens para voce decidir**, e as duas mudam trabalho: quanto do manifesto a entrada repete (Codex quer comando e hashes dentro, Grok quer ponte curta), e se os diagnosticos novos sao ERRO ou AVISO em entrada automatizada.

**Um conflito entre decisoes ja ratificadas, achado pelo Grok e sem dono:** DEC-003 e DEC-006 nao escolhem o **momento da escrita**, e escrita incremental no meio da rodada vaza posicao contemporanea pelo proprio repositorio.

### Decisao Para Registrar Em DECISIONS.md

Nada ainda. As duas viram DEC na spec 0006 quando o usuario ratificar, junto com a calibragem que ele escolher. Nenhuma das duas parece ter impacto alem da spec, ao contrario da DEC-002, que precisou subir porque mexia no alcance da 0004/DEC-019.

## 2026-09-03 - As seis perguntas da spec 0006 (automacao do consenso)

**Status:** resolvido

**Resolvido em:** 2026-09-03. O usuario ratificou as seis, tanto as tres unanimes quanto as tres de maioria, e elas viraram DEC-001 a DEC-006 em `docs/specs/0006-automacao-do-consenso.md`. Ficaram fora da ratificacao, e seguem em T-053: P-7, sobre a forma da entrada, e P-8, sobre proveniencia entrar no escopo.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

### Contexto

Primeira vez que este projeto roda uma rodada de consenso de verdade cega, e ela e sobre a spec que quer automatizar exatamente isso. Foi feita na mao, que e o Problema 2 da propria spec.

Como a cegueira foi obtida, para ela ser conferivel e nao so declarada:

- A posicao do Claude foi escrita **antes** de qualquer agente rodar e selada em arquivo fora do repositorio. Escrever depois seria `debate-aberto` disfarcado de parecer independente.
- Claude e Codex receberam o **mesmo** arquivo de prompt, e rodaram em processos separados, com as saidas em arquivos distintos fora do repositorio. Nenhum dos dois teve como ler a saida do outro.
- Comando do Codex: `codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high"`. O sandbox `read-only` garante que ele nao escreveu nada; **nao** garante que ele nao leu nada, e essa distincao foi levantada pelo proprio Codex na critica dele.

Limitacao declarada, e ela e material: o Claude e autor da spec e das perguntas, entao a posicao dele nao e independente do enquadramento. Isso nao da para consertar nesta rodada, so declarar.

Segunda limitacao, apontada pelo Codex e aceita: o artefato bruto de cada agente ficou fora do repositorio e nao foi preservado. As posicoes abaixo sao resumo fiel, conferido, mas resumo. E exatamente o que a resposta dele a P-1 diz que nao deveria acontecer.

### Pergunta Ou Decisao

As seis perguntas abertas de `docs/specs/0006-automacao-do-consenso.md`: o que a operacao entrega (P-1), se ela pode escrever em `CONSENSUS.md` (P-2), que isolamento garantir (P-3), se cobre debate, achado ou os dois (P-4), quantos agentes e quem escolhe (P-5), e se a rodada 1 cega e obrigatoria por construcao (P-6).

### Posicao Do Claude

Selada antes das demais rodarem.

- **P-1:** (b), a entrada montada com posicoes preenchidas e as secoes de julgamento em branco. (a) nao resolve o Problema 2, porque o custo que trava a segunda opiniao e o de transcrever e formatar, nao o de rodar o agente. (c) e onde apodrece: quem sintetiza acordo esta julgando, e vira participante nao declarado com poder de edicao sobre a fala dos outros. Criterio proposto: a operacao pode preencher qualquer campo cuja veracidade uma pessoa consiga conferir olhando o artefato bruto ao lado. A entrada precisa apontar para o bruto, nunca substitui-lo.
- **P-2:** sim, com excecao declarada, e nao por heranca automatica da DEC-019. A razao daquela decisao era "um agente so"; com N agentes isolados ela nao sobrevive. A excecao e estreita: escreve posicoes e campos declarativos, nao escreve julgamento, nunca escreve `Status: resolvido`. E os campos `Metodo`, `Exposicao previa` e `Rodada` passam a ser escritos **pela execucao**, com base no que ela fez, e nao copiados de um valor que o usuario digitou. E o unico jeito de eles pararem de ser autodeclarados.
- **P-3:** (c), com discordancia do proprio enunciado: "sem acesso ao repositorio" e forte demais e prejudica a qualidade. A rodada de ontem foi boa porque o Codex leu o codigo e as fixtures; sem isso ele opinaria sobre um resumo meu, que e o acoplamento que se quer quebrar. Proposta: leitura do repositorio sim, escrita nao, posicoes dos outros nao, com isolamento por **ordem de escrita** (todos leem o estado anterior a rodada, e a rodada so escreve quando todos terminaram).
- **P-4:** so debate na primeira versao, achado explicitamente fora. Motivo desconfortavel: existe **um** achado registrado neste repositorio e fui eu que escrevi ontem. Desenhar automacao para uma forma com n=1 e desenhar para o proprio palpite.
- **P-5:** lista de perfis nomeada em `docs/MEMORY.md`, sem N fixo na ferramenta, dois a tres agentes por padrao. Agente que falha nao derruba a rodada, e a ausencia dele fica escrita: rodada com dois de tres respondendo e legitima, rodada que silencia o terceiro e mentira por omissao.
- **P-6:** os dois modos, com a rodada 1 cega como padrao. O que importa e que o modo **determine** o valor de `Exposicao previa` em vez de o usuario digitar: passou as outras posicoes no prompt, sai `sim`; nao passou, sai `nao`.
- **Onde achei a propria spec fraca:** P-3 mistura isolamento entre agentes com isolamento do repositorio, e as duas coisas nao andam juntas. E nenhuma pergunta cobre o caso de dois agentes concordarem por terem o mesmo vies de treino: isolamento por construcao nao produz independencia estatistica, e a spec fala como se produzisse.

### Posicao Do Codex

`gpt-5.6-sol`, esforco `high`, sandbox `read-only`.

- **P-1:** alternativa combinada, recusando a exclusao da pergunta: preservar o material bruto de cada agente **e** gerar uma minuta deterministica, com posicoes reproduzidas sem resumo e campos de julgamento como `(A preencher.)`. O bruto da auditabilidade; a minuta elimina a transcricao feita pelo modelo criticado. Aceita perder: a entrada nao sai concluida, e os artefatos ocupam espaco.
- **P-2:** sim, mas **so um orquestrador mecanico** pode escrever, por opcao explicita, registrando pergunta, posicoes literais, falhas, comandos, hashes, metodo, exposicao e rodada. Nao escreve entrada com menos de duas posicoes validas. Correcao direta ao Claude: "o fundamento nao e haver N agentes, mas separar os agentes opinantes do escritor deterministico". Aceita perder: complexidade do escritor, necessidade de append atomico, e entradas abertas acumuladas se a sintese humana nao acontecer.
- **P-3:** alternativa as tres opcoes: sessao nova e snapshot privado, imutavel e identico dos insumos autorizados, com o snapshot da rodada 1 excluindo as posicoes da rodada, e os resultados fora do alcance dos demais ate todos terminarem. "Sandbox somente-leitura impede escrita, nao leitura." Manifesto e hashes para conferir quais insumos entraram. Aceita perder: portabilidade e simplicidade.
- **P-4:** **os dois**, sobre um coletor comum e dois renderizadores. Em achado, revalidar **somente uma disposicao ja existente**, sem criar o achado nem decidir a disposicao. Fazer so debate ignora o unico caso doloroso observado; fazer so achado entrega ferramenta especializada demais. Aceita perder: entrega inicial maior e mais lenta, com fixtures proprias para dois formatos.
- **P-5:** N derivado de lista explicita **por chamada**, aprovada pelo usuario antes de executar, sem N padrao oculto, exigindo ao menos duas configuracoes distintas de ferramenta ou modelo. Grupos nomeados em `MEMORY.md` sao conveniencia resolvida pelo agente de chat: "o executor nao deve interpretar Markdown nem escolher modelos". A lista explicita ja funciona como teto local de custo. Aceita perder: a conveniencia da rodada automatica com revisores padrao.
- **P-6:** os dois modos, rodada 1 obrigatoriamente cega por construcao, rodada 2 em diante em modo explicito recebendo os artefatos indicados. A operacao **nunca deduz** sozinha o numero da rodada nem quais posicoes anteriores fornecer. Aceita perder: interface unica e permissiva.

Criticas a spec, resumidas (as que mais mudam trabalho):

1. **O reuso do `loop.sh` esta superestimado.** O conceito de comando neutro se reaproveita; o script pressupoe tarefa, mutacao de arquivos, portao, tentativas e `.loop-pergunta`. **Conferido no codigo antes de aceitar:** `loop.sh:145` decide se o agente fez algo com `find -type f -newer`, e um agente de parecer nao escreve nada no projeto, entao cairia no `exit 4` da DEC-014 sempre. A critica procede inteira.
2. **A DEC-001 foi generalizada alem do que ela prova.** Um comando comprova exit code e bytes capturados; nao comprova qual modelo respondeu, se houve fallback, se a sessao era nova, nem se o isolamento existiu.
3. **"N agentes" conflita com manter a forma atual fora do escopo.** O modelo de debate tem secoes nomeadas para Codex, Claude e Gemini, e o achado tem uma `Revalidacao` unica. Nenhum dos dois representa N arbitrario, falha individual, comandos, hashes ou varias revalidacoes. Ou a forma muda, ou o requisito encolhe para o que ja e representavel.
4. O criterio de aceite "o artefato nao contem o texto das outras posicoes" **nao prova cegueira**: o agente pode ter lido e parafraseado. A evidencia teria de ser o manifesto do ambiente e a barreira de acesso.
5. `Rodada: N de N` ficou fragil depois que o teto saiu: em entrada aberta o total futuro e desconhecido, e o validador so reconhece dois numeros sem conferir coerencia. A automacao nao deve inventar o denominador.
6. Faltam da spec: politica de quando restam posicoes suficientes para a rodada existir; definicao de sessao realmente nova (cache de contexto pode vazar posicao mesmo com arquivos isolados); tratamento de saida hostil ou acidentalmente estrutural, porque colar resposta literal em `CONSENSUS.md` pode injetar headings e campos; localizacao, retencao e append atomico dos artefatos; e **risco de confidencialidade**, porque o mesmo snapshot vai para varios fornecedores externos e a lista de insumos e destinos precisa ser mostrada antes de executar.
7. Correcao de enquadramento: P-1(c) **nao e fraude por natureza**. Sintese feita por agente separado, identificada como proposta e sujeita a decisao humana, pode ser legitima. Deixar fora desta versao e escolha de escopo, nao impossibilidade logica.

O que declarou nao ter conseguido avaliar: nao executou as CLIs nem prototipou barreira de filesystem, entao nao confirmou quais ferramentas garantem o isolamento que recomenda; nao mediu qualidade, consumo nem taxa de falha com N agentes; e nao avaliou convergencia com o outro modelo, porque a resposta ficou oculta por construcao.

### Posicao Do Grok

`cursor-grok-4.6-xhigh`, via `cursor-agent -p --mode ask --force`, em modo read-only **por construcao** e nao por pedido no prompt.

Cinco tentativas pela CLI propria do Grok falharam antes disso, todas com `You've reached your free Grok Build usage limit`, mesmo apos o usuario assinar e refazer o login. A rodada so aconteceu porque a assinatura do Cursor expoe o mesmo modelo por outro caminho.

- **P-1:** (b), com uma precisao que as opcoes nao dao: quem monta a entrada e **o script orquestrador, nunca um dos agentes**. `Status`, `Proximo passo`, `Metodo`, `Exposicao previa` e `Rodada` saem da execucao; acordo e consenso final ficam em branco; os artefatos brutos ficam gravados ao lado como fonte. Aceita perder: entrada com consenso vazio pode ser lida como acordo por omissao, e montador fragil cola posicao no lugar errado sem o validador pegar, porque ele nunca checa merito.
- **P-2:** **o script desta operacao escreve o que P-1 marcar como mecanico; os agentes continuam proibidos.** "Nao e abrir a DEC-019 nem manter por simetria": a DEC-019 nomeia o **agente**, entao aplica-la ao script nao e heranca, e extensao a um sujeito que ela nao nomeia. Aplicar ao script recria o Problema 3; deixar os N agentes escreverem recria a fraude, agora com corrida no mesmo Markdown. Aceita perder: bug no montador carimba `Metodo` ou `Rodada` errados com cara de fato, e sem sidecar de proveniencia o criterio de coerencia com a execucao vira forma, nao verdade.
- **P-3:** nenhuma das tres. Isolar as **posicoes contemporaneas**, mantendo leitura do repositorio. E `CONSENSUS.md` nao e um degrau unico: em debate rodada 1 o arquivo fica fora do workspace; em revalidacao de achado a entrada sob revisao entra **de proposito**, porque e o objeto da pergunta. Aceita perder: `AGENTS.md`, `DECISIONS.md` e `SESSION.md` ainda correlacionam os modelos, entao o ponto cego nao some com isolamento de posicao.
- **P-4:** **os dois**, como dois pacotes sobre um primitivo unico (invocar agentes isolados e coletar artefatos). "O caro e isolamento e invocacao, nao o template." Se o corte for inevitavel: primitivo mais pareceres primeiro, e o pacote de achado na sequencia imediata, nao numa spec futura. Aceita perder: esforco G cresce e a v1 pode sair pela metade.
- **P-5:** N e os comandos entram **na chamada**, no contrato que o loop ja ensinou; lista em `MEMORY.md` e o padrao deste usuario, resolvido pelo agente de chat, nunca catalogo dentro da skill. **`N=1` e valido**, porque debate quer `N>=2` e achado quer `N=1`, e recusar 1 quebraria o caso que doeu. Aceita perder: `MEMORY.md` desatualizado dispara o revisor errado, e o usuario pode passar quatro agentes e queimar plano.
- **P-6:** **divergiu dos outros dois.** A automacao cobre a rodada 1 cega quando o metodo e `pareceres-independentes`, e ali a cegueira e obrigatoria por construcao; rodada 2 de debate fica **manual nesta versao**, porque exige o pacote inteiro das posicoes anteriores e nunca um resumo, senao o Problema 3 volta pelo orquestrador. E revalidacao de achado nao e "rodada 2 de debate": e pacote proprio, com exposicao controlada da entrada-alvo. Aceita perder: o custo medido no Problema 2 foi o da revalidacao do `0005-A1`, que e rodada com exposicao, entao automatizar so a cegueira de debate nao teria evitado aquela transcricao.

Criticas a spec, as que mudam trabalho:

1. **P-3(c) atribui a 2026-09-03 um isolamento que nao aconteceu.** Aquela rodada teve sandbox `read-only` **com o repositorio visivel**, e foi lendo o codigo que o Codex pegou o erro factual. "Sem acesso ao repositorio" teria cegado a unica rodada que a spec usa como prova. Premissa falsa, e ela e a ancora empirica da spec.
2. **P-3, P-4 e P-6 nao sao independentes**, e a escada (a) para (c) esconde isso: o isolamento que o achado precisa e o **oposto** do isolamento da rodada 1 cega, porque revalidar uma disposicao exige ve-la.
3. **P-5 usa como exemplo os revisores deste usuario.** Isso e o catalogo que a DEC-016 proibiu, so que dentro do enunciado da pergunta.
4. **"Alterar qualquer projeto que nao seja este repositorio" esta confuso no Fora Do Escopo.** Parece copiado da 0005/DEC-001, que fala do projeto-evidencia. Mas se o produto e um script da skill, ele **vai** rodar em projeto de usuario por desenho. Dogfood aqui ou feature distribuida? O escopo fica ilegivel.
5. **Proveniencia deveria estar dentro do escopo**, e nao fora: sem comando, exit e caminho do artefato, os campos escritos pela automacao voltam a ser autodeclaracao, so que do script em vez do modelo.
6. **Risco nao listado, e o mais grave:** se quem dispara a operacao for o modelo criticado, o Problema 3 sobrevive mesmo com N isolados. O script tem de escrever o artefato e a entrada; o chat nao transcreve.
7. Risco nao listado: agentes em paralelo no mesmo checkout vazam por arquivo, mesmo com prompt cego. Isolamento por construcao exige workspace separado, nao so prompt separado.
8. Risco nao listado: o mesmo `AGENTS.md` e a mesma spec, escritos pelo Claude, enquadram todos os pareceres. Isolar posicoes nao isola o enquadramento.

O que declarou nao ter conseguido avaliar: as flags de sandbox somente-leitura equivalentes ao `read-only` do Codex nas outras ferramentas; se extrair um invocador compartilhado do `loop.sh` e barato; o custo empirico de N agentes em paralelo; e a posicao dos outros modelos, por construcao.

### Pontos De Acordo

Com tres posicoes o placar mudou em relacao ao que duas sugeriam. **Tres unanimidades, duas maiorias de 2 a 1 contra o Claude, e uma maioria de 2 a 1 com dissidencia substantiva.**

- **P-1: 3 de 3.** Os tres recusaram a exclusao entre bruto e minuta, e puseram a linha de corte no mesmo lugar: a operacao para onde comeca o julgamento. Codex e Grok acrescentaram, separadamente, que quem monta e o orquestrador e nunca um dos agentes.
- **P-2: 3 de 3 no resultado, com o Claude perdendo o fundamento.** Codex e Grok chegaram sozinhos a mesma correcao: o que sustenta a excecao nao e haver N agentes, e sim o **escritor deterministico**. O Grok foi mais preciso que os dois: a DEC-019 nomeia o **agente**, entao aplica-la ao script nao seria heranca, seria estender a decisao a um sujeito que ela nunca nomeou.
- **P-3: 3 de 3, e os tres disseram que a pergunta esta mal posta.** Todos rejeitaram a escada pelo mesmo motivo: o que se isola sao as posicoes contemporaneas, nao o repositorio. O Grok foi alem e mostrou que a premissa empirica da pergunta e falsa, porque a rodada de 2026-09-03 teve o repositorio visivel, e foi lendo o codigo que o Codex achou o erro.
- **P-4: 2 a 1, o Claude perdeu.** Codex e Grok convergiram em cobrir debate e achado sobre um primitivo comum. O argumento do Claude, "existe um achado so e fui eu que escrevi, entao e n=1", levou dos dois o mesmo contra-argumento: o caro e isolamento e invocacao, nao o template, e cortar o achado faz a spec nao resolver o problema que a motivou.
- **P-5: 2 a 1, o Claude perdeu, e ha fato verificado do lado da maioria.** Codex e Grok disseram que N e os comandos entram na chamada, com `MEMORY.md` sendo padrao resolvido pelo agente de chat e nunca configuracao lida por script. Conferido: o `loop.sh` recebe `--agente` e obedece, sem ler `MEMORY.md` em momento nenhum. O Grok acrescentou o que os outros dois nao viram: **`N=1` precisa ser valido**, porque revalidacao de achado tem exatamente um revisor.
- **P-6: 2 a 1 pelos dois modos, com dissidencia que nao da para ignorar.** Claude e Codex querem os dois modos automatizados. O Grok quer so a rodada 1 cega na v1, e o motivo e forte: rodada 2 exige o pacote **inteiro** das posicoes anteriores, e no instante em que o orquestrador resume, o Problema 3 volta por dentro da propria automacao.

Um acordo que ninguem foi solicitado a dar, e que os tres deram: **isolamento por construcao nao produz independencia real.** Claude falou de vies de treino compartilhado, Codex de manifesto e barreira de acesso, Grok do enquadramento comum vindo do mesmo `AGENTS.md` e da mesma spec escrita por um dos participantes.

### Riscos E Tradeoffs

- **O risco que o Grok listou esta acontecendo neste registro.** "Se quem dispara a operacao for o modelo criticado, o Problema 3 sobrevive mesmo com N isolados." Quem isolou as tres posicoes, leu as tres e escreveu este resumo foi o Claude, que e uma das tres e o alvo das criticas das outras duas. O isolamento resolveu a **producao** das posicoes e nao resolveu a **transcricao**, que era o Problema 3 desde o inicio. Esta entrada e evidencia de que a spec ataca o problema certo, e de que a rodada manual nao o resolve.
- **A rodada tem n=3 e nao tem tres enquadramentos.** Os tres leram a mesma spec, escrita por um deles, com as perguntas redigidas por ele. Onde os tres concordam, concordam dentro de um enquadramento so.
- **As criticas mais duras vieram de fora do que foi perguntado.** Nenhuma pergunta cobria "a ancora empirica da spec e falsa" nem "P-3, P-4 e P-6 nao sao independentes". O valor da rodada esteve menos nas respostas e mais no que o enunciado nao previu.
- O campo `**Rodada:** 1 de 1` continua afirmando um denominador que ninguem sabe, e o Codex apontou essa fragilidade na mesma rodada em que ela aparece.
- O material bruto de cada agente segue fora do repositorio, contra o que os tres recomendam em P-1.

### Consenso Final

**Tres perguntas fechadas por unanimidade, tres decididas por maioria, e quatro defeitos confirmados na spec.**

Prontas para virar DEC, com 3 de 3: **P-1** (minuta deterministica mais bruto preservado, montada pelo orquestrador, julgamento em branco), **P-2** (o script escreve o recorte mecanico, os agentes seguem proibidos, e o fundamento e o escritor deterministico e nao a cardinalidade) e **P-3** (isolar posicoes contemporaneas, manter leitura do repositorio, e tratar `CONSENSUS.md` conforme o caso: fora em debate rodada 1, dentro em revalidacao de achado).

Decididas por maioria, para o usuario ratificar ou virar: **P-4** (cobrir os dois, 2 a 1), **P-5** (N e comandos na chamada, com `N=1` valido, 2 a 1 e com fato verificado) e **P-6** (dois modos, 2 a 1, com a dissidencia do Grok registrada porque o argumento dela sobrevive a derrota).

Defeitos que nao dependem de decisao e precisam ser corrigidos: a premissa falsa em P-3(c) sobre a rodada de 2026-09-03; a nao independencia entre P-3, P-4 e P-6; o exemplo de revisores dentro do enunciado de P-5, que e o catalogo que a DEC-016 proibiu; e o "Fora Do Escopo" que confunde o projeto-evidencia da 0005 com o projeto-alvo de um script distribuido.

Uma mudanca de escopo recomendada pelos tres, que so o usuario pode fazer: **proveniencia (comando, exit code, caminho do artefato) sai de fora e entra no escopo.** Sem ela, os campos escritos pela automacao voltam a ser autodeclaracao, so que do script em vez do modelo, e o Resultado esperado 1 nao se cumpre.

### Decisao Para Registrar Em DECISIONS.md

Cinco das seis ficam **so na spec 0006** (DEC-001 e DEC-003 a DEC-006), porque sao desenho local dela.

Uma sobe para `docs/DECISIONS.md`, porque muda o alcance de uma decisao ja registrada do projeto: a **DEC-002**, que estende a 0004/DEC-019. Aquela decisao proibia o **agente** do loop de escrever em `CONSENSUS.md`; agora fica dito que a proibicao vale para agente e nao para um orquestrador mecanico, e que o que a sustenta e a separacao entre quem opina e quem escreve, nunca a quantidade de agentes. Registrada em 2026-09-03 com o titulo "Agente nao escreve consenso; orquestrador deterministico escreve o recorte que a execucao comprova".

## 2026-09-03 - Par de fixture nao separa nada quando o check novo e AVISO

**Achado:** 0005-A1

**Status:** resolvido

**Resolvido em:** 2026-09-03, depois da rodada 2. A disposicao se sustenta com as correcoes registradas em "Revalidacao", e o residuo saiu daqui para o backlog: T-050, T-051 e T-052. A pergunta que a rodada 2 deixou aberta (identificador estavel de diagnostico ou fragmento de mensagem) foi respondida pelo usuario no mesmo dia: identificador estavel, e T-051 foi desbloqueada com essa escolha.

**Metodo:** debate-aberto

**Exposicao previa a outras posicoes:** sim

**Rodada:** 2 de 2

**Escapou de verificacao:** sim

### Contexto

- Primeiro uso do formato de achado neste repositorio, no dogfood da 2.4.0 (T-049), sobre trabalho da propria T-048.
- Proveniencia dos campos declarativos: a rodada 1 foi escrita so pelo Claude, sem outra posicao a vista (`pareceres-independentes`, exposicao previa `nao`). Os campos acima descrevem a rodada 2, em que o Codex leu a disposicao antes de escrever. As secoes "Disposicao" e "Por Que Nada Pegou Antes" continuam como saidas da rodada 1: o que a rodada 2 corrigiu esta em "Revalidacao", e nao reescrito por cima.
- O repositorio tem um unico padrao de fixture, herdado da 2.2.0: um par `valido`/`invalido` declarado no dicionario `FIXTURES` de `verify_repository.py`, com o exit code esperado de cada lado. Ele funciona porque todo check daquela versao era ERRO, e ERRO muda o exit code.

### O Que Foi Encontrado

- Os checks de achado da 2.4.0 sao AVISO, por decisao da spec: a forma e verificavel, o merito nao. Sem `--strict`, aviso nao muda exit code.
- Consequencia: a fixture `achado-project`, escrita no padrao existente, teria `invalido: 0` e `valido: 0` no `FIXTURES`, e `verify_repository.py` imprimiria `[OK] fixture achado-project/invalido: exit 0 (esperado 0)`. Verde, e sem provar nada: os cinco avisos poderiam nunca ter disparado, ou disparar na entrada errada, e o check passaria igual.

### Disposicao

- A fixture continua no `FIXTURES` (que cobre a regressao de "nao virou ERRO por acidente"), e ganhou `verificar_achado` ao lado: roda os dois lados com `--strict`, exige exit 0 no valido e exit 1 no invalido, **conta** os avisos e confere que nenhum deles cita a entrada de debate que abre os dois arquivos.
- A contagem e a checagem do controle sao o que faltava: sem elas, o par mede presenca de aviso, nao qual aviso.

### Revalidacao

Rodada 2, em 2026-09-03, pelo Codex CLI (`gpt-5.6-sol`, `model_reasoning_effort=high`, sandbox `read-only`), a pedido do usuario. Veredito: **se sustenta com ressalva**.

Aceito, e sao correcoes de fato, todas conferidas no codigo antes de registrar:

- **A disposicao descreve mal o proprio codigo.** `verificar_achado` conta linhas `[AVISO]` e confere uma unica exclusao, o titulo da entrada de controle. Ela nao compara motivo nem titulo dos avisos. A frase "sem elas, o par mede presenca de aviso, nao qual aviso" prometeu mais do que o codigo entrega: o portao continua sem saber **qual** aviso saiu. A entrada correspondente de `DECISIONS.md` herdou o mesmo exagero e foi corrigida.
- **A contagem fixa em cinco e rigida e fraca ao mesmo tempo.** Quebra quando a fixture cresce por motivo legitimo, e aceita regressao compensada: um aviso certo some, outro errado aparece, o total continua cinco e o portao passa. Contraexemplo do Codex: os cinco avisos caindo todos na mesma entrada.
- **T-050, como estava escrita, contradizia a propria disposicao.** Ela mandava recusar par cujos dois lados declarem o mesmo exit code, e `achado-project` tem os dois lados em 0 **de proposito**, que e exatamente a guarda de regressao que esta disposicao decidiu manter. Reescrita.
- **A causa estrutural e mais funda que "exit codes iguais".** O `FIXTURES` modela status de processo e nao associa cada fixture aos diagnosticos que ela deve produzir. Exit codes diferentes tambem escondem teste inutil: um lado invalido que sai 1 por arquivo obrigatorio ausente passaria por T-050 sem nunca exercitar o check pretendido.
- **O criterio "projeto que nunca registra achado nao recebe aviso novo" nao e exercitado literalmente.** Os dois lados de `achado-project` tem achado. Um bug que so emitisse aviso em arquivo sem nenhum achado passaria. Conferido: nenhuma outra fixture com entrada de debate roda em `--strict` (a do `v1-project` tem uma, e roda sem a flag).

Onde a revalidacao ficou incompleta, e isso tambem e registro:

- O Codex nao considerou que a **raiz deste repositorio ja e um controle vivo** do ultimo item: ela roda em `--strict` no primeiro check de `verify_repository.py`, tem uma entrada de debate sem `**Achado:**` (a de 2026-09-02) e fecha com zero avisos. Um `check_consensus_achado` que disparasse em entrada de debate reprovaria ali. E controle parcial, porque depende do dogfood e nao de fixture, e nao cobre arquivo sem nenhum achado; a critica sobrevive, mas nao inteira.
- Sobre `**Escapou de verificacao:** sim`, o Codex considera discutivel, porque nenhum portao verde chegou a existir. **Mantido `sim`**: o criterio da DEC-007 e se a verificacao existente pegaria o defeito, e ela nao pegaria. A secao "Por Que Nada Pegou Antes" ja declara essa nuance em vez de esconde-la.
- Os contraexemplos do Codex foram derivados por leitura, sem mutacao de fixture nem do validador, porque esta rodada proibiu editar arquivos. Nenhum deles foi executado.

Residuo desta rodada: T-050 (reescrita), T-051 (desbloqueada em 2026-09-03, com o usuario escolhendo identificador estavel de diagnostico em vez de fragmento de mensagem) e T-052.

### Por Que Nada Pegou Antes

- O que passou verde: nada, e a nuance importa. O defeito nunca chegou a ser commitado, porque apareceu ao escrever a fixture. O que escapa aqui e outra coisa: **nenhuma verificacao existente teria notado**, e o mecanismo de fixture nao tem como reclamar de um par que nao separa. Se a fixture tivesse sido escrita no padrao herdado, a suite reportaria 36 de 36 com um check inutil dentro.
- Mecanismo do ponto cego: o padrao de fixture foi desenhado quando todo check novo era ERRO, e o exit code separava os casos por construcao. A hipotese "o exit code separa" ficou implicita no padrao em vez de escrita, e um check AVISO a quebra sem que nada acuse.
- Conserto de portao proposto: `verificar_achado` ja cobre este par. O conserto geral, que continua em aberto, seria `verify_repository.py` recusar um par `valido`/`invalido` cujos dois lados declarem o mesmo exit code esperado, em vez de depender de quem escreve a proxima fixture lembrar disso.

### Decisao Para Registrar Em DECISIONS.md

- Fixture cujo caso invalido produz apenas AVISO nao prova nada pelo exit code sem `--strict`: ela roda com a flag e confere quais avisos sairam, nunca so quantos exit codes bateram.

## 2026-09-02 - Revisao da spec 0003 (skill 2.2.0) por modelo distinto

**Status:** resolvido

**Resolvido em:** 2026-09-02 (usuário ratificou as 6 mudanças do Codex e decidiu os 2 resíduos; spec 0003 passou para `Definida`).

**Metodo:** debate-aberto

**Exposicao previa a outras posicoes:** sim

**Rodada:** 2 de 3

### Contexto

A spec `docs/specs/0003-tasks-verificaveis.md` foi escrita como PRD da skill 2.2.0 e submetida a validação por modelo distinto no Codex CLI, em duas rodadas: rodada 1 cega (proibida a leitura da spec, só os quatro problemas), rodada 2 adversarial com a spec à vista. Primeiro uso real da regra de rodada cega que a própria spec propõe.

Proveniência: apenas a resposta da rodada 2 foi registrada aqui. A posição da rodada 1 do Codex está reconstruída a partir das referências que a rodada 2 faz a ela.

### Pergunta Ou Decisao

A spec 0003 deve passar para `Definida` como está?

### Posicao Do Codex

Veredito: passar para `Definida` **com mudanças**. Concorda com a direção geral (seção própria para tarefa parada, rodada cega no consenso, loop fora desta versão e fora do scaffold, comando único de integridade) e valida DEC-001, DEC-002, DEC-003 e DEC-005. Seis mudanças exigidas:

1. **Evidência de fechamento obrigatória para toda tarefa em `Concluidas`**, mantendo `(verifica: <comando>)` opcional. Argumento: se a verificação for inteiramente opcional, o agente conclui justamente as tarefas menos verificadas sem consequência, preservando a lacuna que a spec quer fechar. Formato proposto atende conteúdo e produto sem exigir comando falso: `Evidencia: tipo=revisao-manual; procedimento=conferencia dos links; resultado=12 links validos`.
2. **Evidência ausente em tarefa que declarou `(verifica:)` deve ser ERRO, não aviso.** Tarefa que declarou comando e foi movida para `Concluidas` sem resultado contradiz o próprio contrato; aviso não protege o estado concluído.
3. **Renomear `## Bloqueadas` para `## Aguardando Usuario`.** `Bloqueadas` sugere também dependência técnica, fornecedor ou incidente, e o formato obrigatório de pergunta e resposta não serve para esses casos. Mantém `**Resposta:**` e a data de bloqueio.
4. **Campos declarativos no registro de consenso**: `**Metodo:**`, `**Exposicao previa a outras posicoes:**`, `**Rodada:** N de 3`. O validador checaria presença, valor permitido e coerência do teto, e deve declarar explicitamente que não verifica a cegueira real.
5. **Mover o comando de integridade para dentro da skill**, por exemplo `docs/skills/ai-project-structure/evals/verify_repository.py`. Criar `scripts/` na raiz viola a regra de raiz mínima. Comparar a raiz inteira com `assets/` por `diff` seria incorreto, porque a raiz contém estado real do projeto dogfood.
6. **Corrigir caminhos e ampliar critérios de aceite.** A spec cita `scripts/validate_structure.py`, mas o validador está em `docs/skills/ai-project-structure/scripts/`.

Respostas às quatro perguntas abertas: (1) `(verifica:)` opcional inclusive em projetos com código, porque código também tem tarefa de pesquisa, documentação e decisão sem comando honesto; a obrigatoriedade correta é a evidência ao concluir. (2) Evidência ausente após `(verifica:)` é ERRO. (3) A seção de espera não rotaciona; gera AVISO após 30 dias, porque tarefa antiga bloqueada é informação operacional ativa, não histórico. (4) A seção entra em todos os scaffolds; o custo é uma seção vazia e o benefício é regra única disponível desde a primeira pergunta bloqueante.

Critérios de aceite que o Codex aponta como não verificáveis por comando: scaffold minimal e completa (exige rodar o fluxo de uma IA e responder à entrevista, sem runner automatizado de eval hoje); atualização 2.1.0 para 2.2.0 (`references/atualizacao.md` é instrução, não migrador executável); paridade dos três destinos após `install.sh` (verificável, mas hoje mutaria instalações locais, então deve rodar em destino temporário). Critérios faltantes que aponta: evidência obrigatória, ERRO de `(verifica:)` sem resultado, marcador com valor desconhecido, tarefa bloqueada válida retornando sucesso, os três campos de consenso, teto de três rodadas, paridade dos templates de `TASKS.md` e `CONSENSUS.md`, e atualização de projeto 2.1.0 com histórico sem transformar registros antigos em alegações falsas.

### Posicao Do Claude

Aceito as 6 mudanças. Duas delas são erro meu, e confirmei os dois no repositório:

- **Raiz mínima:** `scripts/check.sh` na raiz viola a regra registrada em "Regras Do Projeto" do `AGENTS.md` e o checklist de `QUALITY.md` ("A raiz mantem apenas os arquivos Markdown de entrada dos agentes"). A exceção registrada cobre apenas `README.md`, `LICENSE` e `.gitignore`. Codex está certo.
- **Caminho do validador:** a spec escreve `python3 scripts/validate_structure.py .`; o caminho real é `docs/skills/ai-project-structure/scripts/validate_structure.py`. Codex está certo.

Acrescento uma razão a mais para a colocação do item 5, que o Codex não citou: `evals/` **não é distribuído**. `diff -rq` entre a fonte canônica e `~/.claude/skills/ai-project-structure` mostra `evals`, `install.sh`, `README.md` e `CHANGELOG.md` como presentes apenas na fonte. Um verificador em `scripts/` da skill seria instalado na máquina de todo usuário; em `evals/` fica restrito ao repositório. A colocação proposta está certa por dois motivos, não um.

Onde o Codex leu errado: a spec **não** propõe comparar a raiz inteira com `assets/` por `diff`. Propõe diff do bloco `core` e das duas pontes. A crítica não se aplica, mas a sugestão embutida (definir paridade explícita também para os templates de `TASKS.md` e `CONSENSUS.md`) é válida e entra.

Sobre o item 4, o Codex conserta DEC-004 melhor do que eu escrevi. Meu texto aceitava "prosa não enforçável" e parava aí; os campos declarativos não provam independência, mas tornam o grau de confiança observável, que era o problema 3 original. Correção aceita.

Custo que o Codex não precificou no item 1: toda linha concluída passa a carregar sub-linha de evidência. Em projeto com centenas de tarefas, `TASKS.md` engorda rápido. Mitigado pela rotação opcional de "Concluidas" já prevista em `AGENTS.md`, mas a rotação deixa de ser opcional na prática.

Consequência que nenhum dos dois tirou: a 0003 aumenta o número de contratos verificados por script **e** o número de contratos verificados na mão ao mesmo tempo (scaffold, atualização, evals). Sem runner de eval, a razão entre automático e manual pode piorar em vez de melhorar.

### Posicao Do Gemini

(Nao consultado nesta rodada.)

### Pontos De Acordo

- Evidência de fechamento obrigatória para toda tarefa concluída, com `(verifica: <comando>)` permanecendo opcional.
- `(verifica:)` declarado e resultado ausente em `Concluidas` é ERRO.
- Seção de espera com pergunta, resposta e data; sem rotação, com aviso por idade.
- Consenso ganha campos declarativos de método, exposição prévia e rodada, com o validador checando presença e não veracidade.
- Verificador de integridade dentro da skill, em `evals/`, nunca em `scripts/` na raiz.
- Loop fora da 2.2.0 e fora do scaffold (DEC-003 mantida por ambos).
- Sem check de `QUALITY.md` vazio nesta versão (DEC-005 mantida por ambos).

### Riscos E Tradeoffs

- **Peso de convenção.** A versão revisada adiciona mais ao bloco core do que a original (evidência obrigatória, três campos de consenso). Cada linha é lida por todo modelo, em todo projeto, para sempre.
- **Teatro de conformidade.** Evidência obrigatória em projeto de conteúdo pode degenerar em `Evidencia: tipo=revisao-manual` colado sem conferência real. A regra fica verificável quanto à forma e não quanto ao conteúdo, que é a mesma limitação que ela pretende resolver.
- **Autodeclaração no consenso.** `Exposicao previa: nao` é escrito pelo mesmo modelo cuja cegueira o campo afirma. O Codex reconhece isso; vale registrar que o campo aumenta a rastreabilidade e não a garantia.
- **Verificação manual crescente.** Mais contratos, mesmo runner inexistente para evals.

### Consenso Final

Spec 0003 passa para `Definida` com as seis mudanças do Codex incorporadas. Os dois resíduos que nenhum dos dois modelos resolveu foram decididos pelo usuário em 2026-09-02:

**R-1. Nome e escopo da seção de espera.** `Aguardando Usuario` (Codex) cobre só bloqueio humano e é semanticamente mais preciso; `Bloqueadas` (spec original) cobre mais casos, mas o formato pergunta e resposta não serve para bloqueio técnico, fornecedor ou release upstream.

**Decisão do usuário:** adotar `## Aguardando Usuario` agora, com o formato `**Pergunta:**` / `**Resposta:**` / `(bloqueada: AAAA-MM-DD)`. Seção separada para bloqueio não humano só quando o primeiro caso real aparecer, com formato próprio. Motivo: não desenhar para caso que ainda não existe.

**R-2. Retroatividade da evidência obrigatória.** Tornar a regra retroativa converteria as 15 linhas históricas de `docs/TASKS.md` deste repositório, e as de todo projeto que atualizar, em alegações sem evidência.

**Decisão do usuário:** a regra vale apenas para tarefa concluída a partir da 2.2.0. O validador não cobra evidência de tarefa concluída antes da versão, e o fluxo de `references/atualizacao.md` não reescreve histórico.

### Decisao Para Registrar Em DECISIONS.md

Registrar em `docs/DECISIONS.md` como `2026-09-02 - Evidencia obrigatoria em tarefa, secao Aguardando Usuario e consenso declarado`, cobrindo: evidência de fechamento obrigatória para toda tarefa concluída a partir da 2.2.0, com `(verifica:)` permanecendo opcional; `(verifica:)` sem resultado em `Concluidas` como ERRO; seção `## Aguardando Usuario` sem rotação e com aviso por idade; campos declarativos de método, exposição prévia e rodada no consenso, checados quanto à presença e não quanto à veracidade; verificador de integridade em `evals/`, nunca em `scripts/` na raiz.

## 2026-04-25 - Validação da estrutura multiagente

**Status:** resolvido

**Resolvido em:** 2026-04-25 (estrutura aprovada; melhorias aplicadas no consenso seguinte do mesmo dia).

### Contexto

Validação da estrutura Markdown multiagente criada para projetos tocados por IA, com AGENTS.md como fonte central, arquivos-ponte para Claude e Gemini, memória de sessões em docs/SESSION.md e debate entre modelos em docs/CONSENSUS.md.

### Pergunta Ou Decisao

A estrutura atual é clara, segura e prática para projetos tocados por IA? O que pode melhorar?

### Posicao Do Claude

A estrutura é boa, prática e bem dimensionada para o objetivo. Os pontos mais fortes são: raiz mínima, hierarquia explícita de conflitos em `AGENTS.md` (usuário > AGENTS.md > docs/ > inferência), separação entre debate (`CONSENSUS.md`) e decisão final (`DECISIONS.md`), e checklist de qualidade aplicável. O fluxo é compreensível em uma única leitura, o que é raro.

Pontos de atenção concretos:

1. **`SESSION.md` cresce de forma ilimitada.** Sem política de rotação, em poucos meses fica caro de carregar e ruidoso. Sugiro adicionar em `AGENTS.md` uma regra simples: quando `SESSION.md` passar de N entradas (ex: 20) ou X KB, mover as mais antigas para `docs/archive/SESSIONS-AAAA.md`. As últimas 5 entradas bastam para continuidade real.
2. **Sobreposição entre `TASKS.md` e a seção "Pendencias" de cada sessão.** Hoje não está claro qual é canônico para o trabalho em aberto. Proposta: `TASKS.md` é a fonte de verdade do backlog vivo; "Pendencias" em `SESSION.md` é só o snapshot daquela sessão e deve ser refletido em `TASKS.md` antes de fechar.
3. **`CONSENSUS.md` não tem ciclo de vida.** Debates resolvidos ficam misturados com abertos. Sugiro um campo `Status: aberto | resolvido | arquivado` no template e mover resolvidos antigos para `docs/archive/` quando o arquivo crescer.
4. **Ordem de leitura é única para qualquer mudança.** Para tarefas triviais (ajuste de typo, renomear variável), ler 6 arquivos é overhead. Sugiro um nível "mudanca trivial" em `AGENTS.md` que exige só `SESSION.md` + `TASKS.md`, mantendo a leitura completa para mudanças relevantes.
5. **Não há regra de desempate.** Se Claude e Gemini não convergirem em `CONSENSUS.md`, o que acontece? Proposta: deixar explícito que o usuário é o desempate final e que, na ausência dele, prevalece a posição com menor risco reversível.
6. **Concordo com o Gemini quanto a reforçar a imutabilidade dos arquivos-ponte.** Hoje `CLAUDE.md` e `GEMINI.md` já mencionam `SESSION.md` e `CONSENSUS.md`, o que tecnicamente é uma duplicação leve do `AGENTS.md`. Útil como rede de segurança, mas vale uma linha em `AGENTS.md` proibindo qualquer regra de produto/arquitetura nesses arquivos.
7. **Concordo também quanto a handover direcionado.** "Próximo passo recomendado" ganha muito quando indica o agente esperado e por quê (ex: "Para Gemini, porque envolve análise multimodal de imagens em docs/").

Nada disso é bloqueante - a estrutura já pode ser usada como está. São melhorias incrementais.

### Posicao Do Gemini

A estrutura é excelente e segue as melhores práticas de gerenciamento de contexto para LLMs. A centralização em `AGENTS.md` reduz drasticamente o risco de instruções conflitantes ("instruction drift"), enquanto os arquivos-ponte (`CLAUDE.md`, `GEMINI.md`) garantem que cada ferramenta saiba onde buscar sua base de regras sem redundância. O uso de `SESSION.md` para continuidade e `CONSENSUS.md` para alinhamento entre modelos formaliza um fluxo de trabalho colaborativo que é raro mas necessário em projetos complexos.

Sugestões de melhoria:
1. **Handover Detalhado**: No `SESSION.md`, incentivar que o "Próximo Passo Recomendado" seja específico para o agente esperado (ex: "Para Claude: Finalizar refatoração do módulo X").
2. **Imutabilidade dos Pontos-Ponte**: Reforçar em `AGENTS.md` que `CLAUDE.md` e `GEMINI.md` não devem conter lógica de negócio ou regras de projeto, apenas redirecionamentos, para evitar sombreamento de regras.

### Pontos De Acordo

- Centralização de regras em `AGENTS.md`.
- Uso de `SESSION.md` para continuidade entre turnos/agentes.
- `CONSENSUS.md` como repositório de decisões complexas e debate multi-modelo.
- Arquivos-ponte (`CLAUDE.md`, `GEMINI.md`) devem ficar mínimos e sem lógica de projeto.
- Hierarquia de conflitos explícita em `AGENTS.md` é um diferencial e deve ser mantida.
- Separação clara entre `CONSENSUS.md` (debate) e `DECISIONS.md` (decisão final) é correta.

### Riscos E Tradeoffs

- **Overhead de Documentação**: O excesso de arquivos pode intimidar novos usuários, mas é um tradeoff necessário para manter a sanidade do contexto em projetos de longo prazo.
- **Sincronização**: O risco de um agente esquecer de atualizar `SESSION.md` ao final de uma sessão intensa.
- **Crescimento ilimitado de `SESSION.md` e `CONSENSUS.md`** sem política de arquivamento - vira ruído e custo de tokens com o tempo.
- **Sobreposição entre `TASKS.md` e "Pendencias" das sessões** sem regra clara de qual é canônico.
- **Custo de leitura para mudanças triviais** - ler 6 arquivos para um ajuste pequeno desincentiva o cumprimento da regra.
- **Ausência de regra de desempate** quando dois modelos não convergem em `CONSENSUS.md`.
- **Risco de drift dos arquivos-ponte** caso alguém adicione regra de projeto em `CLAUDE.md` ou `GEMINI.md` no futuro.

### Consenso Final

A estrutura está aprovada para uso imediato. Claude e Gemini concordam que ela é clara, segura e prática, e que reduz risco de instruction drift em projetos tocados por múltiplas IAs. Convergência em sete melhorias incrementais não-bloqueantes:

1. Política de rotação para `SESSION.md` (e `CONSENSUS.md`) com pasta `docs/archive/`.
2. Regra explícita: `TASKS.md` é canônico para backlog vivo; "Pendencias" da sessão é snapshot.
3. Campo `Status` no template de `CONSENSUS.md` (aberto / resolvido / arquivado).
4. Nível de leitura "mudanca trivial" em `AGENTS.md` (só `SESSION.md` + `TASKS.md`).
5. Regra de desempate explícita em `AGENTS.md` (usuário decide; na ausência, opção de menor risco reversível).
6. Reforço em `AGENTS.md` de que `CLAUDE.md` e `GEMINI.md` são imutáveis quanto a regras de projeto.
7. "Próximo passo recomendado" em `SESSION.md` deve indicar o agente-alvo quando fizer diferença.

Recomenda-se aplicar essas melhorias incrementalmente, não em uma única refatoração.

### Decisao Para Registrar Em DECISIONS.md

Nenhuma decisão nova por enquanto. As sete melhorias acima são sugestões; só viram decisão em `DECISIONS.md` quando o usuário aprovar e instruir aplicação.

## 2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias

**Status:** resolvido

**Resolvido em:** 2026-04-25 (apos aprovacao do usuario; mudancas aplicadas - ver `docs/DECISIONS.md`).

### Contexto

No consenso anterior do mesmo dia, Claude e Gemini aprovaram a estrutura e listaram sete melhorias incrementais. O usuario apontou que sentiu falta de um `MEMORY.md` na lista e pediu detalhamento dos sete pontos. Esta entrada abre o debate sobre adicionar `docs/MEMORY.md` (oitava melhoria) e formaliza a explicacao concreta de cada ponto.

### Pergunta Ou Decisao

Faz sentido adicionar `docs/MEMORY.md` a estrutura? Como ele convive com `PROJECT_CONTEXT.md`, `SESSION.md` e `DECISIONS.md` sem duplicar funcao? E qual a forma final dos sete pontos do consenso anterior depois de detalhados?

### Posicao Do Claude

**Sobre `MEMORY.md` (proposta nova):**

Sim, faz sentido. Hoje a estrutura tem cobertura para:

- O que o projeto **e** (estatico): `PROJECT_CONTEXT.md`
- O que **aconteceu** (cronologico): `SESSION.md`
- O que foi **decidido** (formal): `DECISIONS.md`
- O que esta **em aberto** (backlog): `TASKS.md`

Falta cobertura para o que o projeto **aprendeu** - fatos consolidados que valem "a partir de agora, sempre" e que se acumulam sem caber bem em nenhum dos arquivos acima. Exemplos concretos:

- "O usuario prefere portugues claro e respostas curtas." (nao e decisao, nao e contexto inicial, e preferencia que vale sempre)
- "Mocks em testes de migracao falharam em producao no Q4 - sempre usar banco real." (licao aprendida, nao decisao formal)
- "Issues do produto X sao trackeadas no Linear projeto INGEST." (referencia externa)
- "Ao gerar copy, evitar superlativos - o usuario corta sempre." (feedback que vira regra)

Proposta concreta para `docs/MEMORY.md`:

```md
# MEMORY

Memoria persistente do projeto. Diferente de SESSION.md (cronologico) e DECISIONS.md (decisoes formais), aqui ficam fatos que valem "a partir de agora, sempre" e se acumulam ao longo do tempo.

## User
Quem e o usuario, suas preferencias, contexto e expertise.

## Feedback
Guidance de "faca/nao faca isso". Cada item: regra + por que + quando aplicar.

## Project
Fatos sobre o projeto descobertos na pratica que nao estao em PROJECT_CONTEXT.

## Reference
Pointers para sistemas externos (Linear, Slack, Grafana, etc).
```

Convivencia com vizinhos:
- `PROJECT_CONTEXT.md` = o que o projeto **e** (raramente muda)
- `MEMORY.md` = o que o projeto **aprendeu** (acumula com tempo)
- `SESSION.md` = o que **aconteceu** em data X
- `DECISIONS.md` = o que foi **decidido** formalmente

Risco real: agente nao saber em qual dos quatro escrever. Mitigacao: regra simples em `AGENTS.md` - "se e cronologico, vai pro SESSION; se e decisao formal, vai pro DECISIONS; se e fato persistente nao-decidido, vai pro MEMORY; se e estrutural permanente, vai pro PROJECT_CONTEXT".

**Detalhamento dos sete pontos do consenso anterior:**

1. **Rotacao de `SESSION.md` e `CONSENSUS.md`.** Problema: arquivos crescem indefinidamente. Em 6 meses, `SESSION.md` pode ter 50+ entradas e fica caro de carregar. Proposta: regra em `AGENTS.md` - quando passar de ~20 entradas (ou ~30KB), mover as mais antigas para `docs/archive/SESSIONS-AAAA.md` (mesmo para CONSENSUS). Manter as 5-10 mais recentes, que sao as que importam para continuidade.

2. **`TASKS.md` canonico vs "Pendencias" em SESSION.** Problema: ha duas fontes de "o que esta em aberto" e nao esta claro qual prevalece. Proposta: `TASKS.md` e fonte unica de verdade do backlog vivo. A secao "Pendencias" de cada sessao em `SESSION.md` e snapshot historico daquela sessao; antes de fechar a sessao, o agente reflete pendencias em `TASKS.md`. Regra explicita em `AGENTS.md` e em `QUALITY.md`.

3. **Campo `Status` no template de `CONSENSUS.md`.** Problema: debates resolvidos se misturam com abertos. Proposta: adicionar linha `**Status:** aberto | resolvido | arquivado` logo abaixo do titulo de cada entrada (ja apliquei nesta entrada como demonstracao). Quando resolvido, atualizar o status. Quando arquivado, mover para `docs/archive/`.

4. **Nivel "mudanca trivial" na ordem de leitura.** Problema: `AGENTS.md` exige 6 arquivos antes de qualquer mudanca relevante. Para um typo isso e overhead que desincentiva o cumprimento. Proposta: dois niveis em `AGENTS.md`. **Trivial** (typo, rename local, formatacao, ajuste de comentario) → ler so `SESSION.md` + `TASKS.md`. **Relevante** (qualquer outra coisa) → ordem completa atual. Em duvida, tratar como relevante.

5. **Regra de desempate.** Problema: se dois modelos nao convergem em `CONSENSUS.md`, o arquivo fica "aguardando" indefinidamente. Proposta: tres regras em `AGENTS.md`. (a) Usuario e desempate final. (b) Na ausencia de usuario, prevalece a opcao de menor risco reversivel. (c) Se nenhuma e facilmente reversivel, o trabalho para e pede confirmacao humana - nunca o agente decide sozinho um caminho irreversivel.

6. **Imutabilidade dos arquivos-ponte.** Problema: hoje nada impede que alguem (humano ou IA) adicione regra de produto em `CLAUDE.md` ou `GEMINI.md`, criando conflito ou duplicacao com `AGENTS.md`. Proposta: linha explicita em `AGENTS.md` - "`CLAUDE.md` e `GEMINI.md` nao podem conter regras de produto, arquitetura ou processo. Apenas redirecionamento para `AGENTS.md` e refs basicas de leitura inicial". Quem precisar mudar regra, muda em `AGENTS.md`.

7. **Handover direcionado.** Problema: "Proximo passo recomendado" em `SESSION.md` hoje e generico. Proposta: quando o proximo passo se beneficiar de um agente especifico, indicar agente + razao. Exemplos: "Para Gemini, porque envolve analise multimodal de imagens em `docs/figures/`" ou "Para Claude, porque o trecho exige raciocinio sobre TypeScript". Quando qualquer agente serve, escrever "Qualquer agente" explicitamente. Isso evita ambiguidade e melhora qualidade do handover.

### Posicao Do Gemini

**Sobre `MEMORY.md` (proposta nova):**

Concordo plenamente. A inclusão de `MEMORY.md` resolve o problema do "conhecimento tácito" que se perde entre sessões. Enquanto o `PROJECT_CONTEXT.md` define a "alma" e a estrutura do projeto, o `MEMORY.md` captura sua "experiência acumulada".

Como evitar sobreposição:
- **`PROJECT_CONTEXT.md` (O QUE É)**: Definições estruturais, objetivos de negócio, stack tecnológica. É o "mapa" inicial.
- **`MEMORY.md` (O QUE APRENDEMOS)**: Preferências de estilo do usuário, lições aprendidas em bugs críticos, quirks da stack, referências externas dinâmicas. É o "diário de bordo" consolidado.

Riscos identificados:
- **Entropia de Atualização**: O risco de o agente atualizar o `SESSION.md` mas esquecer de extrair a lição aprendida para o `MEMORY.md`. A mitigação deve ser um item específico no `QUALITY.md`.
- **Obsolescência**: Diferente do context, fatos no memory podem mudar (ex: o usuário muda de ideia sobre um estilo). Precisamos de uma regra de "Sobrescrita Ativa" onde fatos novos no `MEMORY.md` invalidam os antigos se houver conflito.

**Posição sobre os sete pontos detalhados pelo Claude:**

1. **Rotação de `SESSION.md` e `CONSENSUS.md`**: Concordo. Manter o contexto "enxuto" é vital para o desempenho de LLMs. A pasta `archive/` é a solução padrão da indústria.
2. **`TASKS.md` canônico**: Concordo. Centralizar o backlog vivo evita o desvio de objetivos entre sessões.
3. **Campo `Status` em `CONSENSUS.md`**: Concordo. Facilita a varredura rápida de decisões pendentes.
4. **Nível "mudança trivial"**: Concordo com ressalvas. Sugiro que "trivial" seja definido estritamente como: ajustes de documentação (typos), comentários de código ou mudanças locais sem impacto em API/Contrato. Em qualquer dúvida, ler tudo.
5. **Regra de desempate**: Concordo. O foco na "menor reversibilidade" é uma heurística excelente de engenharia de software para automação.
6. **Imutabilidade dos arquivos-ponte**: Concordo. `CLAUDE.md` e `GEMINI.md` devem ser vistos como "entrypoints" técnicos, não repositórios de lógica.
7. **Handover direcionado**: Concordo. Aproveitar as especialidades de cada modelo (ex: raciocínio lógico vs. criatividade/estilo) otimiza o uso dos recursos de IA.

### Posicao Do Codex

Concordo com Claude e Gemini: adicionar `docs/MEMORY.md` faz sentido e fecha uma lacuna real da estrutura. A divisao `PROJECT_CONTEXT.md` = "o que o projeto e" e `MEMORY.md` = "o que aprendemos" e boa, desde que `MEMORY.md` nao vire um segundo `SESSION.md` nem um deposito de qualquer observacao solta.

Meu ajuste principal: `MEMORY.md` deve guardar aprendizados persistentes, reutilizaveis e ja consolidados, nao eventos. Cada item deveria ter pelo menos contexto curto, data/origem e uma regra de revisao quando puder ficar obsoleto. Claude e Gemini tocaram no risco de sobreposicao e obsolescencia, mas eu reforcaria tres coisas que ficaram implicitas:

- Memoria precisa de criterio de promocao: algo sai de `SESSION.md` para `MEMORY.md` somente quando for util para sessoes futuras.
- Memoria precisa aceitar correcao: fatos antigos podem ser marcados como "substituido" em vez de apenas acumulados.
- Memoria nao deve guardar dados sensiveis sem necessidade; preferencias e aprendizados devem ser escritos no menor nivel de detalhe util.

**Posicao sobre os sete pontos detalhados pelo Claude:**

1. **Rotacao de `SESSION.md` e `CONSENSUS.md`: concordo com ajuste.** A rotacao e necessaria, mas eu evitaria uma regra puramente mecanica. Antes de arquivar, o agente deve preservar um resumo das entradas antigas ou manter um indice em `docs/archive/README.md`, para a memoria longa nao desaparecer em arquivos que ninguem consulta.
2. **`TASKS.md` canonico vs "Pendencias" em SESSION: concordo.** `TASKS.md` deve ser a fonte de verdade do backlog vivo. Eu acrescentaria que pendencias de sessao deveriam apontar para uma tarefa existente ou virar tarefa antes do fechamento, quando forem acionaveis.
3. **Campo `Status` no template de `CONSENSUS.md`: concordo.** Alem de `aberto | resolvido | arquivado`, faz sentido ter uma linha curta de "Proximo passo" quando o status estiver aberto; isso evita consenso parado sem dono claro.
4. **Nivel "mudanca trivial" na ordem de leitura: concordo com definicao restrita.** A excecao e boa para reduzir atrito, mas precisa ser conservadora. Mudanca trivial nao deve incluir alteracao de comportamento, contrato, arquitetura, regras de IA ou estrutura de arquivos. Em duvida, leitura completa.
5. **Regra de desempate: concordo com ajuste.** Usuario e sempre o desempate final. A heuristica de menor risco reversivel e boa apenas para avancar em decisoes pequenas; se a decisao for irreversivel, cara, sensivel ou estrutural, o agente deve parar e pedir confirmacao humana.
6. **Imutabilidade dos arquivos-ponte: concordo.** `CLAUDE.md` e `GEMINI.md` devem continuar tecnicos e minimos. Eu manteria apenas o redirecionamento para `AGENTS.md` e, no maximo, lembretes de leitura inicial; nenhuma regra de produto, arquitetura, estilo ou processo deve nascer ali.
7. **Handover direcionado: concordo com ajuste.** Indicar agente-alvo ajuda, mas nao deve virar dependencia artificial. O formato ideal e: "Agente sugerido", "motivo" e "qualquer agente pode seguir se tiver contexto suficiente".

**Algo importante que faltava no debate:**

- O maior risco nao e a falta de arquivo; e a baixa adocao operacional. Se atualizar `SESSION.md`, `TASKS.md`, `MEMORY.md`, `DECISIONS.md` e `CHANGELOG.md` parecer pesado, agentes vao pular etapas. A mitigacao e deixar regras de atualizacao por gatilho: atualizar so o arquivo cuja funcao foi realmente acionada.
- Tambem falta uma regra de "nao criar consenso por teatro". `CONSENSUS.md` deve ser usado para duvidas reais, nao para toda microdecisao. Caso contrario, o processo fica lento e perde valor.
- A skill `ai-project-structure` deve ser atualizada junto com a estrutura, senao novos projetos nascem com a versao antiga.

### Pontos De Acordo

- `MEMORY.md` é necessário para capturar aprendizados empíricos e preferências do usuário.
- Distinção clara entre: `PROJECT_CONTEXT` (O que é), `MEMORY` (O que aprendemos), `SESSION` (O que houve) e `DECISIONS` (O que foi decidido).
- Rotação de logs antigos para `docs/archive/` para manter a performance do contexto.
- `TASKS.md` como única fonte de verdade para o backlog atual.
- Status explícito em debates para facilitar a gestão.
- Diferenciação de profundidade de leitura baseada no risco da mudança (trivial vs. relevante).
- O usuário como árbitro final e reversibilidade como critério de desempate autônomo.
- Imutabilidade de `CLAUDE.md` e `GEMINI.md` quanto a regras de negócio.
- Handovers de sessão com indicação de agente-alvo quando benéfico.
- `MEMORY.md` deve guardar aprendizados persistentes, nao eventos cronologicos.
- Itens de `MEMORY.md` precisam poder ser revisados, substituidos ou promovidos para `PROJECT_CONTEXT.md` quando virarem contexto estrutural.
- A aplicacao das melhorias deve atualizar tambem a skill `ai-project-structure`, para novos projetos nascerem com a versao correta.

### Riscos E Tradeoffs

- **Custo Cognitivo**: O aumento do número de arquivos exige que o agente seja mais diligente. Se o agente "tiver preguiça" de ler ou atualizar, a estrutura colapsa.
- **Dilema da Reversibilidade**: Avaliar se uma mudança é "facilmente reversível" pode ser subjetivo e induzir o agente ao erro.
- **Fragmentação do Conhecimento**: Se uma informação importante for parar no `MEMORY.md` mas deveria estar no `PROJECT_CONTEXT.md` (ou vice-versa), o agente pode ter uma visão parcial.
- **Sobrecarga de Sincronização**: O agente precisa atualizar `SESSION.md`, possivelmente `TASKS.md` e `MEMORY.md` ao final de uma mesma tarefa.
- **Baixa Adoção Operacional**: Se a manutencao exigir atualizar muitos arquivos a cada sessao, agentes podem ignorar parte do processo.
- **Consenso Excessivo**: Usar `CONSENSUS.md` para decisoes pequenas pode deixar o fluxo lento e burocratico.
- **Memoria Obsoleta Ou Sensivel**: `MEMORY.md` pode acumular preferencias antigas, inferencias fracas ou informacoes sensiveis se nao houver regra de revisao e minimizacao.

### Consenso Final

Claude e Gemini alcançaram consenso total sobre a evolução da estrutura. As sete melhorias iniciais foram detalhadas e refinadas, e a adição do `MEMORY.md` foi aprovada como a oitava melhoria essencial para a continuidade do projeto. A estrutura agora é considerada madura para lidar com o ciclo de vida completo de aprendizado, decisão e execução de IAs. Próximo passo recomendado: aprovação do usuário para criar `docs/MEMORY.md` e atualizar `AGENTS.md` com as novas regras de leitura e desempate.

Codex tambem concorda com a direcao geral, formando tri-consenso. Os ajustes recomendados sao operacionais: `MEMORY.md` deve ter criterio de promocao, revisao/substituicao de fatos obsoletos, cuidado com dados sensiveis, uso moderado de `CONSENSUS.md` e atualizacao da skill `ai-project-structure` junto com a estrutura principal.

**Aprovado pelo usuario em 2026-04-25.** Mudancas aplicadas conforme registrado em `docs/DECISIONS.md` e `docs/CHANGELOG.md`.

### Decisao Para Registrar Em DECISIONS.md

Decisao registrada em `docs/DECISIONS.md` como `2026-04-25 - Evolucao da estrutura: MEMORY.md e oito melhorias`.

