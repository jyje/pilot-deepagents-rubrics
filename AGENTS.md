# AGENTS.md — Project Context for AI Agents

> Updated: 2026-06-03

## 프로젝트 목적

Anthropic Claude를 AI 공급자로 사용하여 LangChain DeepAgents의 `RubricMiddleware`를 실행하는 파일럿 프로젝트.
에이전트 출력물을 루브릭 기준으로 자동 채점하고 재시도하는 미들웨어의 동작을 코드 레벨에서 검증한다.

## 현재 상태 (2026-06-03) — 완료

모든 목표 달성. 초기 커밋 완료: `🎉 init(deepagents-rubrics): initial commit`

## 프로젝트 구조

```
pilot-deepagents-rubrics/
├── README.md / README-ko.md       ← 프로젝트 문서 (EN/KO, 간결 버전)
├── AGENTS.md                      ← 이 파일: AI 에이전트용 컨텍스트
├── LICENSE                        ← MIT
├── .vscode/settings.json          ← IDE Python 인터프리터 설정
├── docs/                          ← 분석 문서 및 설정 가이드
│   ├── README.md                  ← 문서 인덱스 (EN/KO)
│   ├── 00-research-plan(-ko).md   ← 리서치 목표 및 핵심 질문
│   ├── 01-overview(-ko).md        ← RubricMiddleware 개념 및 동작 원리
│   ├── 02-api-reference(-ko).md   ← API 클래스 레퍼런스
│   ├── 03-anthropic-setup(-ko).md ← Anthropic API 설정 가이드
│   ├── 04-langgraph-studio(-ko).md← LangGraph Studio 실행 가이드
│   ├── 05-lmstudio(-ko).md        ← LM Studio 로컬 무료 대안
│   └── result.txt                 ← 검증 실행 결과 (3회 루프, satisfied)
└── src/                           ← 모든 소스 코드 (uv 관리)
    ├── .env.sample                ← 환경변수 템플릿
    ├── .env                       ← 실제 환경변수 (git 제외)
    ├── .python-version            ← Python 3.14
    ├── pyproject.toml
    ├── uv.lock
    ├── langgraph.json             ← langgraph dev 설정
    ├── doctor.py                  ← 진단 스크립트
    ├── graph.py                   ← LangGraph Studio 진입점
    └── main.py                    ← CLI 실행 스크립트
```

## 실행 방법 요약

```bash
cd src/
cp .env.sample .env  # → ANTHROPIC_API_KEY 입력
# 기본 의존성 설치
uv sync

# 설정 확인
uv run python doctor.py

# CLI 실행
uv run python main.py

# LangGraph Studio (최초 1회 studio 의존성 설치)
uv sync --extra studio
uv run langgraph dev --tunnel
```

## 환경변수 (src/.env)

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `ANTHROPIC_API_KEY` | 필수 | — | console.anthropic.com API 키 |
| `ANTHROPIC_BASE_URL` | 선택 | (공식 Anthropic API) | LM Studio 등 호환 프록시 사용 시 |
| `MAIN_MODEL` | 선택 | `claude-sonnet-4-6` | 메인 에이전트 모델 |
| `GRADER_MODEL` | 선택 | `claude-haiku-4-5-20251001` | 채점 에이전트 모델 |
| `LANGSMITH_API_KEY` | 선택 | — | LangGraph Studio Trace 탭 활성화 |

## 핵심 참고자료

| 자료 | URL |
|------|-----|
| 블로그 포스트 | https://www.langchain.com/blog/introducing-rubrics-for-deepagents |
| deepagents GitHub | https://github.com/langchain-ai/deepagents |
| rubric.py 소스 | https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py |
| API 레퍼런스 | https://reference.langchain.com/python/deepagents/ |
| Anthropic | https://console.anthropic.com |
| Interrupt 2026 | https://www.youtube.com/watch?v=LdQpoK2TzSo |
