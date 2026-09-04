#!/usr/bin/env python3
"""Valida a estrutura Markdown multiagente criada pela skill ai-project-structure.

Uso:
    python3 validate_structure.py [CAMINHO_DO_PROJETO] [--strict]

Saida: relatorio em portugues agrupado por arquivo, com prefixos
[ERRO] / [AVISO] / [INFO] e resumo final.
Exit code: 1 se houver erro (ou aviso, com --strict); 0 caso contrario.

Somente biblioteca padrao (Python 3.8+).
"""

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

CORE_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "docs/README.md",
    "docs/PROJECT_CONTEXT.md",
    "docs/SESSION.md",
    "docs/MEMORY.md",
    "docs/CONSENSUS.md",
    "docs/TASKS.md",
    "docs/DECISIONS.md",
    "docs/QUALITY.md",
    "docs/CHANGELOG.md",
    "docs/archive/README.md",
]

SESSION_HEADINGS = [
    "Objetivo",
    "O Que Foi Feito",
    "Arquivos Criados Ou Alterados",
    "Decisoes Tomadas",
    "Aprendizados Para MEMORY.md",
    "Pendencias",
    "Proximo Passo Recomendado",
]

CONSENSUS_STATUSES = {"aberto", "resolvido", "arquivado"}
SPEC_STATUSES = {"rascunho", "definida", "em andamento", "concluida", "cancelada"}
PRIORITIES = {"alta", "media", "baixa"}
EVIDENCE_TYPES = {"comando", "revisao-manual", "conferencia"}
CONSENSUS_METHODS = {"pareceres-independentes", "debate-aberto"}
CONSENSUS_EXPOSURE = {"sim", "nao"}
CONSENSUS_ESCAPOU = {"sim", "nao"}
ACHADO_SECAO_ESCAPE = "Por Que Nada Pegou Antes"

MARKER_RE = re.compile(
    r"<!--\s*ai-project-structure:(core|specs|loop):(start|end)(?:\s+v(\S+))?\s*-->"
)
ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}", re.MULTILINE)
TASK_ID_RE = re.compile(r"\bT-(\d+)\b")
# ID proprio da tarefa: o que abre a linha, depois da data quando ela e concluida.
# Qualquer outro T-NNN no texto e referencia a outra tarefa, nao um segundo ID.
# Tres digitos ou mais: `T-1` e formato invalido, `T-1000` continua ID.
TASK_OWN_ID_RE = re.compile(r"^(?:\d{4}-\d{2}-\d{2}\s+)?T-(\d{3,})\b")
TASK_OWN_ID_CANDIDATE_RE = re.compile(r"^(?:\d{4}-\d{2}-\d{2}\s+)?T-([^\s:]+)\b")
SPEC_REF_RE = re.compile(r"\(spec:\s*([^)]+)\)")
SPEC_NAME_RE = re.compile(r"^(\d{4})-[a-z0-9][a-z0-9-]*\.md$")
PRIORITY_RE = re.compile(r"\(prioridade:\s*([^)]*)\)")
# Marcador so vale no fim da linha, opcionalmente seguido por outros marcadores.
# Uma mencao em prosa como "`(verifica:)` sem resultado" nao declara comando.
VERIFICA_RE = re.compile(r"\(verifica:\s*([^)]*)\)(?=\s*(?:\([^)]*\)\s*)*$)")
BLOCKED_RE = re.compile(r"\(bloqueada:\s*([^)]*)\)")
ADOPTION_RE = re.compile(r"\(convencoes-2-2-0-desde:\s*([^)]*)\)")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\b")
EVIDENCE_TYPE_RE = re.compile(r"\btipo\s*=\s*([^;]+)")
ROTATION_MAX_ENTRIES = 20
ROTATION_MAX_BYTES = 30 * 1024
BLOCKED_MAX_DAYS = 30
# Nao e teto: da rodada seguinte a esta, a entrada precisa declarar o que a
# rodada anterior deixou em aberto. O teto de 3 da 2.2.0 foi escrito sem
# evidencia e o uso real chegou a sete revalidacoes sem que isso fosse fracasso.
CONSENSUS_ROUNDS_SEM_PENDENCIA = 3

# Identificador estavel de cada diagnostico. E contrato publico: a redacao da
# mensagem pode mudar quando melhorar, o codigo so muda em mudanca de versao.
# `Report.add` recusa codigo que nao esteja aqui, entao um erro de digitacao
# quebra na hora em vez de virar diagnostico sem identidade.
CODIGOS = {
    # Arquivos e blocos gerenciados
    "NUCLEO-AUSENTE",
    "TRAVESSAO",
    "PONTE-QUEBRADA",
    "ESTRUTURA-V1",
    "MARCADOR-DESPAREADO",
    "MARCADOR-VERSAO-INVALIDA",
    "MARCADOR-ORDEM-INVALIDA",
    "MARCADOR-LOOP-INVALIDO",
    "NUCLEO-VAZIO",
    # SESSION.md
    "SESSAO-SEM-HEADINGS",
    # CONSENSUS.md, debate
    "CONSENSO-CAMPO-AUSENTE",
    "CONSENSO-CAMPO-INVALIDO",
    "CONSENSO-RODADA-FORMATO",
    "CONSENSO-SEM-PENDENTE",
    "CONSENSO-SEM-STATUS",
    "CONSENSO-STATUS-INVALIDO",
    "CONSENSO-ABERTO-SEM-PROXIMO-PASSO",
    "CONSENSO-RODADA-EXPOSICAO-INVALIDA",
    # CONSENSUS.md, achado
    "ACHADO-SEM-IDENTIFICADOR",
    "ACHADO-SEM-ESCAPOU",
    "ACHADO-ESCAPOU-INVALIDO",
    "ACHADO-SEM-SECAO-PONTO-CEGO",
    # Rotacao
    "ROTACAO",
    # TASKS.md
    "TASK-ID-DUPLICADO",
    "TASK-ID-ARQUIVADO-DUPLICADO",
    "TASKS-FORMATO-V1",
    "TASK-SEM-ID",
    "TASK-CONCLUIDA-SEM-DATA",
    "TASK-PRIORIDADE-INVALIDA",
    "TASK-BLOQUEADA-FORMATO",
    "TASK-BLOQUEADA-ANTIGA",
    "SPEC-REF-NAO-RESOLVE",
    "AGUARDANDO-SEM-PERGUNTA",
    # Evidencia de fechamento
    "CONVENCOES-DATA-INVALIDA",
    "EVIDENCIA-AUSENTE",
    "EVIDENCIA-AUSENTE-COM-VERIFICA",
    "EVIDENCIA-SEM-RESULTADO",
    "EVIDENCIA-TIPO-INVALIDO",
    "EVIDENCIA-FORMATO-INVALIDO",
    "VERIFICA-COMANDO-VAZIO",
    "AGUARDANDO-SEM-RESPOSTA",
    "AGUARDANDO-SEM-BLOQUEADA",
    "TASK-ID-FORMATO-INVALIDO",
    "TASK-BLOQUEADA-FORA-DE-AGUARDANDO",
    "CERCA-ABERTA",
    # specs/
    "SPEC-NOME-INVALIDO",
    "SPEC-PREFIXO-DUPLICADO",
    "SPEC-SEM-STATUS",
    "SPEC-STATUS-INVALIDO",
    "SPEC-TASK-INEXISTENTE",
    "SPEC-CONCLUIDA-COM-PENDENTE",
    "SPEC-CONCLUIDA-SEM-EVIDENCIA",
    "SPEC-TASK-COM-STATUS",
}


def normalize(text):
    """Minusculas sem acentos, para comparacao tolerante."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.casefold().strip()


def strip_fences(text):
    """Remove conteudo dentro de cercas ``` (os templates trazem modelos cercados)."""
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def check_unclosed_fences(root, report):
    """Cerca ``` sem fechamento esconde o restante do arquivo do parser."""
    targets = [root / "AGENTS.md", root / "CLAUDE.md", root / "GEMINI.md"]
    docs = root / "docs"
    if docs.is_dir():
        targets.extend(sorted(docs.glob("*.md")))
        specs = docs / "specs"
        if specs.is_dir():
            targets.extend(sorted(specs.rglob("*.md")))
    for path in targets:
        if not path.is_file():
            continue
        text = read(path)
        if text is None:
            continue
        opened = False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                opened = not opened
        if opened:
            rel = path.relative_to(root).as_posix()
            report.aviso(rel, "CERCA-ABERTA", "Cerca de codigo ``` aberta ate o fim do arquivo.")


class Report:
    """Diagnosticos do validador.

    Cada diagnostico carrega um `codigo` estavel e um `sujeito` opcional (a
    tarefa, a entrada ou a spec de que ele fala). O codigo e o **contrato
    publico**: a redacao da mensagem pode melhorar a qualquer momento, o codigo
    nao muda sem ser mudanca de versao. Quem escreve portao em cima da saida
    deste script casa `--codigos`, nunca fragmento de texto."""

    def __init__(self):
        self.items = {}  # arquivo -> [(nivel, codigo, sujeito, mensagem)]

    def add(self, level, file, code, message, subject=None):
        if code not in CODIGOS:
            raise ValueError(
                f"Codigo de diagnostico desconhecido: {code!r}. "
                "Todo diagnostico precisa estar declarado em CODIGOS."
            )
        self.items.setdefault(file, []).append((level, code, subject, message))

    def erro(self, file, code, message, subject=None):
        self.add("ERRO", file, code, message, subject)

    def aviso(self, file, code, message, subject=None):
        self.add("AVISO", file, code, message, subject)

    def info(self, file, code, message, subject=None):
        self.add("INFO", file, code, message, subject)

    def counts(self):
        flat = [lvl for msgs in self.items.values() for lvl, _, _, _ in msgs]
        return flat.count("ERRO"), flat.count("AVISO")

    def print(self):
        if not self.items:
            print("Nenhum problema encontrado.")
        for file in sorted(self.items):
            print(f"\n{file}")
            for level, code, _, message in self.items[file]:
                print(f"  [{level}] [{code}] {message}")
        errors, warnings = self.counts()
        print(f"\nResumo: {errors} erros, {warnings} avisos.")

    def print_codigos(self):
        """Saida legivel por maquina, uma linha por diagnostico.

        Formato: NIVEL|CODIGO|ARQUIVO|SUJEITO. Sem prosa de proposito: e o que
        um portao deve casar, e nada aqui muda quando a mensagem muda."""
        for file in sorted(self.items):
            for level, code, subject, _ in self.items[file]:
                print(f"{level}|{code}|{file}|{subject or ''}")


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def split_entries(clean_text):
    """Divide texto (ja sem cercas) em entradas '## AAAA-MM-DD ...'.

    Retorna lista de (titulo, corpo)."""
    entries = []
    matches = list(re.finditer(r"^## (\d{4}-\d{2}-\d{2}.*)$", clean_text, re.MULTILINE))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(clean_text)
        entries.append((m.group(1).strip(), clean_text[start:end]))
    return entries


def check_core_files(root, report):
    for rel in CORE_FILES:
        path = root / rel
        if not path.is_file():
            report.erro(rel, "NUCLEO-AUSENTE", "Arquivo do nucleo ausente.", rel)
        elif path.stat().st_size == 0:
            report.erro(rel, "NUCLEO-VAZIO", "Arquivo do nucleo esta vazio.", rel)


def check_em_dash(root, report):
    """Regra do projeto: o travessao (em dash, U+2014) e proibido em qualquer texto."""
    targets = [root / "AGENTS.md", root / "CLAUDE.md", root / "GEMINI.md"]
    docs = root / "docs"
    if docs.is_dir():
        targets.extend(sorted(docs.rglob("*.md")))
    for path in targets:
        if not path.is_file():
            continue
        text = read(path)
        if text is None:
            continue
        count = text.count("\u2014")
        if count:
            rel = path.relative_to(root).as_posix()
            report.erro(
                rel,
                "TRAVESSAO",
                f"Contem travessao (em dash, U+2014) {count}x; proibido pela regra "
                "do projeto. Use dois-pontos, virgula, parenteses ou hifen simples.",
            )


def check_bridges(root, report):
    for rel in ("CLAUDE.md", "GEMINI.md"):
        text = read(root / rel)
        if text is not None and "AGENTS.md" not in text:
            report.aviso(
                rel, "PONTE-QUEBRADA",
                "Arquivo-ponte nao menciona AGENTS.md (ponte quebrada?).",
            )


def check_markers(root, report):
    text = read(root / "AGENTS.md")
    if text is None:
        return
    found = {}  # bloco -> {"start": [(versao, posicao)], "end": [posicao]}
    for m in MARKER_RE.finditer(text):
        block, kind, version = m.group(1), m.group(2), m.group(3)
        entry = found.setdefault(block, {"start": [], "end": []})
        if kind == "start":
            entry["start"].append((version, m.start()))
        else:
            entry["end"].append(m.start())
    if not found:
        report.info(
            "AGENTS.md",
            "ESTRUTURA-V1",
            "Estrutura v1 detectada (sem bloco gerenciado). "
            "Rode a skill ai-project-structure para atualizar.",
        )
        return
    for block, entry in found.items():
        starts, ends = entry["start"], entry["end"]
        pareado = len(starts) == 1 and len(ends) == 1
        if not pareado:
            report.erro(
                "AGENTS.md",
                "MARCADOR-DESPAREADO",
                f"Marcadores do bloco '{block}' despareados "
                f"({len(starts)} start, {len(ends)} end). Esperado exatamente 1 de cada.",
                block,
            )
        if pareado and starts[0][1] > ends[0]:
            report.erro(
                "AGENTS.md",
                "MARCADOR-ORDEM-INVALIDA",
                f"Marcador end do bloco '{block}' aparece antes do start.",
                block,
            )
        version = starts[0][0] if len(starts) == 1 else None
        versao_invalida = not version or not re.fullmatch(r"v?\d+\.\d+\.\d+", version)
        if pareado and versao_invalida:
            report.erro(
                "AGENTS.md",
                "MARCADOR-VERSAO-INVALIDA",
                f"Versao ausente ou invalida no marcador do bloco '{block}' "
                f"(esperado ex: 'v2.0.0', encontrado: {version!r}).",
                block,
            )
        if block == "loop" and (not pareado or versao_invalida):
            report.erro(
                "AGENTS.md",
                "MARCADOR-LOOP-INVALIDO",
                "Bloco 'loop' sem marcadores pareados e versao valida no start.",
                block,
            )


def check_session(root, report):
    text = read(root / "docs" / "SESSION.md")
    if text is None:
        return
    clean = strip_fences(text)
    entries = split_entries(clean)
    wanted = [normalize(h) for h in SESSION_HEADINGS]
    for title, body in entries:
        headings = [normalize(h) for h in re.findall(r"^### (.+)$", body, re.MULTILINE)]
        missing = [
            SESSION_HEADINGS[i] for i, w in enumerate(wanted) if w not in headings
        ]
        if missing:
            report.aviso(
                "docs/SESSION.md",
                "SESSAO-SEM-HEADINGS",
                f"Entrada '{title}' sem os headings: {', '.join(missing)}.",
                title,
            )
    check_rotation(root / "docs" / "SESSION.md", len(entries), report)


def field_value(body, label):
    """Valor de uma linha '**Rotulo:** valor', tolerante a acento e caixa."""
    wanted = f"**{normalize(label)}:**"
    for line in body.splitlines():
        if normalize(line).startswith(wanted):
            return line.split(":**", 1)[1].strip()
    return None


def check_consensus_declaration(title, body, report):
    """Campos declarativos de independencia (Metodo, Exposicao previa, Rodada).

    Checa presenca e valor permitido, nunca veracidade: nenhum script prova que
    um modelo nao leu a posicao do outro."""
    rel = "docs/CONSENSUS.md"
    for label, allowed in (
        ("Metodo", CONSENSUS_METHODS),
        ("Exposicao previa a outras posicoes", CONSENSUS_EXPOSURE),
    ):
        value = field_value(body, label)
        if value is None:
            report.aviso(
                rel, "CONSENSO-CAMPO-AUSENTE",
                f"Entrada '{title}' sem linha '**{label}:**'.", title,
            )
        elif normalize(value) not in allowed:
            report.aviso(
                rel,
                "CONSENSO-CAMPO-INVALIDO",
                f"Entrada '{title}' com '**{label}:** {value}' fora do conjunto "
                f"({' | '.join(sorted(allowed))}).",
                title,
            )
    rodada = field_value(body, "Rodada")
    if rodada is None:
        return
    m = re.match(r"(\d+)\s*de\s*(\d+)", normalize(rodada))
    if not m:
        report.aviso(
            rel,
            "CONSENSO-RODADA-FORMATO",
            f"Entrada '{title}' com '**Rodada:** {rodada}' fora do formato 'N de N'.",
            title,
        )
    else:
        number = int(m.group(1))
        exposure = normalize(field_value(body, "Exposicao previa a outras posicoes") or "")
        if number >= 2 and exposure == "nao":
            report.aviso(
                rel,
                "CONSENSO-RODADA-EXPOSICAO-INVALIDA",
                f"Entrada '{title}' esta na rodada {number} com exposicao previa 'nao'; "
                "da rodada 2 em diante a exposicao previa deve ser 'sim'.",
                title,
            )
        if number > CONSENSUS_ROUNDS_SEM_PENDENCIA and not (
            field_value(body, "Pendente da rodada anterior") or ""
        ).strip():
            report.aviso(
                rel,
                "CONSENSO-SEM-PENDENTE",
                f"Entrada '{title}' esta na rodada {m.group(1)} sem "
                "'**Pendente da rodada anterior:**' dizendo o que a anterior deixou "
                "em aberto.",
                title,
            )


def check_consensus_achado(title, body, report):
    """Formato de achado (2.4.0), cobrado so de quem declara '**Achado:**'.

    Entrada de debate nao ganha cobranca nova: sem o campo, esta funcao sai
    sem escrever nada. O identificador e livre (DEC-002 da spec 0005), entao o
    validador confere presenca e valor nao vazio, nunca o valor em si."""
    rel = "docs/CONSENSUS.md"
    achado = field_value(body, "Achado")
    if achado is None:
        return
    if not achado.strip():
        report.aviso(
            rel,
            "ACHADO-SEM-IDENTIFICADOR",
            f"Entrada '{title}' declara '**Achado:**' sem identificador. "
            "O identificador e livre, mas precisa existir para dar para "
            "referenciar o achado depois.",
            title,
        )
    escapou = field_value(body, "Escapou de verificacao")
    if escapou is None:
        report.aviso(
            rel,
            "ACHADO-SEM-ESCAPOU",
            f"Achado '{title}' sem linha '**Escapou de verificacao:**' "
            f"({' | '.join(sorted(CONSENSUS_ESCAPOU))}).",
            title,
        )
        return
    if normalize(escapou) not in CONSENSUS_ESCAPOU:
        report.aviso(
            rel,
            "ACHADO-ESCAPOU-INVALIDO",
            f"Achado '{title}' com '**Escapou de verificacao:** {escapou}' fora "
            f"do conjunto ({' | '.join(sorted(CONSENSUS_ESCAPOU))}).",
            title,
        )
        return
    if normalize(escapou) != "sim":
        return
    headings = [normalize(h) for h in re.findall(r"^#{3,4} (.+)$", body, re.MULTILINE)]
    if normalize(ACHADO_SECAO_ESCAPE) not in headings:
        report.aviso(
            rel,
            "ACHADO-SEM-SECAO-PONTO-CEGO",
            f"Achado '{title}' declarou '**Escapou de verificacao:** sim' e nao "
            f"tem a secao '{ACHADO_SECAO_ESCAPE}', com o que passou verde e o "
            "mecanismo do ponto cego.",
            title,
        )


def check_consensus(root, report, adopted=None):
    text = read(root / "docs" / "CONSENSUS.md")
    if text is None:
        return
    clean = strip_fences(text)
    entries = split_entries(clean)
    for title, body in entries:
        # A declaracao de independencia nao e retroativa: vale para entradas a
        # partir da data de adocao declarada em TASKS.md.
        entry_date = parse_date(title[:10])
        if adopted is not None and entry_date is not None and entry_date >= adopted:
            check_consensus_declaration(title, body, report)
        # O formato de achado nao depende da data de adocao: a entrada opta por
        # ele ao declarar '**Achado:**', e quem nunca declara nunca e cobrado.
        check_consensus_achado(title, body, report)
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)$", body, re.MULTILINE)
        if not status_match:
            report.aviso(
                "docs/CONSENSUS.md", "CONSENSO-SEM-STATUS",
                f"Entrada '{title}' sem linha '**Status:**'.", title,
            )
            continue
        status = normalize(status_match.group(1))
        if status not in CONSENSUS_STATUSES:
            report.aviso(
                "docs/CONSENSUS.md",
                "CONSENSO-STATUS-INVALIDO",
                f"Entrada '{title}' com Status invalido: '{status_match.group(1).strip()}' "
                "(esperado: aberto | resolvido | arquivado).",
                title,
            )
        elif status == "aberto" and not (field_value(body, "Proximo passo") or "").strip():
            report.aviso(
                "docs/CONSENSUS.md",
                "CONSENSO-ABERTO-SEM-PROXIMO-PASSO",
                f"Entrada '{title}' esta aberta sem '**Proximo passo:**' com dono.",
                title,
            )
    check_rotation(root / "docs" / "CONSENSUS.md", len(entries), report)


def check_rotation(path, entry_count, report):
    rel = f"docs/{path.name}"
    try:
        size = path.stat().st_size
    except OSError:
        return
    if entry_count > ROTATION_MAX_ENTRIES or size > ROTATION_MAX_BYTES:
        report.aviso(
            rel,
            "ROTACAO",
            f"Arquivo com {entry_count} entradas e {size // 1024}KB; "
            "considere rotacionar as mais antigas para docs/archive/ "
            "(regra em AGENTS.md).",
        )


def collect_tasks(root):
    """Retorna {secao: [tarefa]}, com a secao normalizada.

    Cada tarefa e um dict {"line": texto da linha, "sub": [sub-linhas]}. As
    sub-linhas sao os itens indentados logo abaixo da tarefa (`Evidencia:`,
    `**Pergunta:**`, `**Resposta:**`)."""
    text = read(root / "docs" / "TASKS.md")
    if text is None:
        return None
    clean = strip_fences(text)
    sections = {}
    current = None
    task = None
    for line in clean.splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            current = normalize(m.group(1))
            sections.setdefault(current, [])
            task = None
            continue
        if current is None:
            continue
        if line.startswith("- "):
            task = {"line": line[2:].strip(), "sub": []}
            sections[current].append(task)
            continue
        sub = re.match(r"^\s+[-*]\s+(.*)$", line)
        if sub is not None:
            if task is not None:
                task["sub"].append(sub.group(1).strip())
            continue
        if line.strip():
            task = None
    return sections


def is_placeholder(line):
    content = line.strip()
    return content.startswith("(") or normalize(content).startswith("nenhuma tarefa")


def squeeze(text):
    """Espacos colapsados, para comparar comando declarado contra evidencia."""
    return re.sub(r"\s+", " ", text).strip()


def parse_date(value):
    """Converte 'AAAA-MM-DD' em date; None se nao for uma data valida."""
    try:
        year, month, day = (int(p) for p in value.strip().split("-"))
        return date(year, month, day)
    except (ValueError, AttributeError):
        return None


def adoption_date(root):
    """Data em que o projeto adotou as convencoes 2.2.0, declarada em TASKS.md.

    Retorna (data, marcador_presente). Sem marcador, as regras que dependem
    dele ficam silenciosas: projeto anterior a 2.2.0 nao e cobrado (DEC-008)."""
    text = read(root / "docs" / "TASKS.md")
    if text is None:
        return None, False
    m = ADOPTION_RE.search(strip_fences(text))
    if not m:
        return None, False
    return parse_date(m.group(1)), True


def evidence_lines(task):
    return [s for s in task["sub"] if normalize(s).startswith("evidencia:")]


def check_tasks(root, report):
    sections = collect_tasks(root)
    if sections is None:
        return set(), set()
    # Linhas sem ID so sao cobradas nas secoes de trabalho aberto; entradas
    # historicas de "Concluidas" anteriores a v2 podem ficar sem ID.
    open_sections = ["em andamento", "proximas tarefas", "aguardando usuario"]
    all_ids = []
    ids_done = set()
    lines_without_id = []
    any_line = False
    for sec, tasks in sections.items():
        for task in tasks:
            line = task["line"]
            if is_placeholder(line):
                continue
            own = TASK_OWN_ID_RE.match(line)
            candidate = TASK_OWN_ID_CANDIDATE_RE.match(line)
            ids = [own.group(1)] if own else []
            # Unicidade vale no arquivo todo (inclusive Ideias e Concluidas).
            all_ids.extend(ids)
            if sec == "concluidas":
                ids_done.update(ids)
            if candidate and not own:
                report.aviso(
                    "docs/TASKS.md",
                    "TASK-ID-FORMATO-INVALIDO",
                    f"ID proprio fora do formato T-NNN (pelo menos tres digitos): T-{candidate.group(1)}.",
                    f"T-{candidate.group(1)}",
                )
            if sec in open_sections:
                any_line = True
                if not ids and not candidate:
                    lines_without_id.append((sec, line))
    # Check 7: unicidade
    seen = set()
    for tid in all_ids:
        if tid in seen:
            report.erro(
                "docs/TASKS.md", "TASK-ID-DUPLICADO",
                f"ID duplicado: T-{tid}.", f"T-{tid}",
            )
        seen.add(tid)
    archived = archive_task_ids(root)
    for tid in sorted(seen & archived):
        report.erro(
            "docs/TASKS.md",
            "TASK-ID-ARQUIVADO-DUPLICADO",
            f"ID T-{tid} existe no arquivo vivo e em docs/archive/TASKS-*.md.",
            f"T-{tid}",
        )
    # Check 8: formato v1 vs misto
    if any_line and not all_ids and lines_without_id:
        report.info(
            "docs/TASKS.md",
            "TASKS-FORMATO-V1",
            "Nenhuma tarefa usa ID T-NNN (formato v1). "
            "A skill pode migrar os IDs no fluxo de atualizacao.",
        )
    elif all_ids and lines_without_id:
        for sec, line in lines_without_id:
            report.aviso(
                "docs/TASKS.md",
                "TASK-SEM-ID",
                f"Tarefa sem ID T-NNN na secao '{sec}': \"{line[:60]}\".",
                sec,
            )
    # Check 9: refs de spec resolvem (so em linhas de tarefa; ignora o
    # placeholder NNNN usado na documentacao de formato do proprio template)
    for tasks in sections.values():
        for task in tasks:
            line = task["line"]
            if is_placeholder(line):
                continue
            for ref in SPEC_REF_RE.findall(line):
                ref = ref.strip()
                if "NNNN" in ref:
                    continue
                if not (root / "docs" / "specs" / f"{ref}.md").is_file():
                    report.erro(
                        "docs/TASKS.md",
                        "SPEC-REF-NAO-RESOLVE",
                        f"Referencia '(spec: {ref})' nao resolve para docs/specs/{ref}.md.",
                        ref,
                    )
    check_markers_values(sections, report)
    check_waiting(sections, report)
    check_evidence(root, sections, report)
    return seen, ids_done


def task_label(line):
    own = TASK_OWN_ID_RE.match(line)
    return f"T-{own.group(1)}" if own else f'"{line[:60]}"'


def check_markers_values(sections, report):
    """Marcador conhecido com valor fora do conjunto esperado vira AVISO."""
    today = date.today()
    for sec, tasks in sections.items():
        for task in tasks:
            line = task["line"]
            if is_placeholder(line):
                continue
            label = task_label(line)
            m = PRIORITY_RE.search(line)
            if m and normalize(m.group(1)) not in PRIORITIES:
                report.aviso(
                    "docs/TASKS.md",
                    "TASK-PRIORIDADE-INVALIDA",
                    f"{label} com '(prioridade: {m.group(1).strip()})' fora do "
                    "conjunto conhecido (alta | media | baixa).",
                    label,
                )
            m = VERIFICA_RE.search(line)
            if m and not squeeze(m.group(1)):
                report.erro(
                    "docs/TASKS.md",
                    "VERIFICA-COMANDO-VAZIO",
                    f"{label} declara '(verifica:)' sem comando.",
                    label,
                )
            m = BLOCKED_RE.search(line)
            if m:
                if sec != "aguardando usuario":
                    report.aviso(
                        "docs/TASKS.md",
                        "TASK-BLOQUEADA-FORA-DE-AGUARDANDO",
                        f"{label} usa '(bloqueada: ...)' fora de 'Aguardando Usuario'.",
                        label,
                    )
                blocked = parse_date(m.group(1))
                if blocked is None:
                    report.aviso(
                        "docs/TASKS.md",
                        "TASK-BLOQUEADA-FORMATO",
                        f"{label} com '(bloqueada: {m.group(1).strip()})' fora do "
                        "formato AAAA-MM-DD.",
                        label,
                    )
                else:
                    days = (today - blocked).days
                    if days > BLOCKED_MAX_DAYS:
                        report.aviso(
                            "docs/TASKS.md",
                            "TASK-BLOQUEADA-ANTIGA",
                            f"{label} bloqueada ha {days} dias (limite: "
                            f"{BLOCKED_MAX_DAYS}). Cobre a resposta ou feche a tarefa.",
                            label,
                        )
            for evidence in evidence_lines(task):
                m = EVIDENCE_TYPE_RE.search(evidence)
                if m and normalize(m.group(1)) not in EVIDENCE_TYPES:
                    report.aviso(
                        "docs/TASKS.md",
                        "EVIDENCIA-TIPO-INVALIDO",
                        f"{label} com 'tipo={m.group(1).strip()}' na evidencia, fora "
                        "do conjunto conhecido (comando | revisao-manual | conferencia).",
                        label,
                    )


def check_waiting(sections, report):
    """Tarefa em 'Aguardando Usuario' precisa registrar a pergunta que a travou."""
    for task in sections.get("aguardando usuario", []):
        line = task["line"]
        if is_placeholder(line):
            continue
        if not any(normalize(s).startswith("**pergunta:**") for s in task["sub"]):
            report.erro(
                "docs/TASKS.md",
                "AGUARDANDO-SEM-PERGUNTA",
                f"{task_label(line)} esta em 'Aguardando Usuario' sem a sub-linha "
                "'**Pergunta:**'. Sem a pergunta registrada, a espera nao e verificavel.",
                task_label(line),
            )
        if not any(normalize(s).startswith("**resposta:**") for s in task["sub"]):
            report.aviso(
                "docs/TASKS.md",
                "AGUARDANDO-SEM-RESPOSTA",
                f"{task_label(line)} esta em 'Aguardando Usuario' sem a sub-linha "
                "'**Resposta:**'.",
                task_label(line),
            )
        if not BLOCKED_RE.search(line):
            report.aviso(
                "docs/TASKS.md",
                "AGUARDANDO-SEM-BLOQUEADA",
                f"{task_label(line)} esta em 'Aguardando Usuario' sem marcador "
                "'(bloqueada: AAAA-MM-DD)'.",
                task_label(line),
            )


def check_evidence(root, sections, report):
    """Evidencia de fechamento em 'Concluidas'.

    `(verifica: <comando>)` declarado e contrato da propria tarefa: concluir sem
    o resultado desse comando e ERRO, independente de data. A evidencia em si e
    cobrada como AVISO, e so a partir da data declarada no marcador
    `(convencoes-2-2-0-desde:)` em TASKS.md; sem marcador, nada e cobrado
    (a regra nao e retroativa)."""
    adopted, declared = adoption_date(root)
    if declared and adopted is None:
        report.aviso(
            "docs/TASKS.md",
            "CONVENCOES-DATA-INVALIDA",
            "Marcador '(convencoes-2-2-0-desde:)' sem data valida; preencha com a "
            "data de adocao para que a evidencia de fechamento passe a ser cobrada.",
        )
    for task in sections.get("concluidas", []):
        line = task["line"]
        if is_placeholder(line):
            continue
        label = task_label(line)
        if TASK_OWN_ID_RE.match(line) and not DATE_PREFIX_RE.match(line):
            report.erro(
                "docs/TASKS.md",
                "TASK-CONCLUIDA-SEM-DATA",
                f"{label} em 'Concluidas' nao comeca com data AAAA-MM-DD.",
                label,
            )
        evidences = evidence_lines(task)
        done = DATE_PREFIX_RE.match(line)
        done_date = parse_date(done.group(1)) if done else None
        if adopted is not None and done_date is not None and done_date >= adopted:
            for evidence in evidences:
                invalid = []
                for field in ("tipo", "procedimento", "resultado"):
                    match = re.search(rf"\b{field}\s*=\s*([^;]*)", evidence)
                    if not match or not match.group(1).strip():
                        invalid.append(field)
                if invalid:
                    report.aviso(
                        "docs/TASKS.md",
                        "EVIDENCIA-FORMATO-INVALIDO",
                        f"{label} com evidencia sem campo preenchido: {', '.join(invalid)}.",
                        label,
                    )
        declared_cmd = VERIFICA_RE.search(line)
        if declared_cmd:
            command = squeeze(declared_cmd.group(1))
            joined = squeeze(" ".join(evidences))
            if not evidences:
                report.erro(
                    "docs/TASKS.md",
                    "EVIDENCIA-AUSENTE-COM-VERIFICA",
                    f"{label} declarou '(verifica: {command})' e foi concluida sem "
                    "sub-linha 'Evidencia:' com o resultado desse comando.",
                    label,
                )
            elif "resultado=" not in normalize(joined) or command not in joined:
                report.erro(
                    "docs/TASKS.md",
                    "EVIDENCIA-SEM-RESULTADO",
                    f"{label} declarou '(verifica: {command})', mas a evidencia nao "
                    "registra o resultado desse comando (esperado 'resultado=' "
                    "citando o comando declarado).",
                    label,
                )
            continue
        if evidences or adopted is None:
            continue
        if done_date is not None and done_date >= adopted:
            report.aviso(
                "docs/TASKS.md",
                "EVIDENCIA-AUSENTE",
                f"{label} concluida sem sub-linha 'Evidencia:' "
                "(tipo=; procedimento=; resultado=).",
                label,
            )


def archive_task_ids(root):
    ids = set()
    archive = root / "docs" / "archive"
    if archive.is_dir():
        for path in archive.glob("TASKS-*.md"):
            text = read(path)
            if text:
                ids.update(TASK_ID_RE.findall(strip_fences(text)))
    return ids


def check_specs(root, report, task_ids, done_ids):
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return
    archived = archive_task_ids(root)
    prefixes = {}
    for path in sorted(specs_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        rel = f"docs/specs/{path.name}"
        m = SPEC_NAME_RE.match(path.name)
        if not m:
            report.aviso(
                rel,
                "SPEC-NOME-INVALIDO",
                "Nome fora do padrao NNNN-slug.md (ex: 0001-login-social.md).",
                path.name,
            )
        else:
            prefix = m.group(1)
            if prefix in prefixes:
                report.erro(
                    rel,
                    "SPEC-PREFIXO-DUPLICADO",
                    f"Prefixo {prefix} duplicado (ja usado por {prefixes[prefix]}).",
                    path.name,
                )
            prefixes[prefix] = path.name
        text = read(path)
        if text is None:
            continue
        clean = strip_fences(text)
        # Check 11: Status valido
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)$", clean, re.MULTILINE)
        status = None
        if not status_match:
            report.erro(rel, "SPEC-SEM-STATUS", "Spec sem linha '**Status:**'.", path.name)
        else:
            status = normalize(status_match.group(1))
            if status not in SPEC_STATUSES:
                report.erro(
                    rel,
                    "SPEC-STATUS-INVALIDO",
                    f"Status invalido: '{status_match.group(1).strip()}' (esperado: "
                    "Rascunho | Definida | Em andamento | Concluida | Cancelada).",
                    path.name,
                )
        # Check 12: T-IDs da secao Tarefas existem
        tasks_section = re.search(
            r"^## Tarefas\s*$(.*?)(?=^## |\Z)", clean, re.MULTILINE | re.DOTALL
        )
        spec_ids = TASK_ID_RE.findall(tasks_section.group(1)) if tasks_section else []
        for tid in spec_ids:
            if tid not in task_ids and tid not in archived:
                report.erro(
                    rel,
                    "SPEC-TASK-INEXISTENTE",
                    f"T-{tid} listado na spec nao existe em docs/TASKS.md "
                    "nem em docs/archive/TASKS-*.md.",
                    f"T-{tid}",
                )
        # Check 13: spec concluida coerente
        if status == "concluida":
            pending = [
                tid
                for tid in spec_ids
                if tid in task_ids and tid not in done_ids and tid not in archived
            ]
            if pending:
                report.aviso(
                    rel,
                    "SPEC-CONCLUIDA-COM-PENDENTE",
                    "Spec Concluida com tarefas fora de 'Concluidas' em TASKS.md: "
                    + ", ".join(f"T-{t}" for t in pending)
                    + ".",
                    path.name,
                )
            evidence = re.search(
                r"^## Evidencia De Conclusao\s*$(.*?)(?=^## |\Z)",
                clean,
                re.MULTILINE | re.DOTALL,
            )
            if not evidence or not evidence.group(1).strip() or "(a preencher" in normalize(evidence.group(1)):
                report.aviso(
                    rel, "SPEC-CONCLUIDA-SEM-EVIDENCIA",
                    "Spec Concluida sem 'Evidencia De Conclusao' preenchida.",
                    path.name,
                )
        if tasks_section and re.search(
            r"^\s*-\s*T-\d+[^\n]*\(status:\s*[^)]*\)",
            tasks_section.group(1),
            re.MULTILINE | re.IGNORECASE,
        ):
            report.aviso(
                rel,
                "SPEC-TASK-COM-STATUS",
                "Spec registra status de tarefa na secao 'Tarefas'; o status vive so em TASKS.md.",
                path.name,
            )


def spec_overview(root, done_ids, archived):
    """Lista (nome, status, total, concluidas, perguntas abertas) por spec.

    Retorna None quando o modulo de specs nao esta ativo."""
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return None
    rows = []
    for path in sorted(specs_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = read(path)
        if text is None:
            continue
        clean = strip_fences(text)
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)$", clean, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else "(sem Status)"
        tasks_section = re.search(
            r"^## Tarefas\s*$(.*?)(?=^## |\Z)", clean, re.MULTILINE | re.DOTALL
        )
        spec_ids = TASK_ID_RE.findall(tasks_section.group(1)) if tasks_section else []
        done = sum(1 for tid in spec_ids if tid in done_ids or tid in archived)
        questions = re.search(
            r"^## Perguntas Abertas\s*$(.*?)(?=^## |\Z)", clean, re.MULTILINE | re.DOTALL
        )
        open_q = 0
        if questions:
            for line in questions.group(1).splitlines():
                line = line.strip()
                if line.startswith("- ") and not line[2:].lstrip().startswith("("):
                    open_q += 1
        rows.append((path.stem, status, len(spec_ids), done, open_q))
    return rows


def show_progress(root):
    """Projecao somente-leitura de tarefas e specs. Nunca altera arquivos."""
    print(f"Progresso de: {root}\n")
    sections = collect_tasks(root)
    if sections is None:
        print("docs/TASKS.md nao encontrado.")
        sections = {}

    def count(sec):
        return sum(1 for t in sections.get(sec, []) if not is_placeholder(t["line"]))

    done_ids = set()
    for task in sections.get("concluidas", []):
        own = TASK_OWN_ID_RE.match(task["line"])
        if own:
            done_ids.add(own.group(1))

    print("Tarefas (docs/TASKS.md):")
    print(f"  Em andamento: {count('em andamento')}")
    print(f"  Proximas:     {count('proximas tarefas')}")
    print(f"  Aguardando:   {count('aguardando usuario')}")
    print(f"  Concluidas:   {count('concluidas')}")
    print(f"  Ideias:       {count('ideias')}")

    rows = spec_overview(root, done_ids, archive_task_ids(root))
    print("\nSpecs (docs/specs/):")
    if rows is None:
        print("  (modulo de specs nao ativo)")
    elif not rows:
        print("  (nenhuma spec criada)")
    else:
        for name, status, total, done, open_q in rows:
            extra = f"  perguntas abertas: {open_q}" if open_q else ""
            print(f"  {name}  [{status}]  tarefas: {done}/{total} concluidas{extra}")

    print("\nProjecao somente-leitura; nada foi alterado. Sem a flag --progress, o script valida a estrutura.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Valida a estrutura Markdown multiagente (ai-project-structure)."
    )
    parser.add_argument(
        "caminho", nargs="?", default=".", help="Raiz do projeto (default: .)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Trata avisos como falha (exit 1)."
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Mostra projecao read-only de tarefas e specs; nao valida nem altera nada.",
    )
    parser.add_argument(
        "--codigos",
        action="store_true",
        help="Saida legivel por maquina (NIVEL|CODIGO|ARQUIVO|SUJEITO), uma linha "
             "por diagnostico, sem prosa. E o que um portao deve casar.",
    )
    args = parser.parse_args(argv)

    root = Path(args.caminho).resolve()
    if not root.is_dir():
        print(f"[ERRO] Caminho nao encontrado: {root}")
        return 1

    if args.progress:
        show_progress(root)
        return 0

    if not args.codigos:
        print(f"Validando estrutura em: {root}")
    report = Report()
    check_core_files(root, report)
    check_em_dash(root, report)
    check_unclosed_fences(root, report)
    check_bridges(root, report)
    check_markers(root, report)
    check_session(root, report)
    check_consensus(root, report, adoption_date(root)[0])
    task_ids, done_ids = check_tasks(root, report)
    check_specs(root, report, task_ids, done_ids)
    if args.codigos:
        report.print_codigos()
    else:
        report.print()

    errors, warnings = report.counts()
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
