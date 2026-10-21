#!/usr/bin/env python3
"""Portao da T-104: AVISO de proveniencia incompleta no validador (consenso da T-083, rodada 2).

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: o validador so confere se o manifesto citado existe, nunca o conteudo.

Decisao em `docs/DECISIONS.md` ("Validador avisa corrida incompleta so quando uma entrada de
CONSENSUS.md aponta para ela"). Cada caso monta um projeto limpo dos assets, acrescenta uma
entrada automatizada em `docs/CONSENSUS.md` e um sidecar em `docs/consensus/<run>/`:

1. manifesto `concluida`, bruto presente: sem o codigo novo, `--strict` limpo;
2. manifesto `em-andamento`: AVISO `CONSENSO-ORIGEM-CORRIDA-INCOMPLETA`;
3. manifesto `interrompida`: o mesmo AVISO;
4. manifesto ilegivel (JSON quebrado): o mesmo AVISO;
5. participante com `resultado: posicao` e `stdout.txt` ausente: o mesmo AVISO;
6. participante com `resultado: falha` e `stdout.txt` vazio: sem o codigo (falha registrada);
7. corrida incompleta sem entrada que aponte para ela: sem o codigo;
8. entrada manual (sem `**Origem:**`) apontando para corrida incompleta: sem o codigo;
9. o codigo esta em `CODIGOS`, e o nivel e AVISO (exit 0 sem `--strict`, 1 com);
10. o validador nao escreveu nada no projeto (nao retoma, nao limpa, nao repara);
11. fixture com o codigo declarado no verificador, e verificador em exit 0.
"""

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import SKILL, check, ler, montar, resumo, validar, verify_ok  # noqa: E402

import tempfile  # noqa: E402

CODIGO = "CONSENSO-ORIGEM-CORRIDA-INCOMPLETA"
RUN = "2026-09-03-120000-debate"
ENTRADA = """
## 2026-09-03 - Rodada automatizada de teste

**Status:** aberto

**Proximo passo:** usuario le as posicoes

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

{origem}**Manifesto:** docs/consensus/{run}/manifesto.json

**Participantes:** alfa, beta

**Falhas:** {falhas}

### Contexto

- Teste.

### Posicao De alfa

> Posicao de alfa.

{beta}### Pontos De Acordo

- (A preencher.)

### Riscos E Tradeoffs

- (A preencher.)

### Consenso Final

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)
"""


def manifesto(status="concluida", beta="posicao"):
    return {
        "versao": 1, "run_id": RUN, "modo": "debate", "rodada": 1, "status": status,
        "participantes": [
            {"id": "alfa", "resultado": "posicao", "stdout": "alfa/stdout.txt"},
            {"id": "beta", "resultado": beta, "stdout": "beta/stdout.txt"},
        ],
    }


def montar_caso(tmp, nome, *, man=None, cru=None, beta_stdout="Posicao de beta.\n", beta="posicao",
                com_entrada=True, origem=True):
    r = montar(tmp, nome)
    run = r / "docs" / "consensus" / RUN
    (run / "alfa").mkdir(parents=True)
    (run / "beta").mkdir(parents=True)
    (run / "alfa" / "stdout.txt").write_text("Posicao de alfa.\n", encoding="utf-8")
    if beta_stdout is not None:
        (run / "beta" / "stdout.txt").write_text(beta_stdout, encoding="utf-8")
    texto = cru if cru is not None else json.dumps(man or manifesto(beta=beta), indent=1)
    (run / "manifesto.json").write_text(texto, encoding="utf-8")
    if com_entrada:
        falha = beta != "posicao"
        corpo = ENTRADA.format(
            origem="**Origem:** automacao\n\n" if origem else "",
            run=RUN, falhas="beta" if falha else "nenhuma",
            beta="### Falha De beta\n\n- Exit 1.\n\n" if falha else "### Posicao De beta\n\n> Posicao de beta.\n\n")
        c = r / "docs" / "CONSENSUS.md"
        c.write_text(ler(c).rstrip("\n") + "\n" + corpo, encoding="utf-8")
    return r


def codigos(r, *flags):
    codigo, linhas, _ = validar(r, "--codigos", *flags)
    return codigo, [l for l in linhas if "|" in l]


def tem(linhas, nivel=None):
    return any(l.split("|")[1] == CODIGO and (nivel is None or l.split("|")[0] == nivel) for l in linhas)


def foto(r):
    return sorted((str(p.relative_to(r)), p.stat().st_size) for p in r.rglob("*") if p.is_file())


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = montar_caso(tmp, "c1")
        codigo, linhas = codigos(r, "--strict")
        check(codigo == 0 and not tem(linhas), "1. manifesto concluida e bruto presente: --strict limpo, sem o codigo",
              "; ".join(linhas[:4]) or "exit %s" % codigo)

        for n, status in (("2", "em-andamento"), ("3", "interrompida")):
            r = montar_caso(tmp, "c" + n, man=manifesto(status=status))
            _, linhas = codigos(r)
            check(tem(linhas, "AVISO"), "%s. manifesto %s: AVISO %s" % (n, status, CODIGO), "; ".join(linhas[:4]))

        r = montar_caso(tmp, "c4", cru='{"versao": 1, "status": "concl')
        _, linhas = codigos(r)
        check(tem(linhas, "AVISO"), "4. manifesto ilegivel: AVISO %s" % CODIGO, "; ".join(linhas[:4]))

        r = montar_caso(tmp, "c5", beta_stdout=None)
        _, linhas = codigos(r)
        check(tem(linhas, "AVISO"), "5. participante com posicao e stdout.txt ausente: AVISO %s" % CODIGO,
              "; ".join(linhas[:4]))

        r = montar_caso(tmp, "c6", beta="falha", beta_stdout="")
        codigo, linhas = codigos(r, "--strict")
        check(not tem(linhas), "6. participante com falha registrada e stdout vazio: sem o codigo",
              "; ".join(linhas[:4]) or "exit %s" % codigo)

        r = montar_caso(tmp, "c7", man=manifesto(status="em-andamento"), beta_stdout=None, com_entrada=False)
        codigo, linhas = codigos(r, "--strict")
        check(codigo == 0 and not tem(linhas), "7. corrida incompleta sem entrada que aponte: sem diagnostico, --strict limpo",
              "; ".join(linhas[:4]) or "exit %s" % codigo)

        r = montar_caso(tmp, "c8", man=manifesto(status="em-andamento"), origem=False)
        _, linhas = codigos(r)
        check(not tem(linhas), "8. entrada manual (sem **Origem:**) apontando para corrida incompleta: sem o codigo",
              "; ".join(linhas[:4]))

        r = montar_caso(tmp, "c9", man=manifesto(status="em-andamento"))
        antes = foto(r)
        c_sem, _ = codigos(r)
        c_com, _ = codigos(r, "--strict")
        fonte = ler(SKILL / "scripts" / "validate_structure.py")
        check(CODIGO in fonte.split("def ", 1)[0] and c_sem == 0 and c_com == 1,
              "9. codigo em CODIGOS e nivel AVISO (exit 0 sem --strict, 1 com)", "exit %s / %s" % (c_sem, c_com))
        check(foto(r) == antes, "10. o validador nao escreveu nada no projeto")

    verificador = ler(SKILL / "evals" / "verify_repository.py")
    check(CODIGO in verificador, "11. o codigo aparece num oraculo de fixture do verificador")
    ok, detalhe = verify_ok()
    check(ok, "11b. verify_repository.py em exit 0", detalhe)
    return resumo("T-104")


if __name__ == "__main__":
    sys.exit(main())
