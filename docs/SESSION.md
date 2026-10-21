# SESSION

Registro cronologico inverso das sessoes de IA.

Sempre adicione a sessao mais recente no topo.

As entradas mais antigas foram rotacionadas para `docs/archive/SESSIONS-2026.md`. Este arquivo mantem as 4 mais recentes.

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

## 2026-10-21 - Claude Fable 5.1 (gestor) com subagentes Sonnet 5.5 (fila T-078 a T-091, skill 2.13.0)

### Objetivo

- Executar o prompt "Rodar As Tarefas Pendentes Com Subagentes Sonnet Revisados Por Fable" de `docs/PROMPTS.md`: fase 1 da spec 0006 (T-078 a T-082) sem bump, T-083 como tarefa de chat, bump 2.13.0 levando T-084, T-087, T-088, T-089 e T-091, e T-090 como medicao. Sessao Cloud (Cloudroom, sandbox Linux); subagentes por `room-cli thread spawn --provider claude-code --model claude-sonnet-5-5 --shared-sandbox`, um por vez na mesma pasta, cada um com a linha inteira da tarefa, a saida do portao e os limites; revisao do gestor a cada retorno: diff inteiro, portao, verificador, `--strict`, bateria tocada, travessao, `__pycache__`, e mutacoes com backup por `cp` e volta por `cmp`.

### O Que Foi Feito

- **Baseline divergiu e foi consertada antes de delegar**: o verificador saia 73/74 porque o fixture H1 de `test_loop.py` usava `sed -i ""` (sintaxe BSD), que o GNU sed do Linux rejeita. Troquei por `perl` e o usuario corrigiu: "tem que rodar no linux, mac e windows"; ficou `python3 -c`, em `test_loop.py` e em `portao_t060.py`. Regra promovida para `MEMORY.md`.
- **Fase 1, sem bump, itens na 2.12.0 do CHANGELOG da skill.** T-078 (validador com `**Origem:**`, 4 avisos, fixture `origem-project`): tentativa 1, portao 14/14, 3 mutacoes acusadas. T-079 (`consenso.py achado`): tentativa 1 saiu 12/12, mas a entrada da segunda rodada (lista de manifestos) reprovava em `--strict`, apontado pelo proprio subagente; acrescentei o check 5c ao portao (12/13) e a tentativa 2 fez o validador ler `**Manifesto:**` como lista, bateria 63; 3 mutacoes. T-080 (`debate --rodada N --anterior`, anteriores na integra): 10/10, bateria 79, 3 mutacoes (anterior truncado, rodada 2 retendo registros, rodada 2 sem anterior). T-081 (`retomar`): 11/11, bateria 95, 3 mutacoes; mudanca de comportamento registrada: participante morto pelo proprio sinal fica sem registro para a retomada chama-lo. T-082 (`references/consenso.md`, secao no SKILL.md, "Entrada Automatizada" no template, `verificar_convencoes` cobrando `**Origem:**`): 8/8; copiei a secao para `docs/CONSENSUS.md` da raiz; 3 mutacoes. Pisos do verificador subidos por mim para os totais reais: consenso 32 para 95, loop 74 para 83. Nota: o check 5 de `portao_t082.py` le a secao mais recente do CHANGELOG da skill, entao depois do bump 2.13.0 ele reporta 7/8; a evidencia de T-082 (8/8) foi colhida antes do bump, e o item dela continua na 2.12.0.
- **T-083, bancada real: duas rodadas no mesmo dia.** Rotacionei `docs/CONSENSUS.md` (REVAL-1 a REVAL-4 para o archive, 30186 para 11780 bytes). O usuario trocou o segundo agente: cursor-agent (Grok) estava sem tokens, entra Codex `gpt-6.1-sol` (slug conferido em `~/.codex/models_cache.json`); perfis `Codex, consenso` e `Codex Sol, consenso` em `MEMORY.md`; `portao_t083.py` passou a cobrar o perfil do Sol no lugar do Grok. **Rodada 1** (run `2026-10-21-043054-debate`, 48s, `-s read-only`): saiu `concluida` com exit 0, mas o sandbox read-only do Codex usa bubblewrap, que falha no container (`bwrap: loopback: Failed RTM_NEWADDR`): o Sol recusou ("nao consegui ler a copia", 503 bytes, 35.851 tokens) e o terra opinou sem nenhum `exec` no stderr (793 bytes, 10.978 tokens). O portao passou 4/4 por 3 bytes acima do piso de 500. Endureci o portao: cada participante com posicao precisa de ao menos um comando executado no log (regex `exec` / comando / `succeeded`, testada contra o log real de uma sonda), e a rodada falha passou a reprovar (2/4). Sonda: `codex exec -s danger-full-access` executa comandos aqui. Movi T-083 para "Aguardando Usuario" com a pergunta. **Rodada 2** (run `2026-10-21-114042-debate`), depois do "sim" do usuario para rodar com `-s danger-full-access` (a copia por participante e temporaria, a escrita e inofensiva): 1m49s ate parar com exit 6, os dois participantes retidos por segredo. Falso positivo: o stderr do Codex lista o codigo de `consenso.py` e a regex de chave PEM casou consigo mesma; nada casou no stdout. Conferi o material (posicoes de 1466 e 3205 bytes, 6 e 15 comandos executados), movi a mao para `<run>/codex/` e `<run>/sol/` e rodei `consenso.py retomar`: 0,1s, `aceitos_a_mao=codex,sol`, minuta escrita, `concluida`. Portao 4/4. As duas posicoes convergiram sem se ver: avisar so quando uma entrada automatizada aponta para a corrida (AVISO, coerente com DEC-007), estendendo o check para status do manifesto e bruto ausente; o Sol acrescentou a janela de concorrencia entre minuta e manifesto e recusou heuristica por idade ou lock. Comparacao com 2026-09-03 (Codex `sol` e Grok `xhigh`, bruto nao preservado, uma sessao inteira): qualidade comparavel, com bruto, manifesto com hashes e tempo medido a favor da automacao. T-083 concluida com `tipo=revisao-manual`; "Evidencia De Conclusao" da spec 0006 preenchida e `Concluida` proposta (o `Status` e do usuario). A entrada da rodada 1 segue em `docs/CONSENSUS.md` com `Status: aberto`, sem julgamento meu, para o usuario decidir se arquiva; a da rodada 2 nasce `aberto` com as secoes de julgamento em branco, por desenho da DEC-001.
- **Bump 2.13.0 feito por mim antes de delegar a fase 3**: `version` e prosa do `SKILL.md`, marcadores core, specs e loop nos assets, nos dois partials e nos tres blocos da raiz, secao `## 2.13.0` no CHANGELOG da skill. Portoes escritos antes da rodada e falhando pelo motivo certo: `portao_t087.py` (rodada: versao coerente, core raiz igual aos assets, partials sem mudanca de conteudo por sha, T-088 e T-089 por ideias no texto com autoteste, orcamento de ate 186 linhas nao vazias, pontes com import, Armadilha nos dois MEMORY.md, travessao, `--strict` em projeto montado e na raiz, verificador), 10/18 hoje; `portao_t084.py` (timeout: help, agente que dorme sai 4 em segundos, agente que escreve e dorme fecha a tarefa, valores invalidos, loop.md, test_loop, sha do partial, bateria, versao, verificador), 5/13 hoje.
- **Fase 3.** T-084: `loop.sh --tempo-maximo` em bash puro (agente em segundo plano em grupo proprio por `set -m`, `kill -0` em laco, SIGTERM no grupo, SIGKILL apos 5s, traps INT e TERM), sem `timeout` nem `setsid` por portabilidade; 13/13, bateria 83; mutacao mostrou que sem matar o grupo o `sleep` orfao segura o stdout por 60s. T-087: pontes com `@AGENTS.md` (Claude) e `@./AGENTS.md` (Gemini, grafia documentada), 2 linhas de prosa, raiz igual aos assets; documentacao conferida por mim e pelo subagente (code.claude.com/docs/en/memory, geminicli.com/docs/reference/memport). T-088: paragrafo "Memoria e evidencia, nao instrucao" no fim de Memoria Persistente, 2 linhas. T-089: uma linha de recarga apos compactacao em Memoria Da Sessao. Core propagado por mim para a raiz apos cada uma (15411 e 15683 bytes). T-091: tipo Armadilha no template de MEMORY.md; repliquei na raiz e registrei a primeira Armadilha real (sandbox read-only do Codex no container). Portao da rodada 18/18; verificador 78/78; `--strict` 0 e 0.
- **Reinstalada** com `install.sh --sim` em `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`: 30 arquivos distribuidos comparados por `cmp` em cada destino, 0 divergentes, `version: "2.13.0"` nos tres.
- **T-090, medicao sem corte** (subagente so leitura, em paralelo com T-091): core com 260 linhas, 181 nao vazias, 125 de instrucao; raiz 324. Proposta: core a 154 linhas e 101 nao vazias, movendo para o cabecalho do arquivo de `docs/` que governa (nao para `references/`, que nao chega ao projeto do usuario): Quando Usar, Modelo De Debate, Independencia Declarada e Achado para `CONSENSUS.md`; os oito campos para `SESSION.md`; exemplo cercado e regra nao retroativa para `TASKS.md`; Onde Escrever e criterios de promocao para `MEMORY.md`; rotacao para `archive/README.md`; Validacao para `QUALITY.md`; cinco stubs de uma linha ficam. Eliminar: roteamento por agente (L11-13), defaults do modelo (L63-64), repeticoes (L67-68, L127-131, Decisoes E Historico). Ficam: Ponto Cego (criterio da spec 0005 e verificador), Desempate, Passagem De Trabalho, Nunca Inferir, Gatilho, Ordem De Leitura. Correcoes ao texto da tarefa: as tres subsecoes somam 25 linhas e nao 55. Portao de contagem proposto para a rodada do corte: teto de 105 linhas nao vazias e 48 bullets, ancoras dos portoes antigos presentes, conteudo movido encontrado nos destinos. Nenhum corte executado. Decisoes para o usuario: remover "Onde Escrever" inteiro (maior risco); Ponto Cego fica; Validacao para QUALITY.md ou comprimida; apagar L63-64; segunda rodada nos blocos loop e specs (34 e 22 linhas).
- Pedido seguinte do usuario: um subagente do Cloudroom poderia ser o agente do `consenso.py` e do `loop.sh`? Resposta no chat: sim, como adaptador (wrapper que se comporta como CLI headless), sem tocar no contrato dos scripts. Prompt de planejamento salvo em `docs/PROMPTS.md`, secao "Planejar O Adaptador Cloudroom Para Consenso E Loop (Subagentes Visiveis)".
- Registro: `SESSION.md` rotacionado (tres entradas de 2026-10-17 para o archive, indice com 51), `TASKS.md` (dez concluidas, fila vazia), `MEMORY.md` (perfis, Armadilha, duas regras), `CHANGELOG.md` do projeto. Nada commitado.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `scripts/validate_structure.py`, `scripts/consenso.py`, `scripts/loop.sh`, `references/loop.md`, `references/consenso.md` (novo), `assets/AGENTS.md`, `assets/CLAUDE.md`, `assets/GEMINI.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`, `assets/docs/CONSENSUS.md`, `assets/docs/MEMORY.md`; `evals/verify_repository.py`, `evals/test_consenso.py`, `evals/test_loop.py`, `evals/evals.json`, `evals/portao_t060.py`, `evals/portao_t079.py`, `evals/portao_t083.py`, `evals/portao_t084.py` (novo), `evals/portao_t087.py` (novo), `evals/fixtures/origem-project/` (novo).
- Projeto: `AGENTS.md` (bloco core e marcadores), `CLAUDE.md`, `GEMINI.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/MEMORY.md`, `docs/CONSENSUS.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`, `docs/consensus/2026-10-21-043054-debate/` e `docs/consensus/2026-10-21-114042-debate/` (novos, as duas rodadas de T-083).
- Instalacao: `~/.claude/skills`, `~/.agents/skills`, `~/.gemini/skills` desta sandbox.

### Decisoes Tomadas

- Do usuario, no chat: fixtures e scripts tem de rodar em Linux, macOS e Windows; T-083 sem cursor-agent (sem tokens), segundo agente Codex `gpt-6.1-sol`; repetir a bancada nesta sandbox em `-s danger-full-access`. Nenhuma decisao formal nova em `DECISIONS.md`.
- Do gestor, registradas na evidencia: pisos das baterias no verificador iguais aos totais reais; check 5c em `portao_t079.py`; exigencia de comando executado em `portao_t083.py`; bump 2.13.0 antes de delegar a fase 3.

### Aprendizados Para MEMORY.md

- Promovidos (Feedback): portabilidade nos tres sistemas (sem `sed -i`, `perl`, `timeout`, `setsid`); portao de bancada real exige evidencia de leitura do repositorio, nao tamanho de saida. Promovido (Armadilha): sandbox read-only do Codex nao roda no container Cloudroom, e agente que le `consenso.py` na copia dispara a varredura de segredo pelo log (falso positivo previsto na DEC-010). Promovidos (User): perfis `Codex, consenso` e `Codex Sol, consenso`.

### Pendencias

- Do usuario: commitar; preencher o julgamento da entrada da rodada 2 em `docs/CONSENSUS.md` (Pontos De Acordo, Consenso Final, Decisao) e decidir se a posicao convergente vira tarefa no validador; decidir se arquiva a entrada da rodada 1 (falha de ambiente); mudar o `Status` da spec 0006 para `Concluida` se aceitar a evidencia; decidir o corte de T-090 (cinco perguntas acima).
- Fila de `docs/TASKS.md` vazia em "Proximas Tarefas" e em "Aguardando Usuario".

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para commitar, julgar a entrada da rodada 2 e fechar a spec 0006; depois qualquer agente de chat para a rodada do corte de T-090, se aprovada, com o portao de contagem proposto.
- Motivo: tudo o que nao depende de decisao humana esta feito; o que sobra e julgamento de consenso, status da spec e decisao de corte.

## 2026-10-20 - Claude (camada GitHub: comparacao com o ai-memory, decisao e prompt)

### Objetivo

- Analisar como o repositorio `github.com/adejaimejr/ai-project-structure` e usado e apresentado no GitHub, contra `github.com/akitaonrails/ai-memory`, e propor o que fazer. Pedido do usuario: analise e plano; depois, so o prompt para outra sessao executar.

### O Que Foi Feito

- Levantamento pela API do GitHub nos dois repositorios (sem clonar o ai-memory) e mapa local por tres subagentes Explore: nosso lado (arquivos de comunidade, CI, versao, fluxo git), o lado deles (README, CONTRIBUTING, SECURITY, templates, 9 workflows, 137 tags `vX.Y.Z` anotadas, releases com checksums, Keep a Changelog) e a mecanica de modulo opcional da skill (`SKILL.md`, partials, `MARKER_RE`, `verify_repository.py`, evals), para o modulo `github` seguir o molde de specs e loop.
- Diagnostico: 12 minors da skill no CHANGELOG e nenhuma tag nem Release; nenhum workflow (os dois portoes rodam so na maquina do mantenedor; o PR #1 mostrou que no Linux `sed -i ""` em `evals/test_loop.py:435` e `find -newer` em `scripts/loop.sh:173` derrubam o harness); descricao e topics vazios; health de comunidade 28% contra 85%; PR #1 de 4 linhas aberto ha 45 dias criando `.cursor/` na raiz; 73 commits diretos em `main`, nunca um PR integrado; `ROADMAP.md` parado em "lancar a v2". O que nao copiar: a maquinaria de binario Rust (Docker, AUR, RPM, Nix, CodeQL, gitleaks, branches `release/x.y`, README de 742 linhas). O plano completo, com a tabela comparativa e a fase B, ficou em `/Users/adejaimejunioer/.claude/plans/eu-preciso-de-uma-dynamic-lemur.md`.
- Decisoes do usuario: ingles so na camada GitHub, com `README.pt-BR.md`; praticas de GitHub entram em "Regras Do Projeto" e viram modulo opcional `github` da skill; o modulo e 2.14.0, depois da 2.13.0, com spec 0007. Registrado em `docs/DECISIONS.md` (raiz minima com `.github/` e comunidade em `docs/`; tag e Release a cada bump; PR para mudanca na skill), seis regras em `AGENTS.md`, excecao de idioma e estado atual em `PROJECT_CONTEXT.md`, `ROADMAP.md` reescrito.
- Executado no GitHub antes de o usuario pedir para parar: descricao em ingles, nove topics (`agents-md`, `agent-skills`, `claude-code`, `codex-cli`, `gemini-cli`, `multi-agent`, `context-engineering`, `markdown`, `ai-agents`), Wiki e Projects desligados; PR #1 fechado sem merge, com comentario, e a branch `cursor/setup-dev-environment-36f3` apagada (o commit `f330a8a` segue no objeto local e o GitHub oferece "Restore branch" no PR). Uma proposta de sessao para os arquivos de comunidade foi aberta e retirada.
- A pedido do usuario ("so quero o prompt, nao e para executar"), o resto nao foi executado: virou T-092 a T-099 em `TASKS.md` e o prompt "Aplicar A Camada GitHub E Abrir A Spec Do Modulo Github" em `docs/PROMPTS.md`, no molde do prompt anterior (gestor Fable, subagentes Sonnet, acao externa so com sim do usuario).
- Depois: `validate_structure.py . --strict` 0 erros e 0 avisos; `verify_repository.py` 74/74; zero travessao nos arquivos tocados.

### Arquivos Criados Ou Alterados

- `AGENTS.md` ("Regras Do Projeto"), `docs/DECISIONS.md`, `docs/PROJECT_CONTEXT.md`, `docs/ROADMAP.md`, `docs/TASKS.md` (T-092 a T-099), `docs/PROMPTS.md`, `docs/CHANGELOG.md`, `docs/SESSION.md`. Nenhum arquivo da skill.

### Decisoes Tomadas

- Camada GitHub do repositorio: raiz com `.github/` e dotfiles, comunidade em `docs/`, ingles por padrao com pt-BR opcional, tag e Release a cada bump, PR para mudanca na skill, modulo `github` na 2.14.0. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum promovido. Candidato: plano aprovado em plan mode nao e licenca para executar; quando o pedido original era "analise e me apresente", perguntar se o passo seguinte e executar ou escrever o prompt, antes de tocar o GitHub.

### Pendencias

- Do usuario: commitar (sugestao: `docs: camada GitHub, decisao, regras e prompt`).
- T-092 a T-099 na fila; a sessao que rodar o prompt abre a spec 0007 por ultimo.
- `docs/QUALITY.md`, linha "A raiz mantem apenas os arquivos Markdown de entrada dos agentes", e "Links Internos" de `PROJECT_CONTEXT.md` ficam para T-096.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): sessao nova em Fable 5.1 com o prompt "Aplicar A Camada GitHub E Abrir A Spec Do Modulo Github" de `docs/PROMPTS.md`.
- Motivo: as tarefas estao escritas com portao e ordem; o que falta e executar com o sim do usuario em cada acao externa.

## 2026-10-20 - Claude (analise do ai-memory de akitaonrails)

### Objetivo

- Responder se `github.com/akitaonrails/ai-memory` tem relacao com o ai-project-structure, se algo de la vale importar e se os dois deveriam ser mesclados.

### O Que Foi Feito

- Leitura do ai-memory pela API do GitHub, sem clonar: README, `AGENTS.md`, `INSTALL_FOR_AGENTS.md`, `DATA_HANDLING.md`, `docs/usage.md` (precedencia regras, memoria, perfil; compaction recap), `docs/cookbook.md`, `docs/comparison.md`, `docs/design-rules-promotion.md`, `docs/design-handoff-offer-not-claim.md`, as quatro Agent Skills de roteamento (`handoff`, `durable-pages`, `retrieval`, `learning-maintenance`), o README do companion `wikisync` e o snippet que ele injeta em `AGENTS.md` (`routing_snippet.rs`). Mapa do nosso lado por subagente Explore (layout, scripts, modelo de memoria, tarefas abertas, limites reconhecidos).
- O que ele e: binario Rust (11,9 mil stars, MIT) com servidor MCP/HTTP, hooks de ciclo de vida em mais de vinte harnesses, wiki Markdown propria em `<data_dir>/wiki/` com indice SQLite FTS5 (vetores opcionais), handoff tipado claim-once, perfil cross-project, decay e compactacao reversiveis, zero LLM e dado local por padrao.
- Veredito: sem relacao de origem (nenhum cita o outro; linhagens distintas), convergencia de desenho (`AGENTS.md` canonico, `CLAUDE.md` ponte, Markdown fonte). Camadas diferentes: nos somos o rules file e o registro revisado dentro do repo; ele e infraestrutura fora do repo que, pela precedencia que declara (usuario, rules file, memoria, perfil), fica abaixo de `AGENTS.md` e diz nao duplicar registro de decisao mantido no repo. Nao mesclar.
- Sobreposicao real: `SESSION.md` curado versus `sessions/<id>.md` capturado; "Proximo Passo Recomendado" versus handoff (o nosso ja e "oferta, nao reivindicacao", desenho que eles precisaram de um design doc, #959, para adotar); `MEMORY.md` versus `_rules/`, `gotchas/` e perfil; `DECISIONS.md` versus `decisions/` ADR fixada. Sem equivalente la: tarefas com evidencia, consenso com independencia declarada, specs, loop com portao, validador. Sem equivalente ca: captura automatica, busca, multi-maquina e time, compaction recap.
- Ideias apresentadas ao usuario, A a F; escolhidas A a E, todas em texto: import real `@AGENTS.md` nas pontes (ponteiro em prosa nao carrega nada no inicio; Claude Code 2.1.277+ so le `AGENTS.md` sozinho sem `CLAUDE.md`); medir o orcamento de instrucoes do `AGENTS.md` (raiz com 319 linhas; literatura citada por eles poe aderencia confiavel em cerca de 150 a 200 instrucoes); memoria tratada como evidencia, nao instrucao; releitura de `SESSION.md` e `TASKS.md` apos compactacao; tipo "Armadilha" em `MEMORY.md`. Recusada F, receita de coexistencia: fica so a nota em `MEMORY.md`. Nao importar: hooks, MCP, servidor, SQLite, embeddings, decay, captura silenciosa, perfil cross-project, `wikisync` para dentro de `docs/`.
- Registro: decisao em `DECISIONS.md`, referencia em `MEMORY.md`, T-087 a T-091 em `TASKS.md`, linha no `CHANGELOG.md`. Nenhum arquivo da skill mudou. Depois: `validate_structure.py . --strict` 0 erros e 0 avisos; `verify_repository.py` 74/74; zero travessao em `docs/*.md`, `AGENTS.md` e pontes.
- Pedido seguinte do usuario: prompt para a proxima sessao executar a fila (T-078 a T-084, T-087 a T-091) com gestor em Fable 5.1 e subagentes em Sonnet 5.5, um por vez, revisados por portao, verificador e mutacao. Entregue no chat e salvo em `docs/PROMPTS.md`, secao "Rodar As Tarefas Pendentes Com Subagentes Sonnet Revisados Por Fable".

### Arquivos Criados Ou Alterados

- `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/PROMPTS.md`.

### Decisoes Tomadas

- ai-memory e camada complementar fora do repositorio; nao mesclar; importar ideias por tarefa, nunca mecanismo. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Entrada Reference sobre o ai-memory (o que e, precedencia que declara, nota de coexistencia). Promovida.

### Pendencias

- Do usuario: commitar.
- T-087 a T-091 pedem bump 2.13.0: ordem, depois de T-078 a T-083 ou junto com T-084, para nao repetir a troca de "nao suba de novo" nas linhas delas.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): sessao nova em Fable 5.1 com o prompt "Rodar As Tarefas Pendentes Com Subagentes Sonnet Revisados Por Fable" de `docs/PROMPTS.md`, que cobre T-078 a T-084 e T-087 a T-091 em quatro fases, com um bump (2.13.0) na terceira.
- Motivo: a analise nao muda a fila da spec 0006; as adocoes sao texto do bloco core, das pontes e do template de `MEMORY.md`, e cabem numa rodada depois da spec.

## 2026-10-17 - Claude (sessao lateral: T-086, skill 2.12.0 levando Passagem De Trabalho)

### Objetivo

- Fechar T-086: subir a skill para 2.12.0 levando a secao "Passagem De Trabalho" do bloco core, que entrou na 2.11.0 sem bump com a 2.11.0 ja publicada em `origin/main`. Sessao lateral aberta pela sessao do protocolo de handoff, com o briefing no formato da propria secao nova.

### O Que Foi Feito

- Pre-condicoes do briefing: `git status` tinha `AGENTS.md`, `assets/AGENTS.md` e `SESSION.md` sem commit; parei e pedi o commit (fdafa73, arvore limpa). Confirmacao do usuario, relayada pela sessao gestora: "Sim, 2.12.0 agora" (bump antes de T-078 a T-083) e "Migrar os dois" (itens pos-publicacao da 2.11.0 para a secao nova).
- Portao antes do bump: `evals/portao_t086.py`, molde de `portao_t058.py` sobre `portao_consenso_lib.py` (`versao_coerente("2.12.0")`), 8 checks: versao coerente em frontmatter, prosa, marcadores dos assets e CHANGELOG; secao mais recente do CHANGELOG cita "Passagem De Trabalho"; tres marcadores da raiz na versao do frontmatter; bloco core da raiz byte a byte igual ao dos assets e com a secao dentro; T-078 a T-083 sem "a versao ja e 2.11.0" (T-078 a T-082 apontando para a nova; T-083 nunca teve a frase); raiz `--strict`; verificador. Com a arvore de hoje saiu 6/8 pelo motivo certo (1a e 4).
- Bump: `version: "2.12.0"` e `versao da estrutura: 2.12.0` no `SKILL.md`; marcadores `core`, `specs` e `loop` em v2.12.0 em `assets/AGENTS.md`, nos dois partials e nos tres blocos do `AGENTS.md` da raiz, conteudo dos blocos intocado; comentario do `agents/openai.yaml` ("Desde a 2.12.0", porque o item dos gatilhos migrou). CHANGELOG da skill: secao `## 2.12.0 - 2026-10-17` com paragrafo explicando a migracao e os dois itens movidos da 2.11.0 (gatilhos da `description`; secao Passagem De Trabalho e passo 2 de `atualizacao.md`); a 2.11.0 fica so com o que foi publicado.
- `docs/TASKS.md`: nas linhas de T-078 a T-082, "a versao ja e 2.11.0, nao suba de novo, acrescente um item na secao `## 2.11.0`" e "o `AGENTS.md` da raiz ja esta em v2.11.0" passam a 2.12.0 (16 trocas; T-082 tambem "item no CHANGELOG 2.12.0"). T-083 nao tinha a frase. T-077, concluida, fica como registro historico.
- Depois: portao 8/8, `verify_repository.py` 74/74, `validate_structure.py . --strict` 0 erros e 0 avisos, sem `__pycache__`, sem travessao nos arquivos tocados.
- Mutacoes, backup por `cp` e volta conferida por `cmp`: marcador core da raiz de volta a v2.11.0, 5/8 (2, 3a, 6 com 72/74); secao Passagem De Trabalho removida so da raiz, 6/8 (3a, 6 com 73/74); T-080 de volta a 2.11.0, 7/8 (4); prosa do `SKILL.md` em 2.11.0, 6/8 (1a, 6 com 73/74).
- Reinstalada com `install.sh --sim`: 33 arquivos distribuidos comparados por `cmp` em `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`, 0 divergentes, `version: "2.12.0"` nos tres.
- `SESSION.md` passaria de 30KB com esta entrada: as duas entradas de 2026-09-04 (plano da spec 0006 com T-075 a T-077 e a 2.11.0; respostas de T-053 e T-074) foram para `docs/archive/SESSIONS-2026.md`, indice atualizado (48 entradas). Ficam 4 aqui.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `agents/openai.yaml`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`; `evals/portao_t086.py` (novo, nao distribuido).
- Projeto: `AGENTS.md` (so os tres marcadores), `docs/TASKS.md` (T-086 concluida; T-078 a T-082), `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.
- Instalacao: `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`.

### Decisoes Tomadas

- Do usuario, dentro da tarefa: bump 2.12.0 antes de T-078 a T-083, e os dois itens escritos depois da publicacao migram da 2.11.0 para a 2.12.0 no CHANGELOG da skill. Nenhuma decisao formal nova em `DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Candidato, nao promovido (fora do escopo pedido): bloco gerenciado que muda com a versao ja publicada precisa do bump na mesma sessao; adiar o bump por regra de outras tarefas deixou a versao publicada com dois conteudos e custou uma tarefa propria para desfazer.

### Pendencias

- Do usuario: commitar (nada commitado nem pushado nesta sessao).
- T-078 a T-083 seguem na fila, agora com a regra "a versao ja e 2.12.0, nao suba de novo".

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para mandar T-078 ao loop; os portoes delas aceitam 2.11.0 ou acima e o verificador esta verde.
- Motivo: o bump era o unico bloqueio de versao; a spec 0006 segue de onde parou.

