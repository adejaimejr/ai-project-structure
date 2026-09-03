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
