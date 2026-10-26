from pathlib import Path

import pymupdf
import pytest

from pdf_footer_remover import DEFAULT_TEXT, main

BODY = "본문은 그대로 남는다"
FOOTER = DEFAULT_TEXT + " 자료입니다. (SV-12345)"


def make_pdf(path: Path, pages: int = 2) -> None:
    doc = pymupdf.open()
    for n in range(1, pages + 1):
        page = doc.new_page(width=595, height=842)
        page.insert_text((72, 100), BODY, fontname="korea", fontsize=12)
        page.insert_text((60, 800), FOOTER, fontname="korea", fontsize=8)
        page.insert_text((292, 825), str(n), fontsize=10)
    doc.save(path)


def text_of(path: Path) -> list[str]:
    with pymupdf.open(path) as doc:
        return [page.get_text() for page in doc]


def test_removes_footer_and_page_numbers_keeps_body(tmp_path: Path) -> None:
    raw = tmp_path / "raw"; raw.mkdir()
    make_pdf(raw / "a.pdf")
    assert main([str(raw), "-o", str(tmp_path / "out")]) == 0
    for page in text_of(tmp_path / "out" / "a.pdf"):
        assert BODY in page
        assert "저작권" not in page and "SV-12345" not in page
        assert not any(line.strip().isdigit() for line in page.splitlines())
    # the input is untouched
    assert all(DEFAULT_TEXT in page for page in text_of(raw / "a.pdf"))


def test_keep_page_numbers_and_custom_text(tmp_path: Path) -> None:
    make_pdf(tmp_path / "b.pdf", pages=1)
    assert main([str(tmp_path / "b.pdf"), "-o", str(tmp_path / "out"), "--keep-page-numbers", "-t", "SV-12345"]) == 0
    page = text_of(tmp_path / "out" / "b.pdf")[0]
    assert "SV-12345" not in page and "1" in page.split()


def test_refuses_to_overwrite_and_reports_no_input(tmp_path: Path) -> None:
    make_pdf(tmp_path / "c.pdf", pages=1)
    assert main([str(tmp_path / "c.pdf"), "-o", str(tmp_path)]) == 2
    assert main([str(tmp_path / "missing")]) == 1


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    assert "pdf-footer-remover 0.1.0" in capsys.readouterr().out
