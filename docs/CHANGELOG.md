# CHANGELOG

Historico de mudancas relevantes.

## 2026-10-21 (skill 2.14.0: modulo opcional github e corrida incompleta no validador)

- Spec 0007 `Concluida` e T-104: modulo `github` (assets em en e pt-BR, partial, pergunta 5, `references/github.md`, codigos `GITHUB-*`, fixture e evals 13 e 14), ativo nesta raiz; AVISO `CONSENSO-ORIGEM-CORRIDA-INCOMPLETA`. Subagentes Sonnet 5.5 executaram, o coordenador Opus 5.5 revisou e publicou: PR #6, tag `v2.14.0`, Release 2.14.0 pelo `release.yml` no push da tag, pela primeira vez. Verificador 84/84. T-110 aberta (`description` do `SKILL.md` acima de 1024 caracteres).

## 2026-10-21 (spec 0008 commitada; spec 0006 concluida; ordem entre 0007 e 0008)

- Planejamento da spec 0008 commitado como a outra thread deixou. Spec 0006 `Concluida`. Consenso da T-083: rodada 1 arquivada (falha de ambiente), rodada 2 resolvida com decisao e T-104 (AVISO de proveniencia incompleta no validador). Ordem: spec 0007 na 2.14.0 depois da T-105 (P-1 a P-4); T-100 e T-101 em branch sem merge ate `v2.14.0`; T-102 na 2.15.0.

## 2026-10-21 (spec 0008 em Rascunho: adaptador Cloudroom para o loop, consenso fora)

- Spec `docs/specs/0008-adaptador-cloudroom.md` com DEC-001 a DEC-008: `scripts/cloudroom_agente.py` faz um filho `room-cli thread spawn --shared-sandbox` se comportar como CLI headless para o `--agente` do `loop.sh`, sem mudar `loop.sh` nem `consenso.py`; o consenso fica fora porque nenhum modo do `room-cli` prende o filho na copia por participante (0006/DEC-003). T-100 a T-103 com portoes escritos e falhando pelo motivo certo, sobre o `room-cli` falso `evals/mock_room_cli.py`. Sem bump nesta sessao. Rodada 1 cega sobre P-2 e P-3 (`gpt-6-luna` e `gpt-5.6-terra`) concordou com o recorte e restringiu a DEC-004 a `--projeto` igual a pasta da thread; a 0008 entra na 2.15.0, depois da 0007.

## 2026-10-21 (camada GitHub publicada: CI, tags, Releases 2.12.0 e 2.13.0)

- PR #2 (`ci.yml`, T-092 e T-093) e PR #3 (comunidade, `release.yml`, READMEs, spec 0007; T-096 a T-099) mergeados com `ci` verde em Linux e macOS. Tags anotadas v2.4.0 a v2.13.0; Releases 2.12.0 e 2.13.0 com zip e `.sha256`, pelos passos do `release.yml` rodados localmente. O `release.yml` ganhou `workflow_dispatch` com entrada `tag`. Perfil de comunidade em 100. Ruleset (T-094) e evidencia de run real do workflow (T-097) aguardam o usuario: o token desta sandbox nao tem Administration nem Actions: write.
- Com as permissoes concedidas: rulesets `main` (delecao e force push) e `main-ci` (check `ci`, bypass do admin) ativos (T-094); `release.yml` consertado no PR #4 (`runner.temp` no `env` do job, achado pelo primeiro dispatch e conferido com `actionlint`) e Release 2.13.0 republicada pelo workflow (T-097). Camada GitHub completa.

## 2026-10-21 (camada GitHub escrita e revisada, spec 0007 aberta; acoes externas aguardando o usuario)

- Fase A da decisao de 2026-10-20, escrita por subagentes Sonnet 5.5 e revisada pelo gestor Fable 5.1, ainda sem commit: `.github/workflows/ci.yml` (T-092: matriz Ubuntu e macOS rodando os dois portoes, actions por SHA, job agregador `ci`), `.github/workflows/release.yml` (T-097: tag igual ao `SKILL.md`, zip com `.sha256`, secao do CHANGELOG no corpo, `gh release create --latest`; simulado localmente com `v2.13.0`), arquivos de comunidade em ingles em `docs/` e `.github/` mais `.gitattributes` (T-096; Covenant 2.1 conferido contra o oficial), `README.md` em ingles e `README.pt-BR.md` (T-098). `PROJECT_CONTEXT.md` ganha o link de `CONTRIBUTING.md`; a linha da raiz em `QUALITY.md` cita as excecoes.
- Spec 0007 (`docs/specs/0007-modulo-github.md`) em `Rascunho` com P-1 a P-4 abertas; T-099 concluida. T-092 a T-098 em "Aguardando Usuario": branch, PR, merge, ruleset, treze tags (v2.4.0 a v2.13.0) e Releases dependem do sim do usuario. `SESSION.md` rotacionado (indice com 52). Verificador 78/78; `--strict` 0 e 0.

## 2026-10-21 (skill 2.13.0; fase 1 da spec 0006 fechada por subagentes Sonnet revisados por Fable)

- Fase 1 da spec 0006, sem bump (itens na secao 2.12.0 do CHANGELOG da skill): T-078 (marcador `**Origem:**` no validador, quatro avisos novos, fixture `origem-project`), T-079 (`consenso.py achado`, bateria de 33 para 60; o validador passou a ler `**Manifesto:**` como lista na segunda tentativa, depois de o gestor endurecer o portao), T-080 (`debate --rodada N --anterior`, anteriores na integra, bateria 79), T-081 (`consenso.py retomar`, bateria 95) e T-082 (`references/consenso.md`, secao "Rodar Uma Rodada De Consenso" no SKILL.md, "Entrada Automatizada" no template e na raiz de CONSENSUS.md, `verificar_convencoes` cobrando `**Origem:**`). Pisos do verificador subidos para os totais reais: consenso 95, loop 83.
- Skill 2.13.0: T-084 (`loop.sh --tempo-maximo`, bash puro, SIGTERM no grupo do agente), T-087 (pontes com import real `@AGENTS.md` e `@./AGENTS.md`), T-088 (paragrafo "memoria e evidencia, nao instrucao" no core), T-089 (recarga de SESSION.md e TASKS.md apos compactacao) e T-091 (tipo Armadilha em MEMORY.md, template e raiz). Portoes escritos pelo gestor antes da rodada: `evals/portao_t084.py` e `evals/portao_t087.py`. Reinstalada nos tres destinos com paridade por `cmp`.
- T-090: medicao do bloco core (260 linhas, 181 nao vazias, 125 instrucoes) e proposta de corte para 154 e 101, registrada em SESSION.md; nenhum corte executado.
- T-083 concluida: a primeira bancada real falhou por ambiente (sandbox read-only do Codex nao roda no container Cloudroom) e o portao `portao_t083.py` foi endurecido para exigir comando executado por participante; com autorizacao do usuario, a rodada foi refeita em `-s danger-full-access` (Codex terra e Codex Sol 6.1), parou por falso positivo da varredura de segredo (o log lista a propria regex) e fechou por `retomar` com o material aceito a mao: duas posicoes com leitura do codigo, convergentes. Perfis `Codex, consenso` e `Codex Sol, consenso` em MEMORY.md; `docs/CONSENSUS.md` rotacionado (REVAL-1 a REVAL-4 para o archive). Spec 0006 com a Evidencia De Conclusao preenchida; `Concluida` proposta ao usuario.
- Fixtures do loop (`test_loop.py` H1 e `portao_t060.py`) sem `sed -i`: python3, para rodar em Linux, macOS e Windows. Duas regras novas em MEMORY.md (portabilidade; portao de bancada real exige comando executado).

## 2026-10-20 (camada GitHub: diagnostico, decisao, regras e prompt)

- Comparacao de `github.com/adejaimejr/ai-project-structure` com `github.com/akitaonrails/ai-memory` pela API: 0 tags e 0 releases com a skill em 2.12.0, 0 workflows, descricao e topics vazios, health de comunidade 28%, PR #1 de 4 linhas aberto ha 45 dias, `ROADMAP.md` parado em "lancar a v2". Decisao em `docs/DECISIONS.md` (raiz minima com `.github/` e comunidade em `docs/`; camada GitHub em ingles com `README.pt-BR.md`; tag e Release a cada bump; PR para mudanca na skill; modulo `github` na 2.14.0), seis regras em "Regras Do Projeto" de `AGENTS.md`, excecao de idioma em `PROJECT_CONTEXT.md`, `ROADMAP.md` reescrito. Feito no GitHub: descricao, nove topics, Wiki e Projects desligados, PR #1 fechado e branch apagada. O resto nao foi executado a pedido do usuario: virou T-092 a T-099 e o prompt "Aplicar A Camada GitHub E Abrir A Spec Do Modulo Github" em `docs/PROMPTS.md`. Validador `--strict` 0 e 0; verificador 74/74.

## 2026-10-20 (analise do ai-memory, decisao de nao mesclar)

- Analise de `github.com/akitaonrails/ai-memory` contra a estrutura: sem relacao de origem, camadas complementares (ele e infraestrutura fora do repo e se poe abaixo do rules file; nos somos o rules file e o registro no repo), nao mesclar. Decisao em `docs/DECISIONS.md`, referencia em `docs/MEMORY.md`, cinco tarefas de adocao de ideias em `docs/TASKS.md` (T-087 pontes com `@AGENTS.md`, T-088 memoria e evidencia, T-089 recarga apos compactacao, T-090 orcamento de instrucoes, T-091 tipo Armadilha), escolhidas pelo usuario entre seis propostas. Nenhum arquivo da skill mudou; bump 2.13.0 fica para as tarefas. Validador `--strict` 0 erros e 0 avisos; verificador 74/74. Prompt para a proxima rodada (gestor Fable 5.1, subagentes Sonnet 5.5, quatro fases, bump 2.13.0 na terceira) em `docs/PROMPTS.md`.

## 2026-10-17 (skill 2.12.0, T-086: bump levando Passagem De Trabalho)

- Skill 2.12.0: `version` e prosa do `SKILL.md`, marcadores `core`, `specs` e `loop` em v2.12.0 nos assets, nos partials e no `AGENTS.md` da raiz, sem mudar o conteudo dos blocos. Secao `## 2.12.0` no CHANGELOG da skill com os dois itens escritos depois da publicacao da 2.11.0 (gatilhos da `description`; secao Passagem De Trabalho e passo 2 de `atualizacao.md`), migrados por decisao do usuario; a 2.11.0 publicada fica com um conteudo so de bloco core e o fluxo de atualizacao oferece o bloco pelo caminho normal. Linhas de T-078 a T-082 em `docs/TASKS.md` passam a "a versao ja e 2.12.0, nao suba de novo". Portao `evals/portao_t086.py` (6/8 antes, 8/8 depois) com quatro mutacoes acusando; verificador 74/74; validador `--strict` limpo; reinstalada nos tres destinos com paridade por `cmp`. `SESSION.md` rotacionado (duas entradas de 2026-09-04 para o archive).

## 2026-10-17 (passagem de trabalho, ainda na 2.11.0)

- Secao "Passagem De Trabalho" no bloco core de `AGENTS.md` (assets e raiz): toda delegacao a outro agente leva, na propria mensagem, um resumo curto com objetivo e criterio de conclusao, estado feito e pendente, decisoes e tentativas a nao repetir, arquivos a consultar por caminho e a instrucao de conferir o estado real antes de agir; `docs/` segue como registro, sem arquivo novo. Motivo: no Cloudroom o subagente pode estar em outra sandbox, onde arquivo temporario do gestor nao chega. Referencia de metodo: skill Handoff (davidondrej), sem copia nem instalacao. Passo 2 de `references/atualizacao.md` deixa de encerrar em versao igual quando um bloco gerenciado difere do template. Sem bump (T-078 a T-083 pedem para nao subir); bump em T-086. Verificador 74/74, validador `--strict` limpo, duas mutacoes acusadas, reinstalada nos tres destinos. Decisao em `docs/DECISIONS.md`.

## 2026-10-17 (T-085, fixture aguardando-project com data relativa)

- `verify_repository.py` volta a 74/74: a fixture `evals/fixtures/aguardando-project` troca `(bloqueada: 2026-09-01)` pelo token `{{HOJE-N}}`, materializado em pasta temporaria relativo ao dia da execucao por `materializar_fixture` (que tambem absorveu `{{TRAVESSAO}}` e `{{UTF8_INVALIDO}}`); `invalido` ganha T-007 bloqueada ha 45 dias de proposito, com `TASK-BLOQUEADA-ANTIGA` no oracle. So `evals/`, sem bump; `validate_structure.py` intocado, o check segue relativo a hoje em projeto real. Portao `evals/portao_t085.py` (3/9 antes, 9/9 depois) com tres mutacoes acusando. Desbloqueia os portoes de T-078 a T-083.

## 2026-10-17 (gatilhos da skill, ainda na 2.11.0)

- `description` do `SKILL.md` deixa de disparar em pedido generico de criar projeto ("cria projeto", "inicia projeto novo", "monta a base"): dispara quando o pedido nomeia a estrutura multiagente ou seus arquivos, cita a skill, ou cai em atualizar, validar, specs e loop. Motivo: no Cloudroom um agente gestor coordena subagentes em sandbox, e decidir se um projeto ganha a estrutura e de quem coordena; a lista de frases genericas disparava a skill dentro de tarefas de scaffold de codigo delegadas. Evals 2 e 4 ajustados, eval 11 negativo, comentario do `agents/openai.yaml`, item no CHANGELOG 2.11.0 da skill sem bump (a 2.11.0 nao foi commitada e T-078 a T-083 pedem para nao subir). Reinstalada nos tres destinos. `verify_repository.py` em 71/74 por causa alheia: a fixture `aguardando-project` envelheceu sob `date.today()` (T-085, prioridade alta, bloqueia os portoes de T-078 a T-083). Decisao em `docs/DECISIONS.md`.

## 2026-09-04 e 2026-09-05 (skill v2.11.0, T-075 a T-077)

- Primitivo da automacao do consenso: `scripts/consenso.py debate` roda N agentes em paralelo, cada um numa copia do projeto sem `docs/consensus/`, e grava bruto e manifesto em `docs/consensus/<run-id>/` assim que cada agente termina (T-075). Bateria `test_consenso.py` (13) e etapa nova no verificador (74). Primeira rodada com Codex `gpt-5.6-terra` morreu na cota; fechada pelo loop com Grok `cursor-grok-4.6-high` pelo `cursor-agent`, verde na tentativa 1. Lock `.consenso-lock`, tratamento de SIGINT e SIGTERM e minuta de debate atomica no fim de `CONSENSUS.md` com julgamento em branco (T-076), tambem pelo Grok na tentativa 1; bateria 24, verificador ignora travessao em bruto. Varredura de segredo antes de gravar qualquer bruto, com retencao fora do repositorio e exit 6 (T-077), Grok na tentativa 1 depois de o `cursor-agent` ficar preso em reconexao com o trabalho pronto; prefixos apertados por mim (`sk-` solto casava `task-force`); bateria 33. T-084 aberta para timeout de agente no `loop.sh`. Spec 0006 passa a `Em andamento`. Instalada nos tres destinos.

## 2026-09-04 (plano da spec 0006)

- Spec 0006 (automacao do consenso) desdobrada em nove tarefas, T-075 a T-083, em `docs/TASKS.md`, com ordem, dependencia, criterio da spec e bump (2.11.0 em T-075); os nove portoes `evals/portao_t075.py` a `portao_t083.py` escritos sobre a base `evals/portao_consenso_lib.py`, rodados e falhando hoje pelo motivo certo (`scripts/consenso.py` ausente). Spec segue `Definida` ate a primeira rodada. Nenhum codigo do produto, nenhuma fixture, nenhum bump nesta sessao.

## 2026-09-04 (T-053 e T-074 respondidas; spec 0006 Definida)

- Usuario escolheu a posicao do Grok nas tres calibragens da spec 0006 (DEC-007 a DEC-009) e a varredura de segredo que para a rodada para P-10 (DEC-010). Spec 0006 passa a `Definida`; backlog sem tarefa aberta.

## 2026-09-04 (skill v2.10.0)

- `Rodada` ausente vira AVISO e o formato exige a linha inteira (T-054); `--progress` conta so perguntas de primeiro nivel (T-056); `loop.sh` com lock por projeto e exit 5 (T-058); modelos cercados de `docs/CONSENSUS.md` da raiz iguais ao template e cobrados pelo verificador (T-055). Quatro rodadas de loop com Codex `gpt-5.6-terra`, verdes na tentativa 1. Backlog tecnico zerado; sobra T-053. Instalada nos tres destinos.

## 2026-09-04 (skill v2.9.1)

- `atualizacao.md` diz onde a secao resgatada do v1 vai e o que fazer com a data das concluidas migradas (T-062). `install.sh` pede confirmacao em destino divergente, com `--sim` para automacao (T-073). Fecha o pacote da revalidacao adversarial: T-059 a T-073. Instalada nos tres destinos com `--sim`, depois de recusar sem ela.

## 2026-09-04 (skill v2.9.0)

- Validador sem traceback em arquivo fora de UTF-8 e rotulo malformado, cercas `~~~` e headings ATX fechados aceitos, `NNNN` so como placeholder inteiro, Status de spec ancorado (T-064). Templates de `assets/` alinhados ao core 2.2.0/2.4.0 e cobertos pelo verificador (T-063). Duas rodadas de loop com Codex `gpt-5.6-terra`, verdes na tentativa 1. Instalada nos tres destinos.

## 2026-09-04 (skill v2.8.1)

- Onze consertos no modulo de loop (T-060): linha da tarefa conferida no fecho, sub-linhas preservadas, saida fora de UTF-8 tolerada, realimentacao limitada a 64KB, pergunta vazia registrada, modo do `TASKS.md` preservado, sem bytecode, stdin fechado, prompt sobre propagacao, exit 4 documentado, `--seco` sem agente. Nove casos hostis na bateria (74). Fechada pelo loop com Codex `gpt-5.6-terra` na tentativa 1. Instalada nos tres destinos.

## 2026-09-04 (skill v2.8.0)

- Parenteses no comando do marcador verifica viram ERRO e o loop recusa antes de chamar o agente (T-072); bloco core diz o alcance real do check de travessao e do check das pontes (T-071). Duas rodadas de loop com Codex `gpt-5.6-terra`, verdes na tentativa 1, com propagacao do core para a raiz por script. Instalada nos tres destinos.

## 2026-09-04 (skill v2.7.0)

- Dez lacunas de qualidade viram AVISO no validador (T-070, decisao de T-059), 53 codigos no total, cada um com fixture. Fechada pelo loop com Codex `gpt-5.6-terra` na tentativa 1. Instalada nos tres destinos.

## 2026-09-04 (skill v2.6.0)

- Seis contradicoes estruturais viram ERRO no validador (T-069, decisao de T-059), cada uma com fixture. Marcador verifica passa a valer so no fim da linha, o que tambem acaba com a truncagem de comando com parenteses. Fechada pelo loop com Codex `gpt-5.6-terra` na tentativa 1 da rodada 2, depois de parar para perguntar na rodada 1. Instalada nos tres destinos. Verificador 59 de 59, bateria 62 de 62.

## 2026-09-04 (T-065 pelo loop)

- Portao dos evals deixou de ser cego: 39 de 39 codigos com fixture, manifesto de etapas, inventario de fixtures, prompt do loop assertado, versao em prosa conferida. Fechada pelo loop com Codex `gpt-5.6-terra` na tentativa 1, contra portao proprio. As 11 mutacoes cegas da revalidacao agora sao pegas. Verificador 58 de 58, bateria 62 de 62.

## 2026-09-03 (T-059, T-061 e T-067 respondidas)

- Usuario aceitou item a item os niveis propostos em REVAL-1. Decisao em `docs/DECISIONS.md`; T-069 a T-071 abertas para a 2.6.0; REVAL-1, REVAL-2 e REVAL-6 resolvidas.
- T-061: opcao (c), parenteses no marcador verifica nao suportados e acusados (T-072); `--seco` sem `agente=` (T-060). REVAL-3 resolvida.
- T-067: `install.sh` avisa e pede confirmacao quando o destino diverge da fonte (T-073). REVAL-7 resolvida.

## 2026-09-03 (revalidacao adversarial da skill 2.5.1)

- Sete superficies atacadas por quatro familias de modelo, 24 mutacoes no portao dos evals (16 cegas), 70 itens confirmados no codigo, registrados como REVAL-1 a REVAL-7 em `docs/CONSENSUS.md`. Consertos sem bump em `evals/`, `install.sh` e README da skill (T-068); o resto virou T-059 a T-067. Material bruto em `docs/archive/revalidacao-2026-09-03/`.

## 2026-09-03 (skill v2.5.1 publicada)

- 2.5.1 instalada nos tres destinos globais. `diff -rq` acusa so `evals/`, `install.sh`, `README.md` e `CHANGELOG.md`, que nao sao distribuidos, e o `os.replace` da T-057 chegou nos tres `loop_task.py`.
- Reinstalada de proposito **antes** da revalidacao: a superficie de scaffold roda contra a copia instalada, e com os destinos em 2.5.0 a sessao acharia a T-057 de novo como se fosse achado novo, e criaria projeto com marcador de versao divergente da fonte.

## 2026-09-03 (skill v2.5.1)

- `loop_task.py` grava `docs/TASKS.md` por substituicao atomica. Antes usava `write_text` direto, que trunca antes de escrever: crash no meio partia o backlog vivo do projeto. Provado por mutacao; `test_loop.py` de 55 para 58 verificacoes.
- Regra em `docs/DECISIONS.md`: arquivo de memoria se escreve por substituicao atomica, nunca direto. Vale alem desta correcao.
- Prompt de revalidacao adversarial em `docs/PROMPTS.md`, distribuindo cinco superficies entre familias de modelo diferentes.

## 2026-09-03 (rodada de P-9 da spec 0006)

- 3 de 3 no desenho de quando a minuta e escrita. O criterio que resolve o conflito entre DEC-003 e DEC-006: publicado e anterior, nao publicado e contemporaneo. As duas decisoes falavam de momentos diferentes, e faltava escolher o instante da gravacao.
- Risco que a rodada expos e nao resolveu: o bruto pode conter segredo do repositorio, e preservar literal somado a versionar cria exfiltracao permanente para o historico do git.
- Dois defeitos do codigo publicado viraram T-057 (escrita nao atomica em `TASKS.md`, prioridade alta) e T-058 (sem protecao de colisao no `loop.sh`).

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
