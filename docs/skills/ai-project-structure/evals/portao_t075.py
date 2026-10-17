#!/usr/bin/env python3
"""Portao da T-075: primitivo da automacao do consenso (`scripts/consenso.py debate`).

1. Rodada com `alfa`, `beta` e `falho` sai 0; 2. um run dir em docs/consensus/ com manifesto
   de debate, rodada 1, concluida, tres participantes; 3. `alfa` com bruto, hashes e comando
   batendo; 4. `beta` espera o bruto de `alfa` no sidecar real e nao o enxerga na propria copia
   (ISOLADO, nunca VAZOU, sidecar invisivel), copias distintas e fora do projeto; 5. `falho`
   registrado como falha com stderr; 6. `alfa` nao ve a entrada existente de CONSENSUS.md e ve a
   nota de retencao; 7. nada fora de docs/consensus/ e docs/CONSENSUS.md muda, rascunho do
   agente nao chega ao projeto; 8. prompt com a pergunta na integra, o id, a copia e a regra
   de somente-leitura; 9. todos falham: exit 2, sem-posicao, bruto fica, CONSENSUS.md intacto;
   10. sem --agente, pergunta ausente, debate com um agente, sidecar ignorado no git: exit 1
   sem chamar agente; 11. versao 2.11.0 coerente; 12. bateria test_consenso.py e verificador.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (agente, ambiente, arvore, bateria_minimo, campo, check, consenso,  # noqa: E402
                                 entrada_de_debate, ler, manifesto, montar, norm, participante, prompts,
                                 resumo, rodadas, sha256, verify_ok, versao_coerente)

PERGUNTA = "Pergunta de bancada do portao T-075.\n\nTOKEN-PERGUNTA-075: qual e a resposta certa, e por que?\n"

AG_ALFA = r'''
echo "POSICAO-ALFA TOKEN-ALFA-075"
if grep -q "TOKEN-EXISTENTE-075" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-EXISTENTE; fi
if grep -qiE "retid|omitid|removid" docs/CONSENSUS.md 2>/dev/null; then echo NOTA-RETIDA; fi
echo rascunho > rascunho.txt
'''
AG_BETA = r'''
for i in $(seq 1 60); do
  if ls "$PROJETO_REAL"/docs/consensus/*/alfa/stdout.txt >/dev/null 2>&1; then break; fi
  sleep 0.5
done
if ls "$PROJETO_REAL"/docs/consensus/*/alfa/stdout.txt >/dev/null 2>&1; then echo VI-BRUTO-DE-ALFA; else echo TIMEOUT-ESPERANDO-ALFA; fi
if grep -rq "TOKEN-ALFA-075" . 2>/dev/null; then echo VAZOU; else echo ISOLADO; fi
if [ -e docs/consensus ]; then echo SIDECAR-VISIVEL; fi
echo "POSICAO-BETA TOKEN-BETA-075"
'''
AG_FALHO = r'''
echo "cota esgotada" >&2
exit 4
'''

RE_SOMENTE_LEITURA = re.compile(r"nao edite|somente[- ]leitura")


def main():
    from portao_consenso_lib import autoteste
    autoteste(RE_SOMENTE_LEITURA, norm("Esta e uma copia somente-leitura do projeto: leia o que precisar."))
    autoteste(RE_SOMENTE_LEITURA, norm("Nao edite nada fora da sua resposta."), contra=norm("Pode editar a vontade."))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-alfa", AG_ALFA), ("ag-beta", AG_BETA), ("ag-falho", AG_FALHO), ("ag-falho2", AG_FALHO)):
            agente(tmp, nome, corpo)

        # Caso principal: tres agentes, um deles falhando.
        r = montar(tmp, "c1")
        c = r / "docs" / "CONSENSUS.md"
        c.write_text(ler(c) + entrada_de_debate("2026-09-02", "Entrada existente TOKEN-EXISTENTE-075"), encoding="utf-8")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes_arvore = arvore(r)
        log = tmp / "prompts-c1.txt"
        env = ambiente(tmp, PROJETO_REAL=r, LOG_PROMPT=log)
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta",
                              "--agente", "falho", "ag-falho", "--titulo", "Portao T-075"], env)
        check(code == 0, "1. rodada com alfa, beta e falho sai 0", f"exit {code}; {out.strip()[-200:]}")

        runs = rodadas(r)
        m = manifesto(runs[0]) if len(runs) == 1 else {}
        ids = sorted(str(p.get("id")) for p in m.get("participantes", []) if isinstance(p, dict))
        check(len(runs) == 1 and m.get("modo") == "debate" and m.get("rodada") == 1
              and m.get("status") == "concluida" and ids == ["alfa", "beta", "falho"],
              "2. um run dir em docs/consensus/ com manifesto de debate, rodada 1, concluida, tres participantes",
              f"runs={[p.name for p in runs]} modo={m.get('modo')} rodada={m.get('rodada')} status={m.get('status')} ids={ids}")
        run = runs[0] if runs else r
        pa, pb, pf = participante(m, "alfa"), participante(m, "beta"), participante(m, "falho")
        stdout_alfa, prompt_alfa = run / "alfa" / "stdout.txt", run / "alfa" / "prompt.txt"
        stdout_beta, stderr_falho = run / "beta" / "stdout.txt", run / "falho" / "stderr.txt"

        ok3 = (pa.get("resultado") == "posicao" and stdout_alfa.is_file() and prompt_alfa.is_file()
               and "TOKEN-ALFA-075" in ler(stdout_alfa)
               and pa.get("sha256_stdout") == sha256(stdout_alfa) and pa.get("sha256_prompt") == sha256(prompt_alfa)
               and pa.get("comando") == ["ag-alfa"] and pa.get("exit") == 0)
        check(ok3, "3. alfa: resultado=posicao, bruto com o token, sha256 de saida e de prompt batendo, comando registrado",
              f"resultado={pa.get('resultado')} exit={pa.get('exit')} comando={pa.get('comando')}")

        saida_beta = ler(stdout_beta) if stdout_beta.is_file() else ""
        dirs = (str(pa.get("diretorio") or ""), str(pb.get("diretorio") or ""))
        ok4 = ("VI-BRUTO-DE-ALFA" in saida_beta and "ISOLADO" in saida_beta and "VAZOU" not in saida_beta
               and "SIDECAR-VISIVEL" not in saida_beta and all(dirs) and dirs[0] != dirs[1]
               and not any(d.startswith(str(r)) for d in dirs))
        check(ok4, "4. beta viu o bruto de alfa no sidecar real e nao o encontra na propria copia; copias distintas e fora do projeto",
              f"beta={saida_beta.strip().replace(chr(10), ' | ')[:160]} dirs={dirs}")

        check(pf.get("resultado") == "falha" and pf.get("exit") == 4 and stderr_falho.is_file() and "cota" in ler(stderr_falho),
              "5. falho: resultado=falha, exit 4, stderr guardado", f"resultado={pf.get('resultado')} exit={pf.get('exit')}")

        saida_alfa = ler(stdout_alfa) if stdout_alfa.is_file() else ""
        check("VEJO-EXISTENTE" not in saida_alfa and "NOTA-RETIDA" in saida_alfa,
              "6. na rodada 1 a copia nao traz as entradas de CONSENSUS.md e traz a nota de retencao",
              saida_alfa.strip().replace("\n", " | ")[:160])

        check(arvore(r) == antes_arvore and not (r / "rascunho.txt").exists(),
              "7. nada fora de docs/consensus/ e docs/CONSENSUS.md mudou, e o rascunho do agente nao chegou ao projeto")

        prompt = ler(prompt_alfa) if prompt_alfa.is_file() else ""
        check(PERGUNTA in prompt and "alfa" in prompt and dirs[0] and dirs[0] in prompt and RE_SOMENTE_LEITURA.search(norm(prompt)),
              "8. prompt.txt traz a pergunta na integra, o id, o caminho da copia e a regra de somente-leitura",
              f"{len(prompt)} bytes")

        # Todos falham: nenhuma posicao.
        r2 = montar(tmp, "c2")
        (r2 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes = (r2 / "docs" / "CONSENSUS.md").read_bytes()
        code, out = consenso(["debate", "--projeto", str(r2), "--pergunta", str(r2 / "pergunta.md"),
                              "--agente", "falho", "ag-falho", "--agente", "falho2", "ag-falho2"], ambiente(tmp))
        runs2 = rodadas(r2)
        m2 = manifesto(runs2[0]) if len(runs2) == 1 else {}
        check(code == 2 and m2.get("status") == "sem-posicao" and len(runs2) == 1
              and (runs2[0] / "falho" / "stderr.txt").is_file() and (runs2[0] / "falho2" / "stderr.txt").is_file()
              and (r2 / "docs" / "CONSENSUS.md").read_bytes() == antes,
              "9. todos falharam: exit 2, status sem-posicao, bruto das falhas fica, CONSENSUS.md byte a byte",
              f"exit {code} status={m2.get('status')}")

        # Elegibilidade: nada disso chama agente.
        r3 = montar(tmp, "c3")
        (r3 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        log3 = tmp / "prompts-c3.txt"
        env3 = ambiente(tmp, LOG_PROMPT=log3)
        code_a, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md")], env3)
        code_b, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "nao-existe.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta"], env3)
        code_c, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa"], env3)
        check(code_a == 1 and code_b == 1 and code_c == 1 and not prompts(log3) and not rodadas(r3),
              "10a. sem --agente, pergunta ausente ou debate com um agente so: exit 1, agente nao chamado, sem run dir",
              f"exits {code_a} {code_b} {code_c}; prompts={len(prompts(log3))}")

        r4 = montar(tmp, "c4")
        (r4 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=r4, check=False, capture_output=True)
        (r4 / ".gitignore").write_text("docs/consensus/\n", encoding="utf-8")
        log4 = tmp / "prompts-c4.txt"
        code, out = consenso(["debate", "--projeto", str(r4), "--pergunta", str(r4 / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta"], ambiente(tmp, LOG_PROMPT=log4))
        check(code == 1 and not prompts(log4) and not rodadas(r4) and "ignor" in norm(out),
              "10b. projeto git com docs/consensus/ no .gitignore: exit 1 antes de chamar agente, explicando", f"exit {code}")

    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "11. versao 2.11.0 ou acima, coerente em SKILL.md, prosa, marcadores e CHANGELOG", det)
    ok, det = bateria_minimo(12)
    check(ok, "12a. bateria test_consenso.py passa com pelo menos 12 verificacoes", det)
    ok, det = verify_ok()
    check(ok, "12b. verify_repository.py exit 0", det)
    return resumo("T-075")


if __name__ == "__main__":
    sys.exit(main())
