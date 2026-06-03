# AGENTS.md — Project Context for AI Agents

> Updated: 2026-06-03

## 프로젝트 목적

Anthropic Claude를 AI 공급자로 사용하여 LangChain DeepAgents의 `RubricMiddleware`를 실행하는 파일럿 프로젝트.
에이전트 출력물을 루브릭 기준으로 자동 채점하고 재시도하는 미들웨어의 동작을 코드 레벨에서 검증한다.

## 현재 상태 (2026-06-03)

### 완료된 것

- [x] GitHub 레포 생성: `jyje/pilot-deepagents-rubrics` (public)
- [x] README.md / README-ko.md (DeepAgents 공식 로고, Anthropic 뱃지 적용)
- [x] `src/`: uv 초기화 (Python 3.14, `deepagents==0.6.7`)
- [x] AI 공급자: Anthropic Claude (`langchain-anthropic`)
- [x] `src/.env.sample` / `src/.env`: 환경변수 템플릿 및 실제 설정
- [x] `src/pyproject.toml`: base + studio optional dependencies
- [x] `src/main.py`: CLI 실행 스크립트 (Anthropic + RubricMiddleware)
- [x] `src/graph.py`: LangGraph Studio 진입점 (모듈 레벨 `agent` export)
- [x] `src/doctor.py`: ENV / API 연결 / 추론 3단계 진단 스크립트
- [x] `src/langgraph.json`: `langgraph dev` 설정
- [x] `.vscode/settings.json`: IDE Python 인터프리터 경로 지정
- [x] `docs/00-research-plan.md`: 분석 목표 및 핵심 질문
- [x] `docs/01-overview.md`: RubricMiddleware 개념 및 동작 원리
- [x] `docs/02-api-reference.md`: API 클래스 목록
- [x] `docs/03-anthropic-setup.md`: Anthropic API 설정 가이드
- [x] `docs/04-langgraph-studio.md`: LangGraph Studio 실행 가이드

### 다음 할 일

- [ ] `rubric.py` 소스 코드 직접 읽기 → `docs/05-architecture.md` 작성
- [ ] `BaseMiddleware` 인터페이스 분석 (미들웨어 훅 구조)
- [ ] 엣지 케이스 실험: max_iterations 초과, 즉시 통과, 상충 기준
- [ ] LangSmith 트레이싱 연동 실험

## 프로젝트 구조

```
pilot-deepagents-rubrics/
├── README.md / README-ko.md       ← 프로젝트 문서 (EN/KO)
├── AGENTS.md                      ← 이 파일: AI 에이전트용 컨텍스트
├── .vscode/settings.json          ← IDE Python 인터프리터 설정
├── docs/                          ← 분석 문서 및 설정 가이드
│   ├── 00-research-plan.md
│   ├── 01-overview.md
│   ├── 02-api-reference.md
│   ├── 03-anthropic-setup.md
│   └── 04-langgraph-studio.md
└── src/                           ← 모든 소스 코드 (uv 관리)
    ├── .env.sample                ← 환경변수 템플릿 (커밋 가능)
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

# 1. 환경변수 설정
cp .env.sample .env  # → ANTHROPIC_API_KEY 입력

# 2. 의존성 설치
uv sync --extra studio

# 3. 진단
uv run python doctor.py

# 4a. CLI 실행
uv run python main.py

# 4b. LangGraph Studio (웹 UI)
uv run langgraph dev
# → https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
```

## 환경변수 (src/.env)

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `ANTHROPIC_API_KEY` | 필수 | — | console.anthropic.com API 키 |
| `ANTHROPIC_BASE_URL` | 선택 | (공식 Anthropic API) | Anthropic 호환 프록시 사용 시 |
| `MAIN_MODEL` | 선택 | `claude-sonnet-4-6` | 메인 에이전트 모델 |
| `GRADER_MODEL` | 선택 | `claude-haiku-4-5-20251001` | 채점 에이전트 모델 |

## 핵심 참고자료

| 자료 | URL |
|------|-----|
| 블로그 포스트 | https://www.langchain.com/blog/introducing-rubrics-for-deepagents |
| deepagents GitHub | https://github.com/langchain-ai/deepagents |
| rubric.py 소스 | https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py |
| API 레퍼런스 | https://reference.langchain.com/python/deepagents/ |
| Anthropic | https://console.anthropic.com |
| Interrupt 2026 | https://www.youtube.com/watch?v=LdQpoK2TzSo |
