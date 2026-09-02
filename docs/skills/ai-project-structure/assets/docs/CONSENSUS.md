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
- `**Rodada:**` `N de 3`.

Na rodada 1, cada modelo preenche apenas a propria secao, sem ler as demais. Da rodada 2 em diante a exposicao previa e esperada e deve ser declarada como `sim`. Tres rodadas sem convergencia e o teto: escale para o usuario em vez de abrir a quarta, registrando o `**Proximo passo:**` com dono.

Os tres campos sao autodeclarados. O validador checa presenca e valor permitido, nunca veracidade: nenhum script prova que um modelo nao leu a posicao do outro. O ganho e rastreabilidade, nao garantia.

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 3

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

(Vazio. Adicione novas entradas abaixo conforme houver debates.)
