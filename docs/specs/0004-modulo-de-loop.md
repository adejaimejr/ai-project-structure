# Spec 0004 - Modulo de loop (skill 2.3.0)

**Status:** Definida
**Criada em:** 2026-09-02
**Definida em:** 2026-09-02 (apos o usuario responder P-1 a P-8; as respostas viraram DEC-001 a DEC-008)
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
- Em nenhum caminho o `loop.sh` escreve `Evidencia:` de tipo `revisao-manual` ou `conferencia`.
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

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
