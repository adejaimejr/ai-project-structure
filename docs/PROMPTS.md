# PROMPTS

Prompts reutilizaveis para trabalhar com esta estrutura.

## Criar Ou Organizar Projeto Com Esta Estrutura

```md
Use esta estrutura multiagente ao criar ou organizar um projeto tocado por IA. Mantenha na raiz apenas AGENTS.md, CLAUDE.md e GEMINI.md. Coloque a memoria do projeto em docs/. Use AGENTS.md como fonte central, docs/SESSION.md para continuidade entre sessoes e docs/CONSENSUS.md quando modelos diferentes precisarem debater antes de uma decisao.
```

## Pedir Opiniao Ao Claude

```md
Claude, esta estrutura foi criada para manter projetos tocados por IA organizados, com uma fonte central de regras em AGENTS.md, memoria de sessoes em docs/SESSION.md e debate entre modelos em docs/CONSENSUS.md. Analise a estrutura e sugira melhorias se encontrar algo que possa deixar o fluxo mais claro, seguro ou facil de manter.
```

## Iniciar Nova Sessao De IA

```md
Leia AGENTS.md e depois consulte docs/SESSION.md, docs/PROJECT_CONTEXT.md, docs/TASKS.md e docs/QUALITY.md. Continue a partir do estado mais recente do projeto e registre no final da sessao o que foi feito, decisoes, pendencias e proximo passo.
```

## Solicitar Consenso Entre Modelos

```md
Use docs/CONSENSUS.md para registrar sua posicao sobre esta decisao. Inclua contexto, recomendacao, riscos, tradeoffs e o que voce considera necessario para chegar a um consenso com outros modelos.
```

## Revisao Antes De Finalizar

```md
Revise a mudanca usando docs/QUALITY.md. Verifique se a tarefa foi atendida, se o escopo foi respeitado, se a memoria da sessao precisa ser atualizada e se alguma decisao deve ir para docs/DECISIONS.md.
```

## Revalidar A Skill Inteira Em Varios Modelos

Prompt para abrir uma sessao nova cujo objetivo e **atacar** a skill 2.5.1 e tudo que foi construido em cima dela, usando os modelos disponiveis, e transformar o que sobreviver em conserto.

Escrito em 2026-09-03, depois de tres rodadas de consenso que acharam sete defeitos reais em codigo ja publicado. Reaproveitando em versao futura, atualize a versao da skill, a lista de tarefas abertas e o inventario de modelos, que envelhece rapido.

```text
Contexto: /Users/adejaimejunioer/Dev/2026/ai-project-structure. Skill `ai-project-structure` 2.5.1, publicada e instalada. Sou o dono do projeto e quero uma revalidacao adversarial do sistema inteiro, usando varios modelos, para descobrir onde ele nao entrega o que promete.

Nao quero uma nota de aprovacao. Quero achados, e quero que os que sobreviverem virem conserto.

## Leia antes de qualquer coisa

1. `AGENTS.md` inteiro.
2. `docs/SESSION.md`, as quatro entradas mais recentes.
3. `docs/TASKS.md`, secoes abertas.
4. `docs/DECISIONS.md`, as tres entradas de 2026-09-03.
5. `docs/specs/0006-automacao-do-consenso.md`, incluindo DEC-001 a DEC-006 e as tres perguntas abertas.
6. `docs/MEMORY.md`, secoes `## User`, `## Feedback` e `## Project`. E ali que estao os perfis de agente e as licoes que ja custaram tempo.

## O que ja esta resolvido, e voce nao deve redescobrir

- A estrutura, o modulo de specs e o modulo de loop existem e estao validados por bancada. Nao repita bancada de loop.
- O formato de achado (2.4.0) e o diagnostico com identificador estavel (2.5.0) foram desenhados e provados por mutacao.
- Sete defeitos ja foram achados e registrados: T-054, T-055, T-056 e T-058 seguem abertos, com o problema descrito e o conserto ainda em aberto. Nao os reache: confirme que continuam validos e siga adiante.
- Tres calibragens da spec 0006 esperam decisao minha, em T-053. Nao decida por mim.

## O que quero descobrir

Onde o sistema **promete e nao entrega**. A validacao e da skill **inteira**: sete superficies, e nenhum arquivo dela pode ficar de fora. A pergunta que interessa em cada uma:

1. **Contrato do bloco core (`AGENTS.md`).** Que regra dele nao e verificavel, nem por script nem por pessoa? Que regra e violavel sem que nada acuse? Ha regra que contradiz outra?
2. **Validador (`scripts/validate_structure.py`).** Os 39 diagnosticos cobram o que dizem cobrar? Onde estao os falsos negativos, ou seja, o documento errado que passa limpo? Escreva o documento que passa e nao deveria.
3. **Modulo de loop (`scripts/loop.sh`, `scripts/loop_task.py`, `references/loop.md`).** Qual e o caminho em que o loop escreve algo que o comando nao comprova? Onde ele perde trabalho? O que acontece com entrada hostil, arquivo enorme, ou tarefa cujo portao mente?
4. **Portao dos evals (`evals/verify_repository.py`, `evals/test_loop.py`, `evals/fixtures/`, `evals/evals.json`).** Que mutacao no codigo passa verde? Esta e a pergunta mais importante das sete, porque um portao cego faz todas as outras respostas valerem menos.
5. **Fluxos de scaffold, atualizacao e specs (`SKILL.md`, `references/atualizacao.md`, `references/specs.md`).** Um agente que nunca viu este projeto consegue seguir? Onde ele erraria? Aqui **execute de verdade** num diretorio descartavel, contra a **copia instalada** da skill, que e como ela dispara nas ferramentas. Ler o texto nao substitui rodar.
6. **Templates entregues (`assets/`).** E o que o usuario final de fato recebe. Um projeto criado a partir deles passa em `--strict` no dia seguinte? Os templates concordam com o bloco core, ou algum ficou para tras quando o core mudou? T-055 e um defeito exatamente desta classe, ja achado: procure irmaos dele. Confira tambem que `assets/partials/` nunca e copiado para o projeto-alvo.
7. **Distribuicao (`install.sh`, `agents/openai.yaml`, `README.md` e `CHANGELOG.md` da skill).** O `install.sh` e idempotente de verdade? O que ele faz com instalacao parcial, com destino ja existente e diferente, e com `--uninstall`? O que ele **nao** distribui esta certo? O `agents/openai.yaml` declara `allow_implicit_invocation: true`, e isso corresponde ao comportamento real no Codex? O `README.md` da skill descreve o que o codigo faz hoje, ou envelheceu?

**Inventario de cobertura.** Antes de fechar, prove que nada ficou de fora. Todo item abaixo tem de aparecer no seu relatorio com a superficie que o atacou e o veredito:

```
SKILL.md                     -> superficie 5
README.md                    -> superficie 7
CHANGELOG.md                 -> superficie 7
install.sh                   -> superficie 7
agents/openai.yaml           -> superficie 7
assets/AGENTS.md             -> superficies 1 e 6
assets/CLAUDE.md             -> superficie 6
assets/GEMINI.md             -> superficie 6
assets/docs/                 -> superficie 6
assets/partials/             -> superficies 5 e 6
references/atualizacao.md    -> superficie 5
references/specs.md          -> superficie 5
references/loop.md           -> superficie 3
scripts/validate_structure.py-> superficie 2
scripts/loop.sh              -> superficie 3
scripts/loop_task.py         -> superficie 3
evals/                       -> superficie 4
```

Se voce concluir que algum item nao vale ser atacado, diga qual e por que. Omissao declarada e aceitavel; omissao silenciosa nao.

## Metodo

**Confira o inventario de modelos antes de assumir qualquer coisa.** Rode `cursor-agent --list-models`, `codex --version` e `claude --help`. O que sei hoje, e pode ter mudado:

- `cursor-agent -p --force --model <id>` da acesso a varias familias com uma assinatura: `cursor-grok-4.6-xhigh`, `gpt-5.6-sol-xhigh`, `claude-opus-5-thinking-high`, `gemini-3.8-flash-high`, `kimi-k3-max`, `glm-5.2-max`. Use `--mode ask` para parecer somente-leitura.
- `codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high"` funciona direto.
- A CLI propria do Grok esta bloqueada por cota mesmo com assinatura; use o Grok pelo `cursor-agent`.
- A CLI do Gemini nao roda nesta maquina; use o Gemini pelo `cursor-agent`.

**Uma familia de modelo por superficie, nao a mesma pergunta para todos.** Sete agentes fazendo a mesma pergunta produzem sete versoes do mesmo vies. Distribua as sete superficies entre familias diferentes, e use uma familia **diferente da que achou** para verificar cada achado. Se o orcamento nao der para sete rodadas, agrupe superficies vizinhas (2 com 4, 6 com 7) e diga que agrupou, em vez de cortar superficie em silencio.

**Cada agente roda cego e isolado.** Aplique a DEC-003 da spec 0006: crie um worktree descartavel (`git worktree add`) e retire de la o corpo das entradas de `docs/CONSENSUS.md`, **deixando uma nota dizendo que a omissao foi proposital**. Agente que ve arquivo incompleto sem aviso conclui coisa errada sobre o repositorio. Mantenha os modelos de debate e de achado, que sao referencia de forma.

**Sele a sua propria posicao antes de rodar qualquer agente**, num arquivo fora do repositorio, se voce for opinar. Escrever depois de ler os outros e `debate-aberto` fingindo ser parecer independente.

**Confira todo achado no codigo antes de aceitar.** Isto nao e opcional e e o que separou sinal de ruido nas rodadas anteriores: varios achados estavam certos, e a moldura de alguns estava errada. Achado que voce nao conseguiu confirmar no codigo entra como "nao confirmado", nunca como achado.

**Mutacao, e nao leitura, para a superficie 4.** Quebre de proposito o que o portao deveria pegar, rode, e veja se ele acusa. Reverta a mutacao com backup feito por `cp` antes, **nunca com `git checkout`**: o arquivo pode ter trabalho nao commitado por cima, e isso ja destruiu uma reescrita inteira aqui.

## Como registrar

- Cada achado vira uma entrada de achado em `docs/CONSENSUS.md`, no formato da 2.4.0: `**Achado:** <identificador>`, `**Escapou de verificacao:** sim | nao`, disposicao, e a secao "Por Que Nada Pegou Antes" quando escapou. Use identificador ligado a superficie, por exemplo `REVAL-1`.
- Achado so vira tarefa em `docs/TASKS.md` **depois** de a disposicao concluir que ha trabalho (DEC-006 da spec 0005), e a tarefa cita o achado.
- Conserto que voce aplicar carrega evidencia de comando, e o comando declarado em `(verifica:)` precisa aparecer no campo `resultado=`.
- **Nao decida o que e meu.** Calibragem de escopo, mudanca de contrato publico e qualquer coisa que mude o que a skill promete: registre com as opcoes e o tradeoff, e me pergunte.

## Restricoes que ja custaram tempo aqui

- **Nenhum travessao (U+2014).** O validador trata como ERRO e varre tambem arquivo nao commitado.
- **Nada de `scripts/` na raiz.** Ferramenta so-do-repo vai em `docs/skills/ai-project-structure/evals/`.
- `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` da skill **nao sao distribuidos** pelo `install.sh`. Mudanca so neles nao exige reinstalacao nem bump.
- **O bloco core da raiz e do `assets/AGENTS.md` tem de ficar byte a byte identico.** Edite o asset e propague por script.
- **Subiu versao?** `SKILL.md`, os marcadores dos tres blocos e a secao do `CHANGELOG` da skill precisam bater, senao `verify_repository.py` reprova.
- **`docs/CONSENSUS.md` e `docs/SESSION.md` batem em 30KB rapido** e disparam `AVISO|ROTACAO`. Rotacione para `docs/archive/` e atualize o indice de la. Nao encurte conteudo para o portao ficar verde: isso e exatamente o que a regra "Nao Apague O Que Falha" proibe.
- **Ao cortar secao de `CONSENSUS.md` por script, ancore a busca no inicio da entrada.** Os mesmos headings existem no modelo cercado no topo do arquivo, e um `index()` ingenuo casa com o template e duplica a entrada inteira. Ja aconteceu.
- **As CLIs se atualizam sozinhas no meio da sessao.** Antes de atribuir mudanca de comportamento a uma alteracao sua, confira a versao.
- **Nao deixe artefato bruto so em `/tmp`.** Ele some, e o material das rodadas anteriores ja se perdeu assim.

## Verificacao, ao terminar cada tarefa

```
python3 docs/skills/ai-project-structure/evals/verify_repository.py
python3 docs/skills/ai-project-structure/evals/test_loop.py
python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict
```

Baseline de hoje: 44 de 44, 58 de 58, e exit 0 sem erro e sem aviso. Qualquer numero menor e regressao sua, nao ruido.

## Pronto quando

1. As sete superficies foram atacadas, com o registro de qual familia rodou onde e com que comando, e o inventario de cobertura preenchido item a item.
2. Todo achado foi confirmado no codigo, ou marcado explicitamente como nao confirmado.
3. A superficie 4 tem pelo menos tres mutacoes executadas, com o resultado de cada uma escrito, incluindo as que o portao **nao** pegou.
4. Os achados estao em `docs/CONSENSUS.md` e o trabalho que sobrou esta em `docs/TASKS.md`.
5. As tres verificacoes passam, e a sessao esta registrada em `docs/SESSION.md`.
6. Voce me disse, em uma frase, qual foi o achado mais caro e por que ele escapou ate agora.

Comece confirmando o inventario de modelos e me mostrando o plano de distribuicao das cinco superficies antes de gastar a primeira chamada.
```

## Rodar Os Evals Da Skill Em Outra Ferramenta

Os evals de `docs/skills/ai-project-structure/evals/evals.json` precisam rodar nas tres ferramentas (Claude Code, Codex CLI, Gemini CLI) antes de uma versao da skill ser considerada validada. Os dois prompts abaixo cobrem Codex e Gemini.

Tres coisas mudam entre as ferramentas e ja estao ajustadas em cada prompt:

| | Codex CLI | Gemini CLI |
|---|---|---|
| Invocacao | `$ai-project-structure` ou `/skills` | ativa pela `description`, sem citar o nome |
| Skill instalada | `~/.agents/skills/ai-project-structure` | `~/.gemini/skills/ai-project-structure` |
| Diretorio de teste | `/tmp/skill-v2-tests-codex/` | `/tmp/skill-v2-tests-gemini/` |

Rode o Codex primeiro. Assim a ultima ferramenta encontra as outras duas ja registradas e consegue fechar a tarefa e a spec na mesma sessao.

Ao reaproveitar em versoes futuras, troque o numero da tarefa, o numero da spec e a linha de baseline pelos valores da rodada corrente.

### Codex CLI

```text
Invoque a skill $ai-project-structure.

Contexto: projeto /Users/adejaimejunioer/Dev/2026/ai-project-structure. Leia AGENTS.md, docs/SESSION.md (entrada de 2026-08-20 sobre T-002 e T-003), docs/TASKS.md e docs/specs/0001-skill-v2.md antes de comecar. Esta sessao fecha a parte Codex CLI da tarefa T-002.

Regras da sessao (valem para tudo):
- Nunca use o caractere travessao (em dash, U+2014) em nenhum texto.
- Nunca inicialize git, nem nos diretorios de teste.
- Nunca sobrescreva arquivo existente sem me perguntar.
- Trabalhe os testes em diretorios temporarios fora do repo (/tmp/skill-v2-tests-codex/), um subdiretorio limpo por eval.
- A skill instalada esta em ~/.agents/skills/ai-project-structure (fonte canonica em docs/skills/ai-project-structure/). Use a copia instalada, nao a fonte: o objetivo e testar o que esta instalado nesta ferramenta.

TAREFA (T-002): rodar os 7 evals de docs/skills/ai-project-structure/evals/evals.json nesta ferramenta.

Para cada eval, na ordem 1 a 7:
1. Crie um subdiretorio limpo (ex: /tmp/skill-v2-tests-codex/eval-01/). Para os evals 6 e 7, copie antes o fixture indicado no campo "files" (evals/fixtures/v1-project ou evals/fixtures/broken-project) para dentro do subdiretorio e trabalhe sobre a copia, nunca sobre o fixture original. Confira o hash do fixture antes e depois para provar que ficou intacto.
2. Execute o prompt do eval exatamente como esta no JSON, com o diretorio de trabalho no subdiretorio.
3. Compare o que aconteceu com o expected_output do eval. Cheque em especial: perguntas numeradas so quando falta resposta; nada criado antes das respostas no eval 4; marcadores ai-project-structure:core:start v2.0.0 presentes; docs/specs/ so quando pedido; assets/partials/ nunca copiado para o projeto; no eval 6, nada sobrescrito sem confirmacao e secao "Regra Local Do Time" preservada em "Regras Do Projeto"; no eval 7, validador acusando os 2 erros com exit 1.
4. Rode o validador no resultado: python3 ~/.agents/skills/ai-project-structure/scripts/validate_structure.py <subdiretorio>.
5. Registre veredito PASSOU ou FALHOU com a divergencia exata.

Referencia: no Claude Code os 7 evals passaram em 2026-08-20 (7/7), com validador exit 0 nos evals 1 a 6 e exit 1 com os 2 erros esperados no eval 7. Se algum eval falhar aqui, avalie primeiro se e diferenca de comportamento da ferramenta antes de concluir que e defeito da skill.

Se algum eval falhar por defeito da skill (nao do teste), pare, me mostre o problema e proponha a correcao na fonte canonica antes de continuar. Correcao aplicada exige rodar ./install.sh de novo e repetir o eval.

ENCERRAMENTO:
- Atualize docs/TASKS.md. T-002 so vai para Concluidas quando as tres ferramentas (Claude Code, Codex CLI, Gemini CLI) tiverem passado. Claude Code ja passou. Se o Gemini CLI ainda nao tiver rodado, mantenha T-002 em Em Andamento e atualize a nota dizendo quais ferramentas ja passaram.
- Se T-002 fechar (as tres ferramentas aprovadas), complete "Evidencia De Conclusao" da spec 0001-skill-v2 com os comandos executados e o resultado, e mude o Status para Concluida.
- Adicione entrada no docs/SESSION.md com os 7 headings e rode o validador no repo como checagem final. Espere 0 erros; os 4 avisos em entradas de 2026-04-25 sao historicos conhecidos.
- Relatorio final: tabela eval x veredito e o que ficou pendente.
- Me pergunte antes de apagar /tmp/skill-v2-tests-codex/.
```

### Gemini CLI

```text
Contexto: projeto /Users/adejaimejunioer/Dev/2026/ai-project-structure. Leia AGENTS.md, docs/SESSION.md (entrada de 2026-08-20 sobre T-002 e T-003), docs/TASKS.md e docs/specs/0001-skill-v2.md antes de comecar. Esta sessao fecha a parte Gemini CLI da tarefa T-002.

Regras da sessao (valem para tudo):
- Nunca use o caractere travessao (em dash, U+2014) em nenhum texto.
- Nunca inicialize git, nem nos diretorios de teste.
- Nunca sobrescreva arquivo existente sem me perguntar.
- Trabalhe os testes em diretorios temporarios fora do repo (/tmp/skill-v2-tests-gemini/), um subdiretorio limpo por eval.
- A skill instalada esta em ~/.gemini/skills/ai-project-structure (fonte canonica em docs/skills/ai-project-structure/). Use a copia instalada, nao a fonte: o objetivo e testar o que esta instalado nesta ferramenta.

TAREFA (T-002): rodar os 7 evals de docs/skills/ai-project-structure/evals/evals.json nesta ferramenta.

Para cada eval, na ordem 1 a 7:
1. Crie um subdiretorio limpo (ex: /tmp/skill-v2-tests-gemini/eval-01/). Para os evals 6 e 7, copie antes o fixture indicado no campo "files" (evals/fixtures/v1-project ou evals/fixtures/broken-project) para dentro do subdiretorio e trabalhe sobre a copia, nunca sobre o fixture original. Confira o hash do fixture antes e depois para provar que ficou intacto.
2. Execute o prompt do eval exatamente como esta no JSON, com o diretorio de trabalho no subdiretorio.
3. Compare o que aconteceu com o expected_output do eval. Cheque em especial: perguntas numeradas so quando falta resposta; nada criado antes das respostas no eval 4; marcadores ai-project-structure:core:start v2.0.0 presentes; docs/specs/ so quando pedido; assets/partials/ nunca copiado para o projeto; no eval 6, nada sobrescrito sem confirmacao e secao "Regra Local Do Time" preservada em "Regras Do Projeto"; no eval 7, validador acusando os 2 erros com exit 1.
4. Rode o validador no resultado: python3 ~/.gemini/skills/ai-project-structure/scripts/validate_structure.py <subdiretorio>.
5. Registre veredito PASSOU ou FALHOU com a divergencia exata.

Um teste extra vale aqui: a skill deve disparar sozinha, so pela description, sem eu citar o nome dela. Registre se isso aconteceu ou se foi preciso pedir explicitamente.

Referencia: no Claude Code os 7 evals passaram em 2026-08-20 (7/7), com validador exit 0 nos evals 1 a 6 e exit 1 com os 2 erros esperados no eval 7. Se algum eval falhar aqui, avalie primeiro se e diferenca de comportamento da ferramenta antes de concluir que e defeito da skill.

Se algum eval falhar por defeito da skill (nao do teste), pare, me mostre o problema e proponha a correcao na fonte canonica antes de continuar. Correcao aplicada exige rodar ./install.sh de novo e repetir o eval.

ENCERRAMENTO:
- Atualize docs/TASKS.md. T-002 so vai para Concluidas quando as tres ferramentas (Claude Code, Codex CLI, Gemini CLI) tiverem passado. Claude Code ja passou. Se esta for a ultima ferramenta e tudo passou, mova T-002 para Concluidas com a data; senao, atualize a nota dizendo quais ferramentas ja passaram.
- Se T-002 fechar (as tres ferramentas aprovadas), complete "Evidencia De Conclusao" da spec 0001-skill-v2 com os comandos executados e o resultado, e mude o Status para Concluida.
- Adicione entrada no docs/SESSION.md com os 7 headings e rode o validador no repo como checagem final. Espere 0 erros; os 4 avisos em entradas de 2026-04-25 sao historicos conhecidos.
- Relatorio final: tabela eval x veredito e o que ficou pendente.
- Me pergunte antes de apagar /tmp/skill-v2-tests-gemini/.
```

## Desdobrar A Spec 0006 Em Tarefas

Prompt para abrir uma sessao nova cujo objetivo e **planejar** a implementacao da spec 0006 (automacao do consenso): transformar as dez decisoes em tarefas com portao, numa ordem que de para executar pelo loop, sem escrever codigo do produto nesta sessao.

Escrito em 2026-09-04, depois de a spec virar `Definida`. Reaproveitando em versao futura, confira a versao da skill instalada e a lista de tarefas abertas.

```text
Contexto: /Users/adejaimejunioer/Dev/2026/ai-project-structure. Skill `ai-project-structure` 2.10.0, publicada e instalada. Sou o dono do projeto. A spec `docs/specs/0006-automacao-do-consenso.md` esta `Definida`, com DEC-001 a DEC-010, e nao tem nenhuma tarefa de implementacao. Quero que voce a desdobre em tarefas em `docs/TASKS.md`, e me mostre o plano antes de gravar.

Nesta sessao voce NAO escreve codigo do produto, nao cria fixture, nao muda versao. Planeja, registra e para.

## Leia antes de qualquer coisa

1. `AGENTS.md` inteiro. O bloco de loop e o bloco de specs valem para o que voce vai propor.
2. `docs/specs/0006-automacao-do-consenso.md` inteira, com as dez decisoes e os criterios de aceite. Toda tarefa que voce criar aponta para pelo menos um criterio.
3. `docs/SESSION.md`, as quatro entradas mais recentes: sao as rodadas de loop que fecharam T-054 a T-073 e mostram como uma tarefa boa para o loop se parece.
4. `docs/MEMORY.md`, secoes `## Feedback` e `## Project`. Ali estao as regras que ja custaram tempo: portao proprio que falhe antes do trabalho, regex de portao testada contra exemplo, tarefa que exige arquivo proibido ao loop e do agente de chat, custo do Codex.
5. `docs/DECISIONS.md`, as entradas de 2026-09-03 e 2026-09-04.
6. `docs/skills/ai-project-structure/scripts/loop.sh` e `loop_task.py`: e o que ja existe de invocacao de agente; a spec manda reaproveitar o conceito, e o Problema 4 dela explica por que nao da para reaproveitar o script como esta.
7. `docs/skills/ai-project-structure/references/loop.md`, secoes "Perfis" e "Como A Evidencia E Escrita".
8. `docs/archive/CONSENSUS-2026.md`, entradas "P-7 e P-8" e "P-9": as tres posicoes na integra, com o desenho que a DEC-009 ratificou.

## O que ja esta decidido, e voce nao reabre

As dez decisoes da spec. Se uma tarefa parecer exigir mudar uma decisao, registre isso como pergunta em "Aguardando Usuario" e siga planejando o resto. Em especial:

- quem escreve a minuta e um orquestrador mecanico, nunca um agente (DEC-002);
- N e os comandos dos agentes entram na chamada, nao ha catalogo de modelo na skill (DEC-005);
- rodada 1 cega por padrao, rodada 2 recebe as anteriores inteiras (DEC-006);
- diagnosticos novos so para entrada com `**Origem:**`, nivel AVISO (DEC-007);
- bruto e manifesto no repositorio desde o inicio, fora da arvore de execucao, ponte curta na entrada (DEC-008, DEC-009);
- retomada so com palavra humana (DEC-009);
- varredura de segredo que para e pergunta, nunca redige (DEC-010).

## O que quero receber

Um plano em `docs/TASKS.md`, secao "Proximas Tarefas", com estas propriedades:

1. **Cada tarefa cabe numa rodada de loop** de um agente so, com ate 3 tentativas. Tarefa que precisa de mais de uma rodada esta grande demais: divida.
2. **Cada tarefa declara `(verifica: <comando>)`** e o comando e um portao proprio no molde de `docs/skills/ai-project-structure/evals/portao_t0NN.py`: cobra comportamento e texto, nao nome de funcao; falha antes do trabalho e passa depois; inclui `verify_repository.py` quando a tarefa nao toca o bloco core, e nao inclui quando toca (a propagacao para o `AGENTS.md` da raiz e do agente de chat). Voce **escreve os portoes nesta sessao**, porque eles sao a especificacao executavel de cada tarefa; e o unico codigo que nasce aqui. Rode cada um e confirme que falha hoje.
3. **Ordem de execucao explicita**, com dependencia dita na linha ("depende de T-NNN"). Primeiro o que nao depende de decisao nem de outra tarefa. Sugestao de espinha, que voce pode mudar dizendo por que: o primitivo de invocar N agentes isolados e coletar bruto mais manifesto; o lock e a escrita atomica da minuta com os campos de julgamento em branco; a varredura de segredo antes de gravar; o marcador `**Origem:**` e os checks AVISO no validador com fixture; o pacote de debate; o pacote de achado; a rodada 2 com as anteriores inteiras; a retomada por comando; `references/consenso.md` e o bloco gerenciado, se houver; a secao no `SKILL.md` no molde de "Rodar Uma Tarefa Com O Loop".
4. **Cada tarefa diz o que e distribuido e se exige bump**, e qual bump: a release inteira da spec e uma minor (2.11.0). Uma tarefa faz o bump e as outras acrescentam ao CHANGELOG da skill. Marcadores da raiz sao postos pelo agente de chat antes da primeira rodada, e a tarefa diz isso.
5. **Cada tarefa lista o que o agente do loop NAO pode tocar** e o que sobra para o agente de chat: `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `CONSENSUS.md` e specs. Se a tarefa exigir editar um desses, a parte proibida sai da tarefa e vira nota para o agente de chat.
6. **Cada tarefa cita o criterio de aceite da spec** que ela fecha, e a secao "Tarefas" da spec lista todos os T-IDs, sem status (anti-drift).
7. **Uma tarefa de bancada real no fim**: rodar a operacao de verdade, com dois agentes baratos (`gpt-5.6-terra` e o perfil de Grok via `cursor-agent` em `docs/MEMORY.md`), numa pergunta real do projeto, e comparar com a rodada feita na mao em 2026-09-03. E o unico criterio julgado na mao da spec.

Nao invente perfil de modelo: os perfis estao em `docs/MEMORY.md`, secao `## User`, e o custo pedido pelo usuario e `terra` para executar. Nao crie spec nova: e a mesma spec.

## Restricoes que ja custaram tempo aqui

- **Nenhum travessao (U+2014)**, nem nos portoes, nem nas tarefas.
- **Nada de `scripts/` na raiz.** Portao vai em `docs/skills/ai-project-structure/evals/`. Codigo do produto, quando existir, vai em `docs/skills/ai-project-structure/scripts/`.
- Marcador verifica **no fim da linha**, sem parenteses no comando: `(verifica: python3 docs/skills/ai-project-structure/evals/portao_t0NN.py)`.
- `docs/TASKS.md` se edita por substituicao atomica ou por script pequeno; nunca reescreva o arquivo inteiro de cabeca.
- **Nao rode o loop nesta sessao.** Planejar e uma coisa, executar e outra, e a primeira rodada so acontece depois de eu aprovar o plano.
- `docs/SESSION.md` esta perto de 30KB: se a entrada nova estourar, rotacione as mais antigas para `docs/archive/SESSIONS-2026.md` e atualize o indice de la. Nao encurte conteudo.

## Verificacao, ao terminar

```
python3 docs/skills/ai-project-structure/evals/verify_repository.py
python3 docs/skills/ai-project-structure/evals/test_loop.py
python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict
python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --progress
```

Baseline de hoje: 71 de 71, 77 de 77, exit 0 sem erro e sem aviso. Os portoes novos, rodados um a um, precisam **falhar** hoje; portao que passa antes do trabalho nao e portao.

## Pronto quando

1. As tarefas estao em `docs/TASKS.md` com ID, ordem, dependencia, criterio da spec, bump e o que e do agente de chat; a spec lista os T-IDs e passou para `Em andamento` so se eu aprovar, senao continua `Definida`.
2. Cada tarefa tem o portao escrito em `evals/`, rodado, e falhando hoje pelo motivo certo.
3. `docs/SESSION.md` tem a entrada da sessao, e `docs/CHANGELOG.md` a linha.
4. Voce me mostrou o plano numa tabela (tarefa, o que entrega, portao, depende de, bump, parte do agente de chat) e parou. Nao commite: eu commito depois de ler.

Comece me dizendo, em cinco linhas, como voce leu a spec: qual e o primitivo, o que e pacote em cima dele, e onde voce acha que o plano vai errar.
```

## Rodar As Tarefas Pendentes Com Subagentes Sonnet Revisados Por Fable

Prompt para abrir uma sessao nova cujo objetivo e **executar** a fila de tarefas abertas (T-078 a T-084 e T-087 a T-091) com um agente gestor em Fable 5.1 delegando cada tarefa a um subagente em Sonnet 5.5, um por vez, e revisando o que volta com portao, verificador e mutacao antes de fechar.

Escrito em 2026-10-20, com a skill em 2.12.0 publicada, logo depois da analise do ai-memory que abriu T-087 a T-091. Reaproveitando em versao futura, atualize a versao da skill, a lista de tarefas abertas, os pisos das baterias e o alias de modelo dos subagentes, que envelhece rapido.

```text
Contexto: /Users/adejaimejunioer/Dev/2026/ai-project-structure. Skill `ai-project-structure` 2.12.0, publicada e instalada. Sou o dono do projeto.

Voce e o agente gestor desta sessao, rodando em Fable 5.1. Voce nao executa as tarefas: delega cada uma a um subagente em Sonnet 5.5 (ferramenta Agent, `model: sonnet`, tipo general-purpose), revisa o que volta, roda os portoes e registra. So voce escreve em `docs/SESSION.md`, `docs/MEMORY.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/TASKS.md`, `AGENTS.md` da raiz e `docs/specs/`. Subagente nunca commita; voce tambem nao, sem eu pedir.

## Leia antes de qualquer coisa

1. `AGENTS.md` (ordem de leitura para mudanca relevante; secoes "Evidencia De Fechamento", "Passagem De Trabalho" e "Loop").
2. `docs/SESSION.md`, entrada de 2026-10-20 (analise do ai-memory) e a anterior (T-086).
3. `docs/TASKS.md`, secao "Proximas Tarefas": T-078 a T-084 e T-087 a T-091. O texto de cada tarefa e o contrato; nao resuma ao delegar, cole a linha inteira.
4. `docs/MEMORY.md`, secao Feedback inteira: cada regra ali custou uma sessao. As que mais pegam aqui: portao novo so entra depois de voce quebrar de proposito o que ele pega; reverter mutacao de backup por `cp`, nunca `git checkout`; check de prosa exige que toda ocorrencia bata; tarefa apontada para verificador que ja passa nao vale, precisa de portao proprio.
5. `docs/specs/0006-automacao-do-consenso.md` (DEC-003 a DEC-010) e `docs/skills/ai-project-structure/references/loop.md`, secao "A Evidencia Vale O Que O Portao Vale".
6. `docs/skills/ai-project-structure/evals/portao_t086.py` e `portao_consenso_lib.py`: molde dos portoes.

Confira o estado real antes de agir: `git status` limpo, `python3 docs/skills/ai-project-structure/evals/verify_repository.py` em 74/74, `python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict` em 0 erros e 0 avisos. Se algo divergir, pare e me diga.

## O que ja esta decidido, e voce nao reabre

- Versao atual da skill: 2.12.0, publicada. T-078 a T-083 acrescentam item na secao `## 2.12.0` do CHANGELOG da skill, sem bump. O bump para 2.13.0 acontece uma vez so, na fase 3, levando T-084, T-087, T-088, T-089 e T-091.
- ai-memory (akitaonrails) nao entra como codigo nem dependencia (`docs/DECISIONS.md`, 2026-10-20). T-087 a T-091 importam ideias em texto.
- Modelos: subagentes em `sonnet`; revisao e registro em voce (Fable). Confirme com `claude --help` que o alias `sonnet` resolve para Sonnet 5.5 antes do primeiro subagente; se nao, me pergunte. Nunca use nivel que abra delegacao automatica (ver nota sobre `ultra` em `MEMORY.md`).
- Subagente trabalha nesta pasta, nao em worktree, um por vez, para que os portoes e as baterias (`test_consenso.py`, `test_loop.py`) vejam o estado real. Nunca dois subagentes escrevendo ao mesmo tempo: T-079, T-080, T-081 e T-082 tocam o mesmo `scripts/consenso.py` e a mesma bateria, com pisos cumulativos (40, 48, 56).

## Fases e ordem

### Fase 1: spec 0006, sem bump

Ordem: T-078, T-079, T-080, T-081, T-082. Cada uma ja tem portao em `evals/portao_tNNN.py`, que hoje falha pelo motivo certo. Rode o portao antes de delegar e cole a saida da falha na delegacao.

T-083 e tarefa de chat, nao de subagente: roda Codex e `cursor-agent` reais numa pergunta que eu preciso confirmar, e a comparacao de qualidade e `revisao-manual`. Antes dela: rotacionar `docs/CONSENSUS.md` (esta a poucos bytes do teto) e registrar os perfis de consenso em `MEMORY.md` com minha confirmacao. Chegando em T-083, pare e me pergunte a pergunta real da rodada; se eu nao estiver, mova T-083 para "Aguardando Usuario" com `**Pergunta:**` e `(bloqueada: AAAA-MM-DD)` e siga para a fase 3.

### Fase 2: fechar o que a fase 1 deixou

Para cada tarefa aprovada: linha em "Concluidas" com `Evidencia: tipo=comando; procedimento=<portao>; resultado=<saida real, nao resumo>`, item na secao 2.12.0 do CHANGELOG da skill (o subagente escreve esse item; voce confere), `verify_repository.py` e `--strict` verdes. Reinstalar nos tres destinos com `install.sh --sim` e conferir paridade por `cmp`.

### Fase 3: rodada do bump 2.13.0

Ordem: T-084 (timeout do `loop.sh`), T-087 (`@AGENTS.md` nas pontes), T-088 (memoria e evidencia), T-089 (recarga apos compactacao), T-091 (tipo Armadilha). Um bump so: `version` e prosa do `SKILL.md`, marcadores `core`, `specs` e `loop` em v2.13.0 nos assets, nos dois partials e nos tres blocos do `AGENTS.md` da raiz; secao `## 2.13.0` no CHANGELOG da skill com os cinco itens. Se T-083 ficou em "Aguardando Usuario", troque na linha dela "a versao ja e 2.12.0" por 2.13.0, como T-086 fez com T-078 a T-082.

Antes de delegar qualquer tarefa desta fase, escreva voce o portao da rodada no molde de `portao_t086.py` (versao coerente em frontmatter, prosa, marcadores e CHANGELOG; bloco core da raiz byte a byte igual ao dos assets; pontes comecando com `@AGENTS.md`; paragrafos novos presentes nos dois `AGENTS.md`; tipo Armadilha nos dois `MEMORY.md`; raiz em `--strict`; verificador). Rode: tem de falhar hoje. Delegue com a saida.

T-087 pede conferir a grafia do import no Gemini CLI (`@AGENTS.md` ou `@./AGENTS.md`) na documentacao antes de aplicar; o subagente registra na resposta o que conferiu e onde. Se nao conseguir confirmar, aplica so a linha do Claude e me pergunta a do Gemini.

T-088 e T-089 mudam o bloco core: ate 6 linhas e ate 2 linhas, respectivamente. Sem travessao. Bloco core de assets e raiz identicos byte a byte.

### Fase 4: T-090, medicao sem corte

Subagente conta linhas e instrucoes por secao do bloco core de `AGENTS.md` (raiz e template) e aplica a cada linha o teste "remover isto faria o agente errar?", devolvendo uma tabela e uma proposta de quais trechos sairiam para `references/` ou para o cabecalho do arquivo de `docs/` que governam. Voce revisa a proposta, nao executa corte nenhum, e registra em `SESSION.md`. Evidencia `tipo=conferencia`. A decisao de cortar e minha, junto com T-082.

## Como delegar (uma mensagem por tarefa)

Siga o modelo de "Passagem De Trabalho" do `AGENTS.md`, com a linha da tarefa colada inteira:

    Tarefa: <linha inteira de T-NNN em docs/TASKS.md>. Pronta quando: `python3 docs/skills/ai-project-structure/evals/portao_tNNN.py` sai 0 e `python3 docs/skills/ai-project-structure/evals/verify_repository.py` sai 0.
    Estado: feito <o que as tarefas anteriores da rodada ja entregaram>; pendente <esta tarefa>. Saida atual do portao: <colar>.
    Decisoes que valem aqui: <DEC-NNN da spec, ou "versao ja e 2.12.0, item na secao 2.12.0 do CHANGELOG da skill, sem bump" / "bump 2.13.0 ja feito por mim, nao mexa na versao">. Nao repetir: <tentativa anterior do mesmo subagente que falhou, com a saida do portao; "nenhuma" na primeira>.
    Consulte antes de agir: AGENTS.md; docs/MEMORY.md (Feedback); docs/specs/0006-automacao-do-consenso.md; docs/skills/ai-project-structure/SKILL.md; references/loop.md; o portao da tarefa.
    Confira o estado real do projeto (arquivos, testes, git) antes de agir: este resumo pode estar desatualizado.
    Limites: nao edite docs/SESSION.md, docs/MEMORY.md, docs/DECISIONS.md, docs/CONSENSUS.md, docs/TASKS.md, AGENTS.md da raiz nem docs/specs/ (os testes escrevem CONSENSUS.md so em projetos temporarios); nao commite; nao crie __pycache__ (rode python com -B ou limpe); nenhum travessao (U+2014) em arquivo nenhum; nao apague teste, check, secao ou link para o portao passar: se a saida obvia for remover conteudo, pare e me pergunte na sua resposta final. Responda com: feito, pendente, aprendido, arquivos tocados, saida do portao e do verificador.

Ate 3 tentativas por tarefa, como o loop: na segunda e na terceira, continue o mesmo subagente (SendMessage) com a saida da falha em "Nao repetir". Na terceira falha, nao feche a tarefa: registre em `SESSION.md` o que cada tentativa produziu e siga para a proxima.

## Como revisar (voce, Fable, a cada retorno)

1. `git diff --stat` e o diff inteiro. Mudanca fora do escopo da tarefa volta, mesmo que o portao passe.
2. Rode o portao da tarefa, `verify_repository.py`, `validate_structure.py . --strict`, a bateria tocada (`test_consenso.py` ou `test_loop.py`), a busca por travessao (U+2014) nos arquivos tocados e `find . -name __pycache__`.
3. Se a tarefa criou ou alterou check, portao ou fixture: quebre de proposito o que ele deveria pegar, com backup por `cp`, e veja acusar; volte do backup e confira por `cmp`. Registre cada mutacao e o que ela produziu na evidencia.
4. Leia o item de CHANGELOG escrito pelo subagente: versao certa, sem travessao, conta o que mudou e por que.
5. So depois mova a tarefa em `TASKS.md` com a evidencia real.

Reprovou: devolva ao mesmo subagente com o motivo exato e a saida. Voce nao conserta no lugar dele, salvo ajuste de uma linha que voce registre como seu na evidencia.

## Restricoes que ja custaram tempo aqui

- `cursor-agent` e Codex nao entram nesta sessao, salvo em T-083 e com minha confirmacao: a rodada e Claude por assinatura.
- Nunca `git checkout <arquivo>` para desfazer: ha trabalho nao commitado o tempo todo.
- `SESSION.md` passa de 30KB rapido: rotacione para `docs/archive/SESSIONS-2026.md` e atualize o indice quando o validador avisar `ROTACAO`.
- Portao verde nao e prova: e ausencia de objecao. Mutacao e leitura do diff sao parte do fechamento.

## Como registrar, ao fim

- `docs/SESSION.md`: uma entrada da sessao, no modelo do arquivo, com cada tarefa, tentativas, mutacoes e o que ficou aberto; "Aprendizados Para MEMORY.md" so com o que satisfaz o criterio de promocao.
- `docs/TASKS.md`: concluidas com evidencia; bloqueadas em "Aguardando Usuario".
- `docs/CHANGELOG.md` do projeto: uma secao por fase fechada.
- `docs/MEMORY.md`: so se surgiu regra nova com motivo e quando aplicar.
- Specs: `Status` da 0006 e "Evidencia De Conclusao" so se T-083 fechar.
- Me entregue a mensagem de commit sugerida (padrao `feat:`/`fix:`/`docs:`) e espere meu sim.

## Pronto quando

- T-078 a T-082 concluidas com evidencia real e item na 2.12.0 do CHANGELOG da skill.
- T-083 concluida, ou em "Aguardando Usuario" com a pergunta escrita.
- Skill em 2.13.0 com T-084, T-087, T-088, T-089 e T-091, portao da rodada verde, reinstalada nos tres destinos com paridade por `cmp`.
- T-090 com tabela e proposta em `SESSION.md`, sem corte.
- `verify_repository.py` verde (o numero sobe com os checks novos; registre o total), `--strict` 0 e 0, zero travessao, zero `__pycache__`, nada commitado sem meu sim.

Comece me dizendo, em cinco linhas, a ordem que vai seguir, qual portao roda primeiro e onde acha que a rodada vai travar.
```

## Aplicar A Camada GitHub E Abrir A Spec Do Modulo Github

Prompt para abrir uma sessao nova cujo objetivo e **executar** a fase A da decisao de 2026-10-20 (CI, protecao de `main`, tags e releases, arquivos de comunidade em ingles, README em ingles) e abrir a spec 0007 do modulo opcional `github` da skill, sem bump. Gestor em Fable 5.1 delegando a escrita de arquivos a subagentes em Sonnet 5.5; toda acao externa espera o sim do usuario.

Escrito em 2026-10-20, com a skill em 2.12.0 publicada, logo depois da comparacao com o ai-memory que abriu a decisao e T-092 a T-099. Reaproveitando em versao futura, atualize a versao da skill, os SHAs dos commits de bump e a lista de tarefas.

```text
Contexto: /Users/adejaimejunioer/Dev/2026/ai-project-structure. Skill `ai-project-structure` 2.12.0, publicada e instalada. Sou o dono do projeto e do repositorio github.com/adejaimejr/ai-project-structure.

Voce e o agente gestor desta sessao, rodando em Fable 5.1. Objetivo: aplicar a camada GitHub decidida em 2026-10-20 (fase A) e abrir a spec do modulo `github` da skill (fase B, so a spec). Escrita de arquivos vai para subagentes em Sonnet 5.5 (ferramenta Agent, `model: sonnet`, tipo general-purpose), um por vez; toda acao externa (push, PR, merge, tag, release, ruleset, labels) e sua, e cada uma espera meu "sim" explicito, uma a uma.

## Leia antes de qualquer coisa

1. `AGENTS.md`: ordem de leitura para mudanca relevante, "Evidencia De Fechamento", "Passagem De Trabalho" e "Regras Do Projeto" (as seis regras da camada GitHub ja estao la).
2. `docs/DECISIONS.md`, entrada "2026-10-20 - Camada GitHub do repositorio": a decisao inteira, com motivo e impacto. Nao reabra.
3. `docs/SESSION.md`, entrada de 2026-10-20 sobre a camada GitHub: o diagnostico contra o ai-memory e o que ja foi feito.
4. `docs/TASKS.md`, "Proximas Tarefas": T-092 a T-099. A linha de cada tarefa e o contrato; ao delegar, cole a linha inteira.
5. `docs/QUALITY.md`, "Testes E Validacao": os dois portoes e a saida esperada.
6. `docs/skills/ai-project-structure/README.md` (flags do `install.sh`, onde cada ferramenta le a skill) e o `CHANGELOG.md` da skill (formato `## X.Y.Z - AAAA-MM-DD`; a secao 2.12.0 e a fonte das notas da release).
7. `docs/MEMORY.md`, secao Feedback inteira.
8. Se ainda existir: `/Users/adejaimejunioer/.claude/plans/eu-preciso-de-uma-dynamic-lemur.md`, o plano completo com a comparacao e a fase B. O essencial esta aqui e nas tarefas.

Confira o estado real antes de agir: `git status` (mudanca sem commit em `AGENTS.md`, `docs/DECISIONS.md`, `docs/PROJECT_CONTEXT.md`, `docs/ROADMAP.md`, `docs/PROMPTS.md`, `docs/SESSION.md`, `docs/TASKS.md` ou `docs/CHANGELOG.md` e o registro da decisao: me proponha o commit `docs: camada GitHub, decisao, regras e prompt` e espere meu sim antes de qualquer outra coisa), `python3 docs/skills/ai-project-structure/evals/verify_repository.py` em 74/74, `python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict` em 0 erros e 0 avisos.

## O que ja esta feito, e voce nao refaz

- Decisao registrada; "Regras Do Projeto" com as seis regras; `PROJECT_CONTEXT.md` com a excecao de idioma; `ROADMAP.md` atualizado.
- No GitHub: descricao em ingles, nove topics, Wiki e Projects desligados; PR #1 fechado sem merge e a branch `cursor/setup-dev-environment-36f3` apagada (o diagnostico de portabilidade dele esta em T-093).

## O que ja esta decidido, e voce nao reabre

- Ingles so na camada GitHub: `README.md`, `docs/CONTRIBUTING.md`, `docs/SECURITY.md`, `docs/CODE_OF_CONDUCT.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `.github/`, corpo de release. `README.pt-BR.md` e a versao em portugues. `AGENTS.md`, `docs/` e a skill seguem em pt-BR.
- Raiz: so `README.md`, `README.pt-BR.md`, `LICENSE`, `.gitignore`, `.gitattributes` e `.github/`. Comunidade em `docs/`. Nada mais na raiz.
- Travessao (U+2014) proibido em todo `.md`, em ingles inclusive. O verificador acusa.
- Sem bump de versao nesta sessao. A 2.13.0 pertence a outra fila (prompt "Rodar As Tarefas Pendentes Com Subagentes Sonnet Revisados Por Fable"). O modulo `github` da skill e 2.14.0: nesta sessao so a spec 0007, nenhum asset, nenhuma linha em `SKILL.md`.
- Conserto de `scripts/loop.sh` (T-093) e mudanca em arquivo distribuido e pede bump: nesta sessao so `evals/test_loop.py`. Se o CI em Linux ficar vermelho so por `loop.sh`, pare e me pergunte (patch 2.12.1 agora, ou esperar a 2.13.0); nao bumpe sozinho.
- Actions fixadas por SHA completo com a versao em comentario; `permissions: contents: read` (so `release.yml` leva `contents: write`); `concurrency` cancelando rodada anterior do mesmo PR.

## Fases e ordem

### Fase 1: CI e portabilidade (T-092, T-093)

Branch `ci/portoes` a partir de `main`. Subagente escreve `.github/workflows/ci.yml` e conserta `evals/test_loop.py`. Voce roda os dois portoes em macOS, abre o PR (com meu sim) e espera o CI nos dois SOs. Verde: merge (com meu sim). Vermelho em Linux: leia o log, devolva ao subagente com a saida; se a causa for `loop.sh`, vale a regra acima.

### Fase 2: protecao e releases (T-094, T-095)

Ruleset em `main` pela API (`gh api -X POST repos/adejaimejr/ai-project-structure/rulesets`): bloquear force push e delecao, exigir o check `ci`; sem review obrigatorio. Depois a tag `v2.12.0` em `7b8bbd7`, as tags retroativas e a Release 2.12.0 manual. Me mostre o comando de cada tag antes de rodar; a tag e anotada e leva `GIT_COMMITTER_DATE` igual a data do commit.

### Fase 3: comunidade, release automatizada e README (T-096, T-097, T-098)

Um subagente por tarefa, nesta ordem, numa branch `github/camada` e um PR so, para o CI rodar. T-098 por ultimo, porque os badges apontam para o workflow `ci`, a Release e o `LICENSE`.

### Fase 4: spec 0007 (T-099)

Voce escreve a spec, no modelo de `docs/specs/README.md`, em `Rascunho`, com as perguntas abertas listadas na tarefa. Nao responda as perguntas por inferencia; e so entao acrescente `(spec: 0007-modulo-github)` na linha de T-099, porque o validador exige que a spec exista.

## Como delegar (uma mensagem por tarefa)

Modelo de "Passagem De Trabalho" do `AGENTS.md`, com a linha da tarefa colada inteira:

    Tarefa: <linha inteira de T-NNN em docs/TASKS.md>. Pronta quando: <o comando de verifica da tarefa, ou a leitura que eu vou fazer>.
    Estado: feito <o que as tarefas anteriores ja entregaram>; pendente <esta tarefa>.
    Decisoes que valem aqui: docs/DECISIONS.md, entrada "Camada GitHub do repositorio" de 2026-10-20; ingles na camada GitHub; sem travessao; sem bump; raiz minima com .github/ e comunidade em docs/. Nao repetir: <tentativa anterior que falhou e por que, ou "nenhuma">.
    Consulte antes de agir: AGENTS.md (Regras Do Projeto); docs/QUALITY.md; docs/skills/ai-project-structure/README.md; <arquivos da tarefa>.
    Confira o estado real do projeto (arquivos, testes, git) antes de agir: este resumo pode estar desatualizado.
    Limites: toque so os arquivos da tarefa; nao edite docs/SESSION.md, docs/MEMORY.md, docs/DECISIONS.md, docs/TASKS.md, AGENTS.md nem nada em docs/skills/ fora do que a tarefa nomeia; nao commite; nao rode git push, gh nem tag; nao crie __pycache__.

Ate 3 tentativas por tarefa: na segunda e na terceira, continue o mesmo subagente (SendMessage) com a saida da falha em "Nao repetir". Na terceira falha, registre em `SESSION.md` o que cada tentativa produziu e siga.

## Como revisar (voce, Fable, a cada retorno)

1. `git diff --stat` e o diff inteiro. Arquivo fora da tarefa volta.
2. `verify_repository.py`, `validate_structure.py . --strict`, e `grep -rn $'\xe2\x80\x94' <arquivos tocados>` vazio, incluindo `.github/` e `README.md`.
3. YAML de workflow: `actionlint` se existir na maquina; senao o proprio GitHub valida no push da branch (`gh run list` mostra a falha de sintaxe). Confira que cada `uses:` tem SHA de 40 caracteres e comentario `# vX.Y.Z`, resolvido por `gh api repos/<owner>/<action>/git/ref/tags/<tag>`.
4. Texto em ingles: leia inteiro; frase que nao soa natural volta. Sem email pessoal, sem segredo; o unico contato e o link do Private Security Advisory.
5. So depois mova a tarefa em `TASKS.md` com a evidencia real (saida do comando, nao resumo).

## Restricoes que ja custaram tempo aqui

- Nunca `git checkout <arquivo>` para desfazer: ha trabalho nao commitado o tempo todo. Reverta por backup com `cp`.
- `(verifica:)` nao aceita parenteses no comando.
- `SESSION.md` passa de 30KB rapido: rotacione para `docs/archive/SESSIONS-2026.md` e atualize o indice quando o validador avisar `ROTACAO`.
- O verificador compara a instalacao real da skill com a fonte: nada desta sessao toca `docs/skills/ai-project-structure/` fora de `evals/`, entao ele continua em 74/74; se cair, alguem mexeu onde nao devia.
- Tag errada no GitHub e lixo publico: confira `git show <sha>` de cada commit de bump antes de criar a tag.

## Como registrar, ao fim

- `docs/SESSION.md`: uma entrada, no modelo do arquivo, com cada tarefa, tentativas, o que ficou aberto e os links de PR, release e workflow.
- `docs/TASKS.md`: concluidas com evidencia; o que depender de mim em "Aguardando Usuario" com a pergunta escrita.
- `docs/CHANGELOG.md` do projeto: uma secao por fase fechada.
- `docs/PROJECT_CONTEXT.md`, "Links Internos": linha para `CONTRIBUTING.md` quando ele existir. `docs/QUALITY.md`, checklist da estrutura: a linha da raiz passa a citar as excecoes.
- `docs/MEMORY.md`: so se surgiu regra nova com motivo e quando aplicar.
- Me entregue a mensagem de commit sugerida de cada PR (padrao `feat:`/`fix:`/`docs:`) e espere meu sim.

## Pronto quando

- `ci` verde em `ubuntu-latest` e `macos-latest` no `main`.
- Ruleset ativo em `main`; `gh release list` mostra `v2.12.0` e `git tag -l` mostra v2.4.0 a v2.12.0.
- `gh api repos/adejaimejr/ai-project-structure/community/profile --jq .health_percentage` em 100.
- `README.md` em ingles com badges funcionando e `README.pt-BR.md` linkado na primeira linha.
- `release.yml` no `main`, pronto para a tag da 2.13.0.
- Spec 0007 em `Rascunho` com as perguntas abertas.
- Verificador 74/74, `--strict` 0 e 0, zero travessao, nada commitado, pushado, tagueado ou publicado sem meu sim.

Comece me dizendo, em cinco linhas, a ordem que vai seguir, o que vai me pedir "sim" primeiro e onde acha que vai travar.
```

## Planejar O Adaptador Cloudroom Para Consenso E Loop (Subagentes Visiveis)

Prompt para abrir uma sessao nova de **planejamento** (spec, nao execucao) de um recurso: quando a skill roda dentro do Cloudroom, `consenso.py` e `loop.sh` poderem usar um subagente do Cloudroom (`room-cli thread spawn`) como agente, em vez de uma CLI invocada direto, sem mudar o contrato dos dois scripts.

Escrito em 2026-10-21, logo depois da bancada real de T-083, em que o usuario estranhou nao ver o agente na barra do Cloudroom: o `consenso.py` chamou `codex exec` como processo, invisivel na interface, e o sandbox read-only do Codex nem rodava no container. Reaproveitando em versao futura, atualize a versao da skill, os nomes de modelo e a sintaxe do `room-cli`, que envelhecem rapido.

```text
Contexto: /Users/adejaimejunioer/Dev/2026/ai-project-structure. Skill `ai-project-structure` 2.13.0, publicada. Sou o dono do projeto. Esta sessao PLANEJA; nao implementa.

## O problema

Em 2026-10-21 a bancada real do consenso (T-083) rodou dentro do Cloudroom. O `consenso.py` invocou `codex exec` direto, como processo filho: nada apareceu na barra de threads do Cloudroom, o sandbox read-only do Codex (bubblewrap) nao rodou no container, e os dois participantes cairam na varredura de segredo porque o log do Codex listou o codigo da propria regex (ver `docs/SESSION.md`, entrada de 2026-10-21, e a Armadilha em `docs/MEMORY.md`). Os subagentes Sonnet das outras tarefas, abertos por `room-cli thread spawn --shared-sandbox`, ficaram visiveis, com log, estado e custo pela assinatura do Claude.

Pergunta a responder: quando a skill roda no Cloudroom, `consenso.py` e `loop.sh` devem poder usar um subagente do Cloudroom como agente? Minha hipotese: sim, mas como ADAPTADOR, nao como reescrita. Os dois scripts recebem `--agente "COMANDO"` e anexam o prompt como ultimo argumento (DEC-005 da spec 0006: o comando vem da chamada, a skill nao tem catalogo de modelo). Um wrapper que se comporte como CLI headless (recebe o prompt como ultimo argumento, imprime a resposta no stdout, sai com o exit code do agente) encaixa nos dois sem tocar neles. Confirme ou derrube a hipotese lendo o codigo antes de propor.

## Leia antes de qualquer coisa

1. `AGENTS.md` (secoes "Passagem De Trabalho", "Consenso Entre Modelos", "Loop").
2. `docs/SESSION.md`, entrada de 2026-10-21 (as duas rodadas de T-083 e o que falhou no container).
3. `docs/MEMORY.md`: secao User (perfis de loop e de consenso), Feedback (portabilidade nos tres sistemas; portao de bancada real exige comando executado), Armadilha (sandbox read-only do Codex).
4. `docs/specs/0006-automacao-do-consenso.md`, DEC-001 a DEC-010, em especial DEC-003 (o que se isola sao as posicoes contemporaneas, por copia separada por participante, nunca por cegueira no prompt), DEC-005 (comando do agente vem da chamada) e DEC-010 (segredo).
5. `docs/skills/ai-project-structure/scripts/consenso.py` (como monta a copia, o prompt e le stdout e stderr), `scripts/loop.sh` (linhas em que chama o agente, o `--tempo-maximo` e a deteccao de "mexeu em arquivo") e `references/consenso.md` e `references/loop.md`.
6. A skill `room-cli` instalada na maquina (`~/.claude/skills/room-cli/SKILL.md`): `room-cli thread spawn --provider ... --model ... [--shared-sandbox] --prompt-file`, `room-cli thread output CHILD_ID`, `room-cli thread list`, `room-cli thread archive`. Confira na propria CLI o que existe hoje; nao confie no que esta escrito aqui.

Confira o estado real antes de agir: `git status` limpo, `python3 docs/skills/ai-project-structure/evals/verify_repository.py` em 78/78, `python3 docs/skills/ai-project-structure/scripts/validate_structure.py . --strict` em 0 erros e 0 avisos. Se divergir, pare e me diga.

## O que ja esta decidido, e voce nao reabre

- `consenso.py` e `loop.sh` continuam agnosticos de ferramenta: nenhum deles importa, detecta ou chama `room-cli` por dentro. O que entra e um comando a mais no catalogo de perfis do usuario em `docs/MEMORY.md`, apontando para o wrapper.
- O isolamento do consenso continua sendo a copia por participante (DEC-003). Se o subagente do Cloudroom precisa rodar na copia, o wrapper tem de garantir isso (diretorio de trabalho, ou o caminho da copia no prompt, ja presente hoje) e a spec tem de dizer como se verifica, nao so afirmar.
- O wrapper e distribuido pela skill (vai em `scripts/`), entao roda em Linux, macOS e Windows (Git Bash): bash puro ou python3 da biblioteca padrao; sem `sed -i`, `perl`, `timeout(1)`, `setsid`.
- Sem `room-cli` no PATH, o wrapper sai com erro claro e codigo diferente de zero antes de qualquer coisa; `loop.sh` entao cai no exit 4 e `consenso.py` registra falha do participante. Nada "degrada" para outra ferramenta em silencio.
- Custo e modelo continuam sendo do usuario: o wrapper recebe provider e modelo por flag, nunca por padrao embutido.

## Perguntas que a spec precisa responder, com leitura de codigo e da CLI

- P-1: `room-cli thread spawn` e assincrono (o pai e avisado quando o filho termina). Como o wrapper bloqueia ate o fim e recupera a resposta integral? (`room-cli thread output CHILD_ID` com polling, `--all`, limites de tamanho, o que acontece se o filho pergunta em vez de responder.)
- P-2: `--shared-sandbox` roda "nesta sandbox e pasta". Qual pasta? Da para apontar o filho para a copia temporaria do consenso? Se nao, o isolamento por copia da DEC-003 sobrevive so pelo prompt, e isso a spec 0006 ja rejeitou. Diga o que e verificavel.
- P-3: filho sem `--shared-sandbox` ganha sandbox propria com copia do codigo (commits e nao commitados). Isso serve ao consenso (isolamento ainda melhor) ou atrapalha (a copia do filho inclui `docs/CONSENSUS.md` inteiro e `docs/consensus/`, que a rodada 1 cega retem)? Em qual dos dois modos cada pacote (debate, achado, loop) deve rodar?
- P-4: `loop.sh` decide se o agente "mexeu em arquivo" por `find -newer` no projeto e mata o agente por grupo de processos no `--tempo-maximo`. Com o trabalho acontecendo em outra sandbox, ou em outro processo que o wrapper so observa, os dois mecanismos ainda valem? O que o wrapper precisa fazer no SIGTERM (`room-cli thread stop`)?
- P-5: o que fica registrado no manifesto do consenso quando o participante e um filho do Cloudroom: id da thread, provider, modelo, link? O bruto continua sendo o stdout do wrapper? E a varredura de segredo le o que?
- P-6: visibilidade e limpeza: titulo da thread filha (tarefa ou pergunta), arquivar ao fim ou deixar para o usuario, e quantas threads uma rodada de N agentes abre.
- P-7: vale para thread Local (Mac) tambem, ou so Cloud? No Mac, `room-cli thread spawn` sem `--machine cloud` abre filho local; com, abre na nuvem a partir do GitHub (exige push). O wrapper precisa saber onde esta?
- P-8: evidencia: qual portao prova que o wrapper funciona sem gastar modelo (agente falso por tras do `room-cli`? mock do `room-cli` no PATH do teste?) e qual bancada real, com um modelo barato, fecha a spec.

## Pronto quando

1. Spec nova em `docs/specs/NNNN-slug.md` no modelo de `docs/specs/README.md`, `Status: Rascunho` ou `Definida` (eu decido), com problema, escopo e fora de escopo, criterios de aceite verificaveis, as decisoes DEC-NNN que voce propoe para P-1 a P-8 (com a alternativa rejeitada e o motivo), perguntas que continuam abertas e o plano de tarefas.
2. Tarefas em `docs/TASKS.md` com ID, ordem, dependencia, criterio da spec, bump (e `scripts/`, entao exige bump) e o que e do agente de chat; cada uma com `(verifica: python3 docs/skills/ai-project-structure/evals/portao_tNNN.py)` e o portao escrito em `evals/`, rodado, e falhando hoje pelo motivo certo. Portao que passa antes do trabalho nao e portao.
3. Uma rodada de consenso sobre P-2 e P-3 (sao as que mexem na DEC-003), com `consenso.py debate` e dois perfis de `docs/MEMORY.md` que eu confirmar; se estiver no Cloudroom, lembre que o Codex read-only nao roda la (Armadilha) e me pergunte o modo antes.
4. `docs/SESSION.md` com a entrada da sessao e `docs/CHANGELOG.md` com a linha. Nao commite: eu commito depois de ler.
5. Voce me mostrou o plano numa tabela (tarefa, o que entrega, portao, depende de, bump, parte do agente de chat) e parou.

Comece me dizendo, em cinco linhas, como voce leu o problema: o que e o wrapper, o que ele nao pode tocar, e onde voce acha que o plano vai errar.
```
