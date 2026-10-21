# CHANGELOG - skill ai-project-structure

Historico de versoes da skill. A versao canonica vive no frontmatter do `SKILL.md`.

## 2.14.1 - 2026-10-21

Patch sem mudanca de comportamento. Marcadores `core`, `specs`, `loop` e `github` em v2.14.1;
o conteudo dos blocos nao muda. Portao: `evals/portao_t110.py`.

- O `description` do frontmatter do `SKILL.md` cai de 1479 para 982 caracteres, dentro do teto
  de 1024 do padrao Agent Skills (agentskills.io/specification), que a 2.13.0 ja passava (1394).
  Ficam todos os gatilhos (estrutura multiagente, converter, atualizar, validar, specs, loop,
  modulo github, consenso) e a regra de nao disparar em pedido generico de criar projeto. Saem
  o gatilho redundante "scaffold Markdown multiagente", o detalhe dos perfis do loop (que esta no
  corpo) e exemplos repetidos. Texto aprovado pelo usuario (T-110).
- Conserto: o `description` da 2.14.0 tinha ": " no meio de um valor sem aspas ("camada GitHub do
  repositorio: comunidade"), YAML invalido que o Claude Code carrega por ser tolerante e que um parser
  estrito recusa. O texto novo nao tem ": " nem " #".
- `evals/verify_repository.py` ganha a etapa `verificar_frontmatter`: YAML seguro em valor sem aspas,
  `description` com 1 a 1024 caracteres e `name` no formato do padrao. Aplicada ao `SKILL.md` da 2.14.0,
  reprova os dois defeitos.

## 2.14.0 - 2026-10-21

Bump que leva o modulo opcional `github` (spec 0007) e a correcao de corrida incompleta na
origem do consenso (T-104). Marcadores `core`, `specs`, `loop` e `github` em v2.14.0; o
conteudo dos blocos core, specs e loop nao muda. Portoes: `evals/portao_t106.py` a
`evals/portao_t109.py` (modulo github) e `evals/portao_t104.py` (T-104).

- Modulo `github`, so com resposta explicita. `assets/github/` (`en/` e `pt-BR/`, mesma lista
  nas duas linguas) traz os arquivos de comunidade em `docs/` (`CONTRIBUTING.md`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `PULL_REQUEST_TEMPLATE.md`), `.github/ISSUE_TEMPLATE/`,
  `dependabot.yml`, `ci.yml` e `.gitattributes`. O partial
  `assets/partials/AGENTS-github-block.md` entra em `AGENTS.md` depois do ultimo bloco
  gerenciado e antes de "## Regras Do Projeto". Arquivo que ja existe no projeto e pulado e
  listado, nunca mesclado. A skill nao roda `gh` nem faz push, tag ou Release.
- Pergunta 5 da entrevista do scaffold ("Ativar a camada GitHub?"): nao, sim em `en` ou sim
  em `pt-BR`. "Avançar" ou silencio contam como nao responder, e a lingua nunca e inferida.
- `references/github.md`: ativacao em projeto existente, placeholders `{{SKILL_VERSION}}` e
  `{{QUALITY_COMMAND}}` do `ci.yml`, checklist de configuracao do repositorio pela CLI `gh`
  (descricao, topics, ruleset de `main`, labels) e o fluxo de bump, tag e Release.
- Validador: `GITHUB-MARCADOR-INVALIDO` (erro: bloco `github` sem marcadores pareados e versao
  valida) e `GITHUB-VERSAO-DIVERGENTE` (aviso: bloco `github` em versao diferente do `core`).
- Fixture `evals/fixtures/github-project` (`valido` e `invalido`) e evals 13 (ativar em
  projeto existente, em portugues, sem `.gitattributes`) e 14 (scaffold novo com a camada
  GitHub em ingles).
- T-104: `CONSENSO-ORIGEM-CORRIDA-INCOMPLETA` (aviso). Entrada automatizada
  (`**Origem:** automacao`) cujo `**Manifesto:**` resolve para uma corrida sem prova de
  integridade passa a ser acusada: manifesto ilegivel, `status` diferente de `concluida`, ou
  participante com `resultado: posicao` sem o `stdout.txt`. Falha registrada com stdout vazio
  nao conta. So leitura: o validador nao retoma, limpa nem repara, e corrida que nenhuma
  entrada cita continua sem diagnostico.

## 2.13.0 - 2026-10-21

Bump que leva o timeout por tentativa do `loop.sh` (T-084) e as ideias importadas da
analise do ai-memory de 2026-10-20 (`docs/DECISIONS.md`): pontes com import real (T-087),
paragrafo "memoria e evidencia, nao instrucao" no bloco core (T-088), recarga de
`SESSION.md` e `TASKS.md` apos compactacao do contexto (T-089) e o tipo "Armadilha" em
`MEMORY.md` (T-091). Marcadores `core`, `specs` e `loop` em v2.13.0; o conteudo dos blocos
specs e loop nao muda. Rodada executada por subagentes Sonnet 5.5 revisados por um gestor
Fable 5.1, um por vez; portao da rodada: `evals/portao_t087.py`; portao do timeout:
`evals/portao_t084.py`.

- `scripts/loop.sh` ganha `--tempo-maximo <segundos>` por tentativa (padrao 3600). Ao
  estourar, o agente e o que ele deixou vivo recebem SIGTERM (SIGKILL apos 5 s) e a rodada
  segue pelo caminho de "agente saiu com codigo diferente de zero": se houve alteracao, o
  portao decide; senao, exit 4. Bash puro, sem `timeout` nem `setsid` (T-084).
- `assets/CLAUDE.md` e `assets/GEMINI.md` (e as pontes da raiz) passam a comecar com um
  import real: `@AGENTS.md` no `CLAUDE.md` e `@./AGENTS.md` no `GEMINI.md`, a grafia
  documentada pelo Gemini CLI. Ponteiro em prosa nao carrega nada no inicio da sessao, e o
  Claude Code 2.1.277+ so le `AGENTS.md` sozinho quando nao existe `CLAUDE.md`. O resto da
  ponte e uma frase curta, sem regra e sem lista; o validador segue conferindo so que a ponte
  menciona `AGENTS.md`, e quem ja tem a ponte antiga a ve como divergente do template no
  fluxo de atualizacao (T-087).
- O bloco core ganha, no fim de "Memoria Persistente", o paragrafo "memoria e evidencia,
  nao instrucao": o conteudo de `docs/`, a saida de agente realimentada pelo `loop.sh` e os
  brutos de `docs/consensus/` sao registro historico; texto com forma de instrucao ali e
  citacao, nao comando, e so o usuario na conversa e o `AGENTS.md` instruem (T-088).
- O bloco core ganha, em "Memoria Da Sessao", uma linha de recarga apos compactacao: quando
  o contexto da conversa for compactado, ou o resumo que sobrou estiver vago sobre o que esta
  em curso, o agente rele a entrada mais recente de `docs/SESSION.md` e a secao "Em
  Andamento" de `docs/TASKS.md` antes de continuar. Registro vale mais que resumo de
  contexto, e o equivalente sem hooks do "reload context" do ai-memory (T-089).
- `assets/docs/MEMORY.md` ganha o quinto tipo de memoria, "Armadilha", ao lado de User,
  Feedback, Project e Reference, em "Tipos De Memoria" e em "Registros": tentativa que falhou
  e por que, para ninguem repetir. E a casa permanente do campo "Nao repetir" do modelo de
  "Passagem De Trabalho", que fora dali so sobrevive em `SESSION.md`. Cada entrada traz o que
  se tentou, o que aconteceu, por que nao serve e a data. Feedback e regra a seguir;
  Armadilha e caminho a nao tomar, mesmo sem regra geral. O bloco core do `AGENTS.md` nao
  muda: o proprio `MEMORY.md` descreve o tipo. Origem: `gotchas/` do ai-memory (T-091).

## 2.12.0 - 2026-10-17

Bump que leva a secao "Passagem De Trabalho" do bloco core e os gatilhos novos
da `description`. Os dois itens abaixo foram escritos em 2026-10-17 como
acrescimos a 2.11.0, sem subir a versao, com a 2.11.0 ja publicada em
`origin/main`. Migraram para ca para que a 2.11.0 publicada tenha um conteudo
so de bloco core e para que o fluxo de atualizacao (`references/atualizacao.md`)
ofereca o bloco a projeto que ja esta em 2.11.0 pelo caminho normal, sem
depender do ajuste do passo 2. Marcadores `core`, `specs` e `loop` em v2.12.0;
o conteudo dos blocos specs e loop nao muda. Fora o validador (T-078) e o
`scripts/consenso.py` (tres ultimos itens, T-079 a T-081), nenhum script distribuido mudou. Portao da tarefa de bloco core:
`evals/portao_t086.py` (T-086).

- `description` do `SKILL.md` deixa de disparar em pedido generico de criar
  projeto, pasta, repositorio ou scaffold ("cria projeto", "inicia projeto
  novo", "monta a base"). Dispara quando o pedido nomeia a estrutura
  multiagente ou seus arquivos, cita a skill, ou cai nos fluxos de atualizar,
  validar, specs e loop. Motivo: com um agente gestor coordenando subagentes,
  decidir se um projeto ganha a estrutura e de quem coordena, e a lista de
  frases genericas tirava essa decisao dele e disparava a skill dentro de
  tarefas de scaffold de codigo. A `description` e prompt, nao trava: baixa o
  disparo errado, nao o zera. Evals 2 e 4 ajustados e eval 11 negativo
  (projeto Vite nao aciona a skill); `agents/openai.yaml` segue com
  invocacao implicita, so o comentario mudou.
- Secao "Passagem De Trabalho" no bloco core de `AGENTS.md`: ao delegar uma
  tarefa a outro agente (subagente, outra sessao, outro modelo), o contexto
  viaja dentro da propria mensagem de delegacao, como resumo curto com
  objetivo e criterio de conclusao, estado feito e pendente, decisoes que
  valem e tentativas que nao se repetem, arquivos a consultar por caminho e
  a instrucao de conferir o estado real antes de agir. Nenhum arquivo novo:
  `docs/` segue como registro e o resumo aponta para ele. Motivo: no
  Cloudroom o subagente pode estar em outra sandbox, e arquivo temporario do
  gestor nao chega la. Metodo inspirado na skill Handoff (davidondrej), sem
  copia-la nem exigir a instalacao dela. O passo 2 de
  `references/atualizacao.md` deixa de encerrar em versao igual quando um
  bloco gerenciado difere do template: o diff do bloco e oferecido mesmo sem
  bump. Validador intocado: o resumo vive na mensagem, nao em arquivo.
- Marcador `**Origem:**` no validador (spec 0006, DEC-007, T-078). Entrada de
  `docs/CONSENSUS.md` que declara `**Origem:**` passa a ser conferida em
  quatro avisos novos: `CONSENSO-ORIGEM-SEM-MANIFESTO` e
  `CONSENSO-ORIGEM-MANIFESTO-QUEBRADO` (sem `**Manifesto:**`, ou caminho que
  nao resolve a partir da raiz), `CONSENSO-PARTICIPANTE-SEM-SECAO` (id em
  `**Participantes:**`, fora de `**Falhas:**`, sem `### Posicao De <id>`, ou
  sem `### Revalidacao De <id>` quando a entrada declara `**Achado:**`) e
  `CONSENSO-FALHA-SEM-SECAO` (id em `**Falhas:**` sem `### Falha De <id>`).
  As duas linhas sao listas separadas por virgula e `nenhuma` vale lista
  vazia. Entrada sem `**Origem:**` nao ganha diagnostico nenhum, nem com
  secoes `### Posicao De` soltas, e projeto que nunca usa a automacao nao
  ganha cobranca. Sao AVISO, entao so travam o exit code com `--strict`.
  Fixture `evals/fixtures/origem-project` (valido e invalido, com uma entrada
  manual de controle) em `FIXTURES`, com oracle exato. Motivo: a automacao do
  consenso escreve entrada sem humano na frente, e entrada malformada precisa
  ser pega antes de alguem ler o manifesto errado. Portao: `evals/portao_t078.py`.
- `consenso.py achado --entrada "<titulo>" --rodada N` (spec 0006, DEC-003 a
  DEC-007, T-079). Segundo pacote sobre o mesmo primitivo do `debate`: a
  execucao isolada (copia por participante, paralelo, bruto gravado ao
  terminar, varredura de segredo, lock, sinais) foi extraida para funcoes
  compartilhadas e os dois pacotes a chamam; o `debate` se comporta como
  antes. O achado revalida a disposicao de uma entrada que ja existe: a
  entrada-alvo vai na integra no prompt (o envelope diz que se avalia a
  disposicao, nao o achado) e `CONSENSUS.md` vai inteiro na copia. Os
  `--agente` se repetem, N maior ou igual a 1 vale, `--pergunta` e opcional,
  `--dono` e `--pendente` sao texto humano, e `--pendente` e obrigatorio da
  rodada 4 em diante (o script nunca inventa). A escrita e uma substituicao
  atomica do arquivo inteiro que troca Rodada (`N de N`), Exposicao previa
  (`sim`), Metodo e Proximo passo, insere ou acrescenta Origem, Manifesto,
  Participantes e Falhas logo apos a linha Rodada, e acrescenta
  `### Revalidacao De <id>` (em citacao) e `### Falha De <id>` antes de
  `### Decisao Para Registrar Em DECISIONS.md`, ou no fim da entrada. Status,
  Achado, Escapou de verificacao, as outras secoes e o resto do arquivo ficam
  byte a byte. Recusa com exit 1, sem tocar em nada: entrada inexistente ou
  repetida, entrada sem `**Achado:**` ou sem `**Rodada:**`, id que ja tem
  secao, rodada ausente ou menor que 1, rodada 4 sem `--pendente`. Sem
  nenhuma posicao sai 2 e a entrada fica intacta. Cada rodada ganha pasta
  propria em `docs/consensus/`, com sufixo `-2`, `-3` quando duas caem no mesmo
  segundo (antes duas rodadas no mesmo segundo falhavam). A bateria
  `test_consenso.py` passa de 33 para 60 verificacoes. O validador passa a ler
  `**Manifesto:**` como lista separada por virgula (crases toleradas), e cada
  caminho que nao resolve a partir da raiz gera um
  `CONSENSO-ORIGEM-MANIFESTO-QUEBRADO`; lista vazia segue sendo
  `CONSENSO-ORIGEM-SEM-MANIFESTO`. A fixture `origem-project` ganha um achado
  de duas rodadas com dois manifestos (valida) e um com um manifesto quebrado
  (invalida), com oracle. Assim a entrada da segunda rodada passa em
  `--strict`. Portao: `evals/portao_t079.py`.
- `consenso.py debate --rodada N --anterior <caminho>` (spec 0006, DEC-006,
  DEC-009, DEC-003, T-080). A rodada 2 em diante recebe as posicoes anteriores
  inteiras. `--anterior` se repete e aceita arquivo (entra verbatim, rotulado
  pelo nome) ou diretorio de rodada em `docs/consensus/` (entra todo
  `<id>/stdout.txt`, byte a byte, rotulado pelo id). As posicoes vao no fim do
  prompt, depois da pergunta, e o prompt segue como ultimo argumento do
  comando, grande que seja: nenhum corte, nenhum resumo, porque resumo ali
  devolve o problema 3 da spec (quem transcreve a critica e o criticado) por
  dentro da automacao. A operacao nunca deduz a rodada nem os anteriores:
  `--rodada` 2 ou mais sem `--anterior`, `--anterior` inexistente ou diretorio
  sem `<id>/stdout.txt`, rodada 4 ou mais sem `--pendente`, rodada nao
  numerica ou menor que 1, e `--anterior` ou `--pendente` na rodada 1 (que e
  cega) saem 1 sem chamar agente nem criar pasta. Padrao de segredo num
  anterior sai 6 antes de qualquer agente, como na pergunta. A entrada escreve
  `Exposicao previa a outras posicoes: sim`, `Rodada: N de N` e, quando ha
  `--pendente`, `Pendente da rodada anterior`. Na rodada 2 ou mais a copia
  leva `docs/CONSENSUS.md` inteiro, porque o publicado e anterior (DEC-009); a
  rodada 1 continua retendo os registros. As posicoes contemporaneas seguem
  fora pela mesma copia isolada. O manifesto ganha `anteriores`
  (`[{caminho, sha256}]`, lista vazia na rodada 1). Limite conhecido: no Linux
  um unico argumento de comando aceita cerca de 128KB; prompt maior que isso
  falha na execucao do agente (exit 127, registrado como falha dele), nunca
  e truncado. A bateria `test_consenso.py` passa de 63 para 79 verificacoes,
  com um anterior de 60KB e marca no fim. Portao: `evals/portao_t080.py`.
- `consenso.py retomar --projeto DIR <run-id>` (spec 0006, DEC-009, DEC-010,
  T-081). Continua uma rodada que nao chegou a `concluida` (interrompida,
  parada por segredo, sem posicao, recusada na escrita) sem repetir trabalho
  pago, e so por comando explicito: nenhuma mensagem executa a retomada, todas
  apenas citam `consenso.py retomar --projeto DIR <run-id>`. Quem tem
  `<id>/stdout.txt` fica como esta, sem nova chamada, falha inclusive; quem nao
  tem roda de novo em copia isolada e com a varredura de segredo de sempre. O
  material retido por segredo que a pessoa moveu a mao para `<run>/<id>/`
  passa a `resultado=posicao` (ou `falha`, se o exit original nao foi 0), com
  `aceito_por_humano` e o hash do bruto, sem varredura nova: a palavra humana
  ja foi dada. Se todos os brutos estao presentes, so escreve a minuta. Vale
  para debate (rodada 1 e rodada N, com o prompt refeito a partir dos
  `anteriores` do manifesto, hash conferido) e para achado (a minuta e a
  reescrita da entrada). Recusa com exit 1: run inexistente, run
  `concluida`, manifesto de rodada anterior a esta versao (sem os parametros),
  pergunta, entrada ou anterior diferentes do hash gravado. Lock ocupado sai
  5; padrao de segredo na pergunta, na entrada ou num anterior sai 6. O lock
  vem antes das demais recusas. Cada retomada entra em `retomadas` (instante,
  chamados, mantidos, aceitos a mao) e o manifesto e selado como nas outras
  rodadas. Para isso o manifesto passou a guardar `agentes` (id e comando),
  `titulo`, `dono` e `pendente`, e o `rotulo` de cada anterior quando difere
  do nome do arquivo. Mudou no que ja existia: participante morto pelo
  nosso SIGINT ou SIGTERM deixa de ser registrado como falha com
  `stdout.txt` vazio (o que a retomada trataria como bruto pago); fica sem
  registro e sem arquivo, e a retomada o chama. As mensagens de interrupcao,
  de lock ocupado (cita o run-id da rodada nao concluida mais recente) e de
  exit 6 citam o comando de retomada com o run-id. O fim de `debate` e de
  `achado` virou `fechar_debate` e `fechar_achado`, compartilhados com a
  retomada. A bateria `test_consenso.py` passa de 79 para 95 verificacoes.
  Portao: `evals/portao_t081.py`.
- Documentacao da automacao do consenso (spec 0006, T-082). Arquivo novo
  `references/consenso.md`, no molde de `loop.md`: uso e flags dos tres
  subcomandos, tabela de comandos somente-leitura por ferramenta (`codex exec
  -s read-only --skip-git-repo-check`, `cursor-agent -p --mode ask --force`,
  com a nota de que a copia isolada torna a escrita inofensiva mas a leitura e
  o que vale), exit codes 0, 1, 2, 5 e 6 (interrupcao por SIGINT ou SIGTERM
  sai 1 com `status=interrompida`), sidecar `docs/consensus/`, forma da
  entrada com `**Origem:**`, `**Manifesto:**`, `**Participantes:**` e
  `**Falhas:**`, rodada 2 e achado, retomada, a secao "O Que A Operacao Nunca
  Faz" (sintetizar, declarar convergencia, decidir por maioria, escrever
  julgamento, redigir segredo, retomar sozinha) e os limites declarados: a
  varredura de segredo tem falso negativo (DEC-010), nao ha teto de custo e
  `MEMORY.md` desatualizado dispara o revisor errado. O `SKILL.md` ganha a
  secao "Rodar Uma Rodada De Consenso" (confirmar a pergunta em arquivo,
  montar cada `--agente` a partir dos perfis de consenso em `docs/MEMORY.md`,
  mostrar o comando, traduzir o exit code, lembrar que o julgamento e da
  pessoa) e frases de gatilho na `description`. O template `CONSENSUS.md`
  ganha a secao "Entrada Automatizada", fora dos modelos cercados, que nao
  mudam. `verificar_convencoes` passa a cobrar `**Origem:**` no template e na
  raiz. O README cita `consenso.py` e o eval 12 roda uma rodada. Bloco core
  intocado, versao mantida em 2.12.0. Portao: `evals/portao_t082.py`.

## 2.11.0 - 2026-09-04

Orquestrador mecanico de consenso: `scripts/consenso.py debate` roda N agentes
em paralelo, cada um numa copia temporaria do projeto sem `docs/consensus/`.
O bruto e o manifesto entram em `docs/consensus/<run-id>/` assim que cada
agente termina. Independencia deixa de ser declaracao e vira propriedade da
execucao.

- `evals/test_consenso.py` cobre o primitivo com agente falso.
- `verify_repository.py` passa a compilar `consenso.py` e a exigir a bateria
  com piso 32.
- Lock exclusivo `.consenso-lock` (diretorio atomico) na abertura; segunda
  execucao simultanea sai 5 e ensina a limpar um orfao. SIGINT e SIGTERM
  encerram os agentes, marcam `status=interrompida` e soltam o lock.
- Minuta de debate no fim de `CONSENSUS.md`, uma vez so, por temporario no
  mesmo diretorio, `fsync` e `os.replace`. Posicoes em citacao linha a linha;
  U+2014 vira hifen so na minuta; julgamento em branco. O manifesto ganha
  `minuta` e so entao `status=concluida`.
- `verify_repository.py` ignora travessao em bruto sob `docs/consensus/`.
- Varredura de padroes de segredo antes de gravar bruto: chave AWS, PEM,
  rotulo com valor, prefixos `ghp_` / `sk-` / `xox` e URL com senha. Achou:
  material fora do projeto, manifesto sem o conteudo, `status=parada-segredo`,
  exit 6, nenhuma minuta. Palavras soltas sem valor nao disparam, e os
  prefixos exigem inicio de palavra e comprimento minimo: `sk-` solto casava
  `task-force`.

## 2.10.0 - 2026-09-04

`validate_structure.py` passa a avisar `**Rodada:**` ausente, pelo mesmo
codigo `CONSENSO-CAMPO-AUSENTE` dos outros campos declarativos. A cobranca
continua limitada a entradas posteriores a data de adocao, sem criar aviso em
projeto que ainda nao adotou essa convencao. O formato agora exige a linha
inteira: `1 de 1` seguido de texto nao passa como rodada valida.

- A projecao `--progress` conta como pergunta aberta apenas bullet de primeiro
  nivel em "Perguntas Abertas". Sub-itens indentados sao contexto da pergunta,
  nao perguntas adicionais.
- `loop.sh` agora usa `.loop-lock`, criado atomicamente por projeto. Uma segunda
  rodada simultanea sai com codigo 5 sem tocar em `TASKS.md`; o lock e removido
  na saida e a mensagem ensina como limpar um orfao depois de confirmar que nao
  ha rodada ativa.

## 2.9.1 - 2026-09-04

O fluxo de atualizacao esclarece que secoes resgatadas de um `AGENTS.md` v1
viram itens ou subsecoes dentro de "## Regras Do Projeto", nunca uma secao
irma. Na migracao de `TASKS.md`, linha concluida recebe data quando ela for
conhecida; sem data, a linha nao e cobrada pela convencao de evidencia.

- `install.sh` (nao distribuido) deixa de sobrescrever destino divergente em
  silencio: compara o que distribui, lista `faltando`, `diferente` e `extra`,
  pede confirmacao `[s/N]`, recusa sem terminal e aceita `--sim` para
  automacao. Arquivo extra no destino nao e apagado. O verificador prova os
  dois lados em destino temporario sujo.

## 2.9.0 - 2026-09-04

O validador passa a diagnosticar arquivo Markdown fora de UTF-8 sem traceback,
reconhece cercas `~~~` e headings ATX com fechamento, e deixa de aceitar
referencia de spec com `NNNN` no meio ou Status de spec no corpo da prosa.
Leitura de campos declarativos tambem recusa rotulo malformado sem derrubar a
validacao. As fixtures com oracle exato cobrem cada correcao.

- Templates de `QUALITY.md`, `PROMPTS.md`, `ONBOARDING.md`, `README.md`,
  `SESSION.md`, `TASKS.md`, `ARCHITECTURE.md` e `GLOSSARY.md` passam a refletir
  as regras atuais do bloco core. O verificador cobre os templates que citam
  essas convencoes. No bloco core, o item `docs/ARCHITECTURE.md` da leitura
  relevante ganhou "quando existir": o nivel minimal nao cria o arquivo.

## 2.8.1 - 2026-09-04

Correcoes no modulo de loop sem mudar o bloco core. O loop passa a conservar a
linha da tarefa capturada no arranque e recusa fecha-la se ela mudar; preserva
sub-linhas ao fechar ou bloquear; le saidas invalidas com substituicao; limita a
realimentacao da falha aos ultimos 64KB (antes ia inteira para o argumento da
CLI e estourava o limite do sistema); registra pergunta vazia como `(vazia)`;
preserva o modo de `TASKS.md`; nao cria bytecode ao consultar o helper; fecha o
stdin do agente; orienta que a propagacao de bloco cabe ao agente de chat; e
documenta o exit code 4. Em modo seco, a evidencia tambem nao atribui agente.

## 2.8.0 - 2026-09-04

Comando de `(verifica:)` com parenteses deixa de parecer tarefa sem portao: o
validador acusa ERRO e o `loop_task.py check` recusa antes de chamar o agente.
O formato nao suporta parenteses no comando, portanto a orientacao e usar um
script auxiliar no projeto, por exemplo `bash portao.sh`. O bloco core, o
template de `TASKS.md` e a referencia do loop passaram a declarar a limitacao.

- **Texto do bloco core**: a regra do travessao agora declara que o validador
  cobre `AGENTS.md`, as pontes e `docs/**/*.md`; a regra das pontes tambem
  esclarece que o script confere somente a mencao a `AGENTS.md`, e que o
  restante continua sendo regra de leitura.

## 2.7.0 - 2026-09-04

Avisos que ja eram promessas da estrutura agora sao diagnosticados pelo
`validate_structure.py`: formato incompleto de evidencia, tarefa aguardando sem
Resposta ou marcador bloqueada, exposicao `nao` da rodada 2 em diante, proximo
passo vazio em consenso aberto, cerca ``` sem fechamento, spec concluida sem
evidencia, status de tarefa dentro de spec, ID proprio fora de `T-NNN`, marcador
bloqueada fora de Aguardando Usuario e data de adocao invalida. Cada codigo tem
fixture com oracle exato, e os tres marcadores dos blocos gerenciados sobem para
v2.7.0.

## 2.6.0 - 2026-09-04

Seis contradicoes estruturais que passavam limpas agora sao ERRO no
`validate_structure.py`: tarefa em Concluidas sem data, marcador verifica vazio,
marcadores em ordem invertida, bloco loop invalido, arquivo do nucleo vazio e ID
repetido entre `TASKS.md` vivo e `docs/archive/TASKS-*.md`. Cada diagnostico tem
fixture com oracle exato no verificador do repositorio. Os tres marcadores dos
blocos gerenciados sobem juntos para v2.6.0.

- **Mudanca de comportamento no marcador verifica**: a regex passou a exigir que ele esteja no fim da linha, seguido no maximo de outros marcadores entre parenteses, como o bloco core sempre disse. Consequencias: mencao em prosa como "o `(verifica: )` vazio" deixa de ser lida como declaracao (era falso positivo do check novo `VERIFICA-COMANDO-VAZIO` na propria raiz deste repositorio); e comando com parenteses, que antes era truncado no primeiro `)` e executado assim pelo loop (REVAL-3), agora simplesmente nao casa, entao o `loop_task.py check` recusa a tarefa como "nao declarou verifica". O diagnostico explicito para esse caso segue em T-072.
- Fechada pelo modulo de loop com Codex `gpt-5.6-terra`, contra portao proprio (`evals/portao_t069.py`), depois de o agente parar na rodada 1 para perguntar sobre a propagacao ao `AGENTS.md` da raiz, que o prompt do loop proibe e o agente de chat fez por script.

## 2.5.1 - 2026-09-03

Conserto de seguranca de dado, nao feature. Achado pelo Grok numa rodada de consenso sobre a spec 0006, e conferido no codigo antes de aceito.

- **`loop_task.py` grava `docs/TASKS.md` por substituicao atomica.** Antes usava `write_text` direto, que trunca o arquivo antes de escrever: crash, disco cheio ou processo morto no meio deixavam partido o backlog vivo do projeto. Agora e temporario no mesmo diretorio, `fsync`, e `os.replace`. O pior caso passou a ser um temporario orfao, que nao destroi nada.
- Regressao provada por mutacao, e nao por leitura: com o `write_text` de volta, o caso novo acusa arquivo truncado. `evals/test_loop.py` foi de 55 para 58 verificacoes.
- Marcadores dos tres blocos em v2.5.1. O conteudo do bloco core nao mudou; eles sobem juntos por DEC-009, para o marcador continuar dizendo qual versao da skill escreveu o bloco.

## 2.5.0 - 2026-09-03

Portao que so olha exit code nao prova nada. Esta versao troca isso por diagnostico com identidade. Veio da revalidacao do achado `0005-A1` pelo Codex, registrada em `docs/CONSENSUS.md` do repositorio-fonte.

- **Identificador estavel por diagnostico.** Os 39 diagnosticos de `validate_structure.py` ganharam codigo (`ACHADO-SEM-ESCAPOU`, `TASK-ID-DUPLICADO`, `SPEC-STATUS-INVALIDO`, e assim por diante). O codigo e **contrato publico**: a redacao da mensagem pode melhorar quando quiser, o codigo so muda em mudanca de versao. Quem monta portao em cima do validador casa codigo, nunca fragmento de texto.
- **Flag `--codigos`**: uma linha por diagnostico, `NIVEL|CODIGO|ARQUIVO|SUJEITO`, sem prosa. O `SUJEITO` e a tarefa, a entrada de consenso ou a spec de que o diagnostico fala, e e ele que denuncia aviso que passou a cair na entrada errada.
- O relatorio humano passa a mostrar o codigo entre colchetes: `[AVISO] [ACHADO-SEM-ESCAPOU] ...`. `Report.add` recusa codigo que nao esteja declarado em `CODIGOS`, entao diagnostico sem identidade quebra na hora de escrever, e nao em producao.
- **Oracle por fixture no `verify_repository.py`** (so no repositorio-fonte). O `FIXTURES` deixou de mapear nome para exit code e passou a declarar modo, exit esperado e o **conjunto exato** de diagnosticos. Diagnostico a mais reprova tanto quanto diagnostico a menos, e fixture sem oracle declarado e recusada em vez de virar aprovacao silenciosa. `verificar_achado` foi absorvida por esse mecanismo: um mecanismo, nao dois.
- Fixture `evals/fixtures/debate-project`: projeto que usa consenso e nunca registra achado, com conjunto de diagnosticos **vazio** em `--strict`. Conjunto vazio nao e teste fraco quando a comparacao e nos dois sentidos. Ela cobre o que `achado-project` nao consegue cobrir, porque la os dois lados tem achado. Medido por mutacao: quebrando `strip_fences`, so esta fixture acusa. Muda apenas `evals/`, que o `install.sh` nao propaga; nao exige reinstalacao.
- Efeito medido por mutacao: com a contagem de linhas antiga, uma regressao compensada (um aviso certo some, outro errado aparece, total igual) passava verde. Com o conjunto exato, ela reprova nomeando o que sumiu e o que sobrou. Aviso que muda de entrada, mesmo com codigo e contagem identicos, tambem reprova.

## 2.4.0 - 2026-09-03

`CONSENSUS.md` deixa de servir so para debate e passa a registrar **achado**, que e o que o uso real produziu. Desenho e decisoes na spec `docs/specs/0005-consenso-para-achados.md` do repositorio-fonte.

- **Formato de achado** no bloco core e no template de `CONSENSUS.md`. Entrada que declara `**Achado:** <identificador>` e tratada como achado, com `Status` e `Proximo passo` proprios, disposicao de quem registrou e revalidacao por outro modelo. O identificador e livre, amarrado a unidade de trabalho do projeto: o validador confere que o campo existe e tem valor, e nunca opina sobre o valor.
- **`**Escapou de verificacao:** sim | nao`** no achado, e a secao `Por Que Nada Pegou Antes` obrigatoria quando a declaracao for `sim`, com o que passou verde e o mecanismo do ponto cego. E o que transforma defeito escapado em conserto de portao, em vez de anedota.
- **O teto de tres rodadas saiu.** Ele foi escrito sem evidencia, e o uso real chegou a sete revalidacoes numa unidade so sem que isso fosse fracasso. No lugar dele, da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`, dizendo o que a anterior deixou em aberto. O proposito original, evitar rodada por cerimonia, sobrevive na exigencia de justificar a continuidade.
- **Aviso do ponto cego da validacao cruzada no bloco core**, em duas linhas: rodada verde e ausencia de objecao, nao prova de que funciona. Antes ele so existia em `references/loop.md`, que quem usa consenso sem usar loop nunca le.
- `validate_structure.py`: checks novos do formato de achado, todos AVISO e todos opt-in. A entrada opta pelo formato ao declarar `**Achado:**`, entao projeto que nunca registra achado nao recebe nenhuma cobranca nova, e entrada de debate segue valendo como esta. A regra de rodada trocou de dono: acima de tres, o que se cobra deixou de ser `**Proximo passo:**` e passou a ser `**Pendente da rodada anterior:**`.
- Fixture `evals/fixtures/achado-project`, com par valido e invalido. A primeira entrada dos dois e a mesma entrada de debate, de proposito: e o controle que prova que nenhum aviso novo encosta em quem nao declarou achado. Como os checks sao AVISO, a fixture roda em `--strict`, senao os dois casos sairiam 0 e nao provariam nada.
- Marcadores dos tres blocos gerenciados atualizados para v2.4.0.

## 2.3.0 - 2026-09-02

Modulo de loop: a estrutura passa a poder executar uma tarefa verificavel, nao so descreve-la. Desenho e decisoes na spec `docs/specs/0004-modulo-de-loop.md` do repositorio-fonte.

- **Modulo opcional de loop**, no padrao do modulo de specs: `references/loop.md`, `assets/partials/AGENTS-loop-block.md` e marcadores `ai-project-structure:loop:start|end`. Ativado so a pedido explicito, nunca no scaffold.
- **Portao de ativacao**: a secao "Testes E Validacao" de `QUALITY.md` do projeto-alvo precisa ter comando executavel. Vazia ou com o texto do template, a ativacao e recusada.
- **Limite do que a automacao escreve**: o loop fecha tarefa apenas quando ela declarou `(verifica: <comando>)` e o comando saiu 0, colando a saida real como `Evidencia: tipo=comando`. Nunca escreve `tipo=revisao-manual` nem `tipo=conferencia`, e nao toca `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` nem specs. Excecao unica: falta de contexto move a tarefa para `Aguardando Usuario` com a pergunta escrita.
- `scripts/loop.sh`: orquestra uma rodada. Uma tarefa, ate 3 tentativas, com a saida do portao voltando como contexto da tentativa seguinte. Exit codes distintos por caminho (0 fechou, 1 nao elegivel, 2 portao falhou, 3 aguardando usuario).
- `scripts/loop_task.py`: toda edicao de `TASKS.md` passa por aqui, reusando o parser do `validate_structure.py`. Um parser so no projeto, em vez de dois divergindo.
- Protocolo de falta de contexto por arquivo (`.loop-pergunta`), nao por linha sentinela no stdout: cada ferramenta formata saida de um jeito, e arquivo existe ou nao existe.
- `evals/test_loop.py`: 47 verificacoes do modulo com agente falso, sem nenhuma chamada de modelo. Roda em segundos e entrou no `verify_repository.py`, que passou a conferir tambem o bloco `loop`, o bit de execucao do `loop.sh` e se os tres scripts distribuidos compilam.
- Exit 4 novo: agente que sai com codigo diferente de zero e nao altera nenhum arquivo encerra a rodada na hora, em vez de queimar as tentativas restantes. Veio de bancada real, onde duas ferramentas mal configuradas fizeram o loop insistir tres vezes e reportar "portao falhou" quando o problema era o comando de `--agente`.
- `references/loop.md` ganhou a tabela de comandos por ferramenta (Claude, Codex, Gemini e Grok), as duas armadilhas que custam uma rodada (`--skip-git-repo-check` no Codex fora de repo git, `--skip-trust` no Gemini) e a secao "A Evidencia Vale O Que O Portao Vale".
- A evidencia escrita pelo loop passa a registrar `agente=<comando>`: quem fechou a tarefa, nao so que o portao passou.
- Chamada assistida: `SKILL.md` ganhou "Rodar Uma Tarefa Com O Loop". O usuario pede em linguagem natural e o agente do chat monta o comando, lendo os perfis por intencao e ferramenta que ficam em `docs/MEMORY.md`, secao `## User`. Nome de modelo e flag de esforco nunca entram na skill: eles envelhecem, e a memoria do projeto e o lugar deles.
- Revisao item a item do bloco, com o criterio da DEC-018: regra vai para o prompt quando a violacao dela deixa o portao verde do mesmo jeito. Achou um buraco: nada impedia o agente de editar `AGENTS.md`, `SESSION.md`, `MEMORY.md`, `DECISIONS.md` ou specs, e o pior caso e afrouxar em `AGENTS.md` a regra que o restringe. Entrou no prompt. O que ficou so no bloco, e por que, esta documentado em `references/loop.md`.
- A restricao "nao apague o que falha" entrou **no prompt** do `loop.sh`, e nao so no bloco. Bancada mostrou que um modelo mais barato ignorava a regra quando ela vivia so no `AGENTS.md`, e passou a obedecer quando ela chegou pelo prompt. Regra cuja violacao passa despercebida no portao nao pode morar so no bloco.
- Mensagem do exit 4 deixou de acusar causa errada: antes afirmava que o comando de `--agente` estava incompleto, e numa bancada a causa real foi cota do plano da ferramenta. Agora aponta a saida do agente e lista as duas causas comuns.
- Regra nova no bloco de loop, vinda de bancada com projeto de conteudo: **nao apague o que falha**. O portao mede o que sobrou, entao remover o teste, a secao ou o link que falha sempre deixa o portao verde. Quando a saida obvia for perder conteudo ou cobertura, o agente para e pergunta pelo `.loop-pergunta`, porque perder informacao e decisao do usuario e o verde fica igual nos dois casos.
- A escolha de degrau deixou de estimar dificuldade lendo a tarefa. Sobra o que se sustenta em evidencia: rodada anterior falhou, duas falharam, ou o usuario disse que e dificil.
- Regra explicita para escada desigual: degrau que nao existe na ferramenta escolhida nao vira degrau parecido em silencio. Duas saidas valem, uma nao. Vale usar o teto da ferramenta quando o usuario ja decidiu isso e esta escrito no perfil, avisando que e o teto; vale dizer qual e o teto e oferecer trocar de ferramenta. Nao vale escolher o degrau parecido sem falar nada: o usuario acharia que pediu esforco maximo e recebeu outra coisa.
- Perfis de execucao podem ter degraus de esforco (`executar`, `executar-dificil`, `executar-muito-dificil`). `references/loop.md` ganhou "Escolher O Nivel De Esforco": comeca sempre no degrau base e sobe so por sinal declarado, dizendo qual foi. Escalada por fracasso de rodada anterior, por pedido do usuario, ou por tarefa que mexe em varias partes com regra de borda. Explicitamente **nao** sao sinais: portao ser suite, tarefa pertencer a spec, ou descricao longa, porque disparam em quase todo trabalho real e nao separam nada.
- `references/loop.md` ganhou "Configurar Os Perfis": fluxo conversacional para ver, trocar e criar perfil, com a regra de confirmar nome de modelo e nivel na propria CLI antes de gravar.
- Marcadores dos tres blocos gerenciados atualizados para v2.3.0. Eles andam juntos mesmo quando o conteudo de um bloco nao muda, porque o marcador diz qual versao da skill escreveu aquele bloco.

## 2.2.0 - 2026-09-02

Tarefa concluida deixa de ser afirmacao em prosa: passa a carregar evidencia. Espera por resposta do usuario ganha lugar proprio. Consenso passa a declarar como foi produzido. Ver a spec `docs/specs/0003-tasks-verificaveis.md` do repositorio-fonte.

- **Evidencia de fechamento obrigatoria** em toda tarefa movida para "Concluidas", como sub-linha `Evidencia: tipo=; procedimento=; resultado=`. `tipo` aceita `comando`, `revisao-manual` ou `conferencia`, para que tarefa de conteudo ou de decisao nao precise inventar comando.
- **Marcador `(verifica: <comando>)` opcional** em tarefa aberta. Declarado, vira contrato: concluir sem registrar o resultado daquele comando e ERRO no validador.
- **Nao retroativo.** A data de adocao fica declarada no proprio `TASKS.md`, no marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)`. Sem o marcador, nada e cobrado; linha concluida antes da data fica como esta. Projeto que atualiza nao tem historico transformado em alegacao sem evidencia.
- **Secao `## Aguardando Usuario`** no template de `TASKS.md`, com `**Pergunta:**`, `**Resposta:**` e `(bloqueada: AAAA-MM-DD)`. A regra "Nunca Inferir" do bloco core agora aponta para ela: pergunta que trava a tarefa tem destino, em vez de virar inferencia. Sem rotacao; aviso quando passa de 30 dias.
- **Consenso declarado**: `**Metodo:**`, `**Exposicao previa a outras posicoes:**` e `**Rodada:** N de 3` no template de `CONSENSUS.md` e no bloco core, com regra de rodada 1 cega e teto de 3 rodadas antes de escalar para o usuario. Os campos sao autodeclarados: o validador checa presenca e valor, nunca veracidade.
- `validate_structure.py`: checks novos de evidencia, `(verifica:)` sem resultado, `Aguardando Usuario` sem pergunta, valor desconhecido em marcador conhecido, idade do bloqueio e campos de consenso. `--progress` passa a contar a secao nova.
- `evals/verify_repository.py` (so no repositorio-fonte): prova em um comando a integridade do meta-projeto (raiz em `--strict`, fixtures, paridade dos blocos gerenciados e das pontes, convencoes nos templates e no dogfood, coerencia de versao, `evals.json`, ausencia de travessao e paridade dos tres destinos com `install.sh` em pasta temporaria).
- Fixture nova `evals/fixtures/aguardando-project` (caso valido exit 0, caso invalido exit 1) e eval 9 correspondente.
- Correcao achada no dogfood do mesmo dia: o validador tratava **qualquer** `T-NNN` da linha como ID da tarefa, entao uma tarefa que cita outra ("continuando o que sobrou de T-001") era acusada de ID duplicado, e uma linha concluida que mencionasse outro ID marcava esse outro como concluido, o que podia dar spec "Concluida" por engano. Agora vale o ID que abre a linha, depois da data quando ela e concluida; o resto do texto e referencia. A fixture `aguardando-project` guarda a correcao.
- Marcadores dos blocos gerenciados atualizados para v2.2.0.

## 2.1.0 - 2026-08-20

- Novo template opcional `docs/STACK.md`: mapa de tecnologias, pacotes principais e links de documentacao oficial, com secao "Onde Consultar Primeiro" para o agente ir direto na fonte certa (inspirado no STACK.md/PACKAGES.md do specsfy).
- `AGENTS.md` (bloco core): STACK.md em "Onde Escrever Cada Coisa" e gatilho novo em "Atualizacao Por Gatilho" (mudou tecnologia ou pacote, atualize STACK.md).
- `validate_structure.py --progress`: projecao somente-leitura de tarefas e specs (contagem por secao, status por spec, tarefas concluidas/total, perguntas abertas). Nunca edita nada (licao do specsfy-progress).
- Marcadores dos blocos gerenciados atualizados para v2.1.0.

## 2.0.0 - 2026-08-20

Inspirada na analise da skill/metodologia `specsfy` (github.com/promovaweb/specsfy), adaptando o que serve ao nosso contexto de memoria multiagente e descartando a cerimonia pesada (coverage math, attestation, pipeline multi-skill, CLI).

- Entrevista numerada com opcoes numeradas no scaffold; "Avançar" adia e registra pendencia, nunca autoriza inferencia.
- Regra "Nunca Inferir" no template `AGENTS.md`.
- `TASKS.md` com IDs `T-NNN`, prioridade opcional e link `(spec: NNNN-slug)`.
- Blocos gerenciados em `AGENTS.md` (`ai-project-structure:core` e `:specs`) + fluxo de atualizacao v1→v2 em `references/atualizacao.md`.
- Validador `scripts/validate_structure.py` (Python 3, stdlib, exit code).
- Modulo opcional de specs em `docs/specs/` (flat, `NNNN-slug.md`, status no arquivo, anti-drift: status de tarefa so em `TASKS.md`). Fluxos em `references/specs.md`.
- Campo `version` no frontmatter do `SKILL.md`; versao tambem gravada nos marcadores do projeto-alvo.
- `install.sh` passa a copiar `scripts/` e `references/`.
- Regra de escrita no template `AGENTS.md`: travessao (em dash, U+2014) proibido em textos do projeto; o validador acusa qualquer ocorrencia como erro.
- Correcao: `assets/docs/README.md` separava errado nucleo e opcionais (ARCHITECTURE e PROMPTS listados como nucleo).
- Correcao no mesmo dia, apos a rodada de validacao: o `expected_output` do eval 4 nao dizia o que esperar do validador depois da entrevista, e ferramentas diferentes leram o cenario de formas diferentes (uma parou na entrevista e viu exit 1 por diretorio vazio, outra respondeu e viu exit 0). Ambas estavam certas. O texto agora explicita que o criterio do eval e o comportamento da entrevista, que exit 1 em diretorio vazio nao reprova, e como exercitar o ramo "Avançar" ate exit 0. Muda apenas `evals/`, que o `install.sh` nao propaga; nao exige reinstalacao.

Ponto de atencao para versoes futuras: a instrucao sobre specs vive em dois lugares com papeis distintos - bloco `specs` em `AGENTS.md` (regra) e `docs/specs/README.md` (modelo). Atualizacoes precisam manter os dois coerentes.

## 1.x - ate 2026-05-26

- 2026-04-25: estrutura criada e refinada (MEMORY.md, archive/, reescrita do AGENTS.md).
- 2026-05-26: empacotamento como skill instalavel cross-tool (Agent Skills Open Standard), `install.sh`, `README.md`, `agents/openai.yaml`; instalacao verificada em Claude Code, Codex CLI e Gemini CLI.

Historico detalhado do projeto em `../../CHANGELOG.md` (docs/CHANGELOG.md do repositorio).
