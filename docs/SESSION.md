# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas mais antigas foram rotacionadas para `docs/archive/SESSIONS-2026.md`. Este arquivo mantem as 5 mais recentes.

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

## 2026-09-03 - Claude (resposta de T-059)

### Objetivo

- Registrar a resposta do usuario a T-059 e desdobrar em trabalho.

### O Que Foi Feito

- Usuario aceitou item a item a proposta de niveis de REVAL-1 (seis ERRO, dez AVISO, dois so texto). T-059 concluida com a resposta transcrita; decisao formal em `docs/DECISIONS.md`; REVAL-1, REVAL-2 e REVAL-6 fechadas como `resolvido`.
- Trabalho desdobrado por nivel: T-069 (ERRO), T-070 (AVISO), T-071 (texto do core). Os tres exigem versao 2.6.0 e dependem de T-065 para cada codigo novo nascer com fixture.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Em `docs/DECISIONS.md`: promessa do core sem check vira check com nivel declarado, ou texto honesto; codigo novo so entra com fixture.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- T-061 e T-067 seguem aguardando o usuario. Pela regra do bloco specs, T-065, T-069, T-070 e T-071 juntas mudam contrato e passam de tres tarefas: cabem numa spec 0007, se o usuario quiser.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, comecando por T-065 e depois T-069.
- Motivo: sem o manifesto de cobertura, os checks novos nasceriam com o mesmo ponto cego que a revalidacao acabou de achar.

## 2026-09-03 - Claude Fable, com Grok, Codex, Gemini, GPT e Claude Opus (revalidacao adversarial da skill 2.5.1)

### Objetivo

- Atacar a skill inteira, sete superficies, com uma familia de modelo por superficie e outra verificando, e transformar o que sobreviver em conserto ou tarefa.

### O Que Foi Feito

- **Inventario conferido antes de gastar chamada**: `cursor-agent --list-models` nao tinha mais Kimi, GLM nem Gemini 3.8; sobraram quatro familias reais (Grok, GPT/Codex, Claude, Gemini 3.7 Flash). Distribuicao: Grok nas superficies 1 e 6, Codex nas 2, 4 e 7, Gemini na 3, Claude Opus executando a 5 pela skill instalada. Claude Fable selou posicao propria antes de qualquer agente rodar (arquivo em `docs/archive/revalidacao-2026-09-03/`), e verificou no codigo cada achado de outra familia.
- **Isolamento por DEC-003**: worktree descartavel com o corpo das duas entradas abertas de `CONSENSUS.md` retirado e nota dizendo que a omissao era proposital. Nenhum agente reportou a omissao como defeito.
- **Sete entradas de achado**, REVAL-1 a REVAL-7, em `docs/CONSENSUS.md` (REVAL-5 ja rotacionada por tamanho). Itens confirmados no codigo, contados por entrada: 10 no contrato do core (REVAL-1), 12 no validador (REVAL-2), 11 no loop (REVAL-3), 16 mutacoes cegas mais 3 efeitos colaterais no portao (REVAL-4), 8 nos templates (REVAL-6) e 10 na distribuicao (REVAL-7); nenhum ficou como "nao confirmado".
- **Superficie 4 por mutacao, 24 rodadas**, cada uma revertida de backup por `cp` e conferida por SHA-256: 16 passaram verde cegas, 8 pegaram. Codex, somente leitura, previu as cegas antes de ver o resultado e acertou todas as que os dois cobriram; a tabela dele mostra 10 de 39 codigos com fixture que os produza.
- **Consertos aplicados sem bump** (T-068): verificador sem `__pycache__` na fonte, piso de 58 na bateria do loop, `install.sh` sem bytecode e com `--all` no cabecalho, `evals.json` em 2.5.1, README da skill com instalacao manual completa.
- **Superficie 5 executada de verdade**, quatro fluxos pelo `claude -p` contra `~/.claude/skills`: scaffold, atualizacao de v1, spec com "Avançar" e ativacao de loop recusada. Nenhum defeito de fluxo.
- **Codex morreu na cota** do plano na superficie 7 depois de 312 mil tokens; refeita com GPT-5.6 via `cursor-agent`, que confirmou os mesmos itens. O usuario pediu no meio da sessao para nao gastar mais Codex nem GPT sol: nenhuma chamada foi feita depois disso.
- Rotacao de `CONSENSUS.md`: as rodadas de P-7/P-8 e P-9 (ainda `aberto`, T-053) foram para o archive por tamanho, com nota e ponteiros na spec 0006.

### Arquivos Criados Ou Alterados

- Skill (nao distribuidos): `evals/verify_repository.py`, `evals/test_loop.py`, `evals/evals.json`, `install.sh`, `README.md`.
- Projeto: `docs/CONSENSUS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/MEMORY.md`, `docs/CHANGELOG.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/` (27 arquivos de material bruto, travessoes trocados por hifen e contados).

### Decisoes Tomadas

- Nenhuma de contrato. As calibragens estao em T-059, T-061 e T-067, em "Aguardando Usuario". Proposta de decisao registrada em REVAL-4: codigo de diagnostico sem fixture que o produza nao entra em `CODIGOS`.

### Aprendizados Para MEMORY.md

- Mutacao vale para portao **antigo**, nao so novo: os 44 de 44 escondiam seis checks inteiros que podiam sumir sem um FALHA.
- Tres sessoes de Codex `xhigh` em paralelo estouram a cota do plano em uma hora; GPT-5.6 via `cursor-agent` e o fallback da mesma familia. O usuario pediu `terra` para teste daqui em diante.

### Pendencias

- T-059, T-061, T-067 aguardam o usuario. T-060, T-062, T-063, T-064, T-065 abertas, alem de T-053 a T-058 que continuam validas (confirmadas pelas quatro familias).
- Achado mais caro: o portao dos evals (REVAL-4). Escapou porque o total de verificacoes e dinamico e nunca foi comparado com nada, e fixture so nascia junto com check novo.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario para T-059 (uma resposta destrava REVAL-1, 2 e 6); qualquer agente para T-065, que nao depende de decisao e e o que impede a proxima regressao silenciosa.
- Motivo: enquanto 29 dos 39 codigos nao tiverem fixture, qualquer conserto de T-060 a T-064 pode regredir sem o portao acusar.

## 2026-09-03 - Claude (T-057 e o prompt de revalidacao)

### Objetivo

- Consertar a escrita nao atomica de `TASKS.md`, e deixar pronto um prompt para uma sessao nova revalidar a skill inteira em varios modelos.

### O Que Foi Feito

- **T-057, o unico defeito aberto que podia destruir dado.** `loop_task.py` gravava `docs/TASKS.md` com `write_text` direto, que trunca antes de escrever. Agora e temporario no mesmo diretorio, `fsync`, e `os.replace`, com o temporario removido se falhar antes do rename. O pior caso passou a ser um orfao ao lado do arquivo.
- **Provado por mutacao, e nao por leitura.** Teste novo em `test_loop.py` quebra `os.fsync` de proposito no meio da escrita e confere que o arquivo original sobreviveu inteiro. Revertendo `escrever` para o comportamento antigo, o teste acusa: "TASKS.md intacto depois de escrita interrompida" falha e o arquivo trunca. Bateria de 55 para 58.
- Versao para **2.5.1**, porque `loop_task.py` e distribuido. Marcadores dos tres blocos subiram juntos por DEC-009, com o bloco core inalterado.
- A regra subiu para `docs/DECISIONS.md`, porque vale alem desta spec: arquivo de memoria do projeto se escreve por substituicao atomica, nunca por escrita direta.
- **Prompt de revalidacao escrito em `docs/PROMPTS.md`**, que e o lugar dele nesta estrutura, e nao um arquivo solto. Ele distribui cinco superficies (contrato do bloco core, validador, modulo de loop, portao dos evals, fluxos de scaffold) entre familias de modelo diferentes, em vez de fazer a mesma pergunta a todos, que so produz cinco versoes do mesmo vies.
- O prompt carrega o inventario de modelos conferido hoje, a lista do que **nao** deve ser redescoberto, e as onze restricoes que ja custaram tempo nesta sessao, incluindo as duas que me morderam: `git checkout` em arquivo com trabalho nao commitado, e `index()` casando com o modelo cercado no topo do `CONSENSUS.md`.
- A pedido do usuario, que quis a validacao da skill **inteira**, o prompt passou de cinco para **sete superficies**: faltavam os templates de `assets/`, que sao o que o usuario final recebe, e a distribuicao (`install.sh`, `agents/openai.yaml`, `README.md` e `CHANGELOG.md` da skill). Entrou tambem um **inventario de cobertura** arquivo a arquivo, para "toda a skill" ser conferivel em vez de afirmada, com a regra de que omissao declarada e aceitavel e omissao silenciosa nao.
- Reinstalacao feita **antes** da revalidacao, e nao por higiene: a superficie 5 roda contra a copia instalada, entao com os destinos em 2.5.0 a sessao nova acharia a T-057 de novo como achado novo, e criaria projeto com marcador divergente da fonte.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop_task.py`, `evals/test_loop.py`, `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/PROMPTS.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Em `docs/DECISIONS.md`: arquivo de memoria do projeto se escreve por substituicao atomica. Vale para o `loop_task.py` ja publicado e para o orquestrador da spec 0006.

### Aprendizados Para MEMORY.md

- Nenhum novo. A licao de mutacao ja esta promovida, e esta sessao so a aplicou mais uma vez.

### Pendencias

- T-053 (tres calibragens da spec 0006 e a pergunta de segredo no bruto), T-054, T-055, T-056 e T-058 seguem abertas.
- Nenhuma. A 2.5.1 foi instalada nos tres destinos, com paridade conferida e o `os.replace` presente nos tres.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): sessao nova rodando o prompt de revalidacao de `docs/PROMPTS.md`.
- Motivo: sete defeitos reais sairam de tres rodadas de consenso feitas de improviso. O prompt existe para fazer isso de proposito, com distribuicao por familia de modelo em vez de repetir a mesma pergunta.

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
