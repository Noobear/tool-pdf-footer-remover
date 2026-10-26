---
name: pdf-footer-remover
description: PDF 각 페이지 하단의 페이지 번호와 저작권 문구(예 "이 자료는 저작권의 보호를 받는 … (SV-XXXXX)")를 지운 사본을 만든다. 사용자가 PDF의 하단 문구·쪽번호·워터마크성 꼬리말을 없애 달라고 할 때 쓴다. 설치된 CLI `pdf-footer-remover`를 실행한다.
allowed-tools: Bash, Read, Glob
---

`pdf-footer-remover`는 도구 장부(ops-control `tools/toolbox`)로 이 기기에 설치된 CLI다. 레포를 clone하거나 pip로 설치하지 말 것.

## 순서

1. 대상 PDF 경로를 확인한다(파일 또는 폴더). 결과는 원본과 다른 폴더에 쓴다.
2. 실행:

```bash
pdf-footer-remover <파일 또는 폴더>... -o <결과 폴더>
```

- 지울 문구가 기본(`이 자료는 저작권의 보호를 받는`)과 다르면 `-t "<문구>"`를 준다. 여러 번 줄 수 있고, 그 문구가 있는 줄 전체가 지워진다.
- 페이지 번호는 남기려면 `--keep-page-numbers`.
- 번호가 하단 10%보다 위에 있으면 `--band 0.15`처럼 넓힌다.
3. 출력 줄의 "N곳 지움"이 0인 파일은 문구가 다르거나 텍스트가 아닌 이미지일 수 있다. 결과 PDF의 마지막 쪽 텍스트를 읽어 확인하고 사용자에게 알린다.

## 알아둘 것

- 원본은 바꾸지 않는다. 결과 폴더가 원본과 같으면 거부한다(exit 2). PDF가 없으면 exit 1.
- 텍스트를 덮는 게 아니라 지운다(redaction). 스캔 이미지에 박힌 글자는 지우지 못한다.
- 도구가 없다고 나오면 사용자에게 ops-control `tools/toolbox/toolbox.py sync`를 안내한다.
