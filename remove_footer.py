import fitz  # pymupdf
import os
from pathlib import Path

INPUT_DIR = Path("raw")
OUTPUT_DIR = Path("output")
COPYRIGHT_TEXT = "이 자료는 저작권의 보호를 받는"

OUTPUT_DIR.mkdir(exist_ok=True)

for pdf_path in INPUT_DIR.glob("*.pdf"):
    doc = fitz.open(pdf_path)
    print(f"처리 중: {pdf_path.name} ({len(doc)}페이지)")

    for page in doc:
        page_height = page.rect.height
        footer_y_start = page_height * 0.9  # 하단 10% 영역

        # 1. 저작권 문구 제거
        rects = page.search_for(COPYRIGHT_TEXT)
        for rect in rects:
            # 해당 줄 전체를 커버하도록 x 범위 확장
            full_rect = fitz.Rect(0, rect.y0, page.rect.width, rect.y1)
            page.add_redact_annot(full_rect, fill=(1, 1, 1))

        # 2. 페이지 번호 제거 (하단 10% 영역 내 숫자 블록)
        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            text = text.strip()
            # 하단 영역에 있고, 숫자로만 이루어진 짧은 텍스트
            if y0 >= footer_y_start and text.isdigit() and len(text) <= 3:
                rect = fitz.Rect(x0, y0, x1, y1)
                page.add_redact_annot(rect, fill=(1, 1, 1))

        page.apply_redactions()

    output_path = OUTPUT_DIR / pdf_path.name
    doc.save(output_path)
    doc.close()
    print(f"  → 저장: {output_path}")

print("\n완료! output/ 폴더를 확인하세요.")
