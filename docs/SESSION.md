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

## 2026-10-17 - Claude (passagem de trabalho entre gestor e subagentes)

### Objetivo

- Dar a estrutura um protocolo leve de passagem de trabalho entre um agente gestor e seus subagentes no Cloudroom, usando a skill Handoff (davidondrej) como referencia de metodo, sem copia-la nem exigir a instalacao dela. Restricoes do pedido: nenhum documento permanente novo, subagente nao le a skill inteira, o resumo leva so o contexto da tarefa e funciona com os agentes em sandboxes diferentes.

### O Que Foi Feito

- Leitura: `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `TASKS.md`, `SKILL.md`, `references/atualizacao.md` e `loop.md`, o prompt do `loop.sh`, o envelope do `consenso.py`, `verify_repository.py` e as referencias do `room-cli` sobre sandboxes (filho Cloud de pai Local tem sandbox propria e parte do GitHub).
- Diagnostico: a estrutura nao tinha regra de delegacao. O unico envelope de passagem existente e o prompt do `loop.sh`, que ja carrega tarefa, portao, saida da falha anterior e proibicoes, mas pressupoe filesystem compartilhado. O principio ja escrito em `loop.md` ("regra critica vai no prompt, nao so no bloco") e o mesmo que vale aqui: o que o subagente precisa chega na mensagem, porque ler arquivo e opcional e arquivo temporario de outra sandbox nem existe.
- Mudanca minima: secao `## Passagem De Trabalho` no bloco core de `AGENTS.md` (assets e raiz), entre "Memoria Persistente" e "Consenso Entre Modelos": 19 linhas, 1362 bytes. Um paragrafo com a premissa (outra sandbox; o resumo viaja na mensagem; `docs/` segue como registro e o resumo aponta para ele), um modelo de cinco linhas (tarefa e criterio de conclusao, estado feito e pendente, decisoes e tentativas a nao repetir, arquivos a consultar por caminho, conferir o estado real antes de agir) e quatro bullets (estado em vez de ordens; so o contexto da tarefa, sem repetir regras nem colar `docs/`; sem segredo; retorno pelo mesmo canal e registro por quem delegou). Validador intocado: o resumo vive na mensagem, nao em arquivo, e nenhum script o ve.
- Sem bump: item na secao 2.11.0 do CHANGELOG da skill, como nas duas sessoes anteriores, porque T-078 a T-083 mandam nao subir a versao. Custo dessa escolha: a 2.11.0 publicada no GitHub (`origin/main` igual a `main`) passa a ter dois conteudos de bloco core, e o passo 2 de `atualizacao.md` encerrava em versao igual sem olhar o bloco. Conserto de uma linha no passo 2: versao igual e bloco diferente do template segue para o passo 4 so com aquele bloco, com diff e confirmacao. O bump virou T-086.
- Verificacao: `verify_repository.py` 74/74 antes e depois; `validate_structure.py . --strict` 0 erros e 0 avisos; scaffold minimal montado dos assets em pasta temporaria passa em `--strict` com a secao dentro; zero travessao e cercas pareadas no bloco core. Mutacoes com backup por `cp` e volta conferida por `cmp`: secao removida so dos assets, verificador 73/74 ("bloco core identico" falha); travessao dentro da secao nos dois arquivos, 70/74 (strict da raiz, as duas baterias e o check de travessao). Reinstalada nos tres destinos com `install.sh --sim`, paridade por `cmp`.
- `SESSION.md` passaria de 30KB: as duas entradas mais antigas (2.10.0 com T-054, T-056, T-058 e T-055; 2.9.1 com T-062 e T-073) foram para `docs/archive/SESSIONS-2026.md`, indice atualizado (46 entradas). A primeira rotacao, de uma entrada so, deixou o arquivo em 31KB e o validador avisou `ROTACAO`.

### Arquivos Criados Ou Alterados

- Skill: `assets/AGENTS.md` (secao nova no core), `references/atualizacao.md` (passo 2), `CHANGELOG.md` (item na 2.11.0).
- Projeto: `AGENTS.md` (mesma secao), `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md` (T-086), `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.
- Instalacao: `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`.

### Decisoes Tomadas

- Contexto de delegacao viaja na mensagem, nunca em arquivo temporario nem em documento novo; `docs/` segue como registro. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum. A premissa do Cloudroom (subagente em outra sandbox) ficou escrita no proprio `AGENTS.md`, onde todo agente a le.

### Pendencias

- T-086: bump da skill levando a secao, para o fluxo de atualizacao oferecer o bloco a projeto ja em 2.11.0 e para a 2.11.0 publicada nao ter dois conteudos; depende de T-078 a T-083 liberarem o "nao suba", ou vai junto com T-084.
- Cloudroom, fora deste repositorio: continua pendente, da sessao anterior, o template de delegacao do gestor para a skill (nomear a estrutura e pre-responder a entrevista); a secao nova cobre a parte geral.
- Do usuario: commitar.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para mandar T-078 ao loop com o verificador verde; o gestor no Cloudroom passa a delegar com o resumo da secao nova.
- Motivo: a secao nao bloqueia nada; T-078 e a proxima da spec 0006 e o verificador esta verde.

## 2026-10-17 - Claude (T-085: fixture aguardando-project com data relativa)

### Objetivo

- Fechar T-085: `verify_repository.py` em 71/74 porque a fixture `aguardando-project` tinha `(bloqueada: 2026-09-01)` absoluto e o validador compara com `date.today()` (limite 30 dias). Envelhecimento, nao regressao: validador e fixture intocados desde setembro. Bloqueava os portoes de T-078 a T-083, que rodam o verificador pela base `portao_consenso_lib.py`.

### O Que Foi Feito

- Portao antes do conserto: `evals/portao_t085.py`, molde de `portao_t058.py`, 9 checks. Com a data real saiu 3/9 pelo motivo certo (tres datas absolutas; verificador sem `materializar_fixture`; 71/74).
- Solucao (b) da tarefa, so em `evals/`, sem bump: token `{{HOJE-N}}` na fixture, materializado em pasta temporaria por `materializar_fixture(origem, destino, hoje)` em `verify_repository.py`, que absorveu as trocas de `{{TRAVESSAO}}` e `{{UTF8_INVALIDO}}`. `valido` e `invalido` usam `{{HOJE-7}}`; `invalido` ganhou T-007 com `{{HOJE-45}}`, bloqueada antiga de proposito, e `TASK-BLOQUEADA-ANTIGA|T-007` entrou no oracle (ate aqui so `cobertura-tarefas`, com 2000-01-01, produzia o codigo). `validate_structure.py` intocado: em projeto real o check segue relativo a hoje. README da fixture explica o token.
- Opcao (a), data de referencia no validador, descartada: toca `scripts/`, exige bump e reinstalacao, e T-078 a T-083 mandam nao subir a 2.11.0 nao commitada.
- Depois: portao 9/9, verificador 74/74, raiz `--strict` com 0 erros e 0 avisos, sem `__pycache__`.
- Mutacoes, backup por `cp` e volta conferida por `cmp`: data absoluta de volta em `valido`, 6/9 (1a, 1b, 3d; verificador 72/74); `hoje` forcado para daqui a um ano no verificador, 6/9 (1c, 2a, 3d; 73/74); para um ano atras, 6/9 (1b, 2b, 3d; 71/74). O parametro `hoje` existe so para o portao viajar no tempo pela mesma funcao do verificador.

### Arquivos Criados Ou Alterados

- Skill, nao distribuidos: `evals/portao_t085.py` (novo), `evals/verify_repository.py`, `evals/fixtures/aguardando-project/README.md`, `valido/docs/TASKS.md` e `invalido/docs/TASKS.md` da mesma fixture.
- Projeto: `docs/TASKS.md` (T-085 concluida), `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Nenhuma formal. Escolha de implementacao dentro da tarefa: fixture relativa em vez de flag no validador.

### Aprendizados Para MEMORY.md

- Confirmado o candidato da sessao anterior: fixture com data absoluta sob check relativo a `date.today()` envelhece sozinha e derruba o verificador sem regressao; data que o validador compara com hoje entra na fixture como token relativo, materializado no teste. Nao promovido aqui: `MEMORY.md` fora do escopo pedido.

### Pendencias

- Promover o aprendizado acima para `MEMORY.md`.
- CHANGELOG da skill (secao 2.11.0) sem item desta mudanca: `evals/` nao e distribuido e o escopo pedido nao o incluia; decidir se entra.
- Do usuario: commitar (2.11.0 inteira, gatilhos e T-085 seguem nao commitados).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para mandar T-078 ao loop com o verificador verde.
- Motivo: a causa alheia dos portoes vermelhos saiu; o que falhar agora e da propria tarefa.

## 2026-10-17 - Claude (gatilhos da skill para o fluxo gestor e subagentes no Cloudroom)

### Objetivo

- Revisar os gatilhos da skill `ai-project-structure` para o uso no Cloudroom, onde um agente gestor coordena subagentes em sandbox: o gestor decide quando um projeto precisa da estrutura, os subagentes so a executam quando recebem essa tarefa, e o pedido direto do usuario continua valendo. Analise e proposta antes de qualquer edicao, a pedido do usuario; aplicacao depois da aprovacao.

### O Que Foi Feito

- Leitura: `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `SKILL.md`, `agents/openai.yaml`, `evals.json`, `install.sh`, `verify_repository.py` (so checa `version` no frontmatter, nunca a `description`) e as referencias do `room-cli` (skills chegam aos agentes pelos roots globais `~/.claude/skills` e `~/.agents/skills`; `.bb/AGENTS.md` na raiz do workspace injeta instrucao em toda thread).
- Diagnostico: a `description` do frontmatter e a unica superficie de roteamento, e a skill nao sabe quem a chama; a tarefa do gestor chega ao subagente como se fosse o pedido do usuario. As frases genericas ("cria projeto", "inicia projeto novo", "scaffold projeto", "estrutura inicial", "monta a base do projeto", "cria a pasta do projeto", "projeto de IA") faziam um subagente mandado fazer scaffold de codigo abrir a entrevista ou criar `AGENTS.md` e `docs/` sem pedido, tirando a decisao do gestor. Os gatilhos especificos (estrutura multiagente, atualizar, validar, specs, loop) nao conflitam.
- Proposta aprovada e aplicada: `description` reescrita com clausula positiva estreita (nomear a estrutura ou seus arquivos, citar a skill, fluxos de atualizar, validar, specs e loop) e clausula negativa (pedido generico nao dispara; quem coordena decide; no maximo oferecer a estrutura em uma linha). Escalar YAML plano, sem `": "` nem travessao; Claude Code releu a skill com o texto novo na mesma sessao. Comentario do `openai.yaml` atualizado, `allow_implicit_invocation` segue `true`. Eval 2 passa a nomear a estrutura no prompt; eval 4 ("Inicia projeto novo aqui.") passa a esperar oferta e confirmacao antes da entrevista; eval 11 novo, negativo (projeto Node com Vite nao aciona). Item na secao 2.11.0 do CHANGELOG da skill, sem bump: a 2.11.0 nao foi commitada e T-078 a T-083 pedem para nao subir; os portoes aceitam "2.11.0 ou acima".
- Casos ambiguos decididos com o usuario: "inicia projeto novo" sozinho sai dos gatilhos (custa um turno de confirmacao no chat direto); "scaffold projeto" e "estrutura inicial" saem por casarem com scaffold de codigo; "projeto de IA" e "repo de IA" saem porque projeto sobre IA nao e projeto para varias IAs. Travas mecanicas (`allow_implicit_invocation: false` no Codex, `disable-model-invocation` no Claude Code, esta a confirmar na documentacao) rejeitadas por exigirem invocar a skill pelo nome e quebrarem o pedido direto em linguagem natural.
- Verificacao: `validate_structure.py . --strict` sem problema; frontmatter com tres chaves; zero travessao nos quatro arquivos. `verify_repository.py` em **71/74**: as tres falhas sao `TASK-BLOQUEADA-ANTIGA` na fixture `aguardando-project` (`valido` em `--strict` e as contagens exatas de `valido` e `invalido`), porque o validador compara `(bloqueada:)` com `date.today()` e as datas de setembro da fixture passaram do limite. Nada a ver com esta mudanca: validador e fixture intocados desde 2026-09-04. Virou T-085, prioridade alta, porque `portao_consenso_lib.py` roda o verificador e toda rodada de loop de T-078 a T-083 ficaria vermelha por causa alheia.
- Reinstalada nos tres destinos com `install.sh --sim` (divergencia listada em cada um: `SKILL.md` e `agents/openai.yaml`); paridade conferida por `cmp` nos dois arquivos, nos tres destinos.
- Rotacao: `SESSION.md` passaria de 30KB com esta entrada; as tres entradas mais antigas (2.9.0 com T-064 e T-063, 2.8.1 com T-060, 2.8.0 com T-072 e T-071) foram para `docs/archive/SESSIONS-2026.md`, indice do archive atualizado (44 entradas).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md` (description), `agents/openai.yaml` (comentario), `evals/evals.json` (evals 2, 4 e 11), `CHANGELOG.md` (item na 2.11.0).
- Projeto: `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/TASKS.md` (T-085), `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.
- Instalacao: `~/.claude/skills`, `~/.agents/skills` e `~/.gemini/skills`.

### Decisoes Tomadas

- Gatilho da skill nao decide se um projeto ganha a estrutura; quem coordena decide. Registrada em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum promovido. Candidato ainda em hipotese: fixture com data absoluta sob check relativo a `date.today()` envelhece sozinha e derruba o verificador sem regressao real; vira regra se T-085 confirmar o conserto.

### Pendencias

- T-085 (fixture `aguardando-project` envelhecendo; verificador em 71/74) antes de qualquer rodada de loop de T-078 a T-083.
- Do usuario: commitar. A 2.11.0 inteira continua nao commitada, e esta sessao soma a mudanca de gatilhos.
- Cloudroom, fora deste repositorio: linha em `.bb/AGENTS.md` do workspace repetindo a regra, e template de delegacao do gestor nomeando a estrutura e pre-respondendo as quatro perguntas da entrevista (nome, objetivo, minimal ou completa, specs), para o subagente nao travar perguntando ao gestor.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente de chat, para T-085 antes de mandar T-078 ao loop; portao proprio escrito antes da rodada.
- Motivo: verificador vermelho por causa alheia esconde regressao real, e todos os portoes abertos passam por ele.
