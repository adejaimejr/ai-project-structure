#!/usr/bin/env python3
"""Portao da T-081: retomada por comando explicito (DEC-009, DEC-010).

1. Rodada interrompida por SIGTERM (alfa rapido, beta lento): `retomar <run-id>` sai 0, alfa
   nao e chamado de novo, beta e, minuta escrita, manifesto concluida com retomadas;
2. retomar em run concluido: exit 1 e CONSENSUS.md intacto; 3. retomar com lock presente:
   exit 5; 4. run parado por segredo com o material movido a mao para <run>/<id>/: retomar
   aceita sem nova chamada e escreve a minuta; 5. run-id inexistente: exit 1; 6. as saidas de
   interrupcao e de exit 6 citam o comando de retomada e o run-id; 7. bateria >= 56; 8. versao;
   9. verificador.
"""

import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (agente, ambiente, bateria_minimo, campo, check, consenso, consenso_popen,  # noqa: E402
                                 entradas, ler, manifesto, montar, participante, resumo, rodadas, secao,
                                 verify_ok, versao_coerente)

PERGUNTA = "Pergunta do portao T-081.\n\nTOKEN-PERGUNTA-081: retomamos?\n"
CONTA = 'echo x >> "$CONTADOR_DIR/$AGENTE_ID"\n'
AG_ALFA = "AGENTE_ID=alfa\n" + CONTA + "echo 'POSICAO-ALFA TOKEN-ALFA-081'\n"
AG_BETA = "AGENTE_ID=beta\n" + CONTA + "sleep 8\necho 'POSICAO-BETA TOKEN-BETA-081'\n"
AG_VAZA = "AGENTE_ID=vaza\n" + CONTA + "echo 'posicao com chave " + "AKIA" + "ABCDEFGHIJKLMNOP" + " TOKEN-VAZA-081'\n"
AG_LIMPO = "AGENTE_ID=limpo\n" + CONTA + "echo 'posicao limpa TOKEN-LIMPO-081'\n"


def chamadas(contadores, pid):
    p = Path(contadores) / pid
    return len(ler(p).split()) if p.is_file() else 0


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-alfa", AG_ALFA), ("ag-beta", AG_BETA), ("ag-vaza", AG_VAZA), ("ag-limpo", AG_LIMPO)):
            agente(tmp, nome, corpo)

        # 1, 2, 3, 6: interrupcao e retomada.
        r = montar(tmp, "c1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        antes = ler(c)
        cont = tmp / "cont-c1"
        cont.mkdir()
        env = ambiente(tmp, CONTADOR_DIR=cont)
        p = consenso_popen(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                            "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta", "--titulo", "Portao T-081"], env)
        saida_int = ""
        if p is not None:
            for _ in range(50):
                if any((run / "alfa" / "stdout.txt").is_file() for run in rodadas(r)):
                    break
                time.sleep(0.1)
            time.sleep(0.5)
            p.terminate()
            try:
                saida_int, _ = p.communicate(timeout=20)
            except Exception:
                p.kill()
        runs = rodadas(r)
        run_id = runs[0].name if runs else "(sem run)"
        check(p is not None and runs and manifesto(runs[0]).get("status") == "interrompida" and ler(c) == antes,
              "1a. rodada interrompida: manifesto interrompida e CONSENSUS.md intacto", f"status={manifesto(runs[0]).get('status') if runs else None}")
        code, out = consenso(["retomar", "--projeto", str(r), run_id], env, timeout=120)
        depois = ler(c)
        novo = depois[len(antes):] if depois.startswith(antes) else ""
        m = manifesto(runs[0]) if runs else {}
        check(code == 0 and chamadas(cont, "alfa") == 1 and chamadas(cont, "beta") == 2 and entradas(novo)
              and campo(novo, "Participantes") == "alfa, beta" and m.get("status") == "concluida" and len(m.get("retomadas", [])) >= 1
              and "TOKEN-BETA-081" in (secao(novo, "Posicao De beta") or ""),
              "1b. retomar chama so quem faltava, escreve a minuta e sela o manifesto com a retomada registrada",
              f"exit {code} alfa={chamadas(cont, 'alfa')} beta={chamadas(cont, 'beta')} status={m.get('status')} retomadas={len(m.get('retomadas', []))}")
        check("retomar" in saida_int and run_id in saida_int, "6a. a saida da interrupcao cita o comando de retomada e o run-id",
              saida_int.strip().replace("\n", " | ")[-160:])

        antes2 = ler(c)
        code2, out2 = consenso(["retomar", "--projeto", str(r), run_id], env)
        check(code2 == 1 and ler(c) == antes2, "2. retomar em run concluido: exit 1 e CONSENSUS.md intacto", f"exit {code2}")

        (r / ".consenso-lock").mkdir()
        code3, out3 = consenso(["retomar", "--projeto", str(r), run_id], env)
        (r / ".consenso-lock").rmdir()
        check(code3 == 5, "3. retomar com lock presente: exit 5", f"exit {code3}")

        code5, _ = consenso(["retomar", "--projeto", str(r), "2000-01-01-000000-debate"], env)
        check(code5 == 1, "5. run-id inexistente: exit 1", f"exit {code5}")

        # 4 e 6b: segredo retido, material movido a mao.
        r4 = montar(tmp, "c4")
        (r4 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c4 = r4 / "docs" / "CONSENSUS.md"
        antes4 = ler(c4)
        cont4 = tmp / "cont-c4"
        cont4.mkdir()
        env4 = ambiente(tmp, CONTADOR_DIR=cont4)
        code6, out6 = consenso(["debate", "--projeto", str(r4), "--pergunta", str(r4 / "pergunta.md"),
                                "--agente", "limpo", "ag-limpo", "--agente", "vaza", "ag-vaza", "--titulo", "Segredo T-081"], env4)
        runs4 = rodadas(r4)
        run4 = runs4[0] if runs4 else None
        pv = participante(manifesto(run4), "vaza") if run4 else {}
        retido = Path(str(pv.get("retido_em") or ""))
        check(code6 == 6 and run4 is not None and "retomar" in out6 and run4.name in out6,
              "6b. a saida de exit 6 cita o comando de retomada e o run-id", f"exit {code6}")
        movido = False
        if run4 is not None and retido.is_dir():
            shutil.copytree(retido, run4 / "vaza", dirs_exist_ok=True)
            movido = (run4 / "vaza" / "stdout.txt").is_file()
        code7, out7 = consenso(["retomar", "--projeto", str(r4), run4.name if run4 else "x"], env4, timeout=120)
        novo4 = ler(c4)[len(antes4):]
        pv2 = participante(manifesto(run4), "vaza") if run4 else {}
        check(movido and code7 == 0 and chamadas(cont4, "vaza") == 1 and chamadas(cont4, "limpo") == 1
              and "TOKEN-VAZA-081" in (secao(novo4, "Posicao De vaza") or "") and pv2.get("resultado") == "posicao",
              "4. material retido movido a mao para <run>/vaza/: retomar aceita sem nova chamada, escreve a minuta e marca posicao",
              f"movido={movido} exit {code7} vaza={chamadas(cont4, 'vaza')} limpo={chamadas(cont4, 'limpo')} resultado={pv2.get('resultado')}")

    ok, det = bateria_minimo(56)
    check(ok, "7. bateria test_consenso.py com pelo menos 56 verificacoes", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "8. versao 2.11.0 ou acima, coerente", det)
    ok, det = verify_ok()
    check(ok, "9. verify_repository.py exit 0", det)
    return resumo("T-081")


if __name__ == "__main__":
    sys.exit(main())
