#!/usr/bin/env python3
"""Portao da T-078: marcador `**Origem:**` no validador, checks AVISO com fixture (DEC-007).

Oito entradas num projeto montado dos assets: E1 automatizada bem formada; E2 sem Manifesto;
E3 Manifesto que nao resolve; E4 participante sem secao; E5 falha sem secao; E6 achado
automatizado bem formado; E7 achado sem a secao de revalidacao; E8 manual sem Origem.
1. E2 a E5 e E7 recebem AVISO em docs/CONSENSUS.md com o proprio titulo como sujeito, sem ERRO;
2. E1, E6 e E8 sem diagnostico; 3. pelo menos tres codigos distintos entre E2 e E5; 4. projeto
limpo dos assets e raiz limpos em --strict; 5. verificador (todo codigo com fixture);
6. versao coerente.
"""

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ROOT, check, ler, montar, resumo, validar, verify_ok, versao_coerente  # noqa: E402

CAMPOS = "**Metodo:** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n\n**Rodada:** 1 de 1\n"


def entrada(titulo, origem=True, manifesto="docs/consensus/run-x/manifesto.json", participantes="alfa, beta, gama",
            falhas="gama", secoes=("Posicao De alfa", "Posicao De beta", "Falha De gama"), achado=None):
    t = f"\n## 2026-09-03 - {titulo}\n\n"
    if achado:
        t += f"**Achado:** {achado}\n\n"
    t += "**Status:** aberto\n\n**Proximo passo:** usuario le e decide\n\n" + CAMPOS
    if achado:
        t += "\n**Escapou de verificacao:** nao\n"
    if origem:
        t += "\n**Origem:** automacao\n"
        if manifesto:
            t += f"\n**Manifesto:** {manifesto}\n"
        if participantes is not None:
            t += f"\n**Participantes:** {participantes}\n"
        if falhas is not None:
            t += f"\n**Falhas:** {falhas}\n"
    t += "\n### Contexto\n\n- contexto.\n"
    for s in secoes:
        t += f"\n### {s}\n\n> posicao ou falha de {s.split()[-1]}.\n"
    t += "\n### Pontos De Acordo\n\n- (A preencher.)\n"
    return t


TITULOS = {
    "E1": "E1 automatizada bem formada",
    "E2": "E2 sem ponte para o manifesto",
    "E3": "E3 com ponte que nao resolve",
    "E4": "E4 participante sem secao",
    "E5": "E5 falha sem secao propria",
    "E6": "E6 achado automatizado bem formado",
    "E7": "E7 achado sem revalidacao",
    "E8": "E8 manual sem Origem",
}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo")
        code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 0 and not out, "4a. projeto limpo montado dos assets passa em --strict", "; ".join(out)[:160])

        r = montar(tmp, "origem")
        (r / "docs" / "consensus" / "run-x").mkdir(parents=True)
        (r / "docs" / "consensus" / "run-x" / "manifesto.json").write_text("{}\n", encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        texto = ler(c)
        texto += entrada(TITULOS["E1"])
        texto += entrada(TITULOS["E2"], manifesto=None)
        texto += entrada(TITULOS["E3"], manifesto="docs/consensus/nao-existe/manifesto.json")
        texto += entrada(TITULOS["E4"], participantes="alfa, beta", falhas="nenhuma", secoes=("Posicao De alfa",))
        texto += entrada(TITULOS["E5"], participantes="alfa, gama", falhas="gama", secoes=("Posicao De alfa",))
        texto += entrada(TITULOS["E6"], participantes="revisor", falhas="nenhuma", secoes=("Revalidacao De revisor",), achado="X-1")
        texto += entrada(TITULOS["E7"], participantes="revisor", falhas="nenhuma", secoes=(), achado="X-2")
        texto += entrada(TITULOS["E8"], origem=False, secoes=("Posicao De alfa",))
        c.write_text(texto, encoding="utf-8")
        code, linhas, err = validar(r, "--strict", "--codigos")
        diag = []
        for l in linhas:
            partes = l.split("|", 3)
            if len(partes) == 4:
                diag.append(tuple(partes))
        por_sujeito = {}
        for nivel, codigo, arquivo, sujeito in diag:
            por_sujeito.setdefault(sujeito, []).append((nivel, codigo, arquivo))

        def avisos(chave):
            return [d for d in por_sujeito.get(f"2026-09-03 - {TITULOS[chave]}", []) if d[0] == "AVISO" and d[2] == "docs/CONSENSUS.md"]

        erros = [d for d in diag if d[0] == "ERRO"]
        for chave in ("E2", "E3", "E4", "E5", "E7"):
            check(avisos(chave) and not erros, f"1. {TITULOS[chave]}: AVISO em docs/CONSENSUS.md com o titulo como sujeito, sem ERRO",
                  ", ".join(sorted({d[1] for d in avisos(chave)})) or f"nenhum diagnostico; stderr={err.strip()[:80]}")
        for chave in ("E1", "E6", "E8"):
            check(not por_sujeito.get(f"2026-09-03 - {TITULOS[chave]}"), f"2. {TITULOS[chave]}: nenhum diagnostico",
                  ", ".join(sorted({d[1] for d in por_sujeito.get(f'2026-09-03 - {TITULOS[chave]}', [])})))
        codigos = {d[1] for chave in ("E2", "E3", "E4", "E5") for d in avisos(chave)}
        check(len(codigos) >= 3, "3. pelo menos tres codigos distintos entre ponte ausente, ponte quebrada, participante sem secao e falha sem secao",
              ", ".join(sorted(codigos)))
        check(code == 1, "1b. o projeto com as entradas malformadas sai 1 em --strict", f"exit {code}")

    code, out, _ = validar(ROOT, "--strict", "--codigos")
    check(code == 0 and not out, "4b. raiz limpa em --strict", "; ".join(out)[:160])
    ok, det = verify_ok()
    check(ok, "5. verify_repository.py exit 0, com todo codigo novo coberto por fixture", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "6. versao 2.11.0 ou acima, coerente", det)
    return resumo("T-078")


if __name__ == "__main__":
    sys.exit(main())
