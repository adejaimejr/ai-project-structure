O bloco core da raiz e o de `assets/AGENTS.md` sao identicos (13101 bytes). Os buracos abaixo foram rodados de verdade em `/tmp/aps-s1-core-review/`, copiando `assets/` e preenchendo `(convencoes-2-2-0-desde: 2026-09-01)`, salvo o caso do placeholder.

## Achados

### A-S1-1: cobranca de evidencia some se a linha concluida nao tem data
- Onde: `docs/skills/ai-project-structure/scripts/validate_structure.py:766-775`; contrato em `AGENTS.md:110-119`
- Promessa: "Toda tarefa movida para `## Concluidas` em `TASKS.md` carrega uma sub-linha" `Evidencia:`; o modelo de linha e `AAAA-MM-DD T-001: ...`. O `SKILL.md:20` diz que a estrutura cobra isso desde 2.2.0.
- Realidade: sem prefixo de data, `done_date` fica `None` e o `if done_date is not None and done_date >= adopted` nao dispara. `T-001` em Concluidas, sem data e sem `Evidencia:`, passa em `--strict`.
- Reproducao: em `/tmp/aps-s1-core-review/02-concluida-sem-data-sem-evidencia/docs/TASKS.md`:

```
## Concluidas
- T-001: Trabalho concluido sem data e sem evidencia.
```

`python3 docs/skills/ai-project-structure/scripts/validate_structure.py /tmp/aps-s1-core-review/02-concluida-sem-data-sem-evidencia --strict` → exit 0, 0 erros, 0 avisos.
- Severidade: alta. E o portao da evidencia de fechamento, e um omitir a data o desliga por completo.

### A-S1-2: o validador nao confere a forma da evidencia
- Onde: `validate_structure.py:121` e `569-570` + `764-775`; contrato em `AGENTS.md:110-121`
- Promessa: o exemplo obrigatorio e `tipo=comando; procedimento=...; resultado=...`. "O validador confere a forma da evidencia, nunca o conteudo." O aviso de ausencia ate escreve `(tipo=; procedimento=; resultado=).`
- Realidade: basta uma sub-linha cujo texto, depois de `normalize`, comeca com `evidencia:`. Os tres campos nao sao exigidos. `tipo=` so e olhado se ja existir (e so para valor fora do conjunto).
- Reproducao: `/tmp/aps-s1-core-review/01-evidencia-sem-forma/docs/TASKS.md`:

```
- 2026-09-03 T-001: Trabalho concluido.
  - Evidencia: copiei e colei um texto qualquer.
```

`--strict` → exit 0. Controle: a mesma tarefa com `(verifica: pytest -q)` e `resultado=passou` (sem o texto `pytest -q`) acusa `EVIDENCIA-SEM-RESULTADO` (caso 29, exit 1). A forma prometida so e cobrada nesse recorte do `(verifica:)`.
- Severidade: alta. A frase "confere a forma" e falsa para o caso geral, que e o que o contrato mostra no bloco de exemplo.

### A-S1-3: travessao nao e acusado em qualquer ocorrencia
- Onde: `AGENTS.md:62`; docstring `validate_structure.py:236` ("proibido em qualquer texto"); implementacao `235-255`; `CHANGELOG.md` da skill, secao 2.0.0: "o validador acusa qualquer ocorrencia como erro"
- Promessa: qualquer ocorrencia de U+2014 em textos do projeto.
- Realidade: so `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e `docs/**/*.md`. `README.md` na raiz, `.py` e qualquer outro texto fora desses caminhos passam.
- Reproducao: `/tmp/aps-s1-core-review/09-travessao-readme-raiz/README.md` com U+2014 entre "teste" e "com"; `--strict` exit 0. `/tmp/aps-s1-core-review/10-travessao-py/app.py` idem, exit 0. Controle: o mesmo caractere em `docs/TASKS.md` (caso 11) → `[ERRO] [TRAVESSAO]` exit 1.
- Severidade: media. A frase e absoluta; a varredura e um subconjunto de Markdown. Neste repositorio o `README.md` da raiz e texto de produto.

### A-S1-4: `(verifica: )` vazio satisfaz o contrato por vacuidade
- Onde: `AGENTS.md:118`; `validate_structure.py:67` (`VERIFICA_RE`) e `742-762`
- Promessa: "declarado, vira contrato: a evidencia da tarefa concluida precisa registrar o resultado daquele comando."
- Realidade: `[^)]*` aceita comando vazio. `squeeze` vira `""`. A guarda `command not in joined` e verdadeira para qualquer evidencia, porque a string vazia esta contida em qualquer texto. Com `resultado=` presente, nao ha `EVIDENCIA-SEM-RESULTADO`.
- Reproducao: `/tmp/aps-s1-core-review/22-verifica-vazio/docs/TASKS.md`:

```
- 2026-09-03 T-001: Fechou com verifica vazio. (verifica: )
  - Evidencia: tipo=comando; procedimento=nada; resultado=ok
```

`--strict` → exit 0.
- Severidade: media. E o unico caminho de evidencia que o contrato chama de ERRO, e ele se deixa anular com um marcador oco.

### A-S1-5: cerca de codigo aberta apaga as checagens de TASKS.md
- Onde: `validate_structure.py:143-153` (`strip_fences`) chamado em `collect_tasks` (`509`)
- Promessa: unicidade de ID, evidencia, aguardando com pergunta, `(verifica:)`. Tudo isso corre sobre o texto ja passado por `strip_fences`.
- Realidade: um ` ``` ` sem par no arquivo deixa `in_fence` verdadeiro ate o proximo fence (ou ate o fim). Tarefas, evidencias e IDs nesse trecho deixam de existir para o validador.
- Reproducao: `/tmp/aps-s1-core-review/17-cerca-aberta-esconde-tarefas/docs/TASKS.md` tem um fence extra antes de `## Em Andamento` e, no fim:

```
## Concluidas
- 2026-09-03 T-099: Escondida na cerca sem evidencia.
```

`--strict` → exit 0, embora a linha seja exatamente o caso que A-S1-1/A-S1-2 dizem que deveria ser cobrado.
- Severidade: media. Nao e so um parser chato: e um jeito de o portao ficar verde apagando visibilidade, o inverso da regra de nao apagar o que falha.

### A-S1-6: Aguardando Usuario cobra so a pergunta
- Onde: `AGENTS.md:77`; `SKILL.md:21`; `validate_structure.py:704-717`
- Promessa: a tarefa travada vai para `## Aguardando Usuario` "com `**Pergunta:**`, `**Resposta:** (A preencher.)` e o marcador `(bloqueada: AAAA-MM-DD)`". O `SKILL.md` diz que a estrutura cobra a secao "com a pergunta registrada e um campo para a resposta".
- Realidade: `check_waiting` e ERRO so se faltar uma sub-linha que comece com `**pergunta:**`. `**Resposta:**` e `(bloqueada:)` nao sao exigidos. `(bloqueada:)` so e validado se ja estiver presente.
- Reproducao: `/tmp/aps-s1-core-review/03-aguardando-so-pergunta/docs/TASKS.md`:

```
- T-001: Precisa de resposta do usuario.
  - **Pergunta:** qual cor?
```

`--strict` → exit 0. Controle: a mesma tarefa sem `**Pergunta:**` (caso 30) → `[ERRO] [AGUARDANDO-SEM-PERGUNTA]` exit 1.
- Severidade: media. Dois dos tres artefatos que o core lista como o registro da espera nao existem para o portao.

### A-S1-7: rodada 2+ exige exposicao `sim`; o validador aceita `nao`
- Onde: `AGENTS.md:184-186`; `validate_structure.py:347-364` e `365-367`
- Promessa: "Da rodada 2 em diante a exposicao previa e esperada e deve ser declarada como `sim`." Em seguida: "O validador checa presenca e valor permitido."
- Realidade: `Exposicao previa a outras posicoes` aceita `sim | nao` em qualquer rodada. Nao ha cruzamento com o numero da `**Rodada:**`.
- Reproducao: `/tmp/aps-s1-core-review/04-rodada2-exposicao-nao/docs/CONSENSUS.md`:

```
**Exposicao previa a outras posicoes:** nao
**Rodada:** 2 de 2
```

`--strict` → exit 0. Controle: `**Rodada:** 4 de 4` sem `Pendente da rodada anterior` (caso 21) acusa `CONSENSO-SEM-PENDENTE`. O cruzamento rodada/pendente existe; o cruzamento rodada/exposicao nao.
- Severidade: media. E exatamente o tipo de consistencia de formulario que o paragrafo diz que o script faz, e ele so faz metade.

### A-S1-8: pontes "so redirecionamento" nascem com regras de processo
- Onde: `AGENTS.md:22-24`; template `assets/CLAUDE.md:5-10` (e `GEMINI.md` igual); `validate_structure.py:258-265`
- Promessa: "`CLAUDE.md` e `GEMINI.md` sao apenas redirecionamentos para `AGENTS.md`. Eles nao podem conter regras de produto, arquitetura, processo, estilo ou qualquer logica."
- Realidade: o arquivo que a skill copia ja tem um procedimento de quatro passos (ler AGENTS, ordem de leitura, SESSION, CONSENSUS). `check_bridges` so testa se o texto contem a substring `AGENTS.md` (AVISO se nao). Um `CLAUDE.md` cheio de regra de produto, arquitetura, processo e estilo passa, desde que mencione `AGENTS.md`.
- Reproducao: `/tmp/aps-s1-core-review/07-ponte-com-regras/CLAUDE.md` declara API `/v2`, monolito com Postgres, PR contra main e tabs; `--strict` exit 0. O `CLAUDE.md` da raiz deste repositorio e o do `assets/` ja trazem o procedimento de quatro passos.
- Severidade: media. A regra e violada no artefato que a skill instala, e o unico check de ponte nao enxerga o resto.

### A-S1-9: leitura relevante obriga `ARCHITECTURE.md`, que o scaffold marca opcional
- Onde: `AGENTS.md:41-49` item 6; `SKILL.md:99-110` (lista de opcionais)
- Promessa: "Para qualquer outra mudanca, leia:" inclui `docs/ARCHITECTURE.md` sem condicional. O mesmo bloco core e copiado no nivel minimal.
- Realidade: `ARCHITECTURE.md` nao esta em `CORE_FILES`. No fluxo minimal o arquivo nao e criado. Projeto sem ele passa `--strict`.
- Reproducao: `/tmp/aps-s1-core-review/28-architecture-ausente` (assets copiados, `docs/ARCHITECTURE.md` apagado). `--strict` exit 0.
- Severidade: media. Todo projeto minimal recebe um contrato que manda ler um arquivo que a skill nao criou.

### A-S1-10: placeholder de adocao nao falha nem em `--strict`
- Onde: `SKILL.md:134-136`; `validate_structure.py:555-567` e `728-735`
- Promessa: o passo 5b manda trocar `AAAA-MM-DD` pela data de hoje; "Sem ela, o validador nao cobra evidencia de nenhuma tarefa."
- Realidade: `(convencoes-2-2-0-desde: AAAA-MM-DD)` casa o regex, `parse_date` devolve `None`, sai `[INFO] [CONVENCOES-DATA-INVALIDA]`. INFO nao vira falha com `--strict`. Tarefa concluida datada, sem evidencia, passa.
- Reproducao: `/tmp/aps-s1-core-review/15-adocao-placeholder-sem-evidencia` (marcador ainda `AAAA-MM-DD` + `2026-09-03 T-001` sem evidencia). `--strict` exit 0, so o INFO.
- Severidade: baixa. O INFO existe, mas o comando que a skill oferece no passo 7, e o `--strict`, nao travam o scaffold que pulou o 5b.

### A-S1-11: marcador `loop` usa o mesmo esquema e o regex o ignora
- Onde: `validate_structure.py:56-58` (`MARKER_RE` = `core|specs`); bloco em `AGENTS.md:263` e `assets/partials/AGENTS-loop-block.md:1`
- Promessa: core, specs e loop se fecham com `<!-- ai-project-structure:<bloco>:(start|end) vX.Y.Z -->`. `MARCADOR-DESPAREADO` e o diagnostico dessa forma.
- Realidade: `loop:start` sem `loop:end` nao entra em `found`. `MARCADOR-DESPAREADO` nao dispara.
- Reproducao: `/tmp/aps-s1-core-review/27-loop-marcador-despareado/AGENTS.md` com `loop:start v2.5.1` e sem `end`. `--strict` exit 0.
- Severidade: baixa. O buraco so aparece com o modulo de loop ativo; o contrato do core nao cita o loop, mas o validador e o mesmo arquivo que deveria enxergar os tres blocos.

## Suspeitas nao demonstradas
- `field_value` compara `normalize(line).startswith("**rodada:**")`. Nao provei um rotulo vizinho que fosse engolido como `Rodada`; o caso `Pendente da rodada anterior` nao casa. Faltou uma bateria de rotulos quase-iguais.
- `**Status:**` do consenso e case-sensitive (`validate_structure.py:456`), diferente de `field_value`. Nao rodei `**status:** aberto` para ver `CONSENSO-SEM-STATUS` em entrada valida.
- O cabecalho de `loop.sh:29-31` lista o que o script "NUNCA" toca e omite `CONSENSUS.md`, enquanto o prompt mais abaixo e o bloco loop proibem. Nao abri `loop_task.py` por inteiro nesta superficie; a omissao pode ser so comentario.
- Nao medi se `SESSION.md` / `CONSENSUS.md` com 5 entradas e mais de 30KB obrigam a rotacionar "recente" para cumprir as duas metades da regra de rotacao. A tensao esta no texto; a prova pediria um arquivo grande, que nao montei.

## Tarefas conhecidas
- T-054: sim. Caso 05 (`**Rodada:**` ausente, Metodo e Exposicao presentes) exit 0. Caso 06 (`**Rodada:** 1 de 1 e qualquer texto extra`) exit 0. `validate_structure.py:365-368` retorna calado se o campo falta; `368` usa `re.match`, nao `fullmatch`.
- T-055: sim. O `Modelo De Debate` cercado em `docs/CONSENSUS.md:21-63` nao tem `Metodo`, `Exposicao previa a outras posicoes` nem `Rodada`. O de `assets/docs/CONSENSUS.md:51-62` tem. `strip_fences` esconde o modelo, entao `--strict` na raiz nao acusa.
- T-056: sim. Spec minima com 2 perguntas e 3 sub-itens indentados: `--progress` imprimiu `perguntas abertas: 5`. `spec_overview` em `validate_structure.py:906-909` faz `line.strip().startswith("- ")`.
- T-058: sim. `loop.sh:36` nome fixo `.loop-pergunta`; `80-84` apaga leftover na abertura. Nao ha lock, `flock` nem arquivo de exclusao no script.

## Inventario
Lidos por inteiro:
- `AGENTS.md`
- `docs/skills/ai-project-structure/assets/AGENTS.md`
- `docs/skills/ai-project-structure/scripts/validate_structure.py`
- `docs/skills/ai-project-structure/SKILL.md`
- `CLAUDE.md`, `GEMINI.md`, `assets/CLAUDE.md`, `assets/GEMINI.md`
- `assets/docs/CONSENSUS.md`, `assets/docs/TASKS.md`, `assets/docs/SESSION.md`
- `assets/partials/AGENTS-specs-block.md`, `assets/partials/AGENTS-loop-block.md`
- `docs/CONSENSUS.md`, `docs/TASKS.md`, `docs/SESSION.md`, `docs/PROJECT_CONTEXT.md`, `docs/QUALITY.md`

Lidos so em parte (nao entram como leitura integral): `docs/MEMORY.md`, `docs/ARCHITECTURE.md`, `docs/skills/ai-project-structure/README.md`, `docs/skills/ai-project-structure/CHANGELOG.md`, `docs/skills/ai-project-structure/scripts/loop.sh`.

## 1. Regras nao verificaveis
Nem script, nem pessoa lendo o repositorio depois. Frases exatas, por secao.

Prioridade e entrada:
- "Claude Code deve entrar por `CLAUDE.md`."
- "Gemini deve entrar por `GEMINI.md`."
- "Codex e outros agentes devem ler este arquivo diretamente."
- "1. Instrucoes diretas do usuario na conversa atual."

Arquivos-ponte: a imutabilidade de conteudo e verificavel; o "nao edite" no momento do trabalho nao deixa artefato de recusa.

Ordem de leitura:
- "Em duvida, trate como relevante."
- A ordem em si (se o agente leu aqueles arquivos naquela sessao).

Como trabalhar:
- "Responda em portugues claro, salvo pedido diferente do usuario."
- "Antes de editar, entenda o objetivo, o contexto e o estado atual."
- "Prefira mudancas pequenas, focadas e faceis de revisar."
- "Nao refatore fora do escopo da tarefa."
- "Nao sobrescreva conteudo existente sem preservar, mesclar ou pedir confirmacao." (o git mostra o overwrite; a confirmacao do usuario nao fica no repo.)

Nunca inferir:
- "**Pergunte.** Nao preencha por inferencia plausivel."
- "Resposta adiada ("Avançar") adia a pergunta; **nunca autoriza inventar** a resposta."
- "Placeholder honesto ("(A preencher.)") e melhor que conteudo inventado."

Evidencia:
- "Nunca invente um comando inexistente so para preencher o campo."
- "Evidencia colada sem conferencia real passa no script e falha no proposito."

Memoria da sessao:
- "leia a sessao mais recente;" / "identifique o que foi feito;" / "confira pendencias e proximo passo recomendado."

Memoria persistente:
- "nao registre dados sensiveis;" (chave obvia e Q2; o que e confidencial sem parecer secreto nao da para saber.)

Consenso:
- "Nao use para microdecisoes. Consenso por teatro deixa o fluxo lento e perde valor."
- "Na rodada 1, cada modelo preenche apenas a propria secao, sem ler as demais."
- "Os campos sao autodeclarados. O validador checa presenca e valor permitido, **nunca veracidade**: nenhum script prova que um modelo nao leu a posicao do outro, nem julga se a pendencia declarada justifica mais uma rodada."
- "A disposicao do achado e de quem o registra; a revalidacao dela e de outro modelo, e conta como rodada."

Ponto cego: o paragrafo inteiro e aviso epistemico, nao regra de arquivo.

Desempate:
- "1. **Usuario decide** sempre que estiver disponivel."
- "2. Na ausencia do usuario, prevalece a opcao de **menor risco reversivel**."
- "3. Se nenhuma opcao for facilmente reversivel, **pare e peca confirmacao humana**. Nunca tome sozinho um caminho irreversivel, caro, sensivel ou estrutural."

Validacao (checklist):
- "se a tarefa pedida foi realmente atendida;"
- "se nao houve mudanca fora de escopo;"
- "se testes, revisao manual ou validacao foram executados quando aplicavel;"
- "se ha pendencias que precisam ser comunicadas."

## 2. Regras violaveis sem acusacao
Projeto base: copia de `assets/` em `/tmp/aps-s1-core-review/`, adocao `2026-09-01`. Comando, em todos: `python3 /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/validate_structure.py <projeto> --strict`. Exit 0 em cada item.

1. Evidencia obrigatoria sem data na linha: conteudo de A-S1-1. Pasta `02-concluida-sem-data-sem-evidencia`.
2. Forma `tipo=` / `procedimento=` / `resultado=`: conteudo de A-S1-2. Pasta `01-evidencia-sem-forma`.
3. Travessao fora de `docs/` e das pontes: `README.md` na raiz com U+2014. Pasta `09-travessao-readme-raiz`.
4. Aguardando sem `**Resposta:**` e sem `(bloqueada:)`: conteudo de A-S1-6. Pasta `03-aguardando-so-pergunta`.
5. "Da rodada 2 em diante ... declarada como `sim`": conteudo de A-S1-7. Pasta `04-rodada2-exposicao-nao`.
6. `**Rodada:**` ausente (T-054): entrada com Metodo, Exposicao, Status, Proximo passo, sem Rodada. Pasta `05-rodada-ausente`.
7. Pontes sem logica: `CLAUDE.md` com regras de produto/arquitetura/processo/estilo, desde que diga `AGENTS.md`. Pasta `07-ponte-com-regras`.
8. "adicione uma nova entrada no topo": duas entradas de sessao com todos os `###`, a de `2026-09-01` antes da de `2026-09-03`. Pasta `08-sessao-ordem-invertida`.
9. "O registro deve separar: contexto da duvida; posicao de cada modelo; pontos de acordo; riscos; consenso final": entrada so com os campos declarativos e Status. Pasta `12-consenso-sem-secoes`.
10. "Nao edite dentro dos marcadores": `AGENTS.md` com start/end v2.5.1 e corpo `bloco esvaziado`. Pasta `13-bloco-core-esvaziado`.
11. "Enquanto a resposta nao chegar, a tarefa nao volta para Proximas Tarefas": `T-001` em Proximas, sem pergunta e sem resposta. Pasta `14-pergunta-nas-proximas`.
12. "a tarefa cita o achado na linha": achado `S1-X` resolvido pedindo tarefa; `T-001` no backlog sem citar `S1-X`. Pasta `16-achado-sem-citacao`.
13. "Pendencias de sessao que sejam acionaveis devem virar tarefa em `TASKS.md`": sessao com pendencia "Implementar o login OAuth agora." e TASKS sem essa tarefa. Pasta `18-pendencia-sessao-fora-de-tasks`.
14. "mantenha as 5 a 10 mais recentes": 12 entradas de sessao, todas com headings, arquivo abaixo de 30KB. Pasta `19-doze-sessoes-sem-rotacao`.
15. "com dono claro": `**Status:** aberto` e `**Proximo passo:**` vazio. Pasta `20-proximo-passo-sem-dono`.
16. "fatos obsoletos devem ser marcados como substituidos, nao apagados": `MEMORY.md` reduzido a `# MEMORY` + "Vazio depois de apagar fatos." Pasta `25-memory-apagada`.
17. Marcadores `loop` despareados: A-S1-11. Pasta `27-loop-marcador-despareado`.

## 3. Contradicoes
Dentro do core, rotacao:
- "`SESSION.md` e `CONSENSUS.md` crescem indefinidamente. Quando passarem de aproximadamente 20 entradas (ou ~30KB):"
- "mantenha as 5 a 10 mais recentes no arquivo principal;"

O gatilho em KB pode disparar com poucas entradas grandes. Aí "rotacionar as mais antigas" e "ficar com 5 a 10" nao cabem no mesmo arquivo. O proprio `SESSION.md` da raiz ja registrou essa tensao; nao e tarefa nova, e contradicao do texto.

Core vs specs, perguntas abertas:
- Core: "Registre perguntas abertas explicitamente: como tarefa em `TASKS.md` ou na secao "Perguntas Abertas" da spec correspondente (quando o modulo de specs estiver ativo)."
- Specs: "Criterios de aceite nao podem ser inventados: se faltar contexto, pergunte (regra "Nunca Inferir") e registre em "Perguntas Abertas"."

O core aceita so `TASKS.md`; o bloco specs manda a secao da spec. Uma pergunta so no backlog satisfaz o core e fura o specs.

Core vs loop, `SESSION.md`:
- Core: "Houve trabalho cronologico relevante? Atualize `SESSION.md`."
- Loop: "O loop nao escreve em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `CONSENSUS.md`, `AGENTS.md` nem em specs."

O gatilho nao abre excecao. Uma rodada de loop que fecha tarefa e trabalho cronologico; o agente do loop e proibido de cumprir o gatilho.

Core vs o que a skill entrega (pontes e `ARCHITECTURE.md`): A-S1-8 e A-S1-9. Nao sao duas frases do core se negando; sao o core contra o template e o `SKILL.md`.

## 4. A raiz (dogfood) viola hoje
- T-055: o `Modelo De Debate` de `docs/CONSENSUS.md:21-63` nao declara os tres campos que `AGENTS.md:180-182` exige. Quem copiar o modelo da raiz produz entrada que falha em `--strict`; o modelo esta cercado, entao a raiz atual passa.
- `CLAUDE.md` e `GEMINI.md` da raiz (iguais aos de `assets/`) contem o procedimento "Antes de trabalhar" de quatro passos, contra `AGENTS.md:22-24`.
- `docs/TASKS.md` em Concluidas ainda tem linhas sem `T-NNN` (`2026-05-26: Skill ... empacotada`, `2026-04-25: Criada a estrutura...`). O core diz "Tarefas usam ID `T-NNN`" sem excecao v1; o validador so cobra ID nas secoes abertas, entao a raiz passa.

O bloco entre `core:start` e `core:end` da raiz e o de `assets/AGENTS.md` e o mesmo byte a byte; a divergencia do dogfood nesta superficie nao esta no contrato gerenciado, esta nos arquivos que o contrato descreve.
