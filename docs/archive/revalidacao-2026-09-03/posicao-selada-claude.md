# Posicao selada do Claude (Fable 5.1), antes de rodar qualquer agente

Data: 2026-09-03. Escrita depois de ler o codigo inteiro da skill 2.5.1, e antes da primeira chamada de modelo externo. Sem exposicao previa a outras posicoes.

## Superficie 1, contrato do bloco core

- Nao verificavel por script nem por pessoa: "Ordem de leitura", "Nao refatore fora do escopo", "Nunca Inferir", "Achado so vira tarefa depois da disposicao", "Regra de desempate", campos de independencia (autodeclarados por desenho).
- Violavel sem acusacao: "Pontes sao imutaveis" (validador so confere que a ponte menciona AGENTS.md; ponte com regra de produto passa limpa). "Tarefa em Aguardando Usuario carrega (bloqueada: AAAA-MM-DD)" (validador so cobra **Pergunta:**; sem o marcador, TASK-BLOQUEADA-ANTIGA nunca dispara). "Toda tarefa em Concluidas carrega Evidencia" (linha concluida sem prefixo de data nao e cobrada).
- Contradicao interna: nenhuma forte. Tensao: bloco de loop diz "Ate 3 tentativas" e o script aceita --tentativas N. Core diz que CONSENSUS.md e "debate entre modelos ... apenas para duvidas reais" em "Onde Escrever Cada Coisa", e a secao Achado diz que nem todo uso e debate.

## Superficie 2, validador

- MARKER_RE so casa `core|specs`. Bloco `loop` com marcador despareado ou sem versao passa limpo. Falso negativo confirmado por leitura (linha 57).
- Entrada de SESSION/CONSENSUS com data malformada no heading (`## 2026-9-3 - X`) nao e entrada: escapa de todos os checks, sem diagnostico.
- Concluida sem data no prefixo: nao cobra evidencia.
- Aguardando sem `(bloqueada:)`: passa; idade nunca cobrada.
- `**Proximo passo:**` vazio passa (so presenca).
- `resultado=` vazio passa.
- Modulo specs: bloco specs em AGENTS.md sem docs/specs/, ou docs/specs/ sem bloco, nenhum diagnostico.
- ENTRY_RE (linha 59) e codigo morto.
- T-054 e T-056 continuam validos.
- Divergencia entre "um parser so": loop_task compara ID por int (T-01 == T-001), validador por string. Sub-linha separada por linha em branco: validador anexa, loop_task nao.

## Superficie 3, loop

- `(verifica: ...)` nao aceita `)` no comando: `VERIFICA_RE = \(verifica:\s*([^)]*)\)`. Comando com parenteses e truncado em silencio e o truncado e executado como portao. Evidencia e escrita com o truncado, e o validador aceita porque usa a mesma regex.
- `FALHA_ANTERIOR` entra no prompt como argumento de linha de comando. Saida de portao muito grande (centenas de KB) estoura o limite de argumento, o agente nem sobe, e o loop reporta exit 4 "agente mal configurado". Diagnostico errado para "arquivo enorme".
- `cmd_fechar` le a linha da tarefa **depois** do agente rodar. Agente que edita `(verifica:)` na propria linha faz a evidencia registrar `procedimento=` diferente do comando que de fato rodou como portao (capturado antes). Agente que apaga o marcador: portao verde e o fecho falha com exit 1.
- Saida de portao com bytes nao UTF-8: `read_text` levanta UnicodeDecodeError sem tratamento, traceback, tarefa nao fecha apesar do portao verde.
- `references/loop.md` tabela de exit codes (linhas 79-87) nao tem o exit 4, que existe no script e no SKILL.md.
- T-058 continua valido.

## Superficie 4, portao dos evals (a provar por mutacao)

- Hipotese central: varios checks do validador nao tem fixture. Desligar `check_session`, `check_bridges`, `check_em_dash` (do validador), `check_evidence` e `check_markers` deve passar verde no verify_repository, porque nenhuma fixture espera diagnostico deles e a raiz em --strict so fica mais limpa.
- Deve pegar: TASK-ID-DUPLICADO (broken), SPEC-STATUS-INVALIDO (broken), AGUARDANDO-SEM-PERGUNTA (aguardando/invalido), os cinco de achado (achado/invalido), strip_fences (debate).
- `verificar_versao` nao olha a versao em prosa no SKILL.md (linha 186, "versao da estrutura: 2.5.1").
- `evals.json` esta com `v2.2.0` nos expected_output (evals 1, 2, 3, 5); `verificar_evals_json` so confere estrutura.
- test_loop nao cobre: truncagem de `resumir_saida`, remocao do `.loop-pergunta` leftover no arranque, `bloquear` em tarefa ja bloqueada, comando com parenteses.

## Superficie 5, fluxos

- SKILL.md passo 6 manda inserir a primeira entrada "no fim do arquivo", o template diz "mais recente no topo". Na primeira entrada da no mesmo; na segunda, agente que releu o SKILL.md pode continuar no fim.
- Atualizacao: versao detectada so pelo marcador core; specs/loop com marcador atrasado mas conteudo igual podem ficar com versao velha ("identico -> pule em silencio").
- A executar de verdade: scaffold minimal, scaffold com specs, atualizacao de v1-project, contra a copia instalada.

## Superficie 6, templates

- assets/docs/QUALITY.md: checklist nao menciona evidencia de fechamento, Aguardando Usuario, achado nem campos de independencia. Irmao de T-055 (asset atras do core).
- assets/docs/TASKS.md com placeholder `AAAA-MM-DD` no marcador passa em --strict (so INFO). Projeto em que o agente esqueceu o passo 5b fica sem cobranca de evidencia e o validador nao reclama de verdade.
- assets/docs/PROMPTS.md: prompts nao mencionam TASKS.md, Evidencia, nem achado. Envelhecido, mas nao contradiz.
- assets/docs/README.md e ONBOARDING.md: nao mencionam MEMORY em ONBOARDING; README ok.

## Superficie 7, distribuicao

- README da skill: "Instalacao manual" copia so SKILL.md, assets e agents (sem scripts e references), entao instalacao manual nao tem validador nem loop. Lista de fixtures desatualizada (falta achado-project e debate-project).
- install.sh: copia `scripts/__pycache__` para os destinos. Destino existente com edicao local e sobrescrito sem aviso ("com seguranca" e promessa vaga). `--all` nao documentado no cabecalho. Uninstall deixa `.claude/skills` vazio (aceitavel).
- agents/openai.yaml: o binario do codex 0.152.1 nao contem a string `allow_implicit_invocation`. Suspeita forte de que a chave e ignorada. Precisa conferir quais chaves de openai.yaml o binario conhece.
- SKILL.md linha 186 tem a versao em prosa, fora de qualquer check.

## Aposta sobre o achado mais caro

O portao dos evals nao cobre a maior parte dos checks do validador. Desligar um check inteiro passa verde porque nenhuma fixture espera o diagnostico dele e a raiz so fica mais limpa. Isso escapou porque as fixtures foram escritas por feature nova (2.2.0, 2.4.0), nunca por check existente, e "verify em 44 de 44" foi lido como cobertura.
