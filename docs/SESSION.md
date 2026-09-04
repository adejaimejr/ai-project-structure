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
