# Spec 0007 - Modulo opcional `github` (skill 2.14.0)

**Status:** Em andamento
**Criada em:** 2026-10-21
**Esforco:** M. Toca validador, verificador, `SKILL.md`, assets, referencia, evals e fixture, mas tudo no molde ja existente dos modulos specs e loop; nenhum mecanismo novo.

## Problema E Resultado Esperado

- Problema: a comparacao de 2026-10-20 com o `ai-memory` (entrada em `docs/SESSION.md` e decisao "Camada GitHub do repositorio" em `docs/DECISIONS.md`) mostrou que este repositorio tinha 12 versoes minor da skill e nenhuma tag, nenhum workflow, descricao e topics vazios e health de comunidade em 28%. Nada disso e defeito da estrutura: e a camada que o GitHub exibe primeiro, e que a skill nao gera. Todo projeto novo criado pela skill nasce com o mesmo vazio.
- Problema: os dois portoes do repositorio (`verify_repository.py` e `validate_structure.py . --strict`) rodavam so na maquina do mantenedor, em macOS. O PR #1 mostrou que no Linux o harness quebrava por `sed -i ""` e `find -newer`. Um projeto que usa a estrutura tem em `docs/QUALITY.md`, secao "Testes E Validacao", o comando que um CI deveria rodar, e essa informacao fica parada.
- Resultado esperado: um modulo opcional `github`, no molde de specs e loop, que ativado sob demanda entrega ao projeto a camada GitHub decidida em 2026-10-20: arquivos de comunidade (em ingles ou em pt-BR, escolha do usuario), templates de issue e PR, `dependabot.yml`, um `ci.yml` que roda o comando de "Testes E Validacao" de `QUALITY.md`, e um bloco gerenciado em `AGENTS.md` com as regras de fluxo (PR, tag, release, raiz minima com `.github/`).
- Resultado esperado: projeto que nao ativa o modulo nao paga nada por ele, nem em instrucao no bloco core, nem em arquivo. Este repositorio ativa o modulo em si mesmo no fim, e a camada aplicada a mao por T-092 a T-098 passa a ser gerida pela skill.

## Escopo

### Incluido

- Bloco gerenciado `<!-- ai-project-structure:github:start vX.Y.Z -->` e `github:end` em `AGENTS.md`, inserido apos o ultimo bloco gerenciado e antes de "## Regras Do Projeto", com conteudo em `assets/partials/AGENTS-github-block.md` (pt-BR, como os partials de specs e loop). O bloco traz as regras ja aplicadas em "Regras Do Projeto" deste repositorio: raiz minima com a excecao de `.github/` e dotfiles e comunidade em `docs/`; idioma da camada GitHub; mudanca em codigo ou skill por PR com CI verde; tag anotada `vX.Y.Z` a cada bump e Release; configuracao do repositorio pela CLI `gh`.
- `assets/github/en/` e `assets/github/pt-BR/`, mesma lista de arquivos nas duas linguas: `docs/CONTRIBUTING.md`, `docs/SECURITY.md`, `docs/CODE_OF_CONDUCT.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, `.github/ISSUE_TEMPLATE/config.yml` (`blank_issues_enabled: false`), `.github/dependabot.yml` (so `github-actions`, mensal), `.gitattributes` (`* text=auto eol=lf`) e `.github/workflows/ci.yml`. Os textos nascem dos arquivos de T-096 deste repositorio, generalizados (sem o nome deste repositorio, sem os dois portoes especificos).
- `ci.yml` gerado com um passo placeholder para o comando de "Testes E Validacao" de `docs/QUALITY.md` do projeto-alvo, preenchido na ativacao. Quando a secao estiver vazia ou com o texto do template, a ativacao avisa e deixa o placeholder visivel, nunca inventa comando (regra "Nunca Inferir"). Actions fixadas por SHA completo com versao em comentario, `permissions: contents: read`, `concurrency` cancelando rodada anterior. `release.yml` fica fora (DEC-001).
- `references/github.md`: ativacao em projeto existente (passo a passo, como `references/specs.md` e `references/loop.md`), checklist de configuracao do repositorio via `gh` (descricao, topics, ruleset de `main`, labels, Wiki e Projects), e fluxo bump, tag anotada, release. Este repositorio hoje guarda esse checklist em `docs/CONTRIBUTING.md` ate a 2.14.0, por regra em `AGENTS.md`.
- Pergunta 5 na entrevista do `SKILL.md`: ativar o modulo `github`, com a lingua dos arquivos como sub-opcao (en, pt-BR). O default e pergunta aberta (P-1).
- `validate_structure.py`: `MARKER_RE` aceita `github`; codigos `GITHUB-*` para bloco despareado, sem versao ou com versao divergente dos demais blocos, no mesmo nivel que os codigos equivalentes de specs e loop. O validador nao checa a existencia nem o conteudo dos arquivos de `.github/` e `docs/` gerados (fora da fronteira do validador, que confere a estrutura Markdown).
- `verify_repository.py`: regex do bloco `github` na lista de blocos, tupla de versao incluindo o marcador `github`, e etapa que compara o bloco da raiz com o partial (paridade), como ja faz para specs e loop.
- `evals/evals.json`: dois evals novos, ativar o modulo em projeto existente e scaffold com a pergunta 5 respondida. Correcao ao texto de T-099: a tarefa dizia "evals 12 e 13", mas `evals.json` ja tem 12 entradas (a 12 e a do consenso, da 2.13.0); os novos sao 13 e 14.
- Fixture `evals/fixtures/github-project/`: projeto com o modulo ativo, usado pelo verificador para provar que o validador aceita o bloco e acusa as mutacoes (bloco despareado, versao divergente).
- Prosa da raiz minima nos templates: `assets/docs/QUALITY.md` ("A raiz mantem apenas os arquivos Markdown de entrada dos agentes") e `SKILL.md` ganham a excecao de `.github/` e dotfiles quando o modulo esta ativo.
- Bump para 2.14.0: `version` do `SKILL.md`, marcadores `core`, `specs`, `loop` e `github` em v2.14.0, secao no CHANGELOG da skill, tag `v2.14.0` e Release (regra do projeto).
- Dogfood: este repositorio ativa o modulo em si mesmo no fim da spec, e `verify_repository.py` passa a cobrar a paridade do bloco `github` da raiz.

### Fora Do Escopo

- `release.yml` como asset do modulo (DEC-001). Fica so neste repositorio (T-097), porque empacota uma skill; projeto comum nao tem o que empacotar.
- Executar `gh` pela skill: a configuracao do repositorio e checklist em `references/github.md`, feita pela pessoa ou pelo agente de chat com o sim dela. A skill nao roda comando com efeito externo (coerente com "Nao inicialize repositorio git" do `SKILL.md`).
- Traduzir a skill, o bloco core ou a memoria em `docs/` para ingles. So os arquivos da camada GitHub tem versao em ingles.
- Qualquer mudanca no bloco core por causa deste modulo.
- Ativacao automatica no scaffold sem resposta explicita na pergunta 5.

## Criterios De Aceite

Estrutura e nao contaminacao (molde de specs e loop):

- Projeto sem o modulo ativado nao ganha nenhum arquivo em `.github/`, nenhum arquivo de comunidade, nenhum marcador `github` e nenhuma linha nova no `AGENTS.md`.
- Ativacao insere o bloco `github` entre o ultimo bloco gerenciado e "## Regras Do Projeto", em v2.14.0, com conteudo identico ao partial; `verify_repository.py` exige a paridade e sai diferente de 0 com divergencia induzida.
- Ativacao copia a lista completa de arquivos da lingua escolhida, sem sobrescrever arquivo existente sem confirmacao por item (regra geral do `SKILL.md`).
- `ci.yml` gerado traz o comando de "Testes E Validacao" de `QUALITY.md` do projeto-alvo no passo de teste, ou o placeholder visivel com aviso quando a secao nao tem comando real. Nenhum comando inventado.
- Nenhum travessao (U+2014) em arquivo novo ou alterado, nas duas linguas.

Validador e verificador:

- `validate_structure.py` aceita bloco `github` bem formado sem aviso e emite codigo `GITHUB-*` para bloco despareado, sem versao ou com versao diferente dos outros blocos; o fixture `github-project` prova os dois lados.
- `verify_repository.py` cobre o bloco `github` na paridade e na coerencia de versao, e o total sobe pelo numero de checks novos (piso atualizado no proprio verificador).
- Os dois portoes do repositorio continuam verdes em Linux e macOS pelo `ci.yml` de T-092.

Entrevista e documentacao:

- Pergunta 5 aparece no scaffold com opcoes numeradas; sem resposta, a skill nao ativa.
- `references/github.md` existe e e citado no `SKILL.md`, no `README.md` da skill e no `CHANGELOG.md` da skill.
- Este repositorio, apos ativar o modulo em si mesmo, continua com `verify_repository.py` verde e `validate_structure.py . --strict` em 0 erros e 0 avisos.

Criterios das respostas (DEC-004 a DEC-007):

- Pergunta 5 com default "Nao"; sub-opcao de lingua so no sim.
- `ci.yml` gerado com passo que baixa zip e `.sha256` da Release fixada, roda `sha256sum -c` e `validate_structure.py . --strict`, e passo separado com o comando de `QUALITY.md`.
- `CODE_OF_CONDUCT.md` (default sim) e `.gitattributes` (default nao) perguntados item a item; o resto entra sempre.
- Arquivo existente e pulado e listado no relatorio, nunca mesclado.

## Decisoes

Herdadas da decisao "Camada GitHub do repositorio" (2026-10-20, `docs/DECISIONS.md`), sem nova discussao: raiz minima com `.github/` e dotfiles; comunidade em `docs/`; ingles por padrao na camada GitHub com pt-BR como opcao; tag anotada e Release a cada bump; PR com CI para mudanca na skill; modulo `github` na 2.14.0.

Desta spec, decididas pelo usuario em 2026-10-20 ao escrever T-099:

- DEC-001: `release.yml` nao e asset do modulo. Motivo: ele empacota a skill deste repositorio; projeto comum nao tem pacote para publicar, e um workflow de release generico sem artefato seria cerimonia. O fluxo bump, tag, release vai em `references/github.md` como checklist, nao como YAML.
- DEC-002: o bloco gerenciado e em pt-BR; so os arquivos copiados para o projeto tem versao em ingles. Motivo: `AGENTS.md` e a memoria em `docs/` seguem em pt-BR por decisao de 2026-10-20; o bloco e regra de agente, nao camada GitHub.
- DEC-003: o `ci.yml` gerado roda o comando de "Testes E Validacao" de `QUALITY.md`, e so ele. Motivo: e o mesmo portao que o loop usa para ativar (0003/DEC-005 e 0004); o CI nao inventa uma segunda definicao de "passou". Complementada pela DEC-005: o validador da estrutura entra como passo proprio, porque confere a estrutura Markdown, nao o produto.

Respostas as Perguntas Abertas, aceitas pelo usuario em 2026-10-21 no chat ("P-1 a P-4 como voce recomendou"):

- DEC-004 (P-1): a pergunta 5 da entrevista tem default "Nao, da para ativar depois", como as perguntas 3 e 4, sem pergunta extra sobre repositorio publico. Rejeitada: sugerir "Sim, em ingles" para repositorio publico (exigiria detectar ou perguntar visibilidade, e o modulo continua ativavel depois). Sub-opcao de lingua (en ou pt-BR) so aparece quando a resposta e sim.
- DEC-005 (P-2): o `ci.yml` gerado tem um passo que baixa o zip da Release `vX.Y.Z` da skill (a versao que ativou o modulo, fixada no arquivo) e o `.sha256` da mesma Release, confere com `sha256sum -c` e roda `validate_structure.py . --strict`; o passo seguinte roda o comando de "Testes E Validacao". Limite declarado em `references/github.md`: o `.sha256` vem da mesma Release, entao prova integridade do download, nao autenticidade. Rejeitadas: clone raso pela tag (traz o repositorio inteiro para usar um script) e nao validar a estrutura no CI (deixa o portao da estrutura so na maquina de quem lembra de rodar).
- DEC-006 (P-3): `CODE_OF_CONDUCT.md` e `.gitattributes` sao opcionais e perguntados item a item na ativacao: o codigo de conduta com default sim (e o que leva o perfil de comunidade do GitHub a 100) e o `.gitattributes` com default nao (`eol=lf` muda o checkout em Windows). Os demais arquivos da lista entram sempre.
- DEC-007 (P-4): em projeto que ja tem algum arquivo da lista (em `.github/` ou em `docs/`), a ativacao pula o que existe, nunca mescla, e lista no relatorio o que pulou. Rejeitadas: mesclar (mexer num `ci.yml` alheio e sobrescrever sem confirmacao) e perguntar por item (a resposta util e quase sempre "mantem o meu", e a lista do que pulou ja deixa a pessoa decidir depois).

## Tarefas

- T-099: escrever esta spec em `Rascunho` (status e andamento vivem so em `docs/TASKS.md`).
- T-105: responder P-1 a P-4 e planejar as tarefas.
- T-106: assets do modulo (`assets/github/en/`, `assets/github/pt-BR/`) e partial do bloco.
- T-107: validador e verificador (marcador `github`, codigos `GITHUB-*`, fixture, paridade e versao).
- T-108: entrevista, `references/github.md`, README da skill, prosa da raiz minima e evals 13 e 14.
- T-109: bump 2.14.0, dogfood nesta raiz e publicacao (PR, tag, Release).
- T-104 (validador, consenso da T-083) entra no mesmo bump, sem ser desta spec.

## Perguntas Abertas

- ~~P-1 a P-4~~ Respondidas em 2026-10-21: DEC-004 a DEC-007.
- P-5: nenhuma aberta hoje. Se a execucao achar ambiguidade, ela entra aqui antes de qualquer inferencia.

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
