# Utils/sanitization.py
from __future__ import annotations
import re
import textwrap


def normalize_text(
    s: str,
    *,
    tabsize: int = 4,
    collapse_blank: bool = True,
) -> str:
    # 1) BOM
    s = s.lstrip("\ufeff")
    # 2) newline → LF
    s = s.replace("\r\n", "\n").replace("\r", "\n")

    lines = s.split("\n")

    # 3) espandi TAB solo in indentazione
    def expand_leading_tabs(line: str) -> str:
        m = re.match(r"^([ \t]+)", line)
        if not m:
            return line
        lead = m.group(1).replace("\t", " " * tabsize)
        return lead + line[len(m.group(1)) :]

    lines = [expand_leading_tabs(l) for l in lines]

    # 4) trim trailing spaces
    lines = [re.sub(r"[ \t]+$", "", l) for l in lines]

    # 5) dedent comune - ma solo se non tutte le righe non-vuote iniziano con tab (prima dell'espansione)
    # Se tutte le righe avevano solo tab leading, significa che l'indentazione è intenzionale
    original_lines = s.split("\n")
    all_leading_tabs = all(
        line.strip() == ""  # linea vuota
        or (line and not line[0].isspace())  # nessun leading whitespace
        or line[0] == "\t"  # inizia con tab
        for line in original_lines
    )

    s = "\n".join(lines)
    if not all_leading_tabs:
        s = textwrap.dedent(s)

    # 6) ricostruisci la stringa
    lines = s.split("\n")

    # 7) comprimi righe vuote e taglia inizio/fine
    lines = s.split("\n")
    # rimuovi vuote all'inizio/fine
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    if collapse_blank:
        out = []
        prev_blank = False
        for l in lines:
            blank = l.strip() == ""
            if blank and prev_blank:
                continue
            out.append(l)
            prev_blank = blank
        lines = out

    # 8) newline finale
    return "\n".join(lines) + "\n"
