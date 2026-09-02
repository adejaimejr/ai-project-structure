# Spec 0003 - Tarefas com evidencia, espera explicita e consenso declarado (skill 2.2.0)

**Status:** Definida
**Criada em:** 2026-09-02
**Definida em:** 2026-09-02 (apos revisao por modelo distinto; ver `docs/CONSENSUS.md`, entrada de 2026-09-02)
**Esforco:** M, quatro mudancas pequenas e independentes na mesma versao, mais o dogfood do meta-projeto.

## Problema E Resultado Esperado

- Problema 1: a linha de tarefa concluida em `TASKS.md` e afirmacao em prosa escrita pelo agente. Nada exige evidencia. O modulo de specs ja cobra o contrario um nivel acima ("Spec so vira `Concluida` com 'Evidencia De Conclusao' preenchida"), e o validador ja checa isso em spec; tarefa nao tem equivalente.
- Problema 2: a regra "Nunca Inferir" manda perguntar quando falta contexto obrigatorio, mas nao existe lugar definido para a tarefa ficar esperando a resposta. Na pratica, ou o agente preenche por inferencia, ou a pergunta se perde entre sessoes. A regra existe e nao e observavel.
- Problema 3: `CONSENSUS.md` tem uma secao por modelo, mas nada exige que as posicoes sejam independentes. Modelo que le a posicao do outro antes de escrever produz concordancia por cortesia, nao segunda opiniao. Consenso fraco fica indistinguivel de consenso forte.
- Problema 4: este repositorio nao tem um comando unico que prove sua integridade. O validador confere a estrutura, mas nao compara a raiz contra `assets/` (drift do dogfood) nem confere os fixtures. A paridade e verificada no olho.

- Resultado esperado 1: toda tarefa concluida carrega evidencia de fechamento; tarefa que declarou comando carrega o resultado daquele comando.
- Resultado esperado 2: tarefa travada por falta de resposta do usuario tem secao propria, com a pergunta registrada e um campo para a resposta.
- Resultado esperado 3: o registro de consenso declara metodo, exposicao previa e rodada, tornando o grau de confianca observavel mesmo sem prova de cegueira.
- Resultado esperado 4: um comando prova a integridade do meta-projeto com exit code.

## Escopo

### Incluido

Skill (o que sai para projetos scaffoldados):

- **Evidencia de fechamento obrigatoria** para toda tarefa em `## Concluidas` a partir da 2.2.0, em sub-linha da propria tarefa. Formato livre em campos, sem exigir comando: `Evidencia: tipo=<comando|revisao-manual|conferencia>; procedimento=<o que foi feito>; resultado=<o que saiu>`.
- **Marcador `(verifica: <comando>)` opcional** em tarefa aberta, como plano antecipado de verificacao. Quando presente, a evidencia da tarefa concluida deve registrar o resultado daquele comando.
- **Secao `## Aguardando Usuario`** no template `assets/docs/TASKS.md`, com sub-linhas `**Pergunta:**` e `**Resposta:** (A preencher.)` e marcador `(bloqueada: AAAA-MM-DD)`. Referenciada na regra "Nunca Inferir" do bloco core como destino de pergunta aberta que trava tarefa. Sem rotacao; aviso por idade.
- **Consenso declarado**: `**Metodo:**` (`pareceres-independentes` | `debate-aberto`), `**Exposicao previa a outras posicoes:**` (`sim` | `nao`) e `**Rodada:** N de 3` no template de `assets/docs/CONSENSUS.md` e na secao de consenso do bloco core. Regra de rodada 1 cega (cada modelo preenche apenas a propria secao) e teto de 3 rodadas antes de escalar para o usuario.
- **`validate_structure.py`**: `aguardando usuario` em `open_sections`; tarefa nessa secao sem `**Pergunta:**` vira ERRO; tarefa em `Concluidas` sem `Evidencia:` vira AVISO; tarefa que declarou `(verifica:)` e concluiu sem resultado correspondente vira ERRO; valor desconhecido em marcador conhecido vira AVISO; `**Metodo:**` ou `**Exposicao previa...:**` com valor fora do conjunto vira AVISO; `**Rodada:** N de 3` com N maior que 3 exige `**Proximo passo:**` apontando o usuario.
- Versao da skill para 2.2.0; marcadores dos blocos `core` e `specs` para v2.2.0; `CHANGELOG.md` da skill.
- Evals: atualizar o texto de expectativa que cita 2.1.0; novo fixture `evals/fixtures/aguardando-project` com um caso valido (retorna 0) e um caso invalido (tarefa sem `**Pergunta:**`, retorna 1).

Meta-projeto (dogfood, pre-requisito):

- **`docs/skills/ai-project-structure/evals/verify_repository.py`**: valida a raiz com `--strict`; roda os fixtures com os exit codes esperados; confere paridade dos blocos gerenciados (bloco `core` da raiz contra `assets/AGENTS.md`), das duas pontes e dos templates de `TASKS.md` e `CONSENSUS.md`; valida a estrutura de `evals.json`; roda `install.sh` em destino temporario e confere paridade dos tres destinos.
- Corrigir as 4 entradas de `docs/SESSION.md` sem o heading "Aprendizados Para MEMORY.md", que hoje reprovam `--strict`.
- Aplicar as convencoes novas no proprio `docs/TASKS.md` e `docs/CONSENSUS.md`.
- Registrar o comando na secao "Testes E Validacao" de `docs/QUALITY.md`.

### Fora Do Escopo

- `scripts/loop.sh`, notificacao, espera bloqueante, sessao de resposta guiada, automacao do consenso, teto de custo, isolamento em worktree. Tudo isso e o **modulo de loop**, previsto para v2.3 ou depois, no mesmo padrao do modulo de specs: `references/loop.md`, `assets/partials/AGENTS-loop-block.md`, marcadores proprios, ativado sob demanda.
- Ativacao do modulo de loop no scaffold. Pre-requisito para ativa-lo em qualquer projeto: secao "Testes E Validacao" de `QUALITY.md` preenchida com comando real.
- Secao separada para bloqueio nao humano (fornecedor, release upstream, incidente). Criar apenas quando o primeiro caso real aparecer, com formato proprio (DEC-007).
- Retroatividade da evidencia obrigatoria (DEC-008).
- Check de `QUALITY.md` vazio no validador.
- CI, runner automatico de evals, `--watch`.

## Criterios De Aceite

Verificaveis por comando:

- `python3 docs/skills/ai-project-structure/evals/verify_repository.py` retorna 0 no meta-projeto limpo, e retorna diferente de 0 quando o bloco core da raiz diverge de `assets/AGENTS.md` (testar com divergencia induzida e desfeita).
- `python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict` retorna 0 no meta-projeto.
- Fixture `aguardando-project`: caso valido (tarefa com `**Pergunta:**` e `**Resposta:** (A preencher.)`) retorna 0; caso invalido (sem `**Pergunta:**`) retorna 1.
- Tarefa concluida sem `Evidencia:` gera AVISO; tarefa que declarou `(verifica:)` e concluiu sem resultado correspondente gera ERRO.
- Marcador conhecido com valor desconhecido gera AVISO.
- Entrada de consenso sem `**Metodo:**`, sem `**Exposicao previa a outras posicoes:**` ou com valor fora do conjunto gera AVISO; `**Rodada:**` acima de 3 sem `**Proximo passo:**` gera AVISO.
- Tarefa concluida antes da 2.2.0, sem `Evidencia:`, nao gera nada (DEC-008).
- Fixture `broken-project` continua com exatamente os 2 erros de hoje; `v1-project` continua exit 0.
- Paridade: bloco core identico entre raiz e `assets/AGENTS.md`, ambos com marcador v2.2.0; pontes identicas aos templates; templates de `TASKS.md` e `CONSENSUS.md` conferidos pelo verificador.
- `install.sh` em destino temporario produz tres destinos identicos (`diff -rq` ignorando `evals/`, `install.sh`, `README.md` e `CHANGELOG.md`, que existem apenas na fonte canonica).
- Nenhum travessao (U+2014) em arquivo novo ou alterado.

Julgados na mao, sem runner hoje (registrado como limitacao conhecida):

- Scaffold minimal e scaffold completa recem-criados com os templates 2.2.0: exige rodar o fluxo da IA e responder a entrevista.
- Atualizacao de um projeto 2.1.0 pelo fluxo de `references/atualizacao.md`, contendo tarefas concluidas, tarefa aguardando e consenso existente, sem perder conteudo abaixo de "## Regras Do Projeto", sem sobrescrever `docs/*.md` do usuario e sem transformar registro historico em alegacao falsa.

## Decisoes

- DEC-001: o marcador se chama `(verifica:)`, nao `(loop:)`. Motivo: o valor da declaracao e independente de loop e vale turno a turno; o modulo de loop futuro le o mesmo campo como criterio de elegibilidade, sem renomear convencao ja distribuida. Confirmada pelo Codex.
- DEC-002: espera e secao, nao campo na linha. Motivo: `TASKS.md` estabelece que "o status da tarefa e a secao onde ela esta" e proibe campo de status na linha. `(bloqueada: AAAA-MM-DD)` entra como dado, nao como status. Confirmada pelo Codex.
- DEC-003: o loop fica fora desta versao e nunca entra no scaffold. Motivo: o portao de verificacao nao pode existir no dia zero de um projeto novo, porque nao ha suite de teste ainda. Um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao. Confirmada pelo Codex, com a ressalva de que "nao ativar" nao implicaria "nao disponibilizar caminho de ativacao"; mantida assim mesmo, porque instrucao de loop no core cobra custo permanente de todo projeto.
- DEC-004 (revisada): rodada 1 cega e teto de 3 rodadas ganham campos declarativos (`Metodo`, `Exposicao previa`, `Rodada`). Motivo: a versao original aceitava prosa nao enforcavel e parava ai, o que nao resolvia o Problema 3; consenso fraco continuava visualmente igual ao forte. Os campos nao provam independencia, e o validador deve declarar explicitamente que checa presenca e valor, nunca veracidade. Revisao proposta pelo Codex e aceita.
- DEC-005: sem check de `QUALITY.md` vazio no validador. Motivo: detectar "o projeto tem codigo" e fragil, e o aviso dispararia em todo projeto de conteudo. A exigencia vira pre-requisito de ativacao do modulo de loop. Confirmada pelo Codex.
- DEC-006 (revertida): `(verifica:)` continua **opcional**, mas a **evidencia de fechamento passa a ser obrigatoria** para toda tarefa concluida. Motivo: com verificacao inteiramente opcional, o agente conclui justamente as tarefas menos verificadas sem consequencia, preservando a lacuna que a spec quer fechar. Tornar `(verifica:)` obrigatorio seria pior, porque empurraria o usuario a inventar comando falso em tarefa de conteudo, pesquisa ou decisao. Argumento do Codex, aceito.
- DEC-007: secao separada para bloqueio nao humano nao entra agora. Motivo: `Aguardando Usuario` e semanticamente preciso para o formato pergunta e resposta; bloqueio por fornecedor ou release upstream tem formato diferente e ainda nao existe caso real neste projeto. Criar quando aparecer. Decisao do usuario em 2026-09-02.
- DEC-008: a evidencia obrigatoria nao e retroativa. Vale para tarefa concluida a partir da 2.2.0. O validador nao cobra evidencia de tarefa anterior, e `references/atualizacao.md` nao reescreve historico. Motivo: tornar retroativa converteria registro historico em alegacao sem evidencia, em todo projeto que atualizar. Decisao do usuario em 2026-09-02.
- DEC-009: o verificador de integridade vive em `docs/skills/ai-project-structure/evals/`, nunca em `scripts/` na raiz. Motivo duplo: `scripts/` na raiz viola a regra de raiz minima registrada em "Regras Do Projeto" do `AGENTS.md`, cuja excecao cobre apenas `README.md`, `LICENSE` e `.gitignore`; e `evals/` nao e distribuido pelo `install.sh`, entao o verificador nao vai parar na maquina de todo usuario. Colocacao proposta pelo Codex; a segunda razao foi verificada por `diff -rq` contra `~/.claude/skills/ai-project-structure`.

## Tarefas

- T-009: bloco core v2.2.0 e templates de TASKS.md e CONSENSUS.md com as convencoes novas
- T-010: checks novos no validador
- T-011: verify_repository.py em evals/ e correcao dos headings de SESSION.md
- T-012: fixture nova, evals atualizados, dogfood e reinstalacao com paridade

## Perguntas Abertas

- (Vazio. As quatro perguntas do Rascunho foram respondidas na revisao por modelo distinto e ratificadas pelo usuario; ver DEC-006, DEC-007, DEC-008 e o criterio de aviso por idade na secao Incluido.)

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
