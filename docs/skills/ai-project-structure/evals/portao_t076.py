#!/usr/bin/env python3
"""Portao da T-076: lock e minuta de debate atomica com julgamento em branco.

1. Rodada com alfa e beta sai 0 e CONSENSUS.md ganha exatamente uma entrada no fim, texto
   anterior byte a byte; 2. campos derivados da execucao (Status, Proximo passo com o dono,
   Metodo, Exposicao, Rodada, Origem, Manifesto, Participantes, Falhas); 3. secoes: Contexto,
   Pergunta Ou Decisao, Posicao De <id> com os tokens em citacao, quatro secoes de julgamento
   com (A preencher.); 4. injecao neutralizada: heading, Status, cerca e U+2014 vindos do agente
   nao alcancam o validador, o travessao e substituido e contado, o bruto fica intacto;
   5. agente falho vira `### Falha De <id>` e entra em Falhas; 6. lock: segunda execucao
   simultanea sai 5 citando o lock, nada sobra, a proxima roda; 7. SIGTERM no meio deixa
   CONSENSUS.md byte a byte, manifesto interrompida, bruto pago presente, sem temporario e sem
   lock; 8. hashes da minuta no manifesto; 9. verify_repository.py ignora travessao em bruto sob
   docs/consensus/; 10. bateria >= 24; 11. versao coerente; 12. verificador.
"""

import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (ROOT, agente, ambiente, bateria_minimo, campo, check, citado, consenso,  # noqa: E402
                                 consenso_popen, entradas, ler, manifesto, montar, norm, participante,
                                 resumo, rodadas, secao, sha256, validar, verify_ok, versao_coerente)

PERGUNTA = "Pergunta do portao T-076.\n\nTOKEN-PERGUNTA-076: o que fazer?\n"
TRAVESSAO = "\u2014"  # escapado de proposito: literal, o verificador acusaria este arquivo

AG_ALFA = "\n".join([
    "echo '## 2026-01-01 - INJETADO'",
    "echo '**Status:** resolvido'",
    "echo '```'",
    "echo 'texto com travessao " + TRAVESSAO + " aqui'",
    "echo 'POSICAO-ALFA TOKEN-ALFA-076'",
    "",
])
AG_BETA = "echo 'POSICAO-BETA TOKEN-BETA-076'\n"
AG_FALHO = "echo 'cota esgotada' >&2\nexit 4\n"
AG_LENTO = "sleep 4\necho 'POSICAO-LENTA TOKEN-LENTO-076'\n"
AG_MUITO_LENTO = "sleep 8\necho 'POSICAO-MUITO-LENTA'\n"
AG_RAPIDO = "echo 'POSICAO-RAPIDA TOKEN-RAPIDO-076'\n"


def preparar(tmp, nome):
    r = montar(tmp, nome)
    (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
    return r


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-alfa", AG_ALFA), ("ag-beta", AG_BETA), ("ag-falho", AG_FALHO),
                            ("ag-lento", AG_LENTO), ("ag-muito-lento", AG_MUITO_LENTO), ("ag-rapido", AG_RAPIDO)):
            agente(tmp, nome, corpo)
        env = ambiente(tmp)

        # 1 a 4 e 8: minuta de debate.
        r = preparar(tmp, "c1")
        c = r / "docs" / "CONSENSUS.md"
        antes = ler(c)
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta",
                              "--titulo", "Portao T-076", "--dono", "fulano"], env)
        depois = ler(c)
        novo = depois[len(antes):] if depois.startswith(antes) else ""
        hoje = time.strftime("%Y-%m-%d")
        check(code == 0 and depois.startswith(antes) and entradas(novo) == [f"{hoje} - Portao T-076"]
              and len(entradas(depois)) == len(entradas(antes)) + 1,
              "1. rodada sai 0 e CONSENSUS.md ganha exatamente uma entrada no fim, texto anterior byte a byte",
              f"exit {code}; entradas novas={entradas(novo)}")

        runs = rodadas(r)
        run = runs[0] if runs else r
        m = manifesto(run)
        manif = campo(novo, "Manifesto") or ""
        ok2 = (campo(novo, "Status") == "aberto" and "fulano" in (campo(novo, "Proximo passo") or "")
               and campo(novo, "Metodo") == "pareceres-independentes"
               and campo(novo, "Exposicao previa a outras posicoes") == "nao" and campo(novo, "Rodada") == "1 de 1"
               and campo(novo, "Origem") == "automacao" and manif and (r / manif).is_file()
               and (r / manif).resolve() == (run / "manifesto.json").resolve()
               and campo(novo, "Participantes") == "alfa, beta" and campo(novo, "Falhas") == "nenhuma")
        check(ok2, "2. campos: Status aberto, Proximo passo com o dono, Metodo, Exposicao nao, Rodada 1 de 1, Origem, Manifesto existente, Participantes, Falhas nenhuma",
              f"status={campo(novo, 'Status')} metodo={campo(novo, 'Metodo')} exp={campo(novo, 'Exposicao previa a outras posicoes')} rodada={campo(novo, 'Rodada')} origem={campo(novo, 'Origem')} manifesto={manif} part={campo(novo, 'Participantes')} falhas={campo(novo, 'Falhas')}")

        julgamento = ["Pontos De Acordo", "Riscos E Tradeoffs", "Consenso Final", "Decisao Para Registrar Em DECISIONS.md"]
        ok3 = (secao(novo, "Contexto") is not None and citado(secao(novo, "Pergunta Ou Decisao"), "TOKEN-PERGUNTA-076")
               and citado(secao(novo, "Posicao De alfa"), "TOKEN-ALFA-076") and citado(secao(novo, "Posicao De beta"), "TOKEN-BETA-076")
               and all("(A preencher.)" in (secao(novo, s) or "") for s in julgamento))
        check(ok3, "3. secoes Contexto, Pergunta Ou Decisao e Posicao De <id> em citacao, e as quatro de julgamento com (A preencher.)",
              "; ".join(f"{s}={'ok' if '(A preencher.)' in (secao(novo, s) or '') else 'falta'}" for s in julgamento))

        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        pa = participante(m, "alfa")
        bruto_alfa = run / "alfa" / "stdout.txt"
        ok4 = (code_v == 0 and not linhas and "> ## 2026-01-01 - INJETADO" in novo and TRAVESSAO not in depois
               and pa.get("travessoes_substituidos") == 1 and bruto_alfa.is_file() and TRAVESSAO in ler(bruto_alfa))
        check(ok4, "4. injecao neutralizada: --strict limpo, heading injetado em citacao, travessao substituido e contado, bruto intacto",
              f"strict exit {code_v} {'; '.join(linhas)[:120]} substituidos={pa.get('travessoes_substituidos')}")

        minuta = m.get("minuta") or {}
        check(minuta.get("sha256_antes") == sha256_texto(antes) and minuta.get("sha256_depois") == sha256(c)
              and m.get("status") == "concluida",
              "8. manifesto com minuta.sha256_antes e sha256_depois batendo com o arquivo, e status concluida depois da minuta",
              f"antes={str(minuta.get('sha256_antes'))[:12]} depois={str(minuta.get('sha256_depois'))[:12]} status={m.get('status')}")

        # 5: agente falho.
        r5 = preparar(tmp, "c5")
        c5 = r5 / "docs" / "CONSENSUS.md"
        antes5 = ler(c5)
        code, out = consenso(["debate", "--projeto", str(r5), "--pergunta", str(r5 / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "falho", "ag-falho"], env)
        novo5 = ler(c5)[len(antes5):]
        falha = secao(novo5, "Falha De falho") or ""
        check(code == 0 and campo(novo5, "Participantes") == "alfa, falho" and campo(novo5, "Falhas") == "falho"
              and "4" in falha and "docs/consensus/" in falha and secao(novo5, "Posicao De falho") is None,
              "5. agente falho: secao Falha De falho com exit e caminho do bruto, Participantes com os dois, Falhas com o id",
              f"exit {code} part={campo(novo5, 'Participantes')} falhas={campo(novo5, 'Falhas')}")

        # 6: lock.
        r6 = preparar(tmp, "c6")
        args6 = ["debate", "--projeto", str(r6), "--pergunta", str(r6 / "pergunta.md"), "--agente", "alfa", "ag-lento", "--agente", "beta", "ag-beta"]
        a = consenso_popen(args6, env)
        time.sleep(1.0)
        code_b, out_b = consenso(args6, env, timeout=3)
        if a is not None:
            sa, _ = a.communicate(timeout=90)
        sobras = [p.name for p in r6.iterdir() if "lock" in p.name.lower()]
        check(a is not None and code_b == 5 and "lock" in norm(out_b) and a.returncode == 0 and not sobras,
              "6a. segunda execucao simultanea sai 5 citando o lock; a primeira segue e fecha; nenhum lock sobra",
              f"segunda exit {code_b}; primeira exit {getattr(a, 'returncode', None)}; sobras={sobras}")
        code_c, _ = consenso(["debate", "--projeto", str(r6), "--pergunta", str(r6 / "pergunta.md"),
                              "--agente", "alfa", "ag-rapido", "--agente", "beta", "ag-beta", "--titulo", "Depois do lock"], env)
        check(code_c == 0, "6b. proxima execucao roda normalmente", f"exit {code_c}")

        # 7: interrupcao.
        r7 = preparar(tmp, "c7")
        c7 = r7 / "docs" / "CONSENSUS.md"
        antes7 = c7.read_bytes()
        p = consenso_popen(["debate", "--projeto", str(r7), "--pergunta", str(r7 / "pergunta.md"),
                            "--agente", "rapido", "ag-rapido", "--agente", "lento", "ag-muito-lento"], env)
        saida7 = ""
        if p is not None:
            for _ in range(50):
                if any((run / "rapido" / "stdout.txt").is_file() for run in rodadas(r7)):
                    break
                time.sleep(0.1)
            time.sleep(0.5)
            p.terminate()
            try:
                saida7, _ = p.communicate(timeout=20)
            except Exception:
                p.kill()
        runs7 = rodadas(r7)
        m7 = manifesto(runs7[0]) if runs7 else {}
        temporarios = [x.name for x in (r7 / "docs").glob("CONSENSUS.md.*")]
        check(p is not None and c7.read_bytes() == antes7 and len(runs7) == 1 and m7.get("status") == "interrompida"
              and (runs7[0] / "rapido" / "stdout.txt").is_file() and not temporarios and not (r7 / ".consenso-lock").exists(),
              "7. SIGTERM no meio: CONSENSUS.md byte a byte, manifesto interrompida, bruto do agente rapido presente, sem temporario, sem lock",
              f"status={m7.get('status')} runs={len(runs7)} temporarios={temporarios} lock={(r7 / '.consenso-lock').exists()}")

    # 9: bruto com travessao sob docs/consensus/ nao derruba o verificador deste repositorio.
    base = ROOT / "docs" / "consensus"
    existia = base.exists()
    tmpdir = base / "portao-t076-temporario"
    try:
        tmpdir.mkdir(parents=True, exist_ok=False)
        (tmpdir / "stdout.txt").write_text("bruto com travessao " + TRAVESSAO + "\n", encoding="utf-8")
        ok, det = verify_ok()
        check(ok, "9. verify_repository.py ignora travessao em bruto sob docs/consensus/", det)
    except FileExistsError:
        check(False, "9. verify_repository.py ignora travessao em bruto sob docs/consensus/", f"{tmpdir} ja existia")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        if not existia and base.exists() and not any(base.iterdir()):
            base.rmdir()

    ok, det = bateria_minimo(24)
    check(ok, "10. bateria test_consenso.py com pelo menos 24 verificacoes", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "11. versao 2.11.0 ou acima, coerente", det)
    ok, det = verify_ok()
    check(ok, "12. verify_repository.py exit 0", det)
    return resumo("T-076")


def sha256_texto(texto):
    import hashlib
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    sys.exit(main())
