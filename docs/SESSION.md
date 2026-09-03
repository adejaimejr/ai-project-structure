# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas mais antigas foram rotacionadas para `docs/archive/SESSIONS-2026.md`. Este arquivo mantem as 7 mais recentes.

## Modelo Para Nova Sessao

```md
## AAAA-MM-DD - Nome do agente

### Objetivo

- 

### O Que Foi Feito

- 

### Arquivos Criados Ou Alterados

- 

### Decisoes Tomadas

- 

### Aprendizados Para MEMORY.md

- (Liste apenas o que satisfaz criterio de promocao em MEMORY.md. Se nada se aplica, escreva "Nenhum".)

### Pendencias

- (Pendencias acionaveis devem virar tasks em TASKS.md antes de fechar a sessao.)

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): 
- Motivo: 
```

## 2026-09-03 - Claude, Codex e Grok (rodada de P-9, o conflito entre DEC-003 e DEC-006)

### Objetivo

- Responder P-9, que nao e pergunta de desenho novo: e conflito entre duas decisoes ratificadas no mesmo dia.

### O Que Foi Feito

- **3 de 3 no desenho**, e o criterio que resolve o conflito veio do Grok: **publicado e anterior, nao publicado e contemporaneo**. A DEC-003 e a DEC-006 nunca se contradisseram; elas falavam de momentos diferentes, e faltava alguem escolher o instante da gravacao. Os tres classificaram o caso como **lacuna**, nao contradicao, e nenhum pediu para reverter decisao ratificada.
- Desenho convergente: lock exclusivo por projeto na abertura, bruto e manifesto gravados assim que cada agente encerra fora do alcance dos demais, minuta escrita uma vez so no fim por substituicao atomica do arquivo inteiro, e interrupcao deixando o `CONSENSUS.md` byte a byte como estava.
- **Argumento que sozinho ja proibe publicar cedo, e veio de uma decisao ratificada:** a DEC-005 tornou `N=1` valido, entao minuta a meio com 1 de 3 posicoes e **indistinguivel de uma corrida `N=1` concluida**. Nao e so vazamento, e ambiguidade de leitura. So o Grok fez essa ligacao.
- **O risco mais grave da rodada nao tem solucao proposta por ninguem.** O Codex mostrou a armadilha inteira: o bruto pode conter segredo do repositorio; a DEC-001 exige preservar literal; a P-8 aponta para artefato versionado; e redigir automaticamente destruiria justamente a evidencia. As tres posicoes juntas nao produziram saida. Ficou escrito na spec como nao resolvido.
- **Dois defeitos do codigo publicado apareceram como efeito colateral**, os dois conferidos antes de aceitos, e viraram T-057 e T-058: `loop_task.py:147` grava `TASKS.md` com `write_text` direto, que nao e atomico e pode rasgar o arquivo de memoria; e o `loop.sh` nao protege contra duas rodadas simultaneas, porque o sinal de pergunta tem nome fixo e o arranque apaga o leftover da rodada anterior.
- Duas ressalvas de independencia registradas na entrada, as duas **contra** a forca desta rodada: quem descobriu o conflito foi o Grok, entao ele respondeu a propria pergunta, ainda que sem lembrar do argumento; e o enunciado que os tres leram e a transcricao que o Claude fez do achado dele. Se a transcricao estreitou o problema, os tres herdaram o estreitamento.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Nenhuma. O desenho de P-9 vira DEC-007 quando o usuario ratificar, e uma parte dele deve subir para `docs/DECISIONS.md`: escrever arquivo de memoria por substituicao atomica, nunca por escrita direta, porque isso vale para o `loop_task.py` ja publicado.

### Aprendizados Para MEMORY.md

- Nenhum novo. O que apareceu virou tarefa (T-057, T-058) por ser defeito de codigo, e nao licao reutilizavel.

### Pendencias

- T-053 acumula tres calibragens (P-7, P-8, P-9) mais a pergunta de segredo no bruto, que nenhuma rodada resolveu.
- T-057 tem prioridade alta: e o unico dos defeitos abertos que pode **destruir** dado do usuario, e nao so reportar errado.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-057, que nao depende de decisao nenhuma; o usuario para as calibragens.
- Motivo: T-057 e conserto de duas linhas com risco real de perda de arquivo, e esta parado atras de decisoes de escopo que nao tem relacao com ele.

## 2026-09-03 - Claude, Codex e Grok (rodada 1 de P-7 e P-8)

### Objetivo

- Responder as duas perguntas que sobraram da spec 0006, com Codex e Grok, a pedido do usuario.

### O Que Foi Feito

- **Primeiro uso da DEC-003**, ratificada horas antes. Os agentes rodaram numa copia do repositorio com o corpo da entrada da rodada anterior **retido**, e uma nota no lugar dizendo que a omissao era proposital. Reter sem avisar faria os dois concluirem que nenhuma rodada havia acontecido, que e falso. O modelo de debate e o de achado ficaram na copia, porque **sao o objeto de P-7**.
- **3 de 3 nas duas perguntas.** A forma entra no escopo e a proveniencia entra no escopo. Nao houve empate: o que sobrou foi calibragem.
- **O achado que mais barateia P-7, conferido no codigo:** o validador **nunca exigiu heading de posicao nomeado**. As unicas exigencias de heading no script inteiro sao as de `SESSION.md` e a de "Por Que Nada Pegou Antes". O congelamento em Codex, Claude e Gemini esta no **template**, e nao no contrato. O Grok viu isso e recusou o binario da pergunta, partindo "forma" em tres camadas que ja nao coincidiam.
- Codex e Grok chegaram, sem combinar, ao mesmo mecanismo para nao quebrar o criterio de "projeto que nao automatiza nao ganha cobranca nova": um marcador `**Origem:**` que faz os checks novos valerem so para entrada automatizada. O Claude tinha declarado esse exato ponto como "buraco que nao sei resolver"; os outros dois resolveram.
- **Conflito entre duas decisoes ja ratificadas, achado pelo Grok:** DEC-003 proibe ver posicao contemporanea e DEC-006 exige ver as anteriores, e nenhuma das duas escolheu **quando** a minuta e escrita. Escrita incremental no meio da rodada vaza o contemporaneo pelo proprio repositorio. Virou P-9.
- **Tres defeitos da 2.5.0 atual**, achados pelos dois e conferidos no codigo antes de aceitos, viraram T-054 e T-055: `Rodada` ausente nao gera diagnostico nenhum; `re.match` em vez de `fullmatch` deixa passar lixo depois do valor; e o `Modelo De Debate` da raiz esta atras do asset da skill nos campos da 2.2.0.
- Um quarto defeito apareceu ao escrever a propria spec e virou T-056: `spec_overview` conta sub-item indentado como pergunta aberta, e a spec 0006 passou a reportar 7 perguntas quando tinha 3.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`.

### Decisoes Tomadas

- Nenhuma. As duas convergencias esperam ratificacao, e P-9 espera decisao.

### Aprendizados Para MEMORY.md

- Nenhum novo. Os desta sessao ja foram promovidos nas entradas anteriores.

### Pendencias

- T-053 segue em "Aguardando Usuario", agora com duas calibragens e P-9.
- T-054, T-055 e T-056 sao defeitos do que ja esta publicado, independentes da spec 0006. T-054 nao e conserto obvio: fechar os dois buracos para toda entrada e cobranca nova em projeto existente, o que esbarra num criterio de aceite da propria 0006.
- A transcricao continua sendo feita pelo modelo criticado. O risco registrado na rodada anterior nao foi resolvido por esta, e nao sera enquanto a operacao nao existir.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para as duas calibragens e P-9.
- Motivo: P-9 e o mais urgente dos tres, porque e conflito entre decisoes ja ratificadas, e nao pergunta nova. Enquanto ele nao for decidido, DEC-003 e DEC-006 se contradizem no papel.

## 2026-09-03 - Claude (ratificacao das seis perguntas da spec 0006)

### Objetivo

- Transformar em decisao o que a rodada 1 cega produziu, apos o usuario ratificar as seis.

### O Que Foi Feito

- **DEC-001 a DEC-006 escritas na spec 0006**, cada uma declarando **como** foi decidida, e nao so o que ficou decidido. Tres unanimes, duas em que o Claude foi vencido por 2 a 1, e uma com dissidencia registrada.
- A forca da decisao entrou no texto de proposito. DEC-004 e DEC-005 dizem que o Claude perdeu e por que; DEC-006 registra o argumento do Grok que perdeu mas sobrevive, e a consequencia pratica dele: quem implementar a rodada 2 tem de passar as posicoes anteriores na integra, porque resumo ali e regressao e nao otimizacao.
- **DEC-002 subiu para `docs/DECISIONS.md`**, porque muda o alcance de uma decisao ja registrada do projeto. A 0004/DEC-019 proibia o **agente** de escrever consenso; agora fica dito que a proibicao e sobre agente e nao sobre software, que um orquestrador mecanico escreve o recorte comprovado, e que o que sustenta a excecao e a separacao entre quem opina e quem escreve, nunca a quantidade de agentes. As outras cinco ficaram so na spec.
- Corrigido o defeito de escopo que o Grok apontou: "alterar qualquer projeto que nao seja este repositorio" confundia o projeto-evidencia da 0005 com o projeto-alvo de um script distribuido. Reescrito sem ambiguidade, e declarado que nao e mudanca de escopo.
- Os outros tres defeitos apontados eram **nas perguntas**, e sairam junto com elas ao virarem DEC. Ficaram registrados dentro das decisoes correspondentes, em vez de apagados: a DEC-003 diz que a premissa empirica de P-3(c) era falsa, e a DEC-005 diz que o exemplo de revisores no enunciado era o catalogo que a DEC-016 proibiu.
- Sobraram duas perguntas: **P-7**, sobre a forma da entrada, que ficou mais urgente porque a DEC-004 mandou cobrir tambem o achado, e sao duas formas para acomodar; e **P-8**, nova, sobre proveniencia entrar no escopo. Registrei P-8 em vez de decidir sozinho, mesmo com as tres posicoes recomendando: recomendacao unanime de modelos continua nao sendo decisao de projeto.
- Entrada de consenso fechada como `resolvido`, com o que ficou de fora da ratificacao dito na propria linha de `Resolvido em`.

### Arquivos Criados Ou Alterados

- Projeto: `docs/specs/0006-automacao-do-consenso.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- DEC-001 a DEC-006 na spec 0006, ratificadas pelo usuario.
- Em `docs/DECISIONS.md`: agente nao escreve consenso, orquestrador deterministico escreve o recorte que a execucao comprova.

### Aprendizados Para MEMORY.md

- Nenhum novo. Os desta sessao (o caminho do `cursor-agent`, e que as CLIs se atualizam sozinhas) ja foram promovidos na entrada anterior.

### Pendencias

- T-053 segue em "Aguardando Usuario", agora so com P-7 e P-8.
- A spec continua `Rascunho`: as duas perguntas restantes mexem em escopo, entao nenhuma das duas e cosmetica.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para P-7 e P-8.
- Motivo: as duas sao escopo, e P-7 ficou acoplada a DEC-004. Decidir P-7 sem lembrar que agora sao duas formas a acomodar levaria a uma resposta que a propria ratificacao ja invalidou.

## 2026-09-03 - Claude, Codex e Grok (rodada 1 cega das perguntas da spec 0006)

### Objetivo

- Responder as seis perguntas abertas da spec 0006 consultando Codex e Grok, a pedido do usuario.

### O Que Foi Feito

- **Primeira rodada de consenso cega de verdade deste projeto, e ela e sobre a spec que quer automatizar exatamente isso.** A posicao do Claude foi escrita e selada em arquivo fora do repositorio **antes** de qualquer agente rodar; escrever depois seria `debate-aberto` disfarcado de parecer independente.
- Codex rodou com `codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high"`, com o mesmo arquivo de prompt, em processo separado e saida em arquivo proprio.
- A CLI propria do Grok recusou cinco vezes, com `You've reached your free Grok Build usage limit`, mesmo com o usuario assinando hoje e refazendo o login no meio. **A rodada so aconteceu por outro caminho:** o `cursor-agent`, ja instalado e autenticado com a assinatura do Cursor, expoe `cursor-grok-4.6-xhigh`. Rodou em `--mode ask`, read-only por construcao em vez de "nao edite" no prompt.
- Diagnostico do bloqueio do Grok foi refeito uma vez. A primeira leitura culpou o tamanho do pedido, porque um prompt de 20 bytes passava e um de 2858 falhava; a sonda de enchimento derrubou isso, porque 1000 bytes tambem falhou depois. O que separa passar de falhar e o momento: franquia pequena que repoe.
- Resultado com tres posicoes: **tres unanimidades (P-1, P-2, P-3), duas derrotas do Claude por 2 a 1 (P-4 e P-5), e uma maioria com dissidencia substantiva (P-6)**.
- Em P-1 e P-3 os tres recusaram as opcoes que a pergunta oferecia, cada um por conta propria. Recusas que coincidem valem mais que votos na mesma alternativa.
- **O Grok achou o risco que estava acontecendo no proprio registro:** se quem dispara a operacao for o modelo criticado, o Problema 3 sobrevive mesmo com N agentes isolados. Quem isolou as tres posicoes e escreveu o resumo das tres foi o Claude, que e uma delas e o alvo das outras duas. O isolamento resolveu a producao das posicoes e nao a transcricao.
- Ele tambem mostrou que a **ancora empirica da spec e falsa**: P-3(c) descreve "sem acesso ao repositorio", e a rodada de 2026-09-03 teve o repositorio visivel, sendo justamente a leitura do codigo que fez o Codex achar o erro factual. Mais tres defeitos confirmados na spec, todos independentes de decisao.
- Em P-1 e P-3 os dois modelos **recusaram as opcoes da pergunta**, independentemente e pelo mesmo motivo. E o sinal mais forte da rodada, porque nao e concordancia com uma opcao oferecida, e sim duas recusas que coincidem.
- O Codex corrigiu o fundamento da P-2 do Claude: a excecao a DEC-019 nao se sustenta por haver N agentes, e sim por separar os agentes opinantes de um **escritor deterministico**. Se quem escreve for um dos opinantes, o acoplamento volta com N igual a qualquer coisa.
- Tres criticas dele mudaram a spec no ato. A primeira foi conferida no codigo antes de aceita: o reuso do `loop.sh` estava superestimado, porque `loop.sh:145` decide se o agente fez algo com `find -type f -newer`, e agente de parecer nao escreve nada, entao cairia no `exit 4` da DEC-014 sempre. Corrigido no Problema 4, com a correcao declarada.
- A segunda virou **P-7**: "N agentes" e "nao mexer na forma" nao cabem juntos, porque nem o modelo de debate (secoes nomeadas para Codex, Claude e Gemini) nem o de achado (uma `Revalidacao` unica) representam N arbitrario, falha individual ou hash de insumo. Contradicao de escopo que o Claude nao tinha visto.
- A terceira ficou registrada como risco: a DEC-001 foi generalizada alem do que ela prova. Um comando comprova exit code e bytes; nao comprova qual modelo respondeu, se houve fallback, nem se o isolamento existiu.
- **A entrada bateu no defeito que ela mesma descreve.** O campo `**Rodada:** 1 de 1` afirma um denominador que ninguem sabe, e o Codex acabara de apontar que `N de N` ficou fragil depois que o teto saiu. Registrado nos riscos da propria entrada.
- `CONSENSUS.md` passou de 30KB e disparou `AVISO|ROTACAO`. A revisao da spec 0003, de 2026-09-02, foi para `docs/archive/CONSENSUS-2026.md`, que ficou com tres entradas.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/MEMORY.md`, `docs/SESSION.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`.
- Dois escorregoes meus na mesma sessao, os dois registrados: usei `t.index()` para cortar secoes da entrada e o indice casou com o **modelo cercado no topo do arquivo**, duplicando a entrada inteira; restaurado por `git checkout` (seguro desta vez, porque so aquele arquivo estava sujo) e refeito com ancora a partir do inicio da entrada. E antes disso, o diagnostico errado do bloqueio do Grok.

### Decisoes Tomadas

- **Nenhuma.** Quatro perguntas convergiram e continuam sem virar DEC, de proposito: parecer de modelo nao e decisao de projeto, e a regra de desempate diz que quem decide e o usuario quando ele esta disponivel.

### Aprendizados Para MEMORY.md

- **`cursor-agent` promovido como caminho de agente**, com os perfis de consenso e de loop, a nota de que os degraus de esforco vem no nome do modelo, e a de que o formato encaixa no `loop.sh` sem mudar nada porque `loop.sh:141` anexa o prompt como ultimo argumento.
- Promovido tambem que `grok` e `cursor-agent` **se atualizam sozinhos**, com o caso concreto de hoje: o `grok` foi de `1.0.5` para `1.0.13` no meio do diagnostico.
- Fato do usuario atualizado com sobrescrita ativa: ele assinou o Grok em 2026-09-03 e a CLI propria continua tratando a conta como free tier.

### Pendencias

- T-053 continua em "Aguardando Usuario", agora com cinco pedidos: ratificar as tres unanimes, ratificar ou virar as tres de maioria, decidir P-7, decidir se proveniencia entra no escopo, e mandar corrigir os quatro defeitos confirmados.
- `CONSENSUS.md` passou de 30KB de novo, e a rotacao expos uma tensao na propria regra: ela manda manter "as 5 a 10 mais recentes" e rotacionar acima de 30KB, e com poucas entradas grandes as duas metades se contradizem. Rotacionei o achado `0005-A1`, ja `resolvido` e com residuo fechado, em vez de encurtar a entrada nova, porque encurtar para o portao ficar verde e o que a regra "Nao Apague O Que Falha" proibe. Nao virou tarefa: e n=1 e pode nao se repetir.
- O artefato bruto de cada agente ficou fora do repositorio e nao foi preservado, contra o que a resposta de P-1 dos dois modelos recomenda. Nao virou tarefa porque o destino desse artefato e parte do que P-1 decide.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: sao cinco pedidos e nenhum deles e do agente. O mais interessante ficou sendo P-6: o Grok perdeu por 2 a 1, e o argumento dele (rodada 2 exige o pacote inteiro, e no instante em que o orquestrador resume o Problema 3 volta por dentro da automacao) sobrevive a derrota e vale ser lido antes de ratificar a maioria.

## 2026-09-03 - Claude (fixture de controle do criterio de achado)

### Objetivo

- T-052, o ultimo residuo da rodada 2 do achado `0005-A1`: exercitar literalmente o criterio "projeto que nunca registra achado nao recebe nenhum aviso novo".

### O Que Foi Feito

- Fixture `debate-project`: projeto que **usa** consenso de verdade e nunca declara `**Achado:**`. Oracle de conjunto vazio em `--strict`, que nesta arquitetura nao e teste fraco, porque a comparacao e nos dois sentidos e qualquer diagnostico reprova.
- Quatro controles no mesmo `CONSENSUS.md`: cerca dentro do corpo de uma entrada citando `**Achado:**`; entrada anterior a data de adocao, sem os campos declarativos; entrada na rodada 5 com `Pendente da rodada anterior`; e entrada que declara `Escapou de verificacao` **sem** declarar `Achado`, que fixa o opt-in do formato.
- Correcao de rota no meio: a primeira versao da fixture punha o modelo de achado cercado no topo do arquivo e o README dizia que aquilo guardava `strip_fences`. Nao guardava: o modelo fica antes de qualquer entrada datada e nunca entra em corpo de entrada. A cerca foi movida para dentro de uma entrada, e so entao o controle passou a existir.
- **Provado por mutacao, com duas rodadas.** Mutacao A (formato de achado deixa de ser opt-in): 37 de 44, com 6 diagnosticos inesperados so nesta fixture. Mutacao B (`strip_fences` para de limpar cercas): 42 de 44, e **so esta fixture acusou**. As outras cinco seguiram verdes, que e exatamente o buraco que T-052 existia para fechar.
- Reversao das mutacoes por backup em `cp`, e nao por `git checkout`, aplicando a licao da sessao anterior.

### Arquivos Criados Ou Alterados

- Skill: `evals/fixtures/debate-project/` (novo, 14 arquivos), `evals/verify_repository.py`, `CHANGELOG.md`.
- Projeto: `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. A fixture **fixa** uma decisao ja tomada na spec 0005: o formato de achado e opt-in pelo campo `**Achado:**`, entao entrada que declara `Escapou de verificacao` sem declarar `Achado` segue sendo debate e nao e cobrada. Mudar isso passa a ser mudanca visivel, e nao silenciosa.

### Aprendizados Para MEMORY.md

- Promovidos dois, no fechamento do dia: portao novo so entra depois de a mutacao provar que ele acusa; e reverter mutacao temporaria por backup proprio, nunca por `git checkout`, quando o arquivo tem trabalho nao commitado.
- O aprendizado anterior sobre check AVISO e portao continua valendo sem alteracao.

### Pendencias

- Nenhuma. Backlog zerado, cinco specs `Concluida`, "Aguardando Usuario" vazia.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, e de preferencia o proprio usuario usando a 2.5.0 em projeto real.
- Motivo: a spec 0005 fechou e o residuo dela tambem. O que vem agora depende de uso: o formato de achado so tem um achado registrado, e a forma dele ainda e n=1.

## 2026-09-03 - Claude (skill 2.5.0, diagnostico com identidade)

### Objetivo

- Fazer T-050 e T-051 juntas, que sao o mesmo desenho: tirar do portao a dependencia de exit code e de texto de mensagem.

### O Que Foi Feito

- T-051: os 39 diagnosticos de `validate_structure.py` ganharam codigo estavel, declarado no conjunto `CODIGOS`. `Report.add` recusa codigo nao declarado, entao diagnostico sem identidade quebra na hora de escrever. Um check estatico por AST conferiu que nenhum dos 39 sites ficou sem codigo e que nenhum codigo declarado sobrou sem uso.
- Flag `--codigos` nova: `NIVEL|CODIGO|ARQUIVO|SUJEITO`, uma linha por diagnostico, sem prosa. O `SUJEITO` (tarefa, entrada de consenso ou spec) e a peca que faltava: e ele que denuncia aviso que passou a cair na entrada errada, com codigo e contagem identicos.
- T-050: `FIXTURES` deixou de mapear nome para exit code e passou a declarar modo, exit esperado e o conjunto exato de diagnosticos. Comparacao nos dois sentidos, e fixture sem a chave `diagnosticos` e recusada em vez de virar aprovacao silenciosa. `verificar_achado` foi absorvida: um mecanismo, nao dois.
- **Discriminacao provada por mutacao, nao por afirmacao.** Tres mutacoes temporarias, revertidas depois: regressao compensada (o contraexemplo exato do Codex, com total e exit code identicos), sujeito trocado com codigos identicos, e fixture declarada sem oracle. As tres reprovaram; a primeira e a segunda passariam verdes na contagem de linhas antiga.
- Versao 2.5.0: mudou script distribuido e o formato da saida virou contrato publico, entao nao cabia amendar a 2.4.0. Marcadores dos tres blocos subiram juntos por DEC-009, com o conteudo do bloco core inalterado.
- Publicada: `git push origin main` levou `e70bd7c..28681fd`, e `./install.sh` propagou a 2.5.0 para os tres destinos globais, com paridade conferida por `diff -rq` e a flag `--codigos` presente nos tres.
- `SESSION.md` passou de 30KB e disparou `AVISO|ROTACAO`. Rotacionadas as quatro entradas mais antigas para `docs/archive/SESSIONS-2026.md`, que ficou com 24, mantendo as 6 mais recentes aqui e atualizando o indice do arquivo. Primeira vez que o aviso foi lido ja pelo codigo, e nao pela prosa.

### Arquivos Criados Ou Alterados

- Skill: `scripts/validate_structure.py`, `evals/verify_repository.py`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/SESSION.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.

### Decisoes Tomadas

- Identificador estavel escolhido pelo usuario na rodada 2 do achado `0005-A1`. Implementado como codigo por diagnostico, com a saida `--codigos` separada do relatorio humano: o relatorio continua legivel e o portao ganha um formato que nao muda quando a redacao muda.

### Aprendizados Para MEMORY.md

- Nenhum novo. O aprendizado ja registrado sobre check AVISO foi atualizado para apontar a implementacao em vez da tarefa pendente.

### Pendencias

- Escorreguei uma vez: usei `git checkout` para reverter uma mutacao de teste em `verify_repository.py`, que e arquivo versionado com trabalho **nao commitado** por cima, e apaguei a reescrita inteira. Refeita na hora, sem perda. A licao e de operacao, nao do produto: para reverter mutacao temporaria em arquivo com trabalho pendente, guarde o original antes em vez de confiar no git.
- T-052 continua aberta e independente destas duas.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para T-052.
- Motivo: a fixture so-debate e o unico residuo da rodada 2 que sobrou, e agora ela tem onde encaixar: entra no `FIXTURES` com oracle de conjunto vazio em `--strict`.

## 2026-09-03 - Claude e Codex (rodada 2 do achado 0005-A1)

### Objetivo

- Revalidar a disposicao do achado `0005-A1` com um modelo distinto, a pedido do usuario. Primeiro uso real da revalidacao que a 2.4.0 acabou de criar.

### O Que Foi Feito

- Rodada 2 no Codex CLI (`gpt-5.6-sol`, `model_reasoning_effort=high`, sandbox `read-only`, para ele nao poder editar nada). Prompt adversarial pedindo especificamente casos em que `verificar_achado` ficaria verde com o comportamento errado.
- Veredito do Codex: **se sustenta com ressalva**. Tres criticas conferidas no codigo antes de aceitar, e as tres procedem.
- **A disposicao da rodada 1 descrevia mal o proprio codigo.** Ela dizia que o check passou a medir "qual aviso", e `verificar_achado` conta linhas `[AVISO]` e confere uma unica exclusao. A entrada de `DECISIONS.md` tinha herdado o mesmo exagero: corrigida, com a correcao declarada em vez de silenciosa.
- **T-050 contradizia a propria disposicao.** Recusar par com o mesmo exit code nos dois lados eliminaria justamente a guarda que a disposicao mandou manter (`achado-project` tem os dois lados em 0 de proposito). Reescrita para exigir oracle discriminante por fixture.
- **O criterio "projeto que nunca registra achado nao recebe aviso novo" nao e exercitado literalmente**: os dois lados de `achado-project` tem achado, e a unica fixture com entrada de debate (`v1-project`) roda sem `--strict`. Virou T-052.
- Onde a revalidacao ficou incompleta, tambem registrado: o Codex nao viu que a raiz ja e um controle vivo desse ultimo item, porque roda em `--strict`, tem entrada de debate e fecha com zero avisos. Controle parcial, e a critica sobrevive reduzida.
- `**Escapou de verificacao:** sim` mantido contra a ressalva do Codex: o criterio da DEC-007 e se a verificacao existente pegaria o defeito, e ela nao pegaria.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. Uma decisao existente (fixture de check AVISO, 2026-09-03) foi **corrigida**: a regra segue valendo, a descricao que ela fazia da implementacao estava errada.

### Aprendizados Para MEMORY.md

- Refinamento do aprendizado ja promovido: contar linhas `[AVISO]` nao basta, porque aceita regressao compensada. Atualizado no lugar em vez de duplicado.

### Pendencias

- Nenhuma bloqueante. T-051 chegou a entrar em "Aguardando Usuario" com a pergunta "identificador estavel de diagnostico ou fragmento da mensagem?", e o usuario respondeu no mesmo dia: **identificador estavel**. A tarefa voltou para "Proximas Tarefas" com a escolha escrita nela. O achado `0005-A1` passou para `resolvido`, com o residuo em T-050, T-051 e T-052.
- Observacao sobre a forma, ainda n=1: o primeiro achado deste repositorio precisou de duas rodadas, e a rodada 2 achou erro factual na rodada 1. Isso e o formato funcionando, nao falhando, mas vale ver se o padrao se repete antes de tirar conclusao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, atacando T-051 e T-050 juntas.
- Motivo: as duas dependem do mesmo desenho (identificador estavel de diagnostico), ja escolhido pelo usuario. Separadas, o oracle seria escrito duas vezes.
