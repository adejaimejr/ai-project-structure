# ARCHITECTURE

Use este arquivo para documentar a arquitetura do projeto.

## Visao Geral

Descrever aqui a estrutura tecnica, os principais componentes e como eles se conectam.

## Modulos Ou Areas

- `AGENTS.md`: regras centrais para agentes.
- `docs/`: memoria e documentacao operacional do projeto.

## Fluxos Importantes

### Fluxo De Trabalho Com IA

1. Agente entra pelo arquivo proprio ou por `AGENTS.md`.
2. Agente le a memoria em `docs/`.
3. Agente executa a tarefa.
4. Agente valida o resultado.
5. Agente atualiza `SESSION.md` e demais arquivos de memoria quando necessario.

### Fluxo De Consenso

1. Uma duvida relevante aparece.
2. Os modelos registram suas posicoes em `CONSENSUS.md`.
3. O consenso final e definido.
4. A decisao relevante e copiada para `DECISIONS.md`.

## Integracoes

Listar aqui APIs, servicos externos, bancos de dados e automacoes quando existirem.

## Riscos Arquiteturais

- Duplicar instrucoes entre arquivos de agentes.
- Esquecer de atualizar `SESSION.md`.
- Registrar debates em `CONSENSUS.md` sem transformar decisoes importantes em `DECISIONS.md`.
