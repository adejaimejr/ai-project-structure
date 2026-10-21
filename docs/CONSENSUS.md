# CONSENSUS

Use este arquivo quando modelos diferentes precisarem debater para chegar a um consenso.

Ele nao substitui `DECISIONS.md`. Quando o debate gerar uma decisao importante, copie a decisao final para `DECISIONS.md`.

## Quando Usar

Use este arquivo quando:

- houver discordancia entre agentes;
- a decisao tiver impacto em arquitetura, produto, dados, seguranca ou custo;
- a tarefa tiver risco alto;
- o usuario pedir opiniao de outro modelo;
- a resposta correta depender de tradeoffs.

Nao use para decisoes simples ou tarefas obvias.

## Entrada Automatizada

Quando a rodada e rodada por `consenso.py` (da skill `ai-project-structure`), a entrada nasce de uma minuta escrita pelo script, nao por um modelo. Ela e a mesma entrada do modelo abaixo, com campos a mais que ligam o texto ao que a execucao comprova:

- `**Origem:**` `automacao`. Marca a entrada como automatizada. O validador so cobra os campos abaixo de quem declara este.
- `**Manifesto:**` caminho, a partir da raiz, do manifesto de cada rodada (`docs/consensus/<run-id>/manifesto.json`), separados por virgula. Ali ficam o comando integral, o diretorio, o exit code e os hashes de insumo e saida; a entrada traz so a ponte.
- `**Participantes:**` ids dos agentes que rodaram, separados por virgula. Cada id tem a secao `### Posicao De <id>` (na revalidacao de achado, `### Revalidacao De <id>`).
- `**Falhas:**` ids que falharam, ou `nenhuma`. Cada id tem a secao `### Falha De <id>`, no lugar da posicao.

O bruto de cada agente fica em `docs/consensus/<run-id>/<id>/stdout.txt` e **nao pode ir para o `.gitignore`**: sem ele ninguem confere a posicao. As posicoes entram literais, em citacao, sem resumo. As secoes de julgamento nascem com "(A preencher.)" e sao de quem le: o script nao sintetiza, nao declara convergencia e nao decide por maioria. A entrada nasce com `**Status:** aberto`. Os campos `Metodo`, `Exposicao previa a outras posicoes` e `Rodada` passam a descrever um fato da execucao; o validador continua checando a forma, nunca a veracidade.

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

### Contexto

- 

### Pergunta Ou Decisao

- 

### Posicao Do Codex

- 

### Posicao Do Claude

- 

### Posicao Do Gemini

- 

### Pontos De Acordo

- 

### Riscos E Tradeoffs

- 

### Consenso Final

- 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Achado

Nem todo uso deste arquivo e debate. Quando a validacao cruzada encontra um defeito, risco ou lacuna, isso e um **achado**, e vira entrada propria, com `**Status:**` e `**Proximo passo:**` proprios.

- `**Achado:**` traz o identificador do achado. Ele e livre, amarrado a unidade de trabalho do projeto (`N10`, `API-3`, o que o projeto ja usar): o validador confere que o campo existe e tem valor, e nunca opina sobre o valor.
- `**Escapou de verificacao:**` `sim` ou `nao`, dizendo se a verificacao que ja existia deixou o achado passar. Declarou `sim`? A entrada traz a secao `### Por Que Nada Pegou Antes`.
- A disposicao do achado e de quem o registra; a revalidacao dela e de outro modelo, e conta como rodada.
- Achado so vira tarefa em `TASKS.md` depois de a disposicao concluir que ha trabalho, e a tarefa cita o achado na linha.

Nao ha teto de rodadas. Da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`, dizendo o que a rodada anterior deixou em aberto.

## Ponto Cego Da Validacao Cruzada

Rodada verde e ausencia de objecao, nao prova de que funciona. Modelos que leem o mesmo texto herdam o mesmo ponto cego, e defeito que so existe em contexto de execucao real sobrevive a N rodadas de leitura.

## Modelo De Achado

```md
## AAAA-MM-DD - Titulo curto do achado

**Achado:** <identificador livre, ex: N10>

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim | nao

**Pendente da rodada anterior:** (obrigatorio da rodada 4 em diante)

### Contexto

- 

### O Que Foi Encontrado

- 

### Disposicao

- (o que quem registrou o achado decidiu fazer, e por que)

### Revalidacao

- (modelo distinto avaliando a disposicao acima, nao o achado em si)

### Por Que Nada Pegou Antes

(obrigatoria quando `**Escapou de verificacao:**` for `sim`; corte a secao quando for `nao`)

- O que passou verde: 
- Mecanismo do ponto cego: 
- Conserto de portao proposto: 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Registros

As entradas anteriores a 2026-09-03 (e as duas rodadas de P-7/P-8 e P-9 da spec 0006, que continuam `aberto` aguardando calibragem do usuario em T-053) foram rotacionadas para `docs/archive/CONSENSUS-2026.md`. Abaixo ficam os dois achados mais recentes da revalidacao adversarial de 2026-09-03 (REVAL-6 e REVAL-7). A entrada REVAL-5 (fluxos de scaffold, atualizacao e specs), unica que fechou `resolvido` sem defeito, foi rotacionada no mesmo dia para `docs/archive/CONSENSUS-2026.md` por tamanho; REVAL-1 a REVAL-4, todas `resolvido`, foram rotacionadas para o mesmo arquivo em 2026-10-21, antes da bancada real da automacao do consenso (T-083), porque o arquivo estava a poucos bytes do teto de 30KB.

## 2026-09-03 - REVAL-6: templates entregues ficaram atras do bloco core, e um deles ensina o anti-padrao

**Achado:** REVAL-6

**Status:** resolvido

**Resolvido em:** 2026-09-03, `CONVENCOES-DATA-INVALIDA` sobe para AVISO por T-059 (T-070); consertos de texto em T-063.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 6. Grok 4.6 (mesmo perfil de REVAL-1) atacou todos os arquivos de `assets/`, montando projeto minimal e completo com specs e simulando o dia seguinte. Claude fez o mesmo antes de ler o Grok (`s6-claude-dia-seguinte.txt`) e conferiu os achados novos no template.

### O Que Foi Encontrado

- **Irmaos de T-055**: `QUALITY.md` (checklists), `PROMPTS.md`, `ONBOARDING.md` e `README.md` nao mencionam evidencia de fechamento, Aguardando Usuario, campos de independencia nem achado. O prompt "Solicitar Consenso Entre Modelos" pede posicao sem `Metodo`, `Exposicao previa` e `Rodada`: quem o segue produz entrada que falha em `--strict`. O modelo de sessao corta a nota "qualquer agente serve se tiver contexto suficiente" que o core pede.
- **Sobras do meta-projeto**: `assets/docs/ARCHITECTURE.md` lista `docs/skills/` como modulo do projeto-alvo; `GLOSSARY.md` define skill como "ensinar o Codex".
- **Core manda ler `docs/ARCHITECTURE.md`** e o nivel minimal, recomendado, nao o cria.
- **Placeholder `AAAA-MM-DD` esquecido** no marcador de adocao e so INFO, `--strict` passa, e a cobranca de evidencia fica desligada no projeto inteiro.
- **O unico exemplo de evidencia** no template e `tipo=comando; procedimento=pytest -q` numa estrutura cuja unica tarefa real e de conteudo, que o core manda fechar com `revisao-manual` ou `conferencia`.
- Copia literal do Modelo De Debate (com os valores em uniao `aberto | resolvido | arquivado`) e do modelo de linha concluida (com `(spec: 0001-login-social)`) falha em `--strict`; o segundo e ERRO por spec inexistente. Baixa: modelo e forma, nao valor, mas o exemplo de spec e uma armadilha real.
- Dia 0, 1 e 2 com os templates preenchidos passam em `--strict`; `partials/` nunca e copiado, e nenhuma instrucao leva a copiar a pasta.

### Disposicao

- Texto: atualizar QUALITY, PROMPTS, ONBOARDING, README e SESSION dos assets para a 2.2.0/2.4.0; limpar ARCHITECTURE e GLOSSARY; trocar o exemplo de evidencia por um de `revisao-manual` ao lado do de comando; tirar `(spec: 0001-login-social)` do modelo de linha; core ganhar "quando existir" em ARCHITECTURE.md. Nada disso muda contrato.
- Decisao do usuario (T-059): `CONVENCOES-DATA-INVALIDA` sobe para AVISO (e `--strict` passa a travar scaffold que pulou o 5b) ou fica INFO.

### Revalidacao

- Claude Fable conferiu cada linha citada nos assets e reproduziu o placeholder e o dia seguinte. Nada nao confirmado.

### Por Que Nada Pegou Antes

- O que passou verde: `verify_repository.py` confere que os templates de `TASKS.md` e `CONSENSUS.md` carregam as convencoes atuais, por substring, e nada mais dos assets.
- Mecanismo do ponto cego: a paridade e verificada so nos arquivos que mudaram na 2.2.0 e na 2.4.0; os outros templates nunca entraram no portao, e o dogfood da raiz reescreveu os proprios `QUALITY.md` e `PROMPTS.md` sem propagar para o asset.
- Conserto de portao proposto: `verificar_convencoes` cobrir todos os templates que citam regra do core, com a lista de termos por arquivo.

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma ate a calibragem do INFO.

## 2026-09-03 - REVAL-7: a distribuicao funciona, mas o README ensinava instalacao quebrada e o instalador levava bytecode

**Achado:** REVAL-7

**Status:** resolvido

**Resolvido em:** 2026-09-03, T-067 respondida pelo usuario (aviso e confirmacao quando o destino diverge); decisao em `docs/DECISIONS.md`, conserto em T-073.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 7. Codex rodou 312 mil tokens e morreu na cota do plano ("You've hit your usage limit") antes do relatorio; a superficie foi refeita com a mesma familia por outra assinatura, GPT-5.6 via `cursor-agent -p --mode ask --force --model gpt-5.6-sol-high`. Claude exercitou o `install.sh` de verdade em HOME falso antes de ler qualquer agente (`s7-claude-install.txt`) e conferiu as strings do binario do Codex 0.152.1.

### O Que Foi Encontrado

- **README da skill**: "Instalacao manual" copiava so `SKILL.md`, `assets` e `agents`, sem `scripts/` e `references/`; quem seguisse ficava sem validador, atualizacao, specs e loop. A lista de fixtures parava em tres (faltavam `achado-project` e `debate-project`). Corrigido hoje.
- **`__pycache__` distribuido**: `scripts/__pycache__` (gravado pelo proprio verificador, ver REVAL-4) ia junto em `cp -R`, seis arquivos por instalacao. Corrigido hoje no `install.sh`.
- **Idempotente, mas nao seguro**: rodar duas vezes da arvore identica; destino editado localmente (`SKILL.md`, `validate_structure.py`) e sobrescrito sem aviso; arquivo extra na raiz do destino sobrevive para sempre (so `assets/`, `agents/`, `scripts/` e `references/` sao apagados antes da copia).
- **Falha parcial**: com `assets/` do destino sem permissao de escrita, o `SKILL.md` ja foi trocado quando o `rm -rf` falha, e o destino fica em 2.5.1 no frontmatter com `assets/` da versao anterior. Nao ha copia atomica nem rollback.
- `--uninstall` em HOME vazio imprime "removido" para cada destino que nao existia; `--all` funcionava e nao estava no cabecalho (adicionado hoje).
- `agents/openai.yaml`: o binario do Codex 0.152.1 contem `policy.allow_implicit_invocation` e o texto "When false, the skill is not injected into..."; a chave e lida. O comportamento real de invocacao implicita nao foi exercitado com uma sessao do Codex, por cota.
- CHANGELOG da skill: a entrada 2.3.0 lista exit codes 0 a 3 e o exit 4 aparece so em item posterior; a 2.5.1 repete a versao em prosa. Nada descreve comportamento que o codigo nao tenha.
- Achados so do GPT-5.6, conferidos: `install.sh --help` omite `--global` e `--help` (o cabecalho e a ajuda sao o mesmo texto); o comentario de `agents/openai.yaml` o chama de "parte do Agent Skills Open Standard" e o proprio Codex o descreve como "extended, product-specific config"; falha forcada no terceiro `cp` deixa `SKILL.md` e `assets/` novos com `scripts/` e `references/` velhos, e uma reinstalacao completa recupera. `codex help skills` nao existe na 0.152.1.

### Disposicao

- Aplicado hoje, sem bump: README, `install.sh` (`__pycache__` e `--all` no cabecalho), `evals.json`.
- Decisao do usuario (T-067): avisar ou recusar quando o destino diverge da fonte; copiar para temporario e trocar com `mv` no fim; apagar arquivo extra na raiz do destino.

### Revalidacao

- GPT-5.6 (cursor), familia diferente de Claude, achou por conta propria os mesmos quatro itens centrais (transacionalidade, `__pycache__`, instalacao manual, versao em prosa) e mais tres pequenos, todos conferidos no codigo por Claude. Nada nao confirmado.

### Por Que Nada Pegou Antes

- O que passou verde: `verificar_install` compara os tres destinos entre si e com a fonte, ignorando `__pycache__` de proposito (`IGNORADOS`), entao o bytecode distribuido nunca apareceu no diff. O README nunca teve check.
- Mecanismo do ponto cego: o portao ignora exatamente o artefato que estava vazando, e testa so o caminho feliz do `install.sh` (destino novo, sem falha, sem edicao local).
- Conserto de portao proposto: `verificar_install` conferir que o destino nao contem `__pycache__` (feito indiretamente hoje, pelo check na fonte) e exercitar reinstalacao sobre destino sujo.

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma.

## 2026-10-21 - Diretorio de corrida incompleto em docs/consensus/ (T-083)

**Status:** aberto

**Proximo passo:** usuario le as posicoes e preenche as secoes de julgamento

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Origem:** automacao

**Manifesto:** docs/consensus/2026-10-21-043054-debate/manifesto.json

**Participantes:** codex, sol

**Falhas:** nenhuma

### Contexto

- Modo: debate
- Rodada: 1 de 1
- N: 2
- Data: 2026-10-21
- Manifesto: docs/consensus/2026-10-21-043054-debate/manifesto.json

### Pergunta Ou Decisao

> O que o validador (scripts/validate_structure.py) deve fazer com um diretorio de corrida incompleto em docs/consensus/ (manifesto com status em-andamento ou interrompida, participante sem stdout.txt, ou pasta sem manifesto.json)? Opcoes em jogo: ignorar por completo (como hoje), avisar so quando uma entrada de docs/CONSENSUS.md aponta para ele, ou avisar sempre que existir. Considere a DEC-009 da spec 0006 (bruto e manifesto moram no repositorio desde o inicio; retomada so por comando explicito) e o custo de falso positivo numa rodada legitimamente em andamento. Leia o codigo do validador e do consenso.py na copia antes de responder.

### Posicao De codex

> O validador deve avisar somente quando uma entrada de `docs/CONSENSUS.md` apontar para o diretório incompleto.
> 
> Isso preserva a DEC-009: o material bruto e o manifesto podem existir no repositório desde o início, e uma corrida só é retomada por comando explícito. Portanto, uma pasta isolada, inclusive com manifesto `em-andamento`, `interrompida`, participante sem `stdout.txt` ou sem manifesto, não prova corrupção nem exige intervenção.
> 
> Já uma referência em `CONSENSUS.md` transforma aquele diretório em evidência declarada de uma rodada. Nesse caso, a incompletude quebra a rastreabilidade e o aviso é apropriado.
> 
> Avisar sempre criaria falso positivo durante uma rodada legítima em andamento. Ignorar sempre permitiria referências documentais quebradas sem detecção.

### Posicao De sol

> Não consegui ler a cópia: as tentativas de acesso falharam antes de executar os comandos, com `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
> 
> Sem ler `scripts/validate_structure.py`, `consenso.py` e a DEC-009 completa, não tenho base para emitir o parecer solicitado. Escolher uma opção agora contrariaria sua exigência de leitura e a regra “Nunca Inferir”.
> 
> É necessário restabelecer o acesso à cópia ou fornecer o conteúdo desses arquivos. Nenhum arquivo foi alterado.

### Pontos De Acordo

- (A preencher.)

### Riscos E Tradeoffs

- (A preencher.)

### Consenso Final

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)

## 2026-10-21 - Diretorio de corrida incompleto em docs/consensus/ (T-083, segunda rodada 1 cega, sandbox sem bubblewrap)

**Status:** aberto

**Proximo passo:** usuario le as posicoes e preenche as secoes de julgamento

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Origem:** automacao

**Manifesto:** docs/consensus/2026-10-21-114042-debate/manifesto.json

**Participantes:** codex, sol

**Falhas:** nenhuma

### Contexto

- Modo: debate
- Rodada: 1 de 1
- N: 2
- Data: 2026-10-21
- Manifesto: docs/consensus/2026-10-21-114042-debate/manifesto.json

### Pergunta Ou Decisao

> O que o validador (scripts/validate_structure.py) deve fazer com um diretorio de corrida incompleto em docs/consensus/ (manifesto com status em-andamento ou interrompida, participante sem stdout.txt, ou pasta sem manifesto.json)? Opcoes em jogo: ignorar por completo (como hoje), avisar so quando uma entrada de docs/CONSENSUS.md aponta para ele, ou avisar sempre que existir. Considere a DEC-009 da spec 0006 (bruto e manifesto moram no repositorio desde o inicio; retomada so por comando explicito) e o custo de falso positivo numa rodada legitimamente em andamento. Leia o codigo do validador e do consenso.py na copia antes de responder.

### Posicao De codex

> Minha posição: avisar somente quando `docs/CONSENSUS.md` apontar para a corrida.
> 
> DEC-009 torna diretórios incompletos um estado normal: o manifesto nasce como `em-andamento`, o bruto é salvo antes da minuta e uma interrupção preserva esse material no repositório sem alterar `CONSENSUS.md`. Avisar sempre transformaria uma rodada legítima em andamento em falso positivo, inclusive se alguém rodar o validador durante a execução.
> 
> O escopo correto é a integridade de uma alegação publicada:
> 
> - Sem ponte em `CONSENSUS.md`: ignorar pasta sem manifesto, manifesto não concluído e participante sem `stdout.txt`. O `consenso.py retomar` é o mecanismo explícito para inspecionar e continuar esse estado.
> - Com ponte em `**Manifesto:**`: avisar se o manifesto não existe, não pode ser lido, não tem `status: concluida`, ou se um participante registrado como artefato da rodada não tem o `stdout.txt` esperado. Uma entrada publicada jamais deveria apontar para corrida ainda em curso, pois o script só escreve a minuta no fim e só marca `concluida` depois dela.
> - Severidade: AVISO, bloqueante apenas em `--strict`, coerente com os checks opt-in de `**Origem:**` da DEC-007.
> 
> Hoje o validador já segue parcialmente esse limite: só verifica se o caminho de manifesto citado resolve. Ele não varre `docs/consensus/` nem interpreta o conteúdo do manifesto. Eu estenderia essa verificação vinculada, sem adicionar uma varredura global do sidecar.

### Posicao De sol

> Minha recomendação é **avisar somente quando uma entrada automatizada de `docs/CONSENSUS.md` aponta para a corrida incompleta**, preservando o opt-in por `**Origem:**`. O diagnóstico deve ser AVISO, coerente com a DEC-007.
> 
> A DEC-009 torna a existência de material incompleto no repositório um estado previsto. Ela não exige que toda corrida seja retomada ou publicada. Avisar sempre transformaria uma execução legítima, ou uma interrupção preservada corretamente, em falha de `--strict`.
> 
> O código confirma essa distinção:
> 
> - `abrir_rodada()` cria a pasta antes da gravação do manifesto. Existe uma janela legítima com pasta sem `manifesto.json`.
> - `_rodar_debate()` grava o manifesto como `em-andamento` antes de executar os agentes. Os arquivos `stdout.txt` aparecem conforme cada participante termina.
> - Uma interrupção pode deixar participantes sem registro nem stdout, deliberadamente. `_retomar()` identifica esses participantes e só os chama mediante comando explícito.
> - `fechar_debate()` publica a minuta antes de selar o manifesto como `concluida`.
> 
> Esses comportamentos estão em [consenso.py](/tmp/consenso-5emyxgmf/projeto/docs/skills/ai-project-structure/scripts/consenso.py:385). Portanto, incompletude isolada não comprova defeito.
> 
> Eu adotaria esta regra:
> 
> | Situação | Comportamento |
> |---|---|
> | Corrida sem referência em entrada automatizada | Não emitir diagnóstico de incompletude |
> | Entrada aponta para manifesto ausente | AVISO, como já ocorre |
> | Entrada aponta para manifesto ilegível ou com status `em-andamento` ou `interrompida` | AVISO de proveniência incompleta |
> | Entrada aponta para corrida cujo bruto esperado está ausente | AVISO, identificando corrida e participante |
> | Stdout existe, mas está vazio por falha registrada | Não considerar incompleto apenas pelo tamanho |
> 
> Hoje, [check_consensus_origem()](/tmp/consenso-5emyxgmf/projeto/docs/skills/ai-project-structure/scripts/validate_structure.py:572) verifica a existência do manifesto, mas explicitamente não examina seu conteúdo. Assim, **a opção intermediária exige ampliar a verificação**: um manifesto existente pode esconder status incompleto ou ausência do bruto. Ignorar esses problemas mesmo depois da publicação enfraquece a ponte de proveniência da DEC-008.
> 
> Há uma ressalva de concorrência: como a minuta e o manifesto são gravados separadamente, o validador pode observar a entrada recém-publicada antes do status `concluida`. O aviso deve descrever o estado observado, sem afirmar corrupção ou abandono. Uma nova validação após o encerramento resolve essa janela. Eu não acrescentaria heurísticas de idade ou existência do lock: o lock é por projeto e pode ficar órfão.
> 
> O custo aceito dessa escolha é deixar corridas interrompidas sem referência fora do diagnóstico padrão. Se houver necessidade de descobrir material esquecido, isso cabe numa inspeção explícita de corridas pendentes. Não deve impor a obrigação de retomar, apagar ou publicar material para obter validação verde.
> 
> O validador também não deve retomar corridas, limpar locks ou reparar artefatos. A DEC-009 reserva a retomada ao comando humano explícito.

### Pontos De Acordo

- (A preencher.)

### Riscos E Tradeoffs

- (A preencher.)

### Consenso Final

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)
