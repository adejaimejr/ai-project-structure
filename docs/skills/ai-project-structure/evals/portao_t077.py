#!/usr/bin/env python3
"""Portao da T-077: varredura de segredo antes de gravar qualquer bruto (DEC-010).

1. Rodada com `limpo` e `vaza` (chave AWS e PEM): exit 6, material retido fora do projeto no
   caminho impresso, nenhuma copia do segredo dentro do projeto, manifesto marcando
   retido-por-segredo sem o conteudo, bruto de `limpo` gravado, CONSENSUS.md byte a byte, sem
   lock; 2. cada classe de padrao sozinha dispara (PEM, token ghp_, api_key=, URL com senha);
   3. rodada limpa que usa as palavras "chave de API" e "token" sem valor sai 0; 4. pergunta com
   segredo: exit 6 antes de chamar qualquer agente e sem bruto; 5. bateria >= 30; 6. versao;
   7. verificador.
"""

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (agente, ambiente, bateria_minimo, check, consenso, ler, manifesto,  # noqa: E402
                                 montar, participante, prompts, resumo, rodadas, verify_ok, versao_coerente)

CHAVE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"
PEM = "-----BEGIN RSA PRIVATE KEY-----"
GHP = "ghp_" + "Ab1" * 12
APIKEY = "Q7pL2mN9xV4cB8zK1wE5rT0y"
URL = "https://joao:senha123@exemplo.com/repo"
PERGUNTA = "Pergunta do portao T-077.\n\nTOKEN-PERGUNTA-077: qual opcao?\n"

AG_LIMPO = "echo 'Posicao limpa: a chave de API e o token nao aparecem aqui. TOKEN-LIMPO-077'\n"
AG_LIMPO2 = "echo 'Outra posicao limpa, falando de senha e de segredo sem valor nenhum. TOKEN-LIMPO2-077'\n"
AG_VAZA = f"echo 'achei no repositorio: {CHAVE_AWS}'\necho '{PEM}'\necho 'MIIEowIBAAKCAQEA'\necho '-----END RSA PRIVATE KEY-----'\n"
AG_PEM = f"echo '{PEM}'\necho 'MIIEowIBAAKCAQEA'\n"
AG_GHP = f"echo 'token: {GHP}'\n"
AG_APIKEY = f"echo 'api_key = \"{APIKEY}\"'\n"
AG_URL = f"echo 'veja {URL}'\n"


def contem_no_projeto(r, texto):
    for p in Path(r).rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            try:
                if texto in p.read_bytes().decode("utf-8", errors="replace"):
                    return p.relative_to(r).as_posix()
            except OSError:
                continue
    return None


def contem_na_arvore(base, texto):
    base = Path(base)
    if base.is_file():
        return texto in ler(base)
    return base.is_dir() and any(p.is_file() and texto in ler(p) for p in base.rglob("*"))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-limpo", AG_LIMPO), ("ag-limpo2", AG_LIMPO2), ("ag-vaza", AG_VAZA), ("ag-pem", AG_PEM),
                            ("ag-ghp", AG_GHP), ("ag-apikey", AG_APIKEY), ("ag-url", AG_URL)):
            agente(tmp, nome, corpo)
        env = ambiente(tmp)

        r = montar(tmp, "c1")
        (r / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        c = r / "docs" / "CONSENSUS.md"
        antes = c.read_bytes()
        code, out = consenso(["debate", "--projeto", str(r), "--pergunta", str(r / "pergunta.md"),
                              "--agente", "limpo", "ag-limpo", "--agente", "vaza", "ag-vaza"], env)
        runs = rodadas(r)
        m = manifesto(runs[0]) if runs else {}
        pv = participante(m, "vaza")
        retido = str(pv.get("retido_em") or "")
        manif_texto = ler(runs[0] / "manifesto.json") if runs and (runs[0] / "manifesto.json").is_file() else ""
        ok1 = (code == 6 and retido and retido in out and Path(retido).exists() and not retido.startswith(str(r))
               and contem_na_arvore(retido, CHAVE_AWS) and contem_no_projeto(r, CHAVE_AWS) is None
               and pv.get("resultado") == "retido-por-segredo" and CHAVE_AWS not in manif_texto
               and runs and (runs[0] / "limpo" / "stdout.txt").is_file() and c.read_bytes() == antes
               and not (r / ".consenso-lock").exists())
        check(ok1, "1. segredo no bruto: exit 6, material retido fora do projeto no caminho impresso, nada do segredo no projeto nem no manifesto, bruto limpo gravado, CONSENSUS.md intacto, sem lock",
              f"exit {code} retido_em={retido or '(vazio)'} no_projeto={contem_no_projeto(r, CHAVE_AWS)} resultado={pv.get('resultado')}")

        for rotulo, nome in (("PEM", "ag-pem"), ("token ghp_", "ag-ghp"), ("api_key =", "ag-apikey"), ("URL com senha", "ag-url")):
            rx = montar(tmp, "c-" + nome)
            (rx / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
            code, out = consenso(["debate", "--projeto", str(rx), "--pergunta", str(rx / "pergunta.md"),
                                  "--agente", "limpo", "ag-limpo", "--agente", "suspeito", nome], env)
            marca = {"ag-pem": PEM, "ag-ghp": GHP, "ag-apikey": APIKEY, "ag-url": "senha123"}[nome]
            check(code == 6 and contem_no_projeto(rx, marca) is None,
                  f"2. padrao {rotulo} sozinho dispara: exit 6 e nada gravado no projeto", f"exit {code}")

        r3 = montar(tmp, "c3")
        (r3 / "pergunta.md").write_text(PERGUNTA, encoding="utf-8")
        code, out = consenso(["debate", "--projeto", str(r3), "--pergunta", str(r3 / "pergunta.md"),
                              "--agente", "limpo", "ag-limpo", "--agente", "limpo2", "ag-limpo2"], env)
        check(code == 0, "3. rodada limpa que cita as palavras chave de API, token, senha e segredo sem valor sai 0", f"exit {code}; {out.strip()[-120:]}")

        r4 = montar(tmp, "c4")
        (r4 / "pergunta.md").write_text(PERGUNTA + f"\nContexto: o repositorio usa {URL} para clonar.\n", encoding="utf-8")
        log4 = tmp / "prompts-c4.txt"
        code, out = consenso(["debate", "--projeto", str(r4), "--pergunta", str(r4 / "pergunta.md"),
                              "--agente", "limpo", "ag-limpo", "--agente", "limpo2", "ag-limpo2"], ambiente(tmp, LOG_PROMPT=log4))
        brutos = [p for run in rodadas(r4) for p in run.rglob("stdout.txt")]
        check(code == 6 and not prompts(log4) and not brutos and contem_no_projeto(r4 / "docs", "senha123") is None,
              "4. pergunta com segredo: exit 6 antes de chamar qualquer agente, sem bruto e sem copia do segredo em docs/",
              f"exit {code} prompts={len(prompts(log4))} brutos={len(brutos)}")

    ok, det = bateria_minimo(30)
    check(ok, "5. bateria test_consenso.py com pelo menos 30 verificacoes", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "6. versao 2.11.0 ou acima, coerente", det)
    ok, det = verify_ok()
    check(ok, "7. verify_repository.py exit 0", det)
    return resumo("T-077")


if __name__ == "__main__":
    sys.exit(main())
