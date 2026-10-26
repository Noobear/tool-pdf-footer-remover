# pdf-footer-remover

PDF 각 페이지 하단의 **페이지 번호**와 **문구**(예: `이 자료는 저작권의 보호를 받는 … (SV-XXXXX)`)를 지운 사본을 만든다. 글자를 흰 상자로 덮는 게 아니라 페이지에서 지우므로(redaction) 검색·복사에도 남지 않는다. 원본은 바꾸지 않는다.

## 설치

도구 장부(ops-control `tools/toolbox`)가 네 기기에 설치한다. 손으로 설치하려면:

```bash
uv tool install git+ssh://git@github.com/Noobear/tool-pdf-footer-remover@v0.1.1
```

## 사용

```bash
pdf-footer-remover                              # raw/ 의 PDF → output/ (예전 동작)
pdf-footer-remover 강의자료.pdf 2주차/ -o 정리본/   # 파일·폴더 여러 개
pdf-footer-remover a.pdf -o out -t "무단 복제 금지"  # 다른 문구 (여러 번 가능)
pdf-footer-remover a.pdf -o out --keep-page-numbers
pdf-footer-remover a.pdf -o out --band 0.15      # 번호를 찾는 하단 범위 (기본 10%)
```

파일마다 `N쪽, M곳 지움`을 출력한다. M이 0이면 문구가 다르거나 글자가 이미지다.

- 문구: 지정한 문구가 있는 **줄 전체**(가로 폭 전부)를 지운다. 문구 뒤의 코드도 함께 사라진다.
- 페이지 번호: 하단 범위 안의, 숫자만으로 된 4자리 이하 블록.
- 결과 폴더가 원본 위치와 같으면 거부한다(exit 2). PDF가 없으면 exit 1.

## 에이전트

`skill/SKILL.md`가 이 도구의 사용 안내다. 도구 장부가 각 기기의 `~/.agents/skills/pdf-footer-remover/`(Claude Code는 `~/.claude/skills/`에 링크)로 설치하므로, 어느 레포에서 일하는 에이전트든 "PDF 하단 문구 지워 줘"에 이 도구를 쓴다.

## 개발

```bash
uv run --group dev pytest -q     # 실제 PDF를 만들어 지우고 확인하는 검사
```

바꾼 뒤에는 `pyproject.toml`의 version을 올리고 같은 이름의 태그(`v0.1.1`)를 push한 다음, ops-control 장부의 버전을 바꾼다.
