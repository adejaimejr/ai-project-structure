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
- Alterar qualquer projeto que nao seja este repositorio.

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

## Tarefas

- T-053: responder as perguntas abertas para a spec poder virar `Definida`

## Perguntas Abertas

Rodada 1 cega com **tres posicoes** (Claude selado, Codex, Grok), registrada em `docs/CONSENSUS.md`, entrada "2026-09-03 - As seis perguntas da spec 0006".

Resultado: **P-1, P-2 e P-3 unanimes**; **P-4, P-5 e P-6 por maioria de 2 a 1**, com o Claude vencido em P-4 e P-5; **P-7** nasceu da rodada anterior e segue aberta. **Nenhuma virou DEC:** parecer de modelo nao e decisao de projeto, e a regra de desempate manda o usuario decidir quando ele esta disponivel.

A rodada tambem confirmou quatro defeitos nesta spec, que nao dependem de decisao: a premissa falsa em P-3(c) sobre o isolamento da rodada de 2026-09-03; a nao independencia entre P-3, P-4 e P-6; o exemplo de revisores dentro do enunciado de P-5, que e o catalogo que a DEC-016 proibiu; e o "Fora Do Escopo" que confunde o projeto-evidencia da 0005 com o projeto-alvo de um script distribuido. Os tres modelos tambem recomendam mover **proveniencia** de fora para dentro do escopo.

- **P-1. O que a operacao entrega no fim?** (a) so o material bruto por agente, em arquivos, e a pessoa monta a entrada de `CONSENSUS.md`; (b) a entrada montada com as posicoes preenchidas e as secoes de julgamento ("Pontos De Acordo", "Consenso Final") em branco; (c) a entrada inteira, incluindo os pontos de acordo. Trade-off: (c) e o que mais economiza tempo e e onde a fraude volta pela porta dos fundos, porque quem sintetiza acordo esta julgando. (a) e o mais conservador e o que menos reduz o custo do Problema 2.

- **P-2. A automacao pode escrever em `CONSENSUS.md`?** A DEC-019 da 0004 proibiu o agente do loop, com motivo especifico: um agente so. Aqui sao N. Manter a proibicao por simetria, abrir excecao declarada para esta operacao, ou permitir a escrita apenas das secoes que nao envolvem julgamento (o que depende de P-1)?

- **P-3. Que grau de isolamento precisa ser garantido?** (a) cada agente nao recebe as posicoes dos outros no prompt; (b) alem disso, nao recebe o `CONSENSUS.md` do projeto, para nao ler rodada anterior; (c) alem disso, roda em sandbox somente-leitura e sem acesso ao repositorio, recebendo so a pergunta e o material minimo. Cada degrau custa mais e cobre mais. O degrau (c) foi o usado na mao em 2026-09-03 e funcionou, mas com um agente so.

- **P-4. Cobre debate, achado, ou os dois?** A revalidacao de achado e o caso que doeu de verdade neste repositorio, e ela tem forma propria: o que se revalida e a **disposicao**, nao o achado. Debate e o caso mais generico e o que o template ja descreve. Fazer os dois de uma vez aumenta o escopo; fazer so um deixa metade do problema.

- **P-5. Quantos agentes por rodada, e quem escolhe?** N fixo na ferramenta, N por chamada, ou uma lista de perfis nomeada em `docs/MEMORY.md` (ex: "revisores padrao: Codex e DeepSeek")? Lembrando que cada agente multiplica o consumo, e que a bancada mostrou uma ferramenta batendo limite de plano no meio de rodada.

- **P-6. A rodada 1 cega e obrigatoria por construcao?** O bloco core diz que na rodada 1 cada modelo preenche so a propria secao, sem ler as demais, e que da rodada 2 em diante a exposicao previa e esperada e declarada como `sim`. Isso sugere dois modos de execucao. A automacao cobre so a rodada 1 cega, os dois modos, ou trata a rodada 2 como caso manual?

- **P-7. A forma da entrada de `CONSENSUS.md` fica mesmo fora do escopo?** (pergunta nova, aberta pela rodada 1: o Codex mostrou uma contradicao que o Claude nao viu). O modelo de debate tem secoes nomeadas para Codex, Claude e Gemini, e o de achado tem uma `Revalidacao` unica. Nenhum dos dois representa N agentes arbitrarios, falha individual de um agente, comando executado, hash de insumo, ou varias revalidacoes. Entao "N agentes" e "nao mexer na forma" nao cabem juntos. Ou a forma muda nesta spec, ou o requisito encolhe para o que ja e representavel, e isso enfraquece o objetivo. Qual dos dois?

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
