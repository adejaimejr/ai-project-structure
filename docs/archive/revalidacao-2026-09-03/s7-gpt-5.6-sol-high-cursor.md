## Achados
### A-S7-1: instalação segura não é transacional
- Onde: `docs/skills/ai-project-structure/install.sh:22,67-80`
- Promessa: rodar novamente “sobrescreve com seguranca”.
- Realidade: execuções completas são idempotentes, mas uma falha intermediária deixa versões misturadas ou diretórios removidos.
- Reproducao: duas instalações completas produziram `arvores_iguais=True; arquivos=99`. Com falha forçada no terceiro `cp`:
```text
exit=42
SKILL.md: existe=True, igual_fonte=True
assets/AGENTS.md: existe=True, igual_fonte=True
agents/openai.yaml: existe=False
scripts/loop_task.py: antigo=True
references/loop.md: antigo=True
```
Uma reinstalação completa recuperou o destino. Em destino divergente:
```text
SKILL_restaurado=True
extra_raiz_sobrou=True
extra_em_assets_sobrou=False
```
- Severidade: media, porque a instalação é reversível, mas uma interrupção deixa a skill quebrada ou internamente incoerente.

### A-S7-2: verificador escreve e distribui `__pycache__`
- Onde: `docs/skills/ai-project-structure/evals/verify_repository.py:25,394-405,453-464`; `docs/skills/ai-project-structure/install.sh:75-76`
- Promessa: o verificador “Nunca escreve no repositorio”; a instalação copia somente o necessário em runtime.
- Realidade: `py_compile` cria `.pyc` dentro de `scripts/__pycache__`; `cp -R scripts` distribui esse cache. A função `hashes` ignora `__pycache__`, ocultando o artefato.
- Reproducao:
```text
$ verificar_scripts(...) em copia temporaria
[OK] scripts/validate_structure.py compila
[OK] scripts/loop_task.py compila
scripts/__pycache__/loop_task.cpython-314.pyc
scripts/__pycache__/validate_structure.cpython-314.pyc
```
Depois da instalação:
```text
cache_copiado=True; conteudo=cache-sentinela
```
Mesmo assim, `verificar_install` retornou:
```text
[OK] destino identico a fonte canonica
Resumo: 4/4 verificacoes passaram.
```
- Severidade: media, porque viola a promessa de somente leitura e instala artefatos locais específicos da versão do Python.

### A-S7-3: instalação manual produz pacote incompleto
- Onde: `docs/skills/ai-project-structure/README.md:74-82`; `docs/skills/ai-project-structure/SKILL.md:207-241`
- Promessa: a seção apresenta uma instalação manual funcional da skill.
- Realidade: copia somente `SKILL.md`, `assets` e `agents`, omitindo `scripts` e `references`, necessários para validar, atualizar, usar specs e operar o loop.
- Reproducao:
```text
$ cp -R SKILL.md assets agents <destino>/
SKILL.md=True
assets=True
agents=True
scripts/validate_structure.py=False
references/atualizacao.md=False
references/specs.md=False
references/loop.md=False

python: can't open file '<destino>/scripts/validate_structure.py'
exit_validador_manual=2
```
- Severidade: media, porque vários modos anunciados ficam inutilizáveis.

### A-S7-4: versão exibida ao usuário não é conferida
- Onde: `docs/skills/ai-project-structure/SKILL.md:186`; `docs/skills/ai-project-structure/CHANGELOG.md:11`; `docs/skills/ai-project-structure/evals/verify_repository.py:308-329`
- Promessa: o verificador confere coerência de versão; o scaffold reporta sua versão.
- Realidade: somente frontmatter, marcadores e heading do CHANGELOG são verificados. Texto em prosa pode envelhecer silenciosamente.
- Reproducao: numa cópia, troquei os dois textos em prosa para `9.9.9`, mantendo os campos canônicos:
```text
[OK] SKILL.md declara version no frontmatter
[OK] marcadores em v2.5.1
[OK] CHANGELOG.md da skill tem a secao 2.5.1
Resumo: 3/3 verificacoes passaram.

SKILL.md:186: versao da estrutura: 9.9.9
CHANGELOG.md:11: Marcadores dos tres blocos em v9.9.9
```
Outras ocorrências em prosa não conferidas: `docs/TASKS.md:51`, `docs/SESSION.md:54,77`, `docs/PROMPTS.md:37,42`, `docs/DECISIONS.md:38` e `docs/CHANGELOG.md:7`.
- Severidade: baixa, porque a versão atual está coerente, mas o próximo release pode reportar versão errada.

### A-S7-5: README e ajuda omitem conteúdo existente
- Onde: `docs/skills/ai-project-structure/README.md:30,46-53`; `docs/skills/ai-project-structure/install.sh:32-41`
- Promessa: a árvore descreve as fixtures e “Opcoes” descreve a interface do instalador.
- Realidade: faltam as fixtures `achado-project` e `debate-project`; faltam as flags `--global`, `--all`, `-h` e `--help`. A própria saída de `--help` também omite essas flags.
- Reproducao:
```text
fixtures=achado-project,aguardando-project,broken-project,debate-project,v1-project

$ bash install.sh --help
# não lista --global, --all ou --help
```
- Severidade: baixa, porque não quebra execução, mas esconde capacidades públicas e deixa o inventário incorreto.

### A-S7-6: metadado Codex é atribuído ao padrão errado
- Onde: `docs/skills/ai-project-structure/agents/openai.yaml:1`
- Promessa: `agents/openai.yaml` é “parte do Agent Skills Open Standard”.
- Realidade: a documentação embutida no Codex 0.152.1 o chama de configuração “extended, product-specific”.
- Reproducao:
```text
$ strings <binario-codex> | rg 'extended, product-specific|allow_implicit_invocation'
agents/openai.yaml is an extended, product-specific config
policy.allow_implicit_invocation
```
- Severidade: baixa, porque o Codex reconhece o arquivo corretamente; o erro é de classificação e portabilidade documental.

## Suspeitas nao demonstradas
- Codex CLI 0.152.1: `codex --help` não apresenta subcomando `skills`; `codex help skills` retorna `unrecognized subcommand`, exit 2. O binário valida `policy.allow_implicit_invocation` como booleano e documenta: `false` não injeta a skill no contexto por padrão, mas `$skill` continua funcionando; o padrão é `true`. O cache em `~/.codex/plugins/cache` contém exemplos oficiais com ambos os valores. Não executei uma sessão real para observar a seleção automática, pois isso escreveria estado fora da cópia.
- `NAO_DISTRIBUIDO` está coerente entre código, comentário e README: `evals`, `install.sh`, `README.md` e `CHANGELOG.md`. A falha demonstrada é `__pycache__`, que não está nessa lista, é copiado e depois ignorado pelo oracle.
- `--uninstall`, `--uninstall --project`, `--uninstall --claude` e `--all --project` funcionaram. A instalação por projeto também funcionou sem `.git`.
- Os 39 valores de `CODIGOS`, os flags do validador e os exit codes 0/1 conferem com o README e os docstrings.
- Não encontrei entrada do CHANGELOG que descreva comportamento atualmente ausente, além da cobertura incompleta de versão registrada em A-S7-4.

## Tarefas conhecidas
- T-054: continua valida? sim, `Rodada` ausente retorna sem diagnóstico e o valor usa `re.match`.
- T-055: continua valida? sim, o Modelo De Debate da raiz continua sem os três campos declarativos.
- T-056: continua valida? sim, `line.strip()` ainda elimina a indentação antes de contar perguntas.
- T-058: continua valida? sim, continua usando `.loop-pergunta` fixo, removido no início, sem lock.

## Inventario
- `AGENTS.md`
- `docs/README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/SESSION.md`
- `docs/MEMORY.md`
- `docs/TASKS.md`
- `docs/ARCHITECTURE.md`
- `docs/QUALITY.md`
- `docs/skills/ai-project-structure/install.sh`
- `docs/skills/ai-project-structure/agents/openai.yaml`
- `docs/skills/ai-project-structure/README.md`
- `docs/skills/ai-project-structure/CHANGELOG.md`
- `docs/skills/ai-project-structure/SKILL.md`
- `docs/skills/ai-project-structure/evals/verify_repository.py`
- `@openai/codex/bin/codex.js`
- Os dois `README.md` instalados do pacote Codex 0.152.1.
