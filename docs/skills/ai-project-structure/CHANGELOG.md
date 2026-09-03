# CHANGELOG - skill ai-project-structure

Historico de versoes da skill. A versao canonica vive no frontmatter do `SKILL.md`.

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
- Regra explicita para escada desigual: degrau que nao existe na ferramenta escolhida nao vira degrau parecido em silencio. A skill diz qual e o teto daquela ferramenta e oferece trocar de ferramenta. Rebaixar calado faz o usuario achar que pediu esforco maximo e recebeu outra coisa.
- Perfis de execucao podem ter degraus de esforco (`executar`, `executar-dificil`, `executar-muito-dificil`). `references/loop.md` ganhou "Escolher O Nivel De Esforco": a skill propoe um degrau a partir de sinais reais e diz por que, em vez de escolher em silencio ou inventar rubrica. Na duvida entre dois, propoe o mais baixo.
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
