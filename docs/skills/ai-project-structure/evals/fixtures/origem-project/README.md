# Fixture origem-project

Dois projetos minimos para exercitar o marcador `**Origem:**` em
`docs/CONSENSUS.md` (spec 0006, DEC-007): a forma da entrada escrita por
automacao, com `**Manifesto:**`, `**Participantes:**`, `**Falhas:**` e uma
secao por participante.

Os checks sao AVISO, nao ERRO, entao o exit code so muda com `--strict`
(decisao de 2026-09-03). O oracle em `evals/verify_repository.py` confere quais
avisos saem, por codigo e por sujeito.

- `valido/`: um debate e um achado automatizados bem formados (o achado usa
  `### Revalidacao De <id>`, o debate usa `### Posicao De <id>` e
  `### Falha De <id>`), um achado de duas rodadas com dois manifestos na lista
  de `**Manifesto:**` (separados por virgula), e uma entrada manual de
  controle. Esperado: exit 0, em `--strict` tambem.
- `invalido/`: a entrada manual de controle, que tem secoes `### Posicao De`
  soltas e nao pode receber diagnostico, seguida de seis entradas com
  `**Origem:**` malformada: sem `**Manifesto:**`; manifesto que nao resolve;
  participante sem secao; falha sem `### Falha De`; achado sem
  `### Revalidacao De`; achado com dois manifestos na lista em que um nao
  resolve (um aviso por caminho quebrado). Esperado: exit 1 em `--strict`.

Rode com:

```bash
python3 ../../scripts/validate_structure.py valido --strict
python3 ../../scripts/validate_structure.py invalido --strict
```
