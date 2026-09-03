# Fixture achado-project

Dois projetos minimos para exercitar o formato de **achado** em
`docs/CONSENSUS.md`, introduzido na versao 2.4.0 da estrutura.

Os checks novos sao AVISO, nao ERRO, entao o exit code so muda com `--strict`.
E de proposito: achado mal preenchido nao invalida a estrutura do projeto.

- `valido/`: um achado que escapou de verificacao, com identificador, com a
  secao "Por Que Nada Pegou Antes" e com `**Pendente da rodada anterior:**` na
  rodada 5; e um achado que nao escapou, sem a secao. Esperado: exit 0, tambem
  em `--strict`.
- `invalido/`: tres achados, cobrindo os cinco avisos do formato (sem
  `**Escapou de verificacao:**`; declarou `sim` sem a secao; rodada acima de 3
  sem `**Pendente da rodada anterior:**`; identificador vazio; valor fora de
  `sim | nao`). Esperado: exit 0 sem `--strict`, exit 1 com `--strict`.

Nos dois casos a **primeira entrada e a mesma entrada de debate**, sem
`**Achado:**`. E o controle do criterio de aceite "projeto que nunca registra
achado nao recebe nenhum aviso novo": nenhum aviso pode citar essa entrada.

Rode com:

```bash
python3 ../../scripts/validate_structure.py valido --strict
python3 ../../scripts/validate_structure.py invalido --strict
```
