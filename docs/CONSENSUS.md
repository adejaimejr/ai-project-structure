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

**Proximo passo:** o usuario ratifica P-1, P-2 e P-3 (unanimes), decide P-4, P-5 e P-6 (maioria de 2 a 1, com o Claude vencido em duas), decide se a proveniencia entra no escopo, e manda corrigir os quatro defeitos da spec que a rodada confirmou.

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

Nada ainda. As quatro convergencias viram `DEC-NNN` **na spec 0006**, nao em `DECISIONS.md`, porque sao decisoes locais de desenho dela. Duas delas podem subir para `DECISIONS.md` depois, se sobreviverem a implementacao: a excecao a DEC-019 por escritor deterministico, que muda uma decisao ja registrada do projeto, e a regra de que campo declarativo escrito por execucao vale mais que campo digitado, que vale para qualquer automacao futura e nao so para esta.
