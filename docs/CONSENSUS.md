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

## Registros

Os debates de 2026-04-25 foram rotacionados para `docs/archive/CONSENSUS-2026.md`.

## 2026-09-02 - Revisao da spec 0003 (skill 2.2.0) por modelo distinto

**Status:** resolvido

**Resolvido em:** 2026-09-02 (usuário ratificou as 6 mudanças do Codex e decidiu os 2 resíduos; spec 0003 passou para `Definida`).

**Metodo:** debate-aberto

**Exposicao previa a outras posicoes:** sim

**Rodada:** 2 de 3

### Contexto

A spec `docs/specs/0003-tasks-verificaveis.md` foi escrita como PRD da skill 2.2.0 e submetida a validação por modelo distinto no Codex CLI, em duas rodadas: rodada 1 cega (proibida a leitura da spec, só os quatro problemas), rodada 2 adversarial com a spec à vista. Primeiro uso real da regra de rodada cega que a própria spec propõe.

Proveniência: apenas a resposta da rodada 2 foi registrada aqui. A posição da rodada 1 do Codex está reconstruída a partir das referências que a rodada 2 faz a ela.

### Pergunta Ou Decisao

A spec 0003 deve passar para `Definida` como está?

### Posicao Do Codex

Veredito: passar para `Definida` **com mudanças**. Concorda com a direção geral (seção própria para tarefa parada, rodada cega no consenso, loop fora desta versão e fora do scaffold, comando único de integridade) e valida DEC-001, DEC-002, DEC-003 e DEC-005. Seis mudanças exigidas:

1. **Evidência de fechamento obrigatória para toda tarefa em `Concluidas`**, mantendo `(verifica: <comando>)` opcional. Argumento: se a verificação for inteiramente opcional, o agente conclui justamente as tarefas menos verificadas sem consequência, preservando a lacuna que a spec quer fechar. Formato proposto atende conteúdo e produto sem exigir comando falso: `Evidencia: tipo=revisao-manual; procedimento=conferencia dos links; resultado=12 links validos`.
2. **Evidência ausente em tarefa que declarou `(verifica:)` deve ser ERRO, não aviso.** Tarefa que declarou comando e foi movida para `Concluidas` sem resultado contradiz o próprio contrato; aviso não protege o estado concluído.
3. **Renomear `## Bloqueadas` para `## Aguardando Usuario`.** `Bloqueadas` sugere também dependência técnica, fornecedor ou incidente, e o formato obrigatório de pergunta e resposta não serve para esses casos. Mantém `**Resposta:**` e a data de bloqueio.
4. **Campos declarativos no registro de consenso**: `**Metodo:**`, `**Exposicao previa a outras posicoes:**`, `**Rodada:** N de 3`. O validador checaria presença, valor permitido e coerência do teto, e deve declarar explicitamente que não verifica a cegueira real.
5. **Mover o comando de integridade para dentro da skill**, por exemplo `docs/skills/ai-project-structure/evals/verify_repository.py`. Criar `scripts/` na raiz viola a regra de raiz mínima. Comparar a raiz inteira com `assets/` por `diff` seria incorreto, porque a raiz contém estado real do projeto dogfood.
6. **Corrigir caminhos e ampliar critérios de aceite.** A spec cita `scripts/validate_structure.py`, mas o validador está em `docs/skills/ai-project-structure/scripts/`.

Respostas às quatro perguntas abertas: (1) `(verifica:)` opcional inclusive em projetos com código, porque código também tem tarefa de pesquisa, documentação e decisão sem comando honesto; a obrigatoriedade correta é a evidência ao concluir. (2) Evidência ausente após `(verifica:)` é ERRO. (3) A seção de espera não rotaciona; gera AVISO após 30 dias, porque tarefa antiga bloqueada é informação operacional ativa, não histórico. (4) A seção entra em todos os scaffolds; o custo é uma seção vazia e o benefício é regra única disponível desde a primeira pergunta bloqueante.

Critérios de aceite que o Codex aponta como não verificáveis por comando: scaffold minimal e completa (exige rodar o fluxo de uma IA e responder à entrevista, sem runner automatizado de eval hoje); atualização 2.1.0 para 2.2.0 (`references/atualizacao.md` é instrução, não migrador executável); paridade dos três destinos após `install.sh` (verificável, mas hoje mutaria instalações locais, então deve rodar em destino temporário). Critérios faltantes que aponta: evidência obrigatória, ERRO de `(verifica:)` sem resultado, marcador com valor desconhecido, tarefa bloqueada válida retornando sucesso, os três campos de consenso, teto de três rodadas, paridade dos templates de `TASKS.md` e `CONSENSUS.md`, e atualização de projeto 2.1.0 com histórico sem transformar registros antigos em alegações falsas.

### Posicao Do Claude

Aceito as 6 mudanças. Duas delas são erro meu, e confirmei os dois no repositório:

- **Raiz mínima:** `scripts/check.sh` na raiz viola a regra registrada em "Regras Do Projeto" do `AGENTS.md` e o checklist de `QUALITY.md` ("A raiz mantem apenas os arquivos Markdown de entrada dos agentes"). A exceção registrada cobre apenas `README.md`, `LICENSE` e `.gitignore`. Codex está certo.
- **Caminho do validador:** a spec escreve `python3 scripts/validate_structure.py .`; o caminho real é `docs/skills/ai-project-structure/scripts/validate_structure.py`. Codex está certo.

Acrescento uma razão a mais para a colocação do item 5, que o Codex não citou: `evals/` **não é distribuído**. `diff -rq` entre a fonte canônica e `~/.claude/skills/ai-project-structure` mostra `evals`, `install.sh`, `README.md` e `CHANGELOG.md` como presentes apenas na fonte. Um verificador em `scripts/` da skill seria instalado na máquina de todo usuário; em `evals/` fica restrito ao repositório. A colocação proposta está certa por dois motivos, não um.

Onde o Codex leu errado: a spec **não** propõe comparar a raiz inteira com `assets/` por `diff`. Propõe diff do bloco `core` e das duas pontes. A crítica não se aplica, mas a sugestão embutida (definir paridade explícita também para os templates de `TASKS.md` e `CONSENSUS.md`) é válida e entra.

Sobre o item 4, o Codex conserta DEC-004 melhor do que eu escrevi. Meu texto aceitava "prosa não enforçável" e parava aí; os campos declarativos não provam independência, mas tornam o grau de confiança observável, que era o problema 3 original. Correção aceita.

Custo que o Codex não precificou no item 1: toda linha concluída passa a carregar sub-linha de evidência. Em projeto com centenas de tarefas, `TASKS.md` engorda rápido. Mitigado pela rotação opcional de "Concluidas" já prevista em `AGENTS.md`, mas a rotação deixa de ser opcional na prática.

Consequência que nenhum dos dois tirou: a 0003 aumenta o número de contratos verificados por script **e** o número de contratos verificados na mão ao mesmo tempo (scaffold, atualização, evals). Sem runner de eval, a razão entre automático e manual pode piorar em vez de melhorar.

### Posicao Do Gemini

(Nao consultado nesta rodada.)

### Pontos De Acordo

- Evidência de fechamento obrigatória para toda tarefa concluída, com `(verifica: <comando>)` permanecendo opcional.
- `(verifica:)` declarado e resultado ausente em `Concluidas` é ERRO.
- Seção de espera com pergunta, resposta e data; sem rotação, com aviso por idade.
- Consenso ganha campos declarativos de método, exposição prévia e rodada, com o validador checando presença e não veracidade.
- Verificador de integridade dentro da skill, em `evals/`, nunca em `scripts/` na raiz.
- Loop fora da 2.2.0 e fora do scaffold (DEC-003 mantida por ambos).
- Sem check de `QUALITY.md` vazio nesta versão (DEC-005 mantida por ambos).

### Riscos E Tradeoffs

- **Peso de convenção.** A versão revisada adiciona mais ao bloco core do que a original (evidência obrigatória, três campos de consenso). Cada linha é lida por todo modelo, em todo projeto, para sempre.
- **Teatro de conformidade.** Evidência obrigatória em projeto de conteúdo pode degenerar em `Evidencia: tipo=revisao-manual` colado sem conferência real. A regra fica verificável quanto à forma e não quanto ao conteúdo, que é a mesma limitação que ela pretende resolver.
- **Autodeclaração no consenso.** `Exposicao previa: nao` é escrito pelo mesmo modelo cuja cegueira o campo afirma. O Codex reconhece isso; vale registrar que o campo aumenta a rastreabilidade e não a garantia.
- **Verificação manual crescente.** Mais contratos, mesmo runner inexistente para evals.

### Consenso Final

Spec 0003 passa para `Definida` com as seis mudanças do Codex incorporadas. Os dois resíduos que nenhum dos dois modelos resolveu foram decididos pelo usuário em 2026-09-02:

**R-1. Nome e escopo da seção de espera.** `Aguardando Usuario` (Codex) cobre só bloqueio humano e é semanticamente mais preciso; `Bloqueadas` (spec original) cobre mais casos, mas o formato pergunta e resposta não serve para bloqueio técnico, fornecedor ou release upstream.

**Decisão do usuário:** adotar `## Aguardando Usuario` agora, com o formato `**Pergunta:**` / `**Resposta:**` / `(bloqueada: AAAA-MM-DD)`. Seção separada para bloqueio não humano só quando o primeiro caso real aparecer, com formato próprio. Motivo: não desenhar para caso que ainda não existe.

**R-2. Retroatividade da evidência obrigatória.** Tornar a regra retroativa converteria as 15 linhas históricas de `docs/TASKS.md` deste repositório, e as de todo projeto que atualizar, em alegações sem evidência.

**Decisão do usuário:** a regra vale apenas para tarefa concluída a partir da 2.2.0. O validador não cobra evidência de tarefa concluída antes da versão, e o fluxo de `references/atualizacao.md` não reescreve histórico.

### Decisao Para Registrar Em DECISIONS.md

Registrar em `docs/DECISIONS.md` como `2026-09-02 - Evidencia obrigatoria em tarefa, secao Aguardando Usuario e consenso declarado`, cobrindo: evidência de fechamento obrigatória para toda tarefa concluída a partir da 2.2.0, com `(verifica:)` permanecendo opcional; `(verifica:)` sem resultado em `Concluidas` como ERRO; seção `## Aguardando Usuario` sem rotação e com aviso por idade; campos declarativos de método, exposição prévia e rodada no consenso, checados quanto à presença e não quanto à veracidade; verificador de integridade em `evals/`, nunca em `scripts/` na raiz.
