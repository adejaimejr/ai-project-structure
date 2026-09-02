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

MARKER_RE = re.compile(
    r"<!--\s*ai-project-structure:(core|specs):(start|end)(?:\s+v(\S+))?\s*-->"
)
ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}", re.MULTILINE)
TASK_ID_RE = re.compile(r"\bT-(\d+)\b")
# ID proprio da tarefa: o que abre a linha, depois da data quando ela e concluida.
# Qualquer outro T-NNN no texto e referencia a outra tarefa, nao um segundo ID.
TASK_OWN_ID_RE = re.compile(r"^(?:\d{4}-\d{2}-\d{2}\s+)?T-(\d+)\b")
SPEC_REF_RE = re.compile(r"\(spec:\s*([^)]+)\)")
SPEC_NAME_RE = re.compile(r"^(\d{4})-[a-z0-9][a-z0-9-]*\.md$")
PRIORITY_RE = re.compile(r"\(prioridade:\s*([^)]*)\)")
VERIFICA_RE = re.compile(r"\(verifica:\s*([^)]*)\)")
BLOCKED_RE = re.compile(r"\(bloqueada:\s*([^)]*)\)")
ADOPTION_RE = re.compile(r"\(convencoes-2-2-0-desde:\s*([^)]*)\)")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\b")
EVIDENCE_TYPE_RE = re.compile(r"\btipo\s*=\s*([^;]+)")
ROTATION_MAX_ENTRIES = 20
ROTATION_MAX_BYTES = 30 * 1024
BLOCKED_MAX_DAYS = 30
CONSENSUS_MAX_ROUNDS = 3


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


class Report:
    def __init__(self):
        self.items = {}  # arquivo -> [(nivel, mensagem)]

    def add(self, level, file, message):
        self.items.setdefault(file, []).append((level, message))

    def erro(self, file, message):
        self.add("ERRO", file, message)

    def aviso(self, file, message):
        self.add("AVISO", file, message)

    def info(self, file, message):
        self.add("INFO", file, message)

    def counts(self):
        errors = sum(1 for msgs in self.items.values() for lvl, _ in msgs if lvl == "ERRO")
        warnings = sum(1 for msgs in self.items.values() for lvl, _ in msgs if lvl == "AVISO")
        return errors, warnings

    def print(self):
        if not self.items:
            print("Nenhum problema encontrado.")
        for file in sorted(self.items):
            print(f"\n{file}")
            for level, message in self.items[file]:
                print(f"  [{level}] {message}")
        errors, warnings = self.counts()
        print(f"\nResumo: {errors} erros, {warnings} avisos.")


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
        if not (root / rel).is_file():
            report.erro(rel, "Arquivo do nucleo ausente.")


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
                f"Contem travessao (em dash, U+2014) {count}x; proibido pela regra "
                "do projeto. Use dois-pontos, virgula, parenteses ou hifen simples.",
            )


def check_bridges(root, report):
    for rel in ("CLAUDE.md", "GEMINI.md"):
        text = read(root / rel)
        if text is not None and "AGENTS.md" not in text:
            report.aviso(rel, "Arquivo-ponte nao menciona AGENTS.md (ponte quebrada?).")


def check_markers(root, report):
    text = read(root / "AGENTS.md")
    if text is None:
        return
    found = {}  # bloco -> {"start": [versoes], "end": contagem}
    for m in MARKER_RE.finditer(text):
        block, kind, version = m.group(1), m.group(2), m.group(3)
        entry = found.setdefault(block, {"start": [], "end": 0})
        if kind == "start":
            entry["start"].append(version)
        else:
            entry["end"] += 1
    if not found:
        report.info(
            "AGENTS.md",
            "Estrutura v1 detectada (sem bloco gerenciado). "
            "Rode a skill ai-project-structure para atualizar.",
        )
        return
    for block, entry in found.items():
        starts, ends = entry["start"], entry["end"]
        if len(starts) != 1 or ends != 1:
            report.erro(
                "AGENTS.md",
                f"Marcadores do bloco '{block}' despareados "
                f"({len(starts)} start, {ends} end). Esperado exatamente 1 de cada.",
            )
            continue
        version = starts[0]
        if not version or not re.fullmatch(r"v?\d+\.\d+\.\d+", version):
            report.erro(
                "AGENTS.md",
                f"Versao ausente ou invalida no marcador do bloco '{block}' "
                f"(esperado ex: 'v2.0.0', encontrado: {version!r}).",
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
                f"Entrada '{title}' sem os headings: {', '.join(missing)}.",
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
            report.aviso(rel, f"Entrada '{title}' sem linha '**{label}:**'.")
        elif normalize(value) not in allowed:
            report.aviso(
                rel,
                f"Entrada '{title}' com '**{label}:** {value}' fora do conjunto "
                f"({' | '.join(sorted(allowed))}).",
            )
    rodada = field_value(body, "Rodada")
    if rodada is None:
        return
    m = re.match(r"(\d+)\s*de\s*(\d+)", normalize(rodada))
    if not m:
        report.aviso(
            rel,
            f"Entrada '{title}' com '**Rodada:** {rodada}' fora do formato "
            f"'N de {CONSENSUS_MAX_ROUNDS}'.",
        )
    elif int(m.group(1)) > CONSENSUS_MAX_ROUNDS and not re.search(
        r"\*\*Pr[oó]ximo passo:\*\*", body
    ):
        report.aviso(
            rel,
            f"Entrada '{title}' passou do teto de {CONSENSUS_MAX_ROUNDS} rodadas "
            "sem '**Proximo passo:**' escalando para o usuario.",
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
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)$", body, re.MULTILINE)
        if not status_match:
            report.aviso(
                "docs/CONSENSUS.md", f"Entrada '{title}' sem linha '**Status:**'."
            )
            continue
        status = normalize(status_match.group(1))
        if status not in CONSENSUS_STATUSES:
            report.aviso(
                "docs/CONSENSUS.md",
                f"Entrada '{title}' com Status invalido: '{status_match.group(1).strip()}' "
                "(esperado: aberto | resolvido | arquivado).",
            )
        elif status == "aberto" and not re.search(
            r"\*\*Pr[oó]ximo passo:\*\*", body
        ):
            report.aviso(
                "docs/CONSENSUS.md",
                f"Entrada '{title}' esta aberta sem '**Proximo passo:**' com dono.",
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
            ids = [own.group(1)] if own else []
            # Unicidade vale no arquivo todo (inclusive Ideias e Concluidas).
            all_ids.extend(ids)
            if sec == "concluidas":
                ids_done.update(ids)
            if sec in open_sections:
                any_line = True
                if not ids:
                    lines_without_id.append((sec, line))
    # Check 7: unicidade
    seen = set()
    for tid in all_ids:
        if tid in seen:
            report.erro("docs/TASKS.md", f"ID duplicado: T-{tid}.")
        seen.add(tid)
    # Check 8: formato v1 vs misto
    if any_line and not all_ids and lines_without_id:
        report.info(
            "docs/TASKS.md",
            "Nenhuma tarefa usa ID T-NNN (formato v1). "
            "A skill pode migrar os IDs no fluxo de atualizacao.",
        )
    elif all_ids and lines_without_id:
        for sec, line in lines_without_id:
            report.aviso(
                "docs/TASKS.md",
                f"Tarefa sem ID T-NNN na secao '{sec}': \"{line[:60]}\".",
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
                        f"Referencia '(spec: {ref})' nao resolve para docs/specs/{ref}.md.",
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
                    f"{label} com '(prioridade: {m.group(1).strip()})' fora do "
                    "conjunto conhecido (alta | media | baixa).",
                )
            m = BLOCKED_RE.search(line)
            if m:
                blocked = parse_date(m.group(1))
                if blocked is None:
                    report.aviso(
                        "docs/TASKS.md",
                        f"{label} com '(bloqueada: {m.group(1).strip()})' fora do "
                        "formato AAAA-MM-DD.",
                    )
                else:
                    days = (today - blocked).days
                    if days > BLOCKED_MAX_DAYS:
                        report.aviso(
                            "docs/TASKS.md",
                            f"{label} bloqueada ha {days} dias (limite: "
                            f"{BLOCKED_MAX_DAYS}). Cobre a resposta ou feche a tarefa.",
                        )
            for evidence in evidence_lines(task):
                m = EVIDENCE_TYPE_RE.search(evidence)
                if m and normalize(m.group(1)) not in EVIDENCE_TYPES:
                    report.aviso(
                        "docs/TASKS.md",
                        f"{label} com 'tipo={m.group(1).strip()}' na evidencia, fora "
                        "do conjunto conhecido (comando | revisao-manual | conferencia).",
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
                f"{task_label(line)} esta em 'Aguardando Usuario' sem a sub-linha "
                "'**Pergunta:**'. Sem a pergunta registrada, a espera nao e verificavel.",
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
        report.info(
            "docs/TASKS.md",
            "Marcador '(convencoes-2-2-0-desde:)' sem data valida; preencha com a "
            "data de adocao para que a evidencia de fechamento passe a ser cobrada.",
        )
    for task in sections.get("concluidas", []):
        line = task["line"]
        if is_placeholder(line):
            continue
        label = task_label(line)
        evidences = evidence_lines(task)
        declared_cmd = VERIFICA_RE.search(line)
        if declared_cmd:
            command = squeeze(declared_cmd.group(1))
            joined = squeeze(" ".join(evidences))
            if not evidences:
                report.erro(
                    "docs/TASKS.md",
                    f"{label} declarou '(verifica: {command})' e foi concluida sem "
                    "sub-linha 'Evidencia:' com o resultado desse comando.",
                )
            elif "resultado=" not in normalize(joined) or command not in joined:
                report.erro(
                    "docs/TASKS.md",
                    f"{label} declarou '(verifica: {command})', mas a evidencia nao "
                    "registra o resultado desse comando (esperado 'resultado=' "
                    "citando o comando declarado).",
                )
            continue
        if evidences or adopted is None:
            continue
        done = DATE_PREFIX_RE.match(line)
        done_date = parse_date(done.group(1)) if done else None
        if done_date is not None and done_date >= adopted:
            report.aviso(
                "docs/TASKS.md",
                f"{label} concluida sem sub-linha 'Evidencia:' "
                "(tipo=; procedimento=; resultado=).",
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
                "Nome fora do padrao NNNN-slug.md (ex: 0001-login-social.md).",
            )
        else:
            prefix = m.group(1)
            if prefix in prefixes:
                report.erro(
                    rel,
                    f"Prefixo {prefix} duplicado (ja usado por {prefixes[prefix]}).",
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
            report.erro(rel, "Spec sem linha '**Status:**'.")
        else:
            status = normalize(status_match.group(1))
            if status not in SPEC_STATUSES:
                report.erro(
                    rel,
                    f"Status invalido: '{status_match.group(1).strip()}' (esperado: "
                    "Rascunho | Definida | Em andamento | Concluida | Cancelada).",
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
                    f"T-{tid} listado na spec nao existe em docs/TASKS.md "
                    "nem em docs/archive/TASKS-*.md.",
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
                    "Spec Concluida com tarefas fora de 'Concluidas' em TASKS.md: "
                    + ", ".join(f"T-{t}" for t in pending)
                    + ".",
                )
            evidence = re.search(
                r"^## Evidencia De Conclusao\s*$(.*?)(?=^## |\Z)",
                clean,
                re.MULTILINE | re.DOTALL,
            )
            if not evidence or "(a preencher" in normalize(evidence.group(1)):
                report.aviso(
                    rel, "Spec Concluida sem 'Evidencia De Conclusao' preenchida."
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
    args = parser.parse_args(argv)

    root = Path(args.caminho).resolve()
    if not root.is_dir():
        print(f"[ERRO] Caminho nao encontrado: {root}")
        return 1

    if args.progress:
        show_progress(root)
        return 0

    print(f"Validando estrutura em: {root}")
    report = Report()
    check_core_files(root, report)
    check_em_dash(root, report)
    check_bridges(root, report)
    check_markers(root, report)
    check_session(root, report)
    check_consensus(root, report, adoption_date(root)[0])
    task_ids, done_ids = check_tasks(root, report)
    check_specs(root, report, task_ids, done_ids)
    report.print()

    errors, warnings = report.counts()
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
