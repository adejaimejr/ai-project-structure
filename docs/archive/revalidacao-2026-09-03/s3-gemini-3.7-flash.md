## Achados

### A-S3-1: `VERIFICA_RE` trunca silenciosamente comandos de `(verifica:)` que contem parenteses
- Onde: `docs/skills/ai-project-structure/scripts/validate_structure.py:68` (reusado em `docs/skills/ai-project-structure/scripts/loop_task.py:122`)
- Promessa: `AGENTS.md:116` e `references/loop.md:28` prometem que o loop extrai e executa integralmente o comando declarado em `(verifica: <comando>)`.
- Realidade: A regex `VERIFICA_RE = re.compile(r"\(verifica:\s*([^)]*)\)")` utiliza `[^)]*`, parando no primeiro parentese de fechamento `)`. Qualquer comando com parenteses (como subshells `(cd dir && pytest)`, comandos Python inline `python3 -c 'import sys; sys.exit(0)'` ou interpolacoes `$(...)`) e truncado no primeiro `)`. O `loop.sh` recebe um comando quebrado, executa no bash resultando em erro de sintaxe (`syntax error: unexpected end of file`), e o `loop_task.py fechar` grava o procedimento corrompido na evidencia.
- Reproducao:
```python
import re
VERIFICA_RE = re.compile(r"\(verifica:\s*([^)]*)\)")
line = "- T-001: Checagem (verifica: python3 -c \"import sys; sys.exit(0)\")"
print(VERIFICA_RE.search(line).group(1))
# Saida: python3 -c "import sys; sys.exit(0
```
- Severidade: alta; quebra comandos validos com parenteses inline e subshells, impedindo a execucao correta do portao.

---

### A-S3-2: Bytes nao-UTF-8 na saida do portao quebram `loop_task.py fechar` com `UnicodeDecodeError`, abortando fecho com exit 1
- Onde: `docs/skills/ai-project-structure/scripts/loop_task.py:212` (e tambem `loop_task.py:238`)
- Promessa: `AGENTS.md:272` e `references/loop.md:32` prometem que, quando o comando do portao sai 0, a tarefa e movida para `Concluidas` com evidencia. O exit code 1 e reservado para "erro de uso ou tarefa nao elegivel".
- Realidade: `loop_task.py` le o arquivo de saida usando `Path(args.saida).read_text(encoding="utf-8")` sem tratamento de erro (`errors="replace"`). Se o comando do portao emitir bytes fora da tabela UTF-8 (como caracteres Latin-1 ou saidas binarias de ferramentas de teste), o Python lanca `UnicodeDecodeError`. A excecao nao e capturada pelo bloco `try/except Erro`, o script termina com stack trace e exit code 1, e o `loop.sh` aborta sem mover a tarefa nem gravar a evidencia, apesar de o portao ter saido 0.
- Reproducao:
```bash
python3 docs/skills/ai-project-structure/scripts/loop_task.py fechar /tmp/proj T-001 --saida /tmp/saida_binaria.txt --codigo 0
# Traceback (most recent call last):
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 3: invalid start byte
```
- Severidade: alta; faz uma rodada valida e bem-sucedida falhar com erro interno (exit 1), deixando a tarefa aberta.

---

### A-S3-3: Arquivo `.loop-pergunta` vazio aborta com exit 1 em vez de 3, nao bloqueia a tarefa e deixa arquivo orfao no disco
- Onde: `docs/skills/ai-project-structure/scripts/loop.sh:160-166` e `docs/skills/ai-project-structure/scripts/loop_task.py:239-240`
- Promessa: `AGENTS.md:280` e `references/loop.md:193-195` prometem: "Achou [.loop-pergunta]: o helper move a tarefa para '## Aguardando Usuario' com `**Pergunta:**` preenchida, o arquivo e apagado e a rodada termina com codigo 3. O portao nem chega a rodar."
- Realidade: Se o agente criar o arquivo `.loop-pergunta` vazio (ex: `touch .loop-pergunta`), `loop_task.py bloquear` lanca `Erro("arquivo de pergunta vazio; nao ha o que registrar.")` e sai com status 1. No `loop.sh:163`, o comando `python3 "$HELPER" bloquear ... || exit 1` captura a falha e dispara `exit 1` antes da linha `rm -f "$SINAL"`. A tarefa nao e movida para `Aguardando Usuario`, o arquivo `.loop-pergunta` permanece no disco e o script encerra com exit 1 (erro de uso) em vez do exit 3 contratado.
- Reproducao:
```bash
# Executar loop.sh com agente que apenas cria o arquivo via touch
touch .loop-pergunta
# loop.sh exibe:
# O agente sinalizou falta de contexto. Registrando a pergunta e parando.
# [ERRO] arquivo de pergunta vazio; nao ha o que registrar.
# Exit code: 1 (arquivo .loop-pergunta permanece na raiz)
```
- Severidade: alta; quebra o tratamento de sinalizacao de falta de contexto, emite exit code incorreto e deixa o repositorio em estado sujo.

---

### A-S3-4: `loop_task.py fechar` e `bloquear` destroem silenciosamente sub-linhas preexistentes da tarefa
- Onde: `docs/skills/ai-project-structure/scripts/loop_task.py:80-84`, `218-226` e `246-253`
- Promessa: `AGENTS.md:66` estabelece "Nao sobrescreva conteudo existente sem preservar, mesclar ou pedir confirmacao." e `AGENTS.md:286` reforca "Perder informacao e decisao de quem pediu a tarefa, nunca sua."
- Realidade: A funcao `achar_tarefa` inclui todas as sub-linhas indentadas (`\s+[-*]\s+`) no intervalo `[inicio, fim)`. Em `cmd_fechar`, `restante = linhas[:inicio] + linhas[fim:]` apaga todas as sub-linhas originais da tarefa, e `novas` reconstroi apenas `- {hoje} {linha}` e a sub-linha `Evidencia:`. Quaisquer notas de contexto, sub-tarefas ou observacoes anexadas abaixo da tarefa em `docs/TASKS.md` sao irremediavelmente apagadas. O mesmo ocorre em `cmd_bloquear`.
- Reproducao:
```markdown
# Antes em TASKS.md:
- T-001: Tarefa com notas (verifica: echo ok)
  - Cuidado: nao alterar a variavel X
  - Contexto: ver spec 0001

# Apos loop_task.py fechar:
- 2026-09-03 T-001: Tarefa com notas (verifica: echo ok)
  - Evidencia: tipo=comando; procedimento=echo ok; resultado=exit 0; ok
# As duas notas foram apagadas silenciosamente.
```
- Severidade: media; perda irreversivel de informacoes e anotacoes estruturadas que o usuario mantinha na tarefa.

---

### A-S3-5: `--seco --agente "CMD"` grava falsa atribuicao de agente (`agente=CMD`) na evidencia sem executar o agente
- Onde: `docs/skills/ai-project-structure/scripts/loop.sh:137`, `177-179` e `loop_task.py:214-220`
- Promessa: `AGENTS.md:270` afirma que "o loop escreve apenas o que um comando comprova", e o comentario em `loop_task.py:214` destaca que "`agente` e fato conhecido com certeza: foi o loop que invocou aquele comando."
- Realidade: Ao rodar `loop.sh --seco --agente "claude -p"`, o script nao invoca o agente (`(modo seco: agente nao chamado)`), roda o portao diretamente e, ao passar, repassa `--agente "$AGENTE"` para `loop_task.py fechar`. A evidencia gerada registra `agente=claude -p;`, atestando falsamente no historico que o Claude produziu a alteracao.
- Reproducao:
```bash
./loop.sh --tarefa T-001 --seco --agente "claude -p" --projeto /tmp/proj
# Resultado em docs/TASKS.md:
# - 2026-09-03 T-001: Tarefa teste (verifica: echo ok)
#   - Evidencia: tipo=comando; agente=claude -p; procedimento=echo ok; resultado=exit 0; ok
```
- Severidade: media; viola a garantia de que a evidencia contem apenas fatos comprovados, adulterando a rastreabilidade do autor da mudanca.

---

### A-S3-6: Discrepancia entre portao executado e procedimento gravado se o agente alterar `(verifica:)` no `TASKS.md`
- Onde: `docs/skills/ai-project-structure/scripts/loop.sh:74`, `170` e `loop_task.py:204`
- Promessa: `AGENTS.md:270` e `references/loop.md:32` prometem que a evidencia registra `procedimento` com o comando declarado executado pelo portao.
- Realidade: O `loop.sh` extrai e armazena em variavel shell o `COMANDO` na inicializacao (linha 74) e executa esse comando em `bash -c "$COMANDO"` (linha 170). Porem, `loop_task.py fechar` reabre `docs/TASKS.md` em tempo de fecho (linha 204) e extrai `(verifica:)` da linha atual. Se o agente modificou a linha da tarefa durante a rodada (ex: alterou de `echo original` para `comando_falso`), o `loop.sh` executou `echo original`, mas a evidencia gravada em `docs/TASKS.md` registra `procedimento=comando_falso; resultado=exit 0; original`.
- Reproducao:
```bash
# Agente executa sed trocando "(verifica: echo original)" por "(verifica: comando_falso)"
# loop.sh roda o portao inicial "echo original" (passa)
# loop_task.py fechar grava:
# - Evidencia: tipo=comando; procedimento=comando_falso; resultado=exit 0; original
```
- Severidade: media; gera evidencia inconsistente onde o procedimento registrado nao corresponde ao comando executado pelo portao.

---

### A-S3-7: Saida do portao sem limite de tamanho em `FALHA_ANTERIOR` estoura `ARG_MAX` na tentativa 2 e mascara falha como exit 4
- Onde: `docs/skills/ai-project-structure/scripts/loop.sh:129-135`, `185`
- Promessa: `references/loop.md:31` promete que a saida do comando com falha volta como contexto para a tentativa seguinte.
- Realidade: O `loop_task.py` limita a saida a 400 caracteres para `TASKS.md` (`RESULTADO_MAX = 400`), mas o `loop.sh` le todo o `saida.txt` para `FALHA_ANTERIOR="$(cat "$TMP/saida.txt")"` sem truncagem e interpola no `$PROMPT` passado via argumento CLI. Se o portao quebrar emitindo logs volumosos (ex: 3MB de dump/traceback), a chamada `"${AGENTE_ARGS[@]}" "$PROMPT"` na tentativa 2 falha no sistema operacional com `Argument list too long` (`E2BIG`). O `loop.sh` captura o erro, nao encontra arquivos alterados e encerra com `exit 4`, exibindo mensagem enganosa que culpa a configuracao da CLI do agente.
- Reproducao:
```bash
# Portao que emite 3MB de texto e sai 1:
# Na tentativa 2:
# loop.sh: line 141: .../agent.sh: Argument list too long
# [ERRO] o agente saiu com codigo 1 e nao alterou nenhum arquivo.
# Exit code: 4
```
- Severidade: media; inviabiliza a realimentacao em suites de teste ou comandos com logs verbosos, interrompendo o ciclo abruptamente.

---

### A-S3-8: Tabela oficial de exit codes em `references/loop.md` omite o exit code 4
- Onde: `docs/skills/ai-project-structure/references/loop.md:80-87`
- Promessa: `references/loop.md` define a especificacao dos exit codes sob a secao "Exit codes, distintos de proposito para dar para ramificar por fora:".
- Realidade: A tabela em `references/loop.md` documenta apenas os codigos 0, 1, 2 e 3. O exit code 4 ("o agente falhou e nao mexeu em nada; provavelmente esta mal configurado"), implementado em `loop.sh:27, 155` e citado no `SKILL.md:230`, foi omitido da tabela contratual em `references/loop.md`.
- Reproducao: Conferencia de `references/loop.md:80-87` em relacao a `loop.sh:22-28`.
- Severidade: baixa; inconsistencia na documentacao de referencia de contratos publicos da skill.

---

### A-S3-9: `--agente` com caminho relativo falha quando `--projeto` aponta para outro diretorio
- Onde: `docs/skills/ai-project-structure/scripts/loop.sh:68-71`, `142`
- Promessa: `loop.sh` permite combinar `--agente` e `--projeto DIR` para operar em projetos localizados em outros caminhos.
- Realidade: A linha 70 valida a existencia do binario com `command -v "${AGENTE_ARGS[0]}"` no diretorio corrente (`$PWD`). Porem, a linha 142 executa `( cd "$PROJETO" && "${AGENTE_ARGS[@]}" "$PROMPT" )`. Se o usuario passar um script relativo (ex: `--agente "./meu_agente.sh"` ou `--agente "bin/runner"`), o comando falha apos o `cd "$PROJETO"` com `No such file or directory`, e o script para com exit 4.
- Reproducao:
```bash
# Estando em /tmp com meu_agente.sh no PWD:
loop.sh --tarefa T-001 --agente "./meu_agente.sh" --projeto /tmp/outro_projeto
# Saida: line 141: ./meu_agente.sh: No such file or directory
# Exit code: 4
```
- Severidade: baixa; falha de resolucao de caminhos relativos ao desacoplar PWD de `--projeto`.

---

## Suspeitas nao demonstradas
- **Condicao de corrida por resolucao de mtime no `find -newer` de `loop.sh:146`**: Em sistemas de arquivos com timestamp de 1 segundo (ex: certos volumes FAT, NFS ou ext3 sem sub-second), se o agente executar e modificar arquivos no exato mesmo segundo em que a `MARCA` foi criada, o teste `find "$PROJETO" -type f -newer "$MARCA"` pode retornar vazio caso `mtime(arquivo) == mtime(MARCA)`. Nao foi demonstrado deterministicamente no ambiente macOS atual porque o APFS opera com resolucao de nanossegundos.

---

## Tarefas conhecidas
- T-054: continua valida? sim. `check_consensus_declaration` retorna silenciosamente sem emitir diagnostico quando `Rodada` esta ausente e usa `re.match` em vez de `fullmatch`, permitindo sufixos espurios em `N de N`.
- T-055: continua valida? sim. O bloco `Modelo De Debate` no `docs/CONSENSUS.md` da raiz nao traz os campos declarativos `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`.
- T-056: continua valida? sim. `spec_overview` usa `line.strip().startswith("- ")` e conta sub-itens indentados da secao `Perguntas Abertas` como perguntas adicionais.
- T-058: continua valida? sim. `loop.sh` utiliza nome fixo `.loop-pergunta`, remove arquivos de rodadas anteriores no arranque e nao implementa lock contra execucoes simultaneas.

---

## Inventario
Arquivos lidos por inteiro:
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md`
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/loop.sh`
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/loop_task.py`
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/references/loop.md`
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/TASKS.md`
- `/private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/validate_structure.py` (funcoes `collect_tasks`, `is_placeholder`, `squeeze`, `evidence_lines`, `check_tasks`, `check_markers_values`, `check_waiting`, `check_evidence`, `spec_overview`, `check_consensus_declaration`, `check_consensus_achado` e constantes de regex).

---

## Demonstracao em projeto temporario

Execucao de `loop.sh` em projeto isolado fora do repositorio com agente falso em shell:

```bash
=== SAIDA DO LOOP.SH (exit code 0) ===
Tarefa:  T-001
Projeto: /private/tmp/eval_demo/meu-projeto
Portao:  grep -q "^v1.0.0$" versao.txt
Limite:  3 tentativa(s)

=== Tentativa 1 de 3 ===
--- portao: grep -q "^v1.0.0$" versao.txt
--- portao saiu com codigo 0
T-001 movida para Concluidas com evidencia de comando.

Portao verde na tentativa 1. Tarefa fechada com evidencia de comando.
A entrada de SESSION.md continua sendo sua: o loop nao escreve la.
```

```markdown
=== DOCS/TASKS.MD RESULTANTE ===
# TASKS

- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-01)`.

## Em Andamento


## Proximas Tarefas

- (Vazio.)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- 2026-09-03 T-001: Criar arquivo versao.txt com o conteudo v1.0.0 (prioridade: alta) (verifica: grep -q "^v1.0.0$" versao.txt)
  - Evidencia: tipo=comando; agente=/private/tmp/eval_demo/agente_falso.sh; procedimento=grep -q "^v1.0.0$" versao.txt; resultado=exit 0; (sem saida)
```
