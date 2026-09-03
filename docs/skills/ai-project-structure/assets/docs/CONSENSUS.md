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

## Independencia Declarada

Consenso so vale como segunda opiniao se as posicoes forem independentes. Modelo que le a posicao do outro antes de escrever produz concordancia por cortesia, e consenso fraco fica indistinguivel de consenso forte. Por isso cada entrada declara como foi produzida:

- `**Metodo:**` `pareceres-independentes` (cada modelo responde sozinho e as posicoes sao reunidas depois) ou `debate-aberto` (cada modelo escreve com as demais posicoes a vista).
- `**Exposicao previa a outras posicoes:**` `sim` ou `nao`.
- `**Rodada:**` `N de N`.

Na rodada 1, cada modelo preenche apenas a propria secao, sem ler as demais. Da rodada 2 em diante a exposicao previa e esperada e deve ser declarada como `sim`.

Nao ha teto de rodadas. Trabalho dificil chega a muitas revalidacoes sem que isso seja fracasso, e o teto de tres da versao 2.2.0 foi escrito sem evidencia. Da quarta rodada em diante, em compensacao, a entrada declara `**Pendente da rodada anterior:**` dizendo o que a rodada anterior deixou em aberto. Rodada por cerimonia nao tem o que escrever ali.

Os campos sao autodeclarados. O validador checa presenca e valor permitido, nunca veracidade: nenhum script prova que um modelo nao leu a posicao do outro, nem julga se a pendencia declarada justifica mais uma rodada. O ganho e rastreabilidade, nao garantia.

## Achado

Nem todo uso deste arquivo e debate. Quando a validacao cruzada encontra um defeito, risco ou lacuna, isso e um **achado**, e vira entrada propria, com `**Status:**` e `**Proximo passo:**` proprios.

- `**Achado:**` traz o identificador do achado. Ele e livre, amarrado a unidade de trabalho do projeto (`N10`, `API-3`, o que o projeto ja usar): o validador confere que o campo existe e tem valor, e nunca opina sobre o valor. Sem identificador nao da para escrever "revalidacao do N10" nem saber se um achado ficou esquecido.
- `**Escapou de verificacao:**` `sim` ou `nao`, dizendo se a verificacao que ja existia deixou o achado passar.
- Declarou `sim`? A entrada traz a secao `### Por Que Nada Pegou Antes`, com o que passou verde e qual foi o mecanismo do ponto cego. E o que transforma defeito escapado em conserto de portao, em vez de anedota.
- A disposicao do achado e de quem o registra; a revalidacao dela e de outro modelo, e conta como rodada.
- Achado so vira tarefa em `TASKS.md` **depois** de a disposicao concluir que ha trabalho, e a tarefa cita o achado na linha. Entre registrar e dispor existe uma janela em que o item so vive aqui: quem fecha a sessao precisa olhar os achados abertos.

## Ponto Cego Da Validacao Cruzada

Rodada verde e ausencia de objecao, nao prova de que funciona. Modelos que leem o mesmo texto herdam o mesmo ponto cego, e defeito que so existe em contexto de execucao real sobrevive a N rodadas de leitura.

Por isso N rodadas verdes nao valem confianca proporcional a N: elas medem quantas vezes ninguem objetou. Quando um achado escapa da verificacao que ja existia, o conserto e no portao, e nao so no achado.

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

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

(Vazio. Adicione novas entradas abaixo conforme houver debates.)
