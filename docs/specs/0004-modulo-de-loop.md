# Spec 0004 - Modulo de loop (skill 2.3.0)

**Status:** Concluida
**Criada em:** 2026-09-02
**Definida em:** 2026-09-02 (apos o usuario responder P-1 a P-8; as respostas viraram DEC-001 a DEC-008)
**Concluida em:** 2026-09-02
**Esforco:** M. Ficou M, e nao G, porque as respostas cortaram worktree, notificacao, teto de custo e automacao de consenso.

## Problema E Resultado Esperado

- Problema: hoje a estrutura descreve trabalho verificavel e nao executa nada. Quem roda o portao e a pessoa, turno a turno. Um projeto com `(verifica: <comando>)` declarado em tarefa aberta e com comando real em `QUALITY.md` ja tem tudo que um loop precisaria para trabalhar sozinho, e essa informacao fica parada.
- Problema: o parecer de 2026-09-02 mostrou por que o loop nao podia entrar na 2.2.0 (0003/DEC-003): no dia zero de um projeto scaffoldado nao existe suite de teste, e um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao. Isso continua verdade para projeto novo, e deixou de ser verdade para projeto maduro.
- Resultado esperado: um modulo opcional, ativado sob demanda em projeto que ja tem portao real, que pega uma tarefa elegivel, trabalha, roda o comando declarado, realimenta a falha e para. Fecha a tarefa apenas quando o comando comprova. Nunca no scaffold.
- Resultado esperado: um projeto que nao ativa o modulo nao paga nada por ele, nem em instrucao no bloco core, nem em arquivo.

## Escopo

### Incluido

- Modulo opcional no padrao do modulo de specs: `references/loop.md`, `assets/partials/AGENTS-loop-block.md`, marcadores `ai-project-structure:loop:start|end`, ativado sob demanda.
- Portao de ativacao: "Testes E Validacao" de `QUALITY.md` do projeto-alvo precisa ter comando real. Sem isso, a skill recusa e explica (0003/DEC-005).
- `scripts/loop.sh`: neutro, parametrizado pelo comando do agente. Uma tarefa por rodada, ate 3 tentativas, realimentando a saida da falha.
- Fecho de tarefa apenas com lastro de comando; tarefa travada por falta de contexto vai para `## Aguardando Usuario` com a pergunta escrita.
- `verify_repository.py` estendido para cobrir o bloco e o partial novos, como ja faz com `core` e `specs`.
- Versao da skill para 2.3.0 e marcadores dos tres blocos para v2.3.0.

### Fora Do Escopo

- Isolamento em worktree (DEC-005 desta spec).
- Notificacao de sistema (DEC-007 desta spec).
- Teto de custo e automacao do consenso (DEC-008 desta spec).
- Ativacao automatica ou por heuristica. A ativacao e sempre pedido explicito do usuario.
- Qualquer instrucao de loop no bloco `core`.
- Reescrita das convencoes da 2.2.0. O loop consome `(verifica:)`, `Evidencia:` e `Aguardando Usuario` como estao.

## Criterios De Aceite

Estrutura e nao contaminacao:

- Projeto sem o modulo ativado nao ganha nenhum arquivo, nenhum marcador e nenhuma linha no `AGENTS.md`.
- Scaffold minimal e scaffold completa continuam sem qualquer vestigio do modulo.
- Ativacao com "Testes E Validacao" vazio ou so com o texto do template e recusada, com a razao dita ao usuario.
- Ativacao com comando real insere o bloco `loop` entre o ultimo bloco gerenciado e "## Regras Do Projeto", em v2.3.0.
- `verify_repository.py` exige do bloco `loop` a mesma paridade que ja exige de `core` e `specs`, e retorna diferente de 0 com divergencia induzida.

Comportamento do `loop.sh`, verificavel com agente falso (um script que finge ser o agente):

- Tarefa sem `(verifica:)` e recusada antes de qualquer chamada de agente, com exit diferente de 0.
- Portao passa na primeira tentativa: a tarefa vai para `## Concluidas` com `Evidencia: tipo=comando`, `procedimento` com o comando declarado e `resultado` com a saida real. Exit 0.
- Portao falha nas 3 tentativas: a tarefa **nao** se move, nada de evidencia e escrito, o relatorio mostra as 3 saidas e o exit e diferente de 0.
- A saida da tentativa que falhou aparece no contexto passado a tentativa seguinte.
- Agente sinaliza falta de contexto: a tarefa vai para `## Aguardando Usuario` com `**Pergunta:**` preenchida, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)` do dia. Nenhuma evidencia e escrita. Exit diferente de 0.
- Em nenhum caminho o `loop.sh` escreve `Evidencia:` de tipo `revisao-manual` ou `conferencia`, nem entrada em `SESSION.md`, nem qualquer linha em `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` ou specs.
- Depois de qualquer rodada, `validate_structure.py <projeto> --strict` continua em exit 0.
- `--tentativas N` muda o numero de tentativas; o padrao e 3.
- Nenhum travessao (U+2014) em arquivo novo ou alterado.

## Decisoes

Herdadas da spec 0003, sem nova discussao:

- 0003/DEC-001: o marcador se chama `(verifica:)` e o loop o le como criterio de elegibilidade, sem renomear.
- 0003/DEC-003: o loop nunca entra no scaffold, mas o caminho de ativacao fica disponivel.
- 0003/DEC-005: a exigencia de comando real em `QUALITY.md` e pre-requisito de ativacao deste modulo, nao check do validador.

Desta spec, todas decididas pelo usuario em 2026-09-02:

- DEC-001 (P-4): o loop escreve na memoria **apenas o que o comando comprova**. Fecha tarefa so se ela declarou `(verifica:)` e o comando saiu 0, colando a saida real como `Evidencia: tipo=comando`. Nunca escreve `tipo=revisao-manual` nem `tipo=conferencia`. Motivo: sem isso, a evidencia passaria a ser escrita pela mesma coisa que ela deveria cobrar, que e o teatro de conformidade que o consenso da 0003 ja listou como risco. Impacto alem desta spec: copiada para `docs/DECISIONS.md`.
- DEC-002 (P-3): a execucao fica num `scripts/loop.sh` neutro, parametrizado pelo comando do agente (`--agente "claude -p"`, `--agente "codex exec"`, `--agente "gemini -p"`). Motivo: o projeto entrega para tres ferramentas e nada nele e acoplado a uma. O script vai em `scripts/` da skill, que e distribuido; isso nao esbarra em 0003/DEC-009, que proibia `scripts/` na raiz do repositorio.
- DEC-003 (P-1): uma tarefa por rodada, indicada no comando (`--tarefa T-042`). Motivo: menor blast radius e facil de abandonar. A ordem de `TASKS.md` nao vira contrato executavel.
- DEC-004 (P-2): a rodada para quando o portao passa ou apos 3 tentativas, o que vier primeiro. A cada falha, a saida do comando volta como contexto para a tentativa seguinte. Numero configuravel por flag. Motivo: a realimentacao da falha e a unica coisa que o loop faz melhor que a pessoa rodando na mao; sem ela nao ha razao para existir.
- DEC-005 (P-5): isolamento em worktree fica fora da 2.3.0. `references/loop.md` documenta a receita (`git worktree add`, e chamar o script la dentro). Motivo: criar, reescrever caminho, mesclar de volta e limpar e muito codigo no primeiro script serio do repositorio, a estrutura nem sempre vive em repositorio git, e a volta viraria merge no arquivo mais editado do projeto. Beneficio ja disponivel sem codigo novo.
- DEC-006 (P-6): falta de contexto move a tarefa para `## Aguardando Usuario` com a pergunta escrita. **Excecao explicita a DEC-001.** Motivo: DEC-001 protege contra alegacao de conclusao nao merecida, e registrar duvida e o oposto disso; o pior que essa escrita produz e uma pergunta boba, que a pessoa le e descarta. E a unica opcao que faz a pergunta sobreviver ao fim da rodada, que era o Problema 2 da spec 0003. Impacto alem desta spec: copiada para `docs/DECISIONS.md` junto com DEC-001.
- DEC-007 (P-7): o aviso de parada e o exit code mais o relatorio em stdout. Quem quiser som, notificacao ou webhook compoe por fora. Motivo: codigo por plataforma numa skill que roda em tres ferramentas e em tres sistemas nao se paga, e nao ha jeito honesto de verificar isso num eval.
- DEC-008 (P-8): teto de custo e automacao do consenso ficam fora da 2.3.0. Motivo: com DEC-003 e DEC-004, o custo ja esta limitado por construcao, e medir tokens de forma portatil nas tres ferramentas nao da. Automacao do consenso mexe em `CONSENSUS.md` e nos campos declarativos da 2.2.0, nao no ciclo de execucao: merece spec propria.
- DEC-010 (consequencia de DEC-001, registrada para nao ficar implicita): o loop tambem **nao escreve entrada em `SESSION.md`**. Uma entrada de sessao afirma o que foi feito, e nenhum comando comprova isso; o relatorio da rodada da o material para a pessoa escrever. Mesma razao exclui `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` e specs.
- DEC-017 (decidida pelo usuario em 2026-09-02, posterior a conclusao): o loop **continua sem registrar rodada que falhou**, mesmo sabendo que isso limita a escalada de esforco a uma unica conversa. Motivo: o custo de escrever tambem no fracasso e mudar o contrato do loop com o arquivo de memoria, que hoje e "so escreve quando o comando comprova conclusao", em troca de um ganho que aparece so em tarefa que falha e volta em outra sessao. Fica registrado que **isto nao e conflito com DEC-001**: fracasso de portao e fato com exit code, tao comprovado quanto sucesso, e poderia ser escrito sem ferir aquela decisao. Nao foi escrito por escolha de escopo, nao por impedimento. Consequencia obrigatoria: a skill nunca afirma "e a primeira rodada", porque nao tem como saber; ela diz que nao tem registro e deixa o usuario corrigir.
- DEC-016 (decidida pelo usuario em 2026-09-02, posterior a conclusao): a escolha de modelo, esforco e modo continua sendo do usuario e **nao entra na linha de tarefa**. Os perfis por intencao e ferramenta ficam em `docs/MEMORY.md`, secao `## User`, que ja e o lugar de preferencia de quem toca o projeto, e o agente do chat monta a chamada a partir deles. Motivo: por tarefa acoplaria o arquivo de memoria a string especifica de CLI, que muda sozinha; e dentro da skill exigiria manter catalogo de modelo de tres fornecedores. O `loop.sh` continua recebendo `--agente` e obedecendo, sem saber o que e perfil.
- DEC-015 (decidida pelo usuario em 2026-09-02, posterior a conclusao): a evidencia passa a registrar `agente=<comando>` antes de `procedimento=`. Motivo: a evidencia dizia que o portao passou e nao dizia quem produziu o trabalho. O loop sabe o comando com certeza, porque foi ele que invocou, entao registrar e fato e nao alegacao, o que respeita DEC-001. Sem isso, uma tarefa fechada meses atras nao tem como dizer com que ferramenta e modelo foi feita.
- DEC-014 (decisao de implementacao posterior a conclusao, 2026-09-02): agente que sai com codigo diferente de zero **e nao altera nenhum arquivo** encerra a rodada na hora, com exit 4, em vez de gastar as tentativas restantes. Motivo: a bancada multi-ferramenta mostrou dois casos reais (`codex exec` sem `--skip-git-repo-check` fora de repo git, e Gemini com conta inelegivel) em que o agente nunca executou e o loop insistiu tres vezes, rodando o portao a toa e reportando "portao falhou" quando o problema era o comando de `--agente`. Agente que falha mas mexeu em arquivo continua seguindo para o portao: trabalho parcial existe e quem julga e o portao.
- DEC-011 (decidida pelo usuario em 2026-09-02, ao implementar T-020): o agente sinaliza falta de contexto **escrevendo a pergunta no arquivo `.loop-pergunta`** na raiz do projeto, nao imprimindo uma linha sentinela no stdout. Motivo: cada uma das tres ferramentas formata a saida de um jeito, e nenhuma garante que o modelo emita uma string exata; arquivo existe ou nao existe. O `loop.sh` procura o arquivo depois de cada tentativa, antes de rodar o portao, e o remove depois de registrar a pergunta.
- DEC-012 (decidida pelo usuario em 2026-09-02, ao implementar T-020): toda edicao de `docs/TASKS.md` passa por `scripts/loop_task.py`, que importa `validate_structure.py` e reusa o parser dele. Motivo: `TASKS.md` e a memoria do usuario, e dois parsers do mesmo arquivo divergem com o tempo. O que o loop entende por secao, ID e marcador passa a ser, por construcao, o que o validador entende. O shell fica so com orquestracao.
- DEC-013 (decisao de implementacao, nao veio de pergunta): o campo `resultado` da evidencia recebe o exit code mais a saida real com espacos colapsados, e saida longa e cortada **pelo comeco**, preservando o fim. Motivo: a evidencia e uma sub-linha e saida multi-linha nao cabe nela; suite de teste costuma imprimir o placar no fim. O corte fica declarado dentro do proprio campo, para nao virar resumo silencioso.
- DEC-009 (decisao de implementacao, nao veio de pergunta): os marcadores dos tres blocos passam a v2.3.0 juntos, mesmo que o conteudo de `core` e `specs` nao mude. Motivo: o marcador diz qual versao da skill escreveu aquele bloco, e `verify_repository.py` ja exige que todos batam com o `SKILL.md`. A alternativa, deixar marcadores em versoes diferentes no mesmo arquivo, exigiria afrouxar essa checagem, que hoje pega drift de verdade. O fluxo de atualizacao vai mostrar um diff de uma linha nesses casos; e ruido pequeno e honesto.

## Tarefas

- T-019: bloco de loop, partial, marcadores v2.3.0 e fluxo de ativacao com o portao de QUALITY.md
- T-020: scripts/loop.sh neutro
- T-021: verify_repository.py cobrindo o bloco novo, e versao 2.3.0 coerente
- T-022: evals e fixtures do modulo
- T-023: dogfood no proprio repositorio

## Perguntas Abertas

- (Vazio. As oito perguntas do Rascunho foram respondidas pelo usuario em 2026-09-02 e viraram DEC-001 a DEC-008.)

## Evidencia De Conclusao

- Verificacao: `python3 docs/skills/ai-project-structure/evals/verify_repository.py`
- Resultado: exit 0, 33 de 33 verificacoes, incluindo "bloco loop identico ao partial da skill" (caminho ativado, depois do dogfood), "bateria do modulo de loop: 47/47", os tres scripts distribuidos compilando e os tres destinos identicos.
- Verificacao: `python3 docs/skills/ai-project-structure/evals/test_loop.py`
- Resultado: 47 de 47, cobrindo os quatro caminhos do `loop.sh` (tarefa sem portao, portao verde, portao vermelho ate esgotar com a realimentacao conferida no prompt da tentativa seguinte, e falta de contexto) e os tres subcomandos do `loop_task.py`. Sem nenhuma chamada de modelo.
- Rodada real: `loop.sh --tarefa T-025 --agente "codex exec -s workspace-write"` neste repositorio, com portao que falhava antes (`git check-ignore -q .loop-pergunta`, exit 1) e passou depois. O loop fechou T-025 com `Evidencia: tipo=comando; resultado=exit 0`, e o Codex reportou que nao tocou em `docs/TASKS.md` nem escreveu evidencia: a regra do bloco foi obedecida por um modelo que nao participou desta implementacao.
- Bancada multi-ferramenta (2026-09-02, depois da conclusao): subprojeto real e identico para cada agente, com duas tarefas. T-001 bem especificada, T-002 deliberadamente sem contexto, num caso em que chutar passaria no portao.
- Resultado de T-001: Claude, Codex e Grok fecharam com portao verde na tentativa 1.
- Consumo de T-001: Claude 5,5k de entrada, 3,1k de saida e 295k de cache read em 6 turnos e 52s; Grok 193.401 tokens; Codex 23.958 tokens. O JSON do Claude reporta USD 1,04 com `"costBasis": "list"`, e o do Grok reporta USD 0,25 sem declarar base. **Esses valores sao preco de tabela da API, derivados dos tokens, e nao o que se paga em assinatura.** Sob assinatura eles medem consumo de plano; comparar ferramentas por eles compara tabela de preco, nao custo real.
- Confusor da bancada: nenhum modelo foi fixado. Cada CLI usou o proprio padrao (Claude em `claude-fable-5-1`, Codex em `gpt-5.6-terra` com reasoning effort `high`, Grok em `grok-4.6`), entao a comparacao entre ferramentas mistura ferramenta, modelo e esforco.
- Resultado de T-002, o teste mais duro do desenho: os tres escreveram `.loop-pergunta` e pararam, em vez de chutar. As tres perguntas registradas eram precisas e diferentes entre si. A regra "Nunca Inferir" sobreviveu a pressao de que chutar sairia de graca.
- Limitacao conhecida: Gemini CLI nao pode ser exercitada nesta maquina. A conta cai em `IneligibleTierError`, com o free tier do Gemini Code Assist descontinuado para este cliente. Nao e limitacao do modulo.
- Limitacao conhecida, mais importante: duas das tres ferramentas entregaram implementacao com bug numa regra de borda que a suite do subprojeto nao cobria, e o loop fechou as duas com evidencia legitima. A evidencia prova que o comando passou, nao que o trabalho esta correto. Registrado em `references/loop.md`.
