# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

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

## 2026-09-02 - Claude + Codex (planejamento da skill 2.2.0)

### Objetivo

- Avaliar tecnicamente se faz sentido adicionar um loop autonomo a este projeto e, se nao fizer agora, extrair da analise as melhorias que valem sem depender dele.

### O Que Foi Feito

- Parecer tecnico sobre loop autonomo, com leitura do repositorio e conferencia da documentacao atual de `/goal`, hooks e modo headless do Claude Code e do Codex CLI. Conclusao: o portao de verificacao nao pode existir no dia zero de um projeto scaffoldado, entao o loop fica como modulo opcional futuro, nunca no scaffold.
- Da analise saiu o PRD da skill 2.2.0, escrito como spec em `Rascunho`: evidencia obrigatoria em tarefa concluida, secao para tarefa esperando resposta do usuario, consenso com independencia declarada e verificador de integridade do meta-projeto.
- Validacao do PRD por modelo distinto no Codex CLI, em duas rodadas: rodada 1 cega (proibida a leitura da spec) e rodada 2 adversarial com a spec a vista. Primeiro uso real da regra de rodada cega que a propria spec propoe.
- O Codex encontrou dois erros reais: `scripts/check.sh` na raiz violava a regra de raiz minima, e o caminho do validador citado na spec estava errado. Ambos confirmados no repositorio.
- Codex tambem reverteu a decisao mais fraca do PRD (verificacao inteiramente opcional) e propos campos declarativos de consenso, que consertam o problema original melhor que a versao anterior.
- Debate registrado em `CONSENSUS.md` e fechado como `resolvido` apos o usuario decidir os dois residuos (nome da secao de espera e retroatividade da evidencia).
- Spec 0003 promovida de `Rascunho` para `Definida` com nove decisoes e criterios de aceite separados entre verificaveis por comando e julgados na mao.
- Tarefas T-009 a T-013 abertas em `TASKS.md`.

### Arquivos Criados Ou Alterados

- `docs/specs/0003-tasks-verificaveis.md` (criado; `Rascunho` e depois `Definida`).
- `docs/CONSENSUS.md` (entrada de 2026-09-02, fechada como `resolvido`).
- `docs/DECISIONS.md` (entrada de 2026-09-02).
- `docs/TASKS.md` (T-009 a T-013 em "Proximas Tarefas").
- `docs/MEMORY.md` (aprendizado sobre o que o `install.sh` distribui).
- `docs/SESSION.md` (esta entrada).

### Decisoes Tomadas

- Loop autonomo fora da 2.2.0 e fora do scaffold; vira modulo opcional futuro, ativavel so em projeto com comando real em `QUALITY.md`.
- Evidencia de fechamento obrigatoria em tarefa concluida a partir da 2.2.0, nao retroativa; `(verifica:)` continua opcional.
- Secao `## Aguardando Usuario` em vez de `## Bloqueadas`; secao para bloqueio nao humano so quando houver caso real.
- Verificador de integridade em `evals/`, nunca em `scripts/` na raiz.
- Registro completo em `docs/DECISIONS.md`, entrada de 2026-09-02.

### Aprendizados Para MEMORY.md

- `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` existem apenas na fonte canonica da skill e nao sao distribuidos pelo `install.sh`. Determina onde colocar ferramenta que deve ficar so no repositorio. Promovido para `MEMORY.md`.

### Pendencias

- Severidade da evidencia ausente em tarefa concluida que nao declarou `(verifica:)`: a spec define AVISO, o Codex pediu apenas "obrigatoria" sem nomear severidade. Decidir ao implementar T-010.
- `CONSENSUS.md` passou de 30KB e o validador ja avisa (T-013).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente; a spec 0003 e autossuficiente.
- Motivo: comecar por T-009 (bloco core e templates), porque T-010, T-011 e T-012 dependem das convencoes estarem escritas.

## 2026-08-20 - Claude (skill 2.1.0)

### Objetivo

- Implementar a skill 2.1.0 com duas features aprovadas pelo usuario: template opcional `STACK.md` (mapa de stack com documentacao oficial) e flag `--progress` no validador (projecao de tarefas e specs).

### O Que Foi Feito

- Criado `assets/docs/STACK.md`: tecnologias, pacotes principais, "Onde Consultar Primeiro" e notas de compatibilidade, para o agente consultar a fonte certa antes de mexer na stack.
- Bloco core do `AGENTS.md` atualizado (v2.1.0): STACK.md em "Onde Escrever Cada Coisa" e gatilho novo de atualizacao; marcador do bloco specs tambem em v2.1.0.
- `validate_structure.py --progress`: contagem de tarefas por secao e, por spec, status + tarefas concluidas/total + perguntas abertas. Somente-leitura por regra (DEC-003 da spec 0002).
- `SKILL.md` para versao 2.1.0; STACK.md incluido no nivel "completa"; evals atualizados (eval 2 com STACK, eval 8 novo de progresso).
- Dogfood: `docs/STACK.md` do meta-projeto preenchido; bloco core da raiz atualizado preservando o restante do arquivo; spec `0002-stack-e-progresso` criada, executada e concluida com evidencia; tarefas T-005 a T-007 registradas e concluidas.
- Skill reinstalada; paridade dos tres destinos conferida; bateria completa aprovada (scaffold completa com STACK exit 0, meta-projeto exit 0, fixtures conforme esperado, zero travessao).
- Decisoes de escopo confirmadas com o usuario: pipeline SDD completo, coverage math, attestation e CLI continuam fora; validacao de stack (rodar testes por framework) fica fora, com comandos do projeto em `QUALITY.md`.
- Projeto publicado no GitHub a pedido do usuario: repositorio publico `adejaimejr/ai-project-structure`, branch `main`, primeiro commit com o estado da skill 2.1.0; `.gitignore` criado (`.DS_Store`, `__pycache__/`).
- Adicionados `README.md` e `LICENSE` (MIT) na raiz a pedido do usuario, com a excecao de raiz minima registrada em "Regras Do Projeto" do `AGENTS.md`.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `evals/evals.json`, `scripts/validate_structure.py`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/docs/STACK.md` (novo), `assets/docs/README.md`.
- Projeto: `AGENTS.md` (raiz), `docs/STACK.md` (novo), `docs/specs/0002-stack-e-progresso.md` (novo), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.
- Instalacoes: tres destinos reinstalados (fora do projeto).

### Decisoes Tomadas

- Ver DEC-001 a DEC-003 na spec `0002-stack-e-progresso` (validacao de stack fora; progresso como flag do validador; projecao somente-leitura).

### Aprendizados Para MEMORY.md

- Nenhum novo (regras ja registradas).

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: 2.1.0 fechada; proximos passos dependem de uso real ou de novas ideias do backlog.

## 2026-08-20 - Claude

### Objetivo

- Fechar duas inconsistencias documentais que apareceram quando os resultados das tres ferramentas foram reunidos.

### O Que Foi Feito

- Diagnosticada a divergencia do eval 4 entre ferramentas: o Codex parou na entrevista e viu exit 1 por diretorio vazio; o Claude Code respondeu a entrevista e viu exit 0. Nenhum dos dois errou. O `expected_output` do eval 4 so descrevia o que acontece antes das respostas e nao dizia o que esperar do validador depois, entao o passo 4 do roteiro de execucao ficava sem criterio.
- Corrigido o `expected_output` do eval 4 em `docs/skills/ai-project-structure/evals/evals.json`: explicita que o criterio do eval e o comportamento da entrevista, que exit 1 em diretorio vazio e o resultado correto daquele ramo e nao reprova, e como exercitar o ramo "Avançar" ate exit 0. JSON revalidado.
- Confirmado que `install.sh` copia apenas `SKILL.md`, `assets/`, `agents/`, `scripts/` e `references/`. Como `evals/` nao e propagado, a correcao nao exigiu reinstalacao nas tres ferramentas.
- Consolidada a secao "Evidencia De Conclusao" da spec `0001-skill-v2`, que tinha ficado auto-contraditoria: linhas antigas ainda diziam "falta repetir no Codex CLI" ao lado das linhas que registravam o Codex concluido. Agora ha um bloco por tarefa e por ferramenta, com o resumo de 21 execucoes aprovadas no topo.
- Registrado o fechamento da validacao em `docs/CHANGELOG.md` do projeto e no CHANGELOG proprio da skill.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/evals/evals.json`
- `docs/skills/ai-project-structure/CHANGELOG.md`
- `docs/specs/0001-skill-v2.md`
- `docs/CHANGELOG.md`
- `docs/SESSION.md` (esta entrada)

### Decisoes Tomadas

- Nao versionar a skill para 2.0.1 por esta correcao: ela toca apenas `evals/`, que nao e material instalado, e nao muda comportamento algum da skill.
- Manter os dois vereditos do eval 4 como validos em vez de escolher um e refazer a rodada da outra ferramenta: o defeito estava na definicao do eval, nao nas execucoes.

### Aprendizados Para MEMORY.md

- Eval cujo criterio e "nao criar nada" precisa dizer explicitamente o que esperar dos passos seguintes do roteiro, senao cada ferramenta interpreta o silencio de um jeito e os resultados ficam incomparaveis.

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a skill v2.0.0 esta validada nas tres ferramentas e a documentacao esta coerente; a proxima acao depende do que o usuario quiser construir em cima.

## 2026-08-20 - Codex

### Objetivo

- Executar a parte Codex CLI da T-002: os 7 evals da skill ai-project-structure v2.

### O Que Foi Feito

- Usada a copia instalada em `~/.agents/skills/ai-project-structure`; a comparacao com a fonte canonica mostrou apenas arquivos que o instalador nao propaga por design.
- Executados os 7 evals em subdiretorios limpos sob `/tmp/skill-v2-tests-codex/`, sem inicializar git. Resultado: 7 de 7 aprovados.
- O validador retornou exit 0 nos evals 1, 2, 3, 5 e 6. No eval 4, nao foi criado nenhum arquivo, como exige a entrevista antes do scaffold; consequentemente, o validador retornou exit 1 por arquivos ausentes. No eval 7, retornou exit 1 com exatamente os 2 erros esperados: ID `T-001` duplicado e Status `Fazendo` invalido.
- No eval 6, o plano e o diff da atualizacao v1 para v2 foram apresentados sem alterar a copia, pois faltava confirmacao por item. As duas fixtures ficaram intactas, com hashes iguais antes e depois.
- Durante esta rodada, o Gemini CLI tambem concluiu os 7 evals. Com as tres ferramentas aprovadas, T-002 foi movida para Concluidas e a spec 0001 foi marcada como Concluida.
- Rodado o validador no repositorio: exit 0, com 4 avisos historicos conhecidos em entradas de 2026-04-25.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests-codex/` (artefatos temporarios dos 7 evals, preservados).

### Decisoes Tomadas

- Considerar o eval 4 aprovado pelo comportamento exigido, mesmo com o exit 1 esperado do validador sobre um diretorio vazio.
- Concluir T-002 e a spec 0001, pois Claude Code, Codex CLI e Gemini CLI aprovaram os 7 cenarios.

### Aprendizados Para MEMORY.md

- Nenhum. O resultado e especifico desta rodada de validacao.

### Pendencias

- Os artefatos em `/tmp/skill-v2-tests-codex/` seguem preservados e so podem ser removidos com confirmacao do usuario.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a validacao da skill v2 foi concluida; qualquer agente serve se tiver contexto suficiente.

## 2026-08-20 - Gemini

### Objetivo

- Fechar a parte Gemini CLI da tarefa T-002, rodando os 7 evals da skill ai-project-structure.

### O Que Foi Feito

- T-002 executado: os 7 evals foram rodados com sucesso em diretorios limpos em `/tmp/skill-v2-tests-gemini/`. 
- Nos evals 6 e 7 as fixtures foram copiadas antes da execucao, permanecendo intactas.
- O validador `scripts/validate_structure.py` retornou exit 0 para os evals 1 a 6.
- No eval 7, o validador retornou exit 1 acusando exatamente os 2 erros esperados (ID duplicado `T-001` e Status invalido `Fazendo`).
- Teste extra: a skill disparou sozinha baseada na description, sem eu precisar citar explicitamente o nome da skill.
- Validador rodado na raiz do projeto como checagem final (0 erros, 4 avisos historicos conhecidos).

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests-gemini/` e os 7 subdiretorios temporarios para cada eval.

### Decisoes Tomadas

- Manter T-002 em aberto, e spec `0001-skill-v2` como "Em andamento", pois falta a avaliacao da ferramenta Codex CLI.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- T-002: Rodar os 7 evals no Codex CLI (invocando `$ai-project-structure`).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): Codex CLI.
- Motivo: Para completar a tarefa T-002.

## 2026-08-20 - Claude

### Objetivo

- Resolver as pendencias T-002 (rodar os 7 evals da skill v2) e T-003 (testar o fluxo de atualizacao v1 para v2 de ponta a ponta), na parte que o Claude Code cobre.

### O Que Foi Feito

- Conferida a paridade fonte x instalado: `diff -r` entre `docs/skills/ai-project-structure/` e `~/.claude/skills/ai-project-structure/` acusa apenas os arquivos que o `install.sh` nao propaga por design (`CHANGELOG.md`, `README.md`, `evals/`, `install.sh`).
- T-002 no Claude Code: os 7 evals executados em subdiretorios limpos sob `/tmp/skill-v2-tests/`, um por eval, fora do repositorio e sem git. Resultado 7/7 aprovados. Evals 6 e 7 rodaram sobre copias das fixtures; os originais ficaram intactos (hash conferido antes e depois).
- Cada eval fechou com `scripts/validate_structure.py`: exit 0 nos evals 1 a 6; exit 1 no eval 7 com exatamente os 2 erros esperados (ID duplicado `T-001` e Status invalido `Fazendo`), relatados sem aplicar correcao.
- T-003: montado um projeto v1 realista em `/tmp/skill-v2-tests/projeto-v1/` (fixture `v1-project` mais 2 entradas de sessao e 1 secao propria extra no `AGENTS.md`) e executado o fluxo de `references/atualizacao.md` inteiro. Os 8 invariantes passaram, incluindo a checagem por `diff` de que o conteudo fora dos marcadores ficou byte-identico.
- Confirmado no T-003 que as duas secoes proprias do usuario ("Regra Local Do Time" e "Padrao De Nomes De Branch") migraram para "Regras Do Projeto" com o corpo inalterado; so o nivel do heading mudou de `##` para `###` para ficar aninhado na secao.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`
- `docs/specs/0001-skill-v2.md`
- `docs/SESSION.md` (esta entrada)
- Fora do repositorio: `/tmp/skill-v2-tests/` (7 subdiretorios de eval mais `projeto-v1/`), todos descartaveis.

### Decisoes Tomadas

- Manter T-002 em aberto: a tarefa exige as tres ferramentas e so o Claude Code foi coberto nesta sessao.
- Preencher "Evidencia De Conclusao" da spec 0001 de forma parcial e marcada como tal, sem mudar o Status para Concluida, para nao perder o registro do que ja foi verificado.
- Na migracao de TASKS do eval 6 e do T-003, atribuir apenas os IDs, sem acrescentar data as linhas de "Concluidas": a data nao foi confirmada pelo usuario e o validador nao a exige.

### Aprendizados Para MEMORY.md

- Nenhum. Os resultados sao execucao de teste ja registrada aqui e na spec.

### Pendencias

- T-002: repetir os mesmos 7 evals no Codex CLI (invocando `$ai-project-structure`) e no Gemini CLI. So entao a tarefa fecha.
- Spec `0001-skill-v2` segue "Em andamento" ate T-002 fechar.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): Codex CLI e depois Gemini CLI, nesta ordem.
- Motivo: o que falta e execucao dos mesmos evals nas outras duas ferramentas; qualquer agente serve se tiver contexto suficiente, mas a tarefa e por definicao amarrada a ferramenta.

## 2026-08-20 - Claude

### Objetivo

- Analisar a skill/metodologia specsfy (github.com/promovaweb/specsfy), extrair o que serve ao nosso contexto e implementar a v2.0.0 da skill ai-project-structure.

### O Que Foi Feito

- Analise completa do specsfy: repo, 18 skills, CLI, metodo MCR-10, gates com scripts; complementada por relatorio dos videos do autor (via NotebookLM). Conclusao: sistemas complementares; importamos mecanismos pontuais, sem a cerimonia pesada.
- Skill v2.0.0 implementada: entrevista numerada com opcoes, regra "Nunca Inferir", TASKS com IDs T-NNN, blocos gerenciados `ai-project-structure:core`/`:specs` com versao, validador `scripts/validate_structure.py` (Python 3, stdlib), modulo opcional de specs (`docs/specs/`), fluxos em `references/atualizacao.md` e `references/specs.md`, 7 evals com fixtures, CHANGELOG proprio da skill, `install.sh` copiando scripts/ e references/.
- Regra nova a pedido do usuario: travessao (em dash, U+2014) proibido em todos os textos do projeto e do core da skill; validador acusa como erro; ocorrencias existentes substituidas.
- Dogfood no meta-projeto: `AGENTS.md` da raiz atualizado para o template v2 com bloco specs; `docs/specs/` ativado com a spec `0001-skill-v2`; `TASKS.md` migrado para T-IDs; `PROJECT_CONTEXT.md` preenchido; `ROADMAP.md` atualizado; entrada de 2026-04-25 do `CONSENSUS.md` recebeu Status.
- Skill reinstalada nas tres ferramentas; paridade conferida por diff; validador rodado do diretorio instalado contra o meta-projeto (0 erros, 4 avisos historicos de SESSION).

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/`: SKILL.md, CHANGELOG.md (novo), install.sh, README.md, evals/evals.json, evals/fixtures/ (novo), scripts/validate_structure.py (novo), references/ (novo), assets/AGENTS.md, assets/partials/ (novo), assets/docs/{README,TASKS,QUALITY,MEMORY}.md, assets/docs/specs/ (novo), assets/docs/archive/README.md.
- Raiz e docs vivos: `AGENTS.md`, `docs/PROJECT_CONTEXT.md`, `docs/TASKS.md`, `docs/ROADMAP.md`, `docs/CONSENSUS.md`, `docs/specs/` (novo), `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`.
- Instalacoes: `~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/` (reinstaladas, fora do projeto).

### Decisoes Tomadas

- Direcao da v2: melhorias pontuais + modulo de specs leve; sem pipeline SDD completo (decisao do usuario; ver `docs/DECISIONS.md` e DEC-001 a DEC-004 na spec 0001).
- Travessao proibido em textos do projeto (pedido do usuario).

### Aprendizados Para MEMORY.md

- O usuario nao quer o caractere travessao (em dash, U+2014) em nenhum texto deste projeto; separadores aceitos: dois-pontos, ponto-e-virgula, virgula, parenteses, hifen.

### Pendencias

- Rodar os 7 evals manualmente nas tres ferramentas (T-002).
- Testar o fluxo de atualizacao v1 para v2 em projeto real externo (T-003).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com acesso as tres ferramentas.
- Motivo: as pendencias sao execucao de evals e teste de fluxo; nao exigem modelo especifico.

## 2026-05-26 - Claude

### Objetivo

- Propagar os ajustes Codex da skill para as tres ferramentas (pendencia deixada pela sessao Codex).

### O Que Foi Feito

- Conferida a fonte canonica: `agents/openai.yaml` (YAML valido por inspecao; PyYAML ausente no ambiente) e `README.md` com as correcoes do Codex.
- Confirmado que o Codex nao deixou `quick_validate.py` na fonte (era do workspace dele).
- Rodado `docs/skills/ai-project-structure/install.sh` (global).
- Verificado por `diff` que `agents/openai.yaml` ficou identico a fonte nos tres destinos (`~/.claude/skills/`, `~/.agents/skills/`, `~/.gemini/skills/`).

### Arquivos Criados Ou Alterados

- `~/.claude/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `~/.agents/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `~/.gemini/skills/ai-project-structure/` (reinstalado, fora do projeto)
- `docs/TASKS.md`, `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma. Apenas execucao da propagacao pendente.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma acionavel.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill revisada, corrigida e instalada nas tres ferramentas; ciclo fonte -> `install.sh` estabelecido para mudancas futuras.

## 2026-05-26 - Codex

### Objetivo

- Revisar e corrigir somente a parte OpenAI/Codex da skill `ai-project-structure`, validando contra a documentacao oficial atual do Codex CLI.

### O Que Foi Feito

- Lidos `AGENTS.md` e a memoria relevante em `docs/`.
- Consultada a documentacao oficial atual do Codex sobre Agent Skills e o guia oficial de evals para skills.
- Confirmado que o caminho atual do Codex e `$HOME/.agents/skills` para usuario e `.agents/skills` para repo/projeto; `~/.codex/skills` aparece em material antigo e nao foi usado.
- Ajustado `agents/openai.yaml`: `short_description` reduzida para caber no intervalo recomendado e `default_prompt` atualizado para mencionar explicitamente `$ai-project-structure`.
- Ajustado `README.md`: invocacao explicita do Codex atualizada para `/skills` ou `$ai-project-structure`; nota adicionada sobre evals com prompts CSV e traces JSONL via `codex exec --json`.
- Validado `SKILL.md`, `agents/openai.yaml` e `install.sh` manualmente. O validador local `quick_validate.py` nao rodou porque o Python do ambiente nao tinha `PyYAML`.
- Tentativa de rodar `./install.sh` para propagar foi bloqueada pela aprovacao de escrita fora do workspace.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/agents/openai.yaml`
- `docs/skills/ai-project-structure/README.md`
- `docs/TASKS.md`
- `docs/CHANGELOG.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma decisao formal nova; foram aplicadas correcoes de conformidade com a documentacao atual.

### Aprendizados Para MEMORY.md

- Nenhum. Os pontos relevantes ficaram registrados nesta sessao e no changelog.

### Pendencias

- Rodar `docs/skills/ai-project-structure/install.sh` para propagar as mudancas para `~/.agents/skills/`, `~/.claude/skills/` e `~/.gemini/skills/` quando houver permissao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a fonte canonica ja foi corrigida; falta apenas propagar a instalacao, e qualquer agente serve se tiver contexto suficiente e permissao para escrever nos diretorios globais.

## 2026-05-26 - Claude

### Objetivo

- Transformar a skill `ai-project-structure` em um pacote instalavel em Claude Code, Codex CLI e Gemini CLI.

### O Que Foi Feito

- Verificado o estado real dos hosts: a instalacao registrada em 2026-04-25 nao existia em nenhum lugar; `~/.codex/skills/` so tinha `.system` (e nao e o caminho lido pelo Codex).
- Confirmado por pesquisa nas docs oficiais que `SKILL.md` virou **Agent Skills Open Standard**, lido por Claude Code, Codex CLI e Gemini CLI - um unico pacote serve aos tres.
- Confirmados os caminhos: Claude `~/.claude/skills/`, Codex `~/.agents/skills/`, Gemini `~/.gemini/skills/`.
- Criados `install.sh` (instalador idempotente, global/projeto, por ferramenta, com `--uninstall`), `README.md` (distribuicao/uso) e `agents/openai.yaml` (metadado opcional do Codex) na pasta da skill.
- Instalada a skill globalmente nas tres ferramentas e verificado o conteudo (SKILL.md + assets/ + agents/) em cada destino.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/install.sh` (novo)
- `docs/skills/ai-project-structure/README.md` (novo)
- `docs/skills/ai-project-structure/agents/openai.yaml` (novo)
- `~/.claude/skills/ai-project-structure/` (instalado, fora do projeto)
- `~/.agents/skills/ai-project-structure/` (instalado, fora do projeto)
- `~/.gemini/skills/ai-project-structure/` (instalado, fora do projeto)
- `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/SESSION.md`

### Decisoes Tomadas

- Distribuir a skill como pacote unico no Agent Skills Open Standard (ver `DECISIONS.md` 2026-05-26).
- Corrigido o caminho do Codex: `~/.agents/skills/`, nao `~/.codex/skills/`.

### Aprendizados Para MEMORY.md

- Nenhum. Decisao e correcao ja registradas em `DECISIONS.md`/`CHANGELOG.md`.

### Pendencias

- Nenhuma acionavel. (Opcional: testar a invocacao em uma sessao real de cada ferramenta.)

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill instalada e distribuivel nas tres ferramentas; para propagar mudancas futuras, edite a fonte em `docs/skills/ai-project-structure/` e rode `install.sh`.

## 2026-04-25 - Claude

### Objetivo

- Instalar a skill `ai-project-structure` globalmente nos hosts do usuario (Claude Code e Codex).

### O Que Foi Feito

- Copiada a skill para `~/.claude/skills/ai-project-structure/SKILL.md`.
- Copiada a skill para `~/.codex/skills/ai-project-structure/SKILL.md` em paralelo com o Codex (resultado idempotente; ver entrada seguinte).
- Consolidada a entrada de instalacao em `TASKS.md` cobrindo ambos os locais.

### Arquivos Criados Ou Alterados

- `~/.claude/skills/ai-project-structure/SKILL.md` (novo, fora do projeto)
- `~/.codex/skills/ai-project-structure/SKILL.md` (novo, fora do projeto)
- `docs/SESSION.md` (esta entrada)
- `docs/TASKS.md`

### Decisoes Tomadas

- Nenhuma.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill disponivel globalmente em ambos os hosts; novos projetos podem invoca-la.

## 2026-04-25 - Codex

### Objetivo

- Instalar skill ai-project-structure globalmente em `~/.codex/skills/`.

### O Que Foi Feito

- Criado o diretorio `~/.codex/skills/ai-project-structure/` se ainda nao existia.
- Copiado `docs/skills/ai-project-structure/SKILL.md` para `~/.codex/skills/ai-project-structure/SKILL.md`.
- Confirmada a instalacao com listagem do diretorio global da skill.
- Atualizado `TASKS.md` movendo a instalacao global da skill para concluidas.

### Arquivos Criados Ou Alterados

- `~/.codex/skills/ai-project-structure/SKILL.md`
- `docs/SESSION.md`
- `docs/TASKS.md`

### Decisoes Tomadas

- Nenhuma decisao nova; foi executada a instalacao solicitada pelo usuario.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: skill instalada globalmente; proxima acao depende do proximo uso ou projeto.

## 2026-04-25 - Claude

### Objetivo

- Aplicar as oito melhorias aprovadas no tri-consenso sobre `MEMORY.md` e estrutura.

### O Que Foi Feito

- Criado `docs/MEMORY.md` com tipos User / Feedback / Project / Reference, criterio de promocao, sobrescrita ativa e regra de dados sensiveis.
- Criado `docs/archive/` com `README.md` indice para rotacao futura de `SESSION.md` e `CONSENSUS.md`.
- Reescrito `AGENTS.md` cobrindo: imutabilidade dos arquivos-ponte, dois niveis de leitura, regra de desempate, atualizacao por gatilho, criterio de "onde escrever cada coisa", politica de rotacao e uso restrito de `CONSENSUS.md`.
- Atualizado template de `SESSION.md` (handover direcionado, secao de aprendizados para `MEMORY.md`).
- Atualizado template de `CONSENSUS.md` (`Status` e `Proximo passo`).
- Atualizado `QUALITY.md` com checklist de atualizacao por gatilho e cuidados com `MEMORY.md`.
- Sincronizada skill `ai-project-structure` com a estrutura nova.
- Registrada decisao `Evolucao da estrutura: MEMORY.md e oito melhorias` em `DECISIONS.md` e atualizado `CHANGELOG.md`.
- Fechada entrada do `CONSENSUS.md` com `Status: resolvido` e nota de aprovacao do usuario.

### Arquivos Criados Ou Alterados

- `AGENTS.md` (reescrito)
- `docs/MEMORY.md` (novo)
- `docs/archive/README.md` (novo)
- `docs/QUALITY.md`
- `docs/SESSION.md` (template + esta entrada)
- `docs/CONSENSUS.md` (template + fechamento)
- `docs/DECISIONS.md`
- `docs/CHANGELOG.md`
- `docs/README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/TASKS.md`
- `docs/skills/ai-project-structure/SKILL.md`

### Decisoes Tomadas

- Aplicacao das oito melhorias do tri-consenso (ver `DECISIONS.md`).

### Aprendizados Para MEMORY.md

- Nenhum. Esta sessao foi exercicio de meta-estrutura, nao gerou aprendizados sobre projetos reais.

### Pendencias

- Preencher `PROJECT_CONTEXT.md` com o contexto real do projeto, quando houver.
- Instalar a skill globalmente no Codex, se desejado.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: estrutura pronta para uso; a proxima acao depende do projeto real que sera tocado nela.

## 2026-04-25 - Codex

### Objetivo

- Preencher a posicao do Codex no consenso aberto sobre `MEMORY.md` e melhorias estruturais.

### O Que Foi Feito

- Leitura de `AGENTS.md` e dos arquivos em `docs/`.
- Atualizacao apenas da secao `Posicao Do Codex` na entrada `2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias`.
- Acrescentados pontos de acordo adicionais, riscos novos e uma frase de tri-consenso no `Consenso Final`.
- Mantido o status da entrada como aberto, conforme solicitado pelo usuario.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Nenhuma decisao formal nova foi registrada; a entrada continua aberta para decisao do usuario.

### Pendencias

- Usuario decidir se aprova a implementacao de `docs/MEMORY.md` e das melhorias consensuadas.
- Se aprovado, atualizar `AGENTS.md`, `QUALITY.md`, `PROMPTS.md`, `docs/skills/ai-project-structure/SKILL.md` e demais referencias afetadas.

### Proximo Passo Recomendado

- Para qualquer agente: aguardar a aprovacao do usuario antes de criar `MEMORY.md` ou aplicar as regras novas.

## 2026-04-25 - Gemini

### Objetivo

- Participar do consenso sobre a adição de `MEMORY.md` e detalhamento de melhorias estruturais.

### O Que Foi Feito

- Análise da posição do Claude em `docs/CONSENSUS.md`.
- Registro da posição do Gemini apoiando a criação de `MEMORY.md` e os sete pontos de melhoria detalhados.
- Atualização dos "Pontos de Acordo", "Riscos e Tradeoffs" e "Consenso Final" no debate.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- Consenso técnico atingido entre Claude e Gemini para evoluir a estrutura com 8 melhorias (7 detalhadas + `MEMORY.md`).

### Pendencias

- Aprovação do usuário para aplicar as mudanças em `AGENTS.md` e criar `MEMORY.md`.

### Proximo Passo Recomendado

- Usuário revisar o consenso final e instruir a implementação das melhorias.

## 2026-04-25 - Gemini

### Objetivo

- Validar a estrutura Markdown multiagente do projeto.

### O Que Foi Feito

- Leitura e análise exaustiva de `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e diretório `docs/`.
- Registro da posição do Gemini em `docs/CONSENSUS.md` sobre a clareza e segurança da estrutura.
- Sugestão de melhorias focadas em handover de sessões e imutabilidade dos arquivos-ponte.

### Arquivos Criados Ou Alterados

- `docs/CONSENSUS.md`
- `docs/SESSION.md`

### Decisoes Tomadas

- A estrutura foi considerada apta para uso imediato em projetos reais tocados por múltiplas IAs.

### Pendencias

- Aguardar a validação e posição do Claude em `docs/CONSENSUS.md`.

### Proximo Passo Recomendado

- Solicitar ao Claude a revisão da estrutura conforme o prompt em `docs/PROMPTS.md`.

## 2026-04-25 - Codex

### Objetivo

- Criar uma estrutura Markdown multiagente para projetos tocados por IA.

### O Que Foi Feito

- Criada a raiz minima com arquivos de entrada para agentes.
- Centralizadas as regras de IA em `AGENTS.md`.
- Criada a memoria do projeto em `docs/`.
- Adicionado registro de sessoes em `SESSION.md`.
- Adicionado arquivo de consenso entre modelos em `CONSENSUS.md`.
- Adicionados prompts reutilizaveis em `PROMPTS.md`.
- Adicionada uma skill portavel em `docs/skills/ai-project-structure/SKILL.md`.

### Arquivos Criados Ou Alterados

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `docs/README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/SESSION.md`
- `docs/CONSENSUS.md`
- `docs/TASKS.md`
- `docs/DECISIONS.md`
- `docs/ARCHITECTURE.md`
- `docs/QUALITY.md`
- `docs/PROMPTS.md`
- `docs/CHANGELOG.md`
- `docs/GLOSSARY.md`
- `docs/ONBOARDING.md`
- `docs/ROADMAP.md`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/skills/ai-project-structure/SKILL.md`

### Decisoes Tomadas

- Manter na raiz apenas os arquivos Markdown de entrada dos agentes.
- Usar `AGENTS.md` como fonte central de regras.
- Usar `CLAUDE.md` e `GEMINI.md` como arquivos-ponte.
- Usar `SESSION.md` para continuidade entre sessoes.
- Usar `CONSENSUS.md` para debate entre modelos quando houver duvida real.

### Pendencias

- Instalar a skill em `~/.codex/skills/ai-project-structure` caso seja desejado torna-la global no Codex.
- Preencher os arquivos de contexto conforme o projeto real evoluir.

### Proximo Passo Recomendado

- Pedir ao Claude para revisar a estrutura usando o prompt em `PROMPTS.md`.
