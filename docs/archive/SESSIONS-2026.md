# SESSIONS 2026

Entradas antigas de `docs/SESSION.md`, rotacionadas em 2026-09-02 pela regra de "Rotacao De Arquivos" do `AGENTS.md`.

Cobre de 2026-04-25 (criacao da estrutura multiagente e validacao por tri-consenso) a 2026-09-03 (skill 2.4.0 e 2.5.0, com o formato de achado, o diagnostico com identidade estavel e as fixtures que os provaram). Ordem cronologica inversa, igual a do arquivo principal. Rotacionado tres vezes em 2026-09-03.

<!-- Rotacionadas em 2026-09-04, terceira vez: as duas entradas abaixo (T-065 pelo loop, e T-069 com a 2.6.0) vieram de docs/SESSION.md por tamanho. -->

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

<!-- Rotacionadas em 2026-09-04, segunda vez: as duas entradas de 2026-09-03 abaixo (respostas de T-059/T-061/T-067, e a revalidacao adversarial da 2.5.1) vieram de docs/SESSION.md por tamanho. -->

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

<!-- Rotacionadas em 2026-09-04: as duas entradas de 2026-09-03 abaixo (rodada 1 cega da spec 0006 e a ratificacao das seis perguntas) vieram de docs/SESSION.md por tamanho. -->

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

## 2026-09-02 - Claude + Codex (evals 1, 2, 5, 6 e 9 no Codex CLI)

### Objetivo

- Rodar em outra ferramenta os cinco evals que dependem de julgamento de comportamento, para tirar do julgamento o modelo que escreveu os templates.

### O Que Foi Feito

- Codex CLI nao estava instalado nesta maquina. Instalado a pedido do usuario (`npm i -g @openai/codex`, versao 0.152.1, autenticado via ChatGPT). A skill 2.2.0 apareceu na lista de skills do Codex, vinda de `~/.agents/skills/`.
- Cinco rodadas de `codex exec` em diretorios descartaveis fora do repositorio, com os prompts literais de `evals.json`. Conferencia feita por script proprio, lendo o diretorio produzido em vez do relato do agente.
- 5 de 5 aprovados. Um modelo sem nenhum contexto desta implementacao preencheu a data de adocao com a data do dia nas tres estruturas novas, manteve a secao `Aguardando Usuario` e, no eval 6, afirmou espontaneamente que a tarefa historica concluida fica sem evidencia porque a regra nao e retroativa.
- Isso valida na pratica o passo 5b do `SKILL.md` e o passo 7b de `references/atualizacao.md`, ambos escritos hoje, e a nao retroatividade de DEC-008 e DEC-011.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`, `docs/SESSION.md`. Nenhum arquivo da skill precisou mudar.

### Decisoes Tomadas

- Nenhuma.

### Aprendizados Para MEMORY.md

- Nenhum promovido. A observacao do eval 2 (o modelo inverteu qual opcao de specs e a recomendada) e desvio de fidelidade de um modelo, nao regra do projeto, e nao esta entre os criterios que aquele eval cobra.

### Pendencias

- Nenhuma acionavel. Fora dos criterios cobrados, duas observacoes: no eval 2 o Codex marcou "Sim (recomendado)" para o modulo de specs, e o `SKILL.md` recomenda "Nao"; e a resposta de chat do eval 9 usou um travessao, caractere proibido nos textos do projeto, sendo que a fixture usa um `AGENTS.md` reduzido que nao carrega essa regra.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a spec 0003 esta fechada e agora tambem validada por ferramenta e modelo diferentes. O backlog volta ao normal.

## 2026-09-02 - Claude (T-014, criterios sem runner)

### Objetivo

- Exercitar na mao os tres criterios de aceite da spec 0003 que nao tem runner: scaffold minimal, scaffold completa e atualizacao de um projeto 2.1.0.

### O Que Foi Feito

- Skill invocada da instalacao real, nao da fonte do repositorio, em tres projetos descartaveis fora do repositorio. Isso tambem testou que a instalacao de ontem esta usavel.
- Scaffold minimal e scaffold completa com o modulo de specs: `--strict` exit 0 nos dois, marcadores em v2.2.0, data de adocao preenchida, sem git, sem `partials/` copiado.
- Projeto 2.1.0 sintetizado com os templates daquela versao tirados do git, com dados de usuario reais (tarefas concluidas sem evidencia, tarefa parada esperando resposta, consenso antigo, regras locais) e atualizado pelo fluxo de `references/atualizacao.md`.
- O projeto 2.1.0 validou limpo **antes** da atualizacao, sob o validador 2.2.0. E a prova pratica de DEC-011: sem o marcador de corte, a cobranca nao existe.
- Depois da atualizacao, a regra foi testada nos dois sentidos: tarefa concluida hoje sem evidencia gerou AVISO, as concluidas em agosto continuaram silenciosas, e o AVISO sumiu quando a evidencia entrou.
- Quatro defeitos achados. Tres eram texto (T-015). O quarto era codigo e apareceu quando o proprio `TASKS.md` deste repositorio ficou com uma tarefa citando outra: o validador contava qualquer `T-NNN` da linha como ID e acusava duplicidade. Corrigido em T-016, com guarda na fixture.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/SKILL.md`, `docs/skills/ai-project-structure/references/atualizacao.md` (correcoes de T-015).
- `docs/skills/ai-project-structure/scripts/validate_structure.py`, `docs/skills/ai-project-structure/evals/fixtures/aguardando-project/` e `docs/skills/ai-project-structure/CHANGELOG.md` (correcao de T-016).
- `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma decisao nova. Tres achados eram defeito de texto e um era defeito de codigo; nenhum tocou o desenho da 2.2.0.

### Aprendizados Para MEMORY.md

- Dogfood pega o que teste sintetico nao pega: o bug de ID so apareceu porque uma tarefa real precisou citar outra. Nao promovido para `MEMORY.md` por ser generico demais para virar regra acionavel.

### Pendencias

- Nenhuma acionavel. As correcoes de T-015 e T-016 foram propagadas para os tres destinos globais a pedido do usuario, com paridade conferida por `diff -rq`.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): outra ferramenta (Codex CLI ou Gemini CLI).
- Motivo: T-014 rodou no Claude Code, e quem escreveu os templates julgou o proprio trabalho. Os evals 1, 2, 5, 6 e 9 continuam valendo mais quando rodados por outro modelo, sem este contexto.

## 2026-09-02 - Claude (implementacao da skill 2.2.0)

### Objetivo

- Implementar a skill 2.2.0 conforme a spec 0003: evidencia de fechamento em tarefa concluida, secao `Aguardando Usuario`, campos declarativos de consenso e verificador de integridade do meta-projeto.

### O Que Foi Feito

- T-009: bloco core em v2.2.0 com a secao nova "Evidencia De Fechamento", o destino da pergunta que trava tarefa dentro de "Nunca Inferir" e a subsecao "Independencia Declarada" no consenso. Bloco propagado para a raiz por script e conferido byte a byte. Templates de `TASKS.md` (secao `Aguardando Usuario`, sub-linha de evidencia, marcadores novos) e de `CONSENSUS.md` (tres campos declarativos) atualizados.
- T-010: checks novos no validador, provados por uma matriz de 17 casos em projeto descartavel, um por regra e um por caso que deve ficar silencioso. A severidade que estava em aberto foi decidida: AVISO, com o motivo registrado em DEC-010.
- Descoberta na implementacao de T-010: a nao retroatividade de DEC-008 nao se sustenta sem um corte declarado por projeto, porque as 15 linhas historicas deste repositorio derrubariam o `--strict` que a propria spec exige. Criado o marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` em `TASKS.md`, que governa a evidencia e tambem os campos de consenso (DEC-011).
- T-011: `evals/verify_repository.py` com 26 checagens, e os 4 headings ausentes de `SESSION.md` corrigidos com nota honesta, sem promover nada retroativamente para `MEMORY.md`.
- T-013 antecipada: `SESSION.md` e `CONSENSUS.md` rotacionados para `docs/archive/`. Veio antes porque o aviso de rotacao reprovava o `--strict` declarado por T-010 e T-011; fechar as duas antes disso teria sido fechar tarefa com o proprio check falhando.
- T-012: fixture `aguardando-project` (caso valido e caso invalido), eval 9, versao 2.2.0 no `SKILL.md` com o passo 5b de preencher a data de adocao, passo 7b em `references/atualizacao.md`, CHANGELOGs, comando de integridade em `QUALITY.md` e reinstalacao nos tres destinos globais.
- O verificador pegou dois problemas reais durante a propria construcao: `SKILL.md` ainda em 2.1.0 com os marcadores em 2.2.0, e ele mesmo carregando um travessao literal no codigo do check de travessao.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `scripts/validate_structure.py`, `evals/verify_repository.py` (novo), `evals/evals.json`, `evals/fixtures/aguardando-project/` (nova), `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/docs/TASKS.md`, `assets/docs/CONSENSUS.md`, `references/atualizacao.md`.
- Projeto: `AGENTS.md` (raiz), `docs/TASKS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/QUALITY.md`, `docs/CHANGELOG.md`, `docs/specs/0003-tasks-verificaveis.md`, `docs/archive/README.md`, `docs/archive/SESSIONS-2026.md` (novo), `docs/archive/CONSENSUS-2026.md` (novo).
- Instalacoes: tres destinos globais reinstalados a pedido do usuario, com paridade conferida.

### Decisoes Tomadas

- DEC-010: evidencia ausente sem `(verifica:)` declarado gera AVISO, nao ERRO.
- DEC-011: a nao retroatividade depende de um corte declarado por projeto, no marcador `(convencoes-2-2-0-desde:)` de `TASKS.md`, que governa tambem os campos declarativos de consenso.
- Ambas em `docs/DECISIONS.md`, entrada de 2026-09-02, e na spec 0003.

### Aprendizados Para MEMORY.md

- Verificador que procura um caractere proibido precisa escrever esse caractere escapado no proprio codigo, senao ele se acusa. Promovido para `MEMORY.md`.

### Pendencias

- Os tres criterios de aceite da spec 0003 sem runner (scaffold minimal, scaffold completa e atualizacao de um projeto 2.1.0) continuam julgados na mao e nao foram exercitados nesta sessao. Viraram T-014 em `TASKS.md`.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente, de preferencia em ferramenta diferente da que implementou.
- Motivo: T-014 e justamente rodar o fluxo da skill de fora, como usuario. Quem escreveu os templates e o pior juiz de saber se eles funcionam sem contexto.

## 2026-09-02 - Claude + Codex (planejamento da skill 2.2.0)

### Objetivo

- Avaliar tecnicamente se faz sentido adicionar um loop autonomo a este projeto e, se nao fizer agora, extrair da analise as melhorias que valem sem depender dele.

### O Que Foi Feito

- Parecer tecnico sobre loop autonomo, com leitura do repositorio e conferencia da documentacao atual de `/goal`, hooks e modo headless do Claude Code e do Codex CLI. Conclusao: o portao de verificacao nao pode existir no dia zero de um projeto scaffoldado, entao o loop fica como modulo opcional futuro, nunca no scaffold.
- Da analise saiu o PRD da skill 2.2.0, escrito como spec em `Rascunho`: evidencia obrigatoria em tarefa concluida, secao para tarefa esperando resposta do usuario, consenso com independencia declarada e verificador de integridade do meta-projeto.
- Validacao do PRD por modelo distinto no Codex CLI, em duas rodadas: rodada 1 cega (proibida a leitura da spec) e rodada 2 adversarial com a spec a vista. Primeiro uso real da regra de rodada cega que a propria spec propoe.
- O Codex encontrou dois erros reais: `scripts/check.sh` na raiz violava a regra de raiz minima, e o caminho do validador citado na spec estava errado. Ambos confirmados no repositorio.
- Codex tambem reverteu a decisao mais fraca do PRD (verificacao inteiramente opcional) e propos campos declarativos de consenso, que consertam o problema original melhor que a versao anterior.
- Debate registrado em `CONSENSUS.md` e fechado como `resolvido` apos o usuario decidir os dois residuos (nome da secao de espera e retroatividade da evidencia).
- Spec 0003 promovida de `Rascunho` para `Definida` com nove decisoes e criterios de aceite separados entre verificaveis por comando e julgados na mao.
- Tarefas T-009 a T-013 abertas em `TASKS.md`.

### Arquivos Criados Ou Alterados

- `docs/specs/0003-tasks-verificaveis.md` (criado; `Rascunho` e depois `Definida`).
- `docs/CONSENSUS.md` (entrada de 2026-09-02, fechada como `resolvido`).
- `docs/DECISIONS.md` (entrada de 2026-09-02).
- `docs/TASKS.md` (T-009 a T-013 em "Proximas Tarefas").
- `docs/MEMORY.md` (aprendizado sobre o que o `install.sh` distribui).
- `docs/SESSION.md` (esta entrada).

### Decisoes Tomadas

- Loop autonomo fora da 2.2.0 e fora do scaffold; vira modulo opcional futuro, ativavel so em projeto com comando real em `QUALITY.md`.
- Evidencia de fechamento obrigatoria em tarefa concluida a partir da 2.2.0, nao retroativa; `(verifica:)` continua opcional.
- Secao `## Aguardando Usuario` em vez de `## Bloqueadas`; secao para bloqueio nao humano so quando houver caso real.
- Verificador de integridade em `evals/`, nunca em `scripts/` na raiz.
- Registro completo em `docs/DECISIONS.md`, entrada de 2026-09-02.

### Aprendizados Para MEMORY.md

- `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` existem apenas na fonte canonica da skill e nao sao distribuidos pelo `install.sh`. Determina onde colocar ferramenta que deve ficar so no repositorio. Promovido para `MEMORY.md`.

### Pendencias

- Severidade da evidencia ausente em tarefa concluida que nao declarou `(verifica:)`: a spec define AVISO, o Codex pediu apenas "obrigatoria" sem nomear severidade. Decidir ao implementar T-010.
- `CONSENSUS.md` passou de 30KB e o validador ja avisa (T-013).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente; a spec 0003 e autossuficiente.
- Motivo: comecar por T-009 (bloco core e templates), porque T-010, T-011 e T-012 dependem das convencoes estarem escritas.

## 2026-08-20 - Claude (skill 2.1.0)

### Objetivo

- Implementar a skill 2.1.0 com duas features aprovadas pelo usuario: template opcional `STACK.md` (mapa de stack com documentacao oficial) e flag `--progress` no validador (projecao de tarefas e specs).

### O Que Foi Feito

- Criado `assets/docs/STACK.md`: tecnologias, pacotes principais, "Onde Consultar Primeiro" e notas de compatibilidade, para o agente consultar a fonte certa antes de mexer na stack.
- Bloco core do `AGENTS.md` atualizado (v2.1.0): STACK.md em "Onde Escrever Cada Coisa" e gatilho novo de atualizacao; marcador do bloco specs tambem em v2.1.0.
- `validate_structure.py --progress`: contagem de tarefas por secao e, por spec, status + tarefas concluidas/total + perguntas abertas. Somente-leitura por regra (DEC-003 da spec 0002).
- `SKILL.md` para versao 2.1.0; STACK.md incluido no nivel "completa"; evals atualizados (eval 2 com STACK, eval 8 novo de progresso).
- Dogfood: `docs/STACK.md` do meta-projeto preenchido; bloco core da raiz atualizado preservando o restante do arquivo; spec `0002-stack-e-progresso` criada, executada e concluida com evidencia; tarefas T-005 a T-007 registradas e concluidas.
- Skill reinstalada; paridade dos tres destinos conferida; bateria completa aprovada (scaffold completa com STACK exit 0, meta-projeto exit 0, fixtures conforme esperado, zero travessao).
- Decisoes de escopo confirmadas com o usuario: pipeline SDD completo, coverage math, attestation e CLI continuam fora; validacao de stack (rodar testes por framework) fica fora, com comandos do projeto em `QUALITY.md`.
- Projeto publicado no GitHub a pedido do usuario: repositorio publico `adejaimejr/ai-project-structure`, branch `main`, primeiro commit com o estado da skill 2.1.0; `.gitignore` criado (`.DS_Store`, `__pycache__/`).
- Adicionados `README.md` e `LICENSE` (MIT) na raiz a pedido do usuario, com a excecao de raiz minima registrada em "Regras Do Projeto" do `AGENTS.md`.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `evals/evals.json`, `scripts/validate_structure.py`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/docs/STACK.md` (novo), `assets/docs/README.md`.
- Projeto: `AGENTS.md` (raiz), `docs/STACK.md` (novo), `docs/specs/0002-stack-e-progresso.md` (novo), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.
- Instalacoes: tres destinos reinstalados (fora do projeto).

### Decisoes Tomadas

- Ver DEC-001 a DEC-003 na spec `0002-stack-e-progresso` (validacao de stack fora; progresso como flag do validador; projecao somente-leitura).

### Aprendizados Para MEMORY.md

- Nenhum novo (regras ja registradas).

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: 2.1.0 fechada; proximos passos dependem de uso real ou de novas ideias do backlog.

## 2026-08-20 - Claude

### Objetivo

- Fechar duas inconsistencias documentais que apareceram quando os resultados das tres ferramentas foram reunidos.

### O Que Foi Feito

- Diagnosticada a divergencia do eval 4 entre ferramentas: o Codex parou na entrevista e viu exit 1 por diretorio vazio; o Claude Code respondeu a entrevista e viu exit 0. Nenhum dos dois errou. O `expected_output` do eval 4 so descrevia o que acontece antes das respostas e nao dizia o que esperar do validador depois, entao o passo 4 do roteiro de execucao ficava sem criterio.
- Corrigido o `expected_output` do eval 4 em `docs/skills/ai-project-structure/evals/evals.json`: explicita que o criterio do eval e o comportamento da entrevista, que exit 1 em diretorio vazio e o resultado correto daquele ramo e nao reprova, e como exercitar o ramo "Avançar" ate exit 0. JSON revalidado.
- Confirmado que `install.sh` copia apenas `SKILL.md`, `assets/`, `agents/`, `scripts/` e `references/`. Como `evals/` nao e propagado, a correcao nao exigiu reinstalacao nas tres ferramentas.
- Consolidada a secao "Evidencia De Conclusao" da spec `0001-skill-v2`, que tinha ficado auto-contraditoria: linhas antigas ainda diziam "falta repetir no Codex CLI" ao lado das linhas que registravam o Codex concluido. Agora ha um bloco por tarefa e por ferramenta, com o resumo de 21 execucoes aprovadas no topo.
- Registrado o fechamento da validacao em `docs/CHANGELOG.md` do projeto e no CHANGELOG proprio da skill.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/evals/evals.json`
- `docs/skills/ai-project-structure/CHANGELOG.md`
- `docs/specs/0001-skill-v2.md`
- `docs/CHANGELOG.md`
- `docs/SESSION.md` (esta entrada)

### Decisoes Tomadas

- Nao versionar a skill para 2.0.1 por esta correcao: ela toca apenas `evals/`, que nao e material instalado, e nao muda comportamento algum da skill.
- Manter os dois vereditos do eval 4 como validos em vez de escolher um e refazer a rodada da outra ferramenta: o defeito estava na definicao do eval, nao nas execucoes.

### Aprendizados Para MEMORY.md

- Eval cujo criterio e "nao criar nada" precisa dizer explicitamente o que esperar dos passos seguintes do roteiro, senao cada ferramenta interpreta o silencio de um jeito e os resultados ficam incomparaveis.

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a skill v2.0.0 esta validada nas tres ferramentas e a documentacao esta coerente; a proxima acao depende do que o usuario quiser construir em cima.

## 2026-08-20 - Codex

### Objetivo

- Executar a parte Codex CLI da T-002: os 7 evals da skill ai-project-structure v2.

### O Que Foi Feito

- Usada a copia instalada em `~/.agents/skills/ai-project-structure`; a comparacao com a fonte canonica mostrou apenas arquivos que o instalador nao propaga por design.
- Executados os 7 evals em subdiretorios limpos sob `/tmp/skill-v2-tests-codex/`, sem inicializar git. Resultado: 7 de 7 aprovados.
- O validador retornou exit 0 nos evals 1, 2, 3, 5 e 6. No eval 4, nao foi criado nenhum arquivo, como exige a entrevista antes do scaffold; consequentemente, o validador retornou exit 1 por arquivos ausentes. No eval 7, retornou exit 1 com exatamente os 2 erros esperados: ID `T-001` duplicado e Status `Fazendo` invalido.
- No eval 6, o plano e o diff da atualizacao v1 para v2 foram apresentados sem alterar a copia, pois faltava confirmacao por item. As duas fixtures ficaram intactas, com hashes iguais antes e depois.
- Durante esta rodada, o Gemini CLI tambem concluiu os 7 evals. Com as tres ferramentas aprovadas, T-002 foi movida para Concluidas e a spec 0001 foi marcada como Concluida.
- Rodado o validador no repositorio: exit 0, com 4 avisos historicos conhecidos em entradas de 2026-04-25.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests-codex/` (artefatos temporarios dos 7 evals, preservados).

### Decisoes Tomadas

- Considerar o eval 4 aprovado pelo comportamento exigido, mesmo com o exit 1 esperado do validador sobre um diretorio vazio.
- Concluir T-002 e a spec 0001, pois Claude Code, Codex CLI e Gemini CLI aprovaram os 7 cenarios.

### Aprendizados Para MEMORY.md

- Nenhum. O resultado e especifico desta rodada de validacao.

### Pendencias

- Os artefatos em `/tmp/skill-v2-tests-codex/` seguem preservados e so podem ser removidos com confirmacao do usuario.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a validacao da skill v2 foi concluida; qualquer agente serve se tiver contexto suficiente.

## 2026-08-20 - Gemini

### Objetivo

- Fechar a parte Gemini CLI da tarefa T-002, rodando os 7 evals da skill ai-project-structure.

### O Que Foi Feito

- T-002 executado: os 7 evals foram rodados com sucesso em diretorios limpos em `/tmp/skill-v2-tests-gemini/`. 
- Nos evals 6 e 7 as fixtures foram copiadas antes da execucao, permanecendo intactas.
- O validador `scripts/validate_structure.py` retornou exit 0 para os evals 1 a 6.
- No eval 7, o validador retornou exit 1 acusando exatamente os 2 erros esperados (ID duplicado `T-001` e Status invalido `Fazendo`).
- Teste extra: a skill disparou sozinha baseada na description, sem eu precisar citar explicitamente o nome da skill.
- Validador rodado na raiz do projeto como checagem final (0 erros, 4 avisos historicos conhecidos).

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests-gemini/` e os 7 subdiretorios temporarios para cada eval.

### Decisoes Tomadas

- Manter T-002 em aberto, e spec `0001-skill-v2` como "Em andamento", pois falta a avaliacao da ferramenta Codex CLI.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- T-002: Rodar os 7 evals no Codex CLI (invocando `$ai-project-structure`).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): Codex CLI.
- Motivo: Para completar a tarefa T-002.

## 2026-08-20 - Claude

### Objetivo

- Resolver as pendencias T-002 (rodar os 7 evals da skill v2) e T-003 (testar o fluxo de atualizacao v1 para v2 de ponta a ponta), na parte que o Claude Code cobre.

### O Que Foi Feito

- Conferida a paridade fonte x instalado: `diff -r` entre `docs/skills/ai-project-structure/` e `~/.claude/skills/ai-project-structure/` acusa apenas os arquivos que o `install.sh` nao propaga por design (`CHANGELOG.md`, `README.md`, `evals/`, `install.sh`).
- T-002 no Claude Code: os 7 evals executados em subdiretorios limpos sob `/tmp/skill-v2-tests/`, um por eval, fora do repositorio e sem git. Resultado 7/7 aprovados. Evals 6 e 7 rodaram sobre copias das fixtures; os originais ficaram intactos (hash conferido antes e depois).
- Cada eval fechou com `scripts/validate_structure.py`: exit 0 nos evals 1 a 6; exit 1 no eval 7 com exatamente os 2 erros esperados (ID duplicado `T-001` e Status invalido `Fazendo`), relatados sem aplicar correcao.
- T-003: montado um projeto v1 realista em `/tmp/skill-v2-tests/projeto-v1/` (fixture `v1-project` mais 2 entradas de sessao e 1 secao propria extra no `AGENTS.md`) e executado o fluxo de `references/atualizacao.md` inteiro. Os 8 invariantes passaram, incluindo a checagem por `diff` de que o conteudo fora dos marcadores ficou byte-identico.
- Confirmado no T-003 que as duas secoes proprias do usuario ("Regra Local Do Time" e "Padrao De Nomes De Branch") migraram para "Regras Do Projeto" com o corpo inalterado; so o nivel do heading mudou de `##` para `###` para ficar aninhado na secao.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests/` (7 subdiretorios de eval mais `projeto-v1/`), todos descartaveis.

### Decisoes Tomadas

- Manter T-002 em aberto: a tarefa exige as tres ferramentas e so o Claude Code foi coberto nesta sessao.
- Preencher "Evidencia De Conclusao" da spec 0001 de forma parcial e marcada como tal, sem mudar o Status para Concluida, para nao perder o registro do que ja foi verificado.
- Na migracao de TASKS do eval 6 e do T-003, atribuir apenas os IDs, sem acrescentar data as linhas de "Concluidas": a data nao foi confirmada pelo usuario e o validador nao a exige.

### Aprendizados Para MEMORY.md

- Nenhum. Os resultados sao execucao de teste ja registrada aqui e na spec.

### Pendencias

- T-002: repetir os mesmos 7 evals no Codex CLI (invocando `$ai-project-structure`) e no Gemini CLI. So entao a tarefa fecha.
- Spec `0001-skill-v2` segue "Em andamento" ate T-002 fechar.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): Codex CLI e depois Gemini CLI, nesta ordem.
- Motivo: o que falta e execucao dos mesmos evals nas outras duas ferramentas; qualquer agente serve se tiver contexto suficiente, mas a tarefa e por definicao amarrada a ferramenta.

## 2026-08-20 - Claude

### Objetivo

- Analisar a skill/metodologia specsfy (github.com/promovaweb/specsfy), extrair o que serve ao nosso contexto e implementar a v2.0.0 da skill ai-project-structure.

### O Que Foi Feito

- Analise completa do specsfy: repo, 18 skills, CLI, metodo MCR-10, gates com scripts; complementada por relatorio dos videos do autor (via NotebookLM). Conclusao: sistemas complementares; importamos mecanismos pontuais, sem a cerimonia pesada.
- Skill v2.0.0 implementada: entrevista numerada com opcoes, regra "Nunca Inferir", TASKS com IDs T-NNN, blocos gerenciados `ai-project-structure:core`/`:specs` com versao, validador `scripts/validate_structure.py` (Python 3, stdlib), modulo opcional de specs (`docs/specs/`), fluxos em `references/atualizacao.md` e `references/specs.md`, 7 evals com fixtures, CHANGELOG proprio da skill, `install.sh` copiando scripts/ e references/.
- Regra nova a pedido do usuario: travessao (em dash, U+2014) proibido em todos os textos do projeto e do core da skill; validador acusa como erro; ocorrencias existentes substituidas.
- Dogfood no meta-projeto: `AGENTS.md` da raiz atualizado para o template v2 com bloco specs; `docs/specs/` ativado com a spec `0001-skill-v2`; `TASKS.md` migrado para T-IDs; `PROJECT_CONTEXT.md` preenchido; `ROADMAP.md` atualizado; entrada de 2026-04-25 do `CONSENSUS.md` recebeu Status.
- Skill reinstalada nas tres ferramentas; paridade conferida por diff; validador rodado do diretorio instalado contra o meta-projeto (0 erros, 4 avisos historicos de SESSION).

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/`: SKILL.md, CHANGELOG.md (novo), install.sh, README.md, evals/evals.json, evals/fixtures/ (novo), scripts/validate_structure.py (novo), references/ (novo), assets/AGENTS.md, assets/partials/ (novo), assets/docs/{README,TASKS,QUALITY,MEMORY}.md, assets/docs/specs/ (novo), assets/docs/archive/README.md.
- Raiz e docs vivos: `AGENTS.md`, `docs/PROJECT_CONTEXT.md`, `docs/TASKS.md`, `docs/ROADMAP.md`, `docs/CONSENSUS.md`, `docs/specs/` (novo), `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`.
- Instalacoes: `~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/` (reinstaladas, fora do projeto).

### Decisoes Tomadas

- Direcao da v2: melhorias pontuais + modulo de specs leve; sem pipeline SDD completo (decisao do usuario; ver `docs/DECISIONS.md` e DEC-001 a DEC-004 na spec 0001).
- Travessao proibido em textos do projeto (pedido do usuario).

### Aprendizados Para MEMORY.md

- O usuario nao quer o caractere travessao (em dash, U+2014) em nenhum texto deste projeto; separadores aceitos: dois-pontos, ponto-e-virgula, virgula, parenteses, hifen.

### Pendencias

- Rodar os 7 evals manualmente nas tres ferramentas (T-002).
- Testar o fluxo de atualizacao v1 para v2 em projeto real externo (T-003).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com acesso as tres ferramentas.
- Motivo: as pendencias sao execucao de evals e teste de fluxo; nao exigem modelo especifico.

## 2026-05-26 - Claude

### Objetivo

- Propagar os ajustes Codex da skill para as tres ferramentas (pendencia deixada pela sessao Codex).

### O Que Foi Feito

- Conferida a fonte canonica: `agents/openai.yaml` (YAML valido por inspecao; PyYAML ausente no ambiente) e `README.md` com as correcoes do Codex.
- Confirmado que o Codex nao deixou `quick_validate.py` na fonte (era do workspace dele).
- Rodado `docs/skills/ai-project-structure/install.sh` (global).
- Verificado por `diff` que `agents/openai.yaml` ficou identico a fonte nos tres destinos (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`).

### Arquivos Criados Ou Alterados

- `~/.claude/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `~/.agents/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `~/.gemini/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `docs/TASKS.md`, `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma. Apenas execucao da propagacao pendente.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill revisada, corrigida e instalada nas tres ferramentas; ciclo fonte -> `install.sh` estabelecido para mudancas futuras.

## 2026-05-26 - Codex

### Objetivo

- Revisar e corrigir somente a parte OpenAI/Codex da skill `ai-project-structure`, validando contra a documentacao oficial atual do Codex CLI.

### O Que Foi Feito

- Lidos `AGENTS.md` e a memoria relevante em `docs/`.
- Consultada a documentacao oficial atual do Codex sobre Agent Skills e o guia oficial de evals para skills.
- Confirmado que o caminho atual do Codex e `$HOME/.agents/skills` para usuario e `.agents/skills` para repo/projeto; `~/.codex/skills` aparece em material antigo e nao foi usado.
- Ajustado `agents/openai.yaml`: `short_description` reduzida para caber no intervalo recomendado e `default_prompt` atualizado para mencionar explicitamente `$ai-project-structure`.
- Ajustado `README.md`: invocacao explicita do Codex atualizada para `/skills` ou `$ai-project-structure`; nota adicionada sobre evals com prompts CSV e traces JSONL via `codex exec --json`.
- Validado `SKILL.md`, `agents/openai.yaml` e `install.sh` manualmente. O validador local `quick_validate.py` nao rodou porque o Python do ambiente nao tinha `PyYAML`.
- Tentativa de rodar `./install.sh` para propagar foi bloqueada pela aprovacao de escrita fora do workspace.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/agents/openai.yaml`
- `docs/skills/ai-project-structure/README.md`
- `docs/TASKS.md`
- `docs/CHANGELOG.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma decisao formal nova; foram aplicadas correcoes de conformidade com a documentacao atual.

### Aprendizados Para MEMORY.md

- Nenhum. Os pontos relevantes ficaram registrados nesta sessao e no changelog.

### Pendencias

- Rodar `docs/skills/ai-project-structure/install.sh` para propagar as mudancas para `~/.agents/skills/`, `~/.claude/skills/` e `~/.gemini/skills/` quando houver permissao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a fonte canonica ja foi corrigida; falta apenas propagar a instalacao, e qualquer agente serve se tiver contexto suficiente e permissao para escrever nos diretorios globais.

## 2026-05-26 - Claude

### Objetivo

- Transformar a skill `ai-project-structure` em um pacote instalavel em Claude Code, Codex CLI e Gemini CLI.

### O Que Foi Feito

- Verificado o estado real dos hosts: a instalacao registrada em 2026-04-25 nao existia em nenhum lugar; `~/.codex/skills/` so tinha `.system` (e nao e o caminho lido pelo Codex).
- Confirmado por pesquisa nas docs oficiais que `SKILL.md` virou **Agent Skills Open Standard**, lido por Claude Code, Codex CLI e Gemini CLI - um unico pacote serve aos tres.
- Confirmados os caminhos: Claude `~/.claude/skills/`, Codex `~/.agents/skills/`, Gemini `~/.gemini/skills/`.
- Criados `install.sh` (instalador idempotente, global/projeto, por ferramenta, com `--uninstall`), `README.md` (distribuicao/uso) e `agents/openai.yaml` (metadado opcional do Codex) na pasta da skill.
- Instalada a skill globalmente nas tres ferramentas e verificado o conteudo (SKILL.md + assets/ + agents/) em cada destino.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/install.sh` (novo)
- `docs/skills/ai-project-structure/README.md` (novo)
- `docs/skills/ai-project-structure/agents/openai.yaml` (novo)
- `~/.claude/skills/ai-project-structure/` (instalado, fora do projeto)
- `~/.agents/skills/ai-project-structure/` (instalado, fora do projeto)
- `~/.gemini/skills/ai-project-structure/` (instalado, fora do projeto)
- `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/SESSION.md`

### Decisoes Tomadas

- Distribuir a skill como pacote unico no Agent Skills Open Standard (ver `DECISIONS.md` 2026-05-26).
- Corrigido o caminho do Codex: `~/.agents/skills/`, nao `~/.codex/skills/`.

### Aprendizados Para MEMORY.md

- Nenhum. Decisao e correcao ja registradas em `DECISIONS.md`/`CHANGELOG.md`.

### Pendencias

- Nenhuma acionavel. (Opcional: testar a invocacao em uma sessao real de cada ferramenta.)

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill instalada e distribuivel nas tres ferramentas; para propagar mudancas futuras, edite a fonte em `docs/skills/ai-project-structure/` e rode `install.sh`.

## 2026-04-25 - Claude

### Objetivo

- Instalar a skill `ai-project-structure` globalmente nos hosts do usuario (Claude Code e Codex).

### O Que Foi Feito

- Copiada a skill para `~/.claude/skills/ai-project-structure/SKILL.md`.
- Copiada a skill para `~/.codex/skills/ai-project-structure/SKILL.md` em paralelo com o Codex (resultado idempotente; ver entrada seguinte).
- Consolidada a entrada de instalacao em `TASKS.md` cobrindo ambos os locais.

### Arquivos Criados Ou Alterados

- `~/.claude/skills/ai-project-structure/SKILL.md` (novo, fora do projeto)
- `~/.codex/skills/ai-project-structure/SKILL.md` (novo, fora do projeto)
- `docs/SESSION.md` (esta entrada)
- `docs/TASKS.md`

### Decisoes Tomadas

- Nenhuma.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill disponivel globalmente em ambos os hosts; novos projetos podem invoca-la.

## 2026-04-25 - Codex

### Objetivo

- Instalar skill ai-project-structure globalmente em `~/.codex/skills/`.

### O Que Foi Feito

- Criado o diretorio `~/.codex/skills/ai-project-structure/` se ainda nao existia.
- Copiado `docs/skills/ai-project-structure/SKILL.md` para `~/.codex/skills/ai-project-structure/SKILL.md`.
- Confirmada a instalacao com listagem do diretorio global da skill.
- Atualizado `TASKS.md` movendo a instalacao global da skill para concluidas.

### Arquivos Criados Ou Alterados

- `~/.codex/skills/ai-project-structure/SKILL.md`
- `docs/SESSION.md`
- `docs/TASKS.md`

### Decisoes Tomadas

- Nenhuma decisao nova; foi executada a instalacao solicitada pelo usuario.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill instalada globalmente; proxima acao depende do proximo uso ou projeto.

## 2026-04-25 - Claude

### Objetivo

- Aplicar as oito melhorias aprovadas no tri-consenso sobre `MEMORY.md` e estrutura.

### O Que Foi Feito

- Criado `docs/MEMORY.md` com tipos User / Feedback / Project / Reference, criterio de promocao, sobrescrita ativa e regra de dados sensiveis.
- Criado `docs/archive/` com `README.md` indice para rotacao futura de `SESSION.md` e `CONSENSUS.md`.
- Reescrito `AGENTS.md` cobrindo: imutabilidade dos arquivos-ponte, dois niveis de leitura, regra de desempate, atualizacao por gatilho, criterio de "onde escrever cada coisa", politica de rotacao e uso restrito de `CONSENSUS.md`.
- Atualizado template de `SESSION.md` (handover direcionado, secao de aprendizados para `MEMORY.md`).
- Atualizado template de `CONSENSUS.md` (`Status` e `Proximo passo`).
- Atualizado `QUALITY.md` com checklist de atualizacao por gatilho e cuidados com `MEMORY.md`.
- Sincronizada skill `ai-project-structure` com a estrutura nova.
- Registrada decisao `Evolucao da estrutura: MEMORY.md e oito melhorias` em `DECISIONS.md` e atualizado `CHANGELOG.md`.
- Fechada entrada do `CONSENSUS.md` com `Status: resolvido` e nota de aprovacao do usuario.

### Arquivos Criados Ou Alterados

- `AGENTS.md` (reescrito)
- `docs/MEMORY.md` (novo)
- `docs/archive/README.md` (novo)
- `docs/QUALITY.md`
- `docs/SESSION.md` (template + esta entrada)
- `docs/CONSENSUS.md` (template + fechamento)
- `docs/DECISIONS.md`
- `docs/CHANGELOG.md`
- `docs/README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/TASKS.md`
- `docs/skills/ai-project-structure/SKILL.md`

### Decisoes Tomadas

- Aplicacao das oito melhorias do tri-consenso (ver `DECISIONS.md`).

### Aprendizados Para MEMORY.md

- Nenhum. Esta sessao foi exercicio de meta-estrutura, nao gerou aprendizados sobre projetos reais.

### Pendencias

- Preencher `PROJECT_CONTEXT.md` com o contexto real do projeto, quando houver.
- Instalar a skill globalmente no Codex, se desejado.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: estrutura pronta para uso; a proxima acao depende do projeto real que sera tocado nela.

## 2026-04-25 - Codex

### Objetivo

- Preencher a posicao do Codex no consenso aberto sobre `MEMORY.md` e melhorias estruturais.

### O Que Foi Feito

- Leitura de `AGENTS.md` e dos arquivos em `docs/`.
- Atualizacao apenas da secao `Posicao Do Codex` na entrada `2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias`.
- Acrescentados pontos de acordo adicionais, riscos novos e uma frase de tri-consenso no `Consenso Final`.
- Mantido o status da entrada como aberto, conforme solicitado pelo usuario.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma decisao formal nova foi registrada; a entrada continua aberta para decisao do usuario.

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

### Pendencias

- Usuario decidir se aprova a implementacao de `docs/MEMORY.md` e das melhorias consensuadas.
- Se aprovado, atualizar `AGENTS.md`, `QUALITY.md`, `PROMPTS.md`, `docs/skills/ai-project-structure/SKILL.md` e demais referencias afetadas.

### Proximo Passo Recomendado

- Para qualquer agente: aguardar a aprovacao do usuario antes de criar `MEMORY.md` ou aplicar as regras novas.

## 2026-04-25 - Gemini

### Objetivo

- Participar do consenso sobre a adição de `MEMORY.md` e detalhamento de melhorias estruturais.

### O Que Foi Feito

- Análise da posição do Claude em `docs/CONSENSUS.md`.
- Registro da posição do Gemini apoiando a criação de `MEMORY.md` e os sete pontos de melhoria detalhados.
- Atualização dos "Pontos de Acordo", "Riscos e Tradeoffs" e "Consenso Final" no debate.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Consenso técnico atingido entre Claude e Gemini para evoluir a estrutura com 8 melhorias (7 detalhadas + `MEMORY.md`).

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

### Pendencias

- Aprovação do usuário para aplicar as mudanças em `AGENTS.md` e criar `MEMORY.md`.

### Proximo Passo Recomendado

- Usuário revisar o consenso final e instruir a implementação das melhorias.

## 2026-04-25 - Gemini

### Objetivo

- Validar a estrutura Markdown multiagente do projeto.

### O Que Foi Feito

- Leitura e análise exaustiva de `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e diretório `docs/`.
- Registro da posição do Gemini em `docs/CONSENSUS.md` sobre a clareza e segurança da estrutura.
- Sugestão de melhorias focadas em handover de sessões e imutabilidade dos arquivos-ponte.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- A estrutura foi considerada apta para uso imediato em projetos reais tocados por múltiplas IAs.

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

### Pendencias

- Aguardar a validação e posição do Claude em `docs/CONSENSUS.md`.

### Proximo Passo Recomendado

- Solicitar ao Claude a revisão da estrutura conforme o prompt em `docs/PROMPTS.md`.

## 2026-04-25 - Codex

### Objetivo

- Criar uma estrutura Markdown multiagente para projetos tocados por IA.

### O Que Foi Feito

- Criada a raiz minima com arquivos de entrada para agentes.
- Centralizadas as regras de IA em `AGENTS.md`.
- Criada a memoria do projeto em `docs/`.
- Adicionado registro de sessoes em `SESSION.md`.
- Adicionado arquivo de consenso entre modelos em `CONSENSUS.md`.
- Adicionados prompts reutilizaveis em `PROMPTS.md`.
- Adicionada uma skill portavel em `docs/skills/ai-project-structure/SKILL.md`.

### Arquivos Criados Ou Alterados

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `docs/README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/SESSION.md`
- `docs/CONSENSUS.md`
- `docs/TASKS.md`
- `docs/DECISIONS.md`
- `docs/ARCHITECTURE.md`
- `docs/QUALITY.md`
- `docs/PROMPTS.md`
- `docs/CHANGELOG.md`
- `docs/GLOSSARY.md`
- `docs/ONBOARDING.md`
- `docs/ROADMAP.md`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/skills/ai-project-structure/SKILL.md`

### Decisoes Tomadas

- Manter na raiz apenas os arquivos Markdown de entrada dos agentes.
- Usar `AGENTS.md` como fonte central de regras.
- Usar `CLAUDE.md` e `GEMINI.md` como arquivos-ponte.
- Usar `SESSION.md` para continuidade entre sessoes.
- Usar `CONSENSUS.md` para debate entre modelos quando houver duvida real.

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

### Pendencias

- Instalar a skill em `~/.codex/skills/ai-project-structure` caso seja desejado torna-la global no Codex.
- Preencher os arquivos de contexto conforme o projeto real evoluir.

### Proximo Passo Recomendado

- Pedir ao Claude para revisar a estrutura usando o prompt em `PROMPTS.md`.
