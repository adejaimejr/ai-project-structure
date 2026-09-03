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

## 2026-09-03 - As seis perguntas da spec 0006 (automacao do consenso)

**Status:** aberto

**Proximo passo:** o usuario decide P-4 e P-5, onde as duas posicoes divergem, e decide se vale rodar o Grok antes disso. As outras quatro convergiram e estao prontas para virar DEC na spec 0006 assim que ele ratificar.

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

**Nao consultado nesta rodada.** Cinco tentativas da rodada real, todas recusadas com a mesma mensagem: `You've reached your free Grok Build usage limit for now. Get SuperGrok for much higher limits`. Entre elas o usuario refez o login e a CLI se atualizou sozinha, de `1.0.5 (5115b46bc909)` para `1.0.13 (5e9a58528b76)`, sem efeito.

O diagnostico foi refeito depois de uma leitura errada, e vale registrar as duas. Em ordem: `grok -p "oi"` passou; a rodada real falhou; `grok --always-approve -m grok-4.6 --effort xhigh -p "Responda apenas: ok"` passou; a rodada em `--effort high` falhou; e tres prompts de enchimento (1000, 2000 e 3000 bytes) falharam. **A primeira leitura foi que o gatilho era o tamanho do pedido, e ela nao se sustenta**: o prompt de 1000 bytes falhou depois de um de 20 bytes ter passado, entao o que separa passar de falhar e o **momento**, nao o volume. O padrao e o de uma franquia pequena que repoe com o tempo (a propria mensagem diz "try again later"), com os dois sucessos gastando o que havia disponivel.

Conclusao com o que da para afirmar: `grok models` responde `You are logged in with grok.com` com `grok-4.6` disponivel, entao nao e autenticacao, e a CLI trata esta conta como **free tier** apesar da assinatura feita hoje. Ou a assinatura nao cobre o produto de CLI, que a mensagem chama de Grok Build, ou ela nao esta sendo aplicada por ele. Pendente do usuario junto ao fornecedor; nao e coisa que agente resolva.

Consequencia para esta rodada: **duas posicoes, nao tres.** Onde as duas divergem, nao ha desempate por terceiro, e a regra de desempate manda o usuario decidir.

### Pontos De Acordo

Quatro das seis perguntas convergiram, e em duas delas os dois modelos rejeitaram as opcoes oferecidas pela pergunta, independentemente:

- **P-1: convergencia forte.** Os dois recusaram a exclusao entre bruto e minuta. O Claude escreveu que "a entrada precisa apontar para o artefato bruto de cada agente, e nao substitui-lo"; o Codex recusou a pergunta e pediu os dois lado a lado. Mesma linha de corte nos dois: a operacao para onde comeca o julgamento.
- **P-2: convergencia no resultado, com o Codex corrigindo o fundamento.** Os dois disseram sim com excecao estreita. O Claude justificou por "sao N agentes, e a razao da DEC-019 era um agente so"; o Codex mostrou que isso nao basta, porque o acoplamento volta se quem escreve for um dos opinantes ou um sintetizador livre. O que sustenta a excecao e o **escritor deterministico**, nao a cardinalidade. Correcao aceita.
- **P-3: convergencia forte, e os dois disseram que a pergunta esta mal posta.** Ambos rejeitaram a escada (a)/(b)/(c) pelo mesmo motivo: o que precisa ser isolado sao as posicoes da rodada atual, nao o repositorio, porque tirar o repositorio degrada a qualidade sem comprar isolamento. O Codex acrescentou o que faltava: sandbox somente-leitura impede escrita e nao leitura, entao o isolamento tem de vir de snapshot e barreira de acesso, com manifesto e hashes.
- **P-6: convergencia forte.** Os dois modos, rodada 1 cega por construcao, e o ponto que os dois fizeram com palavras diferentes: a execucao **determina** os campos declarativos em vez de o usuario digita-los, e a operacao nunca deduz sozinha rodada ou quais posicoes fornecer.

Fora das perguntas, um acordo que nenhum dos dois foi solicitado a dar: os dois apontaram, sem combinar, que a spec trata isolamento por construcao como se produzisse independencia real, e nao produz.

### Riscos E Tradeoffs

- **A rodada tem n=2, e um dos dois escreveu a spec.** E menos independencia do que o formato sugere. Onde os dois concordam, concordam com o enquadramento de um deles.
- **Convergencia nao e prova.** Os quatro acordos podem vir de vies compartilhado de treino, e o proprio Claude levantou isso na posicao dele. Ninguem mediu.
- **A entrada bateu no defeito que a posicao do Codex descreve.** O campo `**Rodada:** 1 de 1` acima afirma um denominador que nao se sabe: se o Grok rodar depois, ainda e rodada 1. E o exemplo vivo da critica 5 dele, acontecendo no registro que a discute.
- **O material bruto nao foi preservado**, contra o que a P-1 dos dois recomenda. Este registro e resumo conferido, nao artefato.
- Quatro decisoes prontas para virar DEC ficam paradas ate o usuario ratificar. O custo de esperar e baixo; o de ratificar por conta propria seria transformar parecer de modelo em decisao de projeto, que e o que a regra de desempate proibe.

### Consenso Final

**Parcial.** Quatro perguntas convergiram (P-1, P-2, P-3, P-6) e estao prontas para virar decisao da spec 0006, com a redacao da P-2 seguindo o fundamento do Codex e nao o do Claude. Duas divergiram e sobem para o usuario:

- **P-4, o que a primeira versao cobre.** Claude: so debate, porque existe um unico achado registrado e ele foi escrito pelo proprio Claude ontem, entao automatizar aquela forma e automatizar um palpite n=1. Codex: os dois, com coletor comum e dois renderizadores, porque a revalidacao de achado e o unico caso doloroso observado e deixa-la de fora entrega ferramenta que nao resolve o que motivou a spec. As duas posicoes usam **o mesmo fato** (existe um achado so, e ele doeu) para concluir o oposto.
- **P-5, onde mora a lista de agentes.** Claude: lista nomeada em `docs/MEMORY.md`, no mesmo lugar dos perfis que ja existem. Codex: lista explicita por chamada, porque o executor nao deve interpretar Markdown nem escolher modelo, e `MEMORY.md` e preferencia resolvida pelo agente de chat, nao configuracao. Ponto de fato a favor do Codex, conferido: o `loop.sh` de hoje recebe `--agente` e obedece, sem ler `MEMORY.md`. Os dois concordam em pelo menos duas configuracoes distintas e em nenhum N padrao oculto.

### Decisao Para Registrar Em DECISIONS.md

Nada ainda. As quatro convergencias viram `DEC-NNN` **na spec 0006**, nao em `DECISIONS.md`, porque sao decisoes locais de desenho dela. Duas delas podem subir para `DECISIONS.md` depois, se sobreviverem a implementacao: a excecao a DEC-019 por escritor deterministico, que muda uma decisao ja registrada do projeto, e a regra de que campo declarativo escrito por execucao vale mais que campo digitado, que vale para qualquer automacao futura e nao so para esta.

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
