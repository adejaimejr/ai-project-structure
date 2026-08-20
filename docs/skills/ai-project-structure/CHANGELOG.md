# CHANGELOG - skill ai-project-structure

Historico de versoes da skill. A versao canonica vive no frontmatter do `SKILL.md`.

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
