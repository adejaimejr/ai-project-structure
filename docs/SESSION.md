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

## 2026-10-17 - Claude (passagem de trabalho entre gestor e subagentes)

### Objetivo

- Dar a estrutura um protocolo leve de passagem de trabalho entre um agente gestor e seus subagentes no Cloudroom, usando a skill Handoff (davidondrej) como referencia de metodo, sem copia-la nem exigir a instalacao dela. Restricoes do pedido: nenhum documento permanente novo, subagente nao le a skill inteira, o resumo leva so o contexto da tarefa e funciona com os agentes em sandboxes diferentes.

### O Que Foi Feito

- Leitura: `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `TASKS.md`, `SKILL.md`, `references/atualizacao.md` e `loop.md`, o prompt do `loop.sh`, o envelope do `consenso.py`, `verify_repository.py` e as referencias do `room-cli` sobre sandboxes (filho Cloud de pai Local tem sandbox propria e parte do GitHub).
- Diagnostico: a estrutura nao tinha regra de delegacao. O unico envelope de passagem existente e o prompt do `loop.sh`, que ja carrega tarefa, portao, saida da falha anterior e proibicoes, mas pressupoe filesystem compartilhado. O principio ja escrito em `loop.md` ("regra critica vai no prompt, nao so no bloco") e o mesmo que vale aqui: o que o subagente precisa chega na mensagem, porque ler arquivo e opcional e arquivo temporario de outra sandbox nem existe.
- Mudanca minima: secao `## Passagem De Trabalho` no bloco core de `AGENTS.md` (assets e raiz), entre "Memoria Persistente" e "Consenso Entre Modelos": 19 linhas, 1362 bytes. Um paragrafo com a premissa (outra sandbox; o resumo viaja na mensagem; `docs/` segue como registro e o resumo aponta para ele), um modelo de cinco linhas (tarefa e criterio de conclusao, estado feito e pendente, decisoes e tentativas a nao repetir, arquivos a consultar por caminho, conferir o estado real antes de agir) e quatro bullets (estado em vez de ordens; so o contexto da tarefa, sem repetir regras nem colar `docs/`; sem segredo; retorno pelo mesmo canal e registro por quem delegou). Validador intocado: o resumo vive na mensagem, nao em arquivo, e nenhum script o ve.
- Sem bump: item na secao 2.11.0 do CHANGELOG da skill, como nas duas sessoes anteriores, porque T-078 a T-083 mandam nao subir a versao. Custo dessa escolha: a 2.11.0 publicada no GitHub (`origin/main` igual a `main`) passa a ter dois conteudos de bloco core, e o passo 2 de `atualizacao.md` encerrava em versao igual sem olhar o bloco. Conserto de uma linha no passo 2: versao igual e bloco diferente do template segue para o passo 4 so com aquele bloco, com diff e confirmacao. O bump virou T-086.
- Verificacao: `verify_repository.py` 74/74 antes e depois; `validate_structure.py . --strict` 0 erros e 0 avisos; scaffold minimal montado dos assets em pasta temporaria passa em `--strict` com a secao dentro; zero travessao e cercas pareadas no bloco core. Mutacoes com backup por `cp` e volta conferida por `cmp`: secao removida so dos assets, verificador 73/74 ("bloco core identico" falha); travessao dentro da secao nos dois arquivos, 70/74 (strict da raiz, as duas baterias e o check de travessao). Reinstalada nos tres destinos com `install.sh --sim`, paridade por `cmp`.
- `SESSION.md` passaria de 30KB: as duas entradas mais antigas (2.10.0 com T-054, T-056, T-058 e T-055; 2.9.1 com T-062 e T-073) foram para `docs/archive/SESSIONS-2026.md`, indice atualizado (46 entradas). A primeira rotacao, de uma entrada so, deixou o arquivo em 31KB e o validador avisou `ROTACAO`.

### Arquivos Criados Ou Alterados

- Skill: `assets/AGENTS.md` (secao nova no core), `references/atualizacao.md` (passo 2), `CHANGELOG.md` (item na 2.11.0).
- Projeto: `AGENTS.md` (mesma secao), `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md` (T-086), `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.
- Instalacao: `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`.

### Decisoes Tomadas

- Contexto de delegacao viaja na mensagem, nunca em arquivo temporario nem em documento novo; `docs/` segue como registro. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum. A premissa do Cloudroom (subagente em outra sandbox) ficou escrita no proprio `AGENTS.md`, onde todo agente a le.

### Pendencias

- T-086: bump da skill levando a secao, para o fluxo de atualizacao oferecer o bloco a projeto ja em 2.11.0 e para a 2.11.0 publicada nao ter dois conteudos; depende de T-078 a T-083 liberarem o "nao suba", ou vai junto com T-084.
- Cloudroom, fora deste repositorio: continua pendente, da sessao anterior, o template de delegacao do gestor para a skill (nomear a estrutura e pre-responder a entrevista); a secao nova cobre a parte geral.
- Do usuario: commitar.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para mandar T-078 ao loop com o verificador verde; o gestor no Cloudroom passa a delegar com o resumo da secao nova.
- Motivo: a secao nao bloqueia nada; T-078 e a proxima da spec 0006 e o verificador esta verde.

## 2026-10-17 - Claude (T-085: fixture aguardando-project com data relativa)

### Objetivo

- Fechar T-085: `verify_repository.py` em 71/74 porque a fixture `aguardando-project` tinha `(bloqueada: 2026-09-01)` absoluto e o validador compara com `date.today()` (limite 30 dias). Envelhecimento, nao regressao: validador e fixture intocados desde setembro. Bloqueava os portoes de T-078 a T-083, que rodam o verificador pela base `portao_consenso_lib.py`.

### O Que Foi Feito

- Portao antes do conserto: `evals/portao_t085.py`, molde de `portao_t058.py`, 9 checks. Com a data real saiu 3/9 pelo motivo certo (tres datas absolutas; verificador sem `materializar_fixture`; 71/74).
- Solucao (b) da tarefa, so em `evals/`, sem bump: token `{{HOJE-N}}` na fixture, materializado em pasta temporaria por `materializar_fixture(origem, destino, hoje)` em `verify_repository.py`, que absorveu as trocas de `{{TRAVESSAO}}` e `{{UTF8_INVALIDO}}`. `valido` e `invalido` usam `{{HOJE-7}}`; `invalido` ganhou T-007 com `{{HOJE-45}}`, bloqueada antiga de proposito, e `TASK-BLOQUEADA-ANTIGA|T-007` entrou no oracle (ate aqui so `cobertura-tarefas`, com 2000-01-01, produzia o codigo). `validate_structure.py` intocado: em projeto real o check segue relativo a hoje. README da fixture explica o token.
- Opcao (a), data de referencia no validador, descartada: toca `scripts/`, exige bump e reinstalacao, e T-078 a T-083 mandam nao subir a 2.11.0 nao commitada.
- Depois: portao 9/9, verificador 74/74, raiz `--strict` com 0 erros e 0 avisos, sem `__pycache__`.
- Mutacoes, backup por `cp` e volta conferida por `cmp`: data absoluta de volta em `valido`, 6/9 (1a, 1b, 3d; verificador 72/74); `hoje` forcado para daqui a um ano no verificador, 6/9 (1c, 2a, 3d; 73/74); para um ano atras, 6/9 (1b, 2b, 3d; 71/74). O parametro `hoje` existe so para o portao viajar no tempo pela mesma funcao do verificador.

### Arquivos Criados Ou Alterados

- Skill, nao distribuidos: `evals/portao_t085.py` (novo), `evals/verify_repository.py`, `evals/fixtures/aguardando-project/README.md`, `valido/docs/TASKS.md` e `invalido/docs/TASKS.md` da mesma fixture.
- Projeto: `docs/TASKS.md` (T-085 concluida), `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Nenhuma formal. Escolha de implementacao dentro da tarefa: fixture relativa em vez de flag no validador.

### Aprendizados Para MEMORY.md

- Confirmado o candidato da sessao anterior: fixture com data absoluta sob check relativo a `date.today()` envelhece sozinha e derruba o verificador sem regressao; data que o validador compara com hoje entra na fixture como token relativo, materializado no teste. Nao promovido aqui: `MEMORY.md` fora do escopo pedido.

### Pendencias

- Promover o aprendizado acima para `MEMORY.md`.
- CHANGELOG da skill (secao 2.11.0) sem item desta mudanca: `evals/` nao e distribuido e o escopo pedido nao o incluia; decidir se entra.
- Do usuario: commitar (2.11.0 inteira, gatilhos e T-085 seguem nao commitados).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para mandar T-078 ao loop com o verificador verde.
- Motivo: a causa alheia dos portoes vermelhos saiu; o que falhar agora e da propria tarefa.

## 2026-10-17 - Claude (gatilhos da skill para o fluxo gestor e subagentes no Cloudroom)

### Objetivo

- Revisar os gatilhos da skill `ai-project-structure` para o uso no Cloudroom, onde um agente gestor coordena subagentes em sandbox: o gestor decide quando um projeto precisa da estrutura, os subagentes so a executam quando recebem essa tarefa, e o pedido direto do usuario continua valendo. Analise e proposta antes de qualquer edicao, a pedido do usuario; aplicacao depois da aprovacao.

### O Que Foi Feito

- Leitura: `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `SKILL.md`, `agents/openai.yaml`, `evals.json`, `install.sh`, `verify_repository.py` (so checa `version` no frontmatter, nunca a `description`) e as referencias do `room-cli` (skills chegam aos agentes pelos roots globais `~/.claude/skills` e `~/.agents/skills`; `.bb/AGENTS.md` na raiz do workspace injeta instrucao em toda thread).
- Diagnostico: a `description` do frontmatter e a unica superficie de roteamento, e a skill nao sabe quem a chama; a tarefa do gestor chega ao subagente como se fosse o pedido do usuario. As frases genericas ("cria projeto", "inicia projeto novo", "scaffold projeto", "estrutura inicial", "monta a base do projeto", "cria a pasta do projeto", "projeto de IA") faziam um subagente mandado fazer scaffold de codigo abrir a entrevista ou criar `AGENTS.md` e `docs/` sem pedido, tirando a decisao do gestor. Os gatilhos especificos (estrutura multiagente, atualizar, validar, specs, loop) nao conflitam.
- Proposta aprovada e aplicada: `description` reescrita com clausula positiva estreita (nomear a estrutura ou seus arquivos, citar a skill, fluxos de atualizar, validar, specs e loop) e clausula negativa (pedido generico nao dispara; quem coordena decide; no maximo oferecer a estrutura em uma linha). Escalar YAML plano, sem `": "` nem travessao; Claude Code releu a skill com o texto novo na mesma sessao. Comentario do `openai.yaml` atualizado, `allow_implicit_invocation` segue `true`. Eval 2 passa a nomear a estrutura no prompt; eval 4 ("Inicia projeto novo aqui.") passa a esperar oferta e confirmacao antes da entrevista; eval 11 novo, negativo (projeto Node com Vite nao aciona). Item na secao 2.11.0 do CHANGELOG da skill, sem bump: a 2.11.0 nao foi commitada e T-078 a T-083 pedem para nao subir; os portoes aceitam "2.11.0 ou acima".
- Casos ambiguos decididos com o usuario: "inicia projeto novo" sozinho sai dos gatilhos (custa um turno de confirmacao no chat direto); "scaffold projeto" e "estrutura inicial" saem por casarem com scaffold de codigo; "projeto de IA" e "repo de IA" saem porque projeto sobre IA nao e projeto para varias IAs. Travas mecanicas (`allow_implicit_invocation: false` no Codex, `disable-model-invocation` no Claude Code, esta a confirmar na documentacao) rejeitadas por exigirem invocar a skill pelo nome e quebrarem o pedido direto em linguagem natural.
- Verificacao: `validate_structure.py . --strict` sem problema; frontmatter com tres chaves; zero travessao nos quatro arquivos. `verify_repository.py` em **71/74**: as tres falhas sao `TASK-BLOQUEADA-ANTIGA` na fixture `aguardando-project` (`valido` em `--strict` e as contagens exatas de `valido` e `invalido`), porque o validador compara `(bloqueada:)` com `date.today()` e as datas de setembro da fixture passaram do limite. Nada a ver com esta mudanca: validador e fixture intocados desde 2026-09-04. Virou T-085, prioridade alta, porque `portao_consenso_lib.py` roda o verificador e toda rodada de loop de T-078 a T-083 ficaria vermelha por causa alheia.
- Reinstalada nos tres destinos com `install.sh --sim` (divergencia listada em cada um: `SKILL.md` e `agents/openai.yaml`); paridade conferida por `cmp` nos dois arquivos, nos tres destinos.
- Rotacao: `SESSION.md` passaria de 30KB com esta entrada; as tres entradas mais antigas (2.9.0 com T-064 e T-063, 2.8.1 com T-060, 2.8.0 com T-072 e T-071) foram para `docs/archive/SESSIONS-2026.md`, indice do archive atualizado (44 entradas).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md` (description), `agents/openai.yaml` (comentario), `evals/evals.json` (evals 2, 4 e 11), `CHANGELOG.md` (item na 2.11.0).
- Projeto: `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md` (T-085), `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.
- Instalacao: `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`.

### Decisoes Tomadas

- Gatilho da skill nao decide se um projeto ganha a estrutura; quem coordena decide. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum promovido. Candidato ainda em hipotese: fixture com data absoluta sob check relativo a `date.today()` envelhece sozinha e derruba o verificador sem regressao real; vira regra se T-085 confirmar o conserto.

### Pendencias

- T-085 (fixture `aguardando-project` envelhecendo; verificador em 71/74) antes de qualquer rodada de loop de T-078 a T-083.
- Do usuario: commitar. A 2.11.0 inteira continua nao commitada, e esta sessao soma a mudanca de gatilhos.
- Cloudroom, fora deste repositorio: linha em `.bb/AGENTS.md` do workspace repetindo a regra, e template de delegacao do gestor nomeando a estrutura e pre-respondendo as quatro perguntas da entrevista (nome, objetivo, minimal ou completa, specs), para o subagente nao travar perguntando ao gestor.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente de chat, para T-085 antes de mandar T-078 ao loop; portao proprio escrito antes da rodada.
- Motivo: verificador vermelho por causa alheia esconde regressao real, e todos os portoes abertos passam por ele.

## 2026-09-04 - Claude, com Grok cursor-grok-4.6-high pelo loop (plano da spec 0006, T-075 a T-077, skill 2.11.0)

### Objetivo

- Desdobrar a spec 0006 (automacao do consenso), `Definida` com DEC-001 a DEC-010 e sem tarefa, em tarefas que cabem numa rodada de loop, cada uma com portao proprio, sem escrever codigo do produto.
- Depois da aprovacao do plano, a pedido do usuario: rodar T-075, T-076 e T-077 pelo loop (a ultima virou a madrugada de 2026-09-05).

### O Que Foi Feito

- Leitura na ordem pedida: `AGENTS.md`, a spec inteira, as quatro rodadas de loop mais recentes, `MEMORY.md` (Feedback e Project), `DECISIONS.md` de 2026-09-03 e 2026-09-04, `loop.sh` e `loop_task.py`, `references/loop.md`, e as entradas de P-7/P-8 e P-9 do archive. Plano mostrado e aprovado pelo usuario **antes** de gravar qualquer coisa.
- **Leitura da spec:** o primitivo e um orquestrador mecanico novo, `scripts/consenso.py`, que roda N agentes em paralelo, cada um numa copia propria do projeto sem `docs/consensus/`, e grava bruto e manifesto em `docs/consensus/<run-id>/` assim que cada agente termina; os pacotes em cima sao a minuta de debate (citacao linha a linha, julgamento em branco, atomica sob lock), a varredura de segredo, o achado (revalidacao dentro da entrada existente), a rodada 2 com anteriores na integra, a retomada por comando e os checks AVISO por `**Origem:**`. Do `loop.sh` reaproveita-se o contrato, nao o codigo.
- **Escolhas de forma, dentro das DECs e vetaveis antes da primeira rodada:** campos `**Origem:** automacao`, `**Manifesto:**`, `**Participantes:**` (todos os ids) e `**Falhas:**` (`nenhuma` ou ids); headings `### Posicao De <id>`, `### Falha De <id>` e `### Revalidacao De <id>`; `Metodo` sempre `pareceres-independentes` (nenhum modo mostra posicao contemporanea); `--pendente` obrigatorio da rodada 4 em diante, porque o campo e julgamento humano; sidecar em `docs/consensus/`, copias com `.git` e sem o sidecar; sem bloco gerenciado novo em `AGENTS.md`.
- **Nove tarefas, T-075 a T-083**, em "Proximas Tarefas" de `docs/TASKS.md` por script com substituicao atomica, na ordem de execucao e com dependencia dita na linha: primitivo (bump 2.11.0), lock e minuta, segredo, validador com fixture, achado, rodada 2, retomada, documentacao (portao sem `verify_repository.py`, porque a raiz precisa da propagacao do agente de chat), bancada real (tarefa do agente de chat, com evidencia `revisao-manual`). Cada linha diz o que e proibido ao loop e o que sobra para o chat. T-IDs listados na spec sem status; a spec segue `Definida` ate a primeira rodada, como combinado.
- **Nove portoes** sobre uma base comum, `evals/portao_consenso_lib.py` (molde de `portao_t058.py` mais agente falso, chamada do orquestrador e leitura do sidecar), cada um com regex autotestada contra exemplo e contraexemplo. Rodados hoje, **todos falham pelo motivo certo** (`scripts/consenso.py` ausente, versao 2.10.0, `test_consenso.py` ausente, sem run dir, sem secao no `SKILL.md`): T-075 1/14, T-076 1/13, T-077 0/10, T-078 6/14, T-079 1/12, T-080 0/11, T-081 0/11, T-082 2/8, T-083 1/4. O que passa hoje e o que deve continuar passando (raiz limpa, controle sem diagnostico, verificador).
- Dois consertos no proprio trabalho antes de qualquer verificacao: `portao_t076.py` nasceu com o travessao literal (trocado por `\u2014` escapado, regra de `MEMORY.md`); e o regex de perfil de `portao_t083.py` casava a nota do `cursor-agent` em `MEMORY.md`, que cita Codex, consenso e read-only na mesma frase, e foi apertado para a forma `- Codex, consenso:` com esse contraexemplo real no autoteste.
- `SESSION.md` passou de 30KB com a entrada nova: quatro entradas rotacionadas para o archive (T-070 e 2.7.0, T-069 e 2.6.0, T-065, respostas de T-059/T-061/T-067), indice do archive corrigido (41 entradas). Linha no CHANGELOG do projeto.
- **Rodada 1 de T-075 com Codex `gpt-5.6-terra`: morreu na cota.** 82.683 tokens na tentativa 1 e `You've hit your usage limit` (volta em 2026-09-05 02:18); tentativas 2 e 3 recusadas na hora; portao 3/14 nas tres, exit 2, nada movido. Sobrou um `consenso.py` parcial com `SyntaxError` (um `+` de patch meio aplicado). Nenhum arquivo de memoria tocado. Os marcadores da raiz estavam de volta em 2.10.0 antes de o loop comecar (o verificador passou 71/71 dentro da tentativa 1; a reversao veio de fora do loop, provavelmente do `sed` que eu mesmo tinha oferecido) e foram repostos.
- **Rodada 2 de T-075 com Grok pelo `cursor-agent` (`-p --force --model cursor-grok-4.6-high`), escolhido pelo usuario entre quatro opcoes: verde na tentativa 1**, em cerca de 8 minutos, no mesmo degrau base (cota nao e sinal de dificuldade). `scripts/consenso.py debate` com copias por agente (`copytree` sem `docs/consensus/`, `.consenso-lock` e `__pycache__`), `ThreadPoolExecutor` para o paralelo, bruto e manifesto gravados no `as_completed` de cada agente, manifesto por substituicao atomica, retencao de `## Registros` com nota, envelope de prompt com os seis itens do contrato, `git check-ignore` para o sidecar ignorado, ids validados contra `/` e `..`. Bateria `evals/test_consenso.py` com 13 checks (espelha o portao e importa a base `portao_consenso_lib.py`), etapa `verificar_testes_do_consenso` com piso 12, `consenso.py` compilado no verificador, bump 2.11.0 em `SKILL.md`, assets, partials e CHANGELOG da skill. `AGENTS.md` da raiz intocado. Portao 14/14; verificador de 71 para 74.
- **Revisao do que o Grok escreveu, sem conserto necessario:** `--titulo` e aceito e ainda nao usado (e de T-076); o envelope diz "copia somente-leitura" enquanto a copia e gravavel, o que e o desenho (isolamento por copia, nao por permissao); `run-id` com resolucao de segundo e recusa de duplicata; `.git` vai na copia, como a tarefa manda. Consumo nao impresso pelo `cursor-agent`. 2.11.0 reinstalada nos tres destinos com `--sim`, paridade limpa fora do nao distribuido.
- **T-076 com o mesmo perfil do Grok, verde na tentativa 1** (portao 13/13, uns 6 minutos), lancada depois de conferir que o portao falhava contra o `consenso.py` real (sem `--dono`, sem lock, sem sinal, sem minuta, bateria em 13, verificador acusando travessao sob `docs/consensus/`). O que entrou: `.consenso-lock` por `mkdir`, exit 5 com a mensagem do orfao, `soltar_lock` em `finally`; handler de SIGINT e SIGTERM que encerra os agentes vivos e leva a rodada a `status=interrompida` com exit 1, sem tocar em `CONSENSUS.md`; minuta no fim do arquivo por `escrever_bytes_atomico` (temporario, `fsync`, `os.replace`), na forma da tarefa, com `citar` pondo `> ` em toda linha e trocando U+2014 por hifen com `travessoes_substituidos` no manifesto; bloco `minuta` com os hashes e so entao `concluida`. Bateria de 13 para 24 (lock, SIGTERM, injecao, minuta), piso 24, `verificar_travessao` ignorando `docs/consensus/`, item no CHANGELOG 2.11.0. `AGENTS.md` da raiz intocado.
- **Revisao de T-076, sem conserto:** tres checagens redundantes de `_interrompendo` no caminho final (inofensivas); a interrupcao sai com exit 1, que a lista de exit codes do plano nao previa; anotado na linha de T-082 para a tabela dizer isso. Verificador 74/74, loop 77/77, consenso 24/24, `--strict` limpo, portao 13/13 de novo, sem sobras.
- **T-077 com o Grok: o trabalho ficou pronto em uns 8 minutos e o `cursor-agent` ficou preso por quase duas horas.** O log mostra seis `Connection lost, reconnecting`; o processo `node` morreu, o wrapper ficou vivo sem filho, e o `loop.sh` esperou, porque nao tem timeout de agente. Evidencia antes de agir: ultimo arquivo tocado as 22:41, `pgrep -P` vazio, e o portao rodado a mao contra o que ficou ja em 10/10. `kill -TERM` no wrapper; o loop viu exit 143 com arquivos alterados, rodou o portao (10/10) e fechou T-077 na tentativa 1. Licao promovida para `MEMORY.md`; o timeout no `loop.sh` virou **T-084**.
- **O que entrou em T-077:** `tem_segredo` com sete regex (AWS, PEM, rotulo com valor de 16+, `ghp_`, `sk-`, `xox`, URL com senha), aplicada a pergunta antes de chamar qualquer agente (exit 6 sem run dir) e a stdout e stderr de cada agente antes de gravar; bruto retido em `tempfile.mkdtemp("consenso-retido-")` com `stdout.txt` e `stderr.txt`, manifesto com `retido-por-segredo` e `retido_em` sem conteudo, `status=parada-segredo`, exit 6, mensagem ensinando mover ou apagar e `retomar`. Bateria 24 para 31, piso 30, CHANGELOG.
- **Um ajuste meu, provado por mutacao:** `sk-[A-Za-z0-9_-]+` casava `task-force`, `risk-based` e `desk-top` (conferido no interpretador), e nem o portao nem a bateria cobriam o prefixo. Regex dos tres prefixos com inicio de palavra e comprimento minimo (`\bsk-[A-Za-z0-9_-]{16,}`, idem `ghp_` 16 e `xox?-` 8), dois casos novos na bateria (chave `sk-` real dispara; `task-force`, `risk-based` e `desk-top` nao), piso 32, bateria 33/33. Efeito colateral meu no meio: um `import consenso` no interpretador gravou `scripts/__pycache__`; removido.

### Arquivos Criados Ou Alterados

- Skill, por mim (nao distribuidos): `evals/portao_consenso_lib.py`, `evals/portao_t075.py` a `evals/portao_t083.py`.
- Skill, pelo Grok nas rodadas de T-075, T-076 e T-077 (com o ajuste do `sk-` por mim): `scripts/consenso.py` (novo, distribuido), `evals/test_consenso.py` (novo), `evals/verify_repository.py`, `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`.
- Projeto: `AGENTS.md` (marcadores em 2.11.0), `docs/TASKS.md`, `docs/specs/0006-automacao-do-consenso.md` (T-IDs e `Em andamento`), `docs/SESSION.md`, `docs/MEMORY.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/` (README e quatro logs), `docs/CHANGELOG.md`. `docs/PROMPTS.md` ja estava alterado pelo usuario com o prompt desta sessao e nao foi tocado.

### Decisoes Tomadas

- Nenhuma formal. As escolhas de forma acima estao escritas nas tarefas, nao em `DECISIONS.md`, porque sao implementacao dentro das DECs; o usuario aprovou o plano sem veta-las. A spec 0006 passou a `Em andamento` com o fecho de T-075.

### Aprendizados Para MEMORY.md

- Promovido em `MEMORY.md`, secao User: o `cursor-agent -p` pode terminar o trabalho e ficar preso em reconexao sem sair; os sinais que separam isso de trabalho lento, e a saida (`kill -TERM` no wrapper, o loop deixa o portao decidir).
- Promovido em `MEMORY.md`, secao User, com sobrescrita ativa: a primeira rodada de loop completa do Grok neste projeto aconteceu hoje, pelo `cursor-agent` com `cursor-grok-4.6-high`, verde na tentativa 1 em cerca de 8 minutos, quando a cota do Codex acabou. Junto, a observacao que decidiu a troca: falha por cota nao e sinal de dificuldade, entao troca-se a ferramenta e mantem-se o degrau.
- O regex que casou a linha errada em T-083 e a regra ja registrada (regex de portao testada contra exemplo) aplicada com um contraexemplo tirado do arquivo real; nada novo.

### Pendencias

- T-078 a T-083 abertas, nessa ordem, mais T-084 (timeout de agente no `loop.sh`, fora da spec, sem portao ainda). T-078 (validador) e a proxima. Antes de T-083: rotacionar `docs/CONSENSUS.md` (30186 de 30720 bytes) e registrar os perfis `Codex, consenso` e `Grok, consenso` em `MEMORY.md` com o usuario.
- Codex `gpt-5.6-terra` sem cota ate 2026-09-05 02:18. Ate la, o loop roda com o Grok pelo `cursor-agent` ou com outro perfil que o usuario escolher.
- Do usuario: commitar. Plano e rodada estao juntos na arvore, separaveis por arquivo: do plano, `evals/portao_*` e os arquivos de `docs/`; da rodada, `scripts/consenso.py`, `evals/test_consenso.py`, `verify_repository.py`, `SKILL.md`, assets e CHANGELOG da skill.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente de chat, para mandar T-078 ao loop (Grok pelo `cursor-agent` no degrau base, ou Codex `terra` se a cota voltou), rodando `portao_t078.py` contra o validador atual antes de lancar. Vigiar o log: se parar em `Retry attempt N` sem arquivo tocado por muito tempo, e o caso de `MEMORY.md`, nao trabalho lento.
- Motivo: T-078 e independente do script e fecha a DEC-007 no validador; T-079 (achado) depende de T-077, que acabou de fechar, e pode ir em seguida.


## 2026-09-04 - Claude (respostas de T-053 e T-074)

### Objetivo

- Registrar as respostas do usuario a T-053 (posicao do Grok nas tres calibragens) e a T-074 (opcao a para o segredo no bruto), e levar a spec 0006 a `Definida`.

### O Que Foi Feito

- DEC-007 (forma entra no escopo, diagnosticos novos como AVISO), DEC-008 (proveniencia com manifesto ao lado e ponte curta) e DEC-009 (retomada sempre humana, bruto in-repo desde o inicio) escritas na spec com a forca de cada uma; copiadas para `docs/DECISIONS.md`; as duas entradas de consenso no archive fechadas como `resolvido`.
- A quarta pergunta, segredo no bruto versionado, ficou primeiro como P-10 e T-074 com tres opcoes esbocadas; o usuario escolheu a (a) em seguida: varredura de padroes antes de gravar, rodada para e pede palavra humana, nunca redige. DEC-010 na spec com as alternativas rejeitadas, criterios de aceite reescritos para DEC-007 a DEC-010, decisao copiada para `docs/DECISIONS.md`. **Spec 0006 passou a `Definida`**, sem pergunta aberta.

### Arquivos Criados Ou Alterados

- `docs/specs/0006-automacao-do-consenso.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/archive/CONSENSUS-2026.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- DEC-007 a DEC-010 da spec 0006, pelo usuario; resumo em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma tarefa aberta. O proximo trabalho e planejar a implementacao da spec 0006 (criar as tarefas dela), que ainda nao tem nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para desdobrar a spec 0006 em tarefas com portao, e o usuario para aprovar o plano antes da primeira rodada.
- Motivo: a spec esta `Definida` com dez decisoes e nenhuma tarefa de implementacao; e trabalho tamanho-feature e merece plano antes de codigo.
