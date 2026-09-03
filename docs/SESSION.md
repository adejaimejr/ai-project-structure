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

## 2026-09-02 - Claude, Codex e Grok (bancada multi-ferramenta do loop)

### Objetivo

- Rodar o modulo de loop com varias ferramentas num subprojeto real, medir custo e descobrir o que quebra fora do teste com agente falso.

### O Que Foi Feito

- Subprojeto `slugkit` montado quatro vezes, identico: portao real (`python3 test_slugify.py`) falhando no inicio, T-001 bem especificada e T-002 deliberadamente sem contexto.
- T-001: Claude, Codex e Grok fecharam com portao verde na tentativa 1. Gemini nao rodou, por `IneligibleTierError` da conta, nao por defeito do modulo.
- T-002 foi o teste que importava: chutar o limite padrao passaria no portao, porque a suite nao cobre isso. Os tres escreveram `.loop-pergunta` e pararam. O bloco de loop no `AGENTS.md` segurou a regra "Nunca Inferir" sob incentivo contrario.
- Consumo: Claude 295k de cache read na primeira tarefa e 233k na segunda; Grok 193k e 155k tokens; Codex 23.958 e 16.817 tokens. Os valores em dolar que as CLIs imprimem sao preco de tabela da API (`costBasis: list` no Claude), nao o que se paga em assinatura: servem para comparar rodadas, nao para prever fatura.
- Dois defeitos achados e corrigidos: o loop insistia com agente que nunca executou (virou exit 4, com teste novo), e as flags por ferramenta nao estavam documentadas (viraram tabela em `references/loop.md`).
- Duas das tres implementacoes de T-001 tinham bug numa regra de borda que a suite nao cobria, e o loop fechou as duas com evidencia legitima. Registrado como limitacao central do desenho: a evidencia vale o que o portao vale.

### Arquivos Criados Ou Alterados

- `scripts/loop.sh` (exit 4), `evals/test_loop.py` (53 verificacoes), `references/loop.md`, `CHANGELOG.md` da skill.
- `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-014 na spec 0004: agente que falha sem mexer em arquivo encerra a rodada em vez de gastar tentativa. Decisao de implementacao posterior a conclusao da spec, registrada la com o motivo.

### Aprendizados Para MEMORY.md

- Portao fraco automatizado continua fraco, so que mais rapido. Duas ferramentas passaram no portao com bug de borda. Ficou em `references/loop.md`, que e onde quem for declarar `(verifica:)` vai ler; nao promovido para `MEMORY.md` por ser regra da skill e nao deste repositorio.

### Pendencias

- Os tres destinos globais continuam na 2.2.0: a skill nao foi reinstalada depois da 2.3.0.
- Decisao de publicar ou nao a 2.3.0 esta com o usuario.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: a bancada respondeu o que dava para responder por teste. O que falta e decisao: publicar, e se o custo por tarefa faz sentido para o uso que voce pretende.

## 2026-09-02 - Claude + Codex (skill 2.3.0, modulo de loop)

### Objetivo

- Implementar a spec 0004 inteira: o modulo de loop, que faz a estrutura executar uma tarefa verificavel em vez de so descreve-la.

### O Que Foi Feito

- T-019: bloco de loop, `references/loop.md`, secao de ativacao no `SKILL.md` com o portao de `QUALITY.md`, marcadores dos tres blocos em v2.3.0, e o fluxo de atualizacao ensinado a tratar o bloco novo sem nunca oferecer a ativacao.
- T-020: `loop.sh` orquestra, `loop_task.py` faz toda edicao de `TASKS.md` reusando o parser do validador. Falta de contexto e sinalizada por arquivo, nao por linha no stdout (DEC-011 e DEC-012, decididas pelo usuario antes da implementacao).
- T-021 e T-022: a bateria do loop saiu do scratchpad e virou `evals/test_loop.py`, com 47 verificacoes e agente falso. O verificador foi de 26 para 33 checagens e passou a rodar a bateria por dentro, alem de conferir o bloco `loop`, o bit de execucao e se os tres scripts distribuidos compilam.
- T-023: modulo ativado neste repositorio e rodada real com o Codex na T-025, uma tarefa pequena e honesta (`.loop-pergunta` no `.gitignore`) cujo portao falhava de proposito antes e passou depois.
- Na rodada real, o Codex declarou por conta propria que nao alterou `TASKS.md` nem escreveu evidencia. E a regra do bloco sendo obedecida por um modelo que nao participou desta implementacao, que era a duvida que sobrava.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `references/loop.md` (novo), `references/atualizacao.md`, `assets/partials/AGENTS-loop-block.md` (novo), `assets/AGENTS.md`, `scripts/loop.sh` (novo), `scripts/loop_task.py` (novo), `evals/test_loop.py` (novo), `evals/verify_repository.py`.
- Projeto: `AGENTS.md` (bloco de loop ativado), `.gitignore` (pelo proprio loop), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-011 e DEC-012 da spec 0004, do usuario: sinal por arquivo e helper em Python reusando o parser do validador.
- DEC-013, minha: formato do campo `resultado`, com corte pelo comeco e truncagem declarada.

### Aprendizados Para MEMORY.md

- Nenhum. As decisoes ficaram na spec e em `DECISIONS.md`.

### Pendencias

- A skill nao foi reinstalada nos tres destinos globais: eles continuam na 2.2.0, sem o modulo de loop.
- A rodada real usou uma ferramenta so. O `--agente` e neutro por construcao, mas `claude -p` e `gemini -p` nao foram exercitados.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a 2.3.0 esta fechada e verificada. O que sobra e propagacao (reinstalar) e uso real, que so o tempo mostra.

## 2026-09-02 - Claude (spec 0004 definida)

### Objetivo

- Levar o usuario pelas oito perguntas abertas da spec 0004 e fechar o escopo da 2.3.0.

### O Que Foi Feito

- As oito perguntas foram decididas uma a uma, em ordem de dependencia: P-4 primeiro, porque a resposta dela restringia P-2 e P-6.
- O escopo encolheu de G para M. Foram cortados worktree, notificacao de sistema, teto de custo e automacao de consenso, tres deles porque outra decisao ja resolvia o problema por construcao.
- Spec 0004 passou para `Definida` com DEC-001 a DEC-009 e "Perguntas Abertas" vazia. Criterios de aceite de comportamento agora existem, porque ha o que cobrar: sao verificaveis com um agente falso, sem gastar chamada de modelo.
- DEC-001 e DEC-006 foram copiadas para `docs/DECISIONS.md`: juntas, definem a fronteira entre o que a maquina pode afirmar e o que so a pessoa pode afirmar nos arquivos de memoria, o que vale para qualquer automacao futura.
- T-019 a T-023 abertas. T-018 concluida.

### Arquivos Criados Ou Alterados

- `docs/specs/0004-modulo-de-loop.md`, `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- DEC-001 a DEC-008 da spec 0004, todas do usuario. DEC-009 e decisao de implementacao minha, sobre versionar os tres marcadores juntos; e a unica que nao veio de pergunta e a que mais merece revisao.

### Aprendizados Para MEMORY.md

- Nenhum. As decisoes ficaram em `DECISIONS.md`, que e o lugar delas.

### Pendencias

- Nenhuma acionavel. T-019 a T-023 estao em "Proximas Tarefas".

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente.
- Motivo: comecar por T-019, porque T-020 depende do bloco e do fluxo de ativacao existirem. T-022 pede um agente falso, entao da para testar o `loop.sh` inteiro sem gastar chamada de modelo.

## 2026-09-02 - Claude (publicacao da 2.2.0 e abertura da spec 0004)

### Objetivo

- Publicar a 2.2.0 no GitHub e abrir a spec do modulo de loop, cujo pre-requisito passou a existir hoje.

### O Que Foi Feito

- `git push origin main`: os 5 commits da 2.2.0 sairam do laptop (`7040e4d..c5d8488`).
- Spec `0004-modulo-de-loop` criada como `Rascunho`. Ela separa o que ja esta decidido (DEC-001, DEC-003 e DEC-005, herdadas da 0003) do que depende de resposta do usuario.
- O pre-requisito que DEC-005 mandou para o modulo de loop, "secao Testes E Validacao de `QUALITY.md` com comando real", passou a ser satisfeito por este repositorio hoje, com `verify_repository.py`. E o que destrava a discussao do loop sem contrariar DEC-003.
- Nenhuma tarefa de implementacao aberta: com oito perguntas em aberto, abrir tarefa seria comprar escopo que ainda nao existe.

### Arquivos Criados Ou Alterados

- `docs/specs/0004-modulo-de-loop.md` (novo), `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. A spec 0004 registra tres decisoes herdadas e nenhuma propria, de proposito: decidir agora seria decidir sem as respostas.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- T-018 em `## Aguardando Usuario`: as oito perguntas da spec 0004. Primeiro uso real da secao neste repositorio, o que tambem exercita a convencao contra um caso que nao foi construido para testa-la.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, nao um agente.
- Motivo: a spec so anda com as respostas de P-1 a P-8. P-3, P-4 e P-8 mudam o escopo o suficiente para que qualquer implementacao antes delas seja retrabalho.

