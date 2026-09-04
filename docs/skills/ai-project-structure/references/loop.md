# Loop: Ativar Modulo E Rodar Uma Tarefa

Modulo opcional. **Nunca entra no scaffold**: um projeto recem-criado nao tem suite de teste, e um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao.

## Portao De Ativacao

O modulo so pode ser ativado em projeto que ja tem verificacao de verdade. Antes de tocar qualquer arquivo:

1. Leia a secao "Testes E Validacao" de `docs/QUALITY.md` do projeto-alvo.
2. Se ela estiver vazia, ou ainda com o texto do template ("Quando o projeto tiver codigo, registrar aqui"), ou sem nenhum comando executavel, **recuse a ativacao** e diga o motivo: sem portao real, o loop nao teria como saber se o trabalho ficou bom. Ofereca preencher a secao primeiro.
3. Se houver comando, mostre ao usuario o que voce encontrou e peca confirmacao de que aquilo e mesmo o portao do projeto. Nao infira.

Esta exigencia e pre-requisito de ativacao, nao check do validador: detectar "o projeto tem codigo" por heuristica e fragil e dispararia em todo projeto de conteudo.

## Ativar O Modulo

1. Confirme que o projeto usa a estrutura e esta na versao atual (marcadores em `AGENTS.md`; se estiver atras, ofereca primeiro o fluxo de `atualizacao.md`).
2. Insira o conteudo de `assets/partials/AGENTS-loop-block.md` em `AGENTS.md`, depois do ultimo bloco gerenciado e antes de "## Regras Do Projeto". Se o bloco `loop` ja existir, nao duplique.
3. Nao copie nenhum arquivo novo para o projeto: o `loop.sh` vive na skill instalada, nao no projeto-alvo.
4. Registre: entrada em `docs/SESSION.md` e linha em `docs/CHANGELOG.md` do projeto.

Desativar e remover o bloco entre os marcadores `loop`. Nada mais fica para tras.

## O Ciclo

Uma rodada trata **uma** tarefa:

1. **Elegibilidade.** A tarefa indicada precisa existir em "Em Andamento" ou "Proximas Tarefas" e ter `(verifica: <comando>)` na linha. Parenteses no comando nao sao suportados: use um script auxiliar no projeto, por exemplo `bash portao.sh`. Sem isso, a rodada termina antes de chamar o agente, com codigo diferente de zero.
2. **Trabalho.** O agente recebe a tarefa e o `AGENTS.md` do projeto, que ja traz os limites do bloco de loop.
3. **Portao.** Roda o comando declarado em `(verifica:)`, no diretorio do projeto.
4. **Realimentacao.** Portao falhou e ainda ha tentativa: a saida do comando volta como contexto para a proxima. Essa realimentacao e a unica coisa que o loop faz melhor que uma pessoa rodando o comando na mao; sem ela o modulo nao teria razao de existir.
5. **Fecho.** Portao passou: move a tarefa para "## Concluidas" com a data do dia e escreve a sub-linha de evidencia, com `tipo=comando`, `procedimento` igual ao comando declarado e `resultado` com a saida real.
6. **Desistencia.** Esgotou as tentativas: nada se move, nada de evidencia, relatorio com as saidas de todas as tentativas, exit diferente de zero.
7. **Bloqueio.** O agente sinalizou falta de contexto obrigatorio: a tarefa vai para "## Aguardando Usuario" com a pergunta escrita, e a rodada para.

## Uso

```bash
loop.sh --tarefa T-042 --agente "claude -p"
loop.sh --tarefa T-042 --agente "codex exec" --tentativas 5
loop.sh --tarefa T-042 --agente "gemini -p" --projeto /caminho/do/projeto
```

### Comandos Por Ferramenta

Rodar sem supervisao nao e o modo padrao de nenhuma CLI: cada uma pede flags proprias para aprovar edicoes sozinha. Estes foram exercitados de verdade:

| Ferramenta | `--agente` |
|---|---|
| Claude Code | `claude -p --permission-mode bypassPermissions` |
| Codex CLI | `codex exec -s workspace-write --skip-git-repo-check` |
| Gemini CLI | `gemini --approval-mode yolo --skip-trust -p` |
| Grok | `grok --always-approve -p` |
| opencode (qualquer provedor) | `opencode run --auto -m <provedor>/<modelo>` |

Duas armadilhas que custam uma rodada inteira quando passam batido:

- `codex exec` **recusa rodar fora de um repositorio git** sem `--skip-git-repo-check`. Projeto de conteudo sem git cai nisso.
- `gemini` recusa rodar em diretorio nao confiavel sem `--skip-trust` (ou `GEMINI_CLI_TRUST_WORKSPACE=true`).

O `opencode` merece nota propria porque nao esta preso a um fornecedor: `-m` recebe `provedor/modelo` (`deepseek/deepseek-v4-pro`, `openrouter/...`, e o que mais aparecer em `opencode models`), e `--variant high|max|minimal` da a escada de esforco. Exercitado com DeepSeek, portao verde na tentativa 1.

Cuidado com o que voce esta gastando: quando o provedor entra por chave de API, e cobranca por token de verdade, e nao consumo de assinatura. Ai o valor em dolar e dinheiro, ao contrario do numero a preco de tabela que as CLIs de assinatura imprimem. `opencode stats` mostra o acumulado da instalacao, nao a rodada; para custo por rodada, use `--format json`.

Nas ferramentas em que a flag de prompt recebe um valor, como `grok -p` e `gemini -p`, deixe a flag **por ultimo**: o `loop.sh` acrescenta o prompt como ultimo argumento, entao ele vira o valor dela.

Acrescentar `--output-format json` no Claude ou no Grok faz a saida trazer os tokens da rodada. O `loop.sh` nao le esses numeros; eles ficam no relatorio para voce.

Cuidado com o campo de custo em dolar: o Claude marca `"costBasis": "list"`, ou seja, preco de tabela da API calculado a partir dos tokens. Quem usa assinatura nao paga aquilo; o numero serve para comparar consumo entre rodadas, nao para prever fatura. O que vale acompanhar sob assinatura e token, turno e tempo.

O modelo e o esforco tambem entram por aqui, e cada CLI tem a propria flag (`--model`, `-m`, `--reasoning-effort`). Sem flag, cada ferramenta usa o padrao dela, que muda com o tempo: numa mesma bancada o Claude rodou em `claude-fable-5-1`, o Codex em `gpt-5.6-terra` com esforco `high` e o Grok em `grok-4.6`, nenhum deles escolhido por quem chamou.

- `--tarefa` (obrigatorio): o `T-NNN`.
- `--agente` (obrigatorio): comando headless da ferramenta que voce usa. O script nao assume nenhuma. O prompt entra como ultimo argumento. Argumento com espaco dentro de aspas nao e suportado.
- `--tentativas` (padrao 3).
- `--projeto` (padrao: diretorio atual).
- `--seco`: roda o ciclo sem chamar o agente, para testar portao e fluxo.

Exit codes, distintos de proposito para dar para ramificar por fora:

| Codigo | Significado |
|---|---|
| 0 | portao passou; tarefa fechada com evidencia de comando |
| 1 | erro de uso, ou tarefa nao elegivel (sem `(verifica:)`, ja concluida, inexistente) |
| 2 | portao falhou em todas as tentativas; nada movido, nada escrito |
| 3 | o agente sinalizou falta de contexto; tarefa em "Aguardando Usuario" |

Qualquer caminho diferente de sucesso sai diferente de zero, o que deixa a composicao por fora funcionar:

```bash
loop.sh --tarefa T-042 --agente "claude -p" && say pronto
```

## Perfis: Nao Digite O Comando Toda Vez

Ninguem quer escrever `--agente "claude -p --permission-mode bypassPermissions --model X --effort max"` na hora de rodar uma tarefa. E o comando muda conforme a intencao: planejar e executar pedem modelo e esforco diferentes, e cada ferramenta tem os proprios.

A solucao nao e mais um arquivo de configuracao. E a memoria do projeto, usada para o que ela ja serve: `docs/MEMORY.md`, secao `## User`, e onde ficam as preferencias de quem toca o projeto. Registre os perfis la, uma vez:

```md
## User

- Perfis de loop, por intencao e ferramenta:
  - Claude, executar: `claude -p --permission-mode bypassPermissions --model <modelo> --effort high`
  - Claude, planejar: `claude -p --permission-mode bypassPermissions --model <modelo> --effort max`
  - Codex, executar: `codex exec -s workspace-write --skip-git-repo-check -m <modelo>`
  - Codex, planejar: `codex exec -s workspace-write --skip-git-repo-check -m <modelo>`
  - Grok, executar: `grok --always-approve -m <modelo> --effort high -p`
```

Use o nome de modelo que a **sua** CLI aceita hoje; confira no `--help` dela. Nome de modelo envelhece rapido, e por isso ele fica na sua memoria de projeto, nao dentro da skill.

Com os perfis registrados, voce pede em linguagem natural ("roda o loop na T-042 para executar") e o agente do chat monta a chamada, mostra antes de rodar e executa. O fluxo esta em "Rodar Uma Tarefa Com O Loop", no `SKILL.md`.

O `loop.sh` continua sem saber o que e perfil: ele recebe uma string de `--agente` e obedece. Quem traduz intencao em comando e o agente do chat, lendo a sua memoria. Assim a escolha de modelo nunca entra no codigo da skill, que nao tem como acompanhar o catalogo de tres fornecedores.

## Escolher O Nivel De Esforco

Quando os perfis de executar tiverem degraus (`executar`, `executar-dificil`, `executar-muito-dificil`), **proponha um e diga por que em uma linha**. Nunca escolha em silencio: o nivel muda o consumo de plano, e quem paga e o usuario.

**Comece sempre em `executar`.** Nao e chute conservador, e o que a evidencia diz: tres bancadas, quatro ferramentas, tarefas indo de implementar funcao do zero a arrumar um manual espalhado por cinco arquivos, e **todas terminaram com portao verde na primeira tentativa**, varias delas no modelo mais barato disponivel.

Suba **so quando algum destes valer**, e diga qual:

1. **A rodada anterior falhou.** Sobe um degrau. E o unico sinal com evidencia de verdade, e o mais forte de todos: em vez de adivinhar dificuldade, voce ja sabe que o degrau anterior nao deu.

   O loop **nao registra fracasso em lugar nenhum**, por decisao registrada. Entao esse sinal so existe dentro da conversa em que a rodada aconteceu: em sessao nova, ele desaparece. Nao trate silencio como prova de que nunca falhou. Proponha o degrau base dizendo **"nao tenho registro de rodada anterior"**, e nao "e a primeira rodada", e deixe uma porta aberta em meia linha: se ja tentou antes, o usuario corrige e voce sobe.
2. **Duas rodadas ja falharam.** Sobe para `executar-muito-dificil`, e diga tambem que talvez o problema nao seja esforco: tarefa que falha duas vezes costuma estar mal especificada ou grande demais para uma rodada.
3. **O usuario disse que e dificil.** Vale mais que qualquer leitura sua da tarefa.
E so isso. **Nao estime dificuldade lendo a tarefa.** Nem por ela tocar varios arquivos, nem por ter regra de borda, nem por pertencer a uma spec, nem por o portao ser uma suite. Ja tentei com esses sinais e eles erraram: numa tarefa de conteudo com sete problemas espalhados por cinco arquivos, o sinal mandou subir um degrau e o modelo mais barato resolveu de primeira.

Nenhuma estimativa a priori se provou util ate agora, e cada degrau desnecessario e cota de plano ou dinheiro gasto a toa. Na duvida, **degrau base**: subir depois de uma falha real custa uma rodada, e comecar alto custa em toda tarefa que passaria de primeira.

Nao invente rubrica com pontuacao. Isso e julgamento declarado, nao medicao: diga o sinal que voce usou e deixe o usuario discordar em uma palavra.

**Degrau que nao existe naquela ferramenta nao vira degrau parecido em silencio.** As escadas nao sao iguais: uma ferramenta pode terminar antes da outra, e o rotulo da interface quase nunca e o valor que a CLI aceita.

Duas saidas legitimas, e uma proibida:

- O usuario ja decidiu antes que aquele degrau aponta para o teto da ferramenta, e isso esta escrito no perfil. Ai use, **e avise que e o teto**: "no Grok isso ja e o maximo".
- Nao ha decisao registrada. Ai diga qual e o teto e ofereca a escolha: ficar nele, ou rodar em outra ferramenta que va mais alto.
- Proibido: escolher o degrau parecido sem falar nada. O usuario acharia que pediu esforco maximo e recebeu outra coisa, sem nada no registro dizendo isso.

## Configurar Os Perfis

Dispare este fluxo quando o usuario pedir para ver, trocar ou criar perfil: "configura os perfis do loop", "quero mudar o modelo que o loop usa", "que modelo o loop esta usando", "o loop esta rodando com o que".

### 1. Mostre o que existe hoje

Leia `docs/MEMORY.md`, secao `## User`, e liste em tabela: intencao, ferramenta e comando. Mostre antes de perguntar qualquer coisa; muita vez o usuario so quer conferir e a conversa acaba aqui.

Sem nenhum perfil registrado, diga isso e va direto para o passo 3.

### 2. Pergunte o que mudar

```text
**1. O que voce quer fazer?**
   1. Trocar modelo ou esforco de um perfil que ja existe
   2. Criar perfil para outra intencao ou outra ferramenta
   3. Remover um perfil
   4. So conferir, nao mudar nada
```

Uma pergunta de cada vez, com opcoes numeradas, como no resto da skill. Resposta livre sempre vale.

### 3. Confirme os valores na ferramenta antes de gravar

**Nunca grave nome de modelo ou nivel de esforco que voce nao viu a CLI aceitar.** Nome de modelo envelhece rapido e perfil quebrado so aparece na hora da rodada, quando ja custou tempo. Onde conferir hoje:

| Ferramenta | Modelos | Esforco |
|---|---|---|
| Claude Code | `claude --help`, em `--model` (aceita alias como `fable`, `opus`, `sonnet`, ou nome completo) | `claude --help`, em `--effort` |
| Codex CLI | `~/.codex/models_cache.json` | chave `model_reasoning_effort` em `~/.codex/config.toml`, passavel por `-c` |
| Grok | `grok --help`, em `--model` | `grok --help`, em `--reasoning-effort` |

Esses caminhos sao detalhe interno de cada ferramenta e podem mudar. Se nao achar, **pergunte ao usuario** em vez de chutar. Ferramenta que nao estiver instalada nao ganha perfil: diga que nao esta e siga.

### 4. Mostre o comando montado e confirme

Monte a string inteira de `--agente`, incluindo as flags de permissao que a ferramenta exige para rodar sem supervisao (ver a tabela de comandos acima), e mostre antes de escrever. Perfil errado que so aparece na rodada custa uma tarefa.

### 5. Grave

Escreva em `docs/MEMORY.md`, secao `## User`. Trocando um perfil, **substitua a linha antiga** em vez de acrescentar outra: dois perfis para a mesma intencao e ferramenta viram ambiguidade na proxima chamada. Anote a data e como voce conferiu os nomes.

Se a mudanca for relevante, registre em `docs/SESSION.md`.

## Como O Agente Pede Ajuda

A regra "Nunca Inferir" manda perguntar quando falta contexto, e numa rodada de loop nao ha com quem falar. O protocolo e um arquivo:

1. O prompt manda o agente escrever a pergunta, em uma frase, em `.loop-pergunta` na raiz do projeto, e parar.
2. Depois de cada tentativa, antes de rodar o portao, o `loop.sh` procura esse arquivo.
3. Achou: o helper move a tarefa para "## Aguardando Usuario" com `**Pergunta:**` preenchida, o arquivo e apagado e a rodada termina com codigo 3. O portao nem chega a rodar.

Arquivo, e nao linha sentinela no stdout, porque cada ferramenta formata a saida de um jeito e nenhuma garante que o modelo emita uma string exata. Arquivo existe ou nao existe.

`.loop-pergunta` e temporario e some assim que e lido. Se sobrar de uma rodada interrompida, a rodada seguinte avisa e remove: uma pergunta ja registrada em `TASKS.md` nao precisa do arquivo de novo.

## Como A Evidencia E Escrita

Quem escreve e o `loop_task.py`, nunca o shell. Ele reusa o parser do `validate_structure.py`, entao o que ele entende por secao, ID e marcador e exatamente o que o validador entende; nao ha dois parsers do mesmo arquivo divergindo com o tempo.

A evidencia e sempre uma sub-linha so:

```md
- AAAA-MM-DD T-042: Descricao da tarefa. (verifica: pytest -q)
  - Evidencia: tipo=comando; procedimento=pytest -q; resultado=exit 0; 42 passed in 3.10s
```

### Regra Critica Vai No Prompt, Nao So No Bloco

O bloco do `AGENTS.md` depende de o agente escolher ler o arquivo. O prompt do `loop.sh` chega sempre. A diferenca nao e teorica: a regra "nao apague o que falha" viveu so no bloco por uma bancada, e um modelo mais barato apagou informacao para o portao passar mesmo com ela escrita la. Movida para o prompt, sem mudar mais nada, o mesmo modelo passou a perguntar.

A regra que sai disso: quando a violacao de uma restricao **passa despercebida no portao**, ela nao pode morar so no bloco. Tem que estar no prompt, onde nao da para nao ler.

E nao custa: na matriz refeita, com a restricao no prompt, o consumo **caiu** em todas as ferramentas que rodaram, uma delas pela metade. Dizer a restricao antes evita o agente explorar um caminho que seria descartado depois.

### O Que Vive No Prompt E O Que Vive No Bloco

Revisao item a item feita em 2026-09-03, com um criterio so: **a regra vai para o prompt quando a violacao dela deixa o portao verde do mesmo jeito.** O resto fica no bloco, que existe para quem le.

No prompt, porque o portao nao pega:

1. trabalhe so na tarefa indicada;
2. nao mova a tarefa nem escreva evidencia;
3. faltou contexto obrigatorio, pergunte e pare;
4. nao apague o que falha;
5. nao edite `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `DECISIONS.md` nem specs.

So no bloco, de proposito:

- **descricao do ciclo, tentativas e exit codes**: o agente nao tem como violar, e repetir isso custaria contexto em toda tentativa;
- **"tarefa sem `(verifica:)` nao e elegivel"**: garantido em codigo pelo `loop_task.py check`, antes de o agente ser chamado. Regra que o codigo enforca nao precisa de boa vontade;
- **"fecha so com exit 0", "nunca evidencia `revisao-manual`"**: descrevem o que o **loop** escreve. A parte que o agente poderia violar ja esta no item 2.

O item 5 foi o unico buraco que a revisao encontrou. Em nove rodadas de bancada nenhum agente havia tocado em arquivo de memoria, entao o risco era teorico; entrou mesmo assim, porque o pior caso e um agente afrouxar em `AGENTS.md` a regra que o restringe, e isso nao aparece em portao nenhum.

### A Evidencia Vale O Que O Portao Vale

Isto precisa estar dito com todas as letras: a evidencia prova que **o comando declarado passou**, e nada alem disso. Numa bancada com tres ferramentas, duas entregaram implementacao com bug numa regra de borda que a suite de testes nao cobria. O portao ficou verde, a evidencia foi escrita com lastro real de exit code, e o bug foi junto.

Isso nao e defeito do loop: e o loop cumprindo exatamente o que promete. A licao e sobre o portao, nao sobre a automacao. Portao fraco automatizado continua fraco, so que mais rapido. Antes de declarar `(verifica:)` numa tarefa, pergunte se aquele comando falharia caso o trabalho saisse errado.

### Formato Do Campo `resultado`

`resultado` recebe o exit code e a saida real do comando, com espacos colapsados para caber em uma linha. Saida longa e cortada pelo comeco, preservando o fim, que e onde suite de teste costuma imprimir o placar; quando isso acontece o corte fica declarado no proprio campo, em vez de escondido.

## Isolamento

O `loop.sh` roda onde voce o chamar, e nao cria worktree. Quem quiser isolar faz antes, com o que o git ja oferece:

```bash
git worktree add ../projeto-loop -b loop/T-042
cd ../projeto-loop
loop.sh --tarefa T-042 --agente "claude -p"
```

Isso foi deixado de fora do modulo de proposito: a estrutura nem sempre vive em repositorio git, e trazer a rodada de volta viraria merge em `TASKS.md`, o arquivo mais editado do projeto.

## O Que O Loop Nunca Faz

- Escolher sozinho em que tarefa trabalhar.
- Fechar tarefa que nao declarou comando.
- Escrever evidencia de `tipo=revisao-manual` ou `tipo=conferencia`.
- Escrever em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` ou em specs.
- Inventar a resposta que falta. Falta de contexto vira pergunta registrada e parada, nunca inferencia.
