# Fixture aguardando-project

Dois projetos minimos para exercitar a secao `## Aguardando Usuario` e a
evidencia de fechamento, introduzidas na versao 2.2.0 da estrutura.

- `valido/`: tarefa aguardando com `**Pergunta:**` e `**Resposta:**`, e tarefa
  concluida que declarou `(verifica:)` e registrou o resultado do comando.
  Esperado: exit 0.
- `invalido/`: a mesma tarefa aguardando, sem a sub-linha `**Pergunta:**`.
  Esperado: exit 1, com o erro apontando a tarefa.

Rode com:

```bash
python3 ../../scripts/validate_structure.py valido
python3 ../../scripts/validate_structure.py invalido
```
