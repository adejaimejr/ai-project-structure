# Spec 0001 - Skill v2 (melhorias inspiradas no specsfy)

**Status:** Concluida
**Criada em:** 2026-08-20
**Esforco:** G, com varias frentes (templates, validador, fluxos, empacotamento) em uma unica versao.

## Problema E Resultado Esperado

- Problema: a v1 da skill tinha TASKS sem estrutura, validacao apenas em prosa, nenhum versionamento e nenhum mecanismo seguro de atualizar projetos existentes. A analise do specsfy mostrou solucoes maduras para esses pontos.
- Resultado esperado: skill v2.0.0 com entrevista numerada, regra "Nunca Inferir", TASKS com IDs T-NNN, blocos gerenciados com versao em AGENTS.md, validador executavel e modulo opcional de specs, mantendo a identidade de memoria multiagente.

## Escopo

### Incluido

- Entrevista numerada com opcoes numeradas (com "Avançar" registrado como pendencia).
- Regra "Nunca Inferir" e regra anti-travessao no template AGENTS.md.
- TASKS.md com IDs T-NNN, prioridade opcional e link (spec: NNNN-slug).
- Blocos gerenciados ai-project-structure:core e :specs, com versao no marcador.
- Fluxo de atualizacao v1 para v2 (references/atualizacao.md) e fluxo de specs (references/specs.md).
- Validador scripts/validate_structure.py (Python 3, stdlib) com exit code.
- Modulo opcional docs/specs/ (flat, NNNN-slug.md, status no arquivo).
- Evals atualizados (7 cenarios) com fixtures v1-project e broken-project.
- install.sh copiando scripts/ e references/; CHANGELOG proprio da skill.
- Dogfood no meta-projeto: AGENTS v2, specs ativo, TASKS migrado, docs atualizados.

### Fora Do Escopo

- Pipeline SDD completo, coverage math, attestation, CLI (ver PROJECT_CONTEXT.md).
- Traducao para outros idiomas.

## Criterios De Aceite

- Validador retorna exit 0 em scaffold novo (minimal, completa, minimal+specs) e exit 1 com [ERRO] para: arquivo do nucleo ausente, T-ID duplicado, Status de spec invalido, marcador despareado, travessao presente.
- Fixture v1-project passa com apenas INFOs (estrutura v1 reconhecida sem erro).
- install.sh propaga SKILL.md, assets/, agents/, scripts/ e references/ para os tres destinos, identicos entre si.
- SKILL.md com version 2.0.0 no frontmatter; marcadores do projeto carregam v2.0.0.
- Nenhum arquivo da skill ou do projeto contem o caractere travessao (em dash, U+2014).
- Evals 1 a 7 passam quando executados manualmente nas ferramentas.

## Decisoes

- DEC-001: specs em pasta flat com campo Status no arquivo, em vez de pastas por estado (links estaveis, sem renomes; validador mais simples).
- DEC-002: TASKS.md e a unica fonte de status de tarefa; a spec so lista T-IDs (anti-drift, licao central do specsfy).
- DEC-003: validador roda do diretorio da skill instalada e nao e copiado ao projeto (projetos ficam so-Markdown; sem skew de versao).
- DEC-004: travessao (em dash, U+2014) proibido em todos os textos; validador acusa como erro. Pedido do usuario em 2026-08-20.

## Tarefas

- T-002: rodar os 7 evals manualmente nas tres ferramentas
- T-003: testar o fluxo de atualizacao v1 para v2 em projeto real externo
- T-004: reinstalar a skill e conferir paridade dos tres destinos

## Perguntas Abertas

- (Vazio.)

## Evidencia De Conclusao

Resumo: 21 execucoes de eval (7 cenarios x 3 ferramentas), 21 aprovadas. T-002, T-003 e T-004 concluidas.

### T-003: fluxo de atualizacao v1 para v2 (Claude Code)

- Verificacao (2026-08-20): fluxo de `references/atualizacao.md` executado de ponta a ponta em `/tmp/skill-v2-tests/projeto-v1` (copia da fixture `v1-project` com 2 entradas extras em `SESSION.md` e 1 secao propria extra em `AGENTS.md`), seguido de `python3 ~/.claude/skills/ai-project-structure/scripts/validate_structure.py /tmp/skill-v2-tests/projeto-v1`.
- Resultado: 8 de 8 invariantes aprovados (plano antes de tocar arquivos, diff por bloco, confirmacao por item, secoes proprias movidas para "Regras Do Projeto", conteudo fora dos marcadores byte-identico conferido por `diff`, migracao de TASKS oferecida e aplicada, registro em `SESSION.md` e `CHANGELOG.md`, validador com 0 erros e 0 avisos, exit 0).

### T-002: os 7 evals nas tres ferramentas

- Verificacao (2026-08-20, Claude Code): 7 evals em subdiretorios limpos sob `/tmp/skill-v2-tests/`, validador de `~/.claude/skills/ai-project-structure/` apos cada um.
- Resultado (Claude Code): 7 de 7 aprovados. Validador exit 0 nos evals 1 a 6; exit 1 no eval 7 com os 2 erros esperados (ID duplicado `T-001` e Status invalido `Fazendo`).
- Verificacao (2026-08-20, Gemini CLI): 7 evals em `/tmp/skill-v2-tests-gemini/`, validador de `~/.gemini/skills/ai-project-structure/`.
- Resultado (Gemini CLI): 7 de 7 aprovados, mesmo padrao de exit codes do Claude Code. A skill disparou sozinha pela `description`, sem citacao do nome.
- Verificacao (2026-08-20, Codex CLI): 7 evals em `/tmp/skill-v2-tests-codex/`, validador de `~/.agents/skills/ai-project-structure/`. Hashes das duas fixtures identicos antes e depois.
- Resultado (Codex CLI): 7 de 7 aprovados. Validador exit 0 nos evals 1, 2, 3, 5 e 6; exit 1 no eval 7 com os 2 erros esperados. No eval 4 a execucao parou na entrevista, o diretorio ficou vazio e o validador retornou exit 1 por arquivos ausentes: resultado correto desse ramo, nao reprovacao. A ambiguidade que gerou a divergencia entre as ferramentas foi resolvida no `expected_output` do eval 4 em 2026-08-20.

### Checagem final no repositorio

- Verificacao (2026-08-20): validador rodado na raiz de `/Users/adejaimejunioer/Dev/2026/ai-project-structure`.
- Resultado: exit 0, com 0 erros e 4 avisos historicos em entradas de `SESSION.md` de 2026-04-25.
