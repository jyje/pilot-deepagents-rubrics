# LangGraph Studio 실행 가이드

## 개요

`create_deep_agent`는 LangGraph `CompiledStateGraph`를 반환합니다.  
`langgraph dev` 명령으로 로컬 API 서버를 띄우고 **LangGraph Studio 웹 UI**에서 그래프 구조, 실행 흐름, 상태를 실시간으로 확인할 수 있습니다.

## 그래프 구조

```
__start__
    │
    ▼
PatchToolCallsMiddleware.before_agent
    │
    ▼
RubricMiddleware.before_agent       ← 루브릭 상태 초기화
    │
    ▼
  model  ◄─────────────────────────────┐
    │                                  │ needs_revision
    ▼                                  │  (재시도)
TodoListMiddleware.after_model         │
    │  ┌─► tools  (tool call 시)       │
    │  └─► RubricMiddleware.after_agent ┘
    │                │
    └────────────────▼
                 __end__
```

`RubricMiddleware.after_agent`가 채점 결과에 따라 `model`(재시도) 또는 `__end__`(종료)로 분기합니다.

## 실행 방법

### 1. 의존성 설치

```bash
cd src/
uv sync --extra studio
```

### 2. 서버 실행

```bash
cd src/
uv run langgraph dev
```

서버가 뜨면 자동으로 브라우저가 열립니다:

```
Ready!
- API:    http://localhost:2024
- Studio: https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
```

브라우저가 자동으로 열리지 않으면 위 Studio URL을 직접 접속합니다.

> LangGraph Studio는 `https://smith.langchain.com`에서 서빙되며,  
> 로컬 `localhost:2024` 서버에 연결합니다. 그래프 시각화는 LangSmith 계정 없이도 동작하지만,  
> **Trace 탭(실행 이력)**을 보려면 `LANGSMITH_API_KEY` 설정이 필요합니다.

### 3. "Failed to initialize Studio" 오류 시

Studio(`https://smith.langchain.com`)가 로컬 `http://` 서버에 접속하려 할 때 브라우저의 **Mixed Content** 보안 정책에 의해 차단됩니다. 서버는 정상이지만 브라우저가 HTTPS → HTTP 요청을 막는 것입니다.

**1단계:** `--tunnel` 플래그로 재시작합니다.

```bash
uv run langgraph dev --tunnel
```

터널이 연결되면 HTTPS URL이 출력됩니다:

```
- Studio: https://smith.langchain.com/studio/?baseUrl=https://xxxx.trycloudflare.com
```

**2단계 — 도메인 허용 오류 시:**

Studio가 열리며 "domain is not allowed" 오류가 뜨면 Cloudflare 도메인을 허용해야 합니다.

- **일회성:** Configure connection → **Advanced Settings** → 해당 도메인 추가 → Connect
- **영구 허용:** LangSmith **Settings → Configuration → Shared URLs** → `*.trycloudflare.com` 추가

> Cloudflare 터널 URL은 재시작마다 변경됩니다. 영구 허용을 권장합니다.

## Studio에서 에이전트 실행하기

Studio 좌측 하단 **Input** 패널에서 입력 후 **Submit** 합니다.

| 필드 | 필수 | 예시 |
|------|------|------|
| **Messages** | 필수 | `Write a Python function that reverses a string` |
| **Rubric** | 선택 | `- Has a docstring\n- Does not use [::-1]` |
| **Files** | 선택 | 파일 첨부 시 사용 |

> ⚠️ **Messages를 비운 채 Submit하면 400 오류가 발생합니다.**  
> DeepAgents가 첫 번째 user 메시지에 tool 정의를 주입하는데, 메시지가 없으면  Anthropic API가 거부합니다.

실행 후 우측 **Trace** 탭에서 각 노드의 입출력과 채점 루프 흐름을 확인할 수 있습니다.

## LangSmith 트레이싱 연동

Studio 상단의 "LangSmith API key is missing" 배너를 없애고 **Trace 탭**을 활성화하려면 LangSmith API 키가 필요합니다.

### LangSmith API 키 발급

**1. 계정 생성**

[https://smith.langchain.com](https://smith.langchain.com) 에 접속하여 계정을 만듭니다.

**2. API Keys 페이지 이동**

좌측 사이드바 **Settings → Access and Security → API Keys** 클릭

**3. API 키 생성**

우측 상단 **+ API Key** 버튼 클릭 후 아래와 같이 입력합니다:

| 항목 | 권장값 |
|------|--------|
| Description | `pilot-deepagents-rubrics` |
| Key Type | **Personal Access Token** |
| Default Workspace | Workspace 1 (기본값) |
| Expiration Date | 30d (권장값) |

**Create API Key** 버튼을 누르면 `lsv2_pt_...` 형식의 키가 표시됩니다.  
> ⚠️ 키는 생성 직후 한 번만 표시됩니다. 반드시 즉시 복사하세요.

**4. `.env`에 주입**

```dotenv
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=pilot-deepagents-rubrics
```

**5. 검증**

```bash
uv run python doctor.py
```

`[PASS] LangSmith` 가 뜨면 정상입니다.

**6. `langgraph dev` 재시작**

이미 서버가 실행 중이라면 재시작합니다. 상단 배너가 사라지고 **Trace** 탭이 활성화됩니다.

## 필요한 계정

| 서비스 | 용도 | 발급 URL |
|--------|------|----------|
|  Anthropic | 메인 에이전트 + 채점 모델 추론 | https://console.anthropic.com |
| LangSmith | Studio Trace 탭 실행 이력 조회 | https://smith.langchain.com |

## 관련 파일

| 파일 | 역할 |
|------|------|
| `src/graph.py` | 모듈 레벨 `agent` 변수 export (Studio 진입점) |
| `src/langgraph.json` | `langgraph dev` 설정 (`graphs`, `env` 경로 지정) |
| `src/.env` | API 키 및 모델 설정 |

## langgraph.json 구조

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./graph.py:agent"
  },
  "env": ".env"
}
```

- `graphs.agent` — Studio에서 보이는 그래프 이름과 진입점
- `env` — 서버 실행 시 자동으로 로드할 `.env` 파일 경로

## main.py vs graph.py

| 파일 | 용도 |
|------|------|
| `main.py` | CLI 실행 (`uv run python main.py`) |
| `graph.py` | LangGraph Studio 용 모듈 레벨 export |

두 파일은 동일한 `_make_model()` 패턴을 사용하며 같은 `.env`를 읽습니다.
