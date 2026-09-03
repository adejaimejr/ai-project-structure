# Spec 0005 - Consenso que serve para achado, e nao so para debate

**Status:** Definida
**Criada em:** 2026-09-03
**Definida em:** 2026-09-03 (apos o usuario responder P-1 a P-6; as respostas viraram DEC-002 a DEC-007)
**Esforco:** M, quatro lacunas independentes no mesmo modulo. Depende de respostas do usuario antes de virar `Definida`.

## Problema E Resultado Esperado

A evidencia desta spec e um projeto real do usuario que usa a estrutura sob pressao: seis modelos distintos, mais de sessenta entradas de consenso, vinte e cinco achados catalogados e ate sete rodadas de revalidacao numa unidade so. Ele foi lido como caso de estudo, com autorizacao, e **nao e alvo de alteracao por esta spec**.

- Problema 1: o template de `CONSENSUS.md` so descreve **debate**, com posicao por modelo e consenso final. O uso real convergiu para outra forma: **achado com identificador, disposicao do autor, e revalidacao independente da disposicao**. A estrutura tem `T-NNN` para tarefa e `DEC-NNN` para decisao, e nada para achado. Sem identificador nao da para escrever "revalidacao do N10", nem rastrear se um achado foi disposto ou esquecido.
- Problema 2: a 2.2.0 fixou `**Rodada:** N de 3` com teto de tres e ordem de escalar para o usuario acima disso. O uso real chegou a **sete revalidacoes independentes** numa unidade, sem que isso fosse fracasso. Ou o teto esta errado para trabalho dificil, ou falta dizer o que significa ultrapassa-lo.
- Problema 3: o registro do achado mais caro daquele projeto trouxe uma secao que o template nao tem: **"Por Que Nada Pegou Antes"**, listando o que passou verde (suite completa, prova por `curl`, cinco rodadas de quatro modelos) e o mecanismo do ponto cego. E a secao que transforma defeito escapado em conserto de portao, e ela nasceu na mao, sem a skill sugerir.
- Problema 4: o aviso de que **validacao cruzada nao pega defeito que so existe em contexto de execucao real** hoje so existe em `references/loop.md`, sob o titulo "A Evidencia Vale O Que O Portao Vale". Quem usa consenso sem usar loop nunca le. Sem esse aviso, N rodadas verdes viram sensacao de seguranca.

- Resultado esperado 1: registrar achado e revalidar disposicao passa a ser forma prevista, com identificador proprio, e nao improviso de cada projeto.
- Resultado esperado 2: o teto de rodadas passa a refletir trabalho dificil de verdade, sem virar carimbo.
- Resultado esperado 3: todo achado escapado deixa escrito por que a verificacao existente nao o pegou, o que vira melhoria de portao em vez de anedota.
- Resultado esperado 4: quem le sobre consenso le tambem o limite dele, sem depender de ter ativado o modulo de loop.

## Escopo

### Incluido

- Formato de **achado** no template de `CONSENSUS.md` e no bloco core: identificador, disposicao, revalidacao independente da disposicao.
- Secao **"Por Que Nada Pegou Antes"** para achado, com o que passou verde e o mecanismo do ponto cego.
- Revisao do teto de rodadas a luz do uso real.
- Aviso do ponto cego da validacao cruzada onde quem usa consenso vai ler.
- Checks correspondentes em `validate_structure.py`, na medida em que sejam verificaveis por forma e nao por conteudo.
- Versao da skill para 2.4.0 e marcadores dos blocos gerenciados para v2.4.0, porque o bloco core muda.

### Fora Do Escopo

- **Automacao do consenso**: rodar a mesma pergunta em N agentes isolados para produzir posicoes independentes por construcao. Depende desta spec estar fechada, e merece a propria. A evidencia de que vale existe (24 dos 25 achados daquele projeto vieram de validacao cruzada), e a de que nao resolve tudo tambem (o vigesimo quinto escapou de cinco rodadas por quatro modelos).
- Alterar qualquer projeto que nao seja este repositorio.
- Validador conferindo **conteudo** de achado ou de disposicao. A forma e verificavel; o merito nao.

## Criterios De Aceite

Verificaveis por comando:

- Entrada de consenso que declara `**Achado:**` e tratada como achado pelo validador; entrada sem esse campo segue sendo debate e nao ganha cobranca nova.
- Achado sem `**Escapou de verificacao:**` gera AVISO; com valor fora de `sim | nao` gera AVISO.
- Achado com `**Escapou de verificacao:** sim` e sem a secao "Por Que Nada Pegou Antes" gera AVISO.
- `**Rodada:** N de N` com N maior que 3 e sem `**Pendente da rodada anterior:**` gera AVISO. Substitui a regra da 2.2.0, que exigia `**Proximo passo:**` acima de 3.
- Projeto que nunca registra achado nao recebe nenhum aviso novo: nada do formato de achado dispara em entrada de debate.
- Bloco core identico entre raiz e `assets/AGENTS.md`, ambos em v2.4.0, e o aviso do ponto cego cabe em ate quatro linhas.
- Templates de `CONSENSUS.md` trazem o modelo de achado, alem do modelo de debate que ja existe.
- `verify_repository.py` em exit 0, e nenhum travessao (U+2014) em arquivo novo ou alterado.

Julgados na mao, sem runner hoje:

- Se a secao "Por Que Nada Pegou Antes", quando preenchida, analisa o mecanismo do ponto cego em vez de repetir "nada a declarar". O validador confere presenca; merito nao da para verificar por script, e essa e a mesma limitacao declarada na 2.2.0 para os campos de independencia.

## Decisoes

- DEC-001: o projeto usado como evidencia foi lido em modo somente-leitura, a pedido do usuario, e nao sera alterado por esta spec. Motivo: ele e a fonte de evidencia; muda-lo contaminaria a propria evidencia, e a decisao de atualizar a estrutura dele e do usuario, em outro momento.

- DEC-002 (P-1, decidida pelo usuario em 2026-09-03): o identificador de achado e **livre**, amarrado a unidade de trabalho de cada projeto, e nao um `A-NNN` global. Motivo: e o que o uso real produziu, e prefixo global engessaria projetos que ja tem a propria nomenclatura. Consequencia aceita: o validador **nao verifica** unicidade nem se uma revalidacao aponta para achado existente, diferente de `(spec: NNNN-slug)`, que resolve hoje. Mitigacao a avaliar na implementacao: o identificador fica livre, mas a entrada o **declara** num campo fixo, o que permite conferir presenca sem opinar sobre valor.
- DEC-004 (P-2, decidida pelo usuario em 2026-09-03): **o teto de tres rodadas deixa de existir**, e no lugar dele cada rodada acima da terceira declara `**Pendente da rodada anterior:**`, dizendo o que a anterior deixou em aberto. Motivo: o teto foi escrito sem evidencia e o uso real chegou a sete rodadas sem que isso fosse fracasso; o proposito original, evitar rodada por cerimonia, sobrevive na exigencia de justificar a continuidade. O validador confere presenca do campo, nunca a qualidade da justificativa.
- DEC-005 (P-3, decidida pelo usuario em 2026-09-03): achado e **entrada propria** em `CONSENSUS.md`, com `Status` e `Proximo passo` proprios, e nao subsecao de uma entrada de rodada. Motivo: e o que o uso real produziu, e so assim da para dizer que um achado especifico esta aberto ou disposto. Consequencia aceita: o arquivo cresce mais rapido, e a rotacao para `docs/archive/` deixa de ser opcional em projeto com muitos achados.
- DEC-006 (P-4, decidida pelo usuario em 2026-09-03): achado vira tarefa em `TASKS.md` **somente depois de a disposicao concluir que ha trabalho**, e a tarefa cita o achado na linha. Motivo: abrir tarefa para todo achado encheria o backlog com item que a disposicao descarta. Risco aceito: entre registrar e dispor existe uma janela em que o item so vive no consenso, e quem fecha a sessao precisa olhar os achados abertos.
- DEC-007 (P-5, decidida pelo usuario em 2026-09-03): a secao "Por Que Nada Pegou Antes" e obrigatoria **quando o achado escapou de verificacao existente**, e dispensada quando a propria validacao o pegou de primeira. Para isso ser verificavel sem julgar merito, o achado declara `**Escapou de verificacao:** sim | nao`, no mesmo padrao dos campos de independencia da 2.2.0: o validador cobra a secao quando a declaracao for `sim`.
- DEC-003 (P-6, decidida pelo usuario em 2026-09-03): o aviso sobre o ponto cego da validacao cruzada vai para o **bloco core**, e nao so para o template de `CONSENSUS.md`. Motivo: quem mais precisa do aviso e quem confia em varias rodadas, e essa confianca se forma antes de a pessoa abrir o template. Consequencia aceita: todo projeto paga a leitura, inclusive quem nunca usa consenso, entao o texto tem de ser curto o bastante para justificar o custo permanente.

## Tarefas

- T-046: bloco core v2.4.0, template de CONSENSUS.md com o modelo de achado, e o aviso do ponto cego
- T-047: checks do formato de achado e do teto de rodadas no validador
- T-048: fixture e evals do formato de achado
- T-049: dogfood, CHANGELOG e reinstalacao com paridade

## Perguntas Abertas

- (Vazio. As seis perguntas do Rascunho foram respondidas pelo usuario em 2026-09-03 e viraram DEC-002 a DEC-007.)

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
