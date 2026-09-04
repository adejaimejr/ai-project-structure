# Fluxo De Atualizacao

Use este fluxo quando o destino ja usa a estrutura (tem `AGENTS.md` e `docs/SESSION.md` com entradas reais) e o usuario quer atualiza-la para a versao atual da skill.

Sequencia:

```text
DETECTAR → (ja atualizado? → RELATAR + VALIDAR) → PLANEJAR → APLICAR POR BLOCO
→ PONTES → NOVOS ARQUIVOS → MIGRAR TASKS → REGISTRAR → VALIDAR
```

## Invariantes (valem em todos os passos)

- **Nada e sobrescrito sem confirmacao por item.** Sem resposta do usuario, nada muda.
- Nunca toque conteudo fora dos marcadores em `AGENTS.md` (excecao: o resgate v1, com consentimento explicito).
- Conteudo abaixo de "## Regras Do Projeto" e intocavel.
- Nunca inicialize repositorio git.

## 1. DETECTAR

Leia o `AGENTS.md` do destino e procure `<!-- ai-project-structure:core:start vX.Y.Z -->`.

- Marcador presente → versao do projeto = `X.Y.Z`.
- Marcador ausente, mas estrutura reconhecivel (`AGENTS.md` + `docs/SESSION.md`) → **v1**.

Compare com a versao no frontmatter do `SKILL.md` desta skill.

## 2. JA ATUALIZADO?

Versoes iguais: informe o usuario, ofereca rodar o validador (`scripts/validate_structure.py`) e encerre.

## 3. PLANEJAR

Monte a lista de acoes e **mostre ao usuario antes de tocar qualquer arquivo**:

- blocos de `AGENTS.md` a atualizar (core; specs, se existir);
- pontes (`CLAUDE.md`/`GEMINI.md`) divergentes do template atual;
- arquivos novos disponiveis (ex: `docs/specs/README.md`, se for ativar o modulo);
- migracao de `TASKS.md` para IDs `T-NNN` (se ainda nao usa).

## 4. APLICAR POR BLOCO (`AGENTS.md`)

### v1 → v2 (sem marcadores)

Mostre o diff entre o `AGENTS.md` atual do projeto e o bloco `core` do template da versao 2. Pergunte:

- **(a) substituir pelo bloco da versao 2** - secoes que existem no arquivo do usuario mas nao no template sao preservadas: mova cada uma para dentro de "## Regras Do Projeto", abaixo do bloco, como item ou como subsecao `###`. Nunca crie uma secao `##` irma de "## Regras Do Projeto". Avise o usuario para revisar o resultado.
- **(b) manter como esta** - o projeto continua v1; registre a pendencia como tarefa em `TASKS.md`.

### v2 → v2.x (com marcadores)

Para cada bloco (`core`; `specs` e `loop`, se existirem no projeto):

- conteudo identico ao template atual → pule em silencio;
- conteudo diferente → mostre o diff **so do bloco** e pergunte: aplicar / pular / decidir depois. Bloco pulado vira tarefa em `TASKS.md`.

Bloco `specs` ausente e usuario nao usa specs → nao ofereca a insercao; apenas mencione que o modulo existe.

Bloco `loop` ausente → **nao ofereca a insercao**. O modulo de loop so entra a pedido explicito do usuario e depois do portao de `QUALITY.md` (ver `loop.md`). Atualizar nao e ocasiao para ativar modulo novo.

## 5. PONTES

`CLAUDE.md` ou `GEMINI.md` diferentes do template atual: mostre o diff e pergunte substituir/manter (lembre a regra: pontes sao imutaveis e nao carregam regras proprias).

## 6. NOVOS ARQUIVOS

Ofereca apenas arquivos que **nao existem** no destino. **Nunca** sobrescreva `docs/*.md` com dados do usuario (SESSION, MEMORY, TASKS, etc.) pelo template.

A unica excecao e o passo 7b, e ela e **aditiva**: acrescenta secao e marcador ao `docs/TASKS.md` sem apagar, reescrever ou reordenar nada que ja estava la. Qualquer outra edicao em arquivo do usuario continua fora.

## 7. MIGRAR TASKS

Se `docs/TASKS.md` nao usa IDs `T-NNN`, ofereca atribuir `T-001, T-002, ...` as tarefas existentes na ordem em que aparecem (Em Andamento primeiro, depois Proximas, depois Concluidas). Recusado → siga em frente; o validador emitira apenas um INFO "formato v1".

Nas linhas de "Concluidas", quando a data de conclusao for conhecida, prefixe a
linha com `AAAA-MM-DD`. Quando nao souber a data, deixe a linha sem data: ela
nao e cobrada pela convencao de evidencia.

## 7b. ADOTAR AS CONVENCOES 2.2.0

Ao atualizar um projeto que vem de 2.1.0 ou anterior:

- adicione a secao `## Aguardando Usuario` em `docs/TASKS.md`, entre "Proximas Tarefas" e "Concluidas", se ainda nao existir;
- adicione ao cabecalho de `docs/TASKS.md` o marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` com a **data da atualizacao**, nunca uma data anterior;
- **nao escreva evidencia em tarefa ja concluida.** A regra nao e retroativa: linha antiga fica como esta, e o validador nao a cobra. Inventar evidencia para historico transforma registro em alegacao falsa;
- **nao preencha os campos declarativos de consenso em entradas antigas** de `docs/CONSENSUS.md` pelo mesmo motivo. Da proxima entrada em diante, use `**Metodo:**`, `**Exposicao previa a outras posicoes:**` e `**Rodada:** N de N`;
- procure tarefas que **ja estavam paradas esperando o usuario** e ofereca mover cada uma para a secao nova. Sem isso a secao nasce vazia e a convencao nao pega no projeto. Use a pergunta e a data que ja estao escritas na tarefa: se a tarefa nao diz qual e a pergunta, **pergunte ao usuario**, nao deduza. Recusado, a tarefa fica onde esta.

## 7c. ADOTAR AS CONVENCOES 2.4.0

Ao atualizar um projeto que vem de 2.3.0 ou anterior:

- acrescente ao `docs/CONSENSUS.md` do destino as secoes "Achado", "Ponto Cego Da Validacao Cruzada" e "Modelo De Achado" do template, **preservando os registros existentes**;
- **nao converta entrada antiga em achado.** Entrada que ja esta escrita como debate continua debate: o formato de achado vale da proxima entrada em diante, e o validador so cobra os campos novos de quem declarar `**Achado:**`;
- o teto de tres rodadas saiu. Entrada antiga com `**Rodada:** N de 3` fica como esta; da proxima em diante use `N de N`, e da quarta rodada em diante declare `**Pendente da rodada anterior:**`.

## 8. REGISTRAR

- Atualize `vX.Y.Z` nos marcadores aplicados.
- Nova entrada em `docs/SESSION.md` do destino: o que foi aplicado e o que foi pulado.
- Linha em `docs/CHANGELOG.md` do destino.
- Blocos/itens pulados → tarefas em `docs/TASKS.md`.

## 9. VALIDAR

Rode `python3 <dir-desta-skill>/scripts/validate_structure.py <destino>` e reporte o resultado ao usuario.
