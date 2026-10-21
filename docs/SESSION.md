# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas mais antigas foram rotacionadas para `docs/archive/SESSIONS-2026.md`. Este arquivo mantem as 3 mais recentes.

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

## 2026-10-21 - Claude Opus 5.5 (gestor) com subagente Sonnet 5.5 (spec 0008: T-102, skill 2.15.0)

### Objetivo

- Com a 2.14.1 publicada, rebasear o PR #5, fazer a T-102 (documentacao e bump 2.15.0), mergear, taguear `v2.15.0` e seguir para a T-103 (bancada real).

### O Que Foi Feito

- Rebase do PR #5 sobre `ee5d37a`: `verify_repository.py` mesclou sozinho; conflitos so de acrescimo em `TASKS.md`, `SESSION.md` e `CHANGELOG.md`, resolvidos mantendo os dois lados (as entradas da 2.14.x por cima). Verificador 91/91. Push com `--force-with-lease` na branch do PR (o rebase pedido exige reescrever a branch).
- T-102 pelo subagente `cr_child_bd31beace8f3c42cf456c429`: `references/cloudroom.md`, `SKILL.md`, `references/loop.md`, `references/consenso.md`, bump 2.15.0 e CHANGELOG da skill. Portao 14/14; revisado pelo gestor.
- T-111 criada com o sim do usuario, para ser a tarefa real da bancada da T-103: o check 1 do `portao_t102.py` imprime "secao faltando" mesmo verde. `portao_t111.py` escrito antes, com autoteste da regex, 2/3 pelo motivo certo.

### Arquivos Criados Ou Alterados

- Skill: `references/cloudroom.md` (novo), `SKILL.md`, `CHANGELOG.md`, `references/loop.md`, `references/consenso.md`, `assets/AGENTS.md`, os tres partials, `evals/portao_t111.py` (novo).
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/specs/0008-adaptador-cloudroom.md` (T-111 na lista).

### Decisoes Tomadas

- Do usuario: criar a T-111 como tarefa da bancada. Do gestor: o bench roda com `--projeto` igual a pasta da thread (`/code/ai-project-structure`), como manda a DEC-004.

### Aprendizados Para MEMORY.md

- Nenhum novo. O subagente confirmou a Armadilha ja registrada: portao, bateria e verificador juntos passam de 120 s e o shell manda para segundo plano; rodar cada um separado.

### Pendencias

- Merge do PR #5, tag `v2.15.0` e Release; depois a T-103 com a T-111 pelo loop.

### Proximo Passo Recomendado

- Agente sugerido: esta thread, para merge, tag e a bancada (Sonnet pelo adaptador, Opus revisa). Qualquer agente serve se tiver contexto suficiente.

## 2026-10-21 - Claude Opus 5.5 (T-110: description do SKILL.md, skill 2.14.1)

### Objetivo

- Resolver a T-110 (`description` acima de 1024 caracteres) com o texto aprovado pelo usuario ("pode, com esse texto"), num patch 2.14.1, antes da 2.15.0 da spec 0008.

### O Que Foi Feito

- Conferido na fonte (agentskills.io/specification): `description` com no maximo 1024 caracteres e obrigatorio, cobrado pelo `skills-ref validate`.
- Portao `portao_t110.py` escrito antes, 3/6 (1479 caracteres, versao 2.14.0).
- Ao aplicar o texto, o parse com `yaml.safe_load` acusou erro: o texto novo e o `description` publicado na 2.14.0 tinham ": " num valor sem aspas. O da 2.14.0 veio da frase do modulo github na T-108. Troquei os dois-pontos (985 caracteres) e acrescentei ao verificador a etapa `verificar_frontmatter` (YAML seguro, teto de 1024, `name` do padrao). Aplicada ao `SKILL.md` da 2.14.0, ela reprova os dois defeitos. Verificador de 84 para 88.
- Bump 2.14.1 (frontmatter, prosa, marcadores core, specs, loop e github nos assets, nos partials e na raiz) e secao no CHANGELOG da skill. Portao 7/7.
- Feito pelo coordenador, sem subagente: um paragrafo e o bump.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, os tres partials, `evals/verify_repository.py`, `evals/portao_t110.py` (novo); `AGENTS.md`; `docs/TASKS.md`, `docs/MEMORY.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Do usuario: o texto do `description`. Do coordenador: tirar os dois-pontos do texto aprovado (mesmo conteudo, pontuacao diferente) e cobrar o frontmatter no verificador.

### Aprendizados Para MEMORY.md

- Promovido (Armadilha): ferramenta que carrega a skill nao prova YAML valido; o frontmatter agora e cobrado pelo verificador.

### Pendencias

- Thread da spec 0008: rebasear o PR #5 sobre a 2.14.1 e seguir para a T-102 (2.15.0).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): a thread da spec 0008.
- Motivo: a 2.15.0 so esperava a 2.14.x.

## 2026-10-21 - Claude Opus 5.5 (coordenador) com subagentes Sonnet 5.5 (spec 0007 e T-104, skill 2.14.0)

### Objetivo

- Executar a spec 0007 (modulo `github`) e a T-104 ate a skill 2.14.0 publicada, depois de o usuario aceitar a recomendacao para P-1 a P-4 ("P-1 a P-4 como voce recomendou"). Sessao Cloud (Cloudroom). Trabalho num `git worktree` em `/tmp/wt-0007` (branch `spec-0007/github`), porque a thread da spec 0008 trabalhava na pasta principal; subagentes Sonnet 5.5 por `room-cli thread spawn --shared-sandbox`, um por vez, com a ordem de trabalhar so no worktree; revisao do coordenador a cada retorno.

### O Que Foi Feito

- **Planejamento:** P-1 a P-4 viraram DEC-004 a DEC-007 na spec 0007 (DEC-005 complementa a DEC-003: o `ci.yml` gerado valida a estrutura em passo proprio, alem do comando de `QUALITY.md`), spec `Definida`, T-105 fechada, T-106 a T-109 criadas, e cinco portoes escritos antes do trabalho (`portao_t104.py`, `portao_t106.py` a `portao_t109.py`), todos falhando pelo motivo certo.
- **T-106** (Sonnet): `assets/github/en/` e `pt-BR/`, 10 arquivos cada, e o partial. Covenant 2.1 baixado do site oficial nas duas linguas e conferido por diff (so a linha de contato muda). Revisao: tirei "ou na skill" do CONTRIBUTING, "nunca apague a branch" virou "nunca apague `main`", e o partial passou a citar o passo do validador. 11/11.
- **T-104** (Sonnet): `corrida_incompleta()` no validador, so leitura; fixtures `origem-project` com tres casos; o `{}` de manifesto em `portao_t078.py` virou manifesto valido (dado de teste, T-078 segue 14/14). Mutacao derrubou portao e verificador. 12/12.
- **T-107** (Sonnet): bloco `github` no validador e no verificador, fixture `github-project`. O check 7 do meu portao procurava a chave errada da fixture; o subagente contornou com uma constante, eu consertei o portao e tirei a constante. Verificador de 78 para 84. 9/9.
- **T-108** (Sonnet): pergunta 5, `references/github.md` (111 linhas, flags de `gh` conferidas por `--help`), README da skill, excecao de `.github/` na raiz minima, evals 13 e 14. Achado na revisao: o `description` do `SKILL.md` tem 1479 caracteres, acima dos 1024 do padrao Agent Skills (ja eram 1394 na 2.13.0): T-110. 9/9.
- **T-109** (Sonnet, arquivos): bump 2.14.0, CHANGELOG da skill, dogfood do bloco `github` na raiz, regra de `AGENTS.md` e `docs/CONTRIBUTING.md` apontando para `references/github.md`. O subagente encerrou o turno com os portoes em segundo plano e sem resultado; rodei os cinco portoes, o verificador e o `--strict` eu mesmo e parei a thread dele. 6/6.
- **Publicacao:** PR #6 com `ci` verde em Linux e macOS, squash `bc06ccc`; tag anotada `v2.14.0`; o `release.yml` rodou pelo push da tag pela primeira vez (run 39663549782, todos os passos em success), Release 2.14.0 Latest, 58 arquivos no zip (20 do modulo, nada do adaptador da 0008, cujo PR #5 segue sem merge), `sha256sum -c` OK no asset baixado.
- **Ponta a ponta do `ci.yml` gerado:** o passo de validacao, extraido do template com `SKILL_VERSION=2.14.0`, baixou da Release real, conferiu o `.sha256` e validou um projeto montado dos assets (0 erros, 0 avisos); com um travessao injetado, exit 1. A sandbox nao tem `unzip` (o `ubuntu-latest` tem); usei um substituto com `python3 -m zipfile`.
- Reinstalada com `install.sh --sim` em `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`: `version: "2.14.0"` e `assets/github/` nos tres.

### Arquivos Criados Ou Alterados

- Pelo PR #6: skill inteira da 2.14.0 (`SKILL.md`, `CHANGELOG.md`, `README.md`, `scripts/validate_structure.py`, `references/github.md`, `references/atualizacao.md`, `assets/github/`, `assets/partials/AGENTS-github-block.md`, marcadores dos assets e partials, `assets/docs/QUALITY.md`, `evals/`), `AGENTS.md`, `docs/CONTRIBUTING.md`, `docs/TASKS.md`, `docs/specs/0007-modulo-github.md`. Por este commit: `docs/TASKS.md`, `docs/specs/0007-modulo-github.md`, `docs/PROJECT_CONTEXT.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, e `docs/archive/SESSIONS-2026.md` com `docs/archive/README.md` (rotacao por tamanho das duas entradas mais antigas).

### Decisoes Tomadas

- Do usuario: P-1 a P-4 como recomendado. Do coordenador, registradas na evidencia: T-109 com arquivos pelo Sonnet e publicacao pelo coordenador; `description` longo vira tarefa, sem corte por conta propria; spec 0007 `Concluida` com a evidencia preenchida.

### Aprendizados Para MEMORY.md

- Promovido (Armadilha): subagente que manda portoes demorados para segundo plano encerra o turno sem resultado; o coordenador roda os portoes ou pede primeiro plano.

### Pendencias

- Do usuario: T-110 (quais gatilhos do `description` cortar).
- Thread da spec 0008: PR #5 pode ser rebaseado sobre `main` e seguir para a T-102 (2.15.0), liberada pela 2.14.0.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): a thread da spec 0008, para rebasear o PR #5 e fazer a T-102; Sonnet executa, Opus revisa.
- Motivo: a DEC-009 da spec 0008 so esperava a 2.14.0, que saiu.

## 2026-10-21 - Claude Opus 5.5 (gestor) com subagentes Sonnet 5.5 (spec 0008: T-100 e T-101)

### Objetivo

- Executar so T-100 e T-101 da spec 0008, como pediu a thread de coordenacao: branch propria `spec-0008/adaptador`, PR aberto com `ci` verde nos dois sistemas, sem merge ate a tag `v2.14.0`; sem tocar `SKILL.md`, CHANGELOG da skill, versao nem `assets/`. Sonnet executa, Opus revisa (papeis em `docs/MEMORY.md`).

### O Que Foi Feito

- Estado conferido antes: `main` limpo em `a1e370f`, adaptador inexistente, T-100 0/17 e T-101 0/6.
- T-100 pelo subagente `cr_child_6cf7253bdcde35eb49218731` (Sonnet 5.5, `--shared-sandbox`): `scripts/cloudroom_agente.py`. Parou em 16/17 e apontou defeito do portao: o check 11 passava 262145 bytes num argumento so, e o Linux limita cada argumento a 131072 bytes. Consertei o portao (runpy num subprocesso, prompt lido de arquivo) e o detalhe do check 1 que imprimia "import fora da stdlib" mesmo passando. 17/17; cinco mutacoes no adaptador, todas acusadas.
- T-101 pelo subagente `cr_child_8b37e51c58deeda7350a346d`: `evals/test_cloudroom_agente.py` (56 verificacoes, `loop.sh` de ponta a ponta incluido) e etapa em `verify_repository.py` (81/81). 22 mutacoes do subagente, todas acusadas; uma minha (sem `--all`), acusada.
- T-100 e T-101 em "Concluidas" com evidencia; commit, push e PR nesta branch.

### Arquivos Criados Ou Alterados

- Criados: `docs/skills/ai-project-structure/scripts/cloudroom_agente.py`, `docs/skills/ai-project-structure/evals/test_cloudroom_agente.py`.
- Alterados: `docs/skills/ai-project-structure/evals/portao_t100.py`, `docs/skills/ai-project-structure/evals/verify_repository.py`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Nenhuma formal. Do gestor: o conserto do check 11 e no portao, nao no adaptador (o limite e do sistema operacional, e o adaptador ja recusa acima de 262144 bytes).

### Aprendizados Para MEMORY.md

- Candidato, nao promovido: no Linux nenhum argumento passa de 131072 bytes, entao prompt acima disso nao chega a nenhum agente pelo `loop.sh` (que passa o prompt por argv); portao que testa prompt grande tem de passar por arquivo. Promover se aparecer de novo fora desta spec.
- O subagente registrou: filho que pergunta na resposta sem gravar `.loop-pergunta` nao leva a tarefa para "Aguardando Usuario", o portao decide; e o exit 4 no `--tempo-maximo` depende de o adaptador nao escrever nada no projeto.

### Pendencias

- Merge do PR so depois da tag `v2.14.0` (spec 0007). T-102 e T-103 esperam a 2.14.0.
- Riscos para a bancada real (T-103): `busy` falso sem `reply` tres vezes seguidas vira exit 2 (se a CLI real reportar ocioso antes do turno comecar); SIGTERM ao grupo que derrube o proprio `room-cli spawn` sai 1, nao 143.
- `Status` da spec 0008 segue `Rascunho`; passar a `Em andamento` (ou `Definida` antes) e do usuario.

### Proximo Passo Recomendado

- Agente sugerido: a thread de coordenacao, para a spec 0007 e a tag `v2.14.0`; depois esta frente faz o merge e a T-102 (Sonnet executa, Opus revisa). Qualquer agente serve se tiver contexto suficiente.

## 2026-10-21 - Claude Opus 5.5 (coordenacao entre as specs 0007 e 0008)

### Objetivo

- Organizar o trabalho depois de duas threads agirem na mesma pasta sobre as mesmas pendencias: o usuario parou a thread do planejamento da spec 0008 e pediu a esta que arrumasse o estado e dissesse o que mandar para la.

### O Que Foi Feito

- Conferido que a outra thread parou (nada escrito desde 17:06, nenhum `scripts/cloudroom_agente.py`, nenhum filho aberto). Portoes na arvore como ela deixou: validador `--strict` 0 e 0, verificador 78/78, T-100 0/17, T-101 0/6, T-102 3/14, T-103 1/4, todos falhando porque o adaptador nao existe.
- Commit `65153b2`: o planejamento da spec 0008 como a outra thread deixou, sem alteracao (spec com DEC-001 a DEC-009, `mock_room_cli.py`, quatro portoes, rodada cega `2026-10-21-161813-debate`, decisao do adaptador fora do consenso, rotacoes).
- Item 5 da lista que esta thread propos (0008 na 2.14.0) cancelado: contradizia a DEC-009 da spec 0008, que o usuario ja tinha decidido na outra thread (0007 primeiro, na 2.14.0; 0008 na 2.15.0). Vale a decisao registrada.
- Item 3: entrada da rodada 1 da T-083 `arquivado` (falha de ambiente, julgamento escrito); entrada da rodada 2 `resolvido`, julgamento redigido por esta thread e ratificado pelo usuario; decisao em `DECISIONS.md`; T-104 aberta para o validador.
- Item 4: spec 0006 `Concluida` (evidencia ja preenchida, nenhuma tarefa aberta).
- Ordem entre specs escrita no backlog: nota na T-100 (branch propria, PR sem merge ate `v2.14.0`, porque o zip da Release empacota `scripts/` inteiro); T-105 em "Aguardando Usuario" com P-1 a P-4 da spec 0007 e a recomendacao.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Do usuario, no chat: "divide assim" (thread da 0008 com T-100 a T-103; esta com o resto), itens 1 a 4 como recomendado.
- Do agente: o PR de T-100 e T-101 so mergeia depois da tag `v2.14.0`; a outra thread nao cria T-ID novo.

### Aprendizados Para MEMORY.md

- Nenhum promovido. Candidato: duas threads na mesma pasta sem dono declarado por arquivo repetem trabalho; so promover se repetir.

### Pendencias

- Do usuario: T-105 (P-1 a P-4 da spec 0007).
- Thread da spec 0008: T-100 e T-101 em branch, PR aberto sem merge.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): a thread da spec 0008 (Sonnet executa, Opus revisa) para T-100 e T-101; esta thread para a spec 0007 depois da T-105.
- Motivo: as duas frentes so se cruzam em `verify_repository.py` e no bump, e a ordem acima resolve as duas.

## 2026-10-21 - Claude Opus 5.5 (execucao da camada GitHub: PRs, tags e Releases)

### Objetivo

- Executar as acoes externas de T-092 a T-098 depois do "sim para tudo" do usuario, na ordem da entrada anterior (camada GitHub escrita e revisada). Sessao Cloud (Cloudroom), na mesma pasta em que outra sessao planejava a spec 0008 sem commitar: os commits sairam de `git worktree` em `/tmp` e levaram so os arquivos e trechos desta camada.

### O Que Foi Feito

- **PR #2** (`ci/portoes`, so `.github/workflows/ci.yml`): `ci` verde em ubuntu-latest (1m03s) e macos-latest, squash em `main` como `3b7a03b`. O `find -newer` de `loop.sh` nao quebrou no Linux: T-093 fecha sem patch.
- **Tags**: doze anotadas, v2.4.0 a v2.12.0, com `GIT_COMMITTER_DATE` da data de cada commit; cada SHA conferido contra o `version:` do `SKILL.md` naquele commit. Depois do PR #3, `v2.13.0` em `a480ed0`.
- **Furo no plano anterior, achado antes de taguear**: push de tag roda o workflow que existe no commit tagueado, e `a480ed0` e anterior ao `release.yml`; a tag `v2.13.0` nunca disparava a Release. Conserto no PR #3: `workflow_dispatch` com entrada `tag` (checkout `refs/tags/<tag>`, `TAG` e `concurrency` pela entrada).
- **PR #3** (`github/camada`): comunidade, `release.yml`, READMEs, spec 0007 e o registro da sessao anterior, sem os trechos da sessao da spec 0008 (montados por script a partir da arvore compartilhada); validador `--strict` 0 e 0 e verificador 78/78 no worktree; `ci` verde nos dois sistemas; squash `c19197d`. CI de `main` em `c19197d`: success.
- **Token sem permissao**: `POST .../rulesets` e `gh workflow run release.yml` deram HTTP 403 (o token tem contents e pull requests, nao Administration nem Actions: write). Releases 2.12.0 e 2.13.0 publicadas rodando localmente os passos do proprio `release.yml` (lidos do YAML por script) no checkout de cada tag, 2.12.0 antes para a 2.13.0 ficar Latest: 35 e 36 arquivos, `sha256sum -c` OK no asset baixado. A 2.12.0 ganhou zip e checksum em vez do corpo manual planejado.
- **Ruleset**: ao montar o JSON, apareceu que check obrigatorio em ruleset tambem rejeita push direto em `main`, contra a regra de `AGENTS.md` que deixa mudanca so em `docs/` ir direta. Proposta em T-094: dois rulesets (abaixo). Nada criado.
- Conferencias: perfil de comunidade em 100; badge do CI `passing`; badge de Release em v2.13.0.
- Registro: T-092, T-093, T-095, T-096 e T-098 em Concluidas com evidencia; T-094 e T-097 continuam em "Aguardando Usuario" com pergunta nova; Armadilha nova em `MEMORY.md`; linha no `CHANGELOG.md`. Commit de docs direto em `main`.
- **Segunda volta, depois de o usuario conceder Administration e Actions: write e escolher os dois rulesets pela recomendacao do agente**: rulesets `main` (25565596) e `main-ci` (25565599) criados e ativos, bypass do admin conferido (`current_user_can_bypass: always`); T-094 fechada. Release 2.13.0 apagada (tag mantida) para o workflow republicar; o dispatch deu HTTP 422 porque `runner.temp` nao vale no `env` do job, entao o `release.yml` nunca tinha sido aceito pelo GitHub, nem em push de tag. A simulacao local rodava o script de cada passo direto e nao avaliava as expressoes `${{ }}`. Conserto no PR #4 (`0d066cd`), conferido com `actionlint` 1.7.12 (acusa a versao antiga, limpo na nova); run 39637733376 em success, Release 2.13.0 Latest por `github-actions[bot]`, `sha256sum -c` OK; T-097 fechada. A Release ficou fora do ar por cerca de 10 minutos, e nao 1 como avisado, por causa do conserto.

### Rulesets Propostos (T-094)

```bash
gh api -X POST repos/adejaimejr/ai-project-structure/rulesets --input - <<'JSON'
{"name": "main", "target": "branch", "enforcement": "active",
 "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
 "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}], "bypass_actors": []}
JSON
gh api -X POST repos/adejaimejr/ai-project-structure/rulesets --input - <<'JSON'
{"name": "main-ci", "target": "branch", "enforcement": "active",
 "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
 "rules": [{"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": false,
   "do_not_enforce_on_create": false, "required_status_checks": [{"context": "ci", "integration_id": 15368}]}}],
 "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]}
JSON
```

### Arquivos Criados Ou Alterados

- Pelo PR #3: `.github/workflows/release.yml` (`workflow_dispatch`). Por este commit: `docs/TASKS.md`, `docs/SESSION.md`, `docs/MEMORY.md`, `docs/CHANGELOG.md`. No GitHub: tags v2.4.0 a v2.13.0, Releases 2.12.0 e 2.13.0, branches `ci/portoes` e `github/camada` (mergeadas, nao apagadas).

### Decisoes Tomadas

- Do usuario: "sim para tudo". Do agente, registradas na evidencia: `workflow_dispatch` no `release.yml`; Releases pelos passos do workflow rodados localmente; dois rulesets propostos, nao criados.

### Aprendizados Para MEMORY.md

- Promovido (Armadilha): tag em commit anterior ao workflow nao o dispara; o token `gh` da sandbox nao tem Administration nem Actions: write.

### Pendencias

- Nenhuma da camada GitHub: T-092 a T-099 concluidas. Candidato a tarefa futura, nao aberto: rodar `actionlint` no CI quando `.github/workflows/` mudar.
- O trabalho da sessao da spec 0008 continua sem commit na arvore compartilhada, como ela pediu.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto, para a spec 0007 (modulo `github`, skill 2.14.0) ou a execucao da spec 0008; a tag `v2.14.0` sera o primeiro push de tag a disparar o `release.yml`.
- Motivo: a camada GitHub do repositorio esta completa; o proximo trabalho e a skill.
