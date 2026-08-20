# Specs

Modulo opcional. Cada arquivo aqui descreve **o que sera construido** em um trabalho tamanho-feature, antes de comecar a construir.

## Quando Criar Uma Spec

Crie uma spec quando o trabalho:

- atravessa mais de uma sessao, ou gera mais de ~3 tarefas;
- muda contrato, arquitetura ou modelo de dados;
- tem ambiguidade que precisa de criterios de aceite explicitos.

Va direto para `TASKS.md`, sem spec, quando for mudanca pequena, correcao ou ajuste. A regra completa esta em `AGENTS.md`.

## Convencoes

- Nome do arquivo: `NNNN-slug.md`, sequencial (ex: `0001-login-social.md`). Nunca reutilize um numero.
- Status no arquivo: `Rascunho → Definida → Em andamento → Concluida`. `Cancelada` e o outro estado terminal valido.
- **Anti-drift**: `docs/TASKS.md` e a unica fonte de status das tarefas. A spec so lista os T-IDs que lhe pertencem; nunca marque andamento de tarefa dentro da spec. Cada tarefa em `TASKS.md` aponta de volta com `(spec: NNNN-slug)`.
- Criterios de aceite nunca sao inventados: faltou contexto, pergunte (regra "Nunca Inferir" em `AGENTS.md`) e registre em "Perguntas Abertas".
- Mudou o requisito depois de `Definida`? Reabra apenas as secoes afetadas e registre a mudanca em "Decisoes" (`DEC-NNN`).
- Spec so vira `Concluida` com "Evidencia De Conclusao" preenchida.
- Decisao com impacto alem da spec deve ser copiada para `docs/DECISIONS.md`.

## Modelo De Spec

```md
# Spec NNNN - Titulo curto

**Status:** Rascunho
**Criada em:** AAAA-MM-DD
**Esforco:** P | M | G, com justificativa em uma frase (opcional)

## Problema E Resultado Esperado

- Problema: (A preencher.)
- Resultado esperado: (A preencher.)

## Escopo

### Incluido

- (A preencher.)

### Fora Do Escopo

- (A preencher.)

## Criterios De Aceite

- (Verificaveis. Sem quantidade minima. Nunca inventados; em duvida, pergunte.)

## Decisoes

- DEC-001: (decisao local da spec; se tiver impacto de projeto, copie para `docs/DECISIONS.md`)

## Tarefas

- T-NNN: rotulo curto (status e andamento vivem so em `docs/TASKS.md`)

## Perguntas Abertas

- (Perguntas adiadas com "Avançar" ou lacunas de contexto. Vazio = nada pendente.)

## Evidencia De Conclusao

- Verificacao: (comando executado ou checagem manual feita)
- Resultado: (A preencher.)
```
