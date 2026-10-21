# Spec 0008 - Adaptador Cloudroom: subagente visivel como agente do loop

**Status:** Rascunho
**Criada em:** 2026-10-21
**Nota de status:** o usuario decidiu em 2026-10-21 manter `Rascunho` ate outro modelo avaliar a spec, antes de implementar.
**Revisao:** Codex `gpt-6-luna`, em 2026-10-21, pela thread filha `cr_child_b0709855d0672dc1fec76ac7` (so leitura). Tres achados: o mock aceita `--request-id` e o portao T-100 nao barrava flag extra (o `--request-id` existe na CLI real, conferido sem abrir filho, entao o mock ficou; o check 4a passou a recusar qualquer flag fora de DEC-003 e DEC-006); os checks de limites do portao T-102 aceitavam palavra solta (passaram a exigir o sentido na mesma frase, com autoteste e contraexemplo, e a mutacao com texto ao contrario reprova); P-D aberta (nao aplicado: segue aberta ate o usuario ratificar a entrada de consenso). Veredito do revisor: falta isso para `Definida`.
**Esforco:** M, porque e um script novo distribuido mais bateria, documentacao e bump, sem mexer em `loop.sh` nem em `consenso.py`; o que pesa e provar o comportamento sem gastar modelo e fechar com uma bancada real.

## Problema E Resultado Esperado

- Problema: na bancada real de T-083 (2026-10-21, sandbox Cloudroom), o `consenso.py` chamou `codex exec` como processo filho. Nada apareceu na barra de threads do Cloudroom, o sandbox read-only do Codex nao rodou no container (Armadilha em `docs/MEMORY.md`) e o usuario nao tinha como acompanhar log, estado ou custo. Os subagentes Sonnet das outras tarefas, abertos por `room-cli thread spawn --shared-sandbox`, ficaram visiveis, com log e estado. O mesmo vale para o `loop.sh`: hoje o agente de uma rodada de loop e sempre um processo invisivel.
- Hipotese de partida (do prompt de planejamento): um wrapper que se comporte como CLI headless (prompt como ultimo argumento, resposta no stdout, exit code do agente) encaixa em `consenso.py` e `loop.sh` sem tocar neles.
- O que a leitura do codigo e as sondas na CLI real (cloudroom 0.1.67, 2026-10-21) mostraram: a hipotese **vale para o `loop.sh` e cai para o `consenso.py`**. O loop so precisa que o agente mexa no projeto e saia; o filho em `--shared-sandbox` faz isso no mesmo sistema de arquivos. O consenso precisa que cada participante rode na propria copia (0006/DEC-003), e nenhum dos dois modos do `room-cli` entrega isso de forma verificavel (DEC-002 e DEC-003 abaixo).
- Resultado esperado: `scripts/cloudroom_agente.py`, distribuido pela skill, que transforma um filho do Cloudroom em agente headless para o `--agente` do `loop.sh`; o loop roda visivel na barra do Cloudroom, sem mudar uma linha de `loop.sh`, e o `consenso.py` continua com CLIs chamadas direto, com o motivo escrito.

## Escopo

### Incluido

- `scripts/cloudroom_agente.py`: python3 so com biblioteca padrao, sem `sed -i`, `perl`, `timeout(1)` nem `setsid`.
- `room-cli` falso em `evals/mock_room_cli.py` (nao distribuido), que imita a CLI real como respondeu nas sondas: spawn imediato com JSON, resposta cortada sem `--all`, filho de sandbox propria ilegivel, `stop` e `archive`.
- Bateria `evals/test_cloudroom_agente.py` com etapa e piso em `verify_repository.py`, cobrindo o adaptador sozinho e o `loop.sh` de ponta a ponta com o filho falso.
- `references/cloudroom.md` (uso, exit codes, limites), linha na tabela de ferramentas de `references/loop.md`, nota em `references/consenso.md`, mencao no `SKILL.md`, bump e secao no CHANGELOG da skill.
- Perfil `Cloudroom, executar:` em `docs/MEMORY.md` e uma bancada real com modelo escolhido pelo usuario (parte do agente de chat).

### Fora Do Escopo

- **Usar o adaptador como participante do `consenso.py`** (debate ou achado). Motivo em DEC-002 e DEC-003. Reabrir exige spec propria e uma forma verificavel de prender o filho na copia.
- Qualquer mudanca em `loop.sh` ou `consenso.py`: nenhum dos dois importa, detecta ou chama `room-cli` (decidido antes desta spec).
- Filho em sandbox propria (sem `--shared-sandbox`), `--top-level` e `--machine cloud`.
- Thread Local (Mac): o adaptador nao foi exercitado la; fica dito nos limites (DEC-007).
- Escolher modelo ou provider por padrao: os dois vem por flag, do usuario.
- Fallback para outra ferramenta quando `room-cli` falta: nada degrada em silencio.

## Criterios De Aceite

Verificaveis por comando:

- `portao_t100.py` 17/17: o adaptador sozinho contra o `room-cli` falso (sem `room-cli` no PATH sai 1 antes de qualquer chamada; resposta integral no stdout, inclusive acima de 2000 caracteres; `--shared-sandbox` e `--prompt-file` acrescentados por ele; filho falho sai 2; SIGTERM vira `thread stop` em ate 5 s e exit 143; titulo; `--arquivar`; flags proibidas recusadas; prompt acima de 262144 bytes recusado).
- `portao_t101.py` 6/6: bateria com ao menos 20 verificacoes no verificador, `loop.sh` fechando uma tarefa com o adaptador como `--agente` e `--tempo-maximo` parando o filho.
- `portao_t102.py` 14/14: documentacao, limites (inclusive `--projeto` so na pasta da thread), bump coerente, `install.sh` distribuindo o script, sem travessao, `--strict` limpo.
- Nenhuma bateria nem portao chama o `room-cli` real: o falso vem primeiro no PATH, e o cenario "sem `room-cli`" usa PATH vazio, porque o real mora em `/usr/local/bin` na sandbox.
- `verify_repository.py` em exit 0 e `validate_structure.py . --strict` com 0 erros e 0 avisos.

Julgados na mao:

- Bancada real (`portao_t103.py` confere so a forma): uma rodada de `loop.sh` com o adaptador e modelo escolhido pelo usuario, com `--projeto` igual a pasta da thread, fecha uma tarefa verde, o arquivo que o filho escreveu e conferido no sistema de arquivos dentro de `$PROJETO` (caminho e mtime posterior ao inicio da tentativa, nao o relato do modelo), a thread filha aparece na barra do Cloudroom com o titulo da tarefa, e a evidencia cita o id `cr_child_...`.

## Decisoes

- **DEC-001 (P-1, como o adaptador bloqueia e recupera a resposta):** `spawn` com `--shared-sandbox --prompt-file <temporario>` (prompt inteiro em arquivo, sem limite de argv nem problema de aspas; o teto de 262144 bytes e da CLI, e o adaptador repassa a mensagem dela com exit 1), depois polling de `room-cli thread output ID --all` a cada `--intervalo` segundos (padrao 10) ate `busy` falso. `state` ocioso com `reply`: imprime a resposta integral mais uma quebra de linha e sai 0. `error` preenchido ou estado de falha ou parada: stderr com o erro do filho, stdout vazio, exit 2. O adaptador nao tem timeout proprio: quem limita e o `--tempo-maximo` do loop. Filho que pergunta em vez de responder sai 0 com a pergunta no stdout; o adaptador nao distingue, e o loop ja manda gravar a pergunta em `.loop-pergunta`. Sem `--all`, a CLI corta a resposta em cerca de 2000 caracteres com o aviso `[... reply truncated ...]` (sonda de 2026-10-21). Rejeitadas: esperar a mensagem que o Cloudroom manda ao pai quando o filho termina (chega para o agente de chat, nao para um processo, entao o wrapper nao a enxerga) e responder perguntas do filho por `thread tell` (no loop nao ha ninguem para responder).
- **DEC-002 (P-2, `--shared-sandbox` e o consenso; ratificada pelo usuario em 2026-10-21 depois da rodada de consenso):** o filho roda na pasta da thread pai, nao na pasta corrente de quem o chamou: a sonda de 2026-10-21 (filho `cr_child_0fd8860dd542df3fb95f7b70`, pedido para imprimir `pwd`) respondeu `/code/ai-project-structure`, e o `spawn` nao tem opcao de diretorio ("Other options are refused, not ignored"). Para o consenso, a copia por participante sobreviveria so como caminho no prompt, e a 0006/DEC-003 rejeitou isolamento por pedido de cegueira. Pior: o filho le o projeto real, onde o `consenso.py` grava o bruto de cada participante assim que ele encerra (0006/DEC-009), entao o segundo participante alcanca a posicao do primeiro. O verificavel aqui e negativo: nenhum perfil de consenso aponta para o adaptador, e `references/consenso.md` diz por que. Rejeitada: o adaptador fazer `cd` na copia e repassar o caminho (o filho nao herda o `cd`; seria isolamento por prompt com outro nome).
- **DEC-003 (P-3, sandbox propria e o modo de cada pacote; ratificada pelo usuario em 2026-10-21 depois da rodada de consenso):** filho sem `--shared-sandbox` ganha id `thr_...`, nao aparece em `thread list` e `thread output` devolve so a nota "Its replies arrive as messages when its turns end" (sonda de 2026-10-21). O adaptador nao consegue esperar nem coletar a resposta, entao o modo esta fora para os tres pacotes. Mesmo que coletasse, a copia do filho leva `docs/CONSENSUS.md` inteiro e `docs/consensus/`, que a rodada 1 cega retem (0006/DEC-003), e o trabalho dele fica em outra branch, longe do portao do loop. Decisao: loop roda em `--shared-sandbox`, que o adaptador acrescenta sempre; debate e achado nao usam o adaptador. `--top-level`, `--prompt` e `--prompt-file` vindos de fora sao recusados com exit 1; o adaptador aceita so `--provider` (obrigatorio), `--model`, `--reasoning-level`, `--service-tier`, `--titulo`, `--arquivar` e `--intervalo`, e recusa o resto, como a propria CLI.
- **DEC-004 (P-4, "mexeu em arquivo" e `--tempo-maximo`):** os dois mecanismos do `loop.sh` continuam valendo, **mas so quando o `$PROJETO` do loop e a pasta da thread do Cloudroom**. O filho em `--shared-sandbox` comeca nessa pasta e escreve no mesmo sistema de arquivos, entao o `find -newer` enxerga o trabalho. Correcao de 2026-10-21, levantada pelos dois participantes da rodada sobre P-2 e P-3 sem um ver o outro (`docs/CONSENSUS.md`, entrada "Spec 0008, P-2 e P-3") e aceita pelo usuario: a sonda de `pwd` prova so o diretorio inicial do filho, nao que ele escreva num `--projeto` arbitrario; a redacao anterior prometia isso por causa do caminho absoluto no prompt, que e instrucao e nao garantia. O adaptador nao promete outro `--projeto`, e `references/cloudroom.md` diz isso nos limites. No estouro, o loop manda SIGTERM ao grupo; o adaptador trata SIGTERM e SIGINT chamando `room-cli thread stop ID` e sai 143 em ate 5 s, antes do SIGKILL do loop. Limite aceito: SIGKILL nao se trata, e o filho seguiria vivo; por isso o id sai no stderr desde o spawn, para quem precisar parar a mao. Rejeitada: mudar o `loop.sh` para conhecer o filho (quebra a decisao de agnosticismo).
- **DEC-005 (P-5, registro):** o manifesto do consenso nao se aplica (DEC-002). No loop, a evidencia ja grava `agente=` com o comando integral, que cita `cloudroom_agente.py`, provider e modelo; o adaptador escreve `thread=<id>` no stderr, que entra no relatorio da rodada. O bruto continua sendo o stdout do adaptador, igual a qualquer CLI. Nenhum link e montado: o Cloudroom nao documenta formato de URL de thread.
- **DEC-006 (P-6, visibilidade e limpeza):** titulo por `--titulo`; sem ele, `loop T-NNN` quando o prompt traz um ID de tarefa (o do `loop.sh` sempre traz); senao a primeira linha do prompt, ate 80 caracteres. Uma thread por tentativa, entao uma rodada de loop abre de 1 a `--tentativas` threads. Arquivar e opt-in por `--arquivar`, depois da ultima leitura: o padrao e deixar a thread para o usuario conferir, que e o motivo do recurso.
- **DEC-007 (P-7, Local e Cloud):** o adaptador nao detecta onde roda; chama `room-cli` e acrescenta `--shared-sandbox`. Exercitado so em thread Cloud. Em thread Local o comportamento de `--shared-sandbox` nao foi conferido, e `--machine cloud` fica recusado porque cai no problema da DEC-003 (sandbox propria a partir do GitHub). `references/cloudroom.md` diz isso nos limites. Rejeitada: detectar Local pelo ambiente e ramificar (logica sem bancada, que nenhum portao prova).
- **DEC-009 (P-A e P-B, versao e papeis; decididas pelo usuario em 2026-10-21):** a spec 0007 (modulo github) sai primeiro, na 2.14.0; esta spec entra na 2.15.0 ou acima, e o portao de T-102 cobra 2.15.0. Trabalho de execucao (T-100 a T-102 e o modelo da bancada de T-103) e do Sonnet (`--provider claude-code --model claude-sonnet-5-5`); validar e coordenar e do Opus, no chat; segunda opiniao e do Codex `gpt-6-luna`.
- **DEC-008 (P-8, evidencia):** `room-cli` falso em `evals/mock_room_cli.py`, posto no PATH pela bateria e pelos portoes, sem gastar modelo, com cenarios `ok`, `longo`, `falha`, `lento`, `pergunta` e `escreve`. Bancada real em T-103: uma rodada de `loop.sh` com o adaptador e modelo barato escolhido pelo usuario, evidencia `tipo=revisao-manual` com o id da thread filha. O falso e uma copia do que a CLI respondeu em 2026-10-21; se a CLI mudar, ele mente, e so a bancada real pega isso (ponto cego declarado).

## Tarefas

- T-100: adaptador `scripts/cloudroom_agente.py`
- T-101: bateria, etapa no verificador e loop de ponta a ponta
- T-102: documentacao e bump
- T-103: perfil em `MEMORY.md` e bancada real (agente de chat)

## Perguntas Abertas

- ~~P-A: em qual versao entra?~~ Respondida em 2026-10-21 (DEC-009): depois da 0007, na 2.15.0.
- ~~P-B: qual provider e modelo na bancada real de T-103?~~ Respondida em 2026-10-21 (DEC-009): Sonnet.
- P-C: `--intervalo` padrao de 10 s e chute de projeto, nao medicao. Cada consulta e uma chamada de CLI, nao de modelo; se o usuario preferir outro valor, e so trocar o padrao.
- ~~P-D: rodada de consenso sobre P-2 e P-3.~~ Respondida em 2026-10-21: rodada 1 cega com `gpt-6-luna` e `gpt-5.6-terra` em `-s danger-full-access`, entrada `resolvido` em `docs/CONSENSUS.md`, DEC-002 e DEC-003 ratificadas pelo usuario, DEC-004 restrita a pasta da thread; decisao copiada para `docs/DECISIONS.md`.

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
