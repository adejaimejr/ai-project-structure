#!/usr/bin/env python3
"""Orquestra uma rodada mecanica de pareceres independentes.

Cada participante trabalha numa copia temporaria do projeto, fora dele, sem
`docs/consensus/`. O bruto e o manifesto entram no sidecar in-repo assim que
cada agente termina. Havendo posicao, a minuta entra no fim de CONSENSUS.md
por substituicao atomica, com julgamento em branco. `retomar` continua uma rodada nao
concluida por comando explicito, sem repetir o que ja foi pago.

Somente biblioteca padrao (Python 3.8+).
"""

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

EXCLUIDOS_DA_COPIA = ["docs/consensus/", ".consenso-lock", "__pycache__/"]
IDS_RESERVADOS = {".", ".."}
TRAVESSAO = "\u2014"
LOCK_NOME = ".consenso-lock"

# Padroes minimos da T-077 / DEC-010. Palavra solta sem valor nao casa.
_RE_AWS = re.compile(r"AKIA[A-Z0-9]{16}")
_RE_PEM = re.compile(r"-----BEGIN[^\n]{0,80}PRIVATE KEY-----")
_RE_ROTULO = re.compile(
    r"(?i)(?:api_key|apikey|\btoken\b|\bsecret\b|\bpassword\b)\s*[=:]\s*\S{16,}"
)
# Prefixos exigem inicio de palavra e comprimento minimo: `sk-` solto casava
# `task-force`, `risk-based` e `desk-top` (falso positivo visto na revisao de T-077).
_RE_GHP = re.compile(r"\bghp_[A-Za-z0-9]{16,}")
_RE_SK = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")
_RE_XOX = re.compile(r"\bxox[A-Za-z]-[A-Za-z0-9-]{8,}")
_RE_URL = re.compile(r"://[^/\s:]+:[^/\s@]+@")
PADROES_SEGREDO = (_RE_AWS, _RE_PEM, _RE_ROTULO, _RE_GHP, _RE_SK, _RE_XOX, _RE_URL)

# Estado da rodada corrente, para o handler de sinal enxergar os processos.
_interrompendo = threading.Event()
_processos_lock = threading.Lock()
_processos_vivos = []


def tem_segredo(texto):
    """True se o texto casa algum padrao minimo de segredo da T-077."""
    if texto is None:
        return False
    if isinstance(texto, bytes):
        texto = texto.decode("utf-8", "replace")
    if not texto:
        return False
    return any(padrao.search(texto) for padrao in PADROES_SEGREDO)


def reter_bruto_fora(stdout, stderr):
    """Guarda stdout e stderr fora do projeto. Nunca redige. Devolve o caminho."""
    destino = Path(tempfile.mkdtemp(prefix="consenso-retido-"))
    if not isinstance(stdout, bytes):
        stdout = stdout.encode("utf-8")
    if not isinstance(stderr, bytes):
        stderr = stderr.encode("utf-8")
    (destino / "stdout.txt").write_bytes(stdout)
    (destino / "stderr.txt").write_bytes(stderr)
    return destino


def comando_de_retomada(projeto, run_id):
    return 'consenso.py retomar --projeto "%s" %s' % (projeto, run_id)


def avisar_retido(retido, projeto, run_id, identificador):
    print("Material retido por padrao de segredo: %s" % retido, file=sys.stderr)
    print("Conferir o material nesse diretorio.", file=sys.stderr)
    print("Para aceitar como esta, mova o diretorio para docs/consensus/%s/%s/."
          % (run_id, identificador), file=sys.stderr)
    print("Para descartar, apague. Depois: %s" % comando_de_retomada(projeto, run_id),
          file=sys.stderr)


def agora():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def soma(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def soma_texto(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def escrever_json(caminho, dados):
    """Grava o manifesto por substituicao atomica no mesmo diretorio."""
    escrever_bytes_atomico(caminho, json.dumps(dados, ensure_ascii=False, indent=2) + "\n")


def escrever_bytes_atomico(caminho, dados):
    """Temporario no mesmo diretorio, fsync e os.replace. Limpa o temporario."""
    caminho = Path(caminho)
    if isinstance(dados, str):
        dados = dados.encode("utf-8")
    temporario = caminho.parent / (".%s.%s.tmp" % (caminho.name, os.getpid()))
    try:
        with temporario.open("wb") as arquivo:
            arquivo.write(dados)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(str(temporario), str(caminho))
    finally:
        if temporario.exists():
            temporario.unlink()


def ignorar_copia(projeto):
    projeto = Path(projeto).resolve()

    def ignorar(atual, nomes):
        removidos = {nome for nome in nomes if nome in {LOCK_NOME, "__pycache__"}}
        try:
            rel = Path(atual).resolve().relative_to(projeto)
        except ValueError:
            return removidos
        if rel.as_posix() == "docs" and "consensus" in nomes:
            removidos.add("consensus")
        return removidos

    return ignorar


def reter_registros(copia):
    """Esconde as entradas anteriores; os modelos cercados acima ficam."""
    caminho = Path(copia) / "docs" / "CONSENSUS.md"
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError:
        return
    marcador = "## Registros"
    inicio = texto.find(marcador)
    if inicio < 0:
        return
    nota = (
        "## Registros\n\n"
        "> As entradas anteriores foram retidas de proposito por esta operacao.\n"
    )
    caminho.write_text(texto[:inicio] + nota, encoding="utf-8")


def prompt_do_participante(pergunta, participante, copia, rodada_n=1, anteriores=()):
    """Rodada 1 e cega. Da rodada 2 em diante o prompt leva as posicoes anteriores inteiras,
    depois da pergunta, cada uma exatamente como veio: resumo ali seria regressao (DEC-006)."""
    base = (
        "Participante: %s\n"
        "Copia isolada do projeto: %s\n"
        "Esta e uma copia somente-leitura do projeto: leia o que precisar. "
        "Nao edite nada fora da sua resposta.\n"
        "Responda em portugues, sem travessao. A resposta inteira no stdout "
        "sera reproduzida sem resumo. Nenhuma posicao contemporanea %sesta "
        "disponivel por construcao.\n\n"
    ) % (participante, copia, "" if rodada_n == 1 else "desta rodada ")
    if rodada_n == 1:
        return base + "Pergunta:\n\n%s" % pergunta
    partes = [
        base,
        "Rodada %d. As posicoes anteriores estao no fim deste prompt, na integra, "
        "exatamente como foram dadas; nada foi resumido. As entradas publicadas estao em "
        "docs/CONSENSUS.md da copia. Responda a pergunta levando-as em conta e diga o que "
        "mudou em relacao a elas.\n\n" % rodada_n,
        "Pergunta:\n\n%s\n\nPosicoes anteriores (na integra):\n" % pergunta,
    ]
    for rotulo, caminho, texto in anteriores:
        partes.append("\n----- Anterior: %s (%s) -----\n" % (rotulo, caminho))
        partes.append(texto)
        partes.append("\n" if not texto.endswith("\n") else "")
        partes.append("----- Fim de %s -----\n" % rotulo)
    return "".join(partes)


def executa(comando, prompt, copia):
    inicio = agora()
    try:
        processo = subprocess.Popen(
            comando + [prompt],
            cwd=str(copia),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as erro:
        return inicio, agora(), 127, b"", str(erro).encode("utf-8", "replace")
    with _processos_lock:
        _processos_vivos.append(processo)
    if _interrompendo.is_set():
        try:
            processo.terminate()
        except OSError:
            pass
    stdout, stderr = processo.communicate()
    with _processos_lock:
        if processo in _processos_vivos:
            _processos_vivos.remove(processo)
    return inicio, agora(), processo.returncode, stdout, stderr


def ao_sinal(signum, _frame):
    _interrompendo.set()
    with _processos_lock:
        alvos = list(_processos_vivos)
    for processo in alvos:
        try:
            processo.terminate()
        except OSError:
            pass
    # SIGINT: nao deixa o KeyboardInterrupt default furar o finally.
    if signum == signal.SIGINT:
        return


def sidecar_ignorado(projeto):
    """True quando o git trata docs/consensus/ como ignorado (DEC-008)."""
    if not (projeto / ".git").exists():
        return False
    processo = subprocess.run(
        ["git", "-C", str(projeto), "check-ignore", "-q", "docs/consensus/"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return processo.returncode == 0


def id_inseguro(identificador):
    if not identificador or identificador in IDS_RESERVADOS:
        return True
    return "/" in identificador or "\\" in identificador or os.sep in identificador


def rodadas_nao_concluidas(projeto):
    """Run-ids em docs/consensus/ cujo manifesto nao esta `concluida`, mais antigos primeiro."""
    base = Path(projeto) / "docs" / "consensus"
    saida = []
    if not base.is_dir():
        return saida
    for pasta in sorted(base.iterdir()):
        try:
            dados = json.loads((pasta / "manifesto.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(dados, dict) and dados.get("status") != "concluida":
            saida.append(pasta.name)
    return saida


def adquirir_lock(projeto, run_id=None):
    lock_dir = Path(projeto) / LOCK_NOME
    try:
        os.mkdir(str(lock_dir))
    except FileExistsError:
        print("[ERRO] outra rodada ja esta em andamento neste projeto: lock em %s."
              % lock_dir, file=sys.stderr)
        print("Se uma rodada anterior terminou de forma inesperada e voce confirmou que",
              file=sys.stderr)
        print("nao ha rodada ativa, limpe o lock orfao com: rmdir \"%s\"" % lock_dir,
              file=sys.stderr)
        # Retomada e palavra humana: a mensagem so mostra o comando, nunca o executa.
        for pendente in ([run_id] if run_id else rodadas_nao_concluidas(projeto)[-3:]):
            print("Para continuar a rodada %s depois disso: %s"
                  % (pendente, comando_de_retomada(projeto, pendente)), file=sys.stderr)
        return None
    except OSError as erro:
        print("[ERRO] nao foi possivel criar o lock da rodada em %s: %s"
              % (lock_dir, erro), file=sys.stderr)
        return None
    return lock_dir


def soltar_lock(lock_dir):
    if lock_dir is None:
        return
    try:
        os.rmdir(str(lock_dir))
    except OSError:
        pass


def citar(texto):
    """Toda linha vira citacao Markdown; U+2014 vira hifen. Devolve (bloco, n)."""
    if texto is None:
        texto = ""
    n = texto.count(TRAVESSAO)
    texto = texto.replace(TRAVESSAO, "-")
    linhas = texto.splitlines()
    if not linhas:
        return "> \n", n
    return "\n".join("> " + linha for linha in linhas) + "\n", n


def montar_minuta(titulo, dono, run_id, pergunta, participantes, data, rodada_n=1, pendente=""):
    ids = [p["id"] for p in participantes]
    falhos = [p["id"] for p in participantes if p.get("resultado") != "posicao"]
    falhas_txt = ", ".join(falhos) if falhos else "nenhuma"
    manifesto_rel = "docs/consensus/%s/manifesto.json" % run_id
    partes = [
        "## %s - %s" % (data, titulo),
        "",
        "**Status:** aberto",
        "",
        "**Proximo passo:** %s le as posicoes e preenche as secoes de julgamento" % dono,
        "",
        "**Metodo:** pareceres-independentes",
        "",
        "**Exposicao previa a outras posicoes:** %s" % ("nao" if rodada_n == 1 else "sim"),
        "",
        "**Rodada:** %d de %d" % (rodada_n, rodada_n),
        "",
    ]
    if pendente:
        partes.extend(["**Pendente da rodada anterior:** %s" % pendente, ""])
    partes += [
        "**Origem:** automacao",
        "",
        "**Manifesto:** %s" % manifesto_rel,
        "",
        "**Participantes:** %s" % ", ".join(ids),
        "",
        "**Falhas:** %s" % falhas_txt,
        "",
        "### Contexto",
        "",
        "- Modo: debate",
        "- Rodada: %d de %d" % (rodada_n, rodada_n),
        "- N: %s" % len(ids),
        "- Data: %s" % data,
        "- Manifesto: %s" % manifesto_rel,
        "",
        "### Pergunta Ou Decisao",
        "",
        citar(pergunta)[0].rstrip("\n"),
        "",
    ]
    for p in participantes:
        if p.get("resultado") == "posicao":
            partes.extend(secao_de_posicao("Posicao De", p["id"], p.get("_stdout_texto", "")) + [""])
        else:
            partes.extend(secao_de_falha(run_id, p) + [""])
    for secao in (
        "Pontos De Acordo",
        "Riscos E Tradeoffs",
        "Consenso Final",
        "Decisao Para Registrar Em DECISIONS.md",
    ):
        partes.extend(["### %s" % secao, "", "- (A preencher.)", ""])
    return "\n".join(partes).rstrip() + "\n"


def gravar_minuta(projeto, minuta):
    """Acrescenta a minuta no fim, sem alterar o prefixo. Devolve hashes e o texto."""
    caminho = Path(projeto) / "docs" / "CONSENSUS.md"
    antes = caminho.read_text(encoding="utf-8")
    sha_antes = soma_texto(antes)
    adendo = ""
    if antes and not antes.endswith("\n"):
        adendo += "\n"
    adendo += "\n" + minuta.lstrip("\n")
    depois = antes + adendo
    escrever_bytes_atomico(caminho, depois.encode("utf-8"))
    return sha_antes, soma(caminho), "docs/CONSENSUS.md"




def abrir_rodada(projeto, sufixo):
    """Cria docs/consensus/<instante>-<sufixo>, com -2, -3 se a pasta ja existe.

    Duas rodadas no mesmo segundo (achado em sequencia) nao podem se atropelar.
    Devolve (run_id, caminho) ou None se nao deu para criar."""
    base = Path(projeto) / "docs" / "consensus"
    run_id = "%s-%s" % (dt.datetime.now().strftime("%Y-%m-%d-%H%M%S"), sufixo)
    try:
        base.mkdir(parents=True, exist_ok=True)
    except OSError as erro:
        print("[ERRO] nao foi possivel criar sidecar: %s" % erro, file=sys.stderr)
        return None
    candidato, n = run_id, 1
    while True:
        try:
            (base / candidato).mkdir()
            return candidato, base / candidato
        except FileExistsError:
            n += 1
            candidato = "%s-%d" % (run_id, n)
        except OSError as erro:
            print("[ERRO] nao foi possivel criar sidecar: %s" % erro, file=sys.stderr)
            return None


def novo_manifesto(modo, rodada_n, run_id, projeto, pergunta_arquivo):
    return {
        "versao": 1,
        "run_id": run_id,
        "modo": modo,
        "rodada": rodada_n,
        "projeto": str(projeto),
        "inicio": agora(),
        "fim": None,
        "status": "em-andamento",
        "pergunta": ({"arquivo": str(pergunta_arquivo), "sha256": soma(pergunta_arquivo)}
                     if pergunta_arquivo else None),
        "excluidos_da_copia": list(EXCLUIDOS_DA_COPIA),
        "participantes": [],
        "minuta": None,
    }


def com_lock_e_sinais(projeto, funcao, run_id=None):
    """Lock exclusivo por projeto e tratamento de SIGINT/SIGTERM em volta de `funcao`."""
    lock_dir = adquirir_lock(projeto, run_id)
    if lock_dir is None:
        return 5
    anteriores = {
        signal.SIGINT: signal.getsignal(signal.SIGINT),
        signal.SIGTERM: signal.getsignal(signal.SIGTERM),
    }
    _interrompendo.clear()
    with _processos_lock:
        _processos_vivos.clear()
    try:
        signal.signal(signal.SIGINT, ao_sinal)
        signal.signal(signal.SIGTERM, ao_sinal)
        return funcao()
    finally:
        for sig, handler in anteriores.items():
            try:
                signal.signal(sig, handler)
            except (OSError, ValueError):
                pass
        soltar_lock(lock_dir)


def rodar_participantes(projeto, rodada, run_id, manifesto, trabalhos_cmd, prompt_de, reter):
    """Primitivo comum a debate e achado: uma copia isolada por participante, execucao
    em paralelo, bruto e manifesto gravados assim que cada um encerra, varredura de
    segredo antes de gravar. `reter` esconde as entradas anteriores de CONSENSUS.md na
    copia (debate); achado a deixa inteira, porque a entrada sob revisao e o objeto
    (DEC-003). Devolve {id: stdout} de quem terminou sem reter por segredo."""
    stdout_por_id = {}
    temporarios = []
    trabalhos = []
    try:
        for identificador, comando in trabalhos_cmd:
            if _interrompendo.is_set():
                break
            raiz_temporaria = Path(tempfile.mkdtemp(prefix="consenso-"))
            temporarios.append(raiz_temporaria)
            copia = raiz_temporaria / "projeto"
            shutil.copytree(str(projeto), str(copia), ignore=ignorar_copia(projeto))
            if reter:
                reter_registros(copia)
            trabalhos.append((identificador, comando, str(copia), prompt_de(identificador, str(copia))))

        if trabalhos and not _interrompendo.is_set():
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(trabalhos)) as executor:
                futuros = {
                    executor.submit(executa, comando, prompt, copia): (
                        identificador, comando, copia, prompt)
                    for identificador, comando, copia, prompt in trabalhos
                }
                for futuro in concurrent.futures.as_completed(futuros):
                    identificador, comando, copia, prompt = futuros[futuro]
                    inicio, fim, codigo, stdout, stderr = futuro.result()
                    if _interrompendo.is_set() and codigo != 0:
                        # Morto pelo nosso sinal: nao ha bruto a guardar. Sem registro e sem
                        # stdout.txt, a retomada chama este participante de novo.
                        continue
                    destino = rodada / identificador
                    destino.mkdir(exist_ok=True)
                    prompt_path = destino / "prompt.txt"
                    prompt_path.write_text(prompt, encoding="utf-8")
                    if tem_segredo(stdout) or tem_segredo(stderr):
                        retido = reter_bruto_fora(stdout, stderr)
                        avisar_retido(retido, projeto, run_id, identificador)
                        registro = {
                            "id": identificador,
                            "comando": comando,
                            "diretorio": copia,
                            "inicio": inicio,
                            "fim": fim,
                            "exit": codigo,
                            "prompt": "%s/prompt.txt" % identificador,
                            "sha256_prompt": soma(prompt_path),
                            "resultado": "retido-por-segredo",
                            "retido_em": str(retido),
                        }
                        manifesto["participantes"].append(registro)
                        escrever_json(rodada / "manifesto.json", manifesto)
                        continue
                    stdout_path = destino / "stdout.txt"
                    stderr_path = destino / "stderr.txt"
                    stdout_path.write_bytes(stdout)
                    stderr_path.write_bytes(stderr)
                    stdout_texto = stdout.decode("utf-8", "replace")
                    stdout_por_id[identificador] = stdout_texto
                    registro = {
                        "id": identificador,
                        "comando": comando,
                        "diretorio": copia,
                        "inicio": inicio,
                        "fim": fim,
                        "exit": codigo,
                        "prompt": "%s/prompt.txt" % identificador,
                        "sha256_prompt": soma(prompt_path),
                        "stdout": "%s/stdout.txt" % identificador,
                        "sha256_stdout": soma(stdout_path),
                        "stderr": "%s/stderr.txt" % identificador,
                        "resultado": "posicao" if codigo == 0 else "falha",
                        "travessoes_substituidos": stdout_texto.count(TRAVESSAO),
                    }
                    manifesto["participantes"].append(registro)
                    escrever_json(rodada / "manifesto.json", manifesto)
    finally:
        for temporario in temporarios:
            shutil.rmtree(str(temporario), ignore_errors=True)
    return stdout_por_id


def marcar_interrompida(manifesto, rodada, run_id):
    manifesto["status"] = "interrompida"
    escrever_json(rodada / "manifesto.json", manifesto)
    print("Rodada interrompida: %s" % run_id, file=sys.stderr)
    print("Para continuar sem repetir o que ja foi pago: %s"
          % comando_de_retomada(manifesto["projeto"], run_id), file=sys.stderr)
    return 1


def fechar_sem_minuta(manifesto, rodada, run_id, participantes):
    """Estados que terminam sem escrever em CONSENSUS.md: interrompida (1), parada por
    segredo (6) e sem nenhuma posicao (2). Devolve o exit, ou None se ha o que escrever."""
    ordem = {identificador: indice for indice, (identificador, _) in enumerate(participantes)}
    manifesto["participantes"].sort(key=lambda p: ordem.get(p["id"], 999))
    manifesto["fim"] = agora()
    if _interrompendo.is_set():
        return marcar_interrompida(manifesto, rodada, run_id)
    if any(p.get("resultado") == "retido-por-segredo" for p in manifesto["participantes"]):
        manifesto["status"] = "parada-segredo"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada parada por segredo: %s" % run_id, file=sys.stderr)
        print("Depois de conferir o material retido: %s"
              % comando_de_retomada(manifesto["projeto"], run_id), file=sys.stderr)
        return 6
    if not any(p["resultado"] == "posicao" for p in manifesto["participantes"]):
        manifesto["status"] = "sem-posicao"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada sem posicao: %s" % run_id, file=sys.stderr)
        return 2
    return None


def validar_participantes(participantes, modo, minimo):
    """Devolve a lista de (id, comando) ou imprime o erro e devolve None."""
    if len(participantes) < minimo:
        print("[ERRO] %s exige pelo menos %s --agente." % (modo, "um" if minimo == 1 else "dois"),
              file=sys.stderr)
        return None
    ids = [par[0] for par in participantes]
    if len(set(ids)) != len(ids) or any(id_inseguro(i) for i in ids):
        print("[ERRO] ids de participantes precisam ser distintos e seguros para diretorio.",
              file=sys.stderr)
        return None
    trabalhos_cmd = []
    for identificador, texto_comando in participantes:
        comando = texto_comando.split()
        if not comando:
            print("[ERRO] comando vazio para %s." % identificador, file=sys.stderr)
            return None
        trabalhos_cmd.append((identificador, comando))
    return trabalhos_cmd


def carregar_anteriores(projeto, caminhos):
    """[(rotulo, caminho, texto, sha256)] ou (None, motivo).

    Arquivo entra inteiro, rotulado pelo nome. Diretorio de rodada entra com todo
    `<id>/stdout.txt`, rotulado pelo id. O texto e o dos bytes lidos, sem resumo, sem corte."""
    saida = []

    def ler_um(rotulo, arquivo):
        dados = arquivo.read_bytes()
        try:
            rel = arquivo.relative_to(projeto).as_posix()
        except ValueError:
            rel = str(arquivo)
        saida.append((rotulo, rel, dados.decode("utf-8", "replace"), hashlib.sha256(dados).hexdigest(),
                      tem_segredo(dados)))

    for bruto in caminhos:
        caminho = Path(bruto).resolve()
        try:
            if caminho.is_file():
                ler_um(caminho.name, caminho)
            elif caminho.is_dir():
                achados = sorted(d for d in caminho.iterdir() if (d / "stdout.txt").is_file())
                if not achados:
                    return None, "--anterior %s e um diretorio sem nenhum <id>/stdout.txt." % bruto
                for d in achados:
                    ler_um(d.name, d / "stdout.txt")
            else:
                return None, "--anterior nao encontrado: %s" % bruto
        except OSError as erro:
            return None, "--anterior ilegivel: %s (%s)" % (bruto, erro)
    return saida, None


def run_debate(args):
    projeto = Path(args.projeto).resolve()
    pergunta_arquivo = Path(args.pergunta).resolve()
    participantes = args.agente or []
    if not projeto.is_dir():
        print("[ERRO] projeto nao encontrado: %s" % projeto, file=sys.stderr)
        return 1
    if not pergunta_arquivo.is_file():
        print("[ERRO] pergunta nao encontrada: %s" % pergunta_arquivo, file=sys.stderr)
        return 1
    trabalhos_cmd = validar_participantes(participantes, "debate", 2)
    if trabalhos_cmd is None:
        return 1
    try:
        rodada_n = int(args.rodada)
    except (TypeError, ValueError):
        print("[ERRO] --rodada precisa ser um numero inteiro.", file=sys.stderr)
        return 1
    if rodada_n < 1:
        print("[ERRO] --rodada precisa ser 1 ou mais.", file=sys.stderr)
        return 1
    pendente = linha_unica(args.pendente)
    caminhos_anteriores = args.anterior or []
    # A operacao nunca deduz a rodada nem quais posicoes anteriores fornecer (DEC-006).
    if rodada_n == 1 and (caminhos_anteriores or pendente):
        print("[ERRO] a rodada 1 e cega: --anterior e --pendente so valem da rodada 2 em diante.",
              file=sys.stderr)
        return 1
    if rodada_n >= 2 and not caminhos_anteriores:
        print("[ERRO] a rodada %d exige pelo menos um --anterior: a operacao nao deduz quais "
              "posicoes anteriores fornecer." % rodada_n, file=sys.stderr)
        return 1
    if rodada_n > RODADAS_SEM_PENDENCIA and not pendente:
        print("[ERRO] a rodada %d exige --pendente: o texto de '**Pendente da rodada anterior:**' "
              "e humano, o script nao inventa." % rodada_n, file=sys.stderr)
        return 1
    anteriores, motivo = carregar_anteriores(projeto, caminhos_anteriores)
    if anteriores is None:
        print("[ERRO] %s" % motivo, file=sys.stderr)
        return 1
    if sidecar_ignorado(projeto):
        print("[ERRO] docs/consensus/ esta ignorado pelo git; remova essa regra antes de rodar.",
              file=sys.stderr)
        return 1
    pergunta = pergunta_arquivo.read_text(encoding="utf-8")
    if tem_segredo(pergunta) or any(a[4] for a in anteriores):
        print("[ERRO] a pergunta ou um --anterior contem padrao de segredo; nenhum agente foi chamado.",
              file=sys.stderr)
        print("Conferir os arquivos. Nada foi gravado em docs/consensus/.", file=sys.stderr)
        return 6
    return com_lock_e_sinais(
        projeto, lambda: _rodar_debate(args, projeto, pergunta_arquivo, participantes, trabalhos_cmd,
                                       rodada_n, pendente, [a[:4] for a in anteriores]))


def _rodar_debate(args, projeto, pergunta_arquivo, participantes, trabalhos_cmd,
                  rodada_n=1, pendente="", anteriores=()):
    pergunta = pergunta_arquivo.read_text(encoding="utf-8")
    aberta = abrir_rodada(projeto, "debate")
    if aberta is None:
        return 1
    run_id, rodada = aberta
    manifesto = novo_manifesto("debate", rodada_n, run_id, projeto, pergunta_arquivo)
    # O rotulo so entra quando difere do nome do arquivo (diretorio de rodada rotula pelo id).
    manifesto["anteriores"] = [
        dict({"rotulo": rotulo} if rotulo != Path(caminho).name else {},
             caminho=caminho, sha256=soma_anterior)
        for rotulo, caminho, _, soma_anterior in anteriores]
    # O que a retomada precisa para continuar sem ninguem repetir argumentos (DEC-009).
    manifesto.update(titulo=args.titulo, dono=args.dono, pendente=pendente,
                     agentes=[{"id": i, "comando": c} for i, c in trabalhos_cmd])
    (rodada / "pergunta.txt").write_bytes(pergunta_arquivo.read_bytes())
    escrever_json(rodada / "manifesto.json", manifesto)

    stdout_por_id = rodar_participantes(
        projeto, rodada, run_id, manifesto, trabalhos_cmd,
        lambda identificador, copia: prompt_do_participante(
            pergunta, identificador, copia, rodada_n, [a[:3] for a in anteriores]),
        reter=rodada_n == 1)

    return fechar_debate(projeto, manifesto, rodada, run_id, participantes, stdout_por_id,
                         args.titulo, args.dono, pergunta, rodada_n, pendente)


def fechar_debate(projeto, manifesto, rodada, run_id, participantes, stdout_por_id,
                  titulo, dono, pergunta, rodada_n, pendente):
    """Fim comum a debate e retomada: fecha sem minuta ou escreve a minuta e sela o manifesto."""
    codigo = fechar_sem_minuta(manifesto, rodada, run_id, participantes)
    if codigo is not None:
        return codigo
    if _interrompendo.is_set():
        return marcar_interrompida(manifesto, rodada, run_id)

    data = dt.date.today().isoformat()
    for p in manifesto["participantes"]:
        p["_stdout_texto"] = stdout_por_id.get(p["id"], "")
    minuta = montar_minuta(titulo, dono, run_id, pergunta,
                           manifesto["participantes"], data, rodada_n, pendente)
    for p in manifesto["participantes"]:
        p.pop("_stdout_texto", None)

    if _interrompendo.is_set():
        return marcar_interrompida(manifesto, rodada, run_id)

    sha_antes, sha_depois, arquivo = gravar_minuta(projeto, minuta)
    manifesto["minuta"] = {
        "arquivo": arquivo,
        "entrada": "%s - %s" % (data, titulo),
        "sha256_antes": sha_antes,
        "sha256_depois": sha_depois,
    }
    manifesto["status"] = "concluida"
    escrever_json(rodada / "manifesto.json", manifesto)
    print("Rodada concluida: %s" % run_id)
    return 0


# --- achado: revalidacao dentro da entrada existente (T-079) -----------------

# Espelha CONSENSUS_ROUNDS_SEM_PENDENCIA do validador: da rodada 4 em diante a entrada
# precisa de '**Pendente da rodada anterior:**'. O script nao inventa o texto (DEC-006).
RODADAS_SEM_PENDENCIA = 3
HEADING_DECISAO = "decisao para registrar em decisions.md"


def norm(texto):
    sem_acento = "".join(c for c in unicodedata.normalize("NFD", texto) if not unicodedata.combining(c))
    return sem_acento.casefold().strip()


def linha_unica(texto):
    """Texto humano de uma linha so, sem travessao: vai para dentro de um campo `**X:** y`."""
    return " ".join((texto or "").replace(TRAVESSAO, "-").split())


def localizar_entrada(texto, titulo):
    """[(inicio, fim)] de cada '## titulo' ate o proximo '## ' ou o fim do arquivo."""
    achados = []
    for m in re.finditer(r"^## " + re.escape(titulo) + r"[ \t]*$", texto, re.M):
        proximo = re.compile(r"^## ", re.M).search(texto, m.end())
        achados.append((m.start(), proximo.start() if proximo else len(texto)))
    return achados


def titulos_da_entrada(linhas):
    """[(indice, texto normalizado)] dos '### ' fora de bloco de codigo."""
    saida, cerca = [], False
    for i, linha in enumerate(linhas):
        if linha.lstrip().startswith(("```", "~~~")):
            cerca = not cerca
        elif not cerca and linha.startswith("### "):
            saida.append((i, norm(linha[4:])))
    return saida


def rotulo_da_linha(linha):
    if linha.startswith("**"):
        fim = linha.find(":**", 2)
        if fim != -1:
            return norm(linha[2:fim]), fim
    return None, -1


def campo_do_cabecalho(linhas, fim_cabecalho, rotulo):
    """(indice, valor) do campo no cabecalho da entrada, ou (None, None)."""
    alvo = norm(rotulo)
    for i in range(fim_cabecalho):
        achado, fim = rotulo_da_linha(linhas[i])
        if achado == alvo:
            return i, linhas[i][fim + 3:].strip()
    return None, None


def juntar_lista(existente, novos):
    """Acrescenta ids a uma lista separada por virgula; `nenhuma` e vazio valem lista vazia."""
    atuais = [x.strip() for x in (existente or "").split(",") if x.strip() and norm(x) != "nenhuma"]
    return ", ".join(atuais + list(novos))


def secao_de_posicao(prefixo, identificador, stdout):
    return ["### %s %s" % (prefixo, identificador), ""] + citar(stdout)[0].rstrip("\n").split("\n")


def secao_de_falha(run_id, p):
    return ["### Falha De %s" % p["id"], "", "- Exit: %s" % p.get("exit"),
            "- Bruto: docs/consensus/%s/%s/" % (run_id, p["id"])]


def reescrever_entrada(entrada, rodada_n, dono, pendente, manifesto_rel, run_id, participantes):
    """Devolve (nova entrada, None) ou (None, motivo). So mexe em: Rodada, Exposicao previa,
    Metodo, Proximo passo, Origem, Manifesto, Participantes, Falhas, Pendente da rodada
    anterior e nas secoes acrescentadas. O resto da entrada fica como estava."""
    linhas = entrada.split("\n")
    titulos = titulos_da_entrada(linhas)
    fim_cab = titulos[0][0] if titulos else len(linhas)
    i_rodada, _ = campo_do_cabecalho(linhas, fim_cab, "Rodada")
    if i_rodada is None:
        return None, "a entrada nao tem '**Rodada:**'; nao ha onde ancorar os campos novos."
    ids = [p["id"] for p in participantes]
    falhos = [p["id"] for p in participantes if p.get("resultado") != "posicao"]

    def trocar(rotulo, valor):
        i, _ = campo_do_cabecalho(linhas, fim_cab, rotulo)
        if i is None:
            return False
        _, fim = rotulo_da_linha(linhas[i])
        linhas[i] = linhas[i][:fim + 3] + " " + valor
        return True

    novos = []  # (rotulo, valor) que entram logo apos a linha Rodada
    trocar("Rodada", "%d de %d" % (rodada_n, rodada_n))
    for rotulo, valor in (("Metodo", "pareceres-independentes"),
                          ("Exposicao previa a outras posicoes", "sim"),
                          ("Proximo passo", "%s le as revalidacoes e decide" % dono)):
        if not trocar(rotulo, valor):
            novos.append((rotulo, valor))
    if campo_do_cabecalho(linhas, fim_cab, "Origem")[0] is None:
        novos.append(("Origem", "automacao"))
    for rotulo, valor in (("Manifesto", manifesto_rel), ("Participantes", None), ("Falhas", None)):
        i, atual = campo_do_cabecalho(linhas, fim_cab, rotulo)
        if rotulo == "Manifesto":
            valor = juntar_lista((atual or "").strip("` "), [manifesto_rel])
        elif rotulo == "Participantes":
            valor = juntar_lista(atual, ids)
        else:
            valor = juntar_lista(atual, falhos) or "nenhuma"
        if i is None:
            novos.append((rotulo, valor))
        else:
            trocar(rotulo, valor)
    if pendente:
        if not trocar("Pendente da rodada anterior", pendente):
            novos.append(("Pendente da rodada anterior", pendente))
    inseridas = []
    for rotulo, valor in novos:
        inseridas.extend(["", "**%s:** %s" % (rotulo, valor)])
    # Insercao de baixo para cima: os indices de cima nao se movem.
    blocos = []
    for p in participantes:
        blocos.append(secao_de_posicao("Revalidacao De", p["id"], p.get("_stdout_texto", ""))
                      if p.get("resultado") == "posicao" else secao_de_falha(run_id, p))
    corpo = []
    for bloco in blocos:
        corpo.extend(bloco + [""])
    i_decisao = next((i for i, t in titulos if t == HEADING_DECISAO), None)
    if i_decisao is not None:
        antes = [""] if i_decisao > 0 and linhas[i_decisao - 1].strip() else []
        linhas[i_decisao:i_decisao] = antes + corpo
    else:
        ultimo = max((i for i, l in enumerate(linhas) if l.strip()), default=len(linhas) - 1)
        linhas[ultimo + 1:ultimo + 1] = [""] + corpo[:-1]
    linhas[i_rodada + 1:i_rodada + 1] = inseridas
    return "\n".join(linhas), None


def preparar_escrita(texto, titulo, rodada_n, dono, pendente, manifesto_rel, run_id, participantes):
    """Devolve (novo texto do arquivo, None) ou (None, motivo). Funcao pura sobre o texto."""
    achados = localizar_entrada(texto, titulo)
    if len(achados) != 1:
        return None, "entrada '%s' nao encontrada, ou ha mais de uma com esse titulo." % titulo
    inicio, fim = achados[0]
    linhas = texto[inicio:fim].split("\n")
    titulos = titulos_da_entrada(linhas)
    fim_cab = titulos[0][0] if titulos else len(linhas)
    if campo_do_cabecalho(linhas, fim_cab, "Achado")[0] is None:
        return None, "a entrada nao declara '**Achado:**'; revalidacao so vale para achado."
    presentes = {t for _, t in titulos}
    for p in participantes:
        for prefixo in ("Revalidacao De", "Falha De"):
            if norm("%s %s" % (prefixo, p["id"])) in presentes:
                return None, "a entrada ja tem a secao '%s %s'; use outro id." % (prefixo, p["id"])
    nova, motivo = reescrever_entrada(texto[inicio:fim], rodada_n, dono, pendente, manifesto_rel,
                                      run_id, participantes)
    if nova is None:
        return None, motivo
    return texto[:inicio] + nova + texto[fim:], None


def prompt_de_achado(participante, copia, titulo, rodada_n, entrada, pergunta):
    partes = [
        "Participante: %s\n"
        "Copia isolada do projeto: %s\n"
        "Esta e uma copia somente-leitura do projeto: leia o que precisar. "
        "Nao edite nada fora da sua resposta.\n"
        "Responda em portugues, sem travessao. A resposta inteira no stdout "
        "sera reproduzida sem resumo. Nenhuma posicao contemporanea desta rodada "
        "esta disponivel por construcao.\n\n"
        "Revalidacao de achado, rodada %d. O que se avalia e a DISPOSICAO que a "
        "entrada propoe, nao o achado: o achado e o ponto de partida. Diga se a "
        "disposicao responde a ele com acerto, aponte o que falta ou esta errado "
        "e confira os fatos no repositorio. A entrada tambem esta em "
        "docs/CONSENSUS.md da copia; a entrada sob revisao entra de proposito.\n\n"
        "Entrada sob revisao (na integra): %s\n\n"
        "%s" % (participante, copia, rodada_n, titulo, entrada.rstrip("\n"))
    ]
    if pergunta:
        partes.append("\n\nPergunta:\n\n%s" % pergunta)
    return "".join(partes) + "\n"


def run_achado(args):
    def erro(msg):
        print("[ERRO] %s" % msg, file=sys.stderr)
        return 1

    projeto = Path(args.projeto).resolve()
    if not projeto.is_dir():
        return erro("projeto nao encontrado: %s" % projeto)
    caminho = projeto / "docs" / "CONSENSUS.md"
    if not caminho.is_file():
        return erro("docs/CONSENSUS.md nao encontrado em %s." % projeto)
    if not args.entrada:
        return erro("achado exige --entrada com o titulo da entrada.")
    try:
        rodada_n = int(args.rodada)
    except (TypeError, ValueError):
        return erro("achado exige --rodada com um numero inteiro.")
    if rodada_n < 1:
        return erro("--rodada precisa ser 1 ou mais.")
    pendente = linha_unica(args.pendente)
    if rodada_n > RODADAS_SEM_PENDENCIA and not pendente:
        return erro("rodada %d exige --pendente: o texto de '**Pendente da rodada anterior:**' "
                    "e humano, o script nao inventa." % rodada_n)
    trabalhos_cmd = validar_participantes(args.agente or [], "achado", 1)
    if trabalhos_cmd is None:
        return 1
    pergunta_arquivo = None
    if args.pergunta:
        pergunta_arquivo = Path(args.pergunta).resolve()
        if not pergunta_arquivo.is_file():
            return erro("pergunta nao encontrada: %s" % pergunta_arquivo)
    dados = caminho.read_bytes()
    if b"\r\n" in dados:
        return erro("docs/CONSENSUS.md usa CRLF; esta operacao so escreve em arquivo LF.")
    try:
        texto = dados.decode("utf-8")
    except UnicodeDecodeError:
        return erro("docs/CONSENSUS.md nao e UTF-8.")
    dono = linha_unica(args.dono) or "usuario"
    sonda = [{"id": i, "resultado": "posicao"} for i, _ in trabalhos_cmd]
    _, motivo = preparar_escrita(texto, args.entrada, rodada_n, dono, pendente, "", "", sonda)
    if motivo:
        return erro(motivo)
    if sidecar_ignorado(projeto):
        return erro("docs/consensus/ esta ignorado pelo git; remova essa regra antes de rodar.")
    inicio, fim = localizar_entrada(texto, args.entrada)[0]
    entrada = texto[inicio:fim]
    pergunta = pergunta_arquivo.read_text(encoding="utf-8") if pergunta_arquivo else ""
    if tem_segredo(entrada) or tem_segredo(pergunta):
        print("[ERRO] a entrada ou a pergunta contem padrao de segredo; nenhum agente foi chamado.",
              file=sys.stderr)
        print("Nada foi gravado em docs/consensus/.", file=sys.stderr)
        return 6
    return com_lock_e_sinais(
        projeto, lambda: _rodar_achado(args, projeto, caminho, rodada_n, dono, pendente, entrada,
                                       pergunta, pergunta_arquivo, args.agente, trabalhos_cmd))


def _rodar_achado(args, projeto, caminho, rodada_n, dono, pendente, entrada, pergunta,
                  pergunta_arquivo, participantes, trabalhos_cmd):
    aberta = abrir_rodada(projeto, "achado")
    if aberta is None:
        return 1
    run_id, rodada = aberta
    manifesto = novo_manifesto("achado", rodada_n, run_id, projeto, pergunta_arquivo)
    manifesto["entrada"] = args.entrada
    manifesto["sha256_entrada"] = soma_texto(entrada)
    manifesto.update(dono=dono, pendente=pendente,
                     agentes=[{"id": i, "comando": c} for i, c in trabalhos_cmd])
    (rodada / "entrada.txt").write_text(entrada, encoding="utf-8")
    if pergunta_arquivo:
        (rodada / "pergunta.txt").write_bytes(pergunta_arquivo.read_bytes())
    escrever_json(rodada / "manifesto.json", manifesto)

    stdout_por_id = rodar_participantes(
        projeto, rodada, run_id, manifesto, trabalhos_cmd,
        lambda identificador, copia: prompt_de_achado(
            identificador, copia, args.entrada, rodada_n, entrada, pergunta),
        reter=False)

    return fechar_achado(caminho, manifesto, rodada, run_id, participantes, stdout_por_id,
                         args.entrada, rodada_n, dono, pendente)


def fechar_achado(caminho, manifesto, rodada, run_id, participantes, stdout_por_id,
                  entrada_titulo, rodada_n, dono, pendente):
    """Fim comum a achado e retomada: reescreve a entrada e sela o manifesto."""
    codigo = fechar_sem_minuta(manifesto, rodada, run_id, participantes)
    if codigo is not None:
        return codigo
    if _interrompendo.is_set():
        return marcar_interrompida(manifesto, rodada, run_id)

    # Rele o arquivo sob o lock: o que se grava e a entrada de agora, nao a do prompt.
    antes = caminho.read_bytes()
    for p in manifesto["participantes"]:
        p["_stdout_texto"] = stdout_por_id.get(p["id"], "")
    novo, motivo = preparar_escrita(antes.decode("utf-8", "replace"), entrada_titulo, rodada_n, dono,
                                    pendente, "docs/consensus/%s/manifesto.json" % run_id, run_id,
                                    manifesto["participantes"])
    for p in manifesto["participantes"]:
        p.pop("_stdout_texto", None)
    if novo is None:
        manifesto["status"] = "recusada-na-escrita"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("[ERRO] %s Bruto e manifesto ficam em docs/consensus/%s/." % (motivo, run_id),
              file=sys.stderr)
        return 1
    if _interrompendo.is_set():
        return marcar_interrompida(manifesto, rodada, run_id)

    escrever_bytes_atomico(caminho, novo.encode("utf-8"))
    manifesto["minuta"] = {
        "arquivo": "docs/CONSENSUS.md",
        "entrada": entrada_titulo,
        "sha256_antes": hashlib.sha256(antes).hexdigest(),
        "sha256_depois": soma(caminho),
    }
    manifesto["status"] = "concluida"
    escrever_json(rodada / "manifesto.json", manifesto)
    print("Rodada concluida: %s" % run_id)
    return 0


# --- retomar: continuar uma rodada nao concluida, por comando explicito (T-081) ---

def aceitar_a_mao(rodada, registro):
    """Material retido que a pessoa moveu para <run>/<id>/ (DEC-010): vira posicao, sem nova chamada
    e sem nova varredura, porque a palavra humana ja foi dada."""
    destino = rodada / registro["id"]
    stdout_path = destino / "stdout.txt"
    texto = stdout_path.read_bytes().decode("utf-8", "replace")
    novo = {k: v for k, v in registro.items() if k != "retido_em"}
    novo.update({
        "stdout": "%s/stdout.txt" % registro["id"],
        "sha256_stdout": soma(stdout_path),
        "resultado": "posicao" if registro.get("exit") == 0 else "falha",
        "travessoes_substituidos": texto.count(TRAVESSAO),
        "aceito_por_humano": True,
    })
    if (destino / "stderr.txt").is_file():
        novo["stderr"] = "%s/stderr.txt" % registro["id"]
    return novo


def run_retomar(args):
    projeto = Path(args.projeto).resolve()
    run_id = args.run_id
    if not projeto.is_dir():
        print("[ERRO] projeto nao encontrado: %s" % projeto, file=sys.stderr)
        return 1
    if id_inseguro(run_id) or not (projeto / "docs" / "consensus" / run_id / "manifesto.json").is_file():
        print("[ERRO] rodada nao encontrada: docs/consensus/%s/manifesto.json" % run_id, file=sys.stderr)
        return 1
    # O lock vem antes do resto: ninguem le o estado de uma rodada que outra execucao escreve.
    return com_lock_e_sinais(
        projeto, lambda: _retomar(projeto, projeto / "docs" / "consensus" / run_id, run_id), run_id)


def _retomar(projeto, rodada, run_id):
    def erro(msg):
        print("[ERRO] %s" % msg, file=sys.stderr)
        return 1

    try:
        manifesto = json.loads((rodada / "manifesto.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as motivo:
        return erro("manifesto ilegivel em docs/consensus/%s: %s" % (run_id, motivo))
    if manifesto.get("status") == "concluida":
        return erro("a rodada %s ja esta concluida; nada a retomar." % run_id)
    modo = manifesto.get("modo")
    agentes = manifesto.get("agentes")
    if modo not in ("debate", "achado") or not agentes:
        return erro("o manifesto de %s nao guarda os parametros da rodada (agentes, comandos); "
                    "rodada de versao anterior nao se retoma. Rode de novo." % run_id)
    trabalhos = [(a["id"], a["comando"]) for a in agentes]
    try:
        rodada_n = int(manifesto["rodada"])
    except (KeyError, TypeError, ValueError):
        return erro("o manifesto de %s nao tem a rodada." % run_id)
    pendente = manifesto.get("pendente") or ""
    caminho = projeto / "docs" / "CONSENSUS.md"
    if not caminho.is_file():
        return erro("docs/CONSENSUS.md nao encontrado em %s." % projeto)
    if sidecar_ignorado(projeto):
        return erro("docs/consensus/ esta ignorado pelo git; remova essa regra antes de retomar.")

    # Pergunta e entrada voltam da copia gravada na rodada, conferida pelo hash do manifesto.
    pergunta = ""
    if manifesto.get("pergunta") or modo == "debate":
        pergunta_path = rodada / "pergunta.txt"
        if not pergunta_path.is_file() or (
                manifesto.get("pergunta") and soma(pergunta_path) != manifesto["pergunta"].get("sha256")):
            return erro("rodada/pergunta.txt ausente ou diferente do manifesto; nada foi chamado.")
        pergunta = pergunta_path.read_text(encoding="utf-8")
    segredo = tem_segredo(pergunta)

    if modo == "debate":
        anteriores = []
        for item in manifesto.get("anteriores") or []:
            arquivo = Path(item["caminho"])
            arquivo = arquivo if arquivo.is_absolute() else projeto / arquivo
            try:
                dados = arquivo.read_bytes()
            except OSError as motivo:
                return erro("--anterior original ilegivel: %s (%s)" % (item["caminho"], motivo))
            if hashlib.sha256(dados).hexdigest() != item["sha256"]:
                return erro("o anterior %s mudou desde a rodada; retomar com outro texto seria "
                            "outra rodada. Nada foi chamado." % item["caminho"])
            segredo = segredo or tem_segredo(dados)
            anteriores.append((item.get("rotulo") or arquivo.name, item["caminho"],
                               dados.decode("utf-8", "replace")))
        prompt_de = lambda identificador, copia: prompt_do_participante(  # noqa: E731
            pergunta, identificador, copia, rodada_n, anteriores)
        reter = rodada_n == 1
    else:
        titulo = manifesto.get("entrada") or ""
        entrada_path = rodada / "entrada.txt"
        if not entrada_path.is_file() or soma(entrada_path) != manifesto.get("sha256_entrada"):
            return erro("rodada/entrada.txt ausente ou diferente do manifesto; nada foi chamado.")
        entrada = entrada_path.read_text(encoding="utf-8")
        segredo = segredo or tem_segredo(entrada)
        dados = caminho.read_bytes()
        if b"\r\n" in dados:
            return erro("docs/CONSENSUS.md usa CRLF; esta operacao so escreve em arquivo LF.")
        sonda = [{"id": i, "resultado": "posicao"} for i, _ in trabalhos]
        _, motivo = preparar_escrita(dados.decode("utf-8", "replace"), titulo, rodada_n,
                                     manifesto.get("dono") or "usuario", pendente, "", "", sonda)
        if motivo:
            return erro(motivo)
        prompt_de = lambda identificador, copia: prompt_de_achado(  # noqa: E731
            identificador, copia, titulo, rodada_n, entrada, pergunta)
        reter = False
    if segredo:
        print("[ERRO] a pergunta, a entrada ou um anterior da rodada contem padrao de segredo; "
              "nenhum agente foi chamado.", file=sys.stderr)
        return 6

    # Quem tem <id>/stdout.txt fica como esta: o bruto ja foi pago. Sem registro no manifesto o
    # arquivo pode estar pela metade (queda entre a escrita e o registro), entao roda de novo.
    registros = {p["id"]: p for p in manifesto.get("participantes", [])}
    mantidos, aceitos, chamar, finais = [], [], [], []
    stdout_por_id = {}
    for identificador, comando in trabalhos:
        registro = registros.get(identificador)
        bruto = rodada / identificador / "stdout.txt"
        if registro is None or not bruto.is_file():
            chamar.append((identificador, comando))
            continue
        if registro.get("resultado") == "retido-por-segredo":
            registro = aceitar_a_mao(rodada, registro)
            aceitos.append(identificador)
        else:
            mantidos.append(identificador)
        finais.append(registro)
        if registro["resultado"] == "posicao":
            stdout_por_id[identificador] = bruto.read_bytes().decode("utf-8", "replace")

    manifesto["participantes"] = finais
    manifesto.setdefault("retomadas", []).append({
        "instante": agora(),
        "chamados": [i for i, _ in chamar],
        "mantidos": mantidos,
        "aceitos_a_mao": aceitos,
    })
    manifesto["status"] = "em-andamento"
    manifesto["fim"] = None
    escrever_json(rodada / "manifesto.json", manifesto)
    print("Retomando %s: chamados=%s mantidos=%s aceitos a mao=%s" % (
        run_id, ",".join(i for i, _ in chamar) or "nenhum", ",".join(mantidos) or "nenhum",
        ",".join(aceitos) or "nenhum"))

    stdout_por_id.update(rodar_participantes(projeto, rodada, run_id, manifesto, chamar, prompt_de, reter))
    if modo == "debate":
        return fechar_debate(projeto, manifesto, rodada, run_id, trabalhos, stdout_por_id,
                             manifesto.get("titulo") or "Debate", manifesto.get("dono") or "usuario",
                             pergunta, rodada_n, pendente)
    return fechar_achado(caminho, manifesto, rodada, run_id, trabalhos, stdout_por_id, titulo,
                         rodada_n, manifesto.get("dono") or "usuario", pendente)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Automacao mecanica de consenso.")
    subcomandos = parser.add_subparsers(dest="subcomando", required=True)
    debate = subcomandos.add_parser("debate", help="Roda pareceres independentes.")
    debate.add_argument("--projeto", default=".")
    debate.add_argument("--pergunta", required=True)
    debate.add_argument("--agente", action="append", nargs=2, metavar=("ID", "COMANDO"))
    debate.add_argument("--titulo", default="Debate")
    debate.add_argument("--dono", default="usuario")
    debate.add_argument("--rodada", default="1", help="Numero da rodada; o script nunca deduz.")
    debate.add_argument("--anterior", action="append", metavar="CAMINHO",
                        help="Posicao anterior: arquivo, ou diretorio de rodada em docs/consensus/. "
                             "Repetivel; obrigatorio da rodada 2 em diante.")
    debate.add_argument("--pendente", help="Obrigatorio da rodada 4 em diante; texto humano.")
    achado = subcomandos.add_parser(
        "achado", help="Revalida a disposicao de um achado, dentro da entrada existente.")
    achado.add_argument("--projeto", default=".")
    achado.add_argument("--entrada", help="Titulo da entrada em CONSENSUS.md, sem o '## '.")
    achado.add_argument("--rodada", help="Numero da rodada (1 ou mais); o script nunca deduz.")
    achado.add_argument("--agente", action="append", nargs=2, metavar=("ID", "COMANDO"))
    achado.add_argument("--pergunta", help="Arquivo opcional com uma pergunta adicional.")
    achado.add_argument("--dono", default="usuario")
    achado.add_argument("--pendente", help="Obrigatorio da rodada 4 em diante; texto humano.")
    retomar = subcomandos.add_parser(
        "retomar", help="Continua uma rodada nao concluida, sem repetir trabalho pago.")
    retomar.add_argument("--projeto", default=".")
    retomar.add_argument("run_id", help="Pasta da rodada em docs/consensus/.")
    args = parser.parse_args(argv)
    if args.subcomando == "achado":
        return run_achado(args)
    if args.subcomando == "retomar":
        return run_retomar(args)
    return run_debate(args)


if __name__ == "__main__":
    sys.exit(main())
