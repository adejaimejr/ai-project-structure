# CHANGELOG - skill ai-project-structure

Historico de versoes da skill. A versao canonica vive no frontmatter do `SKILL.md`.

## 2.5.0 - 2026-09-03

Portao que so olha exit code nao prova nada. Esta versao troca isso por diagnostico com identidade. Veio da revalidacao do achado `0005-A1` pelo Codex, registrada em `docs/CONSENSUS.md` do repositorio-fonte.

- **Identificador estavel por diagnostico.** Os 39 diagnosticos de `validate_structure.py` ganharam codigo (`ACHADO-SEM-ESCAPOU`, `TASK-ID-DUPLICADO`, `SPEC-STATUS-INVALIDO`, e assim por diante). O codigo e **contrato publico**: a redacao da mensagem pode melhorar quando quiser, o codigo so muda em mudanca de versao. Quem monta portao em cima do validador casa codigo, nunca fragmento de texto.
- **Flag `--codigos`**: uma linha por diagnostico, `NIVEL|CODIGO|ARQUIVO|SUJEITO`, sem prosa. O `SUJEITO` e a tarefa, a entrada de consenso ou a spec de que o diagnostico fala, e e ele que denuncia aviso que passou a cair na entrada errada.
- O relatorio humano passa a mostrar o codigo entre colchetes: `[AVISO] [ACHADO-SEM-ESCAPOU] ...`. `Report.add` recusa codigo que nao esteja declarado em `CODIGOS`, entao diagnostico sem identidade quebra na hora de escrever, e nao em producao.
- **Oracle por fixture no `verify_repository.py`** (so no repositorio-fonte). O `FIXTURES` deixou de mapear nome para exit code e passou a declarar modo, exit esperado e o **conjunto exato** de diagnosticos. Diagnostico a mais reprova tanto quanto diagnostico a menos, e fixture sem oracle declarado e recusada em vez de virar aprovacao silenciosa. `verificar_achado` foi absorvida por esse mecanismo: um mecanismo, nao dois.
- Efeito medido por mutacao: com a contagem de linhas antiga, uma regressao compensada (um aviso certo some, outro errado aparece, total igual) passava verde. Com o conjunto exato, ela reprova nomeando o que sumiu e o que sobrou. Aviso que muda de entrada, mesmo com codigo e contagem identicos, tambem reprova.

## 2.4.0 - 2026-09-03

`CONSENSUS.md` deixa de servir so para debate e passa a registrar **achado**, que e o que o uso real produziu. Desenho e decisoes na spec `docs/specs/0005-consenso-para-achados.md` do repositorio-fonte.

- **Formato de achado** no bloco core e no template de `CONSENSUS.md`. Entrada que declara `**Achado:** <identificador>` e tratada como achado, com `Status` e `Proximo passo` proprios, disposicao de quem registrou e revalidacao por outro modelo. O identificador e livre, amarrado a unidade de trabalho do projeto: o validador confere que o campo existe e tem valor, e nunca opina sobre o valor.
- **`**Escapou de verificacao:** sim | nao`** no achado, e a secao `Por Que Nada Pegou Antes` obrigatoria quando a declaracao for `sim`, com o que passou verde e o mecanismo do ponto cego. E o que transforma defeito escapado em conserto de portao, em vez de anedota.
- **O teto de tres rodadas saiu.** Ele foi escrito sem evidencia, e o uso real chegou a sete revalidacoes numa unidade so sem que isso fosse fracasso. No lugar dele, da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`, dizendo o que a anterior deixou em aberto. O proposito original, evitar rodada por cerimonia, sobrevive na exigencia de justificar a continuidade.
- **Aviso do ponto cego da validacao cruzada no bloco core**, em duas linhas: rodada verde e ausencia de objecao, nao prova de que funciona. Antes ele so existia em `references/loop.md`, que quem usa consenso sem usar loop nunca le.
- `validate_structure.py`: checks novos do formato de achado, todos AVISO e todos opt-in. A entrada opta pelo formato ao declarar `**Achado:**`, entao projeto que nunca registra achado nao recebe nenhuma cobranca nova, e entrada de debate segue valendo como esta. A regra de rodada trocou de dono: acima de tres, o que se cobra deixou de ser `**Proximo passo:**` e passou a ser `**Pendente da rodada anterior:**`.
- Fixture `evals/fixtures/achado-project`, com par valido e invalido. A primeira entrada dos dois e a mesma entrada de debate, de proposito: e o controle que prova que nenhum aviso novo encosta em quem nao declarou achado. Como os checks sao AVISO, a fixture roda em `--strict`, senao os dois casos sairiam 0 e nao provariam nada.
- Marcadores dos tres blocos gerenciados atualizados para v2.4.0.

## 2.3.0 - 2026-09-02

Modulo de loop: a estrutura passa a poder executar uma tarefa verificavel, nao so descreve-la. Desenho e decisoes na spec `docs/specs/0004-modulo-de-loop.md` do repositorio-fonte.

- **Modulo opcional de loop**, no padrao do modulo de specs: `references/loop.md`, `assets/partials/AGENTS-loop-block.md` e marcadores `ai-project-structure:loop:start|end`. Ativado so a pedido explicito, nunca no scaffold.
- **Portao de ativacao**: a secao "Testes E Validacao" de `QUALITY.md` do projeto-alvo precisa ter comando executavel. Vazia ou com o texto do template, a ativacao e recusada.
- **Limite do que a automacao escreve**: o loop fecha tarefa apenas quando ela declarou `(verifica: <comando>)` e o comando saiu 0, colando a saida real como `Evidencia: tipo=comando`. Nunca escreve `tipo=revisao-manual` nem `tipo=conferencia`, e nao toca `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` nem specs. Excecao unica: falta de contexto move a tarefa para `Aguardando Usuario` com a pergunta escrita.
- `scripts/loop.sh`: orquestra uma rodada. Uma tarefa, ate 3 tentativas, com a saida do portao voltando como contexto da tentativa seguinte. Exit codes distintos por caminho (0 fechou, 1 nao elegivel, 2 portao falhou, 3 aguardando usuario).
- `scripts/loop_task.py`: toda edicao de `TASKS.md` passa por aqui, reusando o parser do `validate_structure.py`. Um parser so no projeto, em vez de dois divergindo.
- Protocolo de falta de contexto por arquivo (`.loop-pergunta`), nao por linha sentinela no stdout: cada ferramenta formata saida de um jeito, e arquivo existe ou nao existe.
- `evals/test_loop.py`: 47 verificacoes do modulo com agente falso, sem nenhuma chamada de modelo. Roda em segundos e entrou no `verify_repository.py`, que passou a conferir tambem o bloco `loop`, o bit de execucao do `loop.sh` e se os tres scripts distribuidos compilam.
- Exit 4 novo: agente que sai com codigo diferente de zero e nao altera nenhum arquivo encerra a rodada na hora, em vez de queimar as tentativas restantes. Veio de bancada real, onde duas ferramentas mal configuradas fizeram o loop insistir tres vezes e reportar "portao falhou" quando o problema era o comando de `--agente`.
- `references/loop.md` ganhou a tabela de comandos por ferramenta (Claude, Codex, Gemini e Grok), as duas armadilhas que custam uma rodada (`--skip-git-repo-check` no Codex fora de repo git, `--skip-trust` no Gemini) e a secao "A Evidencia Vale O Que O Portao Vale".
- A evidencia escrita pelo loop passa a registrar `agente=<comando>`: quem fechou a tarefa, nao so que o portao passou.
- Chamada assistida: `SKILL.md` ganhou "Rodar Uma Tarefa Com O Loop". O usuario pede em linguagem natural e o agente do chat monta o comando, lendo os perfis por intencao e ferramenta que ficam em `docs/MEMORY.md`, secao `## User`. Nome de modelo e flag de esforco nunca entram na skill: eles envelhecem, e a memoria do projeto e o lugar deles.
- Revisao item a item do bloco, com o criterio da DEC-018: regra vai para o prompt quando a violacao dela deixa o portao verde do mesmo jeito. Achou um buraco: nada impedia o agente de editar `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `DECISIONS.md` ou specs, e o pior caso e afrouxar em `AGENTS.md` a regra que o restringe. Entrou no prompt. O que ficou so no bloco, e por que, esta documentado em `references/loop.md`.
- A restricao "nao apague o que falha" entrou **no prompt** do `loop.sh`, e nao so no bloco. Bancada mostrou que um modelo mais barato ignorava a regra quando ela vivia so no `AGENTS.md`, e passou a obedecer quando ela chegou pelo prompt. Regra cuja violacao passa despercebida no portao nao pode morar so no bloco.
- Mensagem do exit 4 deixou de acusar causa errada: antes afirmava que o comando de `--agente` estava incompleto, e numa bancada a causa real foi cota do plano da ferramenta. Agora aponta a saida do agente e lista as duas causas comuns.
- Regra nova no bloco de loop, vinda de bancada com projeto de conteudo: **nao apague o que falha**. O portao mede o que sobrou, entao remover o teste, a secao ou o link que falha sempre deixa o portao verde. Quando a saida obvia for perder conteudo ou cobertura, o agente para e pergunta pelo `.loop-pergunta`, porque perder informacao e decisao do usuario e o verde fica igual nos dois casos.
- A escolha de degrau deixou de estimar dificuldade lendo a tarefa. Sobra o que se sustenta em evidencia: rodada anterior falhou, duas falharam, ou o usuario disse que e dificil.
- Regra explicita para escada desigual: degrau que nao existe na ferramenta escolhida nao vira degrau parecido em silencio. Duas saidas valem, uma nao. Vale usar o teto da ferramenta quando o usuario ja decidiu isso e esta escrito no perfil, avisando que e o teto; vale dizer qual e o teto e oferecer trocar de ferramenta. Nao vale escolher o degrau parecido sem falar nada: o usuario acharia que pediu esforco maximo e recebeu outra coisa.
- Perfis de execucao podem ter degraus de esforco (`executar`, `executar-dificil`, `executar-muito-dificil`). `references/loop.md` ganhou "Escolher O Nivel De Esforco": comeca sempre no degrau base e sobe so por sinal declarado, dizendo qual foi. Escalada por fracasso de rodada anterior, por pedido do usuario, ou por tarefa que mexe em varias partes com regra de borda. Explicitamente **nao** sao sinais: portao ser suite, tarefa pertencer a spec, ou descricao longa, porque disparam em quase todo trabalho real e nao separam nada.
- `references/loop.md` ganhou "Configurar Os Perfis": fluxo conversacional para ver, trocar e criar perfil, com a regra de confirmar nome de modelo e nivel na propria CLI antes de gravar.
- Marcadores dos tres blocos gerenciados atualizados para v2.3.0. Eles andam juntos mesmo quando o conteudo de um bloco nao muda, porque o marcador diz qual versao da skill escreveu aquele bloco.

## 2.2.0 - 2026-09-02

Tarefa concluida deixa de ser afirmacao em prosa: passa a carregar evidencia. Espera por resposta do usuario ganha lugar proprio. Consenso passa a declarar como foi produzido. Ver a spec `docs/specs/0003-tasks-verificaveis.md` do repositorio-fonte.

- **Evidencia de fechamento obrigatoria** em toda tarefa movida para "Concluidas", como sub-linha `Evidencia: tipo=; procedimento=; resultado=`. `tipo` aceita `comando`, `revisao-manual` ou `conferencia`, para que tarefa de conteudo ou de decisao nao precise inventar comando.
- **Marcador `(verifica: <comando>)` opcional** em tarefa aberta. Declarado, vira contrato: concluir sem registrar o resultado daquele comando e ERRO no validador.
- **Nao retroativo.** A data de adocao fica declarada no proprio `TASKS.md`, no marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)`. Sem o marcador, nada e cobrado; linha concluida antes da data fica como esta. Projeto que atualiza nao tem historico transformado em alegacao sem evidencia.
- **Secao `## Aguardando Usuario`** no template de `TASKS.md`, com `**Pergunta:**`, `**Resposta:**` e `(bloqueada: AAAA-MM-DD)`. A regra "Nunca Inferir" do bloco core agora aponta para ela: pergunta que trava a tarefa tem destino, em vez de virar inferencia. Sem rotacao; aviso quando passa de 30 dias.
- **Consenso declarado**: `**Metodo:**`, `**Exposicao previa a outras posicoes:**` e `**Rodada:** N de 3` no template de `CONSENSUS.md` e no bloco core, com regra de rodada 1 cega e teto de 3 rodadas antes de escalar para o usuario. Os campos sao autodeclarados: o validador checa presenca e valor, nunca veracidade.
- `validate_structure.py`: checks novos de evidencia, `(verifica:)` sem resultado, `Aguardando Usuario` sem pergunta, valor desconhecido em marcador conhecido, idade do bloqueio e campos de consenso. `--progress` passa a contar a secao nova.
- `evals/verify_repository.py` (so no repositorio-fonte): prova em um comando a integridade do meta-projeto (raiz em `--strict`, fixtures, paridade dos blocos gerenciados e das pontes, convencoes nos templates e no dogfood, coerencia de versao, `evals.json`, ausencia de travessao e paridade dos tres destinos com `install.sh` em pasta temporaria).
- Fixture nova `evals/fixtures/aguardando-project` (caso valido exit 0, caso invalido exit 1) e eval 9 correspondente.
- Correcao achada no dogfood do mesmo dia: o validador tratava **qualquer** `T-NNN` da linha como ID da tarefa, entao uma tarefa que cita outra ("continuando o que sobrou de T-001") era acusada de ID duplicado, e uma linha concluida que mencionasse outro ID marcava esse outro como concluido, o que podia dar spec "Concluida" por engano. Agora vale o ID que abre a linha, depois da data quando ela e concluida; o resto do texto e referencia. A fixture `aguardando-project` guarda a correcao.
- Marcadores dos blocos gerenciados atualizados para v2.2.0.

## 2.1.0 - 2026-08-20

- Novo template opcional `docs/STACK.md`: mapa de tecnologias, pacotes principais e links de documentacao oficial, com secao "Onde Consultar Primeiro" para o agente ir direto na fonte certa (inspirado no STACK.md/PACKAGES.md do specsfy).
- `AGENTS.md` (bloco core): STACK.md em "Onde Escrever Cada Coisa" e gatilho novo em "Atualizacao Por Gatilho" (mudou tecnologia ou pacote, atualize STACK.md).
- `validate_structure.py --progress`: projecao somente-leitura de tarefas e specs (contagem por secao, status por spec, tarefas concluidas/total, perguntas abertas). Nunca edita nada (licao do specsfy-progress).
- Marcadores dos blocos gerenciados atualizados para v2.1.0.

## 2.0.0 - 2026-08-20

Inspirada na analise da skill/metodologia `specsfy` (github.com/promovaweb/specsfy), adaptando o que serve ao nosso contexto de memoria multiagente e descartando a cerimonia pesada (coverage math, attestation, pipeline multi-skill, CLI).

- Entrevista numerada com opcoes numeradas no scaffold; "Avançar" adia e registra pendencia, nunca autoriza inferencia.
- Regra "Nunca Inferir" no template `AGENTS.md`.
- `TASKS.md` com IDs `T-NNN`, prioridade opcional e link `(spec: NNNN-slug)`.
- Blocos gerenciados em `AGENTS.md` (`ai-project-structure:core` e `:specs`) + fluxo de atualizacao v1→v2 em `references/atualizacao.md`.
- Validador `scripts/validate_structure.py` (Python 3, stdlib, exit code).
- Modulo opcional de specs em `docs/specs/` (flat, `NNNN-slug.md`, status no arquivo, anti-drift: status de tarefa so em `TASKS.md`). Fluxos em `references/specs.md`.
- Campo `version` no frontmatter do `SKILL.md`; versao tambem gravada nos marcadores do projeto-alvo.
- `install.sh` passa a copiar `scripts/` e `references/`.
- Regra de escrita no template `AGENTS.md`: travessao (em dash, U+2014) proibido em textos do projeto; o validador acusa qualquer ocorrencia como erro.
- Correcao: `assets/docs/README.md` separava errado nucleo e opcionais (ARCHITECTURE e PROMPTS listados como nucleo).
- Correcao no mesmo dia, apos a rodada de validacao: o `expected_output` do eval 4 nao dizia o que esperar do validador depois da entrevista, e ferramentas diferentes leram o cenario de formas diferentes (uma parou na entrevista e viu exit 1 por diretorio vazio, outra respondeu e viu exit 0). Ambas estavam certas. O texto agora explicita que o criterio do eval e o comportamento da entrevista, que exit 1 em diretorio vazio nao reprova, e como exercitar o ramo "Avançar" ate exit 0. Muda apenas `evals/`, que o `install.sh` nao propaga; nao exige reinstalacao.

Ponto de atencao para versoes futuras: a instrucao sobre specs vive em dois lugares com papeis distintos - bloco `specs` em `AGENTS.md` (regra) e `docs/specs/README.md` (modelo). Atualizacoes precisam manter os dois coerentes.

## 1.x - ate 2026-05-26

- 2026-04-25: estrutura criada e refinada (MEMORY.md, archive/, reescrita do AGENTS.md).
- 2026-05-26: empacotamento como skill instalavel cross-tool (Agent Skills Open Standard), `install.sh`, `README.md`, `agents/openai.yaml`; instalacao verificada em Claude Code, Codex CLI e Gemini CLI.

Historico detalhado do projeto em `../../CHANGELOG.md` (docs/CHANGELOG.md do repositorio).
