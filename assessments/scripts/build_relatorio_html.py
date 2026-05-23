"""Gera assessments/relatorio_rodrigo_didier.html a partir do .md homônimo,
embutindo a imagem correlation_matrix.png como data URI base64 para que o
arquivo seja totalmente auto-contido.

Uso (na raiz do repo, com o venv ativo):
    uv run python assessments/scripts/build_relatorio_html.py
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # → assessments/
MD_PATH = BASE / "relatorio_rodrigo_didier.md"
PNG_PATH = BASE / "correlation_matrix.png"
HTML_PATH = BASE / "relatorio_rodrigo_didier.html"


def render_inline(text: str) -> str:
    """Escapa HTML e aplica formatações inline: **negrito** e `código`."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def md_to_html_body(md: str, png_data_uri: str) -> str:
    """Conversão Markdown→HTML minimalista suficiente para este relatório."""
    html_lines: list[str] = []
    lines = md.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Imagem ![alt](path) — substitui a referência ao correlation_matrix.png
        # pelo data URI inline, para que o HTML seja auto-contido.
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if m:
            alt, src = m.group(1), m.group(2)
            if src.endswith("correlation_matrix.png"):
                src = png_data_uri
            html_lines.append(
                f'<figure><img src="{src}" alt="{alt}"/><figcaption>{alt}</figcaption></figure>'
            )
            i += 1
            continue

        # Cabeçalhos
        if line.startswith("### "):
            html_lines.append(f"<h3>{render_inline(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("## "):
            html_lines.append(f"<h2>{render_inline(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("# "):
            html_lines.append(f"<h1>{render_inline(line[2:].strip())}</h1>")
            i += 1
            continue

        # Separador horizontal
        if line.strip() == "---":
            html_lines.append("<hr/>")
            i += 1
            continue

        # Tabelas GFM
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.search(
            r"\|\s*:?-{2,}", lines[i + 1]
        ):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            html_lines.append("<table>")
            html_lines.append(
                "<thead><tr>"
                + "".join(f"<th>{render_inline(c)}</th>" for c in header_cells)
                + "</tr></thead>"
            )
            html_lines.append("<tbody>")
            for row in rows:
                html_lines.append(
                    "<tr>"
                    + "".join(f"<td>{render_inline(c)}</td>" for c in row)
                    + "</tr>"
                )
            html_lines.append("</tbody></table>")
            continue

        # Blockquote
        if line.startswith("> "):
            buf = [render_inline(line[2:])]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(render_inline(lines[i][2:]))
                i += 1
            html_lines.append("<blockquote>" + "<br>".join(buf) + "</blockquote>")
            continue

        # Listas numeradas
        if re.match(r"^\d+\.\s+", line):
            html_lines.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                item = re.sub(r"^\d+\.\s+", "", lines[i])
                html_lines.append(f"<li>{render_inline(item)}</li>")
                i += 1
            html_lines.append("</ol>")
            continue

        # Listas com marcadores
        if line.startswith("- "):
            html_lines.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                html_lines.append(f"<li>{render_inline(lines[i][2:])}</li>")
                i += 1
            html_lines.append("</ul>")
            continue

        # Linha em branco
        if not line.strip():
            i += 1
            continue

        # Parágrafo
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not (
            lines[i].startswith(("#", "- ", "> ", "|"))
            or lines[i].strip() == "---"
            or re.match(r"^\d+\.\s+", lines[i])
            or re.match(r"!\[", lines[i].strip())
        ):
            buf.append(lines[i])
            i += 1
        html_lines.append("<p>" + render_inline(" ".join(buf)) + "</p>")

    return "\n".join(html_lines)


CSS = """
:root { color-scheme: light; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 1.5rem;
    line-height: 1.6;
    color: #1f2328;
    background: #ffffff;
}
h1 { border-bottom: 2px solid #d0d7de; padding-bottom: 0.3em; }
h2 { border-bottom: 1px solid #d0d7de; padding-bottom: 0.2em; margin-top: 2.2em; }
h3 { margin-top: 1.8em; }
code {
    background: #f6f8fa;
    padding: 0.15em 0.35em;
    border-radius: 4px;
    font-size: 0.92em;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
table { border-collapse: collapse; margin: 1em 0; width: 100%; }
th, td {
    border: 1px solid #d0d7de;
    padding: 0.5em 0.75em;
    text-align: left;
    vertical-align: top;
    font-size: 0.92em;
}
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(even) td { background: #fafbfc; }
blockquote {
    border-left: 4px solid #d0d7de;
    margin: 1em 0;
    padding: 0.5em 1em;
    color: #57606a;
    background: #f6f8fa;
    border-radius: 0 4px 4px 0;
}
figure { margin: 1.5em 0; text-align: center; }
figure img {
    max-width: 100%;
    height: auto;
    border: 1px solid #d0d7de;
    border-radius: 6px;
}
figcaption {
    font-size: 0.85em;
    color: #57606a;
    margin-top: 0.5em;
    font-style: italic;
}
ol, ul { padding-left: 1.6em; }
li { margin: 0.2em 0; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 2em 0; }
strong { color: #1f2328; }
"""


def main() -> None:
    md = MD_PATH.read_text(encoding="utf-8")
    png_b64 = base64.b64encode(PNG_PATH.read_bytes()).decode("ascii")
    data_uri = f"data:image/png;base64,{png_b64}"

    body = md_to_html_body(md, data_uri)

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<title>Relatório — Atividade Avaliativa 01 — Rodrigo Didier</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
    HTML_PATH.write_text(html, encoding="utf-8")
    size_kb = HTML_PATH.stat().st_size // 1024
    print(f"OK — gerado {HTML_PATH} ({size_kb} KB)")


if __name__ == "__main__":
    main()
