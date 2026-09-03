# Spec 0006 - Automacao do consenso: independencia por construcao

**Status:** Rascunho
**Criada em:** 2026-09-03
**Esforco:** G, porque toca tres coisas ao mesmo tempo: execucao de agente, escrita em arquivo de memoria, e os campos que a 2.2.0 criou justamente para denunciar consenso fraco. Depende de respostas do usuario antes de virar `Definida`.

## Problema E Resultado Esperado

Esta spec estava pre-registrada em dois lugares, os dois dizendo a mesma coisa: a spec 0005 a listou em "Fora Do Escopo" com a nota "depende desta spec estar fechada, e merece a propria", e a DEC-008 da spec 0004 a tirou da 2.3.0 dizendo que ela "mexe em `CONSENSUS.md` e nos campos declarativos da 2.2.0, nao no ciclo de execucao". A 0005 fechou em 2026-09-03, entao a dependencia caiu.

- Problema 1: **a independencia do consenso e autodeclarada, e a propria skill diz isso em voz alta.** A 2.2.0 criou `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`, e registrou junto que o validador "checa presenca e valor permitido, **nunca veracidade**: nenhum script prova que um modelo nao leu a posicao do outro. O ganho e rastreabilidade, nao garantia." Automatizar muda a natureza da coisa: se a ferramenta roda N agentes isolados entre si, a independencia deixa de ser afirmacao e vira propriedade do processo.

- Problema 2: **a rodada na mao custa caro o bastante para nao acontecer.** Medido neste repositorio em 2026-09-03, na revalidacao do achado `0005-A1`: foi preciso escrever um arquivo de prompt, escolher o perfil, montar a chamada com sandbox `read-only`, esperar, ler a saida e transcrever a posicao. Deu certo e pegou um erro factual real, mas nada disso ficou como procedimento reproduzivel, e o custo de repetir e o mesmo da primeira vez. Segunda opiniao cara e segunda opiniao que so acontece quando alguem lembra.

- Problema 3: **quem transcreve a critica e o modelo criticado.** Naquela mesma rodada, quem escreveu a secao `Revalidacao` foi o Claude, resumindo a critica do Codex ao trabalho do Claude. A entrada declara a proveniencia e o resumo foi conferido no codigo antes de aceito, mas o acoplamento e exatamente do tipo que o consenso existe para evitar: a fidelidade da critica depende da boa fe de quem ela critica.

- Problema 4: **ja existe um caminho de invocar agente no projeto, e o consenso nao usa.** O `loop.sh` resolveu o conceito de comando de agente neutro (`--agente`), com os perfis por intencao vivendo em `docs/MEMORY.md` e resolvidos pelo agente de chat, nunca pelo script. Consenso automatizado que invente o proprio jeito de chamar agente cria duas implementacoes da mesma coisa no mesmo repositorio, e elas divergem com o tempo.
  - **Correcao de 2026-09-03, apontada pelo Codex na rodada 1 e conferida no codigo antes de aceita:** a primeira redacao deste problema superestimava o reuso. O que se reaproveita e o conceito, nao o script. O `loop.sh` de hoje pressupoe tarefa, mutacao de arquivo, portao e tentativas, e em `loop.sh:145` ele decide se o agente fez alguma coisa com `find -type f -newer` no projeto. Um agente de parecer nao escreve nada, entao cairia no `exit 4` da DEC-014 em toda rodada. Reusar o script como esta nao funciona.

- Resultado esperado 1: posicoes independentes **por construcao**, e nao por declaracao, com os campos da 2.2.0 passando a descrever um fato do processo em vez de uma promessa do modelo.
- Resultado esperado 2: segunda opiniao barata o suficiente para ser o padrao em decisao de risco, e nao um esforco especial.
- Resultado esperado 3: proveniencia registrada por quem executou, nao por quem foi revisado.
- Resultado esperado 4: um caminho de invocacao de agente no projeto, reaproveitando o que o modulo de loop ja provou em bancada.

## Escopo

### Incluido

- Executar a mesma pergunta em N agentes, isolados entre si, com o isolamento sendo propriedade da execucao e nao pedido no prompt.
- Reuso do que o modulo de loop ja tem: `--agente` neutro, perfis em `docs/MEMORY.md`, exit codes por caminho.
- Material de saida por agente, em forma que vire entrada de `CONSENSUS.md` sem o resumo passar por quem foi criticado.
- Checks correspondentes em `validate_structure.py`, na medida em que sejam verificaveis por forma.

### Fora Do Escopo

- **Sintetizar o consenso final, declarar convergencia ou decidir por maioria.** Coletar posicoes e uma operacao mecanica; dizer que elas concordam e julgamento. A regra de desempate do bloco core ja diz que, sem convergencia, quem decide e o usuario.
- Mudar os campos declarativos da 2.2.0 ou a forma do achado. Se a automacao mostrar que a forma precisa mudar, isso vira spec propria, e hoje existe exatamente um achado registrado.
- Teto de custo global do projeto. Fica o teto local desta operacao, se P-5 pedir.
- Alterar o **projeto usado como evidencia da spec 0005**, que segue somente-leitura por 0005/DEC-001. Isto nao restringe o produto: o entregavel e um script distribuido pela skill, e ele **vai** rodar em projeto de usuario por desenho, igual ao `loop.sh`. A redacao anterior desta linha era "alterar qualquer projeto que nao seja este repositorio", que o Grok apontou na rodada 1 como confusao entre projeto-evidencia e projeto-alvo, deixando o escopo ilegivel. Corrigido em 2026-09-03; nao e mudanca de escopo, e a mesma restricao dita sem ambiguidade.

## Criterios De Aceite

Escritos ate onde as perguntas abertas permitem. Os que dependem de resposta estao marcados.

Verificaveis por comando:

- Rodar a operacao com N agentes produz N artefatos de posicao, um por agente, e nenhum deles contem o texto das posicoes dos outros.
- Agente que falha (cota, configuracao, indisponibilidade) nao derruba a rodada inteira nem produz posicao vazia passando por posicao real: o artefato daquele agente registra a falha.
- A operacao nao inventa posicao de agente que nao rodou. Nenhum artefato sem execucao por tras.
- Projeto que nunca usa a automacao nao ganha nenhuma cobranca nova no validador.
- `verify_repository.py` em exit 0, e nenhum travessao (U+2014) em arquivo novo ou alterado.
- (Depende de P-1 e P-2.) Se a operacao escrever em `CONSENSUS.md`, a entrada gerada passa em `validate_structure.py --strict` sem aviso, e declara `Metodo`, `Exposicao previa a outras posicoes` e `Rodada` coerentes com o que a execucao de fato fez.
- (Depende de P-3.) O isolamento declarado e o isolamento verificavel sao o mesmo: existe uma forma de conferir, sem confiar no relato do agente, que ele nao teve acesso as outras posicoes.

Julgados na mao, sem runner hoje:

- Se a posicao produzida por agente isolado tem qualidade comparavel a da rodada feita na mao em 2026-09-03. E o unico ponto de comparacao real que existe hoje, e ele e n=1.

## Decisoes

Herdadas, sem nova discussao, e listadas porque restringem o desenho desta spec:

- 0004/DEC-001: o que a automacao escreve na memoria do projeto so pode ser o que um comando comprova. Coletar posicao de agente e fato com execucao por tras; afirmar que as posicoes convergem nao e.
- 0004/DEC-016: escolha de modelo, esforco e modo continua sendo do usuario, com os perfis em `docs/MEMORY.md`. A automacao recebe o comando do agente e obedece, sem catalogo de modelo dentro da skill.
- 0004/DEC-019: o agente do loop **nao** escreve em `CONSENSUS.md`, e a razao foi especifica: uma rodada de loop tem um agente so, e consenso de um modelo so declarando a propria independencia e a fraude que os campos da 2.2.0 existem para denunciar. Esta spec precisa dizer se a razao se aplica quando ha N agentes (ver P-2), em vez de herdar a proibicao sem olhar.
- 0005/DEC-001: o projeto do usuario usado como evidencia da 0005 continua somente-leitura e nao e alvo desta spec.

Desta spec, todas ratificadas pelo usuario em 2026-09-03 a partir da rodada 1 cega registrada em `docs/CONSENSUS.md`. A rodada teve tres posicoes independentes (Claude selado antes das demais rodarem, Codex e Grok), e a forca de cada decisao esta declarada porque nem todas nasceram iguais:

- **DEC-001 (P-1, unanime nas tres posicoes):** a operacao preserva o **artefato bruto de cada agente** e gera uma **minuta deterministica** da entrada, com as posicoes reproduzidas sem resumo e os campos de julgamento em branco. Bruto e minuta nao sao alternativas: os tres modelos recusaram essa exclusao separadamente. A linha de corte e a mesma nos tres: a operacao para onde comeca o julgamento, e o teste pratico e se uma pessoa consegue conferir o campo olhando o artefato bruto ao lado. Consequencia aceita: a entrada nao nasce concluida, e entrada com consenso final vazio pode ser lida como acordo por omissao, o que se mitiga nascendo com `Status: aberto` e `Proximo passo` com dono humano.

- **DEC-002 (P-2, unanime no resultado, com o fundamento corrigido contra a posicao do Claude):** a operacao **pode escrever em `CONSENSUS.md`**, mas so o orquestrador mecanico escreve, e so o recorte que a execucao comprova: pergunta, posicoes literais, falhas, comandos, `Metodo`, `Exposicao previa` e `Rodada`. Os **agentes continuam proibidos**. O fundamento **nao e haver N agentes**, e sim separar os agentes opinantes de um **escritor deterministico**: Codex e Grok chegaram a essa correcao sozinhos, e o Claude, que havia proposto a justificativa pela cardinalidade, foi vencido. O Grok precisou o ponto: a DEC-019 nomeia o **agente**, entao aplica-la ao script nao seria heranca e sim estende-la a um sujeito que ela nunca nomeou. Consequencia aceita: passam a existir duas politicas de escrita no projeto (o loop nunca escreve la, este script escreve um recorte), e isso precisa estar dito no prompt de cada um.

- **DEC-003 (P-3, unanime, com as tres opcoes da pergunta rejeitadas):** o que se isola sao as **posicoes contemporaneas**, nao o repositorio. Leitura do repositorio permanece. E `CONSENSUS.md` nao e um degrau unico: em debate rodada 1 ele fica fora do material do agente; em revalidacao de achado a entrada sob revisao entra **de proposito**, porque e o objeto da pergunta. A escada `(a) < (b) < (c)` da pergunta estava errada, e a premissa empirica dela tambem: a rodada de 2026-09-03 rodou com sandbox `read-only` **e o repositorio visivel**, e foi lendo o codigo que o Codex achou o erro factual. Consequencia aceita: sandbox somente-leitura impede escrita e nao leitura, entao o isolamento real depende de material separado por agente, e nao de pedir cegueira no prompt.

- **DEC-004 (P-4, maioria de 2 a 1, com o Claude vencido):** a operacao cobre **debate e achado**, como dois pacotes sobre um primitivo unico de invocar agentes isolados e coletar artefatos. O Claude defendeu so debate, argumentando que existe um unico achado registrado e que ele proprio o escreveu, entao automatizar aquela forma seria automatizar um palpite n=1. Codex e Grok responderam o mesmo, separadamente: o caro e o isolamento e a invocacao, nao o template, e cortar o achado faz a spec nao resolver o problema que a motivou. Consequencia aceita: o esforco G cresce, com dois mapeamentos, dois prompts e evals proprios, e existe risco real de a primeira versao sair pela metade. Se o corte for inevitavel, a ordem e primitivo mais debate primeiro, e o pacote de achado na sequencia imediata, nunca adiado para outra spec.

- **DEC-005 (P-5, maioria de 2 a 1, com o Claude vencido e fato verificado do lado da maioria):** N e os comandos dos agentes entram **na chamada**, no mesmo contrato que o loop ja usa. A lista em `docs/MEMORY.md` e o padrao **deste usuario**, resolvido pelo agente de chat, e nunca configuracao lida por script nem catalogo dentro da skill. **`N=1` e valido**, porque debate quer `N>=2` e revalidacao de achado tem exatamente um revisor. O Claude propos guardar a lista em `MEMORY.md` como configuracao; conferido no codigo que isso contraria a pratica: o `loop.sh` recebe `--agente` e obedece, sem ler `MEMORY.md` em momento nenhum. Consequencia aceita: `MEMORY.md` desatualizado dispara o revisor errado, e nao ha teto global de custo, entao o usuario pode passar quatro agentes e queimar plano.

- **DEC-006 (P-6, maioria de 2 a 1, com a dissidencia registrada porque o argumento dela sobrevive):** a automacao cobre os **dois modos**, com a rodada 1 cega como padrao, e o modo escolhido **determina** o valor de `Exposicao previa` em vez de o usuario digitar. A operacao nunca deduz sozinha o numero da rodada nem quais posicoes anteriores fornecer. O Grok discordou e defendeu so a rodada 1 cega na primeira versao, com um argumento que continua valendo depois da derrota: rodada 2 exige o pacote **inteiro** das posicoes anteriores, e no instante em que o orquestrador resume, o Problema 3 volta por dentro da propria automacao. Consequencia aceita: quem implementar a rodada 2 tem de passar as posicoes anteriores na integra, e um resumo ali e regressao, nao otimizacao.


## Tarefas

- T-053: responder as perguntas abertas para a spec poder virar `Definida`

## Perguntas Abertas

P-1 a P-6 foram respondidas pela rodada 1 cega de 2026-09-03 e ratificadas pelo usuario no mesmo dia; viraram DEC-001 a DEC-006 acima. A rodada esta em `docs/CONSENSUS.md`, entrada "2026-09-03 - As seis perguntas da spec 0006", com as tres posicoes na integra.

Continuam abertas, e as duas passaram por rodada 1 cega em 2026-09-03, registrada em `docs/CONSENSUS.md`, entrada "2026-09-03 - P-7 e P-8". **As tres posicoes convergiram no que fazer nas duas**, e o que sobrou para o usuario e calibragem, nao empate:


- **P-7. A forma da entrada de `CONSENSUS.md` fica mesmo fora do escopo?** (aberta pela rodada 1: o Codex mostrou uma contradicao que o Claude nao viu). O modelo de debate tem secoes nomeadas para Codex, Claude e Gemini, e o de achado tem uma `Revalidacao` unica. Nenhum dos dois representa N agentes arbitrarios, falha individual de um agente, comando executado, hash de insumo, ou varias revalidacoes. Entao "N agentes" e "nao mexer na forma" nao cabem juntos. Ou a forma muda nesta spec, ou o requisito encolhe para o que ja e representavel, e isso enfraquece o objetivo. Qual dos dois? **Ficou mais urgente depois da DEC-004**, que mandou cobrir tambem o achado: sao duas formas para acomodar, nao uma.
  **Rodada 1: 3 de 3 pela forma entrar no escopo**, com secao repetivel por participante e id arbitrario nas duas formas, secao propria para agente que falhou, e check novo valendo so para entrada automatizada, por marcador opt-in (`**Origem:**`). Fato que barateia a decisao, conferido no codigo: **o validador nunca exigiu heading nomeado**. O congelamento em Codex, Claude e Gemini esta no template, e nao no contrato do script.
  **Calibragem em aberto:** os diagnosticos novos sao ERRO (Codex, porque em entrada automatizada a forma e contrato da operacao) ou AVISO (Grok, por simetria com o resto de consenso)?

- **P-8. Proveniencia entra no escopo?** (recomendada pelas **tres** posicoes da rodada 1, e por isso registrada em vez de decidida por mim). Hoje "Fora Do Escopo" nao a menciona e "Incluido" tambem nao. Os tres modelos disseram, com palavras diferentes, a mesma coisa: sem registrar comando, exit code e caminho do artefato ao lado da entrada, os campos `Metodo`, `Exposicao previa` e `Rodada` escritos pela automacao **voltam a ser autodeclaracao**, so que do script em vez do modelo, e o Resultado esperado 1 nao se cumpre. O custo e um sidecar por rodada e a decisao de onde ele mora, que esbarra em P-1 (o artefato bruto tambem precisa de casa).
  **Rodada 1: 3 de 3 por entrar**, com sidecar guardando bruto e manifesto fora do `CONSENSUS.md`, e ponte dentro da entrada. O bruto **nao** pode ficar em `.gitignore`, senao o teste da DEC-001, conferir o campo olhando o bruto ao lado, morre na sessao seguinte.
  **Calibragem em aberto:** quanto do manifesto a entrada repete? Codex quer comando, diretorio e hashes de insumo e saida **dentro** da entrada, lendo a DEC-002 ao pe da letra. Grok quer o comando integral so no manifesto e uma ponte curta, por rotacao e leitura humana. As duas leituras da DEC-002 se defendem.

- **P-9. Quando a minuta e escrita?** (conflito entre duas decisoes **ja ratificadas**, achado pelo Grok e sem dono ate agora). A DEC-003 manda o agente nao ver as posicoes **contemporaneas**; a DEC-006 manda o agente da rodada 2 ver as **anteriores** na integra. Se o orquestrador gravar a minuta no repositorio no meio da rodada, o repositorio visivel vaza o contemporaneo por dentro. Escrita atomica so no fim da rodada resolve, e custa retomada apos interrupcao e tratamento de colisao de execucao. Nenhuma das seis decisoes escolheu isso.
  **Rodada 1: 3 de 3 no desenho**, registrada em `docs/CONSENSUS.md`, entrada "2026-09-03 - P-9". O criterio operacional que resolve o conflito veio do Grok: **publicado e anterior, nao publicado e contemporaneo**. A DEC-003 e a DEC-006 nunca se contradisseram, falavam de momentos diferentes. Desenho: lock exclusivo por projeto na abertura; bruto e manifesto gravados assim que cada agente encerra, onde os agentes da rodada corrente nao alcancam; minuta escrita uma vez so, no fim, por substituicao atomica do arquivo inteiro, nunca append; interrupcao deixando o `CONSENSUS.md` byte a byte como estava e o material pago preservado.
  **Calibragem em aberto:** retomada apos interrupcao e automatica quando os insumos sao identicos (Codex) ou sempre exige palavra humana (Claude e Grok, 2 a 1)? E o bruto mora fora do repositorio ate o fecho (Codex e Claude) ou in-repo desde o inicio, fora da arvore de execucao (Grok)?
  **Nao resolvido pela rodada, e ninguem deve fingir que foi:** o bruto pode conter segredo do repositorio, e "preservar literal" (DEC-001) somado a "versionar" (P-8) cria caminho de exfiltracao permanente para o historico do git. Redacao automatica destruiria a evidencia que a DEC-001 existe para preservar. Precisa de decisao propria antes de qualquer linha de codigo.

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
