# CONSENSUS

## Registros

## 2026-09-03 - Escolha do formato de data na API

**Status:** resolvido

**Metodo:** debate-aberto

**Exposicao previa a outras posicoes:** sim

**Rodada:** 2 de 2

### Contexto

- Dois formatos candidatos.

### Pergunta Ou Decisao

- Qual formato adotar?

### Consenso Final

- ISO 8601.

## 2026-09-03 - Datas sem fuso passam pelo parser

**Achado:** N10

**Status:** resolvido

**Proximo passo:** (nao se aplica, achado disposto)

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** sim

**Rodada:** 5 de 5

**Escapou de verificacao:** sim

**Pendente da rodada anterior:** a rodada 4 concordou com a disposicao mas nao
olhou o caminho de importacao em lote, que usa outro parser.

### Contexto

- Encontrado por modelo distinto ao revisar a disposicao do achado N9.

### O Que Foi Encontrado

- Data sem fuso e aceita e interpretada como UTC em silencio.

### Disposicao

- Rejeitar a data sem fuso na borda, com erro explicito. Virou T-001.

### Revalidacao

- Modelo distinto confirmou a disposicao e apontou o caminho de importacao em
  lote, que ficou para a rodada seguinte.

### Por Que Nada Pegou Antes

- O que passou verde: a suite inteira, incluindo os testes do parser, e duas
  rodadas de revisao por modelos diferentes.
- Mecanismo do ponto cego: todos os casos de teste do parser foram escritos com
  fuso explicito, entao o ramo sem fuso nunca foi exercitado por ninguem.
- Conserto de portao proposto: caso de teste sem fuso na suite do parser.

### Decisao Para Registrar Em DECISIONS.md

- Data sem fuso e erro na borda, nunca UTC implicito.

## 2026-09-03 - Cache do parser guarda objeto mutavel

**Achado:** N11

**Status:** resolvido

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** nao

### Contexto

- A propria revisao pegou de primeira.

### O Que Foi Encontrado

- O cache devolve a mesma instancia para chamadores diferentes.

### Disposicao

- Devolver copia. Sem tarefa: corrigido na mesma revisao.
