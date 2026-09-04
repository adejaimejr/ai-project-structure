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

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-062 e T-073, skill 2.9.1)

### Objetivo

- Fechar as duas ultimas tarefas da revalidacao adversarial (texto de `atualizacao.md` e `install.sh` com confirmacao) pelo loop com o `terra`.

### O Que Foi Feito

- **T-062** (bump 2.9.1): verde na tentativa 2. O texto do agente estava certo desde a tentativa 1; quem falhava era o meu portao, duas vezes: `.*` no titulo com `re.S` engolia o documento e capturava corpo vazio, e o titulo era comparado sem `re.I`. Corrigido com o loop rodando (ele rele o portao a cada execucao). Efeito colateral: tentando casar a regex, o agente renomeou dois headings de `atualizacao.md` (`MIGRAR TASKS` em minusculo, `v2 -> v2.x` em prosa); restaurados por mim. Licao: portao de texto que casa heading precisa de teste contra o texto **antes** da rodada, senao o agente escreve para a regex e nao para o leitor.
- **T-073** (sem bump): verde na tentativa 1. `install.sh` compara so o que distribui, lista `faltando`, `diferente` e `extra`, pede `[s/N]`, recusa sem terminal, aceita `--sim`; arquivo extra nao e apagado (decisao de T-067). `verificar_install` prova os dois lados com destino temporario sujo (verificador de 63 para 65). README da skill e CHANGELOG completados por mim.
- **Primeiro uso real da protecao**: a reinstalacao da 2.9.1 nos destinos em 2.9.0 recusou sem `--sim`, listando os arquivos, e instalou com `--sim`. `diff -rq` limpo fora do nao distribuido.
- `SESSION.md` rotacionado pela terceira vez no dia.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `install.sh`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/atualizacao.md`, `evals/verify_repository.py`, `evals/portao_t062.py`, `evals/portao_t073.py`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal.

### Aprendizados Para MEMORY.md

- Portao de tarefa que casa texto por regex precisa passar contra um texto de exemplo escrito antes da rodada. Dois bugs de regex no portao de T-062 custaram uma tentativa e dois headings renomeados pelo agente para satisfazer a regex.

### Pendencias

- **O pacote da revalidacao adversarial de 2026-09-03 esta inteiro fechado**: T-059 a T-073, seis releases (2.6.0 a 2.9.1). Abertas so T-053 a T-058, anteriores a revalidacao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario para T-053 (calibragens da spec 0006); qualquer agente para T-054, T-055, T-056 e T-058, que ja tem conserto descrito.
- Motivo: sao as unicas tarefas abertas, e as quatro tecnicas cabem numa release 2.10.0 pelo mesmo molde de portao proprio.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-064 e T-063, skill 2.9.0)

### Objetivo

- Fechar os dois residuos sem decisao da REVAL-2 e da REVAL-6 (consertos do validador e templates atrasados) pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- Portoes proprios por comportamento: `portao_t064.py` (12 checks, reproduzia 4 de 12) com o verificador geral dentro, porque a tarefa nao toca o core; `portao_t063.py` (12 checks, 2 de 12) sem o verificador, porque muda uma frase do core e a propagacao e minha.
- **T-064** (bump 2.9.0), verde na tentativa 1: `ARQUIVO-UTF8-INVALIDO` novo, com fixture materializada em latin-1 so no temporario; cercas `~~~` reconhecidas; headings ATX com fechamento aceitos; `field_value` sem `split` cego; `NNNN` tolerado so como placeholder inteiro; `**Status:**` de spec ancorado; `ENTRY_RE` e `DATE_RE` fora. Fixtures existentes ganharam os casos (debate-project como controle, cobertura-* acusando). Um ajuste meu: a fixture de consenso tinha `\u0301` como texto literal em vez do acento combinante real; trocado.
- **T-063**, verde na tentativa 1: QUALITY, PROMPTS, ONBOARDING, README, SESSION, TASKS, ARCHITECTURE e GLOSSARY dos assets atualizados para o core 2.2.0/2.4.0; exemplo `revisao-manual` no template de tarefas e o exemplo de spec fora do modelo de linha; core com "quando existir" em `docs/ARCHITECTURE.md`; `verificar_convencoes` cobre os quatro templates que citam regra do core (verificador de 59 para 63). Core propagado por mim; CHANGELOG completado com a frase do core.
- 2.9.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/docs/{QUALITY,PROMPTS,ONBOARDING,README,SESSION,TASKS,ARCHITECTURE,GLOSSARY}.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t063.py`, `evals/portao_t064.py`, `evals/fixtures/{cobertura-arquivos,cobertura-consenso,cobertura-tarefas,debate-project}/`.
- Projeto: `AGENTS.md` (core e marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal.

### Aprendizados Para MEMORY.md

- Nenhum novo.

### Pendencias

- Da revalidacao sobram T-062 (texto de `atualizacao.md`) e T-073 (`install.sh` com confirmacao), as duas baixas e sem decisao. Fora dela, T-053 a T-058.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-062 e T-073 juntas; nenhuma exige bump (T-062 muda `references/`, que e distribuido: exige; T-073 nao).
- Motivo: fecham o pacote da revalidacao inteiro.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-060, skill 2.8.1)

### Objetivo

- Fechar T-060, o pacote de consertos do modulo de loop (REVAL-3 e REVAL-4, onze itens), pelo loop com o `terra`.

### O Que Foi Feito

- Portao proprio por comportamento com agente falso por item (`evals/portao_t060.py`, 14 checks, reproduzia 0 de 14). Loop verde na tentativa 1, sem pergunta, stdin fechado no lancamento.
- Consertos do terra, revisados: linha da tarefa capturada no arranque (`loop_task.py linha`) e `fechar --linha-esperada` recusando se mudou; sub-linhas preservadas em `fechar` e `bloquear`; `errors="replace"` na saida e na pergunta; pergunta vazia vira `(vazia)` com exit 3; `fchmod` preservando o modo do `TASKS.md`; `sys.dont_write_bytecode` no helper; agente chamado com `</dev/null`; prompt dizendo que propagar bloco ao `AGENTS.md` e do agente de chat; exit 4 na tabela de `references/loop.md`; `--seco` sem `--agente`. Bump 2.8.1, bloco core intocado.
- Dois ajustes meus: a realimentacao da falha tinha sido truncada a 400 bytes (mesmo teto da evidencia), o que esvazia o que o loop faz de melhor; subi para 64KB. E o agente nao escreveu os casos hostis na bateria, que a tarefa pedia: portados por mim em `testar_hostil` (nove casos, bateria de 63 para 74; piso do verificador subiu junto). O caso de saida fora de UTF-8 quebrou o proprio harness da bateria, que decodificava o stdout do `loop.sh` em UTF-8 estrito; corrigido no harness.
- Seis mutacoes reversas (stdin aberto, `fchmod` fora, sub-linhas apagadas, linha esperada ignorada, realimentacao inteira, `--seco` com agente): seis pegas pela bateria.
- 2.8.1 reinstalada nos tres destinos. `SESSION.md` rotacionado de novo (duas entradas de 2026-09-03 para o archive).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/loop.sh`, `scripts/loop_task.py`, `evals/test_loop.py`, `evals/verify_repository.py`, `evals/portao_t060.py`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. Realimentacao em 64KB e calibragem minha, registrada no CHANGELOG da skill.

### Aprendizados Para MEMORY.md

- Nenhum novo. "Portao por comportamento com agente falso" ja esta na pratica das ultimas cinco rodadas; virou molde (`portao_t0NN.py`), nao regra.

### Pendencias

- Todo o pacote da revalidacao que nao dependia de decisao esta fechado: T-060, T-065, T-069 a T-072. Abertas: T-062, T-063, T-064, T-073, e T-053 a T-058. Os portoes `portao_t0NN.py` ficam em `evals/` como registro; o que eles cobram vive na bateria e no verificador.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-063 (templates) e T-064 (tracebacks do validador), as duas ainda sem decisao pendente; o loop serve, com portao proprio.
- Motivo: T-063 e o que o usuario final recebe, e T-064 sao dois tracebacks reproduzidos.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-072 e T-071, skill 2.8.0)

### Objetivo

- Fechar o residuo de T-059 e T-061 (diagnostico de parenteses no marcador verifica, e texto honesto no core) pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- As duas tarefas mudam o texto do bloco core, que o loop nao pode propagar para a raiz. Portoes proprios por comportamento e texto **sem** o `verify_repository.py` (paridade quebrada de proposito ate a propagacao), replicando o que ele cobraria de versao e cobertura por codigo. Marcadores da raiz em v2.8.0 antes; tarefas refinadas dizendo quem propaga.
- **T-072** (primeiro, faz o bump): loop travou na primeira tentativa de lancamento porque o `codex exec` herdou stdin aberto e ficou em "Reading additional input from stdin"; relancado com `</dev/null`, verde na tentativa 1. `VERIFICA-COMANDO-PARENTESES` (ERRO) com fixture, `loop_task.py check` recusa e explica, texto no item do marcador no core, no cabecalho do template de `TASKS.md` e em `references/loop.md`, teste novo na bateria (63). Core propagado por script, verificador 59 de 59.
- **T-071**: verde na tentativa 1. Secao das pontes diz o que o validador confere de fato (so a mencao a `AGENTS.md`). No travessao o agente **estreitou a regra** para os arquivos que o validador olha; a decisao era texto honesto sobre o alcance, nao regra menor (o verificador deste repo acusa em qualquer arquivo versionado). Reescrito por mim: a regra segue valendo em todo texto, o validador acusa em `AGENTS.md`, pontes e `docs/**/*.md`, fora disso ninguem confere por script. Propagado.
- 2.8.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.
- T-060 ganhou dois itens vindos destas rodadas: agente chamado com stdin fechado, e o prompt dizendo que propagacao ao `AGENTS.md` e do agente de chat.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/docs/TASKS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/validate_structure.py`, `scripts/loop_task.py`, `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t071.py`, `evals/portao_t072.py`, `evals/fixtures/cobertura-tarefas/`.
- Projeto: `AGENTS.md` (core e marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. Aplicadas as de T-059 (texto) e T-061 (opcao c).

### Aprendizados Para MEMORY.md

- Nenhum novo. O stdin aberto e defeito de script (T-060), nao licao de processo.

### Pendencias

- Com T-069 a T-072 fechadas, o residuo de T-059 e T-061 acabou. Abertas: T-060 (loop, agora com quatro itens novos), T-062, T-063, T-064, T-073, e T-053 a T-058.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-060, que e o pacote do loop e ja tem quatro defeitos reproduzidos por comando.
- Motivo: e a unica tarefa aberta com risco de dado (modo 664 para 600, sub-linhas apagadas) e cada rodada de loop desde ontem esbarrou em um item dela.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-070, skill 2.7.0)

### Objetivo

- Fechar T-070 (dez checks AVISO decididos em T-059) pelo loop com o `terra`, e publicar a 2.7.0.

### O Que Foi Feito

- Pre-checagem da raiz contra os dez avisos novos (nenhuma violacao real; `T-1` e `(bloqueada:` aparecem so em prosa e sub-linha), portao proprio por comportamento (`evals/portao_t070.py`, onze casos mais controle, versao e verificador; falhava em 12 de 14), marcadores da raiz em v2.7.0 por script, tarefa refinada dizendo isso para o agente nao parar de novo para perguntar.
- **Loop verde na tentativa 1**, sem pergunta desta vez. Dez codigos novos, 53 no total; `CONVENCOES-DATA-INVALIDA` de INFO para AVISO; `CONSENSO-ABERTO-SEM-PROXIMO-PASSO` passou a exigir valor, nao so presenca. Bump para 2.7.0 propagado, raiz identica ao asset.
- **Revisao:** fixtures existentes ajustadas de forma legitima (`achado-project/valido` tinha rodada 5 com exposicao `nao`, que agora e aviso; `aguardando-project/invalido` ganhou casos e oracle). Tres consertos meus: `TASK_OWN_ID_RE` tinha virado exatamente tres digitos, o que faria `T-1000` deixar de ser ID e o loop nao achar a tarefa (agora tres ou mais); o paragrafo da 2.6.0 no `SKILL.md` foi substituido pelo da 2.7.0 em vez de acrescentado (restaurado); README da skill sem a 2.7.0 (acrescentado).
- Quatro mutacoes contra o verificador (cerca aberta, resposta ausente, formato de evidencia, adocao de volta a INFO): quatro pegas.
- 2.7.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t070.py`, `evals/fixtures/achado-project/valido/`, `evals/fixtures/aguardando-project/invalido/`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. "Tres digitos" da decisao de T-059 lido como "pelo menos tres": `T-1` e invalido, `T-1000` continua ID.

### Aprendizados Para MEMORY.md

- Nenhum novo. O padrao "refinar a tarefa com o que o agente vai perguntar" evitou a rodada perdida de T-069; e pratica, nao regra.

### Pendencias

- T-071 (texto do core), T-072 (diagnostico de parenteses), T-060 (loop) e T-073 (install.sh) abertas. Com T-069 e T-070 fechadas, das 17 promessas violaveis da REVAL-1/2 sobram as duas de texto (T-071).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-071 e T-072 juntas, que sao a proxima release (texto do core mais um ERRO).
- Motivo: fecham o residuo de T-059 e T-061 e cabem numa rodada so.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-069, skill 2.6.0)

### Objetivo

- Fechar T-069 (seis checks ERRO decididos em T-059) pelo loop com o `terra`, e publicar a 2.6.0.

### O Que Foi Feito

- **Portao proprio por comportamento** (`evals/portao_t069.py`): seis documentos errados montados de `assets/` precisam sair ERRO no arquivo certo, um projeto limpo precisa passar em `--strict`, versao acima de 2.5.1, verificador em exit 0. Falhava em 7 de 9. Sem ditar nome de codigo.
- **Rodada 1: exit 3, e era certo.** A tarefa manda propagar marcadores para o `AGENTS.md` da raiz e o prompt do loop proibe editar esse arquivo. O agente parou e perguntou em vez de decidir. Resposta operacional, pela regra do bloco de loop: quem edita `AGENTS.md` e o agente de chat. Marcadores da raiz postos em v2.6.0 por script antes da rodada 2, tarefa devolvida a fila.
- **Rodada 2: verde na tentativa 1.** Codigos novos `TASK-CONCLUIDA-SEM-DATA`, `VERIFICA-COMANDO-VAZIO`, `MARCADOR-ORDEM-INVALIDA`, `MARCADOR-LOOP-INVALIDO`, `NUCLEO-VAZIO`, `TASK-ID-ARQUIVADO-DUPLICADO`, cada um com fixture (o verificador exige desde T-065). Bump para 2.6.0 em `SKILL.md`, assets, partials e CHANGELOG; raiz byte a byte igual ao asset.
- **Revisao do que o terra escreveu, dois pontos:** (1) mudou a regex do marcador verifica para valer so no fim da linha, porque a resposta de T-059 na propria raiz mencionava `(verifica: )` em prosa e disparou o check novo. Defensavel (o core sempre disse "no fim da linha") e com bonus: comando com parenteses deixa de ser truncado e passa a ser recusado como "nao declarou". Mas nao estava no CHANGELOG; agora esta. (2) Satisfez a versao em prosa escrevendo uma frase nova e deixou a linha velha em 2.5.1: portao medindo o que sobrou. Corrigida a linha, e `verificar_versao` passou a exigir que **toda** ocorrencia bata e que a secao mais recente do CHANGELOG so cite a versao atual; provado por mutacao (prosa velha de volta reprova).
- `TASK-CONCLUIDA-SEM-DATA` so cobra linha com `T-NNN`: linha historica sem ID (fixture v1 e a raiz) continua tolerada, coerente com `TASKS-FORMATO-V1`.
- 2.6.0 reinstalada nos tres destinos globais, `diff -rq` limpo fora do nao distribuido, sem `__pycache__`.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t069.py`, `evals/fixtures/cobertura-arquivos/`, `evals/fixtures/cobertura-tarefas/`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. A regex do verifica no fim da linha aplica o texto do core que ja existia.

### Aprendizados Para MEMORY.md

- Portao com regex "existe uma ocorrencia certa" e satisfeito por uma frase nova ao lado da errada. Cobre "toda ocorrencia bate", nunca "alguma".

### Pendencias

- T-070 (AVISO), T-071 (texto do core), T-072 (diagnostico de parenteses) e T-060 (loop) seguem abertas para a proxima release. Duas sessoes de loop consecutivas geraram uma pergunta operacional cada; o prompt do loop poderia dizer que a propagacao ao `AGENTS.md` e do agente de chat, para nao gastar rodada com isso (nao virou tarefa: e frase em `loop.sh`, cabe em T-060).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-070, com portao proprio por comportamento, no mesmo molde de `portao_t069.py`.
- Motivo: e o par de T-069 e depende da mesma decisao, ja tomada.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-065)

### Objetivo

- Fechar T-065, o portao dos evals cego (REVAL-4), pelo modulo de loop com o Codex `terra`, a pedido do usuario.

### O Que Foi Feito

- **Portao proprio antes de rodar.** O marcador da tarefa apontava para `verify_repository.py`, que ja passava com 46 de 46: o loop fecharia a tarefa verde com trabalho zero. Escrito `evals/portao_t065.py`, que cobra o resultado (39 codigos com oracle, inventario de fixtures, manifesto de etapas, prompt assertado, versao em prosa) e falhava em 5 de 6; o marcador da tarefa foi trocado para ele.
- **Loop na T-065**, `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="high"`, degrau base, com `PYTHONDONTWRITEBYTECODE=1` no ambiente porque `loop_task.py check` gravou `__pycache__` na skill e derrubou o check novo. Portao verde na tentativa 1, ~12 minutos. O agente nao tocou em `TASKS.md` nem em arquivo de memoria; um patch caiu em caminho errado (`evals/` na raiz) e ele corrigiu sozinho.
- **Revisao do que o terra escreveu**: quatro fixtures `cobertura-*` com oracle exato (uma por area, acumulando `NUCLEO-AUSENTE` de proposito para ficar pequena), `TRAVESSAO` provado por token `{{TRAVESSAO}}` materializado so no temporario (repo continua sem U+2014), `ETAPAS` com despacho por nome, quatro assercoes de prompt em `test_loop.py`, e a versao em prosa do `SKILL.md` em `verificar_versao`. Duas lacunas fechadas por mim: `verificar_inventario_fixtures` (disco contra `FIXTURES`) e `verificar_etapas` (toda `verificar_*` definida esta em `ETAPAS`).
- **Prova por mutacao**: as 11 mutacoes que passaram cegas em 2026-09-03 (M1, M2, M3, M5, M8, M9, M10, M17, M19, M22, M23) refeitas contra o portao novo: **11 de 11 pegas**, cada uma nomeando o diagnostico ausente. Verificador de 46 para 58, bateria do loop de 58 para 62.

### Arquivos Criados Ou Alterados

- Skill (nao distribuidos): `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t065.py`, `evals/fixtures/cobertura-{arquivos,consenso,rotacao,tarefas}/`, `README.md`.
- Projeto: `docs/TASKS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. REVAL-4 fechada como `resolvido`; as sete entradas da revalidacao estao fechadas.

### Aprendizados Para MEMORY.md

- Portao que ja passa antes do trabalho nao e portao: o loop fecharia a tarefa verde com trabalho zero. Antes de mandar tarefa para o loop, rode o comando declarado; se sair 0, escreva um portao que falhe hoje.

### Pendencias

- T-060 ganhou o item do `__pycache__` do `loop_task.py`. `portao_t065.py` fica em `evals/` como registro; o que ele cobra agora vive no proprio verificador.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-069 e T-070 (checks novos), agora que cada codigo novo tem onde nascer com fixture; o loop serve, com portao proprio pelo mesmo motivo.
- Motivo: a decisao de T-059 esta tomada e o portao deixou de ser cego; e a hora de os checks entrarem.

## 2026-09-03 - Claude (respostas de T-059, T-061 e T-067)

### Objetivo

- Registrar as respostas do usuario a T-059, T-061 e T-067 e desdobrar em trabalho.

### O Que Foi Feito

- Usuario aceitou item a item a proposta de niveis de REVAL-1 (seis ERRO, dez AVISO, dois so texto). T-059 concluida com a resposta transcrita; decisao formal em `docs/DECISIONS.md`; REVAL-1, REVAL-2 e REVAL-6 fechadas como `resolvido`.
- Trabalho desdobrado por nivel: T-069 (ERRO), T-070 (AVISO), T-071 (texto do core). Os tres exigem versao 2.6.0 e dependem de T-065 para cada codigo novo nascer com fixture.
- T-061 respondida em seguida: opcao (c), parenteses no comando do marcador verifica nao sao suportados e o validador acusa (T-072), e `--seco` deixa de gravar `agente=` (item em T-060). REVAL-3 fechada como `resolvido`.
- T-067 respondida: `install.sh` avisa e pede confirmacao quando o destino diverge (T-073, sem bump). REVAL-7 fechada como `resolvido`. Das sete entradas, so REVAL-4 continua aberta, esperando T-065.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Em `docs/DECISIONS.md`: promessa do core sem check vira check com nivel declarado, ou texto honesto; codigo novo so entra com fixture.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma tarefa da revalidacao aguarda o usuario; sobra T-053 (spec 0006). Pela regra do bloco specs, T-065, T-069, T-070 e T-071 juntas mudam contrato e passam de tres tarefas: cabem numa spec 0007, se o usuario quiser.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, comecando por T-065 e depois T-069.
- Motivo: sem o manifesto de cobertura, os checks novos nasceriam com o mesmo ponto cego que a revalidacao acabou de achar.
