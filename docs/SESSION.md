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

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-054, T-056, T-058, T-055, skill 2.10.0)

### Objetivo

- Fechar as quatro tarefas tecnicas anteriores a revalidacao, pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- Duas traziam "decidir antes de consertar"; como o usuario mandou fazer, apliquei criterio ja decidido e deixei escrito na tarefa: **T-054** cobra `Rodada` ausente como AVISO pelo mesmo codigo dos campos irmaos e so apos a data de adocao (criterio de T-059), mais `fullmatch`; **T-058** implementa lock em vez de so documentar, porque documentar nao conserta. Se o usuario discordar, reverte antes do commit.
- Quatro portoes proprios por comportamento (`portao_t054/055/056/058.py`). O da T-058 nasceu com um traceback (a segunda rodada sem lock ficava presa esperando o agente e estourava o `timeout`); tratado como FALHA em vez de excecao. Os quatro reproduziam os defeitos antes das rodadas.
- **T-054** (bump 2.10.0): verde de primeira, fixture `rodada-project` com oracle para ausencia e para sufixo. **T-056**: `--progress` conta so bullet de primeiro nivel; a spec 0006 voltou a reportar 3 perguntas; etapa `verificar_progresso_de_specs` no verificador. **T-058**: `mkdir .loop-lock` atomico, exit 5 para a segunda rodada, `rmdir` no `trap`, mensagem ensina limpar orfao, caso na bateria (77), secao "Uma Rodada Por Projeto" em `loop.md`. **T-055**: os dois modelos cercados da raiz ficam identicos aos do template e o verificador cobra (71 de 71).
- **Registro honesto sobre T-055**: a tarefa exigia editar `docs/CONSENSUS.md`, que o prompt do loop proibe ao agente. O agente **editou mesmo assim** (6 linhas, exatamente os tres campos do modelo cercado, nada nas entradas reais). A culpa e da instrucao: eu mandei para o loop uma tarefa cuja unica saida era um arquivo proibido, e o texto da tarefa venceu o prompt. Duas licoes: tarefa que exige tocar arquivo proibido ao loop e do agente de chat, nao do loop; e a proibicao do prompt nao resiste a instrucao contraria na propria tarefa. A segunda e um achado sobre a forca real do prompt e vai para `MEMORY.md`.
- 2.10.0 reinstalada nos tres destinos com `--sim` (o instalador recusou sem ela, como desenhado).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/loop.sh`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t05{4,5,6,8}.py`, `evals/fixtures/rodada-project/`, `evals/fixtures/progresso-subitens/`.
- Projeto: `AGENTS.md` (marcadores), `docs/CONSENSUS.md` (modelos cercados), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. As duas escolhas de T-054 e T-058 estao declaradas nas tarefas e aqui, com a porta aberta para reverter.

### Aprendizados Para MEMORY.md

- A proibicao no prompt do loop nao resiste a uma tarefa que manda fazer o contrario: o agente editou `CONSENSUS.md` porque a tarefa dizia para editar. Tarefa que exige tocar arquivo proibido ao loop e trabalho do agente de chat.

### Pendencias

- Aberta so **T-053** (calibragens da spec 0006, do usuario). Todo o resto do backlog fechou: 15 tarefas em dois dias, sete releases (2.6.0 a 2.10.0), 54 codigos com fixture.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para T-053.
- Motivo: e a unica tarefa aberta, e destrava a spec 0006 (automacao do consenso), que e o proximo modulo.

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
