# CONSENSUS 2026

Debates antigos de `docs/CONSENSUS.md`, rotacionados em 2026-09-02 pela regra de "Rotacao De Arquivos" do `AGENTS.md`.

Cobre os dois debates de 2026-04-25: a validacao da estrutura multiagente (aprovada com sete melhorias incrementais) e a adicao de `MEMORY.md` com o detalhamento dessas melhorias. Ambos `resolvido`. Sao anteriores a versao 2.2.0 da estrutura, entao nao trazem os campos declarativos de metodo, exposicao previa e rodada.

## 2026-04-25 - Validação da estrutura multiagente

**Status:** resolvido

**Resolvido em:** 2026-04-25 (estrutura aprovada; melhorias aplicadas no consenso seguinte do mesmo dia).

### Contexto

Validação da estrutura Markdown multiagente criada para projetos tocados por IA, com AGENTS.md como fonte central, arquivos-ponte para Claude e Gemini, memória de sessões em docs/SESSION.md e debate entre modelos em docs/CONSENSUS.md.

### Pergunta Ou Decisao

A estrutura atual é clara, segura e prática para projetos tocados por IA? O que pode melhorar?

### Posicao Do Claude

A estrutura é boa, prática e bem dimensionada para o objetivo. Os pontos mais fortes são: raiz mínima, hierarquia explícita de conflitos em `AGENTS.md` (usuário > AGENTS.md > docs/ > inferência), separação entre debate (`CONSENSUS.md`) e decisão final (`DECISIONS.md`), e checklist de qualidade aplicável. O fluxo é compreensível em uma única leitura, o que é raro.

Pontos de atenção concretos:

1. **`SESSION.md` cresce de forma ilimitada.** Sem política de rotação, em poucos meses fica caro de carregar e ruidoso. Sugiro adicionar em `AGENTS.md` uma regra simples: quando `SESSION.md` passar de N entradas (ex: 20) ou X KB, mover as mais antigas para `docs/archive/SESSIONS-AAAA.md`. As últimas 5 entradas bastam para continuidade real.
2. **Sobreposição entre `TASKS.md` e a seção "Pendencias" de cada sessão.** Hoje não está claro qual é canônico para o trabalho em aberto. Proposta: `TASKS.md` é a fonte de verdade do backlog vivo; "Pendencias" em `SESSION.md` é só o snapshot daquela sessão e deve ser refletido em `TASKS.md` antes de fechar.
3. **`CONSENSUS.md` não tem ciclo de vida.** Debates resolvidos ficam misturados com abertos. Sugiro um campo `Status: aberto | resolvido | arquivado` no template e mover resolvidos antigos para `docs/archive/` quando o arquivo crescer.
4. **Ordem de leitura é única para qualquer mudança.** Para tarefas triviais (ajuste de typo, renomear variável), ler 6 arquivos é overhead. Sugiro um nível "mudanca trivial" em `AGENTS.md` que exige só `SESSION.md` + `TASKS.md`, mantendo a leitura completa para mudanças relevantes.
5. **Não há regra de desempate.** Se Claude e Gemini não convergirem em `CONSENSUS.md`, o que acontece? Proposta: deixar explícito que o usuário é o desempate final e que, na ausência dele, prevalece a posição com menor risco reversível.
6. **Concordo com o Gemini quanto a reforçar a imutabilidade dos arquivos-ponte.** Hoje `CLAUDE.md` e `GEMINI.md` já mencionam `SESSION.md` e `CONSENSUS.md`, o que tecnicamente é uma duplicação leve do `AGENTS.md`. Útil como rede de segurança, mas vale uma linha em `AGENTS.md` proibindo qualquer regra de produto/arquitetura nesses arquivos.
7. **Concordo também quanto a handover direcionado.** "Próximo passo recomendado" ganha muito quando indica o agente esperado e por quê (ex: "Para Gemini, porque envolve análise multimodal de imagens em docs/").

Nada disso é bloqueante - a estrutura já pode ser usada como está. São melhorias incrementais.

### Posicao Do Gemini

A estrutura é excelente e segue as melhores práticas de gerenciamento de contexto para LLMs. A centralização em `AGENTS.md` reduz drasticamente o risco de instruções conflitantes ("instruction drift"), enquanto os arquivos-ponte (`CLAUDE.md`, `GEMINI.md`) garantem que cada ferramenta saiba onde buscar sua base de regras sem redundância. O uso de `SESSION.md` para continuidade e `CONSENSUS.md` para alinhamento entre modelos formaliza um fluxo de trabalho colaborativo que é raro mas necessário em projetos complexos.

Sugestões de melhoria:
1. **Handover Detalhado**: No `SESSION.md`, incentivar que o "Próximo Passo Recomendado" seja específico para o agente esperado (ex: "Para Claude: Finalizar refatoração do módulo X").
2. **Imutabilidade dos Pontos-Ponte**: Reforçar em `AGENTS.md` que `CLAUDE.md` e `GEMINI.md` não devem conter lógica de negócio ou regras de projeto, apenas redirecionamentos, para evitar sombreamento de regras.

### Pontos De Acordo

- Centralização de regras em `AGENTS.md`.
- Uso de `SESSION.md` para continuidade entre turnos/agentes.
- `CONSENSUS.md` como repositório de decisões complexas e debate multi-modelo.
- Arquivos-ponte (`CLAUDE.md`, `GEMINI.md`) devem ficar mínimos e sem lógica de projeto.
- Hierarquia de conflitos explícita em `AGENTS.md` é um diferencial e deve ser mantida.
- Separação clara entre `CONSENSUS.md` (debate) e `DECISIONS.md` (decisão final) é correta.

### Riscos E Tradeoffs

- **Overhead de Documentação**: O excesso de arquivos pode intimidar novos usuários, mas é um tradeoff necessário para manter a sanidade do contexto em projetos de longo prazo.
- **Sincronização**: O risco de um agente esquecer de atualizar `SESSION.md` ao final de uma sessão intensa.
- **Crescimento ilimitado de `SESSION.md` e `CONSENSUS.md`** sem política de arquivamento - vira ruído e custo de tokens com o tempo.
- **Sobreposição entre `TASKS.md` e "Pendencias" das sessões** sem regra clara de qual é canônico.
- **Custo de leitura para mudanças triviais** - ler 6 arquivos para um ajuste pequeno desincentiva o cumprimento da regra.
- **Ausência de regra de desempate** quando dois modelos não convergem em `CONSENSUS.md`.
- **Risco de drift dos arquivos-ponte** caso alguém adicione regra de projeto em `CLAUDE.md` ou `GEMINI.md` no futuro.

### Consenso Final

A estrutura está aprovada para uso imediato. Claude e Gemini concordam que ela é clara, segura e prática, e que reduz risco de instruction drift em projetos tocados por múltiplas IAs. Convergência em sete melhorias incrementais não-bloqueantes:

1. Política de rotação para `SESSION.md` (e `CONSENSUS.md`) com pasta `docs/archive/`.
2. Regra explícita: `TASKS.md` é canônico para backlog vivo; "Pendencias" da sessão é snapshot.
3. Campo `Status` no template de `CONSENSUS.md` (aberto / resolvido / arquivado).
4. Nível de leitura "mudanca trivial" em `AGENTS.md` (só `SESSION.md` + `TASKS.md`).
5. Regra de desempate explícita em `AGENTS.md` (usuário decide; na ausência, opção de menor risco reversível).
6. Reforço em `AGENTS.md` de que `CLAUDE.md` e `GEMINI.md` são imutáveis quanto a regras de projeto.
7. "Próximo passo recomendado" em `SESSION.md` deve indicar o agente-alvo quando fizer diferença.

Recomenda-se aplicar essas melhorias incrementalmente, não em uma única refatoração.

### Decisao Para Registrar Em DECISIONS.md

Nenhuma decisão nova por enquanto. As sete melhorias acima são sugestões; só viram decisão em `DECISIONS.md` quando o usuário aprovar e instruir aplicação.

## 2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias

**Status:** resolvido

**Resolvido em:** 2026-04-25 (apos aprovacao do usuario; mudancas aplicadas - ver `docs/DECISIONS.md`).

### Contexto

No consenso anterior do mesmo dia, Claude e Gemini aprovaram a estrutura e listaram sete melhorias incrementais. O usuario apontou que sentiu falta de um `MEMORY.md` na lista e pediu detalhamento dos sete pontos. Esta entrada abre o debate sobre adicionar `docs/MEMORY.md` (oitava melhoria) e formaliza a explicacao concreta de cada ponto.

### Pergunta Ou Decisao

Faz sentido adicionar `docs/MEMORY.md` a estrutura? Como ele convive com `PROJECT_CONTEXT.md`, `SESSION.md` e `DECISIONS.md` sem duplicar funcao? E qual a forma final dos sete pontos do consenso anterior depois de detalhados?

### Posicao Do Claude

**Sobre `MEMORY.md` (proposta nova):**

Sim, faz sentido. Hoje a estrutura tem cobertura para:

- O que o projeto **e** (estatico): `PROJECT_CONTEXT.md`
- O que **aconteceu** (cronologico): `SESSION.md`
- O que foi **decidido** (formal): `DECISIONS.md`
- O que esta **em aberto** (backlog): `TASKS.md`

Falta cobertura para o que o projeto **aprendeu** - fatos consolidados que valem "a partir de agora, sempre" e que se acumulam sem caber bem em nenhum dos arquivos acima. Exemplos concretos:

- "O usuario prefere portugues claro e respostas curtas." (nao e decisao, nao e contexto inicial, e preferencia que vale sempre)
- "Mocks em testes de migracao falharam em producao no Q4 - sempre usar banco real." (licao aprendida, nao decisao formal)
- "Issues do produto X sao trackeadas no Linear projeto INGEST." (referencia externa)
- "Ao gerar copy, evitar superlativos - o usuario corta sempre." (feedback que vira regra)

Proposta concreta para `docs/MEMORY.md`:

```md
# MEMORY

Memoria persistente do projeto. Diferente de SESSION.md (cronologico) e DECISIONS.md (decisoes formais), aqui ficam fatos que valem "a partir de agora, sempre" e se acumulam ao longo do tempo.

## User
Quem e o usuario, suas preferencias, contexto e expertise.

## Feedback
Guidance de "faca/nao faca isso". Cada item: regra + por que + quando aplicar.

## Project
Fatos sobre o projeto descobertos na pratica que nao estao em PROJECT_CONTEXT.

## Reference
Pointers para sistemas externos (Linear, Slack, Grafana, etc).
```

Convivencia com vizinhos:
- `PROJECT_CONTEXT.md` = o que o projeto **e** (raramente muda)
- `MEMORY.md` = o que o projeto **aprendeu** (acumula com tempo)
- `SESSION.md` = o que **aconteceu** em data X
- `DECISIONS.md` = o que foi **decidido** formalmente

Risco real: agente nao saber em qual dos quatro escrever. Mitigacao: regra simples em `AGENTS.md` - "se e cronologico, vai pro SESSION; se e decisao formal, vai pro DECISIONS; se e fato persistente nao-decidido, vai pro MEMORY; se e estrutural permanente, vai pro PROJECT_CONTEXT".

**Detalhamento dos sete pontos do consenso anterior:**

1. **Rotacao de `SESSION.md` e `CONSENSUS.md`.** Problema: arquivos crescem indefinidamente. Em 6 meses, `SESSION.md` pode ter 50+ entradas e fica caro de carregar. Proposta: regra em `AGENTS.md` - quando passar de ~20 entradas (ou ~30KB), mover as mais antigas para `docs/archive/SESSIONS-AAAA.md` (mesmo para CONSENSUS). Manter as 5-10 mais recentes, que sao as que importam para continuidade.

2. **`TASKS.md` canonico vs "Pendencias" em SESSION.** Problema: ha duas fontes de "o que esta em aberto" e nao esta claro qual prevalece. Proposta: `TASKS.md` e fonte unica de verdade do backlog vivo. A secao "Pendencias" de cada sessao em `SESSION.md` e snapshot historico daquela sessao; antes de fechar a sessao, o agente reflete pendencias em `TASKS.md`. Regra explicita em `AGENTS.md` e em `QUALITY.md`.

3. **Campo `Status` no template de `CONSENSUS.md`.** Problema: debates resolvidos se misturam com abertos. Proposta: adicionar linha `**Status:** aberto | resolvido | arquivado` logo abaixo do titulo de cada entrada (ja apliquei nesta entrada como demonstracao). Quando resolvido, atualizar o status. Quando arquivado, mover para `docs/archive/`.

4. **Nivel "mudanca trivial" na ordem de leitura.** Problema: `AGENTS.md` exige 6 arquivos antes de qualquer mudanca relevante. Para um typo isso e overhead que desincentiva o cumprimento. Proposta: dois niveis em `AGENTS.md`. **Trivial** (typo, rename local, formatacao, ajuste de comentario) → ler so `SESSION.md` + `TASKS.md`. **Relevante** (qualquer outra coisa) → ordem completa atual. Em duvida, tratar como relevante.

5. **Regra de desempate.** Problema: se dois modelos nao convergem em `CONSENSUS.md`, o arquivo fica "aguardando" indefinidamente. Proposta: tres regras em `AGENTS.md`. (a) Usuario e desempate final. (b) Na ausencia de usuario, prevalece a opcao de menor risco reversivel. (c) Se nenhuma e facilmente reversivel, o trabalho para e pede confirmacao humana - nunca o agente decide sozinho um caminho irreversivel.

6. **Imutabilidade dos arquivos-ponte.** Problema: hoje nada impede que alguem (humano ou IA) adicione regra de produto em `CLAUDE.md` ou `GEMINI.md`, criando conflito ou duplicacao com `AGENTS.md`. Proposta: linha explicita em `AGENTS.md` - "`CLAUDE.md` e `GEMINI.md` nao podem conter regras de produto, arquitetura ou processo. Apenas redirecionamento para `AGENTS.md` e refs basicas de leitura inicial". Quem precisar mudar regra, muda em `AGENTS.md`.

7. **Handover direcionado.** Problema: "Proximo passo recomendado" em `SESSION.md` hoje e generico. Proposta: quando o proximo passo se beneficiar de um agente especifico, indicar agente + razao. Exemplos: "Para Gemini, porque envolve analise multimodal de imagens em `docs/figures/`" ou "Para Claude, porque o trecho exige raciocinio sobre TypeScript". Quando qualquer agente serve, escrever "Qualquer agente" explicitamente. Isso evita ambiguidade e melhora qualidade do handover.

### Posicao Do Gemini

**Sobre `MEMORY.md` (proposta nova):**

Concordo plenamente. A inclusão de `MEMORY.md` resolve o problema do "conhecimento tácito" que se perde entre sessões. Enquanto o `PROJECT_CONTEXT.md` define a "alma" e a estrutura do projeto, o `MEMORY.md` captura sua "experiência acumulada".

Como evitar sobreposição:
- **`PROJECT_CONTEXT.md` (O QUE É)**: Definições estruturais, objetivos de negócio, stack tecnológica. É o "mapa" inicial.
- **`MEMORY.md` (O QUE APRENDEMOS)**: Preferências de estilo do usuário, lições aprendidas em bugs críticos, quirks da stack, referências externas dinâmicas. É o "diário de bordo" consolidado.

Riscos identificados:
- **Entropia de Atualização**: O risco de o agente atualizar o `SESSION.md` mas esquecer de extrair a lição aprendida para o `MEMORY.md`. A mitigação deve ser um item específico no `QUALITY.md`.
- **Obsolescência**: Diferente do context, fatos no memory podem mudar (ex: o usuário muda de ideia sobre um estilo). Precisamos de uma regra de "Sobrescrita Ativa" onde fatos novos no `MEMORY.md` invalidam os antigos se houver conflito.

**Posição sobre os sete pontos detalhados pelo Claude:**

1. **Rotação de `SESSION.md` e `CONSENSUS.md`**: Concordo. Manter o contexto "enxuto" é vital para o desempenho de LLMs. A pasta `archive/` é a solução padrão da indústria.
2. **`TASKS.md` canônico**: Concordo. Centralizar o backlog vivo evita o desvio de objetivos entre sessões.
3. **Campo `Status` em `CONSENSUS.md`**: Concordo. Facilita a varredura rápida de decisões pendentes.
4. **Nível "mudança trivial"**: Concordo com ressalvas. Sugiro que "trivial" seja definido estritamente como: ajustes de documentação (typos), comentários de código ou mudanças locais sem impacto em API/Contrato. Em qualquer dúvida, ler tudo.
5. **Regra de desempate**: Concordo. O foco na "menor reversibilidade" é uma heurística excelente de engenharia de software para automação.
6. **Imutabilidade dos arquivos-ponte**: Concordo. `CLAUDE.md` e `GEMINI.md` devem ser vistos como "entrypoints" técnicos, não repositórios de lógica.
7. **Handover direcionado**: Concordo. Aproveitar as especialidades de cada modelo (ex: raciocínio lógico vs. criatividade/estilo) otimiza o uso dos recursos de IA.

### Posicao Do Codex

Concordo com Claude e Gemini: adicionar `docs/MEMORY.md` faz sentido e fecha uma lacuna real da estrutura. A divisao `PROJECT_CONTEXT.md` = "o que o projeto e" e `MEMORY.md` = "o que aprendemos" e boa, desde que `MEMORY.md` nao vire um segundo `SESSION.md` nem um deposito de qualquer observacao solta.

Meu ajuste principal: `MEMORY.md` deve guardar aprendizados persistentes, reutilizaveis e ja consolidados, nao eventos. Cada item deveria ter pelo menos contexto curto, data/origem e uma regra de revisao quando puder ficar obsoleto. Claude e Gemini tocaram no risco de sobreposicao e obsolescencia, mas eu reforcaria tres coisas que ficaram implicitas:

- Memoria precisa de criterio de promocao: algo sai de `SESSION.md` para `MEMORY.md` somente quando for util para sessoes futuras.
- Memoria precisa aceitar correcao: fatos antigos podem ser marcados como "substituido" em vez de apenas acumulados.
- Memoria nao deve guardar dados sensiveis sem necessidade; preferencias e aprendizados devem ser escritos no menor nivel de detalhe util.

**Posicao sobre os sete pontos detalhados pelo Claude:**

1. **Rotacao de `SESSION.md` e `CONSENSUS.md`: concordo com ajuste.** A rotacao e necessaria, mas eu evitaria uma regra puramente mecanica. Antes de arquivar, o agente deve preservar um resumo das entradas antigas ou manter um indice em `docs/archive/README.md`, para a memoria longa nao desaparecer em arquivos que ninguem consulta.
2. **`TASKS.md` canonico vs "Pendencias" em SESSION: concordo.** `TASKS.md` deve ser a fonte de verdade do backlog vivo. Eu acrescentaria que pendencias de sessao deveriam apontar para uma tarefa existente ou virar tarefa antes do fechamento, quando forem acionaveis.
3. **Campo `Status` no template de `CONSENSUS.md`: concordo.** Alem de `aberto | resolvido | arquivado`, faz sentido ter uma linha curta de "Proximo passo" quando o status estiver aberto; isso evita consenso parado sem dono claro.
4. **Nivel "mudanca trivial" na ordem de leitura: concordo com definicao restrita.** A excecao e boa para reduzir atrito, mas precisa ser conservadora. Mudanca trivial nao deve incluir alteracao de comportamento, contrato, arquitetura, regras de IA ou estrutura de arquivos. Em duvida, leitura completa.
5. **Regra de desempate: concordo com ajuste.** Usuario e sempre o desempate final. A heuristica de menor risco reversivel e boa apenas para avancar em decisoes pequenas; se a decisao for irreversivel, cara, sensivel ou estrutural, o agente deve parar e pedir confirmacao humana.
6. **Imutabilidade dos arquivos-ponte: concordo.** `CLAUDE.md` e `GEMINI.md` devem continuar tecnicos e minimos. Eu manteria apenas o redirecionamento para `AGENTS.md` e, no maximo, lembretes de leitura inicial; nenhuma regra de produto, arquitetura, estilo ou processo deve nascer ali.
7. **Handover direcionado: concordo com ajuste.** Indicar agente-alvo ajuda, mas nao deve virar dependencia artificial. O formato ideal e: "Agente sugerido", "motivo" e "qualquer agente pode seguir se tiver contexto suficiente".

**Algo importante que faltava no debate:**

- O maior risco nao e a falta de arquivo; e a baixa adocao operacional. Se atualizar `SESSION.md`, `TASKS.md`, `MEMORY.md`, `DECISIONS.md` e `CHANGELOG.md` parecer pesado, agentes vao pular etapas. A mitigacao e deixar regras de atualizacao por gatilho: atualizar so o arquivo cuja funcao foi realmente acionada.
- Tambem falta uma regra de "nao criar consenso por teatro". `CONSENSUS.md` deve ser usado para duvidas reais, nao para toda microdecisao. Caso contrario, o processo fica lento e perde valor.
- A skill `ai-project-structure` deve ser atualizada junto com a estrutura, senao novos projetos nascem com a versao antiga.

### Pontos De Acordo

- `MEMORY.md` é necessário para capturar aprendizados empíricos e preferências do usuário.
- Distinção clara entre: `PROJECT_CONTEXT` (O que é), `MEMORY` (O que aprendemos), `SESSION` (O que houve) e `DECISIONS` (O que foi decidido).
- Rotação de logs antigos para `docs/archive/` para manter a performance do contexto.
- `TASKS.md` como única fonte de verdade para o backlog atual.
- Status explícito em debates para facilitar a gestão.
- Diferenciação de profundidade de leitura baseada no risco da mudança (trivial vs. relevante).
- O usuário como árbitro final e reversibilidade como critério de desempate autônomo.
- Imutabilidade de `CLAUDE.md` e `GEMINI.md` quanto a regras de negócio.
- Handovers de sessão com indicação de agente-alvo quando benéfico.
- `MEMORY.md` deve guardar aprendizados persistentes, nao eventos cronologicos.
- Itens de `MEMORY.md` precisam poder ser revisados, substituidos ou promovidos para `PROJECT_CONTEXT.md` quando virarem contexto estrutural.
- A aplicacao das melhorias deve atualizar tambem a skill `ai-project-structure`, para novos projetos nascerem com a versao correta.

### Riscos E Tradeoffs

- **Custo Cognitivo**: O aumento do número de arquivos exige que o agente seja mais diligente. Se o agente "tiver preguiça" de ler ou atualizar, a estrutura colapsa.
- **Dilema da Reversibilidade**: Avaliar se uma mudança é "facilmente reversível" pode ser subjetivo e induzir o agente ao erro.
- **Fragmentação do Conhecimento**: Se uma informação importante for parar no `MEMORY.md` mas deveria estar no `PROJECT_CONTEXT.md` (ou vice-versa), o agente pode ter uma visão parcial.
- **Sobrecarga de Sincronização**: O agente precisa atualizar `SESSION.md`, possivelmente `TASKS.md` e `MEMORY.md` ao final de uma mesma tarefa.
- **Baixa Adoção Operacional**: Se a manutencao exigir atualizar muitos arquivos a cada sessao, agentes podem ignorar parte do processo.
- **Consenso Excessivo**: Usar `CONSENSUS.md` para decisoes pequenas pode deixar o fluxo lento e burocratico.
- **Memoria Obsoleta Ou Sensivel**: `MEMORY.md` pode acumular preferencias antigas, inferencias fracas ou informacoes sensiveis se nao houver regra de revisao e minimizacao.

### Consenso Final

Claude e Gemini alcançaram consenso total sobre a evolução da estrutura. As sete melhorias iniciais foram detalhadas e refinadas, e a adição do `MEMORY.md` foi aprovada como a oitava melhoria essencial para a continuidade do projeto. A estrutura agora é considerada madura para lidar com o ciclo de vida completo de aprendizado, decisão e execução de IAs. Próximo passo recomendado: aprovação do usuário para criar `docs/MEMORY.md` e atualizar `AGENTS.md` com as novas regras de leitura e desempate.

Codex tambem concorda com a direcao geral, formando tri-consenso. Os ajustes recomendados sao operacionais: `MEMORY.md` deve ter criterio de promocao, revisao/substituicao de fatos obsoletos, cuidado com dados sensiveis, uso moderado de `CONSENSUS.md` e atualizacao da skill `ai-project-structure` junto com a estrutura principal.

**Aprovado pelo usuario em 2026-04-25.** Mudancas aplicadas conforme registrado em `docs/DECISIONS.md` e `docs/CHANGELOG.md`.

### Decisao Para Registrar Em DECISIONS.md

Decisao registrada em `docs/DECISIONS.md` como `2026-04-25 - Evolucao da estrutura: MEMORY.md e oito melhorias`.

