# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas mais antigas foram rotacionadas para `docs/archive/SESSIONS-2026.md`. Este arquivo mantem as 6 mais recentes.

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

## 2026-09-03 - Claude (skill 2.4.0, consenso que serve para achado)

### Objetivo

- Implementar a spec 0005: `CONSENSUS.md` passa a registrar achado, e nao so debate.

### O Que Foi Feito

- T-046: bloco core em v2.4.0 com tres mudancas. `### Achado` (identificador, disposicao, revalidacao), `### Ponto Cego Da Validacao Cruzada` em duas linhas, e o teto de rodadas trocado pela exigencia de `**Pendente da rodada anterior:**` acima de tres. Editado so no `assets/AGENTS.md` e propagado byte a byte para a raiz por script.
- DEC-008 fechou a mitigacao que DEC-002 deixou para a implementacao: o campo chama-se `**Achado:**` e o valor dele **e** o identificador. Um campo so marca e identifica, em vez de dois que podem discordar entre si.
- T-047: checks no validador, todos AVISO e todos opt-in. Antes de trocar a regra de rodada, conferido o que quebrava: a unica entrada real com `Rodada` na raiz e `2 de 3`, abaixo do limiar, e nenhuma fixture declarava rodada. So a mensagem de formato e o texto dos templates dependiam do teto.
- T-048: fixture `achado-project`, com a mesma entrada de debate abrindo os dois lados como controle. Foi ao escrever essa fixture que apareceu o achado do dia, abaixo.
- T-049: dogfood, CHANGELOGs, e reinstalacao com paridade conferida nos tres destinos globais.
- **Achado `0005-A1`, primeiro achado registrado neste repositorio, e sobre o proprio repositorio.** O padrao de fixture herdado da 2.2.0 (par `valido`/`invalido` com exit code esperado no `FIXTURES`) so funciona porque todo check daquela versao era ERRO. Os checks de achado sao AVISO, entao o par teria os dois lados em exit 0 e a suite reportaria `[OK] fixture achado-project/invalido: exit 0 (esperado 0)`: verde, sem provar nada. Corrigido com `verificar_achado`, que roda os dois lados em `--strict`, conta os avisos e confere que nenhum cita a entrada de debate.
- O conserto de portao que sobrou do achado virou T-050: fazer o `verify_repository.py` recusar um par cujos dois lados declarem o mesmo exit code, em vez de depender de quem escrever a proxima fixture lembrar disso.

### Arquivos Criados Ou Alterados

- Skill: `assets/AGENTS.md`, `assets/docs/CONSENSUS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `references/atualizacao.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/evals.json`, `evals/fixtures/achado-project/` (novo).
- Projeto: `AGENTS.md`, `docs/CONSENSUS.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/SESSION.md`, `docs/specs/0005-consenso-para-achados.md`.

### Decisoes Tomadas

- DEC-008 na spec 0005: o campo do identificador de achado e `**Achado:**`, com o identificador como valor.
- Em `docs/DECISIONS.md`: fixture cujo caso invalido produz apenas AVISO roda em `--strict` e confere **quais** avisos sairam, nunca so quantos exit codes bateram.

### Aprendizados Para MEMORY.md

- Check novo que e AVISO nao separa fixture pelo exit code. Promovido, com ponteiro para o achado `0005-A1` e para a decisao.

### Pendencias

- O achado `0005-A1` esta com `**Status:** aberto` de proposito: a disposicao dele nao passou por ninguem alem de quem a escreveu, e a secao `### Revalidacao` esta com `(A preencher.)`. Fechar o status depende de um modelo distinto, ou do usuario, olhar a disposicao.
- Observacao de desenho, sem tarefa: o achado herdou `**Metodo:**` e `**Exposicao previa a outras posicoes:**`, que nasceram para debate. Num achado de um modelo so, a resposta honesta e `pareceres-independentes` com `nao`, o que e verdade mas soa estranho. Nao virou tarefa porque e n=1 e a forma pode encaixar melhor depois de alguns achados reais.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): um modelo distinto do Claude, e depois qualquer agente para T-050.
- Motivo: o achado `0005-A1` esta aberto esperando revalidacao independente, e revalidar a propria disposicao com o mesmo modelo e exatamente o que os campos de independencia existem para denunciar.

## 2026-09-03 - Claude, Codex, Grok e DeepSeek (bancadas de uso real do loop)

### Objetivo

- Usar o modulo de loop em tarefa de verdade, com a grade de perfis, e descobrir onde ele incomoda antes de confiar nele.

### O Que Foi Feito

- Grade de perfis fechada (T-038): `planejar` para Grok e opencode, e os degraus do DeepSeek remapeados a pedido do usuario. So o `grok-4.6` entrou, porque foi o unico exercitado; `--variant` saiu dos perfis DeepSeek por nao haver como confirmar efeito.
- Bancada 3 (T-039), primeira em projeto que **nao e codigo**: manual em Markdown, portao proprio, sete problemas plantados em cinco arquivos. Serviu para testar uma promessa da estrutura que nunca tinha sido exercitada.
- Achado principal: o agente fechou o portao **apagando** a frase que continha o link quebrado. Verde, informacao perdida. Em codigo isso salta aos olhos; em conteudo parece edicao. Virou a regra "Nao Apague O Que Falha".
- Segundo achado (T-039): a regra de estimar dificuldade lendo a tarefa nunca acertou e foi removida. Somando as tres bancadas, quatro ferramentas e tarefas bem diferentes, todas terminaram verdes na primeira tentativa, varias no modelo mais barato. Sobrou escalar so por falha observada ou por pedido do usuario.
- Matriz das quatro ferramentas (T-040), com consumo medido pela primeira vez. Resultado que inverte a leitura ingenua de exit code: a **unica** que fechou o portao foi a unica que destruiu informacao; as duas que sairam com exit 3 perguntando fizeram a coisa certa.
- DEC-018, o achado com mais alcance do dia: a regra vivia no bloco do `AGENTS.md` e foi ignorada; movida para o prompt do `loop.sh`, sem mudar mais nada, o mesmo modelo passou a perguntar. Ler o `AGENTS.md` e escolha do agente; o prompt chega sempre.
- Matriz refeita (T-041) confirmou, e o consumo **caiu** em todas as ferramentas, uma delas pela metade: dizer a restricao antes evita explorar caminho que seria descartado.
- Revisao item a item do bloco (T-042) pelo criterio da DEC-018. Cinco restricoes precisam do prompt, tres podem ficar so no bloco, e o unico buraco encontrado foi a ausencia de qualquer instrucao impedindo o agente de editar `AGENTS.md` e os arquivos de memoria. Risco teorico (nenhuma das nove rodadas fez isso), fechado mesmo assim porque o pior caso e silencioso.
- Variancia medida (T-043): Claude e Codex deterministicos nesta tarefa, tres de tres cada. DeepSeek com duas rodadas destrutivas antes da regra chegar ao prompt e zero em seis depois.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop.sh`, `references/loop.md`, `assets/partials/AGENTS-loop-block.md`, `CHANGELOG.md`, `README.md`.
- Projeto: `AGENTS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-018 na spec 0004: restricao critica vai no prompt, nao so no bloco. Criterio para decidir: se a violacao deixa o portao verde do mesmo jeito, a regra precisa do prompt.
- Escolha de degrau deixou de estimar dificuldade a priori.
- Perfil do Grok e do opencode fechados, com o degrau mais alto do Grok apontando para o teto dele, avisado na hora.

### Aprendizados Para MEMORY.md

- Ponte so existe para ferramenta que nao le `AGENTS.md` sozinha; conferido contando referencias dentro dos binarios do Grok e do opencode. Promovido.
- Comportamento do `deepseek-v4-flash` com a regra so no bloco. Promovido junto ao perfil dele.

### Pendencias

- Grok segue sem rodada completa: bateu limite do plano free nas tres tentativas, inclusive na ultima de hoje, que consumiu 22.503 tokens antes de a plataforma recusar. Depende de assinatura, entao nao vira tarefa: nenhum agente resolve isso.
- A rodada de regressao do DeepSeek criou o documento ausente com placeholder honesto em vez de perguntar. E n=1 e nao pode ser atribuida a nenhuma mudanca especifica; fica como observacao, nao como conclusao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, e de preferencia o proprio usuario usando o loop numa tarefa real dele.
- Motivo: tres bancadas ja cobriram o que teste sintetico alcanca. O que falta descobrir agora so aparece em uso de verdade, com tarefa que importa e portao que ele mesmo escreveu.

## 2026-09-02 - Claude (fechamento da 2.3.0)

### Objetivo

- Validar o modulo de loop numa segunda bancada antes de publicar, e fechar a versao.

### O Que Foi Feito

- Bancada 2 num subprojeto novo (`durakit`, parser de duracao), com tarefa diferente da primeira para nao pegar carona. Rodada nas tres ferramentas com **a string exata dos perfis gravados em `MEMORY.md`**, no degrau `executar-dificil`.
- Provou o que a bancada 1 nao cobria: que os perfis executam de verdade (eu os tinha escrito de help e catalogo, sem nunca rodar), que `agente=` aparece em evidencia real com a string inteira, e que `exit 4` dispara com agente mal configurado de verdade.
- As tres fecharam com portao verde na tentativa 1 e acertaram todos os casos que as regras determinam, inclusive fora da suite. Um caso extra meu nao era determinado pelas regras e as tres divergiram; reclassificado como ambiguo em vez de contado como falha.
- Publicada: `git push origin main` levou 10 commits (`440919f..6ef1a40`) e `./install.sh` propagou a 2.3.0 para os tres destinos globais. Paridade conferida por `diff -rq`, com o modulo de loop presente e `loop.sh` executavel.
- Spec 0004 fechada com quatro tarefas e mais nove de correcao e validacao surgidas depois da conclusao, todas registradas como DEC-014 a DEC-017.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop.sh`, `scripts/loop_task.py`, `evals/test_loop.py`, `evals/verify_repository.py`, `references/loop.md`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/specs/0004-modulo-de-loop.md`, `.gitignore`.

### Decisoes Tomadas

- DEC-014 a DEC-017 na spec 0004, todas posteriores a conclusao dela: exit 4 para agente que falha sem mexer em nada; `agente=` na evidencia; perfis em `MEMORY.md` com a skill montando a chamada; e nao registrar rodada que falhou, com a nota de que isso e escolha de escopo e nao impedimento.

### Aprendizados Para MEMORY.md

- Gemini CLI nao roda nesta maquina por conta, nao por defeito do modulo. Promovido.
- A evidencia vale o que o portao vale: duas de tres ferramentas, na bancada 1, fecharam tarefa com bug que a suite nao cobria. Promovido como ponteiro para `references/loop.md`, onde o argumento completo esta escrito.

### Pendencias

- Nenhuma acionavel. Backlog zerado, quatro specs `Concluida`, verificador em 33 de 33.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a 2.3.0 esta publicada, instalada e validada por duas bancadas. O que vem agora depende de uso real: o que incomodar na pratica vira a proxima spec.

## 2026-09-02 - Claude (rastreabilidade do agente e chamada assistida)

### Objetivo

- Registrar na evidencia quem fez o trabalho, e tirar do usuario a tarefa de digitar o comando do loop.

### O Que Foi Feito

- Correcao de leitura minha, apontada pelo usuario: os valores em dolar das CLIs sao preco de tabela da API. O JSON do Claude declara `"costBasis": "list"`. Quem usa assinatura nao paga aquilo, entao a tabela de custo da bancada estava mal rotulada. Corrigido na spec 0004, em `references/loop.md` e na entrada de sessao da bancada.
- Confusor da bancada tambem registrado: nenhum modelo foi fixado nas rodadas, entao a comparacao misturava ferramenta, modelo e esforco.
- `agente=<comando>` na evidencia, entre `tipo=` e `procedimento=`. O loop sabe o comando com certeza, porque foi ele que invocou; registrar e fato, nao alegacao, e respeita DEC-001.
- Chamada assistida: o usuario pede em linguagem natural e o agente do chat monta o comando. Os perfis por intencao e ferramenta vivem em `docs/MEMORY.md`, secao `## User`, que ja e o lugar de preferencia de quem toca o projeto. Nenhum arquivo de configuracao novo.
- Perfis de executar ganharam tres degraus (`executar`, `executar-dificil`, `executar-muito-dificil`), com a skill propondo qual encaixa a partir de sinais reais: rodada anterior que falhou, tarefa pertencer a spec, portao ser suite inteira, e o que a tarefa diz. Na duvida, o degrau mais baixo. Sem rubrica com pontuacao: julgamento declarado, com o sinal a vista, para o usuario discordar em uma palavra.
- Bancada 2, a pedido do usuario, antes de decidir publicar. Subprojeto novo e tarefa diferente, para nao pegar carona na anterior. Validou tres coisas que a bancada 1 nao cobria: que os perfis gravados executam mesmo (eu os tinha escrito a partir de help e catalogo, sem nunca rodar), que `agente=` aparece em evidencia real com a string inteira, e que exit 4 dispara com agente mal configurado de verdade.
- As tres ferramentas fecharam na tentativa 1 e acertaram tudo que as regras determinam. Um dos meus casos extras nao era determinado pelas regras e as tres divergiram; reclassifiquei como ambiguo em vez de contar como falha do Grok. Erro de teste meu, e uma ilustracao boa: onde a especificacao cala, modelos divergem.
- O usuario apontou um buraco na regra: o sinal mais forte dela, "a rodada anterior falhou", nao sobrevive ao fim da conversa, porque o loop nao registra fracasso. Ao investigar, apareceu que eu tinha descrito mal o impedimento: registrar fracasso nao feriria DEC-001, ja que exit code de portao vermelho e fato comprovado por comando, tao comprovado quanto sucesso. Nao gravar e escolha de escopo, e o usuario decidiu manter (DEC-017).
- Consequencia obrigatoria dessa escolha: a skill nao pode afirmar "e a primeira rodada", porque nao tem como saber. Ela diz que nao tem registro e deixa o usuario corrigir. Ausencia de registro nao e prova de ausencia de fracasso.
- A regra de escolha de degrau foi recalibrada depois de ser aplicada a tarefas reais: dois dos quatro sinais originais (portao ser suite, tarefa pertencer a spec) disparam em quase todo trabalho de codigo, entao a regra mandaria quase tudo para `executar-dificil` e o degrau base ficaria sem uso. Agora comeca no base e sobe so por sinal declarado, com destaque para o unico que tem evidencia: a rodada anterior ter falhado. A bancada sustenta isso, porque a tarefa mais parruda dela passou de primeira no esforco padrao das tres ferramentas.
- O usuario decidiu que o degrau mais alto do Grok aponta para o teto dele (`xhigh`, o mesmo de `executar-dificil`): ficar sem opcao era pior que repetir. Isso nao fere a regra recem-escrita, porque o problema era rebaixar **em silencio**. A regra ficou com tres casos: usar o teto quando ja decidido e registrado, avisando; perguntar quando nao houver decisao; e nunca escolher parecido calado.
- Escada de esforco do Grok confirmada pelo print e pelas strings do binario: termina em `xhigh` ("Extra High"), sem equivalente a `max`. Em vez de forcar tres degraus onde cabem dois, ficou registrado que o Grok nao tem o mais alto, e entrou regra nova: degrau que nao existe na ferramenta escolhida nao vira degrau parecido em silencio, porque rebaixar calado faz o usuario achar que pediu esforco maximo e recebeu outra coisa.
- Rotulo de interface nao e valor de CLI, e isso so apareceu porque o usuario mandou o print do menu do Codex. "Extra High" e `xhigh`; o menu nao mostra `max`; e `ultra` nao e so mais esforco, e raciocinio maximo **com delegacao automatica**, que abre subagentes. Os perfis pararam em `max` por decisao do usuario: numa rodada nao supervisionada, delegacao multiplica consumo de plano sem aviso.
- Fluxo conversacional para configurar os perfis, a pedido do usuario: perfil que so da para editar na mao envelhece. Ficou em `references/loop.md`, e nao no `SKILL.md`, porque o `SKILL.md` entra em contexto toda vez que a skill dispara. O passo que importa e o terceiro: confirmar o nome do modelo na propria CLI antes de gravar, nunca de memoria.
- Perfis do usuario gravados com strings verificadas, nao inventadas: `claude --help` confirma os aliases `fable`, `opus` e `sonnet` e os niveis de `--effort`; `~/.codex/models_cache.json` confirma `gpt-5.6-sol` e `gpt-5.6-terra`; `~/.codex/config.toml` confirma a chave `model_reasoning_effort`.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop_task.py`, `scripts/loop.sh`, `SKILL.md`, `references/loop.md`, `CHANGELOG.md`, `evals/test_loop.py`.
- Projeto: `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-015: `agente=` na evidencia.
- DEC-016: escolha de modelo fica no usuario, com perfis em `MEMORY.md`, e nunca na linha de tarefa nem dentro da skill.

### Aprendizados Para MEMORY.md

- Perfis de loop e a natureza do custo sob assinatura foram promovidos para `MEMORY.md`, secao `## User`.

### Pendencias

- Nenhuma acionavel. Depois da bancada 2 o usuario autorizou publicar: `git push origin main` levou os 9 commits (`440919f..e9640d3`) e `./install.sh` propagou a 2.3.0 para os tres destinos globais, com paridade conferida por `diff -rq` e o modulo de loop presente (`scripts/loop.sh` executavel, `scripts/loop_task.py`, `references/loop.md` e o partial do bloco).
- As linhas de sessoes anteriores que dizem "os tres destinos continuam na 2.2.0" valiam quando foram escritas e ficam como estao: registro historico nao se reescreve.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: o que faltava responder por teste ja foi respondido. O resto e decisao de publicar.
