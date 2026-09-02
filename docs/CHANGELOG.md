# CHANGELOG

Historico de mudancas relevantes.

## 2026-09-02 (skill v2.2.0)

- Evidencia de fechamento obrigatoria em tarefa concluida, marcador `(verifica: <comando>)` opcional em tarefa aberta, secao `## Aguardando Usuario` em `TASKS.md` e campos declarativos (`Metodo`, `Exposicao previa a outras posicoes`, `Rodada`) em `CONSENSUS.md`. Bloco core e templates em v2.2.0.
- A regra nao e retroativa: a data de adocao fica no marcador `(convencoes-2-2-0-desde:)` do proprio `TASKS.md`, e nada anterior a ela e cobrado.
- `validate_structure.py` com os checks correspondentes; `evals/verify_repository.py` novo, provando a integridade do repositorio em um comando; fixture `aguardando-project` e eval 9.
- Dogfood: `docs/TASKS.md` e `docs/CONSENSUS.md` adotaram as convencoes, os 4 headings ausentes de `SESSION.md` foram corrigidos e `SESSION.md`/`CONSENSUS.md` foram rotacionados para `docs/archive/`.
- Comando de integridade registrado em `docs/QUALITY.md`, secao "Testes E Validacao".
- Criterios de aceite sem runner exercitados na mao (scaffold minimal, scaffold completa e atualizacao de um projeto 2.1.0), com quatro correcoes: tres de texto e uma no validador, que tratava qualquer `T-NNN` da linha como ID da tarefa.

## 2026-08-20 (publicacao no GitHub)

- Repositorio git inicializado a pedido do usuario e publicado como publico em `github.com/adejaimejr/ai-project-structure` (branch `main`, estado da skill 2.1.0).
- Adicionados `README.md` (apresentacao para visitantes) e `LICENSE` (MIT) na raiz, com excecao a regra de raiz minima registrada em "Regras Do Projeto" do `AGENTS.md`.

## 2026-08-20 (skill v2.1.0)

- Novo template opcional `docs/STACK.md`: mapa de tecnologias, pacotes principais e documentacao oficial, com "Onde Consultar Primeiro" para o agente ir direto na fonte certa. Incluido no nivel "completa" do scaffold.
- `validate_structure.py --progress`: projecao somente-leitura de tarefas por secao e specs (status, concluidas/total, perguntas abertas).
- Bloco core do `AGENTS.md` atualizado para v2.1.0 (STACK.md em "Onde Escrever Cada Coisa" + gatilho de atualizacao); evals atualizados (eval 8 novo).
- Dogfood: `docs/STACK.md` do meta-projeto preenchido; spec `0002-stack-e-progresso` criada e concluida; skill reinstalada com paridade nos tres destinos.

## 2026-08-20 (skill v2.0.0)

- Skill `ai-project-structure` atualizada para 2.0.0, inspirada na analise da metodologia specsfy (o que foi importado e descartado esta em `docs/DECISIONS.md`).
- Novidades da skill: entrevista numerada com opcoes, regra "Nunca Inferir", `TASKS.md` com IDs `T-NNN`, blocos gerenciados com versao em `AGENTS.md`, validador Python (`scripts/validate_structure.py`), modulo opcional de specs (`docs/specs/`), fluxos de atualizacao e specs em `references/`, 7 evals com fixtures, CHANGELOG proprio da skill.
- Regra nova em todo o projeto e no core da skill: travessao (em dash, U+2014) proibido; validador acusa como erro.
- Meta-projeto atualizado para a propria v2 (dogfood): `AGENTS.md` com blocos gerenciados e specs ativo, `TASKS.md` migrado para T-IDs, spec `0001-skill-v2` criada, `PROJECT_CONTEXT.md` preenchido, `ROADMAP.md` revisado, entrada antiga do `CONSENSUS.md` recebeu `Status`.
- Skill reinstalada nas tres ferramentas com paridade verificada.
- Validacao da v2.0.0 concluida: 21 execucoes de eval (7 cenarios x Claude Code, Codex CLI e Gemini CLI), 21 aprovadas, mais o fluxo de atualizacao v1 para v2 testado de ponta a ponta. Spec `0001-skill-v2` marcada como Concluida.
- Ajuste no `expected_output` do eval 4 apos a rodada: o texto nao dizia o que esperar do validador depois da entrevista e as tres ferramentas divergiram na leitura. Muda apenas `evals/`, que o `install.sh` nao propaga.

## 2026-04-25

- Criada estrutura Markdown multiagente.
- Criados arquivos de entrada `AGENTS.md`, `CLAUDE.md` e `GEMINI.md`.
- Criada memoria do projeto em `docs/`.
- Adicionados `SESSION.md` e `CONSENSUS.md`.
- Adicionados prompts reutilizaveis.
- Adicionada skill portavel `ai-project-structure`.

## 2026-04-25 (atualizacao da estrutura)

- Adicionado `docs/MEMORY.md` como memoria persistente (User / Feedback / Project / Reference).
- Adicionado `docs/archive/` com indice para rotacao de `SESSION.md` e `CONSENSUS.md`.
- `AGENTS.md` revisado: imutabilidade dos arquivos-ponte, dois niveis de leitura (trivial vs relevante), regra de desempate, atualizacao por gatilho, politica de rotacao e criterio de "onde escrever cada coisa".
- Templates de `SESSION.md` e `CONSENSUS.md` atualizados (handover direcionado, `Status`, `Proximo passo`, secao de aprendizados para `MEMORY.md`).
- `QUALITY.md` atualizado com checklist de atualizacao por gatilho.
- Skill `ai-project-structure` sincronizada com a estrutura nova.

## 2026-05-26 (skill instalavel cross-tool)

- Skill `ai-project-structure` empacotada para o **Agent Skills Open Standard** (mesmo `SKILL.md` lido por Claude Code, Codex CLI e Gemini CLI).
- Adicionado `docs/skills/ai-project-structure/install.sh` (instala global ou por-projeto; flags por ferramenta; `--uninstall`; idempotente).
- Adicionado `docs/skills/ai-project-structure/README.md` com caminhos de instalacao e uso por ferramenta.
- Adicionado metadado opcional do Codex em `docs/skills/ai-project-structure/agents/openai.yaml`.
- Skill instalada globalmente em `~/.claude/skills/`, `~/.agents/skills/` (Codex) e `~/.gemini/skills/`.
- Corrigido registro anterior: o caminho oficial do Codex e `~/.agents/skills/`, nao `~/.codex/skills/`; a instalacao de 2026-04-25 nao havia persistido em nenhum host.

## 2026-05-26 (revisao Codex da skill)

- Revisada a parte Codex da skill `ai-project-structure` contra a documentacao oficial atual do Codex.
- `agents/openai.yaml` ajustado: `short_description` reduzida para o intervalo recomendado e `default_prompt` passou a mencionar `$ai-project-structure`.
- `README.md` ajustado para invocacao explicita atual do Codex (`/skills` ou `$ai-project-structure`) e nota sobre a convencao recomendada de evals com `codex exec --json`.
- A fonte canonica foi corrigida, mas a propagacao via `install.sh` ficou pendente porque a execucao fora do workspace nao foi aprovada nesta sessao.
