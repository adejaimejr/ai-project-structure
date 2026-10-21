# SESSIONS 2026

Entradas antigas de `docs/SESSION.md`, rotacionadas em 2026-09-02 pela regra de "Rotacao De Arquivos" do `AGENTS.md`.

Cobre de 2026-04-25 (criacao da estrutura multiagente e validacao por tri-consenso) a 2026-09-03 (skill 2.4.0 e 2.5.0, com o formato de achado, o diagnostico com identidade estavel e as fixtures que os provaram). Ordem cronologica inversa, igual a do arquivo principal. Rotacionado tres vezes em 2026-09-03.

<!-- Rotacionadas em 2026-09-04, terceira vez: as duas entradas abaixo (T-065 pelo loop, e T-069 com a 2.6.0) vieram de docs/SESSION.md por tamanho. -->

<!-- Rotacionadas em 2026-09-04 (quarta rotacao do dia): as quatro entradas de 2026-09-04 abaixo (T-070 e a 2.7.0, T-069 e a 2.6.0, T-065 pelo loop, e as respostas de T-059, T-061 e T-067) vieram de docs/SESSION.md por tamanho. -->

<!-- Rotacionadas em 2026-10-17: as tres entradas de 2026-09-04 abaixo (T-064 e T-063 com a 2.9.0, T-060 com a 2.8.1, T-072 e T-071 com a 2.8.0) vieram de docs/SESSION.md por tamanho. -->

<!-- Rotacionadas em 2026-10-17, segunda vez no dia: as duas entradas de 2026-09-04 abaixo (T-054, T-056, T-058 e T-055 com a 2.10.0; T-062 e T-073 com a 2.9.1) vieram de docs/SESSION.md por tamanho. -->

<!-- Rotacionadas em 2026-10-17, terceira vez no dia: as duas entradas de 2026-09-04 abaixo (plano da spec 0006 com T-075 a T-077 e a 2.11.0, Grok pelo loop; respostas de T-053 e T-074) vieram de docs/SESSION.md por tamanho, antes da entrada da 2.12.0. -->

<!-- Rotacionadas em 2026-10-21: as tres entradas abaixo vieram de docs/SESSION.md por tamanho: 2026-10-17 - Claude (passagem de trabalho entre gestor e subagentes); 2026-10-17 - Claude (T-085: fixture aguardando-project com data relativa); 2026-10-17 - Claude (gatilhos da skill para o fluxo gestor e subagentes no Cloudroom). -->

<!-- Rotacionada em 2026-10-21 (segunda rotacao do dia): a entrada de 2026-10-17 abaixo (T-086, skill 2.12.0 levando Passagem De Trabalho) veio de docs/SESSION.md por tamanho. -->

<!-- Rotacionadas em 2026-10-21, terceira vez: as duas entradas de 2026-10-20 abaixo (camada GitHub e analise do ai-memory) vieram de docs/SESSION.md por tamanho. -->

<!-- Rotacionada em 2026-10-21, quarta vez: a entrada da fila T-078 a T-091 (skill 2.13.0) abaixo veio de docs/SESSION.md por tamanho. -->

## 2026-10-21 - Claude Opus 5.5 (planejamento da spec 0008, adaptador Cloudroom)

### Objetivo

- Executar o prompt "Planejar O Adaptador Cloudroom Para Consenso E Loop (Subagentes Visiveis)" de `docs/PROMPTS.md`: spec, tarefas e portoes, sem implementar. Sessao Cloud (Cloudroom, sandbox Linux), retomada por outro processo do Claude Code depois de o primeiro bater no limite de gasto.

### O Que Foi Feito

- Estado inicial: o working tree nao estava limpo, como o prompt pedia; tinha a camada GitHub da sessao anterior, ainda sem commit e esperando o usuario. Segui sem mexer nela, exceto pela rotacao de `SESSION.md`.
- Sondas na CLI real (cloudroom 0.1.67): `spawn` volta na hora com JSON e recusa opcao desconhecida; filho com `--shared-sandbox` roda na pasta da thread pai (o filho `cr_child_0fd8860dd542df3fb95f7b70` imprimiu `/code/ai-project-structure`) e nao ha opcao de diretorio; `thread output` sem `--all` corta a resposta em cerca de 2000 caracteres; filho em sandbox propria (`thr_...`) nao aparece em `thread list`, e `thread output` devolve so uma nota.
- Hipotese do prompt conferida no codigo: vale para o `loop.sh` (o prompt dele ja traz o caminho absoluto do projeto, e o `find -newer` enxerga o que o filho escreve no mesmo sistema de arquivos) e cai para o `consenso.py` (o filho nao fica preso na copia por participante, e le o projeto real onde o bruto do primeiro participante e gravado; isolamento so por prompt, que a 0006/DEC-003 rejeitou).
- Spec `docs/specs/0008-adaptador-cloudroom.md` em `Rascunho`, com DEC-001 a DEC-008 para P-1 a P-8, cada uma com a alternativa rejeitada, e as perguntas abertas P-A a P-D.
- `room-cli` falso `evals/mock_room_cli.py` e portoes `portao_t100.py` a `portao_t103.py`, rodados e falhando pelo motivo certo: T-100 0/17 (script ausente), T-101 0/6 (sem bateria, sem etapa, sem adaptador), T-102 1/13 (sem referencia, sem bump; so "sem travessao" passa, porque nada foi tocado), T-103 falha nos checks de perfil, bancada e evidencia.
- Tres defeitos meus achados no caminho e corrigidos: o check 3 de `portao_t100.py` tirava do PATH so o `room-cli` falso, e o real (`/usr/local/bin/room-cli`) abriria um filho de verdade quando o adaptador existisse; agora usa PATH vazio. `portao_t102.py` tinha o travessao literal (o verificador acusou; agora escapado). As rodadas dos portoes deixaram `evals/__pycache__` (o verificador acusou; removido).
- `SESSION.md` rotacionado (31KB com 4 entradas): as duas entradas de 2026-10-20 foram para `docs/archive/SESSIONS-2026.md`, indice atualizado para 54.
- T-100 a T-103 em "Proximas Tarefas".
- Respostas do usuario no chat: (1) consenso nesta sandbox com Codex em `-s danger-full-access`; (2) spec fica em `Rascunho` para outro modelo avaliar antes de implementar; (3) a spec 0007 (github) sai primeiro, na 2.14.0, e esta na 2.15.0; (4) Sonnet executa, Opus valida e coordena, Codex `gpt-6-luna` da a segunda opiniao. Viraram DEC-009 da spec, `NOVA = "2.15.0"` em `portao_t102.py`, perfil `Codex Luna, consenso` e a linha de papeis em `MEMORY.md`.
- Rodada de consenso `2026-10-21-161813-debate` (rodada 1 cega, `luna` = `gpt-6-luna` e `terra` = `gpt-5.6-terra`, ambos `high`): parou em exit 6 com os dois retidos por segredo. Falso positivo conhecido: so `_RE_PEM` no stderr (1 casamento no luna, 4 no terra), porque o log do Codex lista o codigo de `consenso.py`; stdout dos dois limpo. Os dois leram o repositorio (3 e 5 `exec`). Com o ok do usuario, movi o material para `docs/consensus/2026-10-21-161813-debate/` e rodei `retomar`: `aceitos_a_mao=luna,terra`, `concluida`, entrada em `docs/CONSENSUS.md` com `Status: aberto` e julgamento em branco. Os dois concordaram com DEC-002 e DEC-003 e acharam, sem se ver, o mesmo excesso na DEC-004: a sonda prova o diretorio inicial do filho, nao a escrita num `--projeto` arbitrario.
- Com o ok do usuario, DEC-004 restrita a `--projeto` igual a pasta da thread; criterio da bancada passa a conferir no sistema de arquivos onde o filho escreveu; T-102 e T-103 ajustadas; check 1e novo em `portao_t102.py`.
- Mutacao no `portao_t102.py` (um `references/cloudroom.md` temporario, sem e com a frase da pasta da thread, apagado depois) achou um bug do proprio portao: `texto.split(<int>)` dava `TypeError` assim que a referencia existisse com secao de limites, e a T-102 nunca passaria. Corrigido para fatiar a partir do heading; nas duas mutacoes 1, 1b, 1c e 1d passaram e 1e reprovou sem a frase e passou com ela.
- `docs/CONSENSUS.md` rotacionado (REVAL-6 e REVAL-7, `resolvido`, para o archive) e `SESSION.md` de novo (a entrada da fila T-078 a T-091 para o archive): os dois tinham passado de 30KB.
- Revisao da spec pelo Codex `gpt-6-luna` como thread filha visivel (`room-cli thread spawn --provider codex --model gpt-6-luna --reasoning-level high --shared-sandbox`, `cr_child_b0709855d0672dc1fec76ac7`, so leitura, sem arquivo tocado). Dos tres achados, dois aplicados nos portoes (4a de T-100 recusa flag fora da spec; 1c e 1e de T-102 exigem o sentido, com autoteste, contraexemplo e mutacao de tres textos: certo passa, ao contrario e palavra solta reprovam) e um nao (P-D segue aberta ate a ratificacao do usuario). Premissa do revisor conferida antes de aceitar: `--request-id` existe na CLI real (sem prompt ela devolve a ajuda; opcao inventada da `Unknown option`), entao o mock ficou como estava.
- Ratificacao pelo usuario ("ok" no chat) do texto de julgamento que eu redigi: entrada de consenso da spec 0008 `resolvido`, DEC-002 e DEC-003 marcadas ratificadas, P-D fechada, decisao nova em `docs/DECISIONS.md` (o adaptador nao entra no consenso enquanto o Cloudroom nao isolar um filho por pasta).
- No meio da sessao, outra sessao commitou a camada GitHub (`3b7a03b`, `c19197d`, `1ebec7d`) e, como commitou `SESSION.md` e o archive inteiros, levou junto a primeira versao desta entrada e a primeira rotacao. Nao reverti nada; spec, portoes, mock, tarefas e a rodada seguem sem commit.

### Arquivos Criados Ou Alterados

- Criados: `docs/specs/0008-adaptador-cloudroom.md`, `docs/skills/ai-project-structure/evals/mock_room_cli.py`, `portao_t100.py`, `portao_t101.py`, `portao_t102.py`, `portao_t103.py`.
- Criados tambem: `docs/consensus/2026-10-21-161813-debate/` (bruto e manifesto da rodada).
- Alterados: `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/CONSENSUS.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`.

### Decisoes Tomadas

- Nenhuma formal: DEC-001 a DEC-008 sao propostas da spec em `Rascunho`. A principal: o adaptador serve so ao loop; o consenso continua chamando CLIs direto.

### Aprendizados Para MEMORY.md

- Candidato, nao promovido (ainda nao consolidado): teste que simula "sem `room-cli`" tirando so o falso do PATH acha o real em `/usr/local/bin` na sandbox Cloudroom e abre filho de verdade; o cenario tem de usar PATH vazio.
- O comportamento do `room-cli` nas sondas ja esta na spec 0008 (DEC-001 a DEC-003); vira fato de `MEMORY.md` so depois da bancada real de T-103.

### Pendencias

- Passar a spec para `Definida`: do usuario (revisao do `gpt-6-luna` feita e ratificacao fechada).
- Os portoes so foram vistos falhando; nenhum foi visto passando, porque isso exigiria escrever o adaptador. O risco e um check impossivel de satisfazer, e a primeira rodada de T-100 mostra.

### Proximo Passo Recomendado

- Agente sugerido: Sonnet executa T-100 (subagente Cloudroom em `--shared-sandbox`), com Opus revisando diff, portao, verificador e mutacoes. Motivo: T-100 e T-101 tem portao mecanico e nao tocam arquivo proibido ao loop. Qualquer agente serve se tiver contexto suficiente.

## 2026-10-21 - Claude Fable 5.1 (gestor) com subagentes Sonnet 5.5 (camada GitHub, T-092 a T-099)

### Objetivo

- Executar o prompt "Aplicar A Camada GitHub E Abrir A Spec Do Modulo Github" de `docs/PROMPTS.md`: fase A da decisao de 2026-10-20 (CI, protecao de `main`, tags e releases, comunidade em ingles, README em ingles) e a spec 0007 do modulo `github`, sem bump. Sessao Cloud (Cloudroom, sandbox Linux), gestor em Fable 5.1, escrita de arquivos por subagentes Sonnet 5.5 (`room-cli thread spawn --shared-sandbox`, um por vez, mensagem no modelo de "Passagem De Trabalho" com a linha inteira da tarefa). Toda acao externa espera o sim do usuario, que nao estava na conversa: a sessao preparou tudo o que e local e parou antes do primeiro commit.

### O Que Foi Feito

- **Prompt desatualizado, adaptado sem reabrir decisao**: escrito com a skill em 2.12.0, mas `main` ja esta em 2.13.0 (`a480ed0`, sem tag), entao a lista de tags cresce para v2.4.0 a v2.13.0 e a Release 2.13.0 pode sair do proprio `release.yml` se a tag for a ultima acao. O commit `docs: camada GitHub, decisao, regras e prompt` que o prompt pedia primeiro ja existia (`7e7fbd3`). A parte de `evals/test_loop.py` de T-093 ja tinha sido resolvida na sessao anterior (fixture com `python3 -c`); `scripts/loop.sh:228` segue com `find -newer`. Baseline conferida: verificador 78/78, `--strict` 0 e 0, `git status` limpo depois da sincronizacao do Cloudroom.
- **T-092 (Sonnet, tentativa 1)**: `.github/workflows/ci.yml`, `name: ci`, push em `main` e `pull_request`, matriz `ubuntu-latest` e `macos-latest` com `fail-fast: false`, `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1` e `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0` (SHAs resolvidos por `gh api .../git/ref/tags/` pelo gestor e reconferidos pelo subagente), `permissions: contents: read`, `concurrency` por `github.ref` com cancelamento. Decisao do gestor: job de matriz `gates` mais um job agregador `ci` (`needs`, `if: always()`, falha se `needs.gates.result` nao for `success`), para o ruleset exigir um unico check chamado `ci` sem sufixo de sistema. Revisao: YAML carregado por `yaml.safe_load`, SHAs de 40 caracteres com comentario de versao, zero travessao. O subagente avisou de `.sonda-antes.txt` e `.sonda-depois.txt` na raiz (6 e 7 bytes, nao rastreados, sem referencia em script nenhum): removidos pelo gestor; mais tarde apareceu `.sonda-sync-marker` (vazio), tambem removido. Parecem da sincronizacao da sandbox, nao do repositorio.
- **T-096 (Sonnet, tentativa 1)**: `docs/CONTRIBUTING.md` (idiomas por camada, setup sem dependencias, os dois portoes com a saida esperada, travessao, commits, PR, releases, checklist de configuracao via `gh` ate a 2.14.0, onde cada coisa e registrada), `docs/SECURITY.md` (escopo local, so a ultima versao recebe conserto, Private Security Advisory, sem email), `docs/CODE_OF_CONDUCT.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `feature.yml`, `config.yml` (`blank_issues_enabled: false`, contact link para o advisory), `.github/dependabot.yml` (`github-actions`, mensal), `.gitattributes`; linha "Contribuicao" em "Links Internos" de `PROJECT_CONTEXT.md` e a linha da raiz em `QUALITY.md` com as excecoes. O subagente escreveu o Contributor Covenant 2.1 de memoria e disse isso; o gestor baixou o texto oficial (`contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md`, 5480 bytes, zero travessao) e comparou por diff normalizado: identico fora o contato (advisory no lugar de `[INSERT CONTACT METHOD]`), a linha de licenca CC BY 4.0 no fim e "email" por "e-mail", corrigido pelo gestor para o original.
- **T-097 (Sonnet, tentativa 1)**: `.github/workflows/release.yml`, gatilho `v*.*.*`, `permissions: contents: write`, `concurrency` sem cancelamento, so `actions/checkout`; passos em Python 3 stdlib: tag igual ao `version:` do `SKILL.md`, empacotamento dos sete itens em `ai-project-structure-X.Y.Z.zip` por `zipfile` (a sandbox nao tem `zip`; a versao Python e portavel e mantem o bit de execucao de `loop.sh` e `install.sh`) com `.sha256`, extracao da secao `## X.Y.Z - AAAA-MM-DD` do CHANGELOG da skill (respeita cercas de codigo, falha se a secao nao existe), corpo em ingles (Install com clone pela tag, Checksum, Changes com link para a ancora `#XYZ---AAAA-MM-DD` mais a secao em pt-BR) e `gh release create --latest`. Simulacao local com `TAG=v2.13.0` em `/tmp/rel-test`: 36 arquivos no zip, sem `evals/` nem `CHANGELOG.md`, `sha256sum -c` OK, corpo sem nada da 2.12.0; caminhos de falha testados (`v2.12.5` diverge do `SKILL.md`, `v9.9.9` sem secao, `v2.12.0` extrai so a 2.12.0). Evidencia real fica para a tag `v2.13.0` depois do merge.
- **T-098 (Sonnet, tentativa 1)**: `README.md` em ingles (104 linhas: link para o pt-BR na primeira linha, badges Release, CI e License, Why, matriz de suporte com caminhos e arquivo de entrada, quick start, tabela de `docs/`, Docs em "For users" e "For contributors", aviso de pt-BR, Inspirations com Specsfy e a comparacao com o ai-memory, Security, License) e `README.pt-BR.md` com o mesmo conteudo; 32 links relativos, 0 quebrados. Gestor corrigiu uma frase redundante no pt-BR.
- **T-099 (gestor)**: `docs/specs/0007-modulo-github.md` em `Rascunho`, no modelo de `docs/specs/README.md`: problema, escopo (bloco `github`, partial em pt-BR, `assets/github/en/` e `pt-BR/`, `ci.yml` gerado com o comando de "Testes E Validacao", `references/github.md`, pergunta 5, `MARKER_RE` e codigos `GITHUB-*`, verificador, evals 13 e 14, fixture `github-project`, prosa da raiz nos templates, bump 2.14.0 e dogfood), fora do escopo (`release.yml` como asset, `gh` pela skill, traducao), criterios de aceite no molde das specs 0004 e 0006, DEC-001 a DEC-003 tiradas do texto da tarefa, e P-1 a P-4 sem resposta. Correcao ao texto da tarefa: `evals.json` ja tem 12 entradas, entao os evals novos sao 13 e 14. Marcador `(spec: 0007-modulo-github)` na linha de T-099 e tarefa concluida com `tipo=conferencia`.
- **Preparado para o sim do usuario** (nada executado): JSON do ruleset (`deletion`, `non_fast_forward`, `required_status_checks` com o contexto `ci`, sem review); os treze comandos de tag abaixo; corpo em ingles da Release 2.12.0. Conferido com `git show -s` que cada SHA e o commit do bump e que o `SKILL.md` naquele commit declara a versao da tag.
- Registro: T-092 a T-098 em "Aguardando Usuario" com a pergunta de cada sim; `SESSION.md` rotacionado (entrada de 2026-10-17 sobre T-086 para o archive, indice com 52); `CHANGELOG.md` do projeto. Portoes finais: verificador 78/78, `--strict` 0 e 0, zero travessao em todo `.md`, `.yml` e `.gitattributes`, sem `__pycache__`. Nada commitado, pushado, tagueado ou publicado.

### Comandos De Tag Preparados

```bash
GIT_COMMITTER_DATE='2026-09-03 08:42:57 -0400' git tag -a v2.4.0 fc21d0e -m 'skill 2.4.0'
GIT_COMMITTER_DATE='2026-09-03 10:46:15 -0400' git tag -a v2.5.0 28681fd -m 'skill 2.5.0'
GIT_COMMITTER_DATE='2026-09-03 17:31:23 -0400' git tag -a v2.5.1 def48fa -m 'skill 2.5.1'
GIT_COMMITTER_DATE='2026-09-04 00:44:57 -0400' git tag -a v2.6.0 c41c0f3 -m 'skill 2.6.0'
GIT_COMMITTER_DATE='2026-09-04 08:32:38 -0400' git tag -a v2.7.0 a0a72f1 -m 'skill 2.7.0'
GIT_COMMITTER_DATE='2026-09-04 10:59:30 -0400' git tag -a v2.8.0 9a491a5 -m 'skill 2.8.0'
GIT_COMMITTER_DATE='2026-09-04 14:25:45 -0400' git tag -a v2.8.1 fb20b58 -m 'skill 2.8.1'
GIT_COMMITTER_DATE='2026-09-04 15:08:55 -0400' git tag -a v2.9.0 80f787f -m 'skill 2.9.0'
GIT_COMMITTER_DATE='2026-09-04 16:55:44 -0400' git tag -a v2.9.1 b1bbf9d -m 'skill 2.9.1'
GIT_COMMITTER_DATE='2026-09-04 17:26:48 -0400' git tag -a v2.10.0 a01fa3f -m 'skill 2.10.0'
GIT_COMMITTER_DATE='2026-10-17 12:36:59 -0400' git tag -a v2.11.0 06341a2 -m 'skill 2.11.0'
GIT_COMMITTER_DATE='2026-10-17 15:20:55 -0400' git tag -a v2.12.0 7b8bbd7 -m 'skill 2.12.0'
GIT_COMMITTER_DATE='2026-10-21 11:58:04 +0000' git tag -a v2.13.0 a480ed0 -m 'skill 2.13.0'
```

### Arquivos Criados Ou Alterados

- Novos: `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/dependabot.yml`, `.gitattributes`, `README.pt-BR.md`, `docs/CONTRIBUTING.md`, `docs/SECURITY.md`, `docs/CODE_OF_CONDUCT.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `docs/specs/0007-modulo-github.md`.
- Alterados: `README.md` (reescrito em ingles), `docs/PROJECT_CONTEXT.md`, `docs/QUALITY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`. Nenhum arquivo da skill.

### Decisoes Tomadas

- Do gestor, sem reabrir a decisao de 2026-10-20: job agregador `ci` no workflow para o ruleset exigir um check so; empacotamento por `zipfile` em vez de `zip -r`; taguear `v2.13.0` por ultimo, depois do merge de `release.yml`, para o workflow publicar a Release 2.13.0 (a 2.12.0 continua manual). As tres estao sujeitas ao sim do usuario.

### Aprendizados Para MEMORY.md

- Nenhum promovido. Candidato: subagente que reproduz texto licenciado (Covenant) de memoria avisa, e o gestor confere contra a fonte; a regra geral "texto de terceiro se baixa, nao se reproduz" so vale promover se repetir.

### Pendencias

- Do usuario, na ordem, cada uma com o sim: (1) branch `ci/portoes`, commit e PR de T-092; (2) merge com `ci` verde nos dois sistemas; (3) ruleset de T-094; (4) tags v2.4.0 a v2.12.0 e Release 2.12.0 (T-095); (5) branch `github/camada`, commit e PR de T-096, T-097 e T-098; (6) merge; (7) tag `v2.13.0` e conferencia da Release 2.13.0 publicada pelo workflow (evidencia de T-097); (8) `gh api .../community/profile` em 100 (T-096) e badges do README (T-098). Refletidas em "Aguardando Usuario" de `TASKS.md`.
- Se o CI em Linux ficar vermelho so por `loop.sh` (`find -newer`), a decisao de patch 2.13.1 ou 2.14.0 e do usuario (pergunta em T-093).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario responde os sins; qualquer agente com `gh` autenticado executa a ordem acima e move T-092 a T-098 para "Concluidas" com a saida real de cada comando de `(verifica:)`.
- Motivo: todo o trabalho local esta escrito e revisado; o que resta e acao externa, que o prompt reservou ao sim do usuario.

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

## 2026-09-04 - Claude, com Grok cursor-grok-4.6-high pelo loop (plano da spec 0006, T-075 a T-077, skill 2.11.0)

### Objetivo

- Desdobrar a spec 0006 (automacao do consenso), `Definida` com DEC-001 a DEC-010 e sem tarefa, em tarefas que cabem numa rodada de loop, cada uma com portao proprio, sem escrever codigo do produto.
- Depois da aprovacao do plano, a pedido do usuario: rodar T-075, T-076 e T-077 pelo loop (a ultima virou a madrugada de 2026-09-05).

### O Que Foi Feito

- Leitura na ordem pedida: `AGENTS.md`, a spec inteira, as quatro rodadas de loop mais recentes, `MEMORY.md` (Feedback e Project), `DECISIONS.md` de 2026-09-03 e 2026-09-04, `loop.sh` e `loop_task.py`, `references/loop.md`, e as entradas de P-7/P-8 e P-9 do archive. Plano mostrado e aprovado pelo usuario **antes** de gravar qualquer coisa.
- **Leitura da spec:** o primitivo e um orquestrador mecanico novo, `scripts/consenso.py`, que roda N agentes em paralelo, cada um numa copia propria do projeto sem `docs/consensus/`, e grava bruto e manifesto em `docs/consensus/<run-id>/` assim que cada agente termina; os pacotes em cima sao a minuta de debate (citacao linha a linha, julgamento em branco, atomica sob lock), a varredura de segredo, o achado (revalidacao dentro da entrada existente), a rodada 2 com anteriores na integra, a retomada por comando e os checks AVISO por `**Origem:**`. Do `loop.sh` reaproveita-se o contrato, nao o codigo.
- **Escolhas de forma, dentro das DECs e vetaveis antes da primeira rodada:** campos `**Origem:** automacao`, `**Manifesto:**`, `**Participantes:**` (todos os ids) e `**Falhas:**` (`nenhuma` ou ids); headings `### Posicao De <id>`, `### Falha De <id>` e `### Revalidacao De <id>`; `Metodo` sempre `pareceres-independentes` (nenhum modo mostra posicao contemporanea); `--pendente` obrigatorio da rodada 4 em diante, porque o campo e julgamento humano; sidecar em `docs/consensus/`, copias com `.git` e sem o sidecar; sem bloco gerenciado novo em `AGENTS.md`.
- **Nove tarefas, T-075 a T-083**, em "Proximas Tarefas" de `docs/TASKS.md` por script com substituicao atomica, na ordem de execucao e com dependencia dita na linha: primitivo (bump 2.11.0), lock e minuta, segredo, validador com fixture, achado, rodada 2, retomada, documentacao (portao sem `verify_repository.py`, porque a raiz precisa da propagacao do agente de chat), bancada real (tarefa do agente de chat, com evidencia `revisao-manual`). Cada linha diz o que e proibido ao loop e o que sobra para o chat. T-IDs listados na spec sem status; a spec segue `Definida` ate a primeira rodada, como combinado.
- **Nove portoes** sobre uma base comum, `evals/portao_consenso_lib.py` (molde de `portao_t058.py` mais agente falso, chamada do orquestrador e leitura do sidecar), cada um com regex autotestada contra exemplo e contraexemplo. Rodados hoje, **todos falham pelo motivo certo** (`scripts/consenso.py` ausente, versao 2.10.0, `test_consenso.py` ausente, sem run dir, sem secao no `SKILL.md`): T-075 1/14, T-076 1/13, T-077 0/10, T-078 6/14, T-079 1/12, T-080 0/11, T-081 0/11, T-082 2/8, T-083 1/4. O que passa hoje e o que deve continuar passando (raiz limpa, controle sem diagnostico, verificador).
- Dois consertos no proprio trabalho antes de qualquer verificacao: `portao_t076.py` nasceu com o travessao literal (trocado por `\u2014` escapado, regra de `MEMORY.md`); e o regex de perfil de `portao_t083.py` casava a nota do `cursor-agent` em `MEMORY.md`, que cita Codex, consenso e read-only na mesma frase, e foi apertado para a forma `- Codex, consenso:` com esse contraexemplo real no autoteste.
- `SESSION.md` passou de 30KB com a entrada nova: quatro entradas rotacionadas para o archive (T-070 e 2.7.0, T-069 e 2.6.0, T-065, respostas de T-059/T-061/T-067), indice do archive corrigido (41 entradas). Linha no CHANGELOG do projeto.
- **Rodada 1 de T-075 com Codex `gpt-5.6-terra`: morreu na cota.** 82.683 tokens na tentativa 1 e `You've hit your usage limit` (volta em 2026-09-05 02:18); tentativas 2 e 3 recusadas na hora; portao 3/14 nas tres, exit 2, nada movido. Sobrou um `consenso.py` parcial com `SyntaxError` (um `+` de patch meio aplicado). Nenhum arquivo de memoria tocado. Os marcadores da raiz estavam de volta em 2.10.0 antes de o loop comecar (o verificador passou 71/71 dentro da tentativa 1; a reversao veio de fora do loop, provavelmente do `sed` que eu mesmo tinha oferecido) e foram repostos.
- **Rodada 2 de T-075 com Grok pelo `cursor-agent` (`-p --force --model cursor-grok-4.6-high`), escolhido pelo usuario entre quatro opcoes: verde na tentativa 1**, em cerca de 8 minutos, no mesmo degrau base (cota nao e sinal de dificuldade). `scripts/consenso.py debate` com copias por agente (`copytree` sem `docs/consensus/`, `.consenso-lock` e `__pycache__`), `ThreadPoolExecutor` para o paralelo, bruto e manifesto gravados no `as_completed` de cada agente, manifesto por substituicao atomica, retencao de `## Registros` com nota, envelope de prompt com os seis itens do contrato, `git check-ignore` para o sidecar ignorado, ids validados contra `/` e `..`. Bateria `evals/test_consenso.py` com 13 checks (espelha o portao e importa a base `portao_consenso_lib.py`), etapa `verificar_testes_do_consenso` com piso 12, `consenso.py` compilado no verificador, bump 2.11.0 em `SKILL.md`, assets, partials e CHANGELOG da skill. `AGENTS.md` da raiz intocado. Portao 14/14; verificador de 71 para 74.
- **Revisao do que o Grok escreveu, sem conserto necessario:** `--titulo` e aceito e ainda nao usado (e de T-076); o envelope diz "copia somente-leitura" enquanto a copia e gravavel, o que e o desenho (isolamento por copia, nao por permissao); `run-id` com resolucao de segundo e recusa de duplicata; `.git` vai na copia, como a tarefa manda. Consumo nao impresso pelo `cursor-agent`. 2.11.0 reinstalada nos tres destinos com `--sim`, paridade limpa fora do nao distribuido.
- **T-076 com o mesmo perfil do Grok, verde na tentativa 1** (portao 13/13, uns 6 minutos), lancada depois de conferir que o portao falhava contra o `consenso.py` real (sem `--dono`, sem lock, sem sinal, sem minuta, bateria em 13, verificador acusando travessao sob `docs/consensus/`). O que entrou: `.consenso-lock` por `mkdir`, exit 5 com a mensagem do orfao, `soltar_lock` em `finally`; handler de SIGINT e SIGTERM que encerra os agentes vivos e leva a rodada a `status=interrompida` com exit 1, sem tocar em `CONSENSUS.md`; minuta no fim do arquivo por `escrever_bytes_atomico` (temporario, `fsync`, `os.replace`), na forma da tarefa, com `citar` pondo `> ` em toda linha e trocando U+2014 por hifen com `travessoes_substituidos` no manifesto; bloco `minuta` com os hashes e so entao `concluida`. Bateria de 13 para 24 (lock, SIGTERM, injecao, minuta), piso 24, `verificar_travessao` ignorando `docs/consensus/`, item no CHANGELOG 2.11.0. `AGENTS.md` da raiz intocado.
- **Revisao de T-076, sem conserto:** tres checagens redundantes de `_interrompendo` no caminho final (inofensivas); a interrupcao sai com exit 1, que a lista de exit codes do plano nao previa; anotado na linha de T-082 para a tabela dizer isso. Verificador 74/74, loop 77/77, consenso 24/24, `--strict` limpo, portao 13/13 de novo, sem sobras.
- **T-077 com o Grok: o trabalho ficou pronto em uns 8 minutos e o `cursor-agent` ficou preso por quase duas horas.** O log mostra seis `Connection lost, reconnecting`; o processo `node` morreu, o wrapper ficou vivo sem filho, e o `loop.sh` esperou, porque nao tem timeout de agente. Evidencia antes de agir: ultimo arquivo tocado as 22:41, `pgrep -P` vazio, e o portao rodado a mao contra o que ficou ja em 10/10. `kill -TERM` no wrapper; o loop viu exit 143 com arquivos alterados, rodou o portao (10/10) e fechou T-077 na tentativa 1. Licao promovida para `MEMORY.md`; o timeout no `loop.sh` virou **T-084**.
- **O que entrou em T-077:** `tem_segredo` com sete regex (AWS, PEM, rotulo com valor de 16+, `ghp_`, `sk-`, `xox`, URL com senha), aplicada a pergunta antes de chamar qualquer agente (exit 6 sem run dir) e a stdout e stderr de cada agente antes de gravar; bruto retido em `tempfile.mkdtemp("consenso-retido-")` com `stdout.txt` e `stderr.txt`, manifesto com `retido-por-segredo` e `retido_em` sem conteudo, `status=parada-segredo`, exit 6, mensagem ensinando mover ou apagar e `retomar`. Bateria 24 para 31, piso 30, CHANGELOG.
- **Um ajuste meu, provado por mutacao:** `sk-[A-Za-z0-9_-]+` casava `task-force`, `risk-based` e `desk-top` (conferido no interpretador), e nem o portao nem a bateria cobriam o prefixo. Regex dos tres prefixos com inicio de palavra e comprimento minimo (`\bsk-[A-Za-z0-9_-]{16,}`, idem `ghp_` 16 e `xox?-` 8), dois casos novos na bateria (chave `sk-` real dispara; `task-force`, `risk-based` e `desk-top` nao), piso 32, bateria 33/33. Efeito colateral meu no meio: um `import consenso` no interpretador gravou `scripts/__pycache__`; removido.

### Arquivos Criados Ou Alterados

- Skill, por mim (nao distribuidos): `evals/portao_consenso_lib.py`, `evals/portao_t075.py` a `evals/portao_t083.py`.
- Skill, pelo Grok nas rodadas de T-075, T-076 e T-077 (com o ajuste do `sk-` por mim): `scripts/consenso.py` (novo, distribuido), `evals/test_consenso.py` (novo), `evals/verify_repository.py`, `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`.
- Projeto: `AGENTS.md` (marcadores em 2.11.0), `docs/TASKS.md`, `docs/specs/0006-automacao-do-consenso.md` (T-IDs e `Em andamento`), `docs/SESSION.md`, `docs/MEMORY.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/` (README e quatro logs), `docs/CHANGELOG.md`. `docs/PROMPTS.md` ja estava alterado pelo usuario com o prompt desta sessao e nao foi tocado.

### Decisoes Tomadas

- Nenhuma formal. As escolhas de forma acima estao escritas nas tarefas, nao em `DECISIONS.md`, porque sao implementacao dentro das DECs; o usuario aprovou o plano sem veta-las. A spec 0006 passou a `Em andamento` com o fecho de T-075.

### Aprendizados Para MEMORY.md

- Promovido em `MEMORY.md`, secao User: o `cursor-agent -p` pode terminar o trabalho e ficar preso em reconexao sem sair; os sinais que separam isso de trabalho lento, e a saida (`kill -TERM` no wrapper, o loop deixa o portao decidir).
- Promovido em `MEMORY.md`, secao User, com sobrescrita ativa: a primeira rodada de loop completa do Grok neste projeto aconteceu hoje, pelo `cursor-agent` com `cursor-grok-4.6-high`, verde na tentativa 1 em cerca de 8 minutos, quando a cota do Codex acabou. Junto, a observacao que decidiu a troca: falha por cota nao e sinal de dificuldade, entao troca-se a ferramenta e mantem-se o degrau.
- O regex que casou a linha errada em T-083 e a regra ja registrada (regex de portao testada contra exemplo) aplicada com um contraexemplo tirado do arquivo real; nada novo.

### Pendencias

- T-078 a T-083 abertas, nessa ordem, mais T-084 (timeout de agente no `loop.sh`, fora da spec, sem portao ainda). T-078 (validador) e a proxima. Antes de T-083: rotacionar `docs/CONSENSUS.md` (30186 de 30720 bytes) e registrar os perfis `Codex, consenso` e `Grok, consenso` em `MEMORY.md` com o usuario.
- Codex `gpt-5.6-terra` sem cota ate 2026-09-05 02:18. Ate la, o loop roda com o Grok pelo `cursor-agent` ou com outro perfil que o usuario escolher.
- Do usuario: commitar. Plano e rodada estao juntos na arvore, separaveis por arquivo: do plano, `evals/portao_*` e os arquivos de `docs/`; da rodada, `scripts/consenso.py`, `evals/test_consenso.py`, `verify_repository.py`, `SKILL.md`, assets e CHANGELOG da skill.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente de chat, para mandar T-078 ao loop (Grok pelo `cursor-agent` no degrau base, ou Codex `terra` se a cota voltou), rodando `portao_t078.py` contra o validador atual antes de lancar. Vigiar o log: se parar em `Retry attempt N` sem arquivo tocado por muito tempo, e o caso de `MEMORY.md`, nao trabalho lento.
- Motivo: T-078 e independente do script e fecha a DEC-007 no validador; T-079 (achado) depende de T-077, que acabou de fechar, e pode ir em seguida.


## 2026-09-04 - Claude (respostas de T-053 e T-074)

### Objetivo

- Registrar as respostas do usuario a T-053 (posicao do Grok nas tres calibragens) e a T-074 (opcao a para o segredo no bruto), e levar a spec 0006 a `Definida`.

### O Que Foi Feito

- DEC-007 (forma entra no escopo, diagnosticos novos como AVISO), DEC-008 (proveniencia com manifesto ao lado e ponte curta) e DEC-009 (retomada sempre humana, bruto in-repo desde o inicio) escritas na spec com a forca de cada uma; copiadas para `docs/DECISIONS.md`; as duas entradas de consenso no archive fechadas como `resolvido`.
- A quarta pergunta, segredo no bruto versionado, ficou primeiro como P-10 e T-074 com tres opcoes esbocadas; o usuario escolheu a (a) em seguida: varredura de padroes antes de gravar, rodada para e pede palavra humana, nunca redige. DEC-010 na spec com as alternativas rejeitadas, criterios de aceite reescritos para DEC-007 a DEC-010, decisao copiada para `docs/DECISIONS.md`. **Spec 0006 passou a `Definida`**, sem pergunta aberta.

### Arquivos Criados Ou Alterados

- `docs/specs/0006-automacao-do-consenso.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/archive/CONSENSUS-2026.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- DEC-007 a DEC-010 da spec 0006, pelo usuario; resumo em `docs/DECISIONS.md`.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma tarefa aberta. O proximo trabalho e planejar a implementacao da spec 0006 (criar as tarefas dela), que ainda nao tem nenhuma.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para desdobrar a spec 0006 em tarefas com portao, e o usuario para aprovar o plano antes da primeira rodada.
- Motivo: a spec esta `Definida` com dez decisoes e nenhuma tarefa de implementacao; e trabalho tamanho-feature e merece plano antes de codigo.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-054, T-056, T-058, T-055, skill 2.10.0)

### Objetivo

- Fechar as quatro tarefas tecnicas anteriores a revalidacao, pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- Duas traziam "decidir antes de consertar"; como o usuario mandou fazer, apliquei criterio ja decidido e deixei escrito na tarefa: **T-054** cobra `Rodada` ausente como AVISO pelo mesmo codigo dos campos irmaos e so apos a data de adocao (criterio de T-059), mais `fullmatch`; **T-058** implementa lock em vez de so documentar, porque documentar nao conserta. Se o usuario discordar, reverte antes do commit.
- Quatro portoes proprios por comportamento (`portao_t054/055/056/058.py`). O da T-058 nasceu com um traceback (a segunda rodada sem lock ficava presa esperando o agente e estourava o `timeout`); tratado como FALHA em vez de excecao. Os quatro reproduziam os defeitos antes das rodadas.
- **T-054** (bump 2.10.0): verde de primeira, fixture `rodada-project` com oracle para ausencia e para sufixo. **T-056**: `--progress` conta so bullet de primeiro nivel; a spec 0006 voltou a reportar 3 perguntas; etapa `verificar_progresso_de_specs` no verificador. **T-058**: `mkdir .loop-lock` atomico, exit 5 para a segunda rodada, `rmdir` no `trap`, mensagem ensina limpar orfao, caso na bateria (77), secao "Uma Rodada Por Projeto" em `loop.md`. **T-055**: os dois modelos cercados da raiz ficam identicos aos do template e o verificador cobra (71 de 71).
- **Registro honesto sobre T-055**: a tarefa exigia editar `docs/CONSENSUS.md`, que o prompt do loop proibe ao agente. O agente **editou mesmo assim** (6 linhas, exatamente os tres campos do modelo cercado, nada nas entradas reais). A culpa e da instrucao: eu mandei para o loop uma tarefa cuja unica saida era um arquivo proibido, e o texto da tarefa venceu o prompt. Duas licoes: tarefa que exige tocar arquivo proibido ao loop e do agente de chat, nao do loop; e a proibicao do prompt nao resiste a instrucao contraria na propria tarefa. A segunda e um achado sobre a forca real do prompt e vai para `MEMORY.md`.
- 2.10.0 reinstalada nos tres destinos com `--sim` (o instalador recusou sem ela, como desenhado).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/loop.sh`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t05{4,5,6,8}.py`, `evals/fixtures/rodada-project/`, `evals/fixtures/progresso-subitens/`.
- Projeto: `AGENTS.md` (marcadores), `docs/CONSENSUS.md` (modelos cercados), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. As duas escolhas de T-054 e T-058 estao declaradas nas tarefas e aqui, com a porta aberta para reverter.

### Aprendizados Para MEMORY.md

- A proibicao no prompt do loop nao resiste a uma tarefa que manda fazer o contrario: o agente editou `CONSENSUS.md` porque a tarefa dizia para editar. Tarefa que exige tocar arquivo proibido ao loop e trabalho do agente de chat.

### Pendencias

- Aberta so **T-053** (calibragens da spec 0006, do usuario). Todo o resto do backlog fechou: 15 tarefas em dois dias, sete releases (2.6.0 a 2.10.0), 54 codigos com fixture.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para T-053.
- Motivo: e a unica tarefa aberta, e destrava a spec 0006 (automacao do consenso), que e o proximo modulo.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-062 e T-073, skill 2.9.1)

### Objetivo

- Fechar as duas ultimas tarefas da revalidacao adversarial (texto de `atualizacao.md` e `install.sh` com confirmacao) pelo loop com o `terra`.

### O Que Foi Feito

- **T-062** (bump 2.9.1): verde na tentativa 2. O texto do agente estava certo desde a tentativa 1; quem falhava era o meu portao, duas vezes: `.*` no titulo com `re.S` engolia o documento e capturava corpo vazio, e o titulo era comparado sem `re.I`. Corrigido com o loop rodando (ele rele o portao a cada execucao). Efeito colateral: tentando casar a regex, o agente renomeou dois headings de `atualizacao.md` (`MIGRAR TASKS` em minusculo, `v2 -> v2.x` em prosa); restaurados por mim. Licao: portao de texto que casa heading precisa de teste contra o texto **antes** da rodada, senao o agente escreve para a regex e nao para o leitor.
- **T-073** (sem bump): verde na tentativa 1. `install.sh` compara so o que distribui, lista `faltando`, `diferente` e `extra`, pede `[s/N]`, recusa sem terminal, aceita `--sim`; arquivo extra nao e apagado (decisao de T-067). `verificar_install` prova os dois lados com destino temporario sujo (verificador de 63 para 65). README da skill e CHANGELOG completados por mim.
- **Primeiro uso real da protecao**: a reinstalacao da 2.9.1 nos destinos em 2.9.0 recusou sem `--sim`, listando os arquivos, e instalou com `--sim`. `diff -rq` limpo fora do nao distribuido.
- `SESSION.md` rotacionado pela terceira vez no dia.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `install.sh`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/atualizacao.md`, `evals/verify_repository.py`, `evals/portao_t062.py`, `evals/portao_t073.py`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal.

### Aprendizados Para MEMORY.md

- Portao de tarefa que casa texto por regex precisa passar contra um texto de exemplo escrito antes da rodada. Dois bugs de regex no portao de T-062 custaram uma tentativa e dois headings renomeados pelo agente para satisfazer a regex.

### Pendencias

- **O pacote da revalidacao adversarial de 2026-09-03 esta inteiro fechado**: T-059 a T-073, seis releases (2.6.0 a 2.9.1). Abertas so T-053 a T-058, anteriores a revalidacao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario para T-053 (calibragens da spec 0006); qualquer agente para T-054, T-055, T-056 e T-058, que ja tem conserto descrito.
- Motivo: sao as unicas tarefas abertas, e as quatro tecnicas cabem numa release 2.10.0 pelo mesmo molde de portao proprio.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-064 e T-063, skill 2.9.0)

### Objetivo

- Fechar os dois residuos sem decisao da REVAL-2 e da REVAL-6 (consertos do validador e templates atrasados) pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- Portoes proprios por comportamento: `portao_t064.py` (12 checks, reproduzia 4 de 12) com o verificador geral dentro, porque a tarefa nao toca o core; `portao_t063.py` (12 checks, 2 de 12) sem o verificador, porque muda uma frase do core e a propagacao e minha.
- **T-064** (bump 2.9.0), verde na tentativa 1: `ARQUIVO-UTF8-INVALIDO` novo, com fixture materializada em latin-1 so no temporario; cercas `~~~` reconhecidas; headings ATX com fechamento aceitos; `field_value` sem `split` cego; `NNNN` tolerado so como placeholder inteiro; `**Status:**` de spec ancorado; `ENTRY_RE` e `DATE_RE` fora. Fixtures existentes ganharam os casos (debate-project como controle, cobertura-* acusando). Um ajuste meu: a fixture de consenso tinha `\u0301` como texto literal em vez do acento combinante real; trocado.
- **T-063**, verde na tentativa 1: QUALITY, PROMPTS, ONBOARDING, README, SESSION, TASKS, ARCHITECTURE e GLOSSARY dos assets atualizados para o core 2.2.0/2.4.0; exemplo `revisao-manual` no template de tarefas e o exemplo de spec fora do modelo de linha; core com "quando existir" em `docs/ARCHITECTURE.md`; `verificar_convencoes` cobre os quatro templates que citam regra do core (verificador de 59 para 63). Core propagado por mim; CHANGELOG completado com a frase do core.
- 2.9.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/docs/{QUALITY,PROMPTS,ONBOARDING,README,SESSION,TASKS,ARCHITECTURE,GLOSSARY}.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t063.py`, `evals/portao_t064.py`, `evals/fixtures/{cobertura-arquivos,cobertura-consenso,cobertura-tarefas,debate-project}/`.
- Projeto: `AGENTS.md` (core e marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal.

### Aprendizados Para MEMORY.md

- Nenhum novo.

### Pendencias

- Da revalidacao sobram T-062 (texto de `atualizacao.md`) e T-073 (`install.sh` com confirmacao), as duas baixas e sem decisao. Fora dela, T-053 a T-058.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-062 e T-073 juntas; nenhuma exige bump (T-062 muda `references/`, que e distribuido: exige; T-073 nao).
- Motivo: fecham o pacote da revalidacao inteiro.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-060, skill 2.8.1)

### Objetivo

- Fechar T-060, o pacote de consertos do modulo de loop (REVAL-3 e REVAL-4, onze itens), pelo loop com o `terra`.

### O Que Foi Feito

- Portao proprio por comportamento com agente falso por item (`evals/portao_t060.py`, 14 checks, reproduzia 0 de 14). Loop verde na tentativa 1, sem pergunta, stdin fechado no lancamento.
- Consertos do terra, revisados: linha da tarefa capturada no arranque (`loop_task.py linha`) e `fechar --linha-esperada` recusando se mudou; sub-linhas preservadas em `fechar` e `bloquear`; `errors="replace"` na saida e na pergunta; pergunta vazia vira `(vazia)` com exit 3; `fchmod` preservando o modo do `TASKS.md`; `sys.dont_write_bytecode` no helper; agente chamado com `</dev/null`; prompt dizendo que propagar bloco ao `AGENTS.md` e do agente de chat; exit 4 na tabela de `references/loop.md`; `--seco` sem `--agente`. Bump 2.8.1, bloco core intocado.
- Dois ajustes meus: a realimentacao da falha tinha sido truncada a 400 bytes (mesmo teto da evidencia), o que esvazia o que o loop faz de melhor; subi para 64KB. E o agente nao escreveu os casos hostis na bateria, que a tarefa pedia: portados por mim em `testar_hostil` (nove casos, bateria de 63 para 74; piso do verificador subiu junto). O caso de saida fora de UTF-8 quebrou o proprio harness da bateria, que decodificava o stdout do `loop.sh` em UTF-8 estrito; corrigido no harness.
- Seis mutacoes reversas (stdin aberto, `fchmod` fora, sub-linhas apagadas, linha esperada ignorada, realimentacao inteira, `--seco` com agente): seis pegas pela bateria.
- 2.8.1 reinstalada nos tres destinos. `SESSION.md` rotacionado de novo (duas entradas de 2026-09-03 para o archive).

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/loop.sh`, `scripts/loop_task.py`, `evals/test_loop.py`, `evals/verify_repository.py`, `evals/portao_t060.py`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. Realimentacao em 64KB e calibragem minha, registrada no CHANGELOG da skill.

### Aprendizados Para MEMORY.md

- Nenhum novo. "Portao por comportamento com agente falso" ja esta na pratica das ultimas cinco rodadas; virou molde (`portao_t0NN.py`), nao regra.

### Pendencias

- Todo o pacote da revalidacao que nao dependia de decisao esta fechado: T-060, T-065, T-069 a T-072. Abertas: T-062, T-063, T-064, T-073, e T-053 a T-058. Os portoes `portao_t0NN.py` ficam em `evals/` como registro; o que eles cobram vive na bateria e no verificador.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-063 (templates) e T-064 (tracebacks do validador), as duas ainda sem decisao pendente; o loop serve, com portao proprio.
- Motivo: T-063 e o que o usuario final recebe, e T-064 sao dois tracebacks reproduzidos.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-072 e T-071, skill 2.8.0)

### Objetivo

- Fechar o residuo de T-059 e T-061 (diagnostico de parenteses no marcador verifica, e texto honesto no core) pelo loop com o `terra`, numa release so.

### O Que Foi Feito

- As duas tarefas mudam o texto do bloco core, que o loop nao pode propagar para a raiz. Portoes proprios por comportamento e texto **sem** o `verify_repository.py` (paridade quebrada de proposito ate a propagacao), replicando o que ele cobraria de versao e cobertura por codigo. Marcadores da raiz em v2.8.0 antes; tarefas refinadas dizendo quem propaga.
- **T-072** (primeiro, faz o bump): loop travou na primeira tentativa de lancamento porque o `codex exec` herdou stdin aberto e ficou em "Reading additional input from stdin"; relancado com `</dev/null`, verde na tentativa 1. `VERIFICA-COMANDO-PARENTESES` (ERRO) com fixture, `loop_task.py check` recusa e explica, texto no item do marcador no core, no cabecalho do template de `TASKS.md` e em `references/loop.md`, teste novo na bateria (63). Core propagado por script, verificador 59 de 59.
- **T-071**: verde na tentativa 1. Secao das pontes diz o que o validador confere de fato (so a mencao a `AGENTS.md`). No travessao o agente **estreitou a regra** para os arquivos que o validador olha; a decisao era texto honesto sobre o alcance, nao regra menor (o verificador deste repo acusa em qualquer arquivo versionado). Reescrito por mim: a regra segue valendo em todo texto, o validador acusa em `AGENTS.md`, pontes e `docs/**/*.md`, fora disso ninguem confere por script. Propagado.
- 2.8.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.
- T-060 ganhou dois itens vindos destas rodadas: agente chamado com stdin fechado, e o prompt dizendo que propagacao ao `AGENTS.md` e do agente de chat.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/docs/TASKS.md`, `assets/partials/*.md`, `references/loop.md`, `scripts/validate_structure.py`, `scripts/loop_task.py`, `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t071.py`, `evals/portao_t072.py`, `evals/fixtures/cobertura-tarefas/`.
- Projeto: `AGENTS.md` (core e marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. Aplicadas as de T-059 (texto) e T-061 (opcao c).

### Aprendizados Para MEMORY.md

- Nenhum novo. O stdin aberto e defeito de script (T-060), nao licao de processo.

### Pendencias

- Com T-069 a T-072 fechadas, o residuo de T-059 e T-061 acabou. Abertas: T-060 (loop, agora com quatro itens novos), T-062, T-063, T-064, T-073, e T-053 a T-058.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-060, que e o pacote do loop e ja tem quatro defeitos reproduzidos por comando.
- Motivo: e a unica tarefa aberta com risco de dado (modo 664 para 600, sub-linhas apagadas) e cada rodada de loop desde ontem esbarrou em um item dela.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-070, skill 2.7.0)

### Objetivo

- Fechar T-070 (dez checks AVISO decididos em T-059) pelo loop com o `terra`, e publicar a 2.7.0.

### O Que Foi Feito

- Pre-checagem da raiz contra os dez avisos novos (nenhuma violacao real; `T-1` e `(bloqueada:` aparecem so em prosa e sub-linha), portao proprio por comportamento (`evals/portao_t070.py`, onze casos mais controle, versao e verificador; falhava em 12 de 14), marcadores da raiz em v2.7.0 por script, tarefa refinada dizendo isso para o agente nao parar de novo para perguntar.
- **Loop verde na tentativa 1**, sem pergunta desta vez. Dez codigos novos, 53 no total; `CONVENCOES-DATA-INVALIDA` de INFO para AVISO; `CONSENSO-ABERTO-SEM-PROXIMO-PASSO` passou a exigir valor, nao so presenca. Bump para 2.7.0 propagado, raiz identica ao asset.
- **Revisao:** fixtures existentes ajustadas de forma legitima (`achado-project/valido` tinha rodada 5 com exposicao `nao`, que agora e aviso; `aguardando-project/invalido` ganhou casos e oracle). Tres consertos meus: `TASK_OWN_ID_RE` tinha virado exatamente tres digitos, o que faria `T-1000` deixar de ser ID e o loop nao achar a tarefa (agora tres ou mais); o paragrafo da 2.6.0 no `SKILL.md` foi substituido pelo da 2.7.0 em vez de acrescentado (restaurado); README da skill sem a 2.7.0 (acrescentado).
- Quatro mutacoes contra o verificador (cerca aberta, resposta ausente, formato de evidencia, adocao de volta a INFO): quatro pegas.
- 2.7.0 reinstalada nos tres destinos, `diff -rq` limpo fora do nao distribuido.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t070.py`, `evals/fixtures/achado-project/valido/`, `evals/fixtures/aguardando-project/invalido/`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. "Tres digitos" da decisao de T-059 lido como "pelo menos tres": `T-1` e invalido, `T-1000` continua ID.

### Aprendizados Para MEMORY.md

- Nenhum novo. O padrao "refinar a tarefa com o que o agente vai perguntar" evitou a rodada perdida de T-069; e pratica, nao regra.

### Pendencias

- T-071 (texto do core), T-072 (diagnostico de parenteses), T-060 (loop) e T-073 (install.sh) abertas. Com T-069 e T-070 fechadas, das 17 promessas violaveis da REVAL-1/2 sobram as duas de texto (T-071).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-071 e T-072 juntas, que sao a proxima release (texto do core mais um ERRO).
- Motivo: fecham o residuo de T-059 e T-061 e cabem numa rodada so.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-069, skill 2.6.0)

### Objetivo

- Fechar T-069 (seis checks ERRO decididos em T-059) pelo loop com o `terra`, e publicar a 2.6.0.

### O Que Foi Feito

- **Portao proprio por comportamento** (`evals/portao_t069.py`): seis documentos errados montados de `assets/` precisam sair ERRO no arquivo certo, um projeto limpo precisa passar em `--strict`, versao acima de 2.5.1, verificador em exit 0. Falhava em 7 de 9. Sem ditar nome de codigo.
- **Rodada 1: exit 3, e era certo.** A tarefa manda propagar marcadores para o `AGENTS.md` da raiz e o prompt do loop proibe editar esse arquivo. O agente parou e perguntou em vez de decidir. Resposta operacional, pela regra do bloco de loop: quem edita `AGENTS.md` e o agente de chat. Marcadores da raiz postos em v2.6.0 por script antes da rodada 2, tarefa devolvida a fila.
- **Rodada 2: verde na tentativa 1.** Codigos novos `TASK-CONCLUIDA-SEM-DATA`, `VERIFICA-COMANDO-VAZIO`, `MARCADOR-ORDEM-INVALIDA`, `MARCADOR-LOOP-INVALIDO`, `NUCLEO-VAZIO`, `TASK-ID-ARQUIVADO-DUPLICADO`, cada um com fixture (o verificador exige desde T-065). Bump para 2.6.0 em `SKILL.md`, assets, partials e CHANGELOG; raiz byte a byte igual ao asset.
- **Revisao do que o terra escreveu, dois pontos:** (1) mudou a regex do marcador verifica para valer so no fim da linha, porque a resposta de T-059 na propria raiz mencionava `(verifica: )` em prosa e disparou o check novo. Defensavel (o core sempre disse "no fim da linha") e com bonus: comando com parenteses deixa de ser truncado e passa a ser recusado como "nao declarou". Mas nao estava no CHANGELOG; agora esta. (2) Satisfez a versao em prosa escrevendo uma frase nova e deixou a linha velha em 2.5.1: portao medindo o que sobrou. Corrigida a linha, e `verificar_versao` passou a exigir que **toda** ocorrencia bata e que a secao mais recente do CHANGELOG so cite a versao atual; provado por mutacao (prosa velha de volta reprova).
- `TASK-CONCLUIDA-SEM-DATA` so cobra linha com `T-NNN`: linha historica sem ID (fixture v1 e a raiz) continua tolerada, coerente com `TASKS-FORMATO-V1`.
- 2.6.0 reinstalada nos tres destinos globais, `diff -rq` limpo fora do nao distribuido, sem `__pycache__`.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/*.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/portao_t069.py`, `evals/fixtures/cobertura-arquivos/`, `evals/fixtures/cobertura-tarefas/`.
- Projeto: `AGENTS.md` (marcadores), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. A regex do verifica no fim da linha aplica o texto do core que ja existia.

### Aprendizados Para MEMORY.md

- Portao com regex "existe uma ocorrencia certa" e satisfeito por uma frase nova ao lado da errada. Cobre "toda ocorrencia bate", nunca "alguma".

### Pendencias

- T-070 (AVISO), T-071 (texto do core), T-072 (diagnostico de parenteses) e T-060 (loop) seguem abertas para a proxima release. Duas sessoes de loop consecutivas geraram uma pergunta operacional cada; o prompt do loop poderia dizer que a propagacao ao `AGENTS.md` e do agente de chat, para nao gastar rodada com isso (nao virou tarefa: e frase em `loop.sh`, cabe em T-060).

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-070, com portao proprio por comportamento, no mesmo molde de `portao_t069.py`.
- Motivo: e o par de T-069 e depende da mesma decisao, ja tomada.

## 2026-09-04 - Claude, com Codex gpt-5.6-terra pelo loop (T-065)

### Objetivo

- Fechar T-065, o portao dos evals cego (REVAL-4), pelo modulo de loop com o Codex `terra`, a pedido do usuario.

### O Que Foi Feito

- **Portao proprio antes de rodar.** O marcador da tarefa apontava para `verify_repository.py`, que ja passava com 46 de 46: o loop fecharia a tarefa verde com trabalho zero. Escrito `evals/portao_t065.py`, que cobra o resultado (39 codigos com oracle, inventario de fixtures, manifesto de etapas, prompt assertado, versao em prosa) e falhava em 5 de 6; o marcador da tarefa foi trocado para ele.
- **Loop na T-065**, `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="high"`, degrau base, com `PYTHONDONTWRITEBYTECODE=1` no ambiente porque `loop_task.py check` gravou `__pycache__` na skill e derrubou o check novo. Portao verde na tentativa 1, ~12 minutos. O agente nao tocou em `TASKS.md` nem em arquivo de memoria; um patch caiu em caminho errado (`evals/` na raiz) e ele corrigiu sozinho.
- **Revisao do que o terra escreveu**: quatro fixtures `cobertura-*` com oracle exato (uma por area, acumulando `NUCLEO-AUSENTE` de proposito para ficar pequena), `TRAVESSAO` provado por token `{{TRAVESSAO}}` materializado so no temporario (repo continua sem U+2014), `ETAPAS` com despacho por nome, quatro assercoes de prompt em `test_loop.py`, e a versao em prosa do `SKILL.md` em `verificar_versao`. Duas lacunas fechadas por mim: `verificar_inventario_fixtures` (disco contra `FIXTURES`) e `verificar_etapas` (toda `verificar_*` definida esta em `ETAPAS`).
- **Prova por mutacao**: as 11 mutacoes que passaram cegas em 2026-09-03 (M1, M2, M3, M5, M8, M9, M10, M17, M19, M22, M23) refeitas contra o portao novo: **11 de 11 pegas**, cada uma nomeando o diagnostico ausente. Verificador de 46 para 58, bateria do loop de 58 para 62.

### Arquivos Criados Ou Alterados

- Skill (nao distribuidos): `evals/verify_repository.py`, `evals/test_loop.py`, `evals/portao_t065.py`, `evals/fixtures/cobertura-{arquivos,consenso,rotacao,tarefas}/`, `README.md`.
- Projeto: `docs/TASKS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/archive/revalidacao-2026-09-03/`.

### Decisoes Tomadas

- Nenhuma formal. REVAL-4 fechada como `resolvido`; as sete entradas da revalidacao estao fechadas.

### Aprendizados Para MEMORY.md

- Portao que ja passa antes do trabalho nao e portao: o loop fecharia a tarefa verde com trabalho zero. Antes de mandar tarefa para o loop, rode o comando declarado; se sair 0, escreva um portao que falhe hoje.

### Pendencias

- T-060 ganhou o item do `__pycache__` do `loop_task.py`. `portao_t065.py` fica em `evals/` como registro; o que ele cobra agora vive no proprio verificador.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-069 e T-070 (checks novos), agora que cada codigo novo tem onde nascer com fixture; o loop serve, com portao proprio pelo mesmo motivo.
- Motivo: a decisao de T-059 esta tomada e o portao deixou de ser cego; e a hora de os checks entrarem.

## 2026-09-03 - Claude (respostas de T-059, T-061 e T-067)

### Objetivo

- Registrar as respostas do usuario a T-059, T-061 e T-067 e desdobrar em trabalho.

### O Que Foi Feito

- Usuario aceitou item a item a proposta de niveis de REVAL-1 (seis ERRO, dez AVISO, dois so texto). T-059 concluida com a resposta transcrita; decisao formal em `docs/DECISIONS.md`; REVAL-1, REVAL-2 e REVAL-6 fechadas como `resolvido`.
- Trabalho desdobrado por nivel: T-069 (ERRO), T-070 (AVISO), T-071 (texto do core). Os tres exigem versao 2.6.0 e dependem de T-065 para cada codigo novo nascer com fixture.
- T-061 respondida em seguida: opcao (c), parenteses no comando do marcador verifica nao sao suportados e o validador acusa (T-072), e `--seco` deixa de gravar `agente=` (item em T-060). REVAL-3 fechada como `resolvido`.
- T-067 respondida: `install.sh` avisa e pede confirmacao quando o destino diverge (T-073, sem bump). REVAL-7 fechada como `resolvido`. Das sete entradas, so REVAL-4 continua aberta, esperando T-065.

### Arquivos Criados Ou Alterados

- `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Em `docs/DECISIONS.md`: promessa do core sem check vira check com nivel declarado, ou texto honesto; codigo novo so entra com fixture.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Nenhuma tarefa da revalidacao aguarda o usuario; sobra T-053 (spec 0006). Pela regra do bloco specs, T-065, T-069, T-070 e T-071 juntas mudam contrato e passam de tres tarefas: cabem numa spec 0007, se o usuario quiser.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, comecando por T-065 e depois T-069.
- Motivo: sem o manifesto de cobertura, os checks novos nasceriam com o mesmo ponto cego que a revalidacao acabou de achar.

## 2026-09-03 - Claude Fable, com Grok, Codex, Gemini, GPT e Claude Opus (revalidacao adversarial da skill 2.5.1)

### Objetivo

- Atacar a skill inteira, sete superficies, com uma familia de modelo por superficie e outra verificando, e transformar o que sobreviver em conserto ou tarefa.

### O Que Foi Feito

- **Inventario conferido antes de gastar chamada**: `cursor-agent --list-models` nao tinha mais Kimi, GLM nem Gemini 3.8; sobraram quatro familias reais (Grok, GPT/Codex, Claude, Gemini 3.7 Flash). Distribuicao: Grok nas superficies 1 e 6, Codex nas 2, 4 e 7, Gemini na 3, Claude Opus executando a 5 pela skill instalada. Claude Fable selou posicao propria antes de qualquer agente rodar (arquivo em `docs/archive/revalidacao-2026-09-03/`), e verificou no codigo cada achado de outra familia.
- **Isolamento por DEC-003**: worktree descartavel com o corpo das duas entradas abertas de `CONSENSUS.md` retirado e nota dizendo que a omissao era proposital. Nenhum agente reportou a omissao como defeito.
- **Sete entradas de achado**, REVAL-1 a REVAL-7, em `docs/CONSENSUS.md` (REVAL-5 ja rotacionada por tamanho). Itens confirmados no codigo, contados por entrada: 10 no contrato do core (REVAL-1), 12 no validador (REVAL-2), 11 no loop (REVAL-3), 16 mutacoes cegas mais 3 efeitos colaterais no portao (REVAL-4), 8 nos templates (REVAL-6) e 10 na distribuicao (REVAL-7); nenhum ficou como "nao confirmado".
- **Superficie 4 por mutacao, 24 rodadas**, cada uma revertida de backup por `cp` e conferida por SHA-256: 16 passaram verde cegas, 8 pegaram. Codex, somente leitura, previu as cegas antes de ver o resultado e acertou todas as que os dois cobriram; a tabela dele mostra 10 de 39 codigos com fixture que os produza.
- **Consertos aplicados sem bump** (T-068): verificador sem `__pycache__` na fonte, piso de 58 na bateria do loop, `install.sh` sem bytecode e com `--all` no cabecalho, `evals.json` em 2.5.1, README da skill com instalacao manual completa.
- **Superficie 5 executada de verdade**, quatro fluxos pelo `claude -p` contra `~/.claude/skills`: scaffold, atualizacao de v1, spec com "Avançar" e ativacao de loop recusada. Nenhum defeito de fluxo.
- **Codex morreu na cota** do plano na superficie 7 depois de 312 mil tokens; refeita com GPT-5.6 via `cursor-agent`, que confirmou os mesmos itens. O usuario pediu no meio da sessao para nao gastar mais Codex nem GPT sol: nenhuma chamada foi feita depois disso.
- Rotacao de `CONSENSUS.md`: as rodadas de P-7/P-8 e P-9 (ainda `aberto`, T-053) foram para o archive por tamanho, com nota e ponteiros na spec 0006.

### Arquivos Criados Ou Alterados

- Skill (nao distribuidos): `evals/verify_repository.py`, `evals/test_loop.py`, `evals/evals.json`, `install.sh`, `README.md`.
- Projeto: `docs/CONSENSUS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/MEMORY.md`, `docs/CHANGELOG.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`, `docs/archive/revalidacao-2026-09-03/` (27 arquivos de material bruto, travessoes trocados por hifen e contados).

### Decisoes Tomadas

- Nenhuma de contrato. As calibragens estao em T-059, T-061 e T-067, em "Aguardando Usuario". Proposta de decisao registrada em REVAL-4: codigo de diagnostico sem fixture que o produza nao entra em `CODIGOS`.

### Aprendizados Para MEMORY.md

- Mutacao vale para portao **antigo**, nao so novo: os 44 de 44 escondiam seis checks inteiros que podiam sumir sem um FALHA.
- Tres sessoes de Codex `xhigh` em paralelo estouram a cota do plano em uma hora; GPT-5.6 via `cursor-agent` e o fallback da mesma familia. O usuario pediu `terra` para teste daqui em diante.

### Pendencias

- T-059, T-061, T-067 aguardam o usuario. T-060, T-062, T-063, T-064, T-065 abertas, alem de T-053 a T-058 que continuam validas (confirmadas pelas quatro familias).
- Achado mais caro: o portao dos evals (REVAL-4). Escapou porque o total de verificacoes e dinamico e nunca foi comparado com nada, e fixture so nascia junto com check novo.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario para T-059 (uma resposta destrava REVAL-1, 2 e 6); qualquer agente para T-065, que nao depende de decisao e e o que impede a proxima regressao silenciosa.
- Motivo: enquanto 29 dos 39 codigos nao tiverem fixture, qualquer conserto de T-060 a T-064 pode regredir sem o portao acusar.

## 2026-09-03 - Claude (T-057 e o prompt de revalidacao)

### Objetivo

- Consertar a escrita nao atomica de `TASKS.md`, e deixar pronto um prompt para uma sessao nova revalidar a skill inteira em varios modelos.

### O Que Foi Feito

- **T-057, o unico defeito aberto que podia destruir dado.** `loop_task.py` gravava `docs/TASKS.md` com `write_text` direto, que trunca antes de escrever. Agora e temporario no mesmo diretorio, `fsync`, e `os.replace`, com o temporario removido se falhar antes do rename. O pior caso passou a ser um orfao ao lado do arquivo.
- **Provado por mutacao, e nao por leitura.** Teste novo em `test_loop.py` quebra `os.fsync` de proposito no meio da escrita e confere que o arquivo original sobreviveu inteiro. Revertendo `escrever` para o comportamento antigo, o teste acusa: "TASKS.md intacto depois de escrita interrompida" falha e o arquivo trunca. Bateria de 55 para 58.
- Versao para **2.5.1**, porque `loop_task.py` e distribuido. Marcadores dos tres blocos subiram juntos por DEC-009, com o bloco core inalterado.
- A regra subiu para `docs/DECISIONS.md`, porque vale alem desta spec: arquivo de memoria do projeto se escreve por substituicao atomica, nunca por escrita direta.
- **Prompt de revalidacao escrito em `docs/PROMPTS.md`**, que e o lugar dele nesta estrutura, e nao um arquivo solto. Ele distribui cinco superficies (contrato do bloco core, validador, modulo de loop, portao dos evals, fluxos de scaffold) entre familias de modelo diferentes, em vez de fazer a mesma pergunta a todos, que so produz cinco versoes do mesmo vies.
- O prompt carrega o inventario de modelos conferido hoje, a lista do que **nao** deve ser redescoberto, e as onze restricoes que ja custaram tempo nesta sessao, incluindo as duas que me morderam: `git checkout` em arquivo com trabalho nao commitado, e `index()` casando com o modelo cercado no topo do `CONSENSUS.md`.
- A pedido do usuario, que quis a validacao da skill **inteira**, o prompt passou de cinco para **sete superficies**: faltavam os templates de `assets/`, que sao o que o usuario final recebe, e a distribuicao (`install.sh`, `agents/openai.yaml`, `README.md` e `CHANGELOG.md` da skill). Entrou tambem um **inventario de cobertura** arquivo a arquivo, para "toda a skill" ser conferivel em vez de afirmada, com a regra de que omissao declarada e aceitavel e omissao silenciosa nao.
- Reinstalacao feita **antes** da revalidacao, e nao por higiene: a superficie 5 roda contra a copia instalada, entao com os destinos em 2.5.0 a sessao nova acharia a T-057 de novo como achado novo, e criaria projeto com marcador divergente da fonte.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop_task.py`, `evals/test_loop.py`, `SKILL.md`, `CHANGELOG.md`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/PROMPTS.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Em `docs/DECISIONS.md`: arquivo de memoria do projeto se escreve por substituicao atomica. Vale para o `loop_task.py` ja publicado e para o orquestrador da spec 0006.

### Aprendizados Para MEMORY.md

- Nenhum novo. A licao de mutacao ja esta promovida, e esta sessao so a aplicou mais uma vez.

### Pendencias

- T-053 (tres calibragens da spec 0006 e a pergunta de segredo no bruto), T-054, T-055, T-056 e T-058 seguem abertas.
- Nenhuma. A 2.5.1 foi instalada nos tres destinos, com paridade conferida e o `os.replace` presente nos tres.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): sessao nova rodando o prompt de revalidacao de `docs/PROMPTS.md`.
- Motivo: sete defeitos reais sairam de tres rodadas de consenso feitas de improviso. O prompt existe para fazer isso de proposito, com distribuicao por familia de modelo em vez de repetir a mesma pergunta.

<!-- Rotacionadas em 2026-09-04, segunda vez: as duas entradas de 2026-09-03 abaixo (respostas de T-059/T-061/T-067, e a revalidacao adversarial da 2.5.1) vieram de docs/SESSION.md por tamanho. -->

## 2026-09-03 - Claude, Codex e Grok (rodada de P-9, o conflito entre DEC-003 e DEC-006)

### Objetivo

- Responder P-9, que nao e pergunta de desenho novo: e conflito entre duas decisoes ratificadas no mesmo dia.

### O Que Foi Feito

- **3 de 3 no desenho**, e o criterio que resolve o conflito veio do Grok: **publicado e anterior, nao publicado e contemporaneo**. A DEC-003 e a DEC-006 nunca se contradisseram; elas falavam de momentos diferentes, e faltava alguem escolher o instante da gravacao. Os tres classificaram o caso como **lacuna**, nao contradicao, e nenhum pediu para reverter decisao ratificada.
- Desenho convergente: lock exclusivo por projeto na abertura, bruto e manifesto gravados assim que cada agente encerra fora do alcance dos demais, minuta escrita uma vez so no fim por substituicao atomica do arquivo inteiro, e interrupcao deixando o `CONSENSUS.md` byte a byte como estava.
- **Argumento que sozinho ja proibe publicar cedo, e veio de uma decisao ratificada:** a DEC-005 tornou `N=1` valido, entao minuta a meio com 1 de 3 posicoes e **indistinguivel de uma corrida `N=1` concluida**. Nao e so vazamento, e ambiguidade de leitura. So o Grok fez essa ligacao.
- **O risco mais grave da rodada nao tem solucao proposta por ninguem.** O Codex mostrou a armadilha inteira: o bruto pode conter segredo do repositorio; a DEC-001 exige preservar literal; a P-8 aponta para artefato versionado; e redigir automaticamente destruiria justamente a evidencia. As tres posicoes juntas nao produziram saida. Ficou escrito na spec como nao resolvido.
- **Dois defeitos do codigo publicado apareceram como efeito colateral**, os dois conferidos antes de aceitos, e viraram T-057 e T-058: `loop_task.py:147` grava `TASKS.md` com `write_text` direto, que nao e atomico e pode rasgar o arquivo de memoria; e o `loop.sh` nao protege contra duas rodadas simultaneas, porque o sinal de pergunta tem nome fixo e o arranque apaga o leftover da rodada anterior.
- Duas ressalvas de independencia registradas na entrada, as duas **contra** a forca desta rodada: quem descobriu o conflito foi o Grok, entao ele respondeu a propria pergunta, ainda que sem lembrar do argumento; e o enunciado que os tres leram e a transcricao que o Claude fez do achado dele. Se a transcricao estreitou o problema, os tres herdaram o estreitamento.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- Nenhuma. O desenho de P-9 vira DEC-007 quando o usuario ratificar, e uma parte dele deve subir para `docs/DECISIONS.md`: escrever arquivo de memoria por substituicao atomica, nunca por escrita direta, porque isso vale para o `loop_task.py` ja publicado.

### Aprendizados Para MEMORY.md

- Nenhum novo. O que apareceu virou tarefa (T-057, T-058) por ser defeito de codigo, e nao licao reutilizavel.

### Pendencias

- T-053 acumula tres calibragens (P-7, P-8, P-9) mais a pergunta de segredo no bruto, que nenhuma rodada resolveu.
- T-057 tem prioridade alta: e o unico dos defeitos abertos que pode **destruir** dado do usuario, e nao so reportar errado.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente para T-057, que nao depende de decisao nenhuma; o usuario para as calibragens.
- Motivo: T-057 e conserto de duas linhas com risco real de perda de arquivo, e esta parado atras de decisoes de escopo que nao tem relacao com ele.

## 2026-09-03 - Claude, Codex e Grok (rodada 1 de P-7 e P-8)

### Objetivo

- Responder as duas perguntas que sobraram da spec 0006, com Codex e Grok, a pedido do usuario.

### O Que Foi Feito

- **Primeiro uso da DEC-003**, ratificada horas antes. Os agentes rodaram numa copia do repositorio com o corpo da entrada da rodada anterior **retido**, e uma nota no lugar dizendo que a omissao era proposital. Reter sem avisar faria os dois concluirem que nenhuma rodada havia acontecido, que e falso. O modelo de debate e o de achado ficaram na copia, porque **sao o objeto de P-7**.
- **3 de 3 nas duas perguntas.** A forma entra no escopo e a proveniencia entra no escopo. Nao houve empate: o que sobrou foi calibragem.
- **O achado que mais barateia P-7, conferido no codigo:** o validador **nunca exigiu heading de posicao nomeado**. As unicas exigencias de heading no script inteiro sao as de `SESSION.md` e a de "Por Que Nada Pegou Antes". O congelamento em Codex, Claude e Gemini esta no **template**, e nao no contrato. O Grok viu isso e recusou o binario da pergunta, partindo "forma" em tres camadas que ja nao coincidiam.
- Codex e Grok chegaram, sem combinar, ao mesmo mecanismo para nao quebrar o criterio de "projeto que nao automatiza nao ganha cobranca nova": um marcador `**Origem:**` que faz os checks novos valerem so para entrada automatizada. O Claude tinha declarado esse exato ponto como "buraco que nao sei resolver"; os outros dois resolveram.
- **Conflito entre duas decisoes ja ratificadas, achado pelo Grok:** DEC-003 proibe ver posicao contemporanea e DEC-006 exige ver as anteriores, e nenhuma das duas escolheu **quando** a minuta e escrita. Escrita incremental no meio da rodada vaza o contemporaneo pelo proprio repositorio. Virou P-9.
- **Tres defeitos da 2.5.0 atual**, achados pelos dois e conferidos no codigo antes de aceitos, viraram T-054 e T-055: `Rodada` ausente nao gera diagnostico nenhum; `re.match` em vez de `fullmatch` deixa passar lixo depois do valor; e o `Modelo De Debate` da raiz esta atras do asset da skill nos campos da 2.2.0.
- Um quarto defeito apareceu ao escrever a propria spec e virou T-056: `spec_overview` conta sub-item indentado como pergunta aberta, e a spec 0006 passou a reportar 7 perguntas quando tinha 3.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`.

### Decisoes Tomadas

- Nenhuma. As duas convergencias esperam ratificacao, e P-9 espera decisao.

### Aprendizados Para MEMORY.md

- Nenhum novo. Os desta sessao ja foram promovidos nas entradas anteriores.

### Pendencias

- T-053 segue em "Aguardando Usuario", agora com duas calibragens e P-9.
- T-054, T-055 e T-056 sao defeitos do que ja esta publicado, independentes da spec 0006. T-054 nao e conserto obvio: fechar os dois buracos para toda entrada e cobranca nova em projeto existente, o que esbarra num criterio de aceite da propria 0006.
- A transcricao continua sendo feita pelo modelo criticado. O risco registrado na rodada anterior nao foi resolvido por esta, e nao sera enquanto a operacao nao existir.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para as duas calibragens e P-9.
- Motivo: P-9 e o mais urgente dos tres, porque e conflito entre decisoes ja ratificadas, e nao pergunta nova. Enquanto ele nao for decidido, DEC-003 e DEC-006 se contradizem no papel.

<!-- Rotacionadas em 2026-09-04: as duas entradas de 2026-09-03 abaixo (rodada 1 cega da spec 0006 e a ratificacao das seis perguntas) vieram de docs/SESSION.md por tamanho. -->

## 2026-09-03 - Claude (ratificacao das seis perguntas da spec 0006)

### Objetivo

- Transformar em decisao o que a rodada 1 cega produziu, apos o usuario ratificar as seis.

### O Que Foi Feito

- **DEC-001 a DEC-006 escritas na spec 0006**, cada uma declarando **como** foi decidida, e nao so o que ficou decidido. Tres unanimes, duas em que o Claude foi vencido por 2 a 1, e uma com dissidencia registrada.
- A forca da decisao entrou no texto de proposito. DEC-004 e DEC-005 dizem que o Claude perdeu e por que; DEC-006 registra o argumento do Grok que perdeu mas sobrevive, e a consequencia pratica dele: quem implementar a rodada 2 tem de passar as posicoes anteriores na integra, porque resumo ali e regressao e nao otimizacao.
- **DEC-002 subiu para `docs/DECISIONS.md`**, porque muda o alcance de uma decisao ja registrada do projeto. A 0004/DEC-019 proibia o **agente** de escrever consenso; agora fica dito que a proibicao e sobre agente e nao sobre software, que um orquestrador mecanico escreve o recorte comprovado, e que o que sustenta a excecao e a separacao entre quem opina e quem escreve, nunca a quantidade de agentes. As outras cinco ficaram so na spec.
- Corrigido o defeito de escopo que o Grok apontou: "alterar qualquer projeto que nao seja este repositorio" confundia o projeto-evidencia da 0005 com o projeto-alvo de um script distribuido. Reescrito sem ambiguidade, e declarado que nao e mudanca de escopo.
- Os outros tres defeitos apontados eram **nas perguntas**, e sairam junto com elas ao virarem DEC. Ficaram registrados dentro das decisoes correspondentes, em vez de apagados: a DEC-003 diz que a premissa empirica de P-3(c) era falsa, e a DEC-005 diz que o exemplo de revisores no enunciado era o catalogo que a DEC-016 proibiu.
- Sobraram duas perguntas: **P-7**, sobre a forma da entrada, que ficou mais urgente porque a DEC-004 mandou cobrir tambem o achado, e sao duas formas para acomodar; e **P-8**, nova, sobre proveniencia entrar no escopo. Registrei P-8 em vez de decidir sozinho, mesmo com as tres posicoes recomendando: recomendacao unanime de modelos continua nao sendo decisao de projeto.
- Entrada de consenso fechada como `resolvido`, com o que ficou de fora da ratificacao dito na propria linha de `Resolvido em`.

### Arquivos Criados Ou Alterados

- Projeto: `docs/specs/0006-automacao-do-consenso.md`, `docs/DECISIONS.md`, `docs/CONSENSUS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`.

### Decisoes Tomadas

- DEC-001 a DEC-006 na spec 0006, ratificadas pelo usuario.
- Em `docs/DECISIONS.md`: agente nao escreve consenso, orquestrador deterministico escreve o recorte que a execucao comprova.

### Aprendizados Para MEMORY.md

- Nenhum novo. Os desta sessao (o caminho do `cursor-agent`, e que as CLIs se atualizam sozinhas) ja foram promovidos na entrada anterior.

### Pendencias

- T-053 segue em "Aguardando Usuario", agora so com P-7 e P-8.
- A spec continua `Rascunho`: as duas perguntas restantes mexem em escopo, entao nenhuma das duas e cosmetica.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario, para P-7 e P-8.
- Motivo: as duas sao escopo, e P-7 ficou acoplada a DEC-004. Decidir P-7 sem lembrar que agora sao duas formas a acomodar levaria a uma resposta que a propria ratificacao ja invalidou.

## 2026-09-03 - Claude, Codex e Grok (rodada 1 cega das perguntas da spec 0006)

### Objetivo

- Responder as seis perguntas abertas da spec 0006 consultando Codex e Grok, a pedido do usuario.

### O Que Foi Feito

- **Primeira rodada de consenso cega de verdade deste projeto, e ela e sobre a spec que quer automatizar exatamente isso.** A posicao do Claude foi escrita e selada em arquivo fora do repositorio **antes** de qualquer agente rodar; escrever depois seria `debate-aberto` disfarcado de parecer independente.
- Codex rodou com `codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high"`, com o mesmo arquivo de prompt, em processo separado e saida em arquivo proprio.
- A CLI propria do Grok recusou cinco vezes, com `You've reached your free Grok Build usage limit`, mesmo com o usuario assinando hoje e refazendo o login no meio. **A rodada so aconteceu por outro caminho:** o `cursor-agent`, ja instalado e autenticado com a assinatura do Cursor, expoe `cursor-grok-4.6-xhigh`. Rodou em `--mode ask`, read-only por construcao em vez de "nao edite" no prompt.
- Diagnostico do bloqueio do Grok foi refeito uma vez. A primeira leitura culpou o tamanho do pedido, porque um prompt de 20 bytes passava e um de 2858 falhava; a sonda de enchimento derrubou isso, porque 1000 bytes tambem falhou depois. O que separa passar de falhar e o momento: franquia pequena que repoe.
- Resultado com tres posicoes: **tres unanimidades (P-1, P-2, P-3), duas derrotas do Claude por 2 a 1 (P-4 e P-5), e uma maioria com dissidencia substantiva (P-6)**.
- Em P-1 e P-3 os tres recusaram as opcoes que a pergunta oferecia, cada um por conta propria. Recusas que coincidem valem mais que votos na mesma alternativa.
- **O Grok achou o risco que estava acontecendo no proprio registro:** se quem dispara a operacao for o modelo criticado, o Problema 3 sobrevive mesmo com N agentes isolados. Quem isolou as tres posicoes e escreveu o resumo das tres foi o Claude, que e uma delas e o alvo das outras duas. O isolamento resolveu a producao das posicoes e nao a transcricao.
- Ele tambem mostrou que a **ancora empirica da spec e falsa**: P-3(c) descreve "sem acesso ao repositorio", e a rodada de 2026-09-03 teve o repositorio visivel, sendo justamente a leitura do codigo que fez o Codex achar o erro factual. Mais tres defeitos confirmados na spec, todos independentes de decisao.
- Em P-1 e P-3 os dois modelos **recusaram as opcoes da pergunta**, independentemente e pelo mesmo motivo. E o sinal mais forte da rodada, porque nao e concordancia com uma opcao oferecida, e sim duas recusas que coincidem.
- O Codex corrigiu o fundamento da P-2 do Claude: a excecao a DEC-019 nao se sustenta por haver N agentes, e sim por separar os agentes opinantes de um **escritor deterministico**. Se quem escreve for um dos opinantes, o acoplamento volta com N igual a qualquer coisa.
- Tres criticas dele mudaram a spec no ato. A primeira foi conferida no codigo antes de aceita: o reuso do `loop.sh` estava superestimado, porque `loop.sh:145` decide se o agente fez algo com `find -type f -newer`, e agente de parecer nao escreve nada, entao cairia no `exit 4` da DEC-014 sempre. Corrigido no Problema 4, com a correcao declarada.
- A segunda virou **P-7**: "N agentes" e "nao mexer na forma" nao cabem juntos, porque nem o modelo de debate (secoes nomeadas para Codex, Claude e Gemini) nem o de achado (uma `Revalidacao` unica) representam N arbitrario, falha individual ou hash de insumo. Contradicao de escopo que o Claude nao tinha visto.
- A terceira ficou registrada como risco: a DEC-001 foi generalizada alem do que ela prova. Um comando comprova exit code e bytes; nao comprova qual modelo respondeu, se houve fallback, nem se o isolamento existiu.
- **A entrada bateu no defeito que ela mesma descreve.** O campo `**Rodada:** 1 de 1` afirma um denominador que ninguem sabe, e o Codex acabara de apontar que `N de N` ficou fragil depois que o teto saiu. Registrado nos riscos da propria entrada.
- `CONSENSUS.md` passou de 30KB e disparou `AVISO|ROTACAO`. A revisao da spec 0003, de 2026-09-02, foi para `docs/archive/CONSENSUS-2026.md`, que ficou com tres entradas.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/specs/0006-automacao-do-consenso.md`, `docs/TASKS.md`, `docs/MEMORY.md`, `docs/SESSION.md`, `docs/archive/CONSENSUS-2026.md`, `docs/archive/README.md`.
- Dois escorregoes meus na mesma sessao, os dois registrados: usei `t.index()` para cortar secoes da entrada e o indice casou com o **modelo cercado no topo do arquivo**, duplicando a entrada inteira; restaurado por `git checkout` (seguro desta vez, porque so aquele arquivo estava sujo) e refeito com ancora a partir do inicio da entrada. E antes disso, o diagnostico errado do bloqueio do Grok.

### Decisoes Tomadas

- **Nenhuma.** Quatro perguntas convergiram e continuam sem virar DEC, de proposito: parecer de modelo nao e decisao de projeto, e a regra de desempate diz que quem decide e o usuario quando ele esta disponivel.

### Aprendizados Para MEMORY.md

- **`cursor-agent` promovido como caminho de agente**, com os perfis de consenso e de loop, a nota de que os degraus de esforco vem no nome do modelo, e a de que o formato encaixa no `loop.sh` sem mudar nada porque `loop.sh:141` anexa o prompt como ultimo argumento.
- Promovido tambem que `grok` e `cursor-agent` **se atualizam sozinhos**, com o caso concreto de hoje: o `grok` foi de `1.0.5` para `1.0.13` no meio do diagnostico.
- Fato do usuario atualizado com sobrescrita ativa: ele assinou o Grok em 2026-09-03 e a CLI propria continua tratando a conta como free tier.

### Pendencias

- T-053 continua em "Aguardando Usuario", agora com cinco pedidos: ratificar as tres unanimes, ratificar ou virar as tres de maioria, decidir P-7, decidir se proveniencia entra no escopo, e mandar corrigir os quatro defeitos confirmados.
- `CONSENSUS.md` passou de 30KB de novo, e a rotacao expos uma tensao na propria regra: ela manda manter "as 5 a 10 mais recentes" e rotacionar acima de 30KB, e com poucas entradas grandes as duas metades se contradizem. Rotacionei o achado `0005-A1`, ja `resolvido` e com residuo fechado, em vez de encurtar a entrada nova, porque encurtar para o portao ficar verde e o que a regra "Nao Apague O Que Falha" proibe. Nao virou tarefa: e n=1 e pode nao se repetir.
- O artefato bruto de cada agente ficou fora do repositorio e nao foi preservado, contra o que a resposta de P-1 dos dois modelos recomenda. Nao virou tarefa porque o destino desse artefato e parte do que P-1 decide.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: sao cinco pedidos e nenhum deles e do agente. O mais interessante ficou sendo P-6: o Grok perdeu por 2 a 1, e o argumento dele (rodada 2 exige o pacote inteiro, e no instante em que o orquestrador resume o Problema 3 volta por dentro da automacao) sobrevive a derrota e vale ser lido antes de ratificar a maioria.

## 2026-09-03 - Claude (fixture de controle do criterio de achado)

### Objetivo

- T-052, o ultimo residuo da rodada 2 do achado `0005-A1`: exercitar literalmente o criterio "projeto que nunca registra achado nao recebe nenhum aviso novo".

### O Que Foi Feito

- Fixture `debate-project`: projeto que **usa** consenso de verdade e nunca declara `**Achado:**`. Oracle de conjunto vazio em `--strict`, que nesta arquitetura nao e teste fraco, porque a comparacao e nos dois sentidos e qualquer diagnostico reprova.
- Quatro controles no mesmo `CONSENSUS.md`: cerca dentro do corpo de uma entrada citando `**Achado:**`; entrada anterior a data de adocao, sem os campos declarativos; entrada na rodada 5 com `Pendente da rodada anterior`; e entrada que declara `Escapou de verificacao` **sem** declarar `Achado`, que fixa o opt-in do formato.
- Correcao de rota no meio: a primeira versao da fixture punha o modelo de achado cercado no topo do arquivo e o README dizia que aquilo guardava `strip_fences`. Nao guardava: o modelo fica antes de qualquer entrada datada e nunca entra em corpo de entrada. A cerca foi movida para dentro de uma entrada, e so entao o controle passou a existir.
- **Provado por mutacao, com duas rodadas.** Mutacao A (formato de achado deixa de ser opt-in): 37 de 44, com 6 diagnosticos inesperados so nesta fixture. Mutacao B (`strip_fences` para de limpar cercas): 42 de 44, e **so esta fixture acusou**. As outras cinco seguiram verdes, que e exatamente o buraco que T-052 existia para fechar.
- Reversao das mutacoes por backup em `cp`, e nao por `git checkout`, aplicando a licao da sessao anterior.

### Arquivos Criados Ou Alterados

- Skill: `evals/fixtures/debate-project/` (novo, 14 arquivos), `evals/verify_repository.py`, `CHANGELOG.md`.
- Projeto: `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. A fixture **fixa** uma decisao ja tomada na spec 0005: o formato de achado e opt-in pelo campo `**Achado:**`, entao entrada que declara `Escapou de verificacao` sem declarar `Achado` segue sendo debate e nao e cobrada. Mudar isso passa a ser mudanca visivel, e nao silenciosa.

### Aprendizados Para MEMORY.md

- Promovidos dois, no fechamento do dia: portao novo so entra depois de a mutacao provar que ele acusa; e reverter mutacao temporaria por backup proprio, nunca por `git checkout`, quando o arquivo tem trabalho nao commitado.
- O aprendizado anterior sobre check AVISO e portao continua valendo sem alteracao.

### Pendencias

- Nenhuma. Backlog zerado, cinco specs `Concluida`, "Aguardando Usuario" vazia.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, e de preferencia o proprio usuario usando a 2.5.0 em projeto real.
- Motivo: a spec 0005 fechou e o residuo dela tambem. O que vem agora depende de uso: o formato de achado so tem um achado registrado, e a forma dele ainda e n=1.

## 2026-09-03 - Claude (skill 2.5.0, diagnostico com identidade)

### Objetivo

- Fazer T-050 e T-051 juntas, que sao o mesmo desenho: tirar do portao a dependencia de exit code e de texto de mensagem.

### O Que Foi Feito

- T-051: os 39 diagnosticos de `validate_structure.py` ganharam codigo estavel, declarado no conjunto `CODIGOS`. `Report.add` recusa codigo nao declarado, entao diagnostico sem identidade quebra na hora de escrever. Um check estatico por AST conferiu que nenhum dos 39 sites ficou sem codigo e que nenhum codigo declarado sobrou sem uso.
- Flag `--codigos` nova: `NIVEL|CODIGO|ARQUIVO|SUJEITO`, uma linha por diagnostico, sem prosa. O `SUJEITO` (tarefa, entrada de consenso ou spec) e a peca que faltava: e ele que denuncia aviso que passou a cair na entrada errada, com codigo e contagem identicos.
- T-050: `FIXTURES` deixou de mapear nome para exit code e passou a declarar modo, exit esperado e o conjunto exato de diagnosticos. Comparacao nos dois sentidos, e fixture sem a chave `diagnosticos` e recusada em vez de virar aprovacao silenciosa. `verificar_achado` foi absorvida: um mecanismo, nao dois.
- **Discriminacao provada por mutacao, nao por afirmacao.** Tres mutacoes temporarias, revertidas depois: regressao compensada (o contraexemplo exato do Codex, com total e exit code identicos), sujeito trocado com codigos identicos, e fixture declarada sem oracle. As tres reprovaram; a primeira e a segunda passariam verdes na contagem de linhas antiga.
- Versao 2.5.0: mudou script distribuido e o formato da saida virou contrato publico, entao nao cabia amendar a 2.4.0. Marcadores dos tres blocos subiram juntos por DEC-009, com o conteudo do bloco core inalterado.
- Publicada: `git push origin main` levou `e70bd7c..28681fd`, e `./install.sh` propagou a 2.5.0 para os tres destinos globais, com paridade conferida por `diff -rq` e a flag `--codigos` presente nos tres.
- `SESSION.md` passou de 30KB e disparou `AVISO|ROTACAO`. Rotacionadas as quatro entradas mais antigas para `docs/archive/SESSIONS-2026.md`, que ficou com 24, mantendo as 6 mais recentes aqui e atualizando o indice do arquivo. Primeira vez que o aviso foi lido ja pelo codigo, e nao pela prosa.

### Arquivos Criados Ou Alterados

- Skill: `scripts/validate_structure.py`, `evals/verify_repository.py`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/AGENTS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/MEMORY.md`, `docs/SESSION.md`, `docs/archive/SESSIONS-2026.md`, `docs/archive/README.md`.

### Decisoes Tomadas

- Identificador estavel escolhido pelo usuario na rodada 2 do achado `0005-A1`. Implementado como codigo por diagnostico, com a saida `--codigos` separada do relatorio humano: o relatorio continua legivel e o portao ganha um formato que nao muda quando a redacao muda.

### Aprendizados Para MEMORY.md

- Nenhum novo. O aprendizado ja registrado sobre check AVISO foi atualizado para apontar a implementacao em vez da tarefa pendente.

### Pendencias

- Escorreguei uma vez: usei `git checkout` para reverter uma mutacao de teste em `verify_repository.py`, que e arquivo versionado com trabalho **nao commitado** por cima, e apaguei a reescrita inteira. Refeita na hora, sem perda. A licao e de operacao, nao do produto: para reverter mutacao temporaria em arquivo com trabalho pendente, guarde o original antes em vez de confiar no git.
- T-052 continua aberta e independente destas duas.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, para T-052.
- Motivo: a fixture so-debate e o unico residuo da rodada 2 que sobrou, e agora ela tem onde encaixar: entra no `FIXTURES` com oracle de conjunto vazio em `--strict`.

## 2026-09-03 - Claude e Codex (rodada 2 do achado 0005-A1)

### Objetivo

- Revalidar a disposicao do achado `0005-A1` com um modelo distinto, a pedido do usuario. Primeiro uso real da revalidacao que a 2.4.0 acabou de criar.

### O Que Foi Feito

- Rodada 2 no Codex CLI (`gpt-5.6-sol`, `model_reasoning_effort=high`, sandbox `read-only`, para ele nao poder editar nada). Prompt adversarial pedindo especificamente casos em que `verificar_achado` ficaria verde com o comportamento errado.
- Veredito do Codex: **se sustenta com ressalva**. Tres criticas conferidas no codigo antes de aceitar, e as tres procedem.
- **A disposicao da rodada 1 descrevia mal o proprio codigo.** Ela dizia que o check passou a medir "qual aviso", e `verificar_achado` conta linhas `[AVISO]` e confere uma unica exclusao. A entrada de `DECISIONS.md` tinha herdado o mesmo exagero: corrigida, com a correcao declarada em vez de silenciosa.
- **T-050 contradizia a propria disposicao.** Recusar par com o mesmo exit code nos dois lados eliminaria justamente a guarda que a disposicao mandou manter (`achado-project` tem os dois lados em 0 de proposito). Reescrita para exigir oracle discriminante por fixture.
- **O criterio "projeto que nunca registra achado nao recebe aviso novo" nao e exercitado literalmente**: os dois lados de `achado-project` tem achado, e a unica fixture com entrada de debate (`v1-project`) roda sem `--strict`. Virou T-052.
- Onde a revalidacao ficou incompleta, tambem registrado: o Codex nao viu que a raiz ja e um controle vivo desse ultimo item, porque roda em `--strict`, tem entrada de debate e fecha com zero avisos. Controle parcial, e a critica sobrevive reduzida.
- `**Escapou de verificacao:** sim` mantido contra a ressalva do Codex: o criterio da DEC-007 e se a verificacao existente pegaria o defeito, e ela nao pegaria.

### Arquivos Criados Ou Alterados

- Projeto: `docs/CONSENSUS.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`.

### Decisoes Tomadas

- Nenhuma nova. Uma decisao existente (fixture de check AVISO, 2026-09-03) foi **corrigida**: a regra segue valendo, a descricao que ela fazia da implementacao estava errada.

### Aprendizados Para MEMORY.md

- Refinamento do aprendizado ja promovido: contar linhas `[AVISO]` nao basta, porque aceita regressao compensada. Atualizado no lugar em vez de duplicado.

### Pendencias

- Nenhuma bloqueante. T-051 chegou a entrar em "Aguardando Usuario" com a pergunta "identificador estavel de diagnostico ou fragmento da mensagem?", e o usuario respondeu no mesmo dia: **identificador estavel**. A tarefa voltou para "Proximas Tarefas" com a escolha escrita nela. O achado `0005-A1` passou para `resolvido`, com o residuo em T-050, T-051 e T-052.
- Observacao sobre a forma, ainda n=1: o primeiro achado deste repositorio precisou de duas rodadas, e a rodada 2 achou erro factual na rodada 1. Isso e o formato funcionando, nao falhando, mas vale ver se o padrao se repete antes de tirar conclusao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, atacando T-051 e T-050 juntas.
- Motivo: as duas dependem do mesmo desenho (identificador estavel de diagnostico), ja escolhido pelo usuario. Separadas, o oracle seria escrito duas vezes.

## 2026-09-03 - Claude (skill 2.4.0, consenso que serve para achado)

### Objetivo

- Implementar a spec 0005: `CONSENSUS.md` passa a registrar achado, e nao so debate.

### O Que Foi Feito

- T-046: bloco core em v2.4.0 com tres mudancas. `### Achado` (identificador, disposicao, revalidacao), `### Ponto Cego Da Validacao Cruzada` em duas linhas, e o teto de rodadas trocado pela exigencia de `**Pendente da rodada anterior:**` acima de tres. Editado so no `assets/AGENTS.md` e propagado byte a byte para a raiz por script.
- DEC-008 fechou a mitigacao que DEC-002 deixou para a implementacao: o campo chama-se `**Achado:**` e o valor dele **e** o identificador. Um campo so marca e identifica, em vez de dois que podem discordar entre si.
- T-047: checks no validador, todos AVISO e todos opt-in. Antes de trocar a regra de rodada, conferido o que quebrava: a unica entrada real com `Rodada` na raiz e `2 de 3`, abaixo do limiar, e nenhuma fixture declarava rodada. So a mensagem de formato e o texto dos templates dependiam do teto.
- T-048: fixture `achado-project`, com a mesma entrada de debate abrindo os dois lados como controle. Foi ao escrever essa fixture que apareceu o achado do dia, abaixo.
- T-049: dogfood, CHANGELOGs, e reinstalacao com paridade conferida nos tres destinos globais.
- **Achado `0005-A1`, primeiro achado registrado neste repositorio, e sobre o proprio repositorio.** O padrao de fixture herdado da 2.2.0 (par `valido`/`invalido` com exit code esperado no `FIXTURES`) so funciona porque todo check daquela versao era ERRO. Os checks de achado sao AVISO, entao o par teria os dois lados em exit 0 e a suite reportaria `[OK] fixture achado-project/invalido: exit 0 (esperado 0)`: verde, sem provar nada. Corrigido com `verificar_achado`, que roda os dois lados em `--strict`, conta os avisos e confere que nenhum cita a entrada de debate.
- O conserto de portao que sobrou do achado virou T-050: fazer o `verify_repository.py` recusar um par cujos dois lados declarem o mesmo exit code, em vez de depender de quem escrever a proxima fixture lembrar disso.

### Arquivos Criados Ou Alterados

- Skill: `assets/AGENTS.md`, `assets/docs/CONSENSUS.md`, `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `references/atualizacao.md`, `scripts/validate_structure.py`, `evals/verify_repository.py`, `evals/evals.json`, `evals/fixtures/achado-project/` (novo).
- Projeto: `AGENTS.md`, `docs/CONSENSUS.md`, `docs/DECISIONS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/CHANGELOG.md`, `docs/SESSION.md`, `docs/specs/0005-consenso-para-achados.md`.

### Decisoes Tomadas

- DEC-008 na spec 0005: o campo do identificador de achado e `**Achado:**`, com o identificador como valor.
- Em `docs/DECISIONS.md`: fixture cujo caso invalido produz apenas AVISO roda em `--strict` e confere **quais** avisos sairam, nunca so quantos exit codes bateram.

### Aprendizados Para MEMORY.md

- Check novo que e AVISO nao separa fixture pelo exit code. Promovido, com ponteiro para o achado `0005-A1` e para a decisao.

### Pendencias

- O achado `0005-A1` esta com `**Status:** aberto` de proposito: a disposicao dele nao passou por ninguem alem de quem a escreveu, e a secao `### Revalidacao` esta com `(A preencher.)`. Fechar o status depende de um modelo distinto, ou do usuario, olhar a disposicao.
- Observacao de desenho, sem tarefa: o achado herdou `**Metodo:**` e `**Exposicao previa a outras posicoes:**`, que nasceram para debate. Num achado de um modelo so, a resposta honesta e `pareceres-independentes` com `nao`, o que e verdade mas soa estranho. Nao virou tarefa porque e n=1 e a forma pode encaixar melhor depois de alguns achados reais.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): um modelo distinto do Claude, e depois qualquer agente para T-050.
- Motivo: o achado `0005-A1` esta aberto esperando revalidacao independente, e revalidar a propria disposicao com o mesmo modelo e exatamente o que os campos de independencia existem para denunciar.

## 2026-09-03 - Claude, Codex, Grok e DeepSeek (bancadas de uso real do loop)

### Objetivo

- Usar o modulo de loop em tarefa de verdade, com a grade de perfis, e descobrir onde ele incomoda antes de confiar nele.

### O Que Foi Feito

- Grade de perfis fechada (T-038): `planejar` para Grok e opencode, e os degraus do DeepSeek remapeados a pedido do usuario. So o `grok-4.6` entrou, porque foi o unico exercitado; `--variant` saiu dos perfis DeepSeek por nao haver como confirmar efeito.
- Bancada 3 (T-039), primeira em projeto que **nao e codigo**: manual em Markdown, portao proprio, sete problemas plantados em cinco arquivos. Serviu para testar uma promessa da estrutura que nunca tinha sido exercitada.
- Achado principal: o agente fechou o portao **apagando** a frase que continha o link quebrado. Verde, informacao perdida. Em codigo isso salta aos olhos; em conteudo parece edicao. Virou a regra "Nao Apague O Que Falha".
- Segundo achado (T-039): a regra de estimar dificuldade lendo a tarefa nunca acertou e foi removida. Somando as tres bancadas, quatro ferramentas e tarefas bem diferentes, todas terminaram verdes na primeira tentativa, varias no modelo mais barato. Sobrou escalar so por falha observada ou por pedido do usuario.
- Matriz das quatro ferramentas (T-040), com consumo medido pela primeira vez. Resultado que inverte a leitura ingenua de exit code: a **unica** que fechou o portao foi a unica que destruiu informacao; as duas que sairam com exit 3 perguntando fizeram a coisa certa.
- DEC-018, o achado com mais alcance do dia: a regra vivia no bloco do `AGENTS.md` e foi ignorada; movida para o prompt do `loop.sh`, sem mudar mais nada, o mesmo modelo passou a perguntar. Ler o `AGENTS.md` e escolha do agente; o prompt chega sempre.
- Matriz refeita (T-041) confirmou, e o consumo **caiu** em todas as ferramentas, uma delas pela metade: dizer a restricao antes evita explorar caminho que seria descartado.
- Revisao item a item do bloco (T-042) pelo criterio da DEC-018. Cinco restricoes precisam do prompt, tres podem ficar so no bloco, e o unico buraco encontrado foi a ausencia de qualquer instrucao impedindo o agente de editar `AGENTS.md` e os arquivos de memoria. Risco teorico (nenhuma das nove rodadas fez isso), fechado mesmo assim porque o pior caso e silencioso.
- Variancia medida (T-043): Claude e Codex deterministicos nesta tarefa, tres de tres cada. DeepSeek com duas rodadas destrutivas antes da regra chegar ao prompt e zero em seis depois.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop.sh`, `references/loop.md`, `assets/partials/AGENTS-loop-block.md`, `CHANGELOG.md`, `README.md`.
- Projeto: `AGENTS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-018 na spec 0004: restricao critica vai no prompt, nao so no bloco. Criterio para decidir: se a violacao deixa o portao verde do mesmo jeito, a regra precisa do prompt.
- Escolha de degrau deixou de estimar dificuldade a priori.
- Perfil do Grok e do opencode fechados, com o degrau mais alto do Grok apontando para o teto dele, avisado na hora.

### Aprendizados Para MEMORY.md

- Ponte so existe para ferramenta que nao le `AGENTS.md` sozinha; conferido contando referencias dentro dos binarios do Grok e do opencode. Promovido.
- Comportamento do `deepseek-v4-flash` com a regra so no bloco. Promovido junto ao perfil dele.

### Pendencias

- Grok segue sem rodada completa: bateu limite do plano free nas tres tentativas, inclusive na ultima de hoje, que consumiu 22.503 tokens antes de a plataforma recusar. Depende de assinatura, entao nao vira tarefa: nenhum agente resolve isso.
- A rodada de regressao do DeepSeek criou o documento ausente com placeholder honesto em vez de perguntar. E n=1 e nao pode ser atribuida a nenhuma mudanca especifica; fica como observacao, nao como conclusao.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente, e de preferencia o proprio usuario usando o loop numa tarefa real dele.
- Motivo: tres bancadas ja cobriram o que teste sintetico alcanca. O que falta descobrir agora so aparece em uso de verdade, com tarefa que importa e portao que ele mesmo escreveu.

## 2026-09-02 - Claude (fechamento da 2.3.0)

### Objetivo

- Validar o modulo de loop numa segunda bancada antes de publicar, e fechar a versao.

### O Que Foi Feito

- Bancada 2 num subprojeto novo (`durakit`, parser de duracao), com tarefa diferente da primeira para nao pegar carona. Rodada nas tres ferramentas com **a string exata dos perfis gravados em `MEMORY.md`**, no degrau `executar-dificil`.
- Provou o que a bancada 1 nao cobria: que os perfis executam de verdade (eu os tinha escrito de help e catalogo, sem nunca rodar), que `agente=` aparece em evidencia real com a string inteira, e que `exit 4` dispara com agente mal configurado de verdade.
- As tres fecharam com portao verde na tentativa 1 e acertaram todos os casos que as regras determinam, inclusive fora da suite. Um caso extra meu nao era determinado pelas regras e as tres divergiram; reclassificado como ambiguo em vez de contado como falha.
- Publicada: `git push origin main` levou 10 commits (`440919f..6ef1a40`) e `./install.sh` propagou a 2.3.0 para os tres destinos globais. Paridade conferida por `diff -rq`, com o modulo de loop presente e `loop.sh` executavel.
- Spec 0004 fechada com quatro tarefas e mais nove de correcao e validacao surgidas depois da conclusao, todas registradas como DEC-014 a DEC-017.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop.sh`, `scripts/loop_task.py`, `evals/test_loop.py`, `evals/verify_repository.py`, `references/loop.md`, `SKILL.md`, `CHANGELOG.md`, `README.md`, `assets/partials/AGENTS-loop-block.md`.
- Projeto: `AGENTS.md`, `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`, `docs/specs/0004-modulo-de-loop.md`, `.gitignore`.

### Decisoes Tomadas

- DEC-014 a DEC-017 na spec 0004, todas posteriores a conclusao dela: exit 4 para agente que falha sem mexer em nada; `agente=` na evidencia; perfis em `MEMORY.md` com a skill montando a chamada; e nao registrar rodada que falhou, com a nota de que isso e escolha de escopo e nao impedimento.

### Aprendizados Para MEMORY.md

- Gemini CLI nao roda nesta maquina por conta, nao por defeito do modulo. Promovido.
- A evidencia vale o que o portao vale: duas de tres ferramentas, na bancada 1, fecharam tarefa com bug que a suite nao cobria. Promovido como ponteiro para `references/loop.md`, onde o argumento completo esta escrito.

### Pendencias

- Nenhuma acionavel. Backlog zerado, quatro specs `Concluida`, verificador em 33 de 33.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a 2.3.0 esta publicada, instalada e validada por duas bancadas. O que vem agora depende de uso real: o que incomodar na pratica vira a proxima spec.

## 2026-09-02 - Claude (rastreabilidade do agente e chamada assistida)

### Objetivo

- Registrar na evidencia quem fez o trabalho, e tirar do usuario a tarefa de digitar o comando do loop.

### O Que Foi Feito

- Correcao de leitura minha, apontada pelo usuario: os valores em dolar das CLIs sao preco de tabela da API. O JSON do Claude declara `"costBasis": "list"`. Quem usa assinatura nao paga aquilo, entao a tabela de custo da bancada estava mal rotulada. Corrigido na spec 0004, em `references/loop.md` e na entrada de sessao da bancada.
- Confusor da bancada tambem registrado: nenhum modelo foi fixado nas rodadas, entao a comparacao misturava ferramenta, modelo e esforco.
- `agente=<comando>` na evidencia, entre `tipo=` e `procedimento=`. O loop sabe o comando com certeza, porque foi ele que invocou; registrar e fato, nao alegacao, e respeita DEC-001.
- Chamada assistida: o usuario pede em linguagem natural e o agente do chat monta o comando. Os perfis por intencao e ferramenta vivem em `docs/MEMORY.md`, secao `## User`, que ja e o lugar de preferencia de quem toca o projeto. Nenhum arquivo de configuracao novo.
- Perfis de executar ganharam tres degraus (`executar`, `executar-dificil`, `executar-muito-dificil`), com a skill propondo qual encaixa a partir de sinais reais: rodada anterior que falhou, tarefa pertencer a spec, portao ser suite inteira, e o que a tarefa diz. Na duvida, o degrau mais baixo. Sem rubrica com pontuacao: julgamento declarado, com o sinal a vista, para o usuario discordar em uma palavra.
- Bancada 2, a pedido do usuario, antes de decidir publicar. Subprojeto novo e tarefa diferente, para nao pegar carona na anterior. Validou tres coisas que a bancada 1 nao cobria: que os perfis gravados executam mesmo (eu os tinha escrito a partir de help e catalogo, sem nunca rodar), que `agente=` aparece em evidencia real com a string inteira, e que exit 4 dispara com agente mal configurado de verdade.
- As tres ferramentas fecharam na tentativa 1 e acertaram tudo que as regras determinam. Um dos meus casos extras nao era determinado pelas regras e as tres divergiram; reclassifiquei como ambiguo em vez de contar como falha do Grok. Erro de teste meu, e uma ilustracao boa: onde a especificacao cala, modelos divergem.
- O usuario apontou um buraco na regra: o sinal mais forte dela, "a rodada anterior falhou", nao sobrevive ao fim da conversa, porque o loop nao registra fracasso. Ao investigar, apareceu que eu tinha descrito mal o impedimento: registrar fracasso nao feriria DEC-001, ja que exit code de portao vermelho e fato comprovado por comando, tao comprovado quanto sucesso. Nao gravar e escolha de escopo, e o usuario decidiu manter (DEC-017).
- Consequencia obrigatoria dessa escolha: a skill nao pode afirmar "e a primeira rodada", porque nao tem como saber. Ela diz que nao tem registro e deixa o usuario corrigir. Ausencia de registro nao e prova de ausencia de fracasso.
- A regra de escolha de degrau foi recalibrada depois de ser aplicada a tarefas reais: dois dos quatro sinais originais (portao ser suite, tarefa pertencer a spec) disparam em quase todo trabalho de codigo, entao a regra mandaria quase tudo para `executar-dificil` e o degrau base ficaria sem uso. Agora comeca no base e sobe so por sinal declarado, com destaque para o unico que tem evidencia: a rodada anterior ter falhado. A bancada sustenta isso, porque a tarefa mais parruda dela passou de primeira no esforco padrao das tres ferramentas.
- O usuario decidiu que o degrau mais alto do Grok aponta para o teto dele (`xhigh`, o mesmo de `executar-dificil`): ficar sem opcao era pior que repetir. Isso nao fere a regra recem-escrita, porque o problema era rebaixar **em silencio**. A regra ficou com tres casos: usar o teto quando ja decidido e registrado, avisando; perguntar quando nao houver decisao; e nunca escolher parecido calado.
- Escada de esforco do Grok confirmada pelo print e pelas strings do binario: termina em `xhigh` ("Extra High"), sem equivalente a `max`. Em vez de forcar tres degraus onde cabem dois, ficou registrado que o Grok nao tem o mais alto, e entrou regra nova: degrau que nao existe na ferramenta escolhida nao vira degrau parecido em silencio, porque rebaixar calado faz o usuario achar que pediu esforco maximo e recebeu outra coisa.
- Rotulo de interface nao e valor de CLI, e isso so apareceu porque o usuario mandou o print do menu do Codex. "Extra High" e `xhigh`; o menu nao mostra `max`; e `ultra` nao e so mais esforco, e raciocinio maximo **com delegacao automatica**, que abre subagentes. Os perfis pararam em `max` por decisao do usuario: numa rodada nao supervisionada, delegacao multiplica consumo de plano sem aviso.
- Fluxo conversacional para configurar os perfis, a pedido do usuario: perfil que so da para editar na mao envelhece. Ficou em `references/loop.md`, e nao no `SKILL.md`, porque o `SKILL.md` entra em contexto toda vez que a skill dispara. O passo que importa e o terceiro: confirmar o nome do modelo na propria CLI antes de gravar, nunca de memoria.
- Perfis do usuario gravados com strings verificadas, nao inventadas: `claude --help` confirma os aliases `fable`, `opus` e `sonnet` e os niveis de `--effort`; `~/.codex/models_cache.json` confirma `gpt-5.6-sol` e `gpt-5.6-terra`; `~/.codex/config.toml` confirma a chave `model_reasoning_effort`.

### Arquivos Criados Ou Alterados

- Skill: `scripts/loop_task.py`, `scripts/loop.sh`, `SKILL.md`, `references/loop.md`, `CHANGELOG.md`, `evals/test_loop.py`.
- Projeto: `docs/MEMORY.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-015: `agente=` na evidencia.
- DEC-016: escolha de modelo fica no usuario, com perfis em `MEMORY.md`, e nunca na linha de tarefa nem dentro da skill.

### Aprendizados Para MEMORY.md

- Perfis de loop e a natureza do custo sob assinatura foram promovidos para `MEMORY.md`, secao `## User`.

### Pendencias

- Nenhuma acionavel. Depois da bancada 2 o usuario autorizou publicar: `git push origin main` levou os 9 commits (`440919f..e9640d3`) e `./install.sh` propagou a 2.3.0 para os tres destinos globais, com paridade conferida por `diff -rq` e o modulo de loop presente (`scripts/loop.sh` executavel, `scripts/loop_task.py`, `references/loop.md` e o partial do bloco).
- As linhas de sessoes anteriores que dizem "os tres destinos continuam na 2.2.0" valiam quando foram escritas e ficam como estao: registro historico nao se reescreve.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: o que faltava responder por teste ja foi respondido. O resto e decisao de publicar.

## 2026-09-02 - Claude, Codex e Grok (bancada multi-ferramenta do loop)

### Objetivo

- Rodar o modulo de loop com varias ferramentas num subprojeto real, medir custo e descobrir o que quebra fora do teste com agente falso.

### O Que Foi Feito

- Subprojeto `slugkit` montado quatro vezes, identico: portao real (`python3 test_slugify.py`) falhando no inicio, T-001 bem especificada e T-002 deliberadamente sem contexto.
- T-001: Claude, Codex e Grok fecharam com portao verde na tentativa 1. Gemini nao rodou, por `IneligibleTierError` da conta, nao por defeito do modulo.
- T-002 foi o teste que importava: chutar o limite padrao passaria no portao, porque a suite nao cobre isso. Os tres escreveram `.loop-pergunta` e pararam. O bloco de loop no `AGENTS.md` segurou a regra "Nunca Inferir" sob incentivo contrario.
- Consumo: Claude 295k de cache read na primeira tarefa e 233k na segunda; Grok 193k e 155k tokens; Codex 23.958 e 16.817 tokens. Os valores em dolar que as CLIs imprimem sao preco de tabela da API (`costBasis: list` no Claude), nao o que se paga em assinatura: servem para comparar rodadas, nao para prever fatura.
- Dois defeitos achados e corrigidos: o loop insistia com agente que nunca executou (virou exit 4, com teste novo), e as flags por ferramenta nao estavam documentadas (viraram tabela em `references/loop.md`).
- Duas das tres implementacoes de T-001 tinham bug numa regra de borda que a suite nao cobria, e o loop fechou as duas com evidencia legitima. Registrado como limitacao central do desenho: a evidencia vale o que o portao vale.

### Arquivos Criados Ou Alterados

- `scripts/loop.sh` (exit 4), `evals/test_loop.py` (53 verificacoes), `references/loop.md`, `CHANGELOG.md` da skill.
- `docs/TASKS.md`, `docs/SESSION.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-014 na spec 0004: agente que falha sem mexer em arquivo encerra a rodada em vez de gastar tentativa. Decisao de implementacao posterior a conclusao da spec, registrada la com o motivo.

### Aprendizados Para MEMORY.md

- Portao fraco automatizado continua fraco, so que mais rapido. Duas ferramentas passaram no portao com bug de borda. Ficou em `references/loop.md`, que e onde quem for declarar `(verifica:)` vai ler; nao promovido para `MEMORY.md` por ser regra da skill e nao deste repositorio.

### Pendencias

- Os tres destinos globais continuam na 2.2.0: a skill nao foi reinstalada depois da 2.3.0.
- Decisao de publicar ou nao a 2.3.0 esta com o usuario.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): o usuario.
- Motivo: a bancada respondeu o que dava para responder por teste. O que falta e decisao: publicar, e se o custo por tarefa faz sentido para o uso que voce pretende.

## 2026-09-02 - Claude + Codex (skill 2.3.0, modulo de loop)

### Objetivo

- Implementar a spec 0004 inteira: o modulo de loop, que faz a estrutura executar uma tarefa verificavel em vez de so descreve-la.

### O Que Foi Feito

- T-019: bloco de loop, `references/loop.md`, secao de ativacao no `SKILL.md` com o portao de `QUALITY.md`, marcadores dos tres blocos em v2.3.0, e o fluxo de atualizacao ensinado a tratar o bloco novo sem nunca oferecer a ativacao.
- T-020: `loop.sh` orquestra, `loop_task.py` faz toda edicao de `TASKS.md` reusando o parser do validador. Falta de contexto e sinalizada por arquivo, nao por linha no stdout (DEC-011 e DEC-012, decididas pelo usuario antes da implementacao).
- T-021 e T-022: a bateria do loop saiu do scratchpad e virou `evals/test_loop.py`, com 47 verificacoes e agente falso. O verificador foi de 26 para 33 checagens e passou a rodar a bateria por dentro, alem de conferir o bloco `loop`, o bit de execucao e se os tres scripts distribuidos compilam.
- T-023: modulo ativado neste repositorio e rodada real com o Codex na T-025, uma tarefa pequena e honesta (`.loop-pergunta` no `.gitignore`) cujo portao falhava de proposito antes e passou depois.
- Na rodada real, o Codex declarou por conta propria que nao alterou `TASKS.md` nem escreveu evidencia. E a regra do bloco sendo obedecida por um modelo que nao participou desta implementacao, que era a duvida que sobrava.

### Arquivos Criados Ou Alterados

- Skill: `SKILL.md`, `CHANGELOG.md`, `README.md`, `references/loop.md` (novo), `references/atualizacao.md`, `assets/partials/AGENTS-loop-block.md` (novo), `assets/AGENTS.md`, `scripts/loop.sh` (novo), `scripts/loop_task.py` (novo), `evals/test_loop.py` (novo), `evals/verify_repository.py`.
- Projeto: `AGENTS.md` (bloco de loop ativado), `.gitignore` (pelo proprio loop), `docs/TASKS.md`, `docs/SESSION.md`, `docs/CHANGELOG.md`, `docs/specs/0004-modulo-de-loop.md`.

### Decisoes Tomadas

- DEC-011 e DEC-012 da spec 0004, do usuario: sinal por arquivo e helper em Python reusando o parser do validador.
- DEC-013, minha: formato do campo `resultado`, com corte pelo comeco e truncagem declarada.

### Aprendizados Para MEMORY.md

- Nenhum. As decisoes ficaram na spec e em `DECISIONS.md`.

### Pendencias

- A skill nao foi reinstalada nos tres destinos globais: eles continuam na 2.2.0, sem o modulo de loop.
- A rodada real usou uma ferramenta so. O `--agente` e neutro por construcao, mas `claude -p` e `gemini -p` nao foram exercitados.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: a 2.3.0 esta fechada e verificada. O que sobra e propagacao (reinstalar) e uso real, que so o tempo mostra.

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

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

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

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

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

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

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

### Aprendizados Para MEMORY.md

- (Nao registrado nesta sessao. Heading adicionado em 2026-09-02 para conformidade com o template; nada foi promovido para `MEMORY.md` retroativamente.)

### Pendencias

- Instalar a skill em `~/.codex/skills/ai-project-structure` caso seja desejado torna-la global no Codex.
- Preencher os arquivos de contexto conforme o projeto real evoluir.

### Proximo Passo Recomendado

- Pedir ao Claude para revisar a estrutura usando o prompt em `PROMPTS.md`.
