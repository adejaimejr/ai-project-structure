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
