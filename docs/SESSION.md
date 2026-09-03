# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas anteriores a 2026-09-02 foram rotacionadas para `docs/archive/SESSIONS-2026.md`.

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

## 2026-09-02 - Claude (spec 0004 definida)

### Objetivo

- Levar o usuario pelas oito perguntas abertas da spec 0004 e fechar o escopo da 2.3.0.

### O Que Foi Feito

- As oito perguntas foram decididas uma a uma, em ordem de dependencia: P-4 primeiro, porque a resposta dela restringia P-2 e P-6.
- O escopo encolheu de G para M. Foram cortados worktree, notificacao de sistema, teto de custo e automacao de consenso, tres deles porque outra decisao ja resolvia o problema por construcao.
- Spec 0004 passou para `Definida` com DEC-001 a DEC-009 e "Perguntas Abertas" vazia. Criterios de aceite de comportamento agora existem, porque ha o que cobrar: sao verificaveis com um agente falso, sem gastar chamada de modelo.
- DEC-001 e DEC-006 foram copiadas para `docs/DECISIONS.md`: juntas, definem a fronteira entre o que a maquina pode afirmar e o que so a pessoa pode afirmar nos arquivos de memoria, o que vale para qualquer automacao futura.
- T-019 a T-023 abertas. T-018 concluida.

### Arquivos Criados Ou Alterados

- `docs/specs/0004-modulo-de-loop.md`, `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- DEC-001 a DEC-008 da spec 0004, todas do usuario. DEC-009 e decisao de implementacao minha, sobre versionar os tres marcadores juntos; e a unica que nao veio de pergunta e a que mais merece revisao.

### Aprendizados Para MEMORY.md

- Nenhum. As decisoes ficaram em `DECISIONS.md`, que e o lugar delas.

### Pendencias

- Nenhuma acionavel. T-019 a T-023 estao em "Proximas Tarefas".

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente.
- Motivo: comecar por T-019, porque T-020 depende do bloco e do fluxo de ativacao existirem. T-022 pede um agente falso, entao da para testar o `loop.sh` inteiro sem gastar chamada de modelo.

## 2026-09-02 - Claude (publicacao da 2.2.0 e abertura da spec 0004)

### Objetivo

- Publicar a 2.2.0 no GitHub e abrir a spec do modulo de loop, cujo pre-requisito passou a existir hoje.

### O Que Foi Feito

- `git push origin main`: os 5 commits da 2.2.0 sairam do laptop (`7040e4d..c5d8488`).
- Spec `0004-modulo-de-loop` criada como `Rascunho`. Ela separa o que ja esta decidido (DEC-001, DEC-003 e DEC-005, herdadas da 0003) do que depende de resposta do usuario.
- O pre-requisito que DEC-005 mandou para o modulo de loop, "secao Testes E Validacao de `QUALITY.md` com comando real", passou a ser satisfeito por este repositorio hoje, com `verify_repository.py`. E o que destrava a discussao do loop sem contrariar DEC-003.
- Nenhuma tarefa de implementacao aberta: com oito perguntas em aberto, abrir tarefa seria comprar escopo que ainda nao existe.

### Arquivos Criados Ou Alterados

- `docs/specs/0004-modulo-de-loop.md` (novo), `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. A spec 0004 registra tres decisoes herdadas e nenhuma propria, de proposito: decidir agora seria decidir sem as respostas.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- T-018 em `## Aguardando Usuario`: as oito perguntas da spec 0004. Primeiro uso real da secao neste repositorio, o que tambem exercita a convencao contra um caso que nao foi construido para testa-la.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, nao um agente.
- Motivo: a spec so anda com as respostas de P-1 a P-8. P-3, P-4 e P-8 mudam o escopo o suficiente para que qualquer implementacao antes delas seja retrabalho.

## 2026-09-02 - Claude + Codex (evals 1, 2, 5, 6 e 9 no Codex CLI)

### Objetivo

- Rodar em outra ferramenta os cinco evals que dependem de julgamento de comportamento, para tirar do julgamento o modelo que escreveu os templates.

### O Que Foi Feito

- Codex CLI nao estava instalado nesta maquina. Instalado a pedido do usuario (`npm i -g @openai/codex`, versao 0.152.1, autenticado via ChatGPT). A skill 2.2.0 apareceu na lista de skills do Codex, vinda de `~/.agents/skills/`.
- Cinco rodadas de `codex exec` em diretorios descartaveis fora do repositorio, com os prompts literais de `evals.json`. Conferencia feita por script proprio, lendo o diretorio produzido em vez do relato do agente.
- 5 de 5 aprovados. Um modelo sem nenhum contexto desta implementacao preencheu a data de adocao com a data do dia nas tres estruturas novas, manteve a secao `Aguardando Usuario` e, no eval 6, afirmou espontaneamente que a tarefa historica concluida fica sem evidencia porque a regra nao e retroativa.
- Isso valida na pratica o passo 5b do `SKILL.md` e o passo 7b de `references/atualizacao.md`, ambos escritos hoje, e a nao retroatividade de DEC-008 e DEC-011.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`, `docs/SESSION.md`. Nenhum arquivo da skill precisou mudar.

### Decisoes Tomadas

- Nenhuma.

### Aprendizados Para MEMORY.md

- Nenhum promovido. A observacao do eval 2 (o modelo inverteu qual opcao de specs e a recomendada) e desvio de fidelidade de um modelo, nao regra do projeto, e nao esta entre os criterios que aquele eval cobra.

### Pendencias

- Nenhuma acionavel. Fora dos criterios cobrados, duas observacoes: no eval 2 o Codex marcou "Sim (recomendado)" para o modulo de specs, e o `SKILL.md` recomenda "Nao"; e a resposta de chat do eval 9 usou um travessao, caractere proibido nos textos do projeto, sendo que a fixture usa um `AGENTS.md` reduzido que nao carrega essa regra.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a spec 0003 esta fechada e agora tambem validada por ferramenta e modelo diferentes. O backlog volta ao normal.

## 2026-09-02 - Claude (T-014, criterios sem runner)

### Objetivo

- Exercitar na mao os tres criterios de aceite da spec 0003 que nao tem runner: scaffold minimal, scaffold completa e atualizacao de um projeto 2.1.0.

### O Que Foi Feito

- Skill invocada da instalacao real, nao da fonte do repositorio, em tres projetos descartaveis fora do repositorio. Isso tambem testou que a instalacao de ontem esta usavel.
- Scaffold minimal e scaffold completa com o modulo de specs: `--strict` exit 0 nos dois, marcadores em v2.2.0, data de adocao preenchida, sem git, sem `partials/` copiado.
- Projeto 2.1.0 sintetizado com os templates daquela versao tirados do git, com dados de usuario reais (tarefas concluidas sem evidencia, tarefa parada esperando resposta, consenso antigo, regras locais) e atualizado pelo fluxo de `references/atualizacao.md`.
- O projeto 2.1.0 validou limpo **antes** da atualizacao, sob o validador 2.2.0. E a prova pratica de DEC-011: sem o marcador de corte, a cobranca nao existe.
- Depois da atualizacao, a regra foi testada nos dois sentidos: tarefa concluida hoje sem evidencia gerou AVISO, as concluidas em agosto continuaram silenciosas, e o AVISO sumiu quando a evidencia entrou.
- Quatro defeitos achados. Tres eram texto (T-015). O quarto era codigo e apareceu quando o proprio `TASKS.md` deste repositorio ficou com uma tarefa citando outra: o validador contava qualquer `T-NNN` da linha como ID e acusava duplicidade. Corrigido em T-016, com guarda na fixture.

### Arquivos Criados Ou Alterados

- `docs/skills/ai-project-structure/SKILL.md`, `docs/skills/ai-project-structure/references/atualizacao.md` (correcoes de T-015).
- `docs/skills/ai-project-structure/scripts/validate_structure.py`, `docs/skills/ai-project-structure/evals/fixtures/aguardando-project/` e `docs/skills/ai-project-structure/CHANGELOG.md` (correcao de T-016).
- `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma decisao nova. Tres achados eram defeito de texto e um era defeito de codigo; nenhum tocou o desenho da 2.2.0.

### Aprendizados Para MEMORY.md

- Dogfood pega o que teste sintetico nao pega: o bug de ID so apareceu porque uma tarefa real precisou citar outra. Nao promovido para `MEMORY.md` por ser generico demais para virar regra acionavel.

### Pendencias

- Nenhuma acionavel. As correcoes de T-015 e T-016 foram propagadas para os tres destinos globais a pedido do usuario, com paridade conferida por `diff -rq`.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): outra ferramenta (Codex CLI ou Gemini CLI).
- Motivo: T-014 rodou no Claude Code, e quem escreveu os templates julgou o proprio trabalho. Os evals 1, 2, 5, 6 e 9 continuam valendo mais quando rodados por outro modelo, sem este contexto.

## 2026-09-02 - Claude (implementacao da skill 2.2.0)

### Objetivo

- Implementar a skill 2.2.0 conforme a spec 0003: evidencia de fechamento em tarefa concluida, secao `Aguardando Usuario`, campos declarativos de consenso e verificador de integridade do meta-projeto.

### O Que Foi Feito

- T-009: bloco core em v2.2.0 com a secao nova "Evidencia De Fechamento", o destino da pergunta que trava tarefa dentro de "Nunca Inferir" e a subsecao "Independencia Declarada" no consenso. Bloco propagado para a raiz por script e conferido byte a byte. Templates de `TASKS.md` (secao `Aguardando Usuario`, sub-linha de evidencia, marcadores novos) e de `CONSENSUS.md` (tres campos declarativos) atualizados.
- T-010: checks novos no validador, provados por uma matriz de 17 casos em projeto descartavel, um por regra e um por caso que deve ficar silencioso. A severidade que estava em aberto foi decidida: AVISO, com o motivo registrado em DEC-010.
- Descoberta na implementacao de T-010: a nao retroatividade de DEC-008 nao se sustenta sem um corte declarado por projeto, porque as 15 linhas historicas deste repositorio derrubariam o `--strict` que a propria spec exige. Criado o marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` em `TASKS.md`, que governa a evidencia e tambem os campos de consenso (DEC-011).
- T-011: `evals/verify_repository.py` com 26 checagens, e os 4 headings ausentes de `SESSION.md` corrigidos com nota honesta, sem promover nada retroativamente para `MEMORY.md`.
- T-013 antecipada: `SESSION.md` e `CONSENSUS.md` rotacionados para `docs/archive/`. Veio antes porque o aviso de rotacao reprovava o `--strict` declarado por T-010 e T-011; fechar as duas antes disso teria sido fechar tarefa com o proprio check falhando.
- T-012: fixture `aguardando-project` (caso valido e caso invalido), eval 9, versao 2.2.0 no `SKILL.md` com o passo 5b de preencher a data de adocao, passo 7b em `references/atualizacao.md`, CHANGELOGs, comando de integridade em `QUALITY.md` e reinstalacao nos tres destinos globais.
- O verificador pegou dois problemas reais durante a propria construcao: `SKILL.md` ainda em 2.1.0 com os marcadores em 2.2.0, e ele mesmo carregando um travessao literal no codigo do check de travessao.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `scripts/validate_structure.py`, `evals/verify_repository.py` (novo), `evals/evals.json`, `evals/fixtures/aguardando-project/` (nova), `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/docs/TASKS.md`, `assets/docs/CONSENSUS.md`, `references/atualizacao.md`.
- Projeto: `AGENTS.md` (raiz), `docs/TASKS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/QUALITY.md`, `docs/CHANGELOG.md`, `docs/specs/0003-tasks-verificaveis.md`, `docs/archive/README.md`, `docs/archive/SESSIONS-2026.md` (novo), `docs/archive/CONSENSUS-2026.md` (novo).
- Instalacoes: tres destinos globais reinstalados a pedido do usuario, com paridade conferida.

### Decisoes Tomadas

- DEC-010: evidencia ausente sem `(verifica:)` declarado gera AVISO, nao ERRO.
- DEC-011: a nao retroatividade depende de um corte declarado por projeto, no marcador `(convencoes-2-2-0-desde:)` de `TASKS.md`, que governa tambem os campos declarativos de consenso.
- Ambas em `docs/DECISIONS.md`, entrada de 2026-09-02, e na spec 0003.

### Aprendizados Para MEMORY.md

- Verificador que procura um caractere proibido precisa escrever esse caractere escapado no proprio codigo, senao ele se acusa. Promovido para `MEMORY.md`.

### Pendencias

- Os tres criterios de aceite da spec 0003 sem runner (scaffold minimal, scaffold completa e atualizacao de um projeto 2.1.0) continuam julgados na mao e nao foram exercitados nesta sessao. Viraram T-014 em `TASKS.md`.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente com contexto suficiente, de preferencia em ferramenta diferente da que implementou.
- Motivo: T-014 e justamente rodar o fluxo da skill de fora, como usuario. Quem escreveu os templates e o pior juiz de saber se eles funcionam sem contexto.

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

