"""Gera assessments/relatorio_rodrigo_didier.pdf a partir do .html homônimo,
usando Google Chrome em modo headless. Não requer libs Python extras.

Pré-requisito: o .html já deve existir (gerar antes com build_relatorio_html.py).

Uso (na raiz do repo):
    uv run python assessments/scripts/build_relatorio_pdf.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # → assessments/
HTML_PATH = BASE / "relatorio_rodrigo_didier.html"
PDF_PATH = BASE / "relatorio_rodrigo_didier.pdf"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    for name in ("google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("ERRO: nenhum binário tipo Chrome encontrado. Instale Chrome ou Chromium.")


def main() -> None:
    if not HTML_PATH.exists():
        sys.exit(
            f"ERRO: {HTML_PATH} não existe. Rode build_relatorio_html.py primeiro."
        )

    chrome = find_chrome()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not PDF_PATH.exists():
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(f"ERRO: Chrome retornou {result.returncode} e o PDF não foi gerado.")

    size_kb = PDF_PATH.stat().st_size // 1024
    print(f"OK — gerado {PDF_PATH} ({size_kb} KB)")


if __name__ == "__main__":
    main()
