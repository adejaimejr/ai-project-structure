#!/usr/bin/env python3
"""Portao da T-079: pacote de achado, revalidacao dentro da entrada existente.

1. `consenso.py achado --entrada <titulo> --rodada 2` com um revisor: exit 0, secao
   `### Revalidacao De revisor` em citacao, campos atualizados (Rodada 2 de 2, Exposicao sim,
   Metodo, Origem, Manifesto, Participantes, Falhas, Proximo passo com o dono, Status intacto),
   Disposicao, entrada de controle e resto do arquivo byte a byte; 2. o revisor ve a entrada-alvo
   na copia e a recebe na integra no prompt; 3. --strict limpo depois; 4. entrada inexistente,
   sem --rodada ou rodada 4 sem --pendente: exit 1 e nada muda; com --pendente a linha entra;
   5. id repetido recusado; id novo acrescenta as listas; 6. N=1 aceito, manifesto modo=achado
   com a entrada; 7. revisor unico falhando: exit 2 e entrada intacta; 8. bateria >= 40;
   9. versao; 10. verificador.
"""

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (agente, ambiente, bateria_minimo, campo, check, citado, consenso,  # noqa: E402
                                 corpo_da_entrada, entrada_de_debate, ler, manifesto, montar, resumo,
                                 rodadas, secao, validar, verify_ok, versao_coerente)

TITULO = "2026-09-01 - Achado X-1 de teste"
ACHADO = f"""
## {TITULO}

**Achado:** X-1

**Status:** aberto

**Proximo passo:** revalidar com outro modelo

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Escapou de verificacao:** nao

### Contexto

- contexto do achado.

### O Que Foi Encontrado

- o defeito.

### Disposicao

- DISPOSICAO-TOKEN-079: manter a fixture e cobrir com oracle.

### Revalidacao

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)
"""
CONTROLE = entrada_de_debate("2026-09-02", "Debate de controle TOKEN-CONTROLE-079")

AG_REVISOR = r'''
if grep -q "DISPOSICAO-TOKEN-079" docs/CONSENSUS.md 2>/dev/null; then echo VEJO-ALVO; fi
echo "Parecer do revisor: TOKEN-REVISOR-079, a disposicao se sustenta."
'''
AG_REVISOR2 = "echo 'Segundo parecer TOKEN-REVISOR2-079'\n"
AG_FALHO = "echo 'cota esgotada' >&2\nexit 4\n"


def preparar(tmp, nome):
    r = montar(tmp, nome)
    c = r / "docs" / "CONSENSUS.md"
    c.write_text(ler(c) + ACHADO + CONTROLE, encoding="utf-8")
    return r, c


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, corpo in (("ag-revisor", AG_REVISOR), ("ag-revisor2", AG_REVISOR2), ("ag-falho", AG_FALHO)):
            agente(tmp, nome, corpo)
        env = ambiente(tmp)

        r, c = preparar(tmp, "c1")
        antes = ler(c)
        e_antes = corpo_da_entrada(antes, TITULO)
        code, out = consenso(["achado", "--projeto", str(r), "--entrada", TITULO, "--rodada", "2",
                              "--agente", "revisor", "ag-revisor", "--dono", "fulano"], env)
        depois = ler(c)
        e = corpo_da_entrada(depois, TITULO) or ""
        manif = campo(e, "Manifesto") or ""
        ok1 = (code == 0 and citado(secao(e, "Revalidacao De revisor"), "TOKEN-REVISOR-079")
               and campo(e, "Rodada") == "2 de 2" and campo(e, "Exposicao previa a outras posicoes") == "sim"
               and campo(e, "Metodo") == "pareceres-independentes" and campo(e, "Origem") == "automacao"
               and manif and (r / manif).is_file() and campo(e, "Participantes") == "revisor" and campo(e, "Falhas") == "nenhuma"
               and "fulano" in (campo(e, "Proximo passo") or "") and campo(e, "Status") == "aberto"
               and campo(e, "Achado") == "X-1" and campo(e, "Escapou de verificacao") == "nao"
               and secao(e, "Disposicao") == secao(e_antes, "Disposicao")
               and corpo_da_entrada(depois, "2026-09-02 - Debate de controle TOKEN-CONTROLE-079") == corpo_da_entrada(antes, "2026-09-02 - Debate de controle TOKEN-CONTROLE-079")
               and depois.replace(e, "") == antes.replace(e_antes, ""))
        check(ok1, "1. revalidacao entra na entrada existente com os campos atualizados; Disposicao, controle e resto do arquivo byte a byte",
              f"exit {code} rodada={campo(e, 'Rodada')} exp={campo(e, 'Exposicao previa a outras posicoes')} part={campo(e, 'Participantes')} manifesto={manif} status={campo(e, 'Status')}")

        runs = rodadas(r)
        run = runs[0] if runs else r
        saida = ler(run / "revisor" / "stdout.txt") if (run / "revisor" / "stdout.txt").is_file() else ""
        prompt = ler(run / "revisor" / "prompt.txt") if (run / "revisor" / "prompt.txt").is_file() else ""
        check("VEJO-ALVO" in saida and "DISPOSICAO-TOKEN-079" in prompt and TITULO in prompt,
              "2. o revisor ve a entrada-alvo no CONSENSUS.md da copia e a recebe na integra no prompt",
              f"stdout={saida.strip()[:60]!r} prompt={len(prompt)} bytes")
        code_v, linhas, _ = validar(r, "--strict", "--codigos")
        check(code_v == 0 and not linhas, "3. --strict limpo depois da revalidacao", "; ".join(linhas)[:160])

        m = manifesto(run)
        check(m.get("modo") == "achado" and m.get("entrada") == TITULO and len(m.get("participantes", [])) == 1,
              "6. N=1 aceito; manifesto com modo=achado e a entrada-alvo", f"modo={m.get('modo')} entrada={m.get('entrada')}")

        # 5: id repetido recusado; id novo acrescenta.
        antes5 = ler(c)
        code_rep, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO, "--rodada", "3", "--agente", "revisor", "ag-revisor2"], env)
        check(code_rep == 1 and ler(c) == antes5, "5a. id que ja tem secao na entrada e recusado com exit 1, sem mudar o arquivo", f"exit {code_rep}")
        code_novo, _ = consenso(["achado", "--projeto", str(r), "--entrada", TITULO, "--rodada", "3", "--agente", "revisor2", "ag-revisor2"], env)
        e3 = corpo_da_entrada(ler(c), TITULO) or ""
        manifs = [x.strip() for x in (campo(e3, "Manifesto") or "").split(",") if x.strip()]
        check(code_novo == 0 and campo(e3, "Participantes") == "revisor, revisor2" and len(manifs) == 2 and all((r / x).is_file() for x in manifs)
              and citado(secao(e3, "Revalidacao De revisor2"), "TOKEN-REVISOR2-079") and citado(secao(e3, "Revalidacao De revisor"), "TOKEN-REVISOR-079")
              and campo(e3, "Rodada") == "3 de 3",
              "5b. id novo acrescenta secao, Participantes e o segundo manifesto, mantendo a revalidacao anterior",
              f"exit {code_novo} part={campo(e3, 'Participantes')} manifestos={manifs} rodada={campo(e3, 'Rodada')}")

        # 4: elegibilidade.
        r4, c4 = preparar(tmp, "c4")
        antes4 = ler(c4)
        code_a, _ = consenso(["achado", "--projeto", str(r4), "--entrada", "2026-09-01 - Nao existe", "--rodada", "2", "--agente", "revisor", "ag-revisor"], env)
        code_b, _ = consenso(["achado", "--projeto", str(r4), "--entrada", TITULO, "--agente", "revisor", "ag-revisor"], env)
        code_c, _ = consenso(["achado", "--projeto", str(r4), "--entrada", TITULO, "--rodada", "4", "--agente", "revisor", "ag-revisor"], env)
        check(code_a == 1 and code_b == 1 and code_c == 1 and ler(c4) == antes4 and not rodadas(r4),
              "4a. entrada inexistente, sem --rodada, ou rodada 4 sem --pendente: exit 1, nada muda, sem run dir",
              f"exits {code_a} {code_b} {code_c}")
        code_d, _ = consenso(["achado", "--projeto", str(r4), "--entrada", TITULO, "--rodada", "4", "--pendente", "ficou aberto o oracle",
                              "--agente", "revisor", "ag-revisor"], env)
        e4 = corpo_da_entrada(ler(c4), TITULO) or ""
        code_v4, linhas4, _ = validar(r4, "--strict", "--codigos")
        check(code_d == 0 and campo(e4, "Pendente da rodada anterior") == "ficou aberto o oracle" and campo(e4, "Rodada") == "4 de 4" and code_v4 == 0,
              "4b. rodada 4 com --pendente: linha Pendente da rodada anterior com o texto humano, --strict limpo",
              f"exit {code_d} pendente={campo(e4, 'Pendente da rodada anterior')} strict={code_v4} {'; '.join(linhas4)[:80]}")

        # 7: revisor unico falhando.
        r7, c7 = preparar(tmp, "c7")
        antes7 = c7.read_bytes()
        code, out = consenso(["achado", "--projeto", str(r7), "--entrada", TITULO, "--rodada", "2", "--agente", "revisor", "ag-falho"], env)
        runs7 = rodadas(r7)
        check(code == 2 and c7.read_bytes() == antes7 and runs7 and (runs7[0] / "revisor" / "stderr.txt").is_file(),
              "7. revisor unico falhando: exit 2, entrada byte a byte, run dir com a falha", f"exit {code}")

    ok, det = bateria_minimo(40)
    check(ok, "8. bateria test_consenso.py com pelo menos 40 verificacoes", det)
    versao, ok, _, det = versao_coerente("2.11.0")
    check(ok, "9. versao 2.11.0 ou acima, coerente", det)
    ok, det = verify_ok()
    check(ok, "10. verify_repository.py exit 0", det)
    return resumo("T-079")


if __name__ == "__main__":
    sys.exit(main())
