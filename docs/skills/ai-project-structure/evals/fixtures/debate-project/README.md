# Fixture debate-project

Projeto que **usa consenso e nunca registra achado**. Existe para exercitar
literalmente o criterio de aceite da spec 0005: "projeto que nunca registra
achado nao recebe nenhum aviso novo".

Saida esperada: **nenhum diagnostico**, em `--strict`, exit 0. Um conjunto
vazio parece um teste fraco e nao e: qualquer diagnostico que apareca aqui
reprova, porque o oracle do `verify_repository.py` compara nos dois sentidos.

Os dois lados de `achado-project` tem achado, entao nenhum deles serve para
este controle: la a pergunta e se os avisos certos saem, aqui e se algum sai
onde nao devia.

Quatro controles no mesmo `docs/CONSENSUS.md`:

1. **Cerca dentro do corpo de uma entrada**, citando `**Achado:**` e
   `**Escapou de verificacao:**` como quem discute o formato. Se `strip_fences`
   parar de limpar cercas, aquela citacao vira declaracao real e a entrada passa
   a ser cobrada como achado. Medido por mutacao: quebrando `strip_fences`,
   **so esta fixture acusa**; todas as outras seguem verdes. O modelo de achado
   cercado no topo do arquivo nao serve para isso, porque fica antes de qualquer
   entrada datada e nunca entra em corpo de entrada.
2. **Entrada anterior a data de adocao**, sem os campos declarativos. Cobra-la
   seria retroatividade, que a 2.2.0 proibiu.
3. **Entrada na rodada 5**, com `**Pendente da rodada anterior:**`. Rodada alta
   em debate e legitima desde que a pendencia esteja declarada.
4. **Entrada que declara `**Escapou de verificacao:**` sem declarar
   `**Achado:**`.** Pelo criterio de aceite, ela segue sendo debate: o formato
   de achado e opt-in pelo campo `**Achado:**`. Este controle fixa esse opt-in,
   entao mudar essa regra passa a ser mudanca visivel, e nao silenciosa.

Rode com:

```bash
python3 ../../scripts/validate_structure.py . --strict
python3 ../../scripts/validate_structure.py . --codigos
```
