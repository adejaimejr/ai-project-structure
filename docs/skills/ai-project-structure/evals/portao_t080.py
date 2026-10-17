#!/usr/bin/env python3
"""Portao da T-080: rodada 2 com as posicoes anteriores na integra (DEC-006).

1. Rodada 2 com `--anterior <run da rodada 1>`: exit 0, entrada com Rodada 2 de 2, Exposicao
   sim, Metodo; 2. o prompt traz o stdout de cada agente da rodada 1 byte a byte, inclusive um
   de ~40KB com marca no fim; 3. contemporaneas continuam isoladas, e a entrada da rodada 1 fica
   visivel no CONSENSUS.md da copia; 4. manifesto com os anteriores e seus sha256; 5. `--anterior`
   arquivo entra verbatim; 6. rodada 2 sem --anterior, --anterior inexistente e rodada 4 sem
   --pendente: exit 1 sem chamar agente; 7. rodada 1 continua retendo os registros; 8. bateria
   >= 48; 9. versao; 10. verificador.
"""

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (agente, ambiente, bateria_minimo, campo, check, consenso, entradas,  # noqa: E402
                                 entrada_de_debate, ler, manifesto, montar, prompts, resumo, rodadas,
                                 sha256, verify_ok, versao_coerente)

PERGUNTA = "Pergunta do portao T-080.\n\nTOKEN-PERGUNTA-080: seguimos?\n"
AG_ALFA1 = r'''
echo "TOKEN-A1-080 posicao da rodada um"
head -c 40000 /dev/zero | tr '\0' 'x'
echo
echo "FIM-A1-080"
'''
AG_BETA1 = "echo 'TOKEN-B1-080 outra posicao da rodada um'\n"
AG_ALFA2 = r'''
P="${@: -1}"
case "$P" in *TOKEN-B1-080*) echo VEJO-B1;; esac
case "$P" in *FIM-A1-080*) echo VEJO-FIM;; esac
case "$P" in *TOKEN-MANUAL-080*) echo VEJO-MANUAL;; esac
echo "TOKEN-A2-080 posicao da rodada dois"
'''
AG_BETA2 = r'''
for i in $(seq 1 60); do
  if ls "$PROJETO_REAL"/docs/consensus/*/alfa2/stdout.txt >/dev/null 2>&1; then break; fi
  sleep 0.5
done
if ls "$PROJETO_REAL"/docs/consensus/*/alfa2/stdout.txt >/dev/null 2>&1; then echo VI-BRUTO-DE-ALFA2; else echo TIMEOUT; fi
if grep -rq "TOKEN-A2-080" . 2>/dev/null; then echo VAZOU; else echo ISOLADO; fi
if grep -q "Rodada um T-080" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-REGISTROS; fi
echo "TOKEN-B2-080 posicao da rodada dois"
'''
AG_OLHA = r'''
if grep -q "TOKEN-EXISTENTE-080" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-EXISTENTE; fi
echo "posicao"
'''


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-alfa1", AG_ALFA1), ("ag-beta1", AG_BETA1), ("ag-alfa2", AG_ALFA2), ("ag-beta2", AG_BETA2), ("ag-olha", AG_OLHA)):
            agente(tmp, nome, corpo)

        r = montar(tmp, "c1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        env = ambiente(tmp, PROJETO_REAL=r)
        code1, out1 = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                                "--agente", "alfa1", "ag-alfa1", "--agente", "beta1", "ag-beta1", "--titulo", "Rodada um T-080"], env)
        runs1 = rodadas(r)
        run1 = runs1[0] if runs1 else None
        if run1 is None:
            check(False, "0. rodada 1 de preparo (depende de T-076)", f"exit {code1}; {out1.strip()[-120:]}")
        antes = ler(c)
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"), "--rodada", "2",
                              "--anterior", str(run1 or r), "--agente", "alfa2", "ag-alfa2", "--agente", "beta2", "ag-beta2",
                              "--titulo", "Rodada dois T-080"], env)
        depois = ler(c)
        novo = depois[len(antes):] if depois.startswith(antes) else ""
        check(code == 0 and entradas(novo) and campo(novo, "Rodada") == "2 de 2"
              and campo(novo, "Exposicao previa a outras posicoes") == "sim" and campo(novo, "Metodo") == "pareceres-independentes",
              "1. rodada 2 sai 0 com Rodada 2 de 2, Exposicao sim e Metodo pareceres-independentes",
              f"exit {code} rodada={campo(novo, 'Rodada')} exp={campo(novo, 'Exposicao previa a outras posicoes')}")

        run2 = next((x for x in rodadas(r) if x != run1), None)
        prompt = ler(run2 / "alfa2" / "prompt.txt") if run2 and (run2 / "alfa2" / "prompt.txt").is_file() else ""
        saida_a2 = ler(run2 / "alfa2" / "stdout.txt") if run2 and (run2 / "alfa2" / "stdout.txt").is_file() else ""
        brutos1 = [ler(run1 / pid / "stdout.txt") for pid in ("alfa1", "beta1")] if run1 else []
        check(brutos1 and all(b in prompt for b in brutos1) and "VEJO-B1" in saida_a2 and "VEJO-FIM" in saida_a2,
              "2. prompt da rodada 2 traz o stdout de cada agente da rodada 1 byte a byte, inclusive os 40KB com a marca no fim",
              f"prompt={len(prompt)} bytes; alfa2={saida_a2.strip().replace(chr(10), ' | ')[:80]}")

        saida_b2 = ler(run2 / "beta2" / "stdout.txt") if run2 and (run2 / "beta2" / "stdout.txt").is_file() else ""
        check("VI-BRUTO-DE-ALFA2" in saida_b2 and "ISOLADO" in saida_b2 and "VAZOU" not in saida_b2 and "VEJO-REGISTROS" in saida_b2,
              "3. contemporanea continua isolada e a entrada publicada da rodada 1 fica visivel na copia",
              saida_b2.strip().replace("\n", " | ")[:120])

        m2 = manifesto(run2) if run2 else {}
        hashes = {a.get("sha256") for a in m2.get("anteriores", []) if isinstance(a, dict)}
        esperados = {sha256(run1 / pid / "stdout.txt") for pid in ("alfa1", "beta1")} if run1 else {"?"}
        check(esperados <= hashes and all(str(a.get("caminho") or "") for a in m2.get("anteriores", [])),
              "4. manifesto lista os anteriores com caminho e sha256 de cada stdout", f"anteriores={len(m2.get('anteriores', []))}")

        manual = tmp / "anterior-manual.md"
        manual.write_text("Posicao manual anterior: TOKEN-MANUAL-080.\n", encoding="utf-8")
        r5 = montar(tmp, "c5")
        (r5 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code, out = consenso(["debate", "--projeto", str(r5), "--pergunta", str(r5 / "pergunta.md"), "--rodada", "2",
                              "--anterior", str(manual), "--agente", "alfa2", "ag-alfa2", "--agente", "beta1", "ag-beta1"], ambiente(tmp, PROJETO_REAL=r5))
        runs5 = rodadas(r5)
        prompt5 = ler(runs5[0] / "alfa2" / "prompt.txt") if runs5 and (runs5[0] / "alfa2" / "prompt.txt").is_file() else ""
        saida5 = ler(runs5[0] / "alfa2" / "stdout.txt") if runs5 and (runs5[0] / "alfa2" / "stdout.txt").is_file() else ""
        check(code == 0 and ler(manual) in prompt5 and "VEJO-MANUAL" in saida5,
              "5. --anterior com arquivo entra verbatim no prompt", f"exit {code}")

        r6 = montar(tmp, "c6")
        (r6 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        log6 = tmp / "prompts-c6.txt"
        env6 = ambiente(tmp, LOG_PROMPT=log6)
        base6 = ["debate", "--projeto", str(r6), "--pergunta", str(r6 / "pergunta.md"), "--agente", "alfa2", "ag-alfa2", "--agente", "beta1", "ag-beta1"]
        code_a, _ = consenso(base6 + ["--rodada", "2"], env6)
        code_b, _ = consenso(base6 + ["--rodada", "2", "--anterior", str(tmp / "nao-existe.md")], env6)
        code_c, _ = consenso(base6 + ["--rodada", "4", "--anterior", str(manual)], env6)
        check(code_a == 1 and code_b == 1 and code_c == 1 and not prompts(log6) and not rodadas(r6),
              "6. rodada 2 sem --anterior, --anterior inexistente e rodada 4 sem --pendente: exit 1 sem chamar agente",
              f"exits {code_a} {code_b} {code_c}; prompts={len(prompts(log6))}")

        r7 = montar(tmp, "c7")
        (r7 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c7 = r7 / "docs" / "CONSENSUS.md"
        c7.write_text(ler(c7) + entrada_de_debate("2026-09-02", "Entrada existente TOKEN-EXISTENTE-080"), encoding="utf-8")
        code, out = consenso(["debate", "--projeto", str(r7), "--pergunta", str(r7 / "pergunta.md"),
                              "--agente", "olha", "ag-olha", "--agente", "beta1", "ag-beta1"], ambiente(tmp))
        runs7 = rodadas(r7)
        saida7 = ler(runs7[0] / "olha" / "stdout.txt") if runs7 and (runs7[0] / "olha" / "stdout.txt").is_file() else "(sem bruto)"
        check(code == 0 and "VEJO-EXISTENTE" not in saida7, "7. rodada 1 continua retendo os registros de CONSENSUS.md na copia", f"exit {code} {saida7.strip()[:60]}")

    ok, det = bateria_minimo(48)
    check(ok, "8. bateria test_consenso.py com pelo menos 48 verificacoes", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "9. versao 2.11.0 ou acima, coerente", det)
    ok, det = verify_ok()
    check(ok, "10. verify_repository.py exit 0", det)
    return resumo("T-080")


if __name__ == "__main__":
    sys.exit(main())
