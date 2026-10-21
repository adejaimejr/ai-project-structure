#!/usr/bin/env python3
"""Testa o primitivo de consenso em projetos descartaveis, com agente falso.

Uso:
    python3 docs/skills/ai-project-structure/evals/test_consenso.py [--verbose]

Cobre os criterios de comportamento da spec 0006 que cabem no primitivo
(`scripts/consenso.py debate` e `achado`): isolamento verificavel sem confiar no relato,
falha registrada sem derrubar a rodada, nenhum artefato sem execucao,
sidecar in-repo fora da arvore de execucao, recusa de elegibilidade, lock
exclusivo, minuta atomica com julgamento em branco, interrupcao sem tocar
em CONSENSUS.md e varredura de segredo que para a rodada sem redigir. O pacote de
achado (T-079) escreve dentro da entrada existente: campos, secoes, recusas e o
resto do arquivo byte a byte.

Nenhuma chamada de modelo: o agente e um shell script que registra o prompt
recebido. Roda em segundos e nao custa nada, entao pode rodar sempre.

Nao e distribuido pelo `install.sh`: vive em `evals/`, so na fonte canonica.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 se tudo passar.
"""

import argparse
import json
import os
import re
import shutil
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


TITULO_A = "2026-09-01 - Achado Z-9 da bateria"
DECISAO = "### Decisao Para Registrar Em DECISIONS.md\n\n- (A preencher.)\n"


def entrada_de_achado(titulo=TITULO_A, rodada="1 de 1", extra_cabecalho="", decisao=True,
                      achado="Z-9"):
    achado_linha = "**Achado:** %s\n\n" % achado if achado else ""
    return (
        "\n## %s\n\n%s**Status:** aberto\n\n**Proximo passo:** revalidar com outro modelo\n\n"
        "**Metodo:** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n\n"
        "**Rodada:** %s\n\n%s**Escapou de verificacao:** nao\n\n### Contexto\n\n- contexto.\n\n"
        "### Disposicao\n\n- DISPOSICAO-TOKEN-079B: manter o oracle.\n\n### Revalidacao\n\n"
        "- (A preencher.)\n%s"
    ) % (titulo, achado_linha, rodada, extra_cabecalho, ("\n" + DECISAO) if decisao else "")


AG_REV_A = "echo 'Parecer A TOKEN-REV-A-079B'\n"
AG_REV_B = "echo 'Parecer B TOKEN-REV-B-079B'\n"
AG_VE_TUDO = r"""
if grep -q "TOKEN-CONTROLE-079B" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-CONTROLE; fi
if grep -q "DISPOSICAO-TOKEN-079B" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-ALVO; fi
if grep -rq "TOKEN-PAR-079B" . 2>/dev/null; then echo VAZOU; else echo ISOLADO; fi
if [ -e docs/consensus ]; then echo SIDECAR-VISIVEL; fi
echo "Parecer TOKEN-VE-079B"
"""
AG_PAR_B = "echo 'Parecer do par TOKEN-PAR-079B'\n"


def montar_achado(tmp, nome, entrada=None, controle=True):
    r = montar(tmp, nome)
    c = r / "docs" / "CONSENSUS.md"
    texto = ler(c) + (entrada if entrada is not None else entrada_de_achado())
    if controle:
        texto += entrada_de_debate("2026-09-02", "Controle TOKEN-CONTROLE-079B")
    c.write_text(texto, encoding="utf-8")
    return r, c


def corpo(texto, titulo=TITULO_A):
    return re.search(r"^## " + re.escape(titulo) + r"\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S).group(0)


def testar_achado(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo_ag in (("ag-a", AG_REV_A), ("ag-b", AG_REV_B), ("ag-falho", AG_FALHO),
                               ("ag-inj", AG_INJETA), ("ag-ve", AG_VE_TUDO), ("ag-par", AG_PAR_B),
                               ("ag-aws", AG_AWS), ("ag-lento", AG_MUITO_LENTO)):
            agente(tmp, nome, corpo_ag)
        env = ambiente(tmp)

        # Dois revisores, um falha, rodada 2, pergunta adicional: campos, secoes, prompt, manifesto.
        r, c = montar_achado(tmp, "a1")
        (r / "extra.md").write_text("Pergunta extra TOKEN-EXTRA-079B: o oracle cobre?\n", encoding="utf-8")
        antes = ler(c)
        e_antes = corpo(antes)
        code, out = consenso(["achado", "--projeto", str(r), "--entrada", TITULO_A, "--rodada", "2",
                              "--agente", "a", "ag-a", "--agente", "falho", "ag-falho",
                              "--pergunta", str(r / "extra.md"), "--dono", "beltrano"],
                             env)
        depois = ler(c)
        e = corpo(depois)
        runs = rodadas(r)
        m = manifesto(runs[0]) if len(runs) == 1 else {}
        res.check(code == 0 and campo(e, "Participantes") == "a, falho" and campo(e, "Falhas") == "falho"
                  and campo(e, "Rodada") == "2 de 2" and campo(e, "Origem") == "automacao"
                  and campo(e, "Proximo passo") == "beltrano le as revalidacoes e decide"
                  and citado(secao(e, "Revalidacao De a"), "TOKEN-REV-A-079B")
                  and secao(e, "Revalidacao De falho") is None
                  and "4" in (secao(e, "Falha De falho") or "")
                  and "docs/consensus/" in (secao(e, "Falha De falho") or ""),
                  "achado com um revisor ok e um falho: posicao em citacao, Falha De com exit e caminho",
                  "exit %s; %s" % (code, out.strip()[-100:]))
        res.check(depois.replace(e, "") == antes.replace(e_antes, "")
                  and all(secao(e, s) == secao(e_antes, s)
                          for s in ("Contexto", "Disposicao", "Revalidacao", "Decisao Para Registrar Em DECISIONS.md"))
                  and campo(e, "Status") == "aberto" and campo(e, "Achado") == "Z-9"
                  and campo(e, "Escapou de verificacao") == "nao",
                  "achado: Status, Achado, Escapou e as secoes de antes ficam byte a byte")
        ordem = [x.group(1) for x in re.finditer(r"^### (.*)$", e, re.M)]
        res.check(ordem.index("Revalidacao De a") < ordem.index("Falha De falho")
                  < ordem.index("Decisao Para Registrar Em DECISIONS.md")
                  and ordem.index("Revalidacao") < ordem.index("Revalidacao De a"),
                  "achado: secoes novas entram antes de Decisao Para Registrar, depois das existentes",
                  str(ordem))
        pa = participante(m, "a")
        run = runs[0] if runs else r
        prompt = ler(run / "a" / "prompt.txt") if (run / "a" / "prompt.txt").is_file() else ""
        npro = norm(prompt)
        res.check(m.get("modo") == "achado" and m.get("rodada") == 2 and m.get("entrada") == TITULO_A
                  and m.get("status") == "concluida" and corpo(antes).strip() in prompt
                  and "TOKEN-EXTRA-079B" in prompt and "disposicao" in npro and "nao o achado" in npro
                  and (run / "falho" / "prompt.txt").is_file() and corpo(antes).strip() in ler(run / "falho" / "prompt.txt")
                  and pa.get("sha256_prompt") == sha256(run / "a" / "prompt.txt"),
                  "prompt traz a entrada na integra, a pergunta extra e diz que se avalia a disposicao, nao o achado")
        entrada_salva = run / "entrada.txt"
        res.check(entrada_salva.is_file() and ler(entrada_salva) == e_antes
                  and m.get("sha256_entrada") == sha256(entrada_salva)
                  and (run / "pergunta.txt").is_file() and sha256(run / "pergunta.txt") == sha256(r / "extra.md"),
                  "sidecar guarda a entrada-alvo e a pergunta byte a byte, com o hash no manifesto")
        minuta = m.get("minuta") or {}
        res.check(minuta.get("entrada") == TITULO_A and minuta.get("arquivo") == "docs/CONSENSUS.md"
                  and minuta.get("sha256_antes") == hashlib_texto(antes) and minuta.get("sha256_depois") == sha256(c)
                  and not (r / ".consenso-lock").exists()
                  and not list((r / "docs").glob("CONSENSUS.md.*")),
                  "manifesto.minuta com hashes batendo; sem lock nem temporario")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "achado com participante falho passa em --strict sem diagnostico",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))

        # Mesmo segundo, mesmo projeto: a segunda rodada nao atropela a primeira.
        code2, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO_A, "--rodada", "3",
                             "--agente", "b", "ag-b"], env)
        e2 = corpo(ler(c))
        runs2 = rodadas(r)
        manifs = [x.strip() for x in (campo(e2, "Manifesto") or "").split(",")]
        res.check(code2 == 0 and len(runs2) == 2 and len(manifs) == 2 and len(set(manifs)) == 2
                  and all((r / x).is_file() for x in manifs)
                  and campo(e2, "Participantes") == "a, falho, b" and campo(e2, "Falhas") == "falho"
                  and citado(secao(e2, "Revalidacao De a"), "TOKEN-REV-A-079B")
                  and citado(secao(e2, "Revalidacao De b"), "TOKEN-REV-B-079B"),
                  "segunda rodada seguida: pasta propria, Manifesto com dois caminhos, lista e secoes acumuladas")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "entrada com dois manifestos na lista passa em --strict sem diagnostico",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))
        r2q, c2q = montar_achado(tmp, "a2q")
        consenso(["achado", "--projeto", str(r2q), "--entrada", TITULO_A, "--rodada", "2", "--agente", "a", "ag-a"], env)
        c2q.write_text(ler(c2q).replace("/manifesto.json\n", "/manifesto.json, docs/consensus/nao-existe/manifesto.json\n", 1), encoding="utf-8")
        code_q, linhas_q, _ = validar(r2q, "--strict", "--codigos")
        res.check(code_q == 1 and len(linhas_q) == 1 and "CONSENSO-ORIGEM-MANIFESTO-QUEBRADO" in linhas_q[0],
                  "um manifesto da lista que nao resolve gera exatamente um CONSENSO-ORIGEM-MANIFESTO-QUEBRADO",
                  "exit %s; %s" % (code_q, "; ".join(linhas_q)[:120]))
        code3, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO_A, "--rodada", "3",
                             "--agente", "falho", "ag-a"], env)
        antes3 = ler(c)
        res.check(code3 == 1 and ler(c) == antes3 and len(rodadas(r)) == 2,
                  "id que so tem 'Falha De' tambem e recusado: exit 1, sem run dir novo")

        # Pendente: rodada 4 escreve, rodada 5 troca o valor em vez de duplicar a linha.
        code4, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO_A, "--rodada", "4",
                             "--pendente", "o oracle ficou aberto", "--agente", "c", "ag-a"], env)
        code5, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO_A, "--rodada", "5",
                             "--pendente", "falta medir " + TRAVESSAO + " custo", "--agente", "d", "ag-b"], env)
        e5 = corpo(ler(c))
        res.check(code4 == 0 and code5 == 0 and e5.count("**Pendente da rodada anterior:**") == 1
                  and campo(e5, "Pendente da rodada anterior") == "falta medir - custo"
                  and e5.count("**Origem:**") == 1 and e5.count("**Rodada:**") == 1
                  and campo(e5, "Rodada") == "5 de 5" and TRAVESSAO not in ler(c),
                  "pendente trocado, nao duplicado; travessao do texto humano vira hifen; Origem uma vez so")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "entrada na rodada 5, com quatro manifestos na lista, passa em --strict",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))
        r3, c3 = montar_achado(tmp, "a3")
        code, _ = consenso(["achado", "--projeto", str(r3), "--entrada", TITULO_A, "--rodada", "4",
                            "--pendente", "o oracle ficou aberto", "--agente", "a", "ag-a"], env)
        code_v, linhas, _ = validar(r3, "--strict", "--codigos")
        res.check(code == 0 and code_v == 0 and not linhas and campo(corpo(ler(c3)), "Rodada") == "4 de 4",
                  "rodada 4 com --pendente e um manifesto so passa em --strict",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))

        # Elegibilidade: nada muda, nada roda.
        r4, c4 = montar_achado(tmp, "a4")
        sem_achado = entrada_de_debate("2026-09-03", "Debate sem achado")
        c4.write_text(ler(c4) + sem_achado, encoding="utf-8")
        antes4 = c4.read_bytes()
        log4 = tmp / "prompts-a4.txt"
        env4 = ambiente(tmp, LOG_PROMPT=log4)
        base4 = ["achado", "--projeto", str(r4), "--agente", "a", "ag-a"]
        codigos = [consenso(base4 + ["--entrada", "2026-09-03 - Debate sem achado", "--rodada", "2"], env4)[0],
                   consenso(base4 + ["--entrada", TITULO_A, "--rodada", "0"], env4)[0],
                   consenso(base4 + ["--entrada", TITULO_A, "--rodada", "dois"], env4)[0],
                   consenso(["achado", "--projeto", str(r4), "--entrada", TITULO_A, "--rodada", "2"], env4)[0],
                   consenso(base4 + ["--rodada", "2"], env4)[0],
                   consenso(base4 + ["--entrada", TITULO_A, "--rodada", "4", "--pendente", "   "], env4)[0]]
        res.check(codigos == [1] * 6 and c4.read_bytes() == antes4 and not prompts(log4) and not rodadas(r4),
                  "entrada sem Achado, rodada 0, rodada nao numerica, sem --agente, sem --entrada, pendente vazio: exit 1 sem tocar em nada",
                  str(codigos))
        r4b, c4b = montar_achado(tmp, "a4b", entrada=entrada_de_achado() + entrada_de_achado(achado="Z-10"))
        antes4b = c4b.read_bytes()
        code_dup, _ = consenso(["achado", "--projeto", str(r4b), "--entrada", TITULO_A, "--rodada", "2",
                                "--agente", "a", "ag-a"], env4)
        res.check(code_dup == 1 and c4b.read_bytes() == antes4b and not rodadas(r4b),
                  "titulo repetido no arquivo: exit 1 em vez de escolher uma das entradas")
        r4c, c4c = montar_achado(tmp, "a4c")
        code_a2, _ = consenso(["achado", "--projeto", str(r4c), "--entrada", TITULO_A, "--rodada", "3",
                               "--agente", "a", "ag-a"], env4)
        res.check(code_a2 == 0 and campo(corpo(ler(c4c)), "Rodada") == "3 de 3",
                  "rodada 3 sem --pendente e aceita (o piso do validador e 4)")
        r4d, c4d = montar_achado(tmp, "a4d")
        subprocess.run(["git", "init", "-q"], cwd=r4d, check=False, capture_output=True)
        (r4d / ".gitignore").write_text("docs/consensus/\n", encoding="utf-8")
        antes4d = c4d.read_bytes()
        code_ig, out_ig = consenso(["achado", "--projeto", str(r4d), "--entrada", TITULO_A, "--rodada", "2",
                                    "--agente", "a", "ag-a"], env4)
        res.check(code_ig == 1 and "ignor" in norm(out_ig) and c4d.read_bytes() == antes4d and not rodadas(r4d),
                  "achado com docs/consensus/ no .gitignore: exit 1 antes de chamar agente")

        # Entrada sem a secao final: as secoes vao para o fim da entrada, antes da proxima.
        r5, c5 = montar_achado(tmp, "a5", entrada=entrada_de_achado(decisao=False))
        antes5 = ler(c5)
        code, _ = consenso(["achado", "--projeto", str(r5), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "a", "ag-a"], env)
        depois5 = ler(c5)
        e5 = corpo(depois5)
        ordem5 = [x.group(1) for x in re.finditer(r"^### (.*)$", e5, re.M)]
        controle5 = "Controle TOKEN-CONTROLE-079B"
        res.check(code == 0 and ordem5[-1] == "Revalidacao De a"
                  and depois5.endswith(antes5[antes5.index("\n## 2026-09-02"):])
                  and corpo(depois5, "2026-09-02 - " + controle5) == corpo(antes5, "2026-09-02 - " + controle5),
                  "entrada sem Decisao: secao no fim da entrada; entrada seguinte byte a byte", str(ordem5))
        code_v, linhas, _ = validar(r5, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "entrada sem Decisao passa em --strict",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:120]))
        r5b, c5b = montar_achado(tmp, "a5b", entrada=entrada_de_achado(decisao=False), controle=False)
        antes5b = ler(c5b)
        code, _ = consenso(["achado", "--projeto", str(r5b), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "a", "ag-a"], env)
        depois5b = ler(c5b)
        res.check(code == 0 and depois5b.startswith(antes5b.rstrip("\n").split("### Revalidacao")[0])
                  and depois5b.endswith("\n") and "Revalidacao De a" in depois5b,
                  "entrada que e a ultima do arquivo e termina sem Decisao: acrescenta e fecha com quebra de linha")

        # Injecao e travessao na resposta: citados, entradas intactas, bruto cru.
        r6, c6 = montar_achado(tmp, "a6")
        antes6 = ler(c6)
        code, _ = consenso(["achado", "--projeto", str(r6), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "alfa", "ag-inj"], env)
        depois6 = ler(c6)
        runs6 = rodadas(r6)
        bruto6 = runs6[0] / "alfa" / "stdout.txt" if runs6 else r6
        res.check(code == 0 and "> ## 2026-01-01 - INJETADO" in depois6 and TRAVESSAO not in depois6
                  and re.findall(r"^## (\d{4}-\d{2}-\d{2}.*)$", depois6, re.M)
                  == re.findall(r"^## (\d{4}-\d{2}-\d{2}.*)$", antes6, re.M)
                  and bruto6.is_file() and TRAVESSAO in ler(bruto6),
                  "resposta com heading falso e travessao: citada, nenhuma entrada nova, bruto intacto")

        # Isolamento: cada revisor ve CONSENSUS.md inteiro e a entrada-alvo, nunca o par nem o sidecar.
        r7, c7 = montar_achado(tmp, "a7")
        code, _ = consenso(["achado", "--projeto", str(r7), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "ve", "ag-ve", "--agente", "par", "ag-par"], env)
        runs7 = rodadas(r7)
        saida7 = ler(runs7[0] / "ve" / "stdout.txt") if runs7 else ""
        res.check(code == 0 and "VEJO-CONTROLE" in saida7 and "VEJO-ALVO" in saida7 and "ISOLADO" in saida7
                  and "VAZOU" not in saida7 and "SIDECAR-VISIVEL" not in saida7,
                  "copia traz CONSENSUS.md inteiro (alvo e controle), sem o par e sem o sidecar",
                  saida7.strip()[:80])

        # Falha unica, segredo, lock, sinal: nada entra em CONSENSUS.md.
        r8, c8 = montar_achado(tmp, "a8")
        antes8 = c8.read_bytes()
        code_f, _ = consenso(["achado", "--projeto", str(r8), "--entrada", TITULO_A, "--rodada", "2",
                              "--agente", "falho", "ag-falho"], env)
        runs8 = rodadas(r8)
        m8 = manifesto(runs8[0]) if runs8 else {}
        res.check(code_f == 2 and c8.read_bytes() == antes8 and m8.get("status") == "sem-posicao"
                  and (runs8[0] / "falho" / "stderr.txt").is_file() and m8.get("minuta") is None,
                  "revisor unico falho: exit 2, sem-posicao, entrada byte a byte, bruto da falha no sidecar")

        r9, c9 = montar_achado(tmp, "a9")
        antes9 = c9.read_bytes()
        code_s, out_s = consenso(["achado", "--projeto", str(r9), "--entrada", TITULO_A, "--rodada", "2",
                                  "--agente", "a", "ag-a", "--agente", "vaza", "ag-aws"], env)
        runs9 = rodadas(r9)
        res.check(code_s == 6 and c9.read_bytes() == antes9 and segredo_no_projeto(r9, CHAVE_AWS) is None
                  and runs9 and manifesto(runs9[0]).get("status") == "parada-segredo"
                  and not (r9 / ".consenso-lock").exists(),
                  "segredo no bruto do revisor: exit 6, retido fora, entrada byte a byte, sem lock")

        r10, c10 = montar_achado(tmp, "a10", entrada=entrada_de_achado().replace(
            "- contexto.", "- contexto com %s no meio." % URL_SEGREDO))
        antes10 = c10.read_bytes()
        log10 = tmp / "prompts-a10.txt"
        code_e, _ = consenso(["achado", "--projeto", str(r10), "--entrada", TITULO_A, "--rodada", "2",
                              "--agente", "a", "ag-a"], ambiente(tmp, LOG_PROMPT=log10))
        res.check(code_e == 6 and c10.read_bytes() == antes10 and not prompts(log10) and not rodadas(r10),
                  "segredo na entrada-alvo: exit 6 antes de chamar agente, sem run dir")

        r11, c11 = montar_achado(tmp, "a11")
        antes11 = c11.read_bytes()
        (r11 / ".consenso-lock").mkdir()
        code_l, out_l = consenso(["achado", "--projeto", str(r11), "--entrada", TITULO_A, "--rodada", "2",
                                  "--agente", "a", "ag-a"], env)
        res.check(code_l == 5 and "lock" in norm(out_l) and c11.read_bytes() == antes11
                  and (r11 / ".consenso-lock").is_dir() and not rodadas(r11),
                  "lock ocupado: achado sai 5, entrada byte a byte, lock alheio fica")

        r12, c12 = montar_achado(tmp, "a12")
        antes12 = c12.read_bytes()
        p = consenso_popen(["achado", "--projeto", str(r12), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "a", "ag-a", "--agente", "lento", "ag-lento"], env)
        if p is not None:
            for _ in range(50):
                if any((run / "a" / "stdout.txt").is_file() for run in rodadas(r12)):
                    break
                time.sleep(0.1)
            time.sleep(0.5)
            p.terminate()
            try:
                p.communicate(timeout=20)
            except Exception:
                p.kill()
        runs12 = rodadas(r12)
        res.check(p is not None and c12.read_bytes() == antes12 and len(runs12) == 1
                  and manifesto(runs12[0]).get("status") == "interrompida"
                  and (runs12[0] / "a" / "stdout.txt").is_file()
                  and not list((r12 / "docs").glob("CONSENSUS.md.*")) and not (r12 / ".consenso-lock").exists(),
                  "SIGTERM no achado: entrada byte a byte, manifesto interrompida, bruto pago, sem temporario, sem lock")

        # Cabecalho incompleto: o que falta e criado, a ancora e obrigatoria.
        r13, c13 = montar_achado(tmp, "a13", entrada=entrada_de_achado().replace(
            "**Metodo:** pareceres-independentes\n\n", "").replace(
            "**Exposicao previa a outras posicoes:** nao\n\n", ""))
        code, _ = consenso(["achado", "--projeto", str(r13), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "a", "ag-a"], env)
        e13 = corpo(ler(c13))
        code_v, linhas, _ = validar(r13, "--strict", "--codigos")
        res.check(code == 0 and campo(e13, "Metodo") == "pareceres-independentes"
                  and campo(e13, "Exposicao previa a outras posicoes") == "sim" and code_v == 0 and not linhas,
                  "cabecalho sem Metodo e Exposicao: os campos sao criados e a entrada passa em --strict",
                  "exit %s; %s" % (code, "; ".join(linhas)[:100]))
        r14, c14 = montar_achado(tmp, "a14", entrada=entrada_de_achado().replace("**Rodada:** 1 de 1\n\n", ""))
        antes14 = c14.read_bytes()
        code, _ = consenso(["achado", "--projeto", str(r14), "--entrada", TITULO_A, "--rodada", "2",
                            "--agente", "a", "ag-a"], env)
        res.check(code == 1 and c14.read_bytes() == antes14 and not rodadas(r14),
                  "entrada sem '**Rodada:**': exit 1, sem ancora para os campos novos, nada muda")


# --- rodada 2 em diante: posicoes anteriores na integra (T-080) ------------

AG_R1_GRANDE = r"""
echo "TOKEN-G1-080 posicao grande da rodada um"
head -c 60000 /dev/zero | tr '\0' 'y'
echo
echo "FIM-GRANDE-080 texto com travessao """ + TRAVESSAO + r""" no fim"
"""
AG_R1_CURTO = "echo 'TOKEN-C1-080 posicao curta da rodada um'\n"
AG_R2_VE = r"""
P="${@: -1}"
case "$P" in *FIM-GRANDE-080*) echo VEJO-FIM;; esac
case "$P" in *TOKEN-C1-080*) echo VEJO-CURTO;; esac
if grep -q "TOKEN-EXISTENTE-080" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-EXISTENTE; fi
if grep -q "TOKEN-PUBLICADA-080" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-PUBLICADA; fi
echo "POSICAO-R2 TOKEN-R2-080"
"""
AG_R2_PAR = r"""
for i in $(seq 1 60); do
  if ls "$PROJETO_REAL"/docs/consensus/*/ve/stdout.txt >/dev/null 2>&1; then break; fi
  sleep 0.5
done
if grep -rq "TOKEN-R2-080" . 2>/dev/null; then echo VAZOU; else echo ISOLADO; fi
echo "POSICAO-R2-PAR TOKEN-R2PAR-080"
"""


def debate_base(r, extra=()):
    return ["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"), *extra]


def testar_rodada_dois(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo_agente in (("ag-g1", AG_R1_GRANDE), ("ag-c1", AG_R1_CURTO), ("ag-ve", AG_R2_VE),
                                   ("ag-par2", AG_R2_PAR), ("ag-falho", AG_FALHO)):
            agente(tmp, nome, corpo_agente)

        r = montar(tmp, "r1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        env = ambiente(tmp, PROJETO_REAL=r)
        code1, _ = consenso(debate_base(r, ["--agente", "grande", "ag-g1", "--agente", "curto", "ag-c1",
                                            "--titulo", "Rodada um TOKEN-PUBLICADA-080"]), env)
        runs = rodadas(r)
        run1 = runs[0] if runs else r
        antes = c.read_bytes()
        code2, out2 = consenso(debate_base(r, ["--rodada", "2", "--anterior", str(run1),
                                               "--agente", "ve", "ag-ve", "--agente", "par", "ag-par2",
                                               "--titulo", "Rodada dois"]), env)
        runs = rodadas(r)
        run2 = next((x for x in runs if x != run1), None)
        depois = c.read_bytes()
        novo = depois[len(antes):].decode("utf-8") if depois.startswith(antes) else ""
        bruto_grande = (run1 / "grande" / "stdout.txt").read_bytes() if code1 == 0 else b"?"
        prompt = ler(run2 / "ve" / "prompt.txt") if run2 else ""
        saida_ve = ler(run2 / "ve" / "stdout.txt") if run2 else ""
        res.check(code1 == 0 and code2 == 0 and len(bruto_grande) > 60000, "rodada 1 e rodada 2 em sequencia saem 0",
                  "exit %s %s; %s" % (code1, code2, out2.strip()[-100:]))
        res.check(bruto_grande.decode("utf-8") in prompt and prompt.rstrip("\n").count("FIM-GRANDE-080") == 1
                  and "VEJO-FIM" in saida_ve and "VEJO-CURTO" in saida_ve,
                  "anterior de 60KB com marca no fim entra inteiro no prompt e o agente enxerga a marca",
                  "prompt=%d bytes; %s" % (len(prompt), saida_ve.strip().replace("\n", " | ")[:80]))
        res.check(TRAVESSAO in prompt and "Anterior: grande (" in prompt and "Anterior: curto (" in prompt
                  and "Fim de grande" in prompt,
                  "anteriores rotulados pelo id, com travessao do bruto preservado no prompt")
        argumentos = ler(run2 / "ve" / "prompt.txt") if run2 else ""
        res.check(prompt.index("Pergunta:") < prompt.index("TOKEN-G1-080")
                  and "TOKEN-BATERIA-075" in argumentos,
                  "pergunta vem antes das posicoes anteriores, que ficam no fim do prompt")

        corpo2 = novo
        res.check(campo(corpo2, "Rodada") == "2 de 2" and campo(corpo2, "Exposicao previa a outras posicoes") == "sim"
                  and campo(corpo2, "Metodo") == "pareceres-independentes" and TRAVESSAO not in novo
                  and "Pendente da rodada anterior" not in corpo2,
                  "minuta da rodada 2: Rodada 2 de 2, Exposicao sim, Metodo, sem travessao, sem pendente espuria")
        res.check(depois.startswith(antes) and novo.startswith("\n## "),
                  "CONSENSUS.md so cresce no fim: o prefixo com a entrada da rodada 1 fica byte a byte")

        m2 = manifesto(run2) if run2 else {}
        esperado = {sha256(run1 / pid / "stdout.txt") for pid in ("grande", "curto")} if code1 == 0 else {"?"}
        anteriores = m2.get("anteriores", [])
        res.check(m2.get("rodada") == 2 and {a.get("sha256") for a in anteriores} == esperado
                  and all(a.get("caminho", "").startswith("docs/consensus/") and a["caminho"].endswith("/stdout.txt")
                          for a in anteriores) and m2.get("status") == "concluida"
                  and manifesto(run1).get("anteriores") == [],
                  "manifesto da rodada 2 lista caminho e sha256 dos stdout anteriores; o da rodada 1 lista vazio")

        # Copia da rodada 2: CONSENSUS.md inteiro (publicado), contemporanea fora (DEC-003, DEC-009).
        res.check("VEJO-PUBLICADA" in saida_ve,
                  "na rodada 2 a copia traz a entrada publicada da rodada 1 em CONSENSUS.md")
        saida_par = ler(run2 / "par" / "stdout.txt") if run2 else ""
        res.check("ISOLADO" in saida_par and "VAZOU" not in saida_par,
                  "na rodada 2 a posicao contemporanea continua fora da copia do par", saida_par.strip()[:60])

        # Rodada 3 encadeia duas rodadas como anteriores: ids repetidos, caminhos distintos.
        antes3 = c.read_bytes()
        code3, _ = consenso(debate_base(r, ["--rodada", "3", "--anterior", str(run1), "--anterior", str(run2),
                                            "--agente", "ve", "ag-ve", "--agente", "curto", "ag-c1",
                                            "--titulo", "Rodada tres"]), env)
        runs3 = [x for x in rodadas(r) if x not in (run1, run2)]
        prompt3 = ler(runs3[0] / "ve" / "prompt.txt") if runs3 else ""
        m3 = manifesto(runs3[0]) if runs3 else {}
        res.check(code3 == 0 and prompt3.count("----- Anterior: ") == 4 and "TOKEN-R2-080" in prompt3
                  and "TOKEN-G1-080" in prompt3 and len(m3.get("anteriores", [])) == 4
                  and c.read_bytes().startswith(antes3),
                  "rodada 3 com duas rodadas como anteriores: quatro posicoes no prompt e no manifesto")

        # Cadeia pequena (a grande acima dispara o aviso de rotacao, que e do tamanho e nao da forma):
        # rodada 1, rodada 2 por diretorio e rodada 4 com --pendente passam em --strict sem aviso.
        r9 = montar(tmp, "r9")
        (r9 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        env9 = ambiente(tmp)
        code9a, _ = consenso(debate_base(r9, ["--agente", "a", "ag-c1", "--agente", "b", "ag-c1"]), env9)
        run9a = rodadas(r9)[0] if rodadas(r9) else r9
        code9b, _ = consenso(debate_base(r9, ["--rodada", "2", "--anterior", str(run9a), "--agente", "a", "ag-c1",
                                              "--agente", "b", "ag-c1", "--titulo", "Rodada dois"]), env9)
        code_v9, linhas9, _ = validar(r9, "--strict", "--codigos")
        res.check(code9a == 0 and code9b == 0 and code_v9 == 0 and not linhas9,
                  "projeto com rodada 1 e rodada 2 passa em --strict sem aviso",
                  "exit %s %s %s; %s" % (code9a, code9b, code_v9, "; ".join(linhas9)[:120]))
        antes4 = (r9 / "docs" / "CONSENSUS.md").read_bytes()
        run9b = next((x for x in rodadas(r9) if x != run9a), r9)
        code4, _ = consenso(debate_base(r9, ["--rodada", "4", "--anterior", str(run9b),
                                             "--pendente", "falta medir " + TRAVESSAO + " o custo",
                                             "--agente", "a", "ag-c1", "--agente", "b", "ag-c1",
                                             "--titulo", "Rodada quatro"]), env9)
        novo4 = (r9 / "docs" / "CONSENSUS.md").read_bytes()[len(antes4):].decode("utf-8")
        code_v4, linhas4, _ = validar(r9, "--strict", "--codigos")
        res.check(code4 == 0 and campo(novo4, "Rodada") == "4 de 4"
                  and campo(novo4, "Pendente da rodada anterior") == "falta medir - o custo"
                  and code_v4 == 0 and not linhas4,
                  "rodada 4 com --pendente: campo na entrada, travessao vira hifen, passa em --strict",
                  "exit %s %s; %s" % (code4, code_v4, "; ".join(linhas4)[:100]))

        # Anterior em arquivo: verbatim, sem rotulo de id, caminho absoluto fora do projeto.
        manual = tmp / "anterior-manual.md"
        manual.write_bytes(("Posicao manual TOKEN-MANUAL-080 com travessao " + TRAVESSAO + "\nsem quebra final").encode("utf-8"))
        r5 = montar(tmp, "r5")
        (r5 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code5, _ = consenso(debate_base(r5, ["--rodada", "2", "--anterior", str(manual),
                                             "--agente", "ve", "ag-ve", "--agente", "curto", "ag-c1"]), env)
        runs5 = rodadas(r5)
        prompt5 = ler(runs5[0] / "ve" / "prompt.txt") if runs5 else ""
        m5 = manifesto(runs5[0]) if runs5 else {}
        res.check(code5 == 0 and manual.read_text(encoding="utf-8") + "\n----- Fim de anterior-manual.md -----" in prompt5
                  and m5.get("anteriores") == [{"caminho": str(manual.resolve()), "sha256": sha256(manual)}],
                  "--anterior em arquivo sem quebra final entra verbatim; o fecho do bloco fica em outra linha")

        # Recusas: exit 1, nada roda, nada se grava.
        r6 = montar(tmp, "r6")
        (r6 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        antes6 = (r6 / "docs" / "CONSENSUS.md").read_bytes()
        log6 = tmp / "prompts-r6.txt"
        env6 = ambiente(tmp, LOG_PROMPT=log6)
        vazio = tmp / "dir-vazio"
        vazio.mkdir()
        ags = ["--agente", "ve", "ag-ve", "--agente", "curto", "ag-c1"]
        casos = [
            ["--rodada", "2"],
            ["--rodada", "2", "--anterior", str(tmp / "nao-existe")],
            ["--rodada", "2", "--anterior", str(vazio)],
            ["--rodada", "4", "--anterior", str(manual)],
            ["--rodada", "0", "--anterior", str(manual)],
            ["--rodada", "dois", "--anterior", str(manual)],
            ["--anterior", str(manual)],
            ["--rodada", "1", "--pendente", "algo"],
        ]
        codigos = [consenso(debate_base(r6, caso + ags), env6)[0] for caso in casos]
        res.check(codigos == [1] * len(casos) and not prompts(log6) and not rodadas(r6)
                  and (r6 / "docs" / "CONSENSUS.md").read_bytes() == antes6,
                  "rodada 2 sem anterior, anterior inexistente ou sem stdout, rodada 4 sem pendente, rodada 0 ou "
                  "nao numerica, anterior ou pendente na rodada 1: exit 1 sem agente, sem run dir",
                  str(codigos))

        # Segredo num anterior: a varredura da T-077 cobre o que entra no prompt.
        sujo = tmp / "anterior-sujo.md"
        sujo.write_text("achei isto: %s\n" % CHAVE_AWS, encoding="utf-8")
        r7 = montar(tmp, "r7")
        (r7 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        log7 = tmp / "prompts-r7.txt"
        code7, out7 = consenso(debate_base(r7, ["--rodada", "2", "--anterior", str(manual), "--anterior", str(sujo)]
                                           + ags), ambiente(tmp, LOG_PROMPT=log7))
        res.check(code7 == 6 and not prompts(log7) and not rodadas(r7) and CHAVE_AWS not in out7
                  and not (r7 / ".consenso-lock").exists(),
                  "segredo num --anterior: exit 6 antes de chamar agente, sem run dir, sem eco do segredo")

        # Retomada do mesmo comportamento: rodada 2 com agente falho registra a falha e segue.
        r8 = montar(tmp, "r8")
        (r8 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code8, _ = consenso(debate_base(r8, ["--rodada", "2", "--anterior", str(manual), "--agente", "ve", "ag-ve",
                                             "--agente", "falho", "ag-falho"]), env)
        novo8 = ler(r8 / "docs" / "CONSENSUS.md")
        code_v8, linhas8, _ = validar(r8, "--strict", "--codigos")
        res.check(code8 == 0 and "### Falha De falho" in novo8 and "### Posicao De ve" in novo8
                  and code_v8 == 0 and not linhas8,
                  "rodada 2 com um agente falho: falha registrada, posicao do outro, passa em --strict",
                  "exit %s %s; %s" % (code8, code_v8, "; ".join(linhas8)[:100]))


# --- retomada por comando explicito (T-081) --------------------------------

CONTA_R = 'echo x >> "$CONTADOR_DIR/$AGENTE_ID"\n'
DORME_R = 'if [ -n "$LENTO" ]; then sleep 3; fi\n'
AG_R_ALFA = "AGENTE_ID=alfa\n" + CONTA_R + "echo 'POSICAO-ALFA TOKEN-ALFA-081'\n"
AG_R_BETA = "AGENTE_ID=beta\n" + CONTA_R + DORME_R + "echo 'POSICAO-BETA TOKEN-BETA-081'\n"
AG_R_FALHO = "AGENTE_ID=falho\n" + CONTA_R + "echo 'cota esgotada' >&2\nexit 4\n"
AG_R_VAZA = "AGENTE_ID=vaza\n" + CONTA_R + "echo 'chave " + CHAVE_AWS + " TOKEN-VAZA-081'\n"
AG_R_REV = "AGENTE_ID=rev\n" + CONTA_R + "echo 'Parecer TOKEN-REV-081'\n"
AG_R_LENTO = "AGENTE_ID=lento\n" + CONTA_R + DORME_R + "echo 'Parecer lento TOKEN-LENTO-081'\n"


def chamadas_de(cont, identificador):
    caminho = Path(cont) / identificador
    return len(ler(caminho).split()) if caminho.is_file() else 0


def interromper(args, env, esperar):
    """Roda `consenso.py`, espera os brutos de `esperar` e manda SIGTERM. Devolve a saida."""
    p = consenso_popen(args, env)
    if p is None:
        return ""
    for _ in range(80):
        if all(any((run / i / "stdout.txt").is_file() for run in rodadas(Path(env["PROJ"]))) for i in esperar):
            break
        time.sleep(0.1)
    time.sleep(0.3)
    p.terminate()
    try:
        saida, _ = p.communicate(timeout=30)
    except Exception:
        p.kill()
        saida = ""
    return saida


def editar_manifesto(run, **mudancas):
    caminho = Path(run) / "manifesto.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    for chave, valor in mudancas.items():
        if valor is None:
            dados.pop(chave, None)
        else:
            dados[chave] = valor
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def testar_retomada(res):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo_ag in (("ag-alfa", AG_R_ALFA), ("ag-beta", AG_R_BETA), ("ag-falho", AG_R_FALHO),
                               ("ag-vaza", AG_R_VAZA), ("ag-rev", AG_R_REV), ("ag-lento", AG_R_LENTO)):
            agente(tmp, nome, corpo_ag)

        def ambiente_de(r, nome, **extra):
            cont = tmp / ("cont-" + nome)
            cont.mkdir(exist_ok=True)
            return ambiente(tmp, CONTADOR_DIR=cont, PROJ=r, **extra), cont

        def retomar(r, run_id, env, timeout=120):
            return consenso(["retomar", "--projeto", str(r), run_id], env, timeout)

        # 1. Debate interrompido: so quem faltava e chamado, a ordem e a minuta sao as de uma rodada normal.
        r = montar(tmp, "t1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        antes = ler(c)
        env_lento, cont = ambiente_de(r, "t1", LENTO="1")
        saida = interromper(debate_base(r, ["--agente", "alfa", "ag-alfa", "--agente", "falho", "ag-falho",
                                            "--agente", "beta", "ag-beta", "--titulo", "Retomada T-081",
                                            "--dono", "fulano"]),
                            env_lento, ["alfa", "falho"])
        runs = rodadas(r)
        run = runs[0] if runs else r
        run_id = run.name
        m = manifesto(run)
        res.check(m.get("status") == "interrompida" and ler(c) == antes
                  and not (run / "beta" / "stdout.txt").exists() and not participante(m, "beta")
                  and "retomar" in saida and run_id in saida,
                  "interrupcao: beta (morto pelo sinal) fica sem bruto e sem registro; a saida cita retomar e o run-id")
        env_rapido, _ = ambiente_de(r, "t1")
        env_rapido["CONTADOR_DIR"] = str(cont)
        log = tmp / "prompts-t1.txt"
        env_rapido["LOG_PROMPT"] = str(log)
        code, out = retomar(r, run_id, env_rapido)
        depois = ler(c)
        novo = depois[len(antes):] if depois.startswith(antes) else ""
        m = manifesto(run)
        ret = (m.get("retomadas") or [{}])[0]
        res.check(code == 0 and chamadas_de(cont, "alfa") == 1 and chamadas_de(cont, "falho") == 1
                  and chamadas_de(cont, "beta") == 2 and len(prompts(log)) == 1
                  and ret.get("chamados") == ["beta"] and ret.get("mantidos") == ["alfa", "falho"]
                  and ret.get("instante") and m.get("status") == "concluida" and m.get("fim"),
                  "retomar chama so beta; alfa e falho (bruto ja pago, mesmo falho) ficam como estavam; retomadas registra",
                  "exit %s %s; %s" % (code, ret, out.strip()[-100:]))
        res.check(campo(novo, "Participantes") == "alfa, falho, beta" and campo(novo, "Falhas") == "falho"
                  and "fulano" in (campo(novo, "Proximo passo") or "")
                  and "Retomada T-081" in novo.splitlines()[1] and "### Falha De falho" in novo
                  and citado(secao(novo, "Posicao De alfa"), "TOKEN-ALFA-081")
                  and citado(secao(novo, "Posicao De beta"), "TOKEN-BETA-081"),
                  "minuta da retomada: titulo, dono, ordem dos participantes e falha como numa rodada normal")
        res.check(m["minuta"]["sha256_antes"] == hashlib_texto(antes) and m["minuta"]["sha256_depois"] == sha256(c)
                  and not (r / ".consenso-lock").exists(),
                  "manifesto selado com os hashes de antes e depois; sem lock sobrando")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        res.check(code_v == 0 and not linhas, "projeto retomado passa em --strict sem diagnostico",
                  "exit %s; %s" % (code_v, "; ".join(linhas)[:100]))
        antes2 = ler(c)
        code2, out2 = retomar(r, run_id, env_rapido)
        res.check(code2 == 1 and ler(c) == antes2 and chamadas_de(cont, "beta") == 2,
                  "retomar em run concluido: exit 1, CONSENSUS.md intacto, ninguem chamado")
        code3, _ = retomar(r, "../fora", env_rapido)
        code4, _ = retomar(r, "2000-01-01-000000-debate", env_rapido)
        res.check(code3 == 1 and code4 == 1, "run-id inseguro ou inexistente: exit 1")

        # 2. Tudo pago, minuta nao saiu: a retomada so escreve a minuta.
        minuta_pronta = novo
        c.write_bytes(antes.encode("utf-8"))
        editar_manifesto(run, status="interrompida", minuta=None, fim=None)
        antes_agentes = json.loads((run / "manifesto.json").read_text(encoding="utf-8"))["agentes"]
        editar_manifesto(run, agentes=None)
        code5, out5 = retomar(r, run_id, env_rapido)
        res.check(code5 == 1 and ler(c) == antes,
                  "manifesto sem os parametros da rodada: exit 1 e nada escrito")
        editar_manifesto(run, agentes=antes_agentes)
        code6, out6 = retomar(r, run_id, env_rapido)
        m = manifesto(run)
        res.check(code6 == 0 and ler(c) == antes + minuta_pronta and chamadas_de(cont, "beta") == 2
                  and chamadas_de(cont, "alfa") == 1 and (m.get("retomadas") or [{}])[-1].get("chamados") == []
                  and len(m.get("retomadas", [])) == 2,
                  "todos os brutos presentes e minuta ausente: so escreve a minuta, ninguem e chamado")

        # 3. Rodada 2 interrompida: o prompt e refeito com os anteriores do manifesto; anterior alterado recusa.
        r2 = montar(tmp, "t2")
        (r2 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        env2, cont2 = ambiente_de(r2, "t2")
        code, _ = consenso(debate_base(r2, ["--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta"]), env2)
        run1 = rodadas(r2)[0] if rodadas(r2) else r2
        env2l, _ = ambiente_de(r2, "t2", LENTO="1")
        c2 = r2 / "docs" / "CONSENSUS.md"
        antes_r2 = ler(c2)
        interromper(debate_base(r2, ["--rodada", "2", "--anterior", str(run1), "--agente", "alfa", "ag-alfa",
                                     "--agente", "beta", "ag-beta", "--titulo", "Rodada dois"]),
                    env2l, ["alfa"])
        run2 = next((x for x in rodadas(r2) if x != run1), r2)
        bruto_ant = run1 / "alfa" / "stdout.txt"
        original = bruto_ant.read_bytes()
        bruto_ant.write_bytes(original + b"mudou\n")
        antes_chamadas = chamadas_de(cont2, "beta")
        code_m, out_m = retomar(r2, run2.name, env2)
        res.check(code_m == 1 and "mudou" in out_m and chamadas_de(cont2, "beta") == antes_chamadas
                  and ler(c2) == antes_r2,
                  "anterior alterado depois da rodada: retomar recusa com exit 1 e nao chama ninguem")
        bruto_ant.write_bytes(original)
        (r2 / ".consenso-lock").mkdir()
        code_l, out_l = retomar(r2, run2.name, env2)
        code_ld, out_ld = consenso(debate_base(r2, ["--agente", "alfa", "ag-alfa", "--agente", "beta", "ag-beta"]), env2)
        (r2 / ".consenso-lock").rmdir()
        res.check(code_l == 5 and "retomar" in out_l and run2.name in out_l
                  and code_ld == 5 and "retomar" in out_ld and run2.name in out_ld,
                  "lock ocupado: a mensagem cita o comando de retomada e o run-id (o proprio, ou o da rodada nao concluida)")
        log2 = tmp / "prompts-t2.txt"
        env2["LOG_PROMPT"] = str(log2)
        code_r, out_r = retomar(r2, run2.name, env2)
        prompt_r = (prompts(log2) or [""])[-1]
        novo2 = ler(c2)[len(antes_r2):]
        code_v2, linhas2, _ = validar(r2, "--strict", "--codigos")
        res.check(code_r == 0 and len(prompts(log2)) == 1 and "Rodada 2." in prompt_r
                  and "Anterior: alfa" in prompt_r and "TOKEN-ALFA-081" in prompt_r and "TOKEN-BETA-081" in prompt_r
                  and campo(novo2, "Rodada") == "2 de 2" and campo(novo2, "Exposicao previa a outras posicoes") == "sim"
                  and code_v2 == 0 and not linhas2,
                  "rodada 2 retomada: prompt refeito com os anteriores na integra e rotulados pelo id; passa em --strict",
                  "exit %s; %s" % (code_r, "; ".join(linhas2)[:100]))

        # 4. Achado interrompido: a entrada e reescrita so no fim, na retomada.
        ra, ca = montar_achado(tmp, "t4")
        env4, cont4 = ambiente_de(ra, "t4", LENTO="1")
        antes_a = ca.read_bytes()
        interromper(["achado", "--projeto", str(ra), "--entrada", TITULO_A, "--rodada", "2",
                     "--agente", "rev", "ag-rev", "--agente", "lento", "ag-lento"], env4, ["rev"])
        runa = rodadas(ra)[0] if rodadas(ra) else ra
        res.check(manifesto(runa).get("status") == "interrompida" and ca.read_bytes() == antes_a,
                  "achado interrompido: entrada byte a byte, manifesto interrompida")
        env4r, _ = ambiente_de(ra, "t4")
        code_a, out_a = retomar(ra, runa.name, env4r)
        ea = corpo(ler(ca))
        code_va, linhas_a, _ = validar(ra, "--strict", "--codigos")
        res.check(code_a == 0 and chamadas_de(cont4, "rev") == 1 and chamadas_de(cont4, "lento") == 2
                  and campo(ea, "Participantes") == "rev, lento" and campo(ea, "Rodada") == "2 de 2"
                  and citado(secao(ea, "Revalidacao De rev"), "TOKEN-REV-081")
                  and citado(secao(ea, "Revalidacao De lento"), "TOKEN-LENTO-081")
                  and manifesto(runa).get("status") == "concluida" and code_va == 0 and not linhas_a,
                  "achado retomado: so o lento e chamado, a entrada recebe as duas revalidacoes e passa em --strict",
                  "exit %s; %s" % (code_a, out_a.strip()[-100:]))

        # 5. Segredo: sem mover nada, o participante roda de novo e a varredura vale; movido a mao, e aceito.
        r5 = montar(tmp, "t5")
        (r5 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        env5, cont5 = ambiente_de(r5, "t5")
        c5 = r5 / "docs" / "CONSENSUS.md"
        antes5 = ler(c5)
        code, out = consenso(debate_base(r5, ["--agente", "alfa", "ag-alfa", "--agente", "vaza", "ag-vaza"]), env5)
        run5 = rodadas(r5)[0] if rodadas(r5) else r5
        code_s, out_s = retomar(r5, run5.name, env5)
        m5 = manifesto(run5)
        res.check(code == 6 and code_s == 6 and chamadas_de(cont5, "vaza") == 2 and chamadas_de(cont5, "alfa") == 1
                  and m5.get("status") == "parada-segredo" and ler(c5) == antes5
                  and "retomar" in out_s and run5.name in out_s,
                  "retido e nada movido: retomar chama o vaza de novo, a varredura para outra vez (exit 6), alfa fica")
        retido = Path(str(participante(m5, "vaza").get("retido_em") or ""))
        if retido.is_dir():
            shutil.copytree(str(retido), str(run5 / "vaza"), dirs_exist_ok=True)
        code_ok, out_ok = retomar(r5, run5.name, env5)
        m5 = manifesto(run5)
        pv = participante(m5, "vaza")
        res.check(code_ok == 0 and chamadas_de(cont5, "vaza") == 2 and pv.get("resultado") == "posicao"
                  and pv.get("aceito_por_humano") is True and "retido_em" not in pv
                  and pv.get("sha256_stdout") == sha256(run5 / "vaza" / "stdout.txt")
                  and (m5["retomadas"][-1].get("aceitos_a_mao") == ["vaza"])
                  and "TOKEN-VAZA-081" in (secao(ler(c5)[len(antes5):], "Posicao De vaza") or ""),
                  "material movido a mao: aceito como posicao sem nova chamada, registrado em aceitos_a_mao",
                  "exit %s; %s" % (code_ok, out_ok.strip()[-100:]))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Testa o primitivo de consenso com agente falso.")
    parser.add_argument("--verbose", action="store_true", help="Mostra tambem o que passou.")
    args = parser.parse_args(argv)

    res = Resultado(args.verbose)
    testar_primitivo(res)
    testar_lock_e_minuta(res)
    testar_varredura_de_segredo(res)
    testar_achado(res)
    testar_rodada_dois(res)
    testar_retomada(res)
    print("Modulo de consenso: %s/%s verificacoes passaram." % (res.total - res.falhas, res.total))
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
