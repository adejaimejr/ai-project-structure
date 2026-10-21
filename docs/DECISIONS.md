# DECISIONS

Registro de decisoes importantes do projeto.

## Modelo

```md
## AAAA-MM-DD - Titulo da decisao

### Decisao

- 

### Motivo

- 

### Impacto

- 
```

## 2026-10-21 - Validador avisa corrida incompleta so quando uma entrada de CONSENSUS.md aponta para ela

### Decisao

- `validate_structure.py` emite AVISO de proveniencia incompleta quando uma entrada com `**Origem:** automacao` aponta, pelo `**Manifesto:**`, para manifesto ilegivel, com status diferente de `concluida`, ou com participante registrado sem `stdout.txt`. Stdout vazio por falha registrada no manifesto nao conta como ausente.
- Corrida em `docs/consensus/` sem entrada que aponte para ela nao gera diagnostico. O validador nao retoma, nao limpa lock e nao repara.

### Motivo

- Consenso da T-083, segunda rodada 1 cega (`docs/CONSENSUS.md`), com Codex e Codex Sol convergindo sem se ver; ratificado pelo usuario no chat. A DEC-009 da spec 0006 faz de corrida incompleta um estado previsto, entao avisar sempre daria falso positivo em rodada legitima; ignorar sempre deixaria entrada publicada apontar para prova incompleta.

### Impacto

- T-104, codigo em `scripts/`, entra no proximo bump da skill. Validacao no meio de uma rodada pode ver o aviso por um instante (janela entre minuta e manifesto); validar de novo resolve.

## 2026-10-21 - O adaptador Cloudroom nao entra no consenso enquanto o Cloudroom nao isolar um filho por pasta

### Decisao

- `scripts/cloudroom_agente.py` (spec 0008) serve so como `--agente` do `loop.sh`, e so quando o `--projeto` e a pasta da thread do Cloudroom. Nenhum perfil de consenso aponta para ele; `consenso.py` continua chamando as CLIs direto, cada uma na propria copia (spec 0006, DEC-003).
- Reabrir exige spec propria e um recurso novo do Cloudroom: pasta isolada por filho, sem acesso ao projeto pai, com a resposta legivel por programa.

### Motivo

- Medido na CLI real em 2026-10-21: com `--shared-sandbox` o filho roda na pasta da thread pai e o `spawn` nao tem opcao de diretorio, entao a copia por participante sobreviveria so como pedido no prompt, e o filho alcancaria o bruto do outro participante. Sem `--shared-sandbox` a resposta nao e legivel por `thread output`.
- Rodada 1 cega com Codex `gpt-6-luna` e `gpt-5.6-terra` (`docs/CONSENSUS.md`, entrada "Spec 0008, P-2 e P-3"): os dois concordaram, sem se ver, e ratificacao do usuario no mesmo dia.

### Impacto

- Consenso segue invisivel na barra do Cloudroom; o loop ganha visibilidade.
- `references/consenso.md` e `references/cloudroom.md` dizem isso (T-102), e o portao de T-102 cobra.

## 2026-10-20 - Camada GitHub do repositorio: raiz com `.github/`, ingles por padrao, tag e release a cada bump

### Decisao

- A regra de raiz minima (2026-04-25) ganha uma segunda excecao, alem de `README.md`, `LICENSE` e `.gitignore`: arquivos e diretorios de configuracao com ponto (`.github/`, `.gitattributes`) sao permitidos na raiz, e `README.pt-BR.md` acompanha o `README.md`. Arquivos de comunidade (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `PULL_REQUEST_TEMPLATE.md`) ficam em `docs/`, onde o GitHub tambem os reconhece; so templates de issue, `dependabot.yml` e workflows exigem `.github/`. Qualquer outro diretorio na raiz (`.cursor/`, `scripts/`) continua proibido.
- A camada GitHub do repositorio (README da raiz, CONTRIBUTING, SECURITY, codigo de conduta, templates de issue e PR, workflows, corpo de release, descricao e topics) e escrita em ingles por padrao, com versao em portugues como opcao (`README.pt-BR.md`). `AGENTS.md`, a memoria em `docs/`, a skill e tudo o que ela gera continuam em pt-BR. A proibicao do travessao vale igual nos arquivos em ingles.
- Todo bump da skill termina em tag anotada `vX.Y.Z` no commit do bump e em GitHub Release; a tag e consequencia do `version:` do `SKILL.md`, nunca uma versao paralela. As versoes 2.4.0 a 2.11.0, publicadas sem tag, recebem tags retroativas nos commits de bump; Release so da 2.12.0 em diante.
- Mudanca na skill (qualquer arquivo em `docs/skills/ai-project-structure/` fora de `evals/`) entra em `main` por pull request, para o CI rodar os dois portoes em Linux e macOS antes do merge. Mudanca so em `docs/` da raiz pode ir direta em `main`. `main` nao aceita force push nem delecao.
- As praticas acima entram agora em "Regras Do Projeto" de `AGENTS.md` e, na skill 2.14.0, viram o modulo opcional `github` (bloco gerenciado, assets em ingles e pt-BR, `references/github.md`), para projeto novo nascer com isso. Spec 0007.

### Motivo

- Comparacao com `github.com/akitaonrails/ai-memory` em 2026-10-20: este repositorio tinha 12 versoes minor no CHANGELOG da skill e nenhuma tag, nenhum workflow, descricao e topics vazios, health de comunidade em 28% e um PR de 4 linhas aberto ha 45 dias. Nada disso e defeito da estrutura; e ausencia da camada que o GitHub exibe primeiro.
- Os dois portoes (`verify_repository.py` 74/74 e `validate_structure.py . --strict`) so rodavam na maquina do mantenedor, em macOS. O PR #1 mostrou que no Linux o harness falha por `sed -i ""` e `find -newer`; um CI em `ubuntu-latest` teria pego isso em setembro.
- Ingles na camada GitHub e o que da alcance a um projeto publico; manter pt-BR dentro (regras, memoria, skill) preserva o publico atual e as decisoes anteriores sem traduzir a skill inteira.
- Raiz minima continua valendo no espirito: `.github/` e configuracao, nao conteudo, e `docs/` ja e o lugar do que se le.

### Impacto

- `docs/PROJECT_CONTEXT.md` (idioma), `AGENTS.md` ("Regras Do Projeto"), `docs/ROADMAP.md` e `docs/QUALITY.md` mudam de texto agora; os templates da skill que descrevem a raiz minima so mudam na 2.14.0.
- Arquivos novos: `.github/workflows/ci.yml` e `release.yml`, `.github/ISSUE_TEMPLATE/`, `.github/dependabot.yml`, `.gitattributes`, `docs/CONTRIBUTING.md`, `docs/SECURITY.md`, `docs/CODE_OF_CONDUCT.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `README.pt-BR.md`; `README.md` reescrito em ingles.
- O validador nao checa a raiz e nao muda; o verificador ja confere travessao em todo `.md` versionado, incluindo os novos.
- PR #1 (`.cursor/environment.json`) fechado sem merge: viola a raiz minima e o fluxo nao usa Cursor Cloud Agent; o diagnostico de portabilidade dele vira tarefa.

## 2026-10-20 - ai-memory (akitaonrails) e camada complementar, fora do repositorio; nao mesclar

### Decisao

- O projeto `github.com/akitaonrails/ai-memory` nao entra no ai-project-structure nem como codigo nem como dependencia. Os dois atendem o mesmo problema (continuidade entre sessoes e entre vendors) em camadas diferentes: o ai-project-structure e o arquivo de regras e o registro revisado dentro do repositorio (`AGENTS.md`, `docs/`); o ai-memory e infraestrutura fora do repositorio (servidor Rust com MCP, hooks, SQLite FTS5, wiki propria) que, pela precedencia que ele mesmo declara, fica abaixo do arquivo de regras e nao duplica registro de decisao mantido no repo.
- Do ai-memory importam-se ideias, em texto do bloco core, das pontes e do template de `MEMORY.md`, nunca mecanismo: import real `@AGENTS.md` nas pontes, memoria tratada como evidencia e nao instrucao, releitura de `SESSION.md` e `TASKS.md` apos compactacao de contexto, medicao do orcamento de instrucoes de `AGENTS.md` e tipo "Armadilha" em `MEMORY.md`. Tarefas T-087 a T-091, escolhidas pelo usuario.
- Receita de coexistencia (alguem instalar o ai-memory ao lado da estrutura) ficou de fora por escolha do usuario; sobra a nota curta em `docs/MEMORY.md`.

### Motivo

- `PROJECT_CONTEXT.md` poe CLI propria fora de escopo e exige validador so com biblioteca padrao; absorver ou depender de um servidor Rust contraria as duas restricoes.
- O proprio ai-memory tracou a fronteira: precedencia usuario, rules file, memoria, perfil; o snippet que ele injeta em `AGENTS.md` diz que registro de decisao mantido no repositorio nao e store local de harness e que ele nao o duplica. Mesclar apagaria uma fronteira que os dois lados ja respeitam.
- A memoria da estrutura viaja no git do projeto (clone, PR, outra maquina, outra pessoa) sem servico rodando; a do ai-memory exige servidor ou o companion `wikisync`.
- Nao ha relacao de origem entre os projetos: nenhum cita o outro; linhagens distintas (Karpathy LLM Wiki, basic-memory e agentmemory de um lado; specsfy e Handoff do davidondrej do outro). A convergencia (`AGENTS.md` canonico, `CLAUDE.md` de ponte, Markdown como fonte) e independente.

### Impacto

- Nenhum arquivo da skill muda por esta decisao; as adocoes entram pelas tarefas, com bump 2.13.0 quando tocarem o bloco core, os assets de ponte ou o template de `MEMORY.md`.
- A analise completa (camadas, mapa de sobreposicao, o que nao importar) fica na entrada de `SESSION.md` de 2026-10-20; quem reavaliar o ai-memory parte dela, nao do zero.

## 2026-10-17 - Contexto de delegacao viaja na mensagem, nunca em arquivo temporario

### Decisao

- Ao delegar uma tarefa a outro agente (subagente, outra sessao, outro modelo), quem delega manda, na propria mensagem, um resumo curto com: objetivo e criterio de conclusao; estado feito e pendente; decisoes que valem e tentativas que nao se repetem; arquivos e registros a consultar, por caminho; e a instrucao de conferir o estado real antes de agir. A regra e o modelo vivem na secao "Passagem De Trabalho" do bloco core de `AGENTS.md`.
- Nenhum documento permanente novo: `SESSION.md`, `MEMORY.md`, `TASKS.md` e os demais seguem como registro do projeto, e o resumo aponta para eles em vez de copia-los. Subagente nao le a skill `ai-project-structure`: le o `AGENTS.md` do projeto e o resumo.

### Motivo

- No Cloudroom, subagente pode rodar em sandbox propria: nao ve a conversa do gestor, e arquivo temporario criado pelo gestor nao chega la. O metodo da skill Handoff (davidondrej) serviu de referencia (estado em vez de ordens, apontar artefatos, preservar o porque, exigir verificacao, sem segredo, so o util), mas o arquivo em `$TMPDIR` dela nao atravessa sandbox; por isso o resumo vai na mensagem.
- Mesmo principio ja registrado para o loop em `references/loop.md`: regra critica vai no prompt, porque ler arquivo e opcional e o prompt chega sempre.

### Impacto

- Bloco core cresce 1362 bytes (cerca de 380 tokens) para todo agente que le `AGENTS.md`; cada delegacao custa um resumo de uns 150 a 400 tokens, contra os cerca de 8 mil de ler `SESSION.md` inteiro ou os 1,2 mil da skill Handoff mais o arquivo que ela gera.
- Sem bump de versao, por T-078 a T-083; o passo 2 de `atualizacao.md` passa a seguir para o diff do bloco quando a versao e igual e o bloco difere. Bump em T-086. Validador intocado.

## 2026-10-17 - Gatilho da skill nao decide se um projeto ganha a estrutura; quem coordena decide

### Decisao

- A `description` do `SKILL.md` dispara a skill so quando o pedido nomeia a estrutura multiagente ou seus arquivos (`AGENTS.md`, `docs/`), cita a skill pelo nome, ou pede atualizar, validar, ativar specs ou rodar o loop. Pedido generico de criar projeto, pasta, repositorio ou scaffold nao dispara: o agente, no maximo, oferece a estrutura em uma linha, e quem coordena (o usuario, ou o agente gestor no Cloudroom) decide.
- `agents/openai.yaml` mantem `allow_implicit_invocation: true`: a invocacao implicita continua, agora contra uma description estreita.

### Motivo

- No Cloudroom, um agente gestor coordena subagentes em sandbox, e a tarefa do gestor chega ao subagente como se fosse o pedido do usuario. A skill nao distingue quem a chama. Com "cria projeto" e "monta a base do projeto" na lista de gatilhos, um subagente mandado fazer scaffold de codigo abria a entrevista da estrutura ou criava `AGENTS.md` e `docs/` sem ninguem pedir, e a decisao saia da mao do gestor.
- Alternativas rejeitadas: `allow_implicit_invocation: false` no Codex e `disable-model-invocation` no Claude Code (a confirmar na documentacao) travam de forma mecanica, mas exigem invocar a skill pelo nome e quebram o pedido direto do usuario em linguagem natural, que deve continuar funcionando.

### Impacto

- "Inicia projeto novo aqui." sozinho deixa de disparar a skill; custa um turno de confirmacao. Evals 2 e 4 refletem isso, e o eval 11 cobre o caso negativo (projeto Node com Vite).
- A description e prompt, nao trava: baixa a probabilidade de disparo errado, nao a zera. Protecao adicional fica fora da skill, no Cloudroom: `.bb/AGENTS.md` do workspace repetindo a regra, e o texto da tarefa que o gestor delega nomeando a estrutura e pre-respondendo a entrevista.
- Sem bump de versao: entra como item da 2.11.0, ainda nao commitada.

## 2026-09-04 - Automacao que grava material de agente no repositorio varre segredo antes e para ao achar

### Decisao

- Nenhuma automacao deste projeto grava no repositorio texto produzido por agente sem antes varrer padroes de segredo (chave de API, token, senha em URL, chave privada). Ao achar, a automacao para antes de gravar, guarda o material fora do repositorio, informa o caminho e pede palavra humana. Nunca redige e nunca grava por conta propria.

### Motivo

- P-10 da spec 0006 (T-074): preservar o bruto literal (DEC-001 da spec) e versiona-lo (DEC-008, DEC-009) cria caminho de exfiltracao permanente para o historico do git. Redigir automaticamente destruiria a evidencia; nao gravar por padrao mataria o teste da DEC-001; documentar o risco transfere o problema para quem nao leu. O usuario escolheu a varredura que para, em 2026-09-04, entre as tres opcoes esbocadas na tarefa.

### Impacto

- Vale para o orquestrador da spec 0006 e para qualquer automacao futura que grave saida de modelo em `docs/`. Padrao nao cobre todo segredo, e a documentacao da operacao precisa dizer isso. A spec 0006 passa a `Definida`.

## 2026-09-04 - Calibragens da spec 0006: aviso, ponte curta, retomada humana e bruto in-repo

### Decisao

- Na automacao do consenso (spec 0006), os checks novos para entrada automatizada sao **AVISO**, valendo so para entrada com marcador `**Origem:**`; a proveniencia fica num **manifesto** ao lado do bruto, com a entrada trazendo so uma ponte curta; a **retomada** de rodada interrompida sempre exige palavra humana; e o **bruto mora no repositorio desde o inicio**, fora da arvore de execucao, nunca em `.gitignore`.
- Detalhe e forca de cada uma em DEC-007, DEC-008 e DEC-009 da spec.

### Motivo

- As tres perguntas passaram por rodada 1 cega com 3 de 3 no que fazer; o que sobrou foi calibragem, e o usuario escolheu a posicao do Grok nas tres em 2026-09-04 (T-053). AVISO por simetria com o resto de `CONSENSUS.md`; ponte curta por rotacao e leitura humana; retomada humana porque insumo identico nao prova intencao identica; bruto in-repo porque o teste da DEC-001 (conferir o campo olhando o bruto ao lado) morre se o bruto sumir na sessao seguinte.

### Impacto

- Vale para o orquestrador da spec 0006 e para qualquer escrita automatizada em `docs/`. Uma pergunta continua a bloquear a spec: segredo no bruto versionado (P-10, T-074). Nenhuma linha de codigo antes dela.

## 2026-09-03 - install.sh avisa e pede confirmacao quando o destino diverge da fonte

### Decisao

- Antes de sobrescrever, o `install.sh` compara o destino existente com o que a fonte distribui e, se houver arquivo diferente ou extra, lista e pede confirmacao. Sem terminal interativo, recusa, salvo flag explicita para script. Destino inexistente ou identico segue sem pergunta.
- Nao adotados: copia por diretorio temporario trocado no fim, e apagar o destino inteiro antes de copiar.

### Motivo

- Escolha do usuario em 2026-09-03 (T-067). A revalidacao (REVAL-7) mostrou edicao local sobrescrita sem aviso e arquivo extra sobrevivendo; a promessa "sobrescreve com seguranca" precisa de uma pergunta antes, nao de mais mecanica.

### Impacto

- So `install.sh`, nao distribuido: sem bump. `verify_repository.py` continua instalando em pasta temporaria limpa, sem prompt. Trabalho em T-073.

## 2026-09-03 - Parenteses no comando do marcador verifica nao sao suportados; --seco nao grava agente

### Decisao

- O marcador verifica continua como esta: o comando vai ate o primeiro `)`. Comando com parenteses nao e suportado; isso fica escrito no bloco core, no template de `TASKS.md` e em `references/loop.md`, e o validador acusa marcador cujo comando contem `(`. O `loop_task.py check` recusa a tarefa antes de chamar o agente.
- `loop.sh --seco` nao repassa `--agente` ao fecho: evidencia so registra `agente=` quando um agente de fato rodou.

### Motivo

- Opcao (c) de T-061, escolhida pelo usuario em 2026-09-03 sobre (a) casar ate o ultimo `)`, que quebra linha com outro marcador depois, e (b) exigir crases, que muda contrato e obriga atualizacao de todo projeto. Comando com parenteses tem saida barata: um script auxiliar no projeto.
- `agente=` foi definido como "fato conhecido com certeza"; gravar sem execucao contradiz a propria razao do campo (REVAL-3).

### Impacto

- Cobranca nova de nivel ERRO em projeto que tenha marcador verifica com parenteses; hoje esse marcador ja nao funciona no loop, entao acusar e tornar visivel o que ja estava quebrado. Trabalho em T-072 e T-060, exige versao nova da skill.

## 2026-09-03 - Promessa do bloco core que o validador nao cobra vira check com nivel declarado, ou texto honesto

### Decisao

- Toda regra do bloco core que a revalidacao adversarial mostrou violavel sem diagnostico (REVAL-1, REVAL-2 e REVAL-6 em `docs/CONSENSUS.md`) ganha check no `validate_structure.py`, com o nivel abaixo, ou tem o texto do core corrigido para dizer o alcance real.
- **ERRO** (contradicao estrutural): linha em Concluidas sem data; marcador verifica com comando vazio; marcadores invertidos; bloco `loop` despareado ou sem versao; arquivo do nucleo vazio; `T-NNN` repetido entre o arquivo vivo e o archive.
- **AVISO** (lacuna de qualidade): forma da evidencia com os tres campos presentes e nao vazios; `Resposta` e marcador bloqueada ausentes em Aguardando Usuario; rodada 2 ou maior com exposicao `nao`; `Proximo passo` vazio; cerca aberta; spec Concluida com evidencia vazia; status de tarefa dentro da spec; ID fora de tres digitos; marcador bloqueada fora de secao; e `CONVENCOES-DATA-INVALIDA` sobe de INFO para AVISO, entao `--strict` passa a travar scaffold que pulou o passo 5b.
- **So texto**: travessao fora de `docs/` e ponte com regra continuam sem check, e o core passa a dizer isso.
- Codigo novo de diagnostico so entra em `CODIGOS` com fixture que o produza e com a mutacao registrada na evidencia da tarefa.

### Motivo

- Proposta registrada em REVAL-1 e aceita pelo usuario item a item em 2026-09-03 (T-059), sem alteracao de nivel. O criterio e o mesmo da decisao de 2026-09-02 sobre severidade: ERRO para contradicao ou quebra estrutural, AVISO para lacuna de qualidade.
- A revalidacao mostrou 22 documentos errados passando limpos em `--strict`, e 10 de 39 codigos com fixture. Cobrar por check em vez de por promessa e o unico jeito de a frase "o validador confere a forma" voltar a ser verdadeira.

### Impacto

- Cobranca nova em projeto que ja usa a estrutura: os AVISOs novos podem aparecer em `--strict` de projeto existente, e o usuario aceitou isso conscientemente. A nao retroatividade por data de adocao continua valendo onde ja valia (evidencia).
- Exige versao nova da skill (2.6.0), porque muda o contrato publico de `CODIGOS` e o texto de `assets/AGENTS.md`. Trabalho em T-069, T-070 e T-071; o portao de cobertura por codigo esta em T-065 e deve entrar antes ou junto.
- REVAL-1, REVAL-2 e REVAL-6 fecham como `resolvido`.

## 2026-09-03 - Arquivo de memoria do projeto se escreve por substituicao atomica

### Decisao

- Toda automacao deste projeto que grave um arquivo de `docs/` usa temporario no mesmo diretorio, `fsync`, e `os.replace`. Nunca `write_text` direto, nunca append no meio do arquivo.
- Vale para o `loop_task.py`, que ja esta publicado, e para qualquer operacao futura, incluindo o orquestrador da spec 0006.

### Motivo

- `write_text` trunca antes de escrever. Crash, disco cheio ou processo morto no meio deixam o arquivo partido, e os arquivos de `docs/` sao a memoria do projeto: `TASKS.md` e o backlog vivo, e perde-lo custa mais que qualquer rodada.
- Achado pelo Grok na rodada de P-9 da spec 0006, ao comparar o que a operacao de consenso precisaria fazer com o que o `loop_task.py` ja fazia. Conferido no codigo antes de aceito.
- A alternativa, confiar que a escrita e curta o bastante para nao ser interrompida, e a mesma aposta que qualquer arquivo de banco de dados aprendeu a nao fazer.

### Impacto

- `loop_task.py` corrigido na 2.5.1, com regressao provada por mutacao: com o comportamento antigo de volta, o teste acusa arquivo truncado.
- O pior caso passa a ser um temporario orfao ao lado do arquivo. Ruim, e nao destrutivo.
- Consequencia para a spec 0006: a minuta em `CONSENSUS.md` se escreve pelo mesmo caminho, substituindo o arquivo inteiro, o que ja era o desenho que a rodada de P-9 convergiu.

## 2026-09-03 - Agente nao escreve consenso; orquestrador deterministico escreve o recorte que a execucao comprova

### Decisao

- A proibicao da 0004/DEC-019 vale para **agente**, e nao para todo software: um agente de IA continua proibido de escrever em `docs/CONSENSUS.md`, em qualquer numero.
- Um **orquestrador mecanico** pode escrever, e so o recorte que a execucao comprova: a pergunta, as posicoes literais dos agentes, as falhas de quem nao respondeu, os comandos usados, e os campos `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`.
- As secoes de julgamento (pontos de acordo, consenso final, qualquer sintese) **nunca** sao escritas por software, e a entrada nasce com `Status: aberto` e `Proximo passo` com dono humano.
- O que sustenta a excecao e a **separacao entre quem opina e quem escreve**, nunca a quantidade de agentes.

### Motivo

- Rodada 1 cega de 2026-09-03 sobre a spec 0006, com tres posicoes independentes. O Claude havia proposto que a DEC-019 caisse por haver N agentes em vez de um; Codex e Grok chegaram sozinhos a mesma correcao, e ela e melhor: se quem escreve for um dos opinantes, ou um sintetizador livre, o acoplamento volta com N igual a qualquer coisa. O Grok precisou o ponto: a DEC-019 nomeia o agente, entao aplica-la a um script nao seria heranca, seria estende-la a um sujeito que ela nunca nomeou.
- A razao original da DEC-019 continua intacta e nao foi afrouxada: consenso escrito por um modelo, declarando a propria independencia, e a fraude que os campos da 2.2.0 existem para denunciar.

### Impacto

- Passam a existir **duas politicas de escrita** no projeto: o agente do loop nunca escreve em `CONSENSUS.md`; o orquestrador da spec 0006 escreve um recorte. Elas divergem de proposito, e cada prompt precisa dizer qual vale ali.
- Sem proveniencia registrada ao lado (comando, exit code, caminho do artefato bruto), os campos escritos pelo orquestrador voltam a ser autodeclaracao, so que do script. As tres posicoes da rodada apontaram isso, e a questao esta aberta como P-8 na spec 0006.
- Limite conhecido, registrado na propria rodada: isolar as posicoes resolve a **producao** delas e nao a **transcricao**. Enquanto quem organiza a saida for um dos participantes, o problema que motivou a spec sobrevive.

## 2026-09-03 - Fixture de check AVISO roda em --strict e confere quais avisos sairam

### Decisao

- Par de fixture `valido`/`invalido` cujo caso invalido produz apenas AVISO nao e verificado pelo exit code sem `--strict`: o par roda com a flag, e o check confere **quais** diagnosticos sairam, por motivo e por entrada, nunca so quantos exit codes bateram.
- O dicionario `FIXTURES` de `verify_repository.py` continua cobrindo esse par, mas como guarda de regressao ("nao virou ERRO por acidente"), nunca como prova de que o caso invalido acusa alguma coisa.

### Motivo

- Achado `0005-A1`, registrado em `docs/CONSENSUS.md`. O padrao de fixture do repositorio nasceu na 2.2.0, quando todo check novo era ERRO, entao "o exit code separa os dois lados" ficou implicito no padrao em vez de escrito. Os checks de achado da 2.4.0 sao AVISO por decisao da spec 0005, e quebram essa hipotese sem que nada acuse: os dois lados sairiam 0 e a suite reportaria um check verde que nao prova nada.

### Impacto

- `verify_repository.py` ganhou `verificar_achado`, com os dois lados em `--strict`, contagem de avisos e conferencia de que a entrada de debate de controle nunca e citada.
- Fica aberto o conserto geral, em `TASKS.md` (T-050): fazer o proprio `verify_repository.py` exigir oracle discriminante por fixture, em vez de depender de quem escrever a proxima fixture lembrar disso.
- **Correcao de 2026-09-03, vinda da revalidacao do achado `0005-A1` pelo Codex.** A redacao original desta decisao afirmava que o check "confere que eles caem na entrada certa". Isso descrevia mal o codigo: `verificar_achado` conta linhas `[AVISO]` e confere uma unica exclusao, a entrada de debate de controle. A regra acima continua valendo como esta escrita; o que faltava era a implementacao dela, agora em T-051. A primeira versao desta decisao tambem propunha, como conserto geral, recusar par com o mesmo exit code nos dois lados, o que contradizia a guarda que ela propria manda manter no `FIXTURES`; T-050 foi reescrita.

## 2026-04-25 - Estrutura multiagente com raiz minima

### Decisao

- Manter na raiz apenas os arquivos Markdown de entrada dos agentes: `AGENTS.md`, `CLAUDE.md` e `GEMINI.md`.
- Colocar a memoria do projeto dentro de `docs/`.
- Usar `AGENTS.md` como fonte central de instrucoes.
- Usar `SESSION.md` para continuidade entre sessoes.
- Usar `CONSENSUS.md` para debate entre modelos quando necessario.

### Motivo

- Evitar duplicacao de regras entre agentes.
- Facilitar continuidade entre sessoes de IA.
- Manter a raiz limpa e previsivel.
- Permitir que modelos diferentes opinem antes de decisoes importantes.

### Impacto

- Claude Code e Gemini passam a usar arquivos-ponte.
- Novos agentes devem ler `AGENTS.md`.
- Mudancas importantes precisam atualizar a memoria do projeto.

## 2026-04-25 - Evolucao da estrutura: MEMORY.md e oito melhorias

### Decisao

- Adicionado `docs/MEMORY.md` como memoria persistente em quatro tipos (User / Feedback / Project / Reference), com criterio de promocao e sobrescrita ativa.
- Adicionado `docs/archive/` com indice em `README.md` para rotacao de `SESSION.md` e `CONSENSUS.md`.
- `AGENTS.md` reescrito definindo: imutabilidade dos arquivos-ponte, dois niveis de leitura (trivial vs relevante), regra de desempate (usuario > menor risco reversivel > parar e pedir humano), atualizacao por gatilho, criterio de "onde escrever cada coisa", politica de rotacao, e que `CONSENSUS.md` so e para duvidas reais.
- Template de `SESSION.md` atualizado com handover direcionado (agente sugerido + motivo) e secao de "Aprendizados Para MEMORY.md".
- Template de `CONSENSUS.md` atualizado com `Status` (aberto | resolvido | arquivado) e `Proximo passo` quando aberto.
- `QUALITY.md` recebeu checklist de atualizacao por gatilho e de cuidados com `MEMORY.md`.
- Skill `ai-project-structure` sincronizada com a estrutura nova.

### Motivo

- Tri-consenso entre Claude, Gemini e Codex em `docs/CONSENSUS.md` (entrada `2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias`).
- Cobrir lacuna de "o que o projeto aprendeu" sem inflar `SESSION.md` ou `DECISIONS.md`.
- Reduzir overhead de leitura/atualizacao em mudancas triviais.
- Garantir que a estrutura nao colapse por baixa adocao operacional.

### Impacto

- Novos projetos criados pela skill ja nascem com a versao nova.
- Agentes precisam ler `MEMORY.md` em mudancas relevantes.
- Pendencias de sessao acionaveis devem virar tasks em `TASKS.md` antes de fechar a sessao.
- `CONSENSUS.md` ganha ciclo de vida (aberto / resolvido / arquivado) e regra de desempate explicita.
- `SESSION.md` e `CONSENSUS.md` passam a rotacionar para `docs/archive/` quando crescerem.

## 2026-08-20 - Skill v2.0.0: emprestimos do specsfy sem a cerimonia

### Decisao

- Evoluir a skill para 2.0.0 importando do specsfy (github.com/promovaweb/specsfy): entrevista numerada com opcoes numeradas ("Avançar" adia e nunca autoriza inferir), regra "Nunca Inferir" no `AGENTS.md`, `TASKS.md` com IDs `T-NNN`, blocos gerenciados com versao (`ai-project-structure:core`/`:specs`), validador executavel com exit code, e modulo opcional de specs leve (`docs/specs/`, arquivos `NNNN-slug.md` com campo `Status`).
- NAO importar: pipeline multi-skill numerado, minimo de 3 criterios/testes por requisito, sistema de attestation, CLI/TUI, monitor de contexto bloqueante.
- Anti-drift: `TASKS.md` e a unica fonte de status de tarefa; specs listam apenas T-IDs.
- Validador roda do diretorio da skill instalada (nao e copiado ao projeto) e usa apenas biblioteca padrao do Python 3.
- Proibir o caractere travessao (em dash, U+2014) em todos os textos do projeto e do core da skill; o validador acusa ocorrencias como erro.

### Motivo

- Analise do specsfy (repo + videos do autor) mostrou que a dor raiz e comum (contexto para a IA sem reler tudo), mas o publico e o eixo diferem: specsfy e pipeline de especificacao para vibe coding; nossa skill e memoria multiagente entre sessoes. Importar mecanismos pontuais resolve nossas lacunas (TASKS sem estrutura, validacao em prosa, sem versionamento/atualizacao) sem herdar a cerimonia.
- Travessao proibido por pedido explicito do usuario em 2026-08-20.

### Impacto

- Novos projetos nascem com estrutura v2 (marcadores versionados, TASKS com IDs, regra anti-travessao).
- Projetos v1 sao atualizaveis pelo fluxo `references/atualizacao.md`, com diff por bloco e confirmacao por item.
- `python3 <skill>/scripts/validate_structure.py <projeto>` vira o gate de qualidade da estrutura.
- O meta-projeto passa a usar a propria v2 (specs ativo; spec `0001-skill-v2`).

## 2026-05-26 - Distribuicao da skill via Agent Skills Open Standard

### Decisao

- Distribuir a skill `ai-project-structure` como um unico pacote no formato **Agent Skills Open Standard** (frontmatter YAML `name` + `description`), valido para Claude Code, Codex CLI e Gemini CLI ao mesmo tempo. Nao manter formatos separados por ferramenta.
- Caminhos canonicos de instalacao: Claude `~/.claude/skills/`, Codex `~/.agents/skills/`, Gemini `~/.gemini/skills/` (e os equivalentes `.<tool>/skills/` por-projeto).
- Adotar `install.sh` na pasta da skill como mecanismo oficial de instalacao/atualizacao/remocao.
- A instalacao copia apenas `SKILL.md`, `assets/` e `agents/`; `evals/`, `install.sh` e `README.md` ficam so na fonte.

### Motivo

- A partir de fins de 2025 o formato `SKILL.md` virou padrao aberto adotado por Claude Code, Codex e Gemini (entre outros), eliminando a necessidade de tres formatos distintos.
- O caminho de skills do Codex e `~/.agents/skills/`; o registro anterior usava `~/.codex/skills/`, que nao e lido pelo Codex.

### Impacto

- Uma unica fonte (`docs/skills/ai-project-structure/`) gera a instalacao nas tres ferramentas; atualizar = editar a fonte e rodar `install.sh`.
- Registro anterior de instalacao (2026-04-25) fica **substituido** por este: aquela instalacao nao persistiu e apontava o Codex para o caminho errado.


## 2026-09-02 - Evidencia obrigatoria em tarefa, secao Aguardando Usuario e consenso declarado

### Decisao

- Toda tarefa movida para `Concluidas` a partir da skill 2.2.0 carrega evidencia de fechamento em sub-linha propria (`Evidencia: tipo=...; procedimento=...; resultado=...`). O marcador `(verifica: <comando>)` na tarefa aberta continua opcional; quando presente, a evidencia deve registrar o resultado daquele comando, e a ausencia do resultado e ERRO.
- A regra nao e retroativa: tarefa concluida antes da 2.2.0 nao e cobrada, e o fluxo de `references/atualizacao.md` nao reescreve historico.
- Tarefa travada por falta de resposta do usuario vive na secao `## Aguardando Usuario`, com `**Pergunta:**`, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)`. A secao nao rotaciona; gera aviso por idade. Secao separada para bloqueio nao humano so quando existir caso real.
- Registro de consenso passa a declarar `**Metodo:**`, `**Exposicao previa a outras posicoes:**` e `**Rodada:** N de 3`, com rodada 1 cega e teto de 3 rodadas antes de escalar para o usuario. O validador checa presenca e valor, nunca veracidade.
- O verificador de integridade do meta-projeto vive em `docs/skills/ai-project-structure/evals/verify_repository.py`. Nao criar `scripts/` na raiz.
- O modulo de loop autonomo fica fora da 2.2.0 e nunca entra no scaffold. Sera modulo opcional, no padrao do modulo de specs, ativavel apenas em projeto cuja secao "Testes E Validacao" de `QUALITY.md` tenha comando real.

### Motivo

- Verificacao inteiramente opcional deixa passar exatamente as tarefas menos verificadas, preservando a lacuna que a mudanca pretende fechar. Tornar `(verifica:)` obrigatorio seria pior: empurraria o usuario a inventar comando falso em tarefa de conteudo, pesquisa ou decisao.
- A regra "Nunca Inferir" manda perguntar quando falta contexto, mas nao existia lugar para a tarefa esperar a resposta; a regra existia e nao era observavel.
- Consenso fraco era visualmente indistinguivel de consenso forte. Os campos declarativos nao provam independencia, mas tornam o grau de confianca observavel.
- `scripts/` na raiz viola a regra de raiz minima, cuja excecao cobre apenas `README.md`, `LICENSE` e `.gitignore`. Alem disso `evals/` nao e distribuido pelo `install.sh`, entao o verificador nao vai parar na maquina de todo usuario.
- O portao de verificacao de um loop nao pode existir no dia zero de um projeto novo, porque nao ha suite de teste ainda. Um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao.

### Impacto

- Bloco core, templates de `TASKS.md` e `CONSENSUS.md`, validador, evals e fixtures mudam na skill 2.2.0.
- `TASKS.md` cresce mais rapido (uma sub-linha por tarefa concluida); a rotacao opcional de "Concluidas" deixa de ser opcional na pratica em projetos longos.
- Aumenta o numero de contratos verificados por script e tambem o de contratos julgados na mao (scaffold e atualizacao), enquanto nao existir runner de evals.
- Decisao tomada apos revisao por modelo distinto; debate completo em `docs/CONSENSUS.md`, entrada de 2026-09-02. Spec de execucao: `docs/specs/0003-tasks-verificaveis.md`.

## 2026-09-02 - Severidade da evidencia ausente e corte declarado por projeto

### Decisao

- Evidencia ausente em tarefa concluida que **nao** declarou `(verifica:)` gera **AVISO**. ERRO fica reservado para a tarefa que declarou comando e concluiu sem o resultado dele. Quem quer portao duro roda `--strict`.
- A nao retroatividade da regra depende de um corte declarado **por projeto**, no marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` do proprio `docs/TASKS.md`. Sem o marcador, nem a evidencia nem os campos declarativos de consenso sao cobrados. O mesmo corte governa as duas regras.
- No scaffold, a skill preenche o marcador com a data do dia; na atualizacao, com a data da atualizacao. Nunca com data anterior.

### Motivo

- ERRO neste validador significa contradicao ou quebra estrutural (arquivo do nucleo ausente, ID duplicado, marcador despareado, Status invalido). Omitir evidencia sem ter declarado nada e lacuna de qualidade, nao contradicao.
- Evidencia e prosa: erro duro compra conformidade formal e aumenta o incentivo ao teatro de conformidade ja registrado como risco no consenso. AVISO para ERRO continua reversivel; o caminho inverso ja teria bloqueado projetos.
- Sem corte declarado, as 15 linhas historicas deste repositorio virariam 15 avisos e `--strict` deixaria de retornar 0, contra dois criterios de aceite da spec 0003.
- Corte fixo no codigo do validador nao serve: o validador e instalado uma vez e roda contra projetos em versoes diferentes. Corte no marcador do `AGENTS.md` tambem nao: quebraria a paridade byte a byte do bloco core.

### Impacto

- Projeto em 2.1.0 nao e afetado ate declarar o marcador; a atualizacao passa a ter um passo explicito para isso (`references/atualizacao.md`, passo 7b).
- Registrado tambem como DEC-010 e DEC-011 na spec `docs/specs/0003-tasks-verificaveis.md`.

## 2026-09-02 - O que a automacao pode escrever na memoria do projeto

### Decisao

- Automacao que executa tarefa (o modulo de loop, previsto para a 2.3.0) so escreve na memoria do projeto **o que um comando comprova**: fecha tarefa apenas se ela declarou `(verifica: <comando>)` e o comando saiu 0, colando a saida real como `Evidencia: tipo=comando`. Nunca escreve `tipo=revisao-manual` nem `tipo=conferencia`.
- Excecao unica: falta de contexto obrigatorio. Nesse caso a automacao move a tarefa para `## Aguardando Usuario` e escreve `**Pergunta:**`, `**Resposta:** (A preencher.)` e `(bloqueada: AAAA-MM-DD)`.

### Motivo

- Sem o limite, a evidencia passaria a ser escrita pela mesma coisa que ela deveria cobrar. Seria o teatro de conformidade que o consenso de 2026-09-02 ja tinha listado como risco, agora automatizado e em escala.
- A excecao se sustenta porque o limite protege contra **alegacao de conclusao nao merecida**, e registrar uma duvida e o oposto disso. O pior resultado possivel dessa escrita e uma pergunta boba, que a pessoa le e descarta.
- Sem a excecao, a pergunta so existiria no relatorio da rodada e se perderia entre sessoes, que e exatamente o Problema 2 que a 2.2.0 fechou.

### Impacto

- Define a fronteira entre o que a maquina pode afirmar e o que so a pessoa pode afirmar nos arquivos de memoria. Vale para qualquer automacao futura, nao so para o modulo de loop.
- A fatia do backlog que a automacao consegue fechar fica limitada as tarefas que declararam comando. Tarefa de conteudo, pesquisa ou decisao continua sendo fechada por gente.
- Registrado como DEC-001 e DEC-006 na spec `docs/specs/0004-modulo-de-loop.md`.
