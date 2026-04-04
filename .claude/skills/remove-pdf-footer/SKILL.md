---
name: remove-pdf-footer
description: PDF 파일의 각 페이지 하단에서 페이지 번호와 저작권 문구를 제거한다. raw/ 폴더의 PDF를 처리해 output/ 폴더에 저장.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob
---

PDF 하단 텍스트(페이지 번호 + 저작권 문구) 제거 작업을 수행합니다.

## 작업 순서

1. **pymupdf 설치 확인 및 설치**

```bash
pip install pymupdf -q
```

2. **raw/ 폴더에 PDF가 있는지 확인**

`raw/` 폴더에 처리할 PDF 파일이 있는지 확인하세요. 없다면 사용자에게 안내합니다.

3. **remove_footer.py 스크립트 실행**

```bash
python remove_footer.py
```

4. **결과 확인**

`output/` 폴더에 저장된 파일 목록을 보여주고, 처리된 페이지 수와 함께 완료를 안내합니다.

## 커스터마이징

저작권 문구가 다른 경우 `remove_footer.py`의 `COPYRIGHT_TEXT` 변수를 수정하세요:

```python
COPYRIGHT_TEXT = "여기에 삭제할 문구 입력"
```

## 참고

- 원본 파일(`raw/`)은 변경되지 않습니다.
- 처리 결과는 `output/` 폴더에 원본과 동일한 파일명으로 저장됩니다.
