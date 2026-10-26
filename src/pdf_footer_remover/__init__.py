"""Remove page numbers and a footer line from every page of PDF files.

The text is redacted (removed from the page content), not covered, so it no longer
appears in search or copy. The input files are never changed.
"""
from __future__ import annotations

import argparse
import sys
from importlib.metadata import version
from pathlib import Path

import pymupdf

DEFAULT_TEXT = "이 자료는 저작권의 보호를 받는"


def clean_page(page: pymupdf.Page, texts: list[str], page_numbers: bool, band: float) -> int:
    """Mark the footer lines and the bottom page number for redaction and apply it; returns the count."""
    marks = 0
    for text in texts:
        for rect in page.search_for(text):
            # the whole line, so a code after the phrase (SV-XXXXX) goes with it
            page.add_redact_annot(pymupdf.Rect(0, rect.y0, page.rect.width, rect.y1), fill=(1, 1, 1))
            marks += 1
    if page_numbers:
        bottom = page.rect.height * (1 - band)
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            text = text.strip()
            if y0 >= bottom and text.isdigit() and len(text) <= 4:
                page.add_redact_annot(pymupdf.Rect(x0, y0, x1, y1), fill=(1, 1, 1))
                marks += 1
    if marks:
        page.apply_redactions()
    return marks


def clean_pdf(source: Path, target: Path, texts: list[str], page_numbers: bool = True, band: float = 0.1) -> tuple[int, int]:
    """Write a cleaned copy of `source` to `target`; returns (pages, removed marks)."""
    with pymupdf.open(source) as doc:
        removed = sum(clean_page(page, texts, page_numbers, band) for page in doc)
        target.parent.mkdir(parents=True, exist_ok=True)
        doc.save(target, garbage=3, deflate=True)
        return len(doc), removed


def collect(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(sorted(p for p in path.glob("*.pdf") if p.is_file()))
        elif path.suffix.lower() == ".pdf" and path.is_file():
            found.append(path)
        else:
            print(f"건너뜀(PDF 아님 또는 없음): {path}", file=sys.stderr)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pdf-footer-remover", description="PDF 각 페이지 하단의 페이지 번호와 문구를 지운 사본을 만든다. 원본은 바꾸지 않는다.")
    parser.add_argument("paths", nargs="*", type=Path, default=[Path("raw")], help="PDF 파일 또는 폴더 (기본: raw/)")
    parser.add_argument("-o", "--output", type=Path, default=Path("output"), help="결과 폴더 (기본: output/)")
    parser.add_argument("-t", "--text", action="append", help=f"지울 문구, 여러 번 가능 (기본: '{DEFAULT_TEXT}')")
    parser.add_argument("--keep-page-numbers", action="store_true", help="페이지 번호는 남긴다")
    parser.add_argument("--band", type=float, default=0.1, help="페이지 번호를 찾을 하단 비율 (기본 0.1 = 아래 10%%)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version('pdf-footer-remover')}")
    args = parser.parse_args(argv)

    pdfs = collect(args.paths)
    if not pdfs:
        print("처리할 PDF가 없습니다.", file=sys.stderr)
        return 1
    texts = args.text or [DEFAULT_TEXT]
    output = args.output.resolve()
    for pdf in pdfs:
        target = output / pdf.name
        if target == pdf.resolve():
            print(f"원본을 덮어쓰지 않습니다: {pdf}", file=sys.stderr)
            return 2
        pages, removed = clean_pdf(pdf, target, texts, not args.keep_page_numbers, args.band)
        print(f"{pdf.name}: {pages}쪽, {removed}곳 지움 → {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
