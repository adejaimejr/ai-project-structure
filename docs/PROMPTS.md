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

