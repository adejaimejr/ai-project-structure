# CHANGELOG

Historico de mudancas relevantes.

## 2026-09-03 (rodada de P-7 e P-8 da spec 0006)

- Rodada 1 cega sobre as duas perguntas restantes, primeiro uso da DEC-003: os agentes rodaram numa copia com a entrada da rodada anterior retida, e com uma nota dizendo que a omissao era proposital.
- 3 de 3 nas duas: a forma da entrada entra no escopo e a proveniencia entra no escopo. Sobrou calibragem, nao empate.
- Fato que barateia a decisao de forma, conferido no codigo: o validador nunca exigiu heading de posicao nomeado. O congelamento em Codex, Claude e Gemini estava no template, e nao no contrato.
- P-9 nova, e e conflito entre DEC-003 e DEC-006 ja ratificadas: nenhuma das duas escolheu quando a minuta e escrita, e escrita incremental vaza posicao contemporanea pelo repositorio.
- Quatro defeitos do que ja esta publicado viraram T-054, T-055 e T-056.

## 2026-09-03 (spec 0006 com seis decisoes ratificadas)

- Rodada 1 cega com tres posicoes independentes (Claude selado antes das demais, Codex, Grok via `cursor-agent`) respondeu as seis perguntas da spec 0006. Tres unanimes, duas com o Claude vencido por 2 a 1, uma com dissidencia registrada.
- Ratificadas pelo usuario e escritas como DEC-001 a DEC-006 na spec, cada uma declarando como foi decidida.
- DEC-002 subiu para `docs/DECISIONS.md`: a proibicao da 0004/DEC-019 vale para agente e nao para software, e um orquestrador mecanico pode escrever o recorte que a execucao comprova. O que sustenta a excecao e a separacao entre quem opina e quem escreve, nunca a quantidade de agentes.
- Restam P-7 (forma da entrada) e P-8 (proveniencia no escopo), as duas mexendo em escopo, entao a spec segue `Rascunho`.

## 2026-09-03 (fixture debate-project)

- Fixture `debate-project`: projeto que usa consenso e nunca registra achado, com conjunto de diagnosticos vazio em `--strict`. Fecha o ultimo residuo da rodada 2 do achado `0005-A1`. `verify_repository.py` de 42 para 44 verificacoes.
- Provada por mutacao: quebrando `strip_fences`, so ela acusa; as outras cinco fixtures seguem verdes. Muda apenas `evals/`, que nao e distribuido, entao nao houve bump de versao nem reinstalacao.

## 2026-09-03 (skill v2.5.0 publicada)

- 2.5.0 empurrada para o GitHub (`e70bd7c..28681fd`) e instalada nos tres destinos globais. Paridade conferida por `diff -rq`: so `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` ficam de fora, como esperado, e os tres `SKILL.md` instalados declaram `version: "2.5.0"`. A flag `--codigos` chegou nos tres.

## 2026-09-03 (skill v2.5.0)

- Identificador estavel por diagnostico em `validate_structure.py`: os 39 diagnosticos ganharam codigo, e o codigo virou contrato publico. A redacao da mensagem pode melhorar; o codigo so muda em mudanca de versao.
- Flag `--codigos`: `NIVEL|CODIGO|ARQUIVO|SUJEITO`, uma linha por diagnostico. O sujeito e a tarefa, entrada ou spec de que ele fala, e e o que denuncia aviso que passou a cair na entrada errada.
- `verify_repository.py` passou a exigir oracle por fixture (modo, exit e conjunto exato de diagnosticos), com fixture sem oracle recusada. De 40 para 42 verificacoes. `verificar_achado` absorvida pelo mecanismo geral.
- Veio da rodada 2 do achado `0005-A1`, que mostrou que contar linhas `[AVISO]` aceita regressao compensada. Provado por mutacao: com a contagem antiga passava verde, com o conjunto exato reprova.

## 2026-09-03 (skill v2.4.0)

- `CONSENSUS.md` deixa de servir so para debate: entrada que declara `**Achado:** <identificador>` e um achado, com `Status` e `Proximo passo` proprios, disposicao de quem registrou e revalidacao por outro modelo. Identificador livre, conferido por presenca e valor nao vazio.
- `**Escapou de verificacao:** sim | nao` no achado, com a secao "Por Que Nada Pegou Antes" obrigatoria quando for `sim`.
- Teto de tres rodadas removido. Da quarta em diante, a entrada declara `**Pendente da rodada anterior:**`.
- Aviso do ponto cego da validacao cruzada no bloco core, em duas linhas. Antes so existia em `references/loop.md`.
- `validate_structure.py` com os checks do formato de achado, todos AVISO e todos opt-in; fixture `achado-project` e eval 10; `verify_repository.py` de 33 para 40 verificacoes, incluindo o orcamento de linhas do aviso no bloco core.
- Bloco core, templates e marcadores dos tres blocos em v2.4.0.
- Dogfood: primeiro achado do repositorio registrado em `docs/CONSENSUS.md` (`0005-A1`), sobre o proprio padrao de fixture, com a decisao correspondente em `docs/DECISIONS.md`.

## 2026-09-02 (skill v2.3.0 publicada)

- 2.3.0 publicada no GitHub e instalada nos tres destinos globais, apos duas bancadas com agentes reais. Paridade conferida por `diff -rq`; `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` seguem so na fonte canonica, como esperado.

## 2026-09-02 (skill v2.3.0)

- Modulo opcional de loop: a estrutura passa a poder executar uma tarefa verificavel, nao so descreve-la. `references/loop.md`, `assets/partials/AGENTS-loop-block.md`, marcadores `loop` e os scripts `loop.sh` e `loop_task.py`. Nunca entra no scaffold.
- Portao de ativacao: so pode ser ativado em projeto com comando executavel em "Testes E Validacao" de `QUALITY.md`.
- Limite do que a automacao escreve: fecha tarefa apenas com `(verifica:)` declarado e exit 0, colando a saida real como `Evidencia: tipo=comando`. Nunca escreve evidencia de tipo nao comprovado, e nao toca `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` nem specs. Falta de contexto vira pergunta em `Aguardando Usuario`.
- `evals/test_loop.py` (47 verificacoes com agente falso) e `verify_repository.py` de 26 para 33 verificacoes.
- Dogfood: modulo ativado neste repositorio e rodada real executada com o Codex.

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
