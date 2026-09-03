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

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

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

As entradas anteriores a 2026-09-03 (e as duas rodadas de P-7/P-8 e P-9 da spec 0006, que continuam `aberto` aguardando calibragem do usuario em T-053) foram rotacionadas para `docs/archive/CONSENSUS-2026.md`. Abaixo ficam os achados da revalidacao adversarial de 2026-09-03. A entrada REVAL-5 (fluxos de scaffold, atualizacao e specs), unica que fechou `resolvido` sem defeito, foi rotacionada no mesmo dia para `docs/archive/CONSENSUS-2026.md` por tamanho.

## 2026-09-03 - REVAL-1: o contrato do bloco core promete o que o validador nao cobra

**Achado:** REVAL-1

**Status:** resolvido

**Resolvido em:** 2026-09-03, proposta aceita item a item pelo usuario (T-059); decisao em `docs/DECISIONS.md`, conserto em T-069, T-070 e T-071.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 1 da revalidacao adversarial da skill 2.5.1. Grok 4.6 (`cursor-agent -p --mode ask --force --model cursor-grok-4.6-xhigh`) atacou o bloco core num worktree com as entradas contemporaneas de `CONSENSUS.md` retiradas. Claude Fable selou posicao antes de rodar qualquer agente e conferiu cada item no codigo, com projeto minimo montado a partir de `assets/` e `validate_structure.py --strict --codigos`. Bruto em `docs/archive/revalidacao-2026-09-03/`.

### O Que Foi Encontrado

Regra do core violavel sem nenhum diagnostico, cada uma reproduzida com exit 0 em `--strict`:

- **Evidencia de fechamento.** Linha em Concluidas sem prefixo de data nao e cobrada (`check_evidence`, `done_date is None`). A migracao real de v1 (superficie 5) produziu exatamente isso: `T-004` sem data, sem evidencia, validador limpo.
- **Forma da evidencia.** O core diz que "o validador confere a forma da evidencia". Basta uma sub-linha que comece com `Evidencia:`; `tipo=`, `procedimento=` e `resultado=` nao sao exigidos. `(verifica: )` vazio anula o unico ERRO da regra, porque string vazia esta contida em qualquer texto. `resultado=` vazio passa.
- **Aguardando Usuario.** O core exige `**Pergunta:**`, `**Resposta:**` e `(bloqueada:)`; so a pergunta e cobrada. Sem `(bloqueada:)`, `TASK-BLOQUEADA-ANTIGA` nunca dispara.
- **Pontes imutaveis.** `check_bridges` so confere a substring `AGENTS.md`. Ponte com regra de produto, arquitetura e estilo passa.
- **Rodada 2 com exposicao `nao`.** O core diz que da rodada 2 em diante a exposicao "deve ser declarada como sim"; nenhum cruzamento existe. `**Proximo passo:**` vazio satisfaz "com dono claro".
- **Travessao "em qualquer texto".** So `AGENTS.md`, as pontes e `docs/**/*.md`. `README.md` da raiz e qualquer `.py` passam.
- **Cerca aberta.** Um ` ``` ` sem par esconde do validador tudo ate o fim do arquivo: ID duplicado e concluida sem evidencia somem.
- **Marcadores.** `MARKER_RE` casa so `core|specs`; bloco `loop` despareado ou sem versao passa. Marcadores invertidos (end antes de start) passam.
- **Modulo incoerente.** Bloco specs em `AGENTS.md` sem `docs/specs/` nao acusa.
- **Leitura obrigatoria.** O core manda ler `docs/ARCHITECTURE.md` sem "se existir"; o scaffold minimal nao cria o arquivo.

Nao verificavel por desenho (e o core ja admite parte disso): ordem de leitura, Nunca Inferir, escopo, desempate, veracidade dos campos de independencia, "achado so vira tarefa depois da disposicao". Contradicoes de texto: core aceita pergunta aberta "como tarefa em TASKS.md **ou** na spec", o bloco specs manda registrar na spec; o gatilho "trabalho relevante atualiza SESSION.md" nao abre excecao para o loop, que e proibido de escrever la; a rotacao por 30KB pode obrigar a arquivar menos de 5 entradas.

### Disposicao

- Cada item e conserto pequeno no validador, mas o **nivel** de cada diagnostico novo e cobranca nova em projeto existente, e isso e calibragem do usuario (mesmo criterio de T-054). Proposta para decisao: data ausente em Concluidas, `(verifica: )` vazio, marcador invertido e loop despareado viram ERRO (sao contradicao estrutural); forma da evidencia, `Resposta`/`(bloqueada:)` ausentes, rodada 2 com `nao`, proximo passo vazio e cerca aberta viram AVISO; travessao fora de `docs/` e ponte com regra ficam como estao, com o texto do core dizendo o alcance real. `ARCHITECTURE.md` ganha "quando existir" no core.

### Revalidacao

- Claude Fable, familia diferente de quem achou: cada item reproduzido em projeto minimo com o comando em `docs/archive/revalidacao-2026-09-03/s1-claude-verifica-grok.txt` e `s2-claude-falsos-negativos.txt`. Nenhum item ficou como "nao confirmado". Ressalva de metodo: a transcricao e do Claude, que tambem opinou; o bruto do Grok esta ao lado para conferencia.

### Por Que Nada Pegou Antes

- O que passou verde: `verify_repository.py` 44 de 44 e a raiz em `--strict`, em todas as versoes desde a 2.2.0.
- Mecanismo do ponto cego: cada check nasceu com fixture para o caso **novo** daquela versao, nunca para o contrato inteiro do bloco core. O core foi escrito como promessa e o validador como amostra, e ninguem cruzou os dois linha a linha. A raiz, dogfood, nunca produziu nenhum dos documentos errados acima.
- Conserto de portao proposto: tabela contrato-para-codigo em `evals/` (cada regra verificavel do core aponta o codigo de diagnostico que a cobra, ou declara "nao verificavel") e uma fixture por codigo. Ver REVAL-4.

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma ate o usuario calibrar os niveis.

## 2026-09-03 - REVAL-2: o validador tem falso negativo em quase toda regra que nao nasceu com fixture

**Achado:** REVAL-2

**Status:** resolvido

**Resolvido em:** 2026-09-03, niveis decididos em T-059 (decisao em `docs/DECISIONS.md`, conserto em T-069 e T-070); tracebacks e codigo morto em T-064.

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 2. Codex (`codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="xhigh"`) atacou `validate_structure.py` com o `main` real sobre `assets/` e overlays em memoria, porque o sandbox recusou escrever em `/tmp`. Claude escreveu dez documentos-que-passam antes de ler o Codex (`s2-claude-falsos-negativos.txt`) e reproduziu cada achado novo em projeto de verdade (`s2-claude-verifica-codex.txt`). Os itens que Grok tambem achou na superficie 1 estao em REVAL-1 e nao se repetem aqui.

### O Que Foi Encontrado

Documento errado que passa limpo em `--strict`, alem dos de REVAL-1:

- `SESSION.md`, `CONSENSUS.md` e `TASKS.md` **vazios** (zero bytes) passam: os parsers devolvem colecoes vazias. O proprio `assets/` passa com so o INFO da data.
- Spec `Concluida` com a secao "Evidencia De Conclusao" **vazia** passa: o check so recusa a substring `(a preencher`. Qualquer texto que nao seja isso, como `- banana`, satisfaz.
- `T-1` e aceito como ID (`\d+`); segunda `(prioridade: lixo)` na mesma linha nao e olhada; `(spec: 0001-NNNN-ausente)` e ignorado porque contem `NNNN` em qualquer posicao; `(bloqueada:)` fora de "Aguardando Usuario" e aceito.
- `T-001` vivo e `T-001` em `docs/archive/TASKS-*.md` nao sao duplicidade: o archive so entra na conferencia de specs.
- Status de spec no meio de um paragrafo (`... contem **Status:** Rascunho`) e aceito: a regex nao esta ancorada.
- Regra anti-drift das specs (`status vive so em TASKS.md`) nao tem check nenhum: `- T-001: tarefa (status: concluida) [x] feito` dentro da spec passa.
- Entrada de `CONSENSUS.md` na rodada 2 com exposicao `nao`, `Proximo passo` vazio e secao "Por Que Nada Pegou Antes" sem conteudo passa.

Traceback em vez de diagnostico:

- Arquivo fora de UTF-8 (`MEMORY.md` em latin-1): `read()` so captura `OSError`, `UnicodeDecodeError` derruba o script inteiro.
- Rotulo com acento combinante (`**Metodo:́**`, U+0301): `field_value` normaliza antes de fazer `split(":**")` e cai em `IndexError`.

Falso positivo: heading ATX com fechamento (`### Objetivo ###`), valido em CommonMark, gera `SESSAO-SEM-HEADINGS`. Exemplo em cerca `~~~` (nao ```) e lido como entrada real.

Codigo morto: `ENTRY_RE` (linha 59) e `DATE_RE` (linha 70) nunca sao usados.

### Disposicao

- Tracebacks, codigo morto, `~~~`, ATX fechado, `NNNN` em qualquer posicao e ancoragem do Status: conserto sem decisao, com fixture ou teste para cada (T-064).
- Arquivo vazio, evidencia de spec vazia, `T-1`, duplicidade com archive, `(bloqueada:)` fora de secao e anti-drift: cada um e cobranca nova em projeto existente; entram na mesma calibragem de REVAL-1 (T-059), com a proposta de ERRO para vazio e duplicidade com archive, AVISO para o resto.

### Revalidacao

- Claude Fable, familia diferente. Todos os itens reproduzidos em projeto minimo montado de `assets/` com `--strict --codigos`; os dois tracebacks reproduzidos com o `stderr` capturado. Nada nao confirmado. A transcricao e do Claude; o bruto do Codex esta ao lado.

### Por Que Nada Pegou Antes

- O que passou verde: `verify_repository.py` 44 de 44 em todas as versoes; sete fixtures com oracle exato.
- Mecanismo do ponto cego: o oracle exato prova que a fixture produz **exatamente** o que declara, e nada sobre o que o check deveria pegar fora dela. Fixture nasce por feature (2.2.0, 2.4.0), nunca por regra; e o documento "errado de um jeito que ninguem escreveu ainda" nunca entrou em fixture nenhuma.
- Conserto de portao proposto: o de REVAL-4.

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma ate a calibragem.

## 2026-09-03 - REVAL-3: o loop escreve o que o comando nao comprova em quatro caminhos, e perde trabalho em tres

**Achado:** REVAL-3

**Status:** aberto

**Proximo passo:** qualquer agente conserta os itens sem decisao (T-060, exige 2.5.2); usuario decide o que fazer com `--seco --agente` e com a truncagem do `(verifica:)` (T-061).

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 3. Gemini 3.7 Flash (`cursor-agent -p --mode ask --force --model gemini-3.7-flash-high`) atacou `loop.sh`, `loop_task.py` e `references/loop.md`. Claude rodou nove entradas hostis com agente falso (`s3-claude-hostil.txt`) antes de ler o Gemini, e depois conferiu os tres achados que nao tinha (`s3-claude-verifica-gemini.txt`).

### O Que Foi Encontrado

Evidencia que o comando nao comprova:

- **Comando com parenteses e truncado e o truncado e executado.** `VERIFICA_RE` para no primeiro `)`. `(verifica: python3 -c "print(1)")` vira `python3 -c "print(1"`, o portao roda isso e falha por sintaxe, e o mesmo regex no validador aceita a evidencia truncada.
- **`procedimento=` nao e o comando que rodou.** `loop.sh` captura o comando antes do agente e `cmd_fechar` rele a linha depois. Agente que troca `(verifica: bash portao.sh)` por `(verifica: true)` fecha com `procedimento=true; resultado=exit 0; suite-real-passou`, e `--strict` aceita.
- **`--seco --agente "claude -p"` grava `agente=claude -p`** sem o agente ter rodado. O comentario do codigo diz que `agente` e "fato conhecido com certeza".
- **`fechar` e `bloquear` apagam as sub-linhas preexistentes** da tarefa (notas, contexto), contra "nao sobrescreva conteudo existente sem preservar".

Trabalho perdido ou exit errado:

- **Saida de portao maior que o limite de argumento** (1.2MB no macOS) faz a tentativa 2 falhar com `Argument list too long`, e o loop reporta exit 4 "agente mal configurado".
- **Bytes fora de UTF-8 na saida do portao** derrubam `cmd_fechar` com traceback; portao verde, tarefa nao fecha, exit 1.
- **`.loop-pergunta` vazio**: exit 1 em vez de 3, tarefa nao bloqueada, arquivo fica no disco.
- Agente que remove o marcador `(verifica:)`: portao verde, fecho falha, exit 1.
- Agente que so apaga arquivo e sai 1: `find -newer` nao ve, exit 4.

Documentacao: a tabela de exit codes de `references/loop.md` nao tem o exit 4; `--agente` relativo com `--projeto` em outro diretorio falha depois do `cd`. Portao que mente (`true`) e por desenho, e a evidencia deixa visivel (`procedimento=true`), como `references/loop.md` ja diz.

### Disposicao

- Conserto direto, sem decisao (T-060): capturar a linha da tarefa junto com o comando no arranque e passar para `fechar` (ou `fechar` recusar se a linha mudou); preservar sub-linhas em `fechar`/`bloquear`; `errors="replace"` na leitura de saida e de pergunta; realimentacao por arquivo ou truncada ao mesmo limite do `resultado`; pergunta vazia vira exit 3 com pergunta "(vazia)" ou exit proprio, e o arquivo some; exit 4 documentado. Teste de mutacao para cada um.
- Decisao do usuario (T-061): `(verifica:)` com parenteses e mudanca de formato (ex: exigir o comando entre crases, ou aceitar ate o ultimo `)` da linha); `--seco` com `--agente` e proibir a combinacao ou nao gravar `agente=`.

### Revalidacao

- Claude Fable, familia diferente. Os nove cenarios de Claude e os tres do Gemini rodaram de verdade com `loop.sh` e agente falso; saidas em `docs/archive/revalidacao-2026-09-03/`. Nada nao confirmado.

### Por Que Nada Pegou Antes

- O que passou verde: `test_loop.py` 58 de 58, e tres bancadas reais com portao verde na tentativa 1.
- Mecanismo do ponto cego: a bateria cobre o caminho feliz de cada exit code e nunca entrada hostil; os agentes reais das bancadas eram cooperativos e os portoes curtos. A evidencia registra o que **a linha diz** no fim, e ninguem perguntou se a linha ainda era a mesma do inicio.
- Conserto de portao proposto: casos hostis em `test_loop.py` (parenteses, saida enorme, nao UTF-8, pergunta vazia, agente que edita a propria tarefa, sub-linhas preexistentes).

### Decisao Para Registrar Em DECISIONS.md

- Nenhuma ate o usuario decidir o formato de `(verifica:)`.

## 2026-09-03 - REVAL-4: o portao dos evals e cego para 29 dos 39 diagnosticos e para o prompt do loop

**Achado:** REVAL-4

**Status:** aberto

**Proximo passo:** qualquer agente escreve o manifesto de cobertura e as fixtures por codigo (T-065); usuario decide se quer piso fixo de verificacoes no `verify_repository.py` (aplicado hoje para a bateria do loop, com 58).

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Superficie 4, a mais importante. Claude executou 16 mutacoes com backup por `cp` antes de ler qualquer agente (`mutacoes-claude.txt`); Codex (mesmo perfil de REVAL-2), somente leitura, **previu** mutacoes e uma tabela de cobertura dos 39 codigos; Claude executou depois as 8 previsoes que ainda nao tinha rodado (`mutacoes-claude-rodada2.txt`). 24 mutacoes no total, cada uma revertida do backup e conferida por SHA-256.

### O Que Foi Encontrado

Mutacao que passa verde no `verify_repository.py` (44 de 44), com a promessa quebrada:

- Desligar `check_session` (M1), `check_em_dash` do validador (M2), `check_bridges` (M3), `check_evidence` (M5), `check_markers_values` (M9), `check_rotation` (M10): seis checks inteiros somem sem um unico FALHA. Codex previu os seis antes de ver o resultado.
- Remover a chamada de `verificar_fixtures` (M17): o resumo cai de 44 para 30 e o exit continua 0. Nao ha manifesto de etapas nem total esperado.
- Esvaziar `test_loop.py` (M18): imprime `0/0 verificacoes passaram`, exit 0, e o verificador aceita.
- Tirar `debate-project` do `FIXTURES` (M19): a fixture continua no disco e ninguem nota. Apagar `assets/docs/STACK.md` (M20): o destino e comparado com a fonte ja reduzida.
- Versao em prosa (`SKILL.md:186`, `CHANGELOG.md:11`) desatualizada (M8): so frontmatter, marcadores e heading do CHANGELOG sao conferidos.
- No prompt do `loop.sh`: mandar o agente trabalhar na `T-999` (M22), remover "nao apague o que falha" e a proibicao de editar memoria (M23): 58 de 58. A unica assercao sobre o conteudo do prompt e a realimentacao da falha. `references/loop.md` diz que essas regras estao no prompt **porque** o portao nao as pega; o teste do prompt tambem nao.
- `loop_task`: leftover de `.loop-pergunta` nao removido (M12), truncagem de `resultado` desligada (M13), `bloquear` aceitando tarefa ja bloqueada (M24): 58 de 58.

Cobertura positiva (tabela do Codex, conferida contra as mutacoes): **10 de 39** codigos tem fixture que acusa se o check sumir. A raiz em `--strict` sai limpa e nao cobre nenhum.

Pegou, como devia: `check_markers` (M4, via `ESTRUTURA-V1`), `check_waiting` (M6), `TASK-ID-DUPLICADO` (M7), `check_specs` (M11), `.loop-pergunta` ignorado (M14), secoes elegiveis (M15), ordem de captura do comando (M16), eval removido do `evals.json` (M21).

Efeitos colaterais achados pelo caminho, os dois de suspeita do Codex e confirmados por execucao: `verify_repository.py` afirma "nunca escreve no repositorio" e gravava `scripts/__pycache__` na fonte via `py_compile`, que o `install.sh` copiava para os tres destinos (6 arquivos por instalacao); e `loop_task.escrever`, da 2.5.1, troca o modo do `TASKS.md` de 664 para 600 porque `mkstemp` cria com 0600 e `os.replace` nao preserva. `evals.json` ainda pede marcador `v2.2.0` nos evals 1, 2, 3 e 5, e o eval 7 nao conhece os codigos da 2.5.0.

### Disposicao

- Aplicado hoje, sem bump (arquivos nao distribuidos): `verify_repository.py` confere os scripts com `ast.parse` e roda a bateria com `PYTHONDONTWRITEBYTECODE`, ganhou o check "nenhum `__pycache__` dentro da skill" e o piso de 58 verificacoes na bateria do loop; `test_loop.py` nao grava bytecode; `install.sh` apaga `__pycache__` do destino; `evals.json` em 2.5.1 com os codigos; README da skill corrigido. Mutacao M18 refeita depois: pega.
- Fica para T-065: manifesto de cobertura codigo-para-fixture com uma fixture por codigo (29 faltam), manifesto de etapas do verificador, inventario de fixtures no disco contra o `FIXTURES`, assercao do conteudo do prompt no `test_loop.py`, e a versao em prosa entrar em `verificar_versao`.
- Fica para T-060 (distribuido, exige 2.5.2): preservar o modo do arquivo em `escrever`, com teste.

### Revalidacao

- Claude executou; Codex previu as cegas. As previsoes bateram nas 8 que os dois cobriram, e o Codex ainda apontou as duas suspeitas que viraram achado. Familia diferente nos dois sentidos.

### Por Que Nada Pegou Antes

- O que passou verde: 44 de 44 e 58 de 58, lidos como "cobertura" em todas as sessoes desde a 2.2.0, inclusive nas tres rodadas de consenso de hoje.
- Mecanismo do ponto cego: o numero total e dinamico e nunca foi comparado com nada, entao verificacao que some nao e regressao; fixture so nasce quando um check nasce, e o contrato do validador nunca foi enumerado contra as fixtures; a bateria do loop assere exit code e arquivos, nunca o texto que o agente recebe. "Mutacao antes de portao novo" virou regra em `MEMORY.md` hoje, mas so para portao **novo**: ninguem mutacionou os antigos.
- Conserto de portao proposto: o manifesto de T-065, e a regra de que todo codigo em `CODIGOS` precisa de fixture que o produza, cobrada pelo proprio `verify_repository.py`.

### Decisao Para Registrar Em DECISIONS.md

- Proposta: "codigo de diagnostico sem fixture que o produza nao entra em `CODIGOS`". Depende do usuario.

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

**Status:** aberto

**Proximo passo:** usuario decide se `install.sh` deve avisar antes de sobrescrever destino editado e se deve virar copia atomica (T-067).

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
