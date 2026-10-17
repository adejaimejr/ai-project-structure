#!/usr/bin/env python3
"""Testa o primitivo de consenso em projetos descartaveis, com agente falso.

Uso:
    python3 docs/skills/ai-project-structure/evals/test_consenso.py [--verbose]

Cobre os criterios de comportamento da spec 0006 que cabem no primitivo
(`scripts/consenso.py debate`): isolamento verificavel sem confiar no relato,
falha registrada sem derrubar a rodada, nenhum artefato sem execucao,
sidecar in-repo fora da arvore de execucao, recusa de elegibilidade, lock
exclusivo, minuta atomica com julgamento em branco, interrupcao sem tocar
em CONSENSUS.md e varredura de segredo que para a rodada sem redigir.

Nenhuma chamada de modelo: o agente e um shell script que registra o prompt
recebido. Roda em segundos e nao custa nada, entao pode rodar sempre.

Nao e distribuido pelo `install.sh`: vive em `evals/`, so na fonte canonica.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 se tudo passar.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (  # noqa: E402
    agente, ambiente, arvore, campo, consenso, consenso_popen, citado,
    entrada_de_debate, ler, manifesto, montar, norm, participante, prompts,
    rodadas, secao, sha256, validar,
)

PERGUNTA = "Pergunta da bateria test_consenso.\n\nTOKEN-BATERIA-075: o que vale?\n"
TRAVESSAO = "\u2014"

AG_OK = r'''
echo "POSICAO-OK TOKEN-OK-075"
if grep -q "TOKEN-EXISTENTE-075" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-EXISTENTE; fi
if grep -qiE "retid|omitid|removid" docs/CONSENSUS.md 2>/dev/null; then echo NOTA-RETIDA; fi
echo rascunho > rascunho.txt
'''
AG_PAR = r'''
for i in $(seq 1 60); do
  if ls "$PROJETO_REAL"/docs/consensus/*/ok/stdout.txt >/dev/null 2>&1; then break; fi
  sleep 0.5
done
if ls "$PROJETO_REAL"/docs/consensus/*/ok/stdout.txt >/dev/null 2>&1; then echo VI-BRUTO-DO-PAR; else echo TIMEOUT-ESPERANDO-PAR; fi
if grep -rq "TOKEN-OK-075" . 2>/dev/null; then echo VAZOU; else echo ISOLADO; fi
if [ -e docs/consensus ]; then echo SIDECAR-VISIVEL; fi
echo "POSICAO-PAR TOKEN-PAR-075"
'''
AG_FALHO = r'''
echo "cota esgotada" >&2
exit 4
'''
AG_INJETA = "\n".join([
    "echo '## 2026-01-01 - INJETADO'",
    "echo '**Status:** resolvido'",
    "echo '```'",
    "echo 'texto com travessao " + TRAVESSAO + " aqui'",
    "echo 'POSICAO-ALFA TOKEN-ALFA-076'",
    "",
])
AG_BETA = "echo 'POSICAO-BETA TOKEN-BETA-076'\n"
AG_LENTO = "sleep 4\necho 'POSICAO-LENTA TOKEN-LENTO-076'\n"
AG_MUITO_LENTO = "sleep 8\necho 'POSICAO-MUITO-LENTA'\n"
AG_RAPIDO = "echo 'POSICAO-RAPIDA TOKEN-RAPIDO-076'\n"

CHAVE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"
PEM = "-----BEGIN RSA PRIVATE KEY-----"
GHP = "ghp_" + "Ab1" * 12
APIKEY = "Q7pL2mN9xV4cB8zK1wE5rT0y"
URL_SEGREDO = "https://joao:senha123@exemplo.com/repo"
SK = "sk-" + "Zq8" * 12

AG_LIMPO_SEGREDO = (
    "echo 'Posicao limpa: a chave de API e o token nao aparecem aqui. TOKEN-LIMPO-077'\n"
)
AG_LIMPO2_SEGREDO = (
    "echo 'Outra posicao limpa, falando de senha e de segredo sem valor nenhum. TOKEN-LIMPO2-077'\n"
)
AG_AWS = "echo 'achei no repositorio: %s'\n" % CHAVE_AWS
AG_PEM = "echo '%s'\necho 'MIIEowIBAAKCAQEA'\n" % PEM
AG_GHP = "echo 'token: %s'\n" % GHP
AG_APIKEY = "echo 'api_key = \"%s\"'\n" % APIKEY
AG_URL = "echo 'veja %s'\n" % URL_SEGREDO
AG_SK = "echo 'chave %s'\n" % SK
AG_LIMPO3_SEGREDO = "echo 'A task-force do projeto usa abordagem risk-based no desk-top. TOKEN-LIMPO3-077'\n"


class Resultado:
    def __init__(self, verbose=False):
        self.falhas = 0
        self.total = 0
        self.verbose = verbose

    def check(self, ok, titulo, detalhe=""):
        self.total += 1
        if not ok:
            self.falhas += 1
        if not ok or self.verbose:
            sufixo = ": %s" % detalhe if detalhe else ""
            print("[%s] %s%s" % ("OK  " if ok else "FALHA", titulo, sufixo))


def testar_primitivo(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-ok", AG_OK), ("ag-par", AG_PAR), ("ag-falho", AG_FALHO),
                            ("ag-falho2", AG_FALHO)):
            agente(tmp, nome, corpo)

        r = montar(tmp, "c1")
        c = r / "docs" / "CONSENSUS.md"
        c.write_text(ler(c) + entrada_de_debate("2026-09-02", "Entrada existente TOKEN-EXISTENTE-075"),
                     encoding="utf-8")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes_arvore = arvore(r)
        antes_consenso = ler(c)
        log = tmp / "prompts-c1.txt"
        env = ambiente(tmp, PROJETO_REAL=r, LOG_PROMPT=log)
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "ok", "ag-ok", "--agente", "par", "ag-par",
                              "--agente", "falho", "ag-falho", "--titulo", "Bateria T-075"], env)
        res.check(code == 0, "rodada com ok, par e falho sai 0", "exit %s; %s" % (code, out.strip()[-120:]))

        runs = rodadas(r)
        m = manifesto(runs[0]) if len(runs) == 1 else {}
        ids = sorted(str(p.get("id")) for p in m.get("participantes", []) if isinstance(p, dict))
        res.check(len(runs) == 1 and m.get("modo") == "debate" and m.get("rodada") == 1
                  and m.get("status") == "concluida" and ids == ["falho", "ok", "par"],
                  "um run dir com manifesto de debate, rodada 1, concluida, tres participantes")

        run = runs[0] if runs else r
        po, pp, pf = participante(m, "ok"), participante(m, "par"), participante(m, "falho")
        stdout_ok = run / "ok" / "stdout.txt"
        prompt_ok = run / "ok" / "prompt.txt"
        stdout_par = run / "par" / "stdout.txt"
        stderr_falho = run / "falho" / "stderr.txt"

        res.check(po.get("resultado") == "posicao" and stdout_ok.is_file() and prompt_ok.is_file()
                  and "TOKEN-OK-075" in ler(stdout_ok)
                  and po.get("sha256_stdout") == sha256(stdout_ok)
                  and po.get("sha256_prompt") == sha256(prompt_ok)
                  and po.get("comando") == ["ag-ok"] and po.get("exit") == 0,
                  "ok: resultado=posicao, bruto com token, hashes e comando batendo")

        saida_par = ler(stdout_par) if stdout_par.is_file() else ""
        dirs = (str(po.get("diretorio") or ""), str(pp.get("diretorio") or ""))
        res.check("VI-BRUTO-DO-PAR" in saida_par and "ISOLADO" in saida_par and "VAZOU" not in saida_par
                  and "SIDECAR-VISIVEL" not in saida_par and all(dirs) and dirs[0] != dirs[1]
                  and not any(d.startswith(str(r)) for d in dirs),
                  "isolamento verificavel: par ve o bruto no sidecar real e nao na copia")

        res.check(pf.get("resultado") == "falha" and pf.get("exit") == 4
                  and stderr_falho.is_file() and "cota" in ler(stderr_falho),
                  "falha registrada sem derrubar a rodada")

        saida_ok = ler(stdout_ok) if stdout_ok.is_file() else ""
        res.check("VEJO-EXISTENTE" not in saida_ok and "NOTA-RETIDA" in saida_ok,
                  "rodada 1: copia nao traz entradas de CONSENSUS.md e traz nota de retencao")

        res.check(arvore(r) == antes_arvore and not (r / "rascunho.txt").exists(),
                  "nada fora de docs/consensus/ e docs/CONSENSUS.md mudou; rascunho nao vaza")

        depois = ler(c)
        novo = depois[len(antes_consenso):] if depois.startswith(antes_consenso) else ""
        res.check(depois.startswith(antes_consenso) and "TOKEN-EXISTENTE-075" in depois
                  and campo(novo, "Status") == "aberto" and campo(novo, "Origem") == "automacao"
                  and campo(novo, "Participantes") == "ok, par, falho"
                  and campo(novo, "Falhas") == "falho" and campo(novo, "Metodo") == "pareceres-independentes",
                  "CONSENSUS.md ganha uma minuta no fim; texto anterior byte a byte")
        res.check(citado(secao(novo, "Posicao De ok"), "TOKEN-OK-075")
                  and citado(secao(novo, "Posicao De par"), "TOKEN-PAR-075")
                  and secao(novo, "Posicao De falho") is None
                  and "4" in (secao(novo, "Falha De falho") or "")
                  and "docs/consensus/" in (secao(novo, "Falha De falho") or ""),
                  "posicoes em citacao; falho vira Falha De falho com exit e caminho")
        julgamento = ["Pontos De Acordo", "Riscos E Tradeoffs", "Consenso Final",
                      "Decisao Para Registrar Em DECISIONS.md"]
        res.check(all("(A preencher.)" in (secao(novo, s) or "") for s in julgamento)
                  and "usuario" in (campo(novo, "Proximo passo") or ""),
                  "julgamento em branco e dono padrao usuario")
        minuta = m.get("minuta") or {}
        res.check(minuta.get("sha256_antes") == hashlib_texto(antes_consenso)
                  and minuta.get("sha256_depois") == sha256(c)
                  and minuta.get("arquivo") == "docs/CONSENSUS.md",
                  "manifesto.minuta com hashes batendo e ponte para CONSENSUS.md")
        res.check(not (r / ".consenso-lock").exists(),
                  "rodada concluida nao deixa .consenso-lock")

        prompt = ler(prompt_ok) if prompt_ok.is_file() else ""
        res.check(PERGUNTA in prompt and "ok" in prompt and dirs[0] and dirs[0] in prompt
                  and re.search(r"nao edite|somente[- ]leitura", norm(prompt)),
                  "prompt.txt traz a pergunta na integra, o id, a copia e somente-leitura")
        res.check((run / "pergunta.txt").is_file() and sha256(run / "pergunta.txt") == sha256(r / "pergunta.md"),
                  "sidecar guarda pergunta.txt byte a byte")

        r2 = montar(tmp, "c2")
        (r2 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes = (r2 / "docs" / "CONSENSUS.md").read_bytes()
        code, out = consenso(["debate", "--projeto", str(r2), "--pergunta", str(r2 / "pergunta.md"),
                              "--agente", "falho", "ag-falho", "--agente", "falho2", "ag-falho2"],
                             ambiente(tmp))
        runs2 = rodadas(r2)
        m2 = manifesto(runs2[0]) if len(runs2) == 1 else {}
        res.check(code == 2 and m2.get("status") == "sem-posicao" and len(runs2) == 1
                  and (runs2[0] / "falho" / "stderr.txt").is_file()
                  and (runs2[0] / "falho2" / "stderr.txt").is_file()
                  and (r2 / "docs" / "CONSENSUS.md").read_bytes() == antes,
                  "todos falharam: exit 2, sem-posicao, bruto fica, CONSENSUS.md byte a byte")

        r3 = montar(tmp, "c3")
        (r3 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        log3 = tmp / "prompts-c3.txt"
        env3 = ambiente(tmp, LOG_PROMPT=log3)
        code_a, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md")], env3)
        code_b, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "nao-existe.md"),
                              "--agente", "ok", "ag-ok", "--agente", "par", "ag-par"], env3)
        code_c, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md"),
                              "--agente", "ok", "ag-ok"], env3)
        res.check(code_a == 1 and code_b == 1 and code_c == 1 and not prompts(log3) and not rodadas(r3),
                  "sem --agente, pergunta ausente ou um agente so: exit 1, sem chamada, sem run dir")

        r4 = montar(tmp, "c4")
        (r4 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=r4, check=False, capture_output=True)
        (r4 / ".gitignore").write_text("docs/consensus/\n", encoding="utf-8")
        log4 = tmp / "prompts-c4.txt"
        code, out = consenso(["debate", "--projeto", str(r4), "--pergunta", str(r4 / "pergunta.md"),
                              "--agente", "ok", "ag-ok", "--agente", "par", "ag-par"],
                             ambiente(tmp, LOG_PROMPT=log4))
        res.check(code == 1 and not prompts(log4) and not rodadas(r4) and "ignor" in norm(out),
                  "projeto git com docs/consensus/ no .gitignore: exit 1 antes de chamar agente")


def testar_lock_e_minuta(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-alfa", AG_INJETA), ("ag-beta", AG_BETA), ("ag-falho", AG_FALHO),
                            ("ag-lento", AG_LENTO), ("ag-muito-lento", AG_MUITO_LENTO),
                            ("ag-rapido", AG_RAPIDO)):
            agente(tmp, nome, corpo)
        env = ambiente(tmp)

        r = montar(tmp, "m1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        antes = ler(c)
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta",
                              "--titulo", "Bateria T-076", "--dono", "fulano"], env)
        depois = ler(c)
        novo = depois[len(antes):] if depois.startswith(antes) else ""
        runs = rodadas(r)
        m = manifesto(runs[0]) if runs else {}
        pa = participante(m, "alfa")
        bruto = runs[0] / "alfa" / "stdout.txt" if runs else r
        res.check(code == 0 and "fulano" in (campo(novo, "Proximo passo") or "")
                  and campo(novo, "Rodada") == "1 de 1"
                  and campo(novo, "Exposicao previa a outras posicoes") == "nao",
                  "minuta com --dono fulano, Rodada 1 de 1 e exposicao nao")
        res.check("> ## 2026-01-01 - INJETADO" in novo and TRAVESSAO not in depois
                  and pa.get("travessoes_substituidos") == 1
                  and bruto.is_file() and TRAVESSAO in ler(bruto),
                  "injecao em citacao; travessao substituido na minuta e intacto no bruto")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "minuta passa em --strict sem diagnostico",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))

        r5 = montar(tmp, "m5")
        (r5 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        (r5 / ".consenso-lock").mkdir()
        code5, out5 = consenso(["debate", "--projeto", str(r5), "--pergunta", str(r5 / "pergunta.md"),
                                "--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta"], env)
        res.check(code5 == 5 and "lock" in norm(out5) and "rmdir" in norm(out5)
                  and (r5 / ".consenso-lock").is_dir() and not rodadas(r5),
                  "lock ocupado: exit 5 citando lock e rmdir, sem run dir, lock alheio fica")
        (r5 / ".consenso-lock").rmdir()
        code5b, _ = consenso(["debate", "--projeto", str(r5), "--pergunta", str(r5 / "pergunta.md"),
                              "--agente", "alfa", "ag-rapido", "--agente", "beta", "ag-beta",
                              "--titulo", "Depois do lock"], env)
        res.check(code5b == 0 and not (r5 / ".consenso-lock").exists(),
                  "depois de limpar o lock orfao a proxima rodada sai 0 e nao deixa lock")

        r6 = montar(tmp, "m6")
        (r6 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        args6 = ["debate", "--projeto", str(r6), "--pergunta", str(r6 / "pergunta.md"),
                 "--agente", "alfa", "ag-lento", "--agente", "beta", "ag-beta"]
        a = consenso_popen(args6, env)
        time.sleep(1.0)
        code_b, out_b = consenso(args6, env, timeout=3)
        if a is not None:
            a.communicate(timeout=90)
        sobras = [p.name for p in r6.iterdir() if "lock" in p.name.lower()]
        res.check(a is not None and code_b == 5 and "lock" in norm(out_b)
                  and a.returncode == 0 and not sobras,
                  "segunda execucao simultanea sai 5; a primeira fecha; nenhum lock sobra")

        r7 = montar(tmp, "m7")
        c7 = r7 / "docs" / "CONSENSUS.md"
        (r7 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes7 = c7.read_bytes()
        p = consenso_popen(["debate", "--projeto", str(r7), "--pergunta", str(r7 / "pergunta.md"),
                            "--agente", "rapido", "ag-rapido", "--agente", "lento", "ag-muito-lento"], env)
        if p is not None:
            for _ in range(50):
                if any((run / "rapido" / "stdout.txt").is_file() for run in rodadas(r7)):
                    break
                time.sleep(0.1)
            time.sleep(0.5)
            p.terminate()
            try:
                p.communicate(timeout=20)
            except Exception:
                p.kill()
        runs7 = rodadas(r7)
        m7 = manifesto(runs7[0]) if runs7 else {}
        temporarios = [x.name for x in (r7 / "docs").glob("CONSENSUS.md.*")]
        res.check(p is not None and c7.read_bytes() == antes7 and len(runs7) == 1
                  and m7.get("status") == "interrompida"
                  and (runs7[0] / "rapido" / "stdout.txt").is_file()
                  and not temporarios and not (r7 / ".consenso-lock").exists(),
                  "SIGTERM: CONSENSUS.md byte a byte, manifesto interrompida, bruto pago, sem temporario, sem lock")


def hashlib_texto(texto):
    import hashlib
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def segredo_no_projeto(r, texto):
    for p in Path(r).rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            try:
                if texto in p.read_bytes().decode("utf-8", errors="replace"):
                    return p.relative_to(r).as_posix()
            except OSError:
                continue
    return None


def testar_varredura_de_segredo(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-limpo", AG_LIMPO_SEGREDO), ("ag-limpo2", AG_LIMPO2_SEGREDO),
                            ("ag-aws", AG_AWS), ("ag-pem", AG_PEM), ("ag-ghp", AG_GHP),
                            ("ag-apikey", AG_APIKEY), ("ag-url", AG_URL),
                            ("ag-sk", AG_SK), ("ag-limpo3", AG_LIMPO3_SEGREDO)):
            agente(tmp, nome, corpo)
        env = ambiente(tmp)

        r = montar(tmp, "s1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        antes = c.read_bytes()
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "limpo", "ag-limpo", "--agente", "vaza", "ag-aws"], env)
        runs = rodadas(r)
        m = manifesto(runs[0]) if runs else {}
        pv = participante(m, "vaza")
        retido = str(pv.get("retido_em") or "")
        manif_texto = ler(runs[0] / "manifesto.json") if runs and (runs[0] / "manifesto.json").is_file() else ""
        retido_ok = (retido and Path(retido).exists() and not retido.startswith(str(r))
                     and (Path(retido) / "stdout.txt").is_file()
                     and CHAVE_AWS in ler(Path(retido) / "stdout.txt"))
        res.check(code == 6 and retido_ok and retido in out
                  and segredo_no_projeto(r, CHAVE_AWS) is None
                  and pv.get("resultado") == "retido-por-segredo" and CHAVE_AWS not in manif_texto
                  and m.get("status") == "parada-segredo"
                  and runs and (runs[0] / "limpo" / "stdout.txt").is_file()
                  and c.read_bytes() == antes and not (r / ".consenso-lock").exists(),
                  "segredo no bruto: exit 6, retido fora, manifesto sem o conteudo, minuta intacta")

        for rotulo, nome, marca in (("PEM", "ag-pem", PEM), ("token ghp_", "ag-ghp", GHP),
                                    ("api_key =", "ag-apikey", APIKEY),
                                    ("URL com senha", "ag-url", "senha123"),
                                    ("prefixo sk-", "ag-sk", SK)):
            rx = montar(tmp, "s-" + nome)
            (rx / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
            code, _ = consenso(["debate", "--projeto", str(rx), "--pergunta", str(rx / "pergunta.md"),
                                "--agente", "limpo", "ag-limpo", "--agente", "suspeito", nome], env)
            res.check(code == 6 and segredo_no_projeto(rx, marca) is None,
                      "padrao %s sozinho dispara: exit 6 e nada gravado no projeto" % rotulo,
                      "exit %s" % code)

        r3 = montar(tmp, "s3")
        (r3 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code, _ = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md"),
                            "--agente", "limpo", "ag-limpo", "--agente", "limpo2", "ag-limpo2"], env)
        res.check(code == 0, "palavras chave de API, token, senha e segredo sem valor nao disparam")
        r3b = montar(tmp, "s3b")
        (r3b / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code, _ = consenso(["debate", "--projeto", str(r3b), "--pergunta", str(r3b / "pergunta.md"),
                            "--agente", "limpo", "ag-limpo", "--agente", "limpo3", "ag-limpo3"], env)
        res.check(code == 0, "task-force, risk-based e desk-top nao disparam o prefixo sk-", "exit %s" % code)

        r4 = montar(tmp, "s4")
        (r4 / "pergunta.md").write_text(PERGUNTA + "\nContexto: o repositorio usa %s para clonar.\n"
                                       % URL_SEGREDO, encoding="utf-8")
        log4 = tmp / "prompts-s4.txt"
        code, _ = consenso(["debate", "--projeto", str(r4), "--pergunta", str(r4 / "pergunta.md"),
                            "--agente", "limpo", "ag-limpo", "--agente", "limpo2", "ag-limpo2"],
                           ambiente(tmp, LOG_PROMPT=log4))
        brutos = [p for run in rodadas(r4) for p in run.rglob("stdout.txt")]
        res.check(code == 6 and not prompts(log4) and not brutos
                  and segredo_no_projeto(r4 / "docs", "senha123") is None,
                  "pergunta com segredo: exit 6 antes de chamar agente, sem bruto em docs/")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Testa o primitivo de consenso com agente falso.")
    parser.add_argument("--verbose", action="store_true", help="Mostra tambem o que passou.")
    args = parser.parse_args(argv)

    res = Resultado(args.verbose)
    testar_primitivo(res)
    testar_lock_e_minuta(res)
    testar_varredura_de_segredo(res)
    print("Modulo de consenso: %s/%s verificacoes passaram." % (res.total - res.falhas, res.total))
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
