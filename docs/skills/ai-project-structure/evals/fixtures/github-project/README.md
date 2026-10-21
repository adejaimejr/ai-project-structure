# Fixture github-project

Dois projetos minimos para exercitar o bloco gerenciado `github` em
`AGENTS.md` (spec 0007): marcadores pareados com versao valida, e versao igual
a do bloco `core`.

- `valido/`: bloco `github` (o do partial `assets/partials/AGENTS-github-block.md`)
  pareado, na mesma versao do bloco `core`. Esperado: exit 0, em `--strict` tambem.
- `invalido/`: bloco `github` sem o marcador `end` e com o start em versao
  diferente da do `core`. Esperado: exit 1 em `--strict`, com ERRO
  `MARCADOR-DESPAREADO`, ERRO `GITHUB-MARCADOR-INVALIDO` e AVISO
  `GITHUB-VERSAO-DIVERGENTE`.

O oracle em `evals/verify_repository.py` confere o conjunto exato de diagnosticos.

Rode com:

```bash
python3 ../../scripts/validate_structure.py valido --strict
python3 ../../scripts/validate_structure.py invalido --strict
```
