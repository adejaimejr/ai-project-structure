# CONSENSUS

Use este arquivo quando modelos diferentes precisarem debater para chegar a um consenso.

Ele nao substitui `DECISIONS.md`. Quando o debate gerar uma decisao importante, copie a decisao final para `DECISIONS.md`.

## Quando Usar

Use este arquivo quando:

- houver discordancia entre agentes;
- a decisao tiver impacto em arquitetura, produto, dados, seguranca ou custo;
- a tarefa tiver risco alto;
- o usuario pedir opiniao de outro modelo;
- a resposta correta depender de tradeoffs.

Nao use para decisoes simples ou tarefas obvias.

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

### Contexto

- 

### Pergunta Ou Decisao

- 

### Posicao Do Codex

- 

### Posicao Do Claude

- 

### Posicao Do Gemini

- 

### Pontos De Acordo

- 

### Riscos E Tradeoffs

- 

### Consenso Final

- 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Achado

Nem todo uso deste arquivo e debate. Quando a validacao cruzada encontra um defeito, risco ou lacuna, isso e um **achado**, e vira entrada propria, com `**Status:**` e `**Proximo passo:**` proprios.

- `**Achado:**` traz o identificador do achado. Ele e livre, amarrado a unidade de trabalho do projeto (`N10`, `API-3`, o que o projeto ja usar): o validador confere que o campo existe e tem valor, e nunca opina sobre o valor.
- `**Escapou de verificacao:**` `sim` ou `nao`, dizendo se a verificacao que ja existia deixou o achado passar. Declarou `sim`? A entrada traz a secao `### Por Que Nada Pegou Antes`.
- A disposicao do achado e de quem o registra; a revalidacao dela e de outro modelo, e conta como rodada.
- Achado so vira tarefa em `TASKS.md` depois de a disposicao concluir que ha trabalho, e a tarefa cita o achado na linha.

Nao ha teto de rodadas. Da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`, dizendo o que a rodada anterior deixou em aberto.

## Ponto Cego Da Validacao Cruzada

Rodada verde e ausencia de objecao, nao prova de que funciona. Modelos que leem o mesmo texto herdam o mesmo ponto cego, e defeito que so existe em contexto de execucao real sobrevive a N rodadas de leitura.

## Modelo De Achado

```md
## AAAA-MM-DD - Titulo curto do achado

**Achado:** <identificador livre, ex: N10>

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim | nao

**Pendente da rodada anterior:** (obrigatorio da rodada 4 em diante)

### Contexto

- 

### O Que Foi Encontrado

- 

### Disposicao

- (o que quem registrou o achado decidiu fazer, e por que)

### Revalidacao

- (modelo distinto avaliando a disposicao acima, nao o achado em si)

### Por Que Nada Pegou Antes

(obrigatoria quando `**Escapou de verificacao:**` for `sim`; corte a secao quando for `nao`)

- O que passou verde: 
- Mecanismo do ponto cego: 
- Conserto de portao proposto: 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Registros

Os debates de 2026-04-25 foram rotacionados para `docs/archive/CONSENSUS-2026.md`.

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
