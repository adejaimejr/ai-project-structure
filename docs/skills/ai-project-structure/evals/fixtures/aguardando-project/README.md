# Fixture aguardando-project

Dois projetos minimos para exercitar a secao `## Aguardando Usuario` e a
evidencia de fechamento, introduzidas na versao 2.2.0 da estrutura.

- `valido/`: tarefa aguardando com `**Pergunta:**` e `**Resposta:**`, e tarefa
  concluida que declarou `(verifica:)` e registrou o resultado do comando.
  Esperado: exit 0.
- `invalido/`: a mesma tarefa aguardando, sem a sub-linha `**Pergunta:**`.
  Esperado: exit 1, com o erro apontando a tarefa. Traz tambem T-007, bloqueada
  ha mais que `BLOCKED_MAX_DAYS` de proposito, para `TASK-BLOQUEADA-ANTIGA`.

As datas de `(bloqueada:)` sao o token `{{HOJE-N}}` (N dias antes do dia da
execucao), que `verify_repository.py` materializa em pasta temporaria. O
validador compara essa data com `date.today()`, e uma data absoluta aqui
envelhece sozinha: em 2026-10-17 as datas de setembro passaram do limite e o
verificador caiu de 74 para 71 sem regressao nenhuma (T-085). Rodando o
validador direto nesta pasta, o token sai como `TASK-BLOQUEADA-FORMATO`
(aviso); os exit codes acima continuam valendo fora de `--strict`.

Nos dois casos a tarefa T-003 cita T-001 no meio da descricao. E de proposito:
guarda contra a regressao em que o validador tratava qualquer `T-NNN` da linha
como ID da tarefa e acusava referencia legitima como ID duplicado.

Rode com:

```bash
python3 ../../scripts/validate_structure.py valido
python3 ../../scripts/validate_structure.py invalido
```
