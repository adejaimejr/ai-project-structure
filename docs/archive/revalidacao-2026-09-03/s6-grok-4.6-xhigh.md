Confirmei T-054 a T-058 no codigo e no validador. Segue o relatorio so com o que deu para reproduzir.

## Achados

### A-S6-1: `(convencoes-2-2-0-desde: AAAA-MM-DD)` esquecido desliga a evidencia e passa em `--strict`
- Onde: `docs/skills/ai-project-structure/SKILL.md:134-136`; `assets/docs/TASKS.md:12`; `scripts/validate_structure.py:555-566` e `729-735`; `scripts/validate_structure.py:1000-1002`
- Promessa: o passo 5b diz para trocar `AAAA-MM-DD` pela data de hoje, porque e a data a partir da qual a evidencia de fechamento e cobrada. O bloco core (`assets/AGENTS.md:108-119`) promete que tarefa concluida a partir dessa data carrega `Evidencia:`. `--strict` promete tratar aviso como falha (`validate_structure.py:960`, `1000-1002`).
- Realidade: o marcador com `AAAA-MM-DD` e detectado, `parse_date` devolve `None`, e o diagnostico e **INFO** (`CONVENCOES-DATA-INVALIDA`), nao AVISO. `--strict` ignora INFO. Sem data valida, `check_evidence` nao cobra `Evidencia:` de nenhuma concluida (`764-765`: `if evidences or adopted is None: continue`). O mesmo vale para os outros preenchimentos do passo 5 e 6: o validador nao le o texto de `PROJECT_CONTEXT.md` e nao exige nenhuma entrada real em `SESSION.md`.
- Reproducao: copia crua do nucleo, sem passos 5/5b/6:

```text
python3 docs/skills/ai-project-structure/scripts/validate_structure.py /tmp/aps-s6-review/placeholders-crus --strict --codigos
# INFO|CONVENCOES-DATA-INVALIDA|docs/TASKS.md|
# EXIT: 0
# prosa: 0 erros, 0 avisos
```

Mesma pasta com T-001 movida para Concluidas **sem** `Evidencia:` (`/tmp/aps-s6-review/placeholders-crus-concluida`): ainda `EXIT: 0`, so o INFO da data. Contraste com adocao preenchida (`/tmp/aps-s6-review/adocao-ok-sem-evidencia`): `AVISO|EVIDENCIA-AUSENTE|docs/TASKS.md|T-001`, `EXIT: 1`.
- Severidade: **alta**, porque o unico preenchimento que o SKILL.md chama de contrato da 2.2.0, se esquecido, apaga a cobranca de evidencia e o portao `--strict` continua verde.

### A-S6-2: copiar o Modelo De Debate e o modelo de linha concluida quebra `--strict` no dia seguinte
- Onde: `assets/docs/CONSENSUS.md:49-63`; `assets/docs/TASKS.md:20-25`; `scripts/validate_structure.py:357-364` e `463-470`; `scripts/validate_structure.py:631-640`
- Promessa: o template e o formato para criar entrada e fechar tarefa. `SKILL.md:278` chama esses arquivos de templates limpos. `assets/AGENTS.md:174-182` e `SKILL.md:20-22` dizem que cada entrada declara `Status` (um de tres) e `Metodo` / `Exposicao previa` / `Rodada` (um de cada conjunto).
- Realidade: os modelos usam a uniao (`aberto | resolvido | arquivado`, `pareceres-independentes | debate-aberto`, `sim | nao`) **como valor da linha**. O validador compara o valor inteiro com o conjunto. A mensagem de status chega a repetir o mesmo texto como invalido e como esperado. O modelo de linha concluida traz `(spec: 0001-login-social)`, que vira `ERRO` `SPEC-REF-NAO-RESOLVE` em projeto sem essa spec (minimal e completa com specs, se a spec exemplo nao existir).
- Reproducao: dia 1, passos 4, 5, 5b e 6 do `SKILL.md`, nivel minimal e completa+specs, **passam**:

```text
python3 .../validate_structure.py /tmp/aps-s6-review/loja-min --strict --codigos
# (saida vazia) EXIT: 0
# prosa: Nenhum problema encontrado. Resumo: 0 erros, 0 avisos.

python3 .../validate_structure.py /tmp/aps-s6-review/finbot --strict --codigos
# (saida vazia) EXIT: 0
# prosa: Nenhum problema encontrado. Resumo: 0 erros, 0 avisos.
```

Dia 2: segunda sessao com os headings do modelo (data `2026-09-04`), T-001 concluida no formato do proprio `TASKS.md` (incluindo `(spec: 0001-login-social)` e a sub-linha de evidencia), entrada de consenso colada do Modelo De Debate (data preenchida, resto literal). **Os dois niveis falham igual:**

```text
python3 .../validate_structure.py /tmp/aps-s6-review/loja-min-d2 --strict --codigos
AVISO|CONSENSO-CAMPO-INVALIDO|docs/CONSENSUS.md|2026-09-04 - Tema do consenso
AVISO|CONSENSO-CAMPO-INVALIDO|docs/CONSENSUS.md|2026-09-04 - Tema do consenso
AVISO|CONSENSO-STATUS-INVALIDO|docs/CONSENSUS.md|2026-09-04 - Tema do consenso
ERRO|SPEC-REF-NAO-RESOLVE|docs/TASKS.md|0001-login-social
EXIT: 1
```

Prosa:

```text
docs/CONSENSUS.md
  [AVISO] [CONSENSO-CAMPO-INVALIDO] Entrada '2026-09-04 - Tema do consenso' com '**Metodo:** pareceres-independentes | debate-aberto' fora do conjunto (debate-aberto | pareceres-independentes).
  [AVISO] [CONSENSO-CAMPO-INVALIDO] Entrada '2026-09-04 - Tema do consenso' com '**Exposicao previa a outras posicoes:** sim | nao' fora do conjunto (nao | sim).
  [AVISO] [CONSENSO-STATUS-INVALIDO] Entrada '2026-09-04 - Tema do consenso' com Status invalido: 'aberto | resolvido | arquivado' (esperado: aberto | resolvido | arquivado).

docs/TASKS.md
  [ERRO] [SPEC-REF-NAO-RESOLVE] Referencia '(spec: 0001-login-social)' nao resolve para docs/specs/0001-login-social.md.

Resumo: 1 erros, 3 avisos.
```

`/tmp/aps-s6-review/finbot-d2` produz as mesmas quatro linhas. A segunda sessao em si nao gerou `SESSAO-SEM-HEADINGS`. O Modelo De Achado (`assets/docs/CONSENSUS.md:101-118`) repete o mesmo padrao de uniao, inclusive `**Escapou de verificacao:** sim | nao`.
- Severidade: **alta**, porque o dia 2 pedido (copiar os modelos do template) e exatamente o que um agente faz, e o portao fecha.

### A-S6-3: checklists e prompts do usuario final nao acompanharam o bloco core 2.2.0/2.4.0
- Onde: `assets/docs/QUALITY.md:5-43`; `assets/docs/PROMPTS.md:23-33`; `assets/docs/ONBOARDING.md:1-28`; `assets/docs/README.md:28-56`; `assets/docs/SESSION.md:36-39`; `assets/AGENTS.md:70-223` (o contrato)
- Promessa: o core exige evidencia de fechamento, secao `Aguardando Usuario`, Nunca Inferir, campos `Metodo` / `Exposicao previa` / `Rodada`, formato de achado, rotacao, `STACK.md` quando existir, e specs quando o modulo estiver ativo. `QUALITY.md:3` se apresenta como checklist antes de finalizar. `PROMPTS.md:29-33` manda revisar pela QUALITY. T-055 e o mesmo descompasso no `docs/CONSENSUS.md` da raiz; o pedido era achar irmaos nos templates.
- Realidade: o `Modelo De Debate` de `assets/docs/CONSENSUS.md` **ja tem** os tres campos (nao e irmao de T-055). Quem ficou para tras:

| Regra do core | Template que deveria carregar | Leva? |
|---|---|---|
| Evidencia de fechamento | `TASKS.md`, `QUALITY.md`, `ONBOARDING.md`, `PROMPTS.md` (revisao), `README.md` | So `TASKS.md:11-24`. QUALITY, ONBOARDING, PROMPTS e README silenciam. |
| Aguardando Usuario | `TASKS.md`, `QUALITY.md`, `ONBOARDING.md` | So `TASKS.md:35-45`. QUALITY e ONBOARDING silenciam. |
| Nunca Inferir | `QUALITY.md`, `ONBOARDING.md`, `specs/README.md`, `PROMPTS.md`, `PROJECT_CONTEXT.md` | `QUALITY.md:41` e `specs/README.md:20`. ONBOARDING, PROMPTS e PROJECT_CONTEXT silenciam. |
| Campos de independencia | `CONSENSUS.md`, `QUALITY.md`, `PROMPTS.md` (pedir consenso) | `CONSENSUS.md:19-61` sim. `QUALITY.md:26` so `Status` e `Proximo passo`. `PROMPTS.md:23-27` pede posicao sem Metodo/Exposicao/Rodada. |
| Achado | `CONSENSUS.md`, `QUALITY.md`, `README.md`, `PROMPTS.md` | `CONSENSUS.md:33-149` sim. QUALITY, README (`CONSENSUS.md`: so "debate") e PROMPTS silenciam. |
| Rotacao | `archive/README.md`, `QUALITY.md`, `SESSION.md`, `CONSENSUS.md` | `archive/README.md:11` e `QUALITY.md:27` sim. SESSION e CONSENSUS templates nao mencionam o gatilho 20 entradas / 30KB. |
| STACK.md | `README.md`, `QUALITY.md`, `ONBOARDING.md`, `PROJECT_CONTEXT.md` (links) | `README.md:51` sim. QUALITY, ONBOARDING e os links de PROJECT_CONTEXT (`32-39`) silenciam. |
| Specs | `specs/README.md`, `README.md`, `TASKS.md`, `QUALITY.md`, `ONBOARDING.md` | specs/README, README e TASKS sim. QUALITY so o item de Status (`40`). ONBOARDING silencia. |

`SESSION.md:36-39` tambem corta o core (`assets/AGENTS.md:142`): o modelo tem agente e motivo, nao a nota "qualquer agente serve se tiver contexto suficiente".
- Reproducao: `rg -n "Evidencia|Aguardando Usuario|Metodo|Achado|STACK|Nunca Inferir" docs/skills/ai-project-structure/assets/docs/QUALITY.md docs/skills/ai-project-structure/assets/docs/PROMPTS.md docs/skills/ai-project-structure/assets/docs/ONBOARDING.md docs/skills/ai-project-structure/assets/docs/README.md`. QUALITY so casa Nunca Inferir. PROMPTS/ONBOARDING/README nao casam evidencia, Aguardando, Metodo nem Achado. O prompt "Solicitar Consenso Entre Modelos" (`PROMPTS.md:23-27`) e o equivalente funcional de T-055: quem o segue produz entrada sem os campos que `--strict` cobra (A-S6-2).
- Severidade: **media**, porque o contrato esta no `AGENTS.md` entregue, mas o checklist e os prompts que o agente usa na hora de fechar sessao ainda descrevem a estrutura 2.1.x.

### A-S6-4: o unico exemplo de evidencia ensina `tipo=comando` com `pytest` numa tarefa de conteudo
- Onde: `assets/docs/TASKS.md:16-25` e `33`; `assets/AGENTS.md:117`; `scripts/validate_structure.py:121`
- Promessa: `tipo` de tarefa de conteudo, pesquisa ou decisao e `revisao-manual` ou `conferencia`. "Nunca invente um comando inexistente so para preencher o campo." O validador "confere a forma da evidencia, nunca o conteudo" (`assets/AGENTS.md:121`).
- Realidade: a unica linha concluida de exemplo e `tipo=comando; procedimento=pytest -q; resultado=42 passed, exit 0`. A unica tarefa real do template (`T-001`) e preencher `PROJECT_CONTEXT.md`. Seguir o exemplo na T-001 inventa um pytest que nao prova a tarefa. `--strict` aceita.
- Reproducao: `/tmp/aps-s6-review/loja-min-d2-preenchido` (T-001 concluida com a evidencia do modelo, **sem** `(spec: 0001-login-social)`, consenso com valores atomicos validos):

```text
python3 .../validate_structure.py /tmp/aps-s6-review/loja-min-d2-preenchido --strict --codigos
# (saida vazia) EXIT: 0
```
- Severidade: **media**, porque o template treina o anti-padrao que o core proibe, e o portao confirma a mentira.

### A-S6-5: `Aguardando Usuario` no core pede tres campos; o validador so recusa sem `Pergunta`
- Onde: `assets/AGENTS.md:77`; `assets/docs/TASKS.md:39-45`; `scripts/validate_structure.py:704-717`
- Promessa: pergunta que trava a tarefa vai para `## Aguardando Usuario` com `**Pergunta:**`, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)`. O modelo do `TASKS.md` mostra os tres.
- Realidade: `check_waiting` so testa se alguma sub-linha comeca com `**pergunta:**`. Sem `Resposta` e sem `(bloqueada:)`, `--strict` e verde.
- Reproducao: em `/tmp/aps-s6-review/aguardando-parcial`, T-002 na secao Aguardando so com `**Pergunta:**`:

```text
python3 .../validate_structure.py /tmp/aps-s6-review/aguardando-parcial --strict --codigos
# (saida vazia) EXIT: 0
```
- Severidade: **media**, porque a espera deixa de ser o protocolo do core e vira so um bullet com pergunta.

### A-S6-6: leitura relevante obriga `docs/ARCHITECTURE.md`; o scaffold minimal nao cria o arquivo
- Onde: `assets/AGENTS.md:41-49`; `SKILL.md:81-110`
- Promessa: em mudanca relevante o agente le, nesta ordem, README, PROJECT_CONTEXT, SESSION, MEMORY, TASKS, **ARCHITECTURE**, QUALITY. Nao ha "se existir" nesse item (diferente de STACK no gatilho, `assets/AGENTS.md:101`).
- Realidade: ARCHITECTURE e opcional, so copiado no nivel completa. Minimal entrega o mesmo bloco core e nao entrega o sexto arquivo da lista.
- Reproducao: `test -f /tmp/aps-s6-review/loja-min/docs/ARCHITECTURE.md; echo $?` devolve `1`. O `AGENTS.md` copiado para essa pasta ainda lista `docs/ARCHITECTURE.md` na linha 46. Completa (`/tmp/aps-s6-review/finbot/docs/ARCHITECTURE.md`) existe.
- Severidade: **media**, porque o contrato de leitura do nucleo nao e verdadeiro no nivel que o SKILL.md recomenda como padrao (`SKILL.md:63-64`).

### A-S6-7: a ponte nao menciona `TASKS.md` nem o contrato 2.2.0/2.4.0
- Onde: `assets/CLAUDE.md:1-12`; `assets/GEMINI.md:1-12`; `assets/AGENTS.md:22-24` e `30-35`
- Promessa: as pontes sao so redirecionamento; Claude/Gemini devem seguir a ordem de leitura do `AGENTS.md`. Mudanca trivial ja exige `SESSION.md` e `TASKS.md`.
- Realidade: "Antes de trabalhar" cita `AGENTS.md`, a ordem (sem lista), `SESSION.md` e `CONSENSUS.md`. Nao cita `TASKS.md`, `QUALITY.md`, `MEMORY.md`, evidencia, Aguardando Usuario, Nunca Inferir, campos de independencia, achado, rotacao, STACK nem specs. Quem obedece o item 1 da ponte e le o `AGENTS.md` recupera tudo. Quem trata a ponte como o conjunto de regras (ferramenta que injeta so `CLAUDE.md` / `GEMINI.md`) trabalha sem o contrato.
- Reproducao: o texto integral da ponte e as 12 linhas de `assets/CLAUDE.md` (Gemini e o mesmo, trocando o nome da ferramenta). Nao ha a string `TASKS.md` nesses arquivos.
- Severidade: **baixa** se a ferramenta realmente le o `AGENTS.md` em seguida; **media** no caso em que a ponte e a unica regra injetada. O furo esta no que a ponte escolhe enumerar, nao no redirecionamento em si.

### A-S6-8: leftovers de meta-projeto em templates que o usuario final recebe
- Onde: `assets/docs/ARCHITECTURE.md:11-13`; `assets/docs/GLOSSARY.md:29-31`
- Promessa: os opcionais descrevem **o projeto-alvo**. `SKILL.md:8-9` e `278` apresentam `assets/` como templates limpos para um projeto novo.
- Realidade: `ARCHITECTURE.md` lista `docs/skills/` como modulo do projeto. Um `finbot` recem-criado nao tem essa pasta. `GLOSSARY.md` define Skill como instrucao "para ensinar o Codex", enquanto a skill e multi-ferramenta (`SKILL.md:3-4`).
- Reproducao: o nivel completa copia esses arquivos sem reescreve-los (`SKILL.md:99-110`). `rg "docs/skills" /tmp/aps-s6-review/finbot/docs/ARCHITECTURE.md` encontra a linha. `rg Codex /tmp/aps-s6-review/finbot/docs/GLOSSARY.md` encontra a definicao.
- Severidade: **baixa**, nao quebra `--strict`; ensina arvore e publico errados no primeiro dia.

**Partials (pergunta 3):** nao e achado. Nada de `assets/partials/` e copiado como pasta. O SKILL.md (`119`, `252-253`), `references/specs.md:7` e `references/loop.md:18-19` mandam **inserir o conteudo** do bloco em `AGENTS.md`. No scaffold que montei, `partials/` e `assets/` nao existem em `/tmp/aps-s6-review/loja-min` nem em `finbot`.

## Suspeitas nao demonstradas
- O titulo do passo 4 (`SKILL.md:77`: "Copie os arquivos do `assets/`") pode ser lido como `cp -R assets/ destino/`, o que levaria `partials/` para o projeto. Nao provei com agente real; o restante do passo lista arquivos e proibe a pasta. Faltou uma rodada de scaffold por modelo, nao por este script.
- O Modelo De Achado com `**Escapou de verificacao:** sim | nao` deve disparar `ACHADO-ESCAPOU-INVALIDO` pelo mesmo mecanismo de A-S6-2. Nao rodei essa cola, so a do Modelo De Debate.
- `MARKER_RE` no validador (`validate_structure.py:56-58`) so casa `core|specs`, nao `loop`. Marcador de loop despareado passaria calado. Fora da superficie de scaffold (loop nunca entra nela); nao exercitei um projeto com bloco loop quebrado.
- Ferramentas que injetam so `CLAUDE.md` como regra da sessao (A-S6-7) dependem do produto, nao do template. Nesta sessao o workspace injeta os dois; nao medi um projeto recem-criado no Claude Code / Gemini CLI.

## Tarefas conhecidas
- T-054: sim. `check_consensus_declaration` retorna calado se `Rodada` e `None` (`validate_structure.py:365-367`) e usa `re.match` (`368`). Fixture `/tmp/aps-s6-review/t054` (entrada sem `Rodada` + `**Rodada:** 1 de 1 e mais texto qualquer`) saiu `--strict` EXIT 0, zero diagnosticos.
- T-055: sim. O Modelo De Debate de `docs/CONSENSUS.md` da raiz (`19-63`) nao tem `**Metodo:**`, `**Exposicao previa a outras posicoes:**` nem `**Rodada:**`. O de `assets/docs/CONSENSUS.md:49-63` tem. Continua defeito da raiz, nao do asset.
- T-056: sim. Spec com 3 perguntas e 3 sub-bullets em `/tmp/aps-s6-review/t056`: `--progress` imprimiu `perguntas abertas: 6` (esperado 3). `spec_overview` faz `line.strip().startswith("- ")` (`validate_structure.py:906-909`).
- T-058: sim. `loop.sh` nao tem `flock` nem arquivo de lock. Sinal fixo `.loop-pergunta` (`36`) e leftover apagado no arranque (`80-84`).

## Inventario
Lidos por inteiro (superficie 6):
- `docs/skills/ai-project-structure/assets/AGENTS.md`
- `docs/skills/ai-project-structure/assets/CLAUDE.md`
- `docs/skills/ai-project-structure/assets/GEMINI.md`
- `docs/skills/ai-project-structure/assets/docs/README.md`
- `docs/skills/ai-project-structure/assets/docs/PROJECT_CONTEXT.md`
- `docs/skills/ai-project-structure/assets/docs/SESSION.md`
- `docs/skills/ai-project-structure/assets/docs/MEMORY.md`
- `docs/skills/ai-project-structure/assets/docs/CONSENSUS.md`
- `docs/skills/ai-project-structure/assets/docs/TASKS.md`
- `docs/skills/ai-project-structure/assets/docs/DECISIONS.md`
- `docs/skills/ai-project-structure/assets/docs/QUALITY.md`
- `docs/skills/ai-project-structure/assets/docs/CHANGELOG.md`
- `docs/skills/ai-project-structure/assets/docs/ARCHITECTURE.md`
- `docs/skills/ai-project-structure/assets/docs/API.md`
- `docs/skills/ai-project-structure/assets/docs/DATA_MODEL.md`
- `docs/skills/ai-project-structure/assets/docs/GLOSSARY.md`
- `docs/skills/ai-project-structure/assets/docs/ONBOARDING.md`
- `docs/skills/ai-project-structure/assets/docs/ROADMAP.md`
- `docs/skills/ai-project-structure/assets/docs/PROMPTS.md`
- `docs/skills/ai-project-structure/assets/docs/STACK.md`
- `docs/skills/ai-project-structure/assets/docs/archive/README.md`
- `docs/skills/ai-project-structure/assets/docs/specs/README.md`
- `docs/skills/ai-project-structure/assets/partials/AGENTS-specs-block.md`
- `docs/skills/ai-project-structure/assets/partials/AGENTS-loop-block.md`

Tambem lidos por inteiro para contrato e fluxo: `AGENTS.md` (raiz), `docs/skills/ai-project-structure/SKILL.md`, `docs/skills/ai-project-structure/references/specs.md`, `docs/TASKS.md`.

Lidos em parte: `docs/SESSION.md` (topo), `docs/CONSENSUS.md` (modelo da raiz), `scripts/validate_structure.py` (checks citados), `scripts/loop.sh` (cabecalho e arranque), `references/loop.md` (ativacao e partials).
