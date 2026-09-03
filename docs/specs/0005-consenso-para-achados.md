# Spec 0005 - Consenso que serve para achado, e nao so para debate

**Status:** Rascunho
**Criada em:** 2026-09-03
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

### Fora Do Escopo

- **Automacao do consenso**: rodar a mesma pergunta em N agentes isolados para produzir posicoes independentes por construcao. Depende desta spec estar fechada, e merece a propria. A evidencia de que vale existe (24 dos 25 achados daquele projeto vieram de validacao cruzada), e a de que nao resolve tudo tambem (o vigesimo quinto escapou de cinco rodadas por quatro modelos).
- Alterar qualquer projeto que nao seja este repositorio.
- Validador conferindo **conteudo** de achado ou de disposicao. A forma e verificavel; o merito nao.

## Criterios De Aceite

Nao podem ser escritos ainda: dependem das respostas em "Perguntas Abertas". Escrever agora seria inventar criterio, que e o que a regra "Nunca Inferir" proibe. O que ja se sabe:

- Nenhum travessao (U+2014) em arquivo novo ou alterado.
- Projeto que nao usa achado nao paga nada por ele.
- `verify_repository.py` continua em exit 0.

## Decisoes

- DEC-001: o projeto usado como evidencia foi lido em modo somente-leitura, a pedido do usuario, e nao sera alterado por esta spec. Motivo: ele e a fonte de evidencia; muda-lo contaminaria a propria evidencia, e a decisao de atualizar a estrutura dele e do usuario, em outro momento.

## Tarefas

- (Vazio ate a spec virar `Definida`.)

## Perguntas Abertas

- P-1: **qual o identificador de achado?** Um `A-NNN` global, no padrao de `T-NNN` e `DEC-NNN`, que o validador consegue conferir quanto a unicidade? Ou identificador livre, amarrado a unidade de trabalho do projeto, como o uso real fez? Livre e mais fiel ao que aconteceu na pratica e impede qualquer verificacao automatica.
- P-2: **o teto de rodadas vira o que?** Sobe para um numero maior, some, ou vira "sem teto, mas cada rodada acima de tres precisa dizer o que a anterior deixou em aberto"? A ultima opcao mantem o proposito original, que era evitar rodada por cerimonia, sem contrariar o uso real.
- P-3: **achado e entrada propria em `CONSENSUS.md`, ou secao dentro de uma entrada?** Entrada propria da rastreabilidade e faz o arquivo crescer rapido; secao agrupa por tema e dificulta apontar para um achado especifico.
- P-4: **achado que exige trabalho abre tarefa em `TASKS.md` automaticamente?** Se nao abrir, o achado pode morrer no registro. Se abrir sempre, todo achado vira backlog, inclusive os que a disposicao descarta.
- P-5: **"Por Que Nada Pegou Antes" e obrigatoria em achado, ou so recomendada?** Obrigatoria garante a analise do ponto cego; tambem cria campo que se preenche com "nada a declarar" quando ninguem quer pensar.
- P-6: **o aviso do ponto cego vai no bloco core, que todo projeto le, ou so no template de `CONSENSUS.md`?** No core, todo projeto paga a leitura, inclusive quem nunca usa consenso. No template, so quem abre o arquivo ve, e quem mais precisa e justamente quem ja esta escrevendo consenso.

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)
