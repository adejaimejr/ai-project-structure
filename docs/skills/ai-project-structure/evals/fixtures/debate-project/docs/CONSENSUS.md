# CONSENSUS

Use este arquivo quando modelos diferentes precisarem debater para chegar a um consenso.

## Modelo De Achado

```md
## AAAA-MM-DD - Titulo curto do achado

**Achado:** <identificador livre, ex: N10>

**Status:** aberto | resolvido | arquivado

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim | nao

### Por Que Nada Pegou Antes

- O que passou verde:
- Mecanismo do ponto cego:
```

## Registros

## 2026-09-03 - Nome do campo de rodada em debate longo

**Status:** aberto

**Proximo passo:** o usuario decide ate sexta.

**Metodo:** debate-aberto

**Exposicao previa a outras posicoes:** sim

**Rodada:** 5 de 5

**Pendente da rodada anterior:** a rodada 4 nao olhou o custo de migrar os registros antigos.

### Contexto

- Debate longo e legitimo. Cinco rodadas sem teto, com a pendencia declarada.

### Consenso Final

- (Ainda aberto.)

## 2026-09-03 - Se vale abrir achado para este caso

**Status:** resolvido

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim

### Contexto

- Entrada que **fala** de achado e ate declara `**Escapou de verificacao:**`, e nao declara `**Achado:**`.
- Pelo criterio de aceite da spec 0005, ela segue sendo debate: o formato de achado e opt-in pelo campo `**Achado:**`. Nenhum aviso pode sair daqui.

### Posicao Do Codex

- O formato que teriamos de preencher, se abrissemos achado, seria este:

```md
**Achado:** N10

**Escapou de verificacao:** sim
```

- Esta cerca esta **dentro do corpo de uma entrada**, de proposito. Se `strip_fences` parar de limpar cercas, o `**Achado:**` acima vira declaracao real e esta entrada passa a ser cobrada como achado. Nenhum diagnostico pode sair daqui enquanto a cerca for respeitada.

### Consenso Final

- Nao vale abrir achado: o caso morreu na propria discussao.

## 2026-08-01 - Escolha do formato de data na API

**Status:** resolvido

### Contexto

- Anterior a data de adocao das convencoes, entao sem os campos declarativos.

### Consenso Final

- ISO 8601.
