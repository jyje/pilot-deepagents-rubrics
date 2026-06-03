# Documentation — pilot-deepagents-rubrics

[English](#english) · [한국어](#한국어)

---

## English

### Index

| Doc (EN) | Doc (KO) | Description |
|----------|----------|-------------|
| [01-overview.md](01-overview.md) | [01-overview-ko.md](01-overview-ko.md) | RubricMiddleware concepts — what it is, how it works, key design points |
| [02-api-reference.md](02-api-reference.md) | [02-api-reference-ko.md](02-api-reference-ko.md) | API class reference: `RubricMiddleware`, `GraderResponse`, `GraderVerdict`, etc. |
| [03-anthropic-setup.md](03-anthropic-setup.md) | [03-anthropic-setup-ko.md](03-anthropic-setup-ko.md) | Anthropic API key setup, recommended models, environment variables |
| [04-langgraph-studio.md](04-langgraph-studio.md) | [04-langgraph-studio-ko.md](04-langgraph-studio-ko.md) | LangGraph Studio web UI — graph visualization, run traces, LangSmith setup |
| [05-lmstudio.md](05-lmstudio.md) | [05-lmstudio-ko.md](05-lmstudio-ko.md) | LM Studio local setup — free alternative when paid Anthropic API is unavailable |
| [06-result-fibonacci.md](06-result-fibonacci.md) | [06-result-fibonacci-ko.md](06-result-fibonacci-ko.md) | Demo result: Fibonacci pytest, 2-iteration rubric loop with screenshots and trace |
| [result.txt](result.txt) | — | First demo run: string reversal, 3-iteration rubric loop with token breakdown |

### Key Concepts

**What RubricMiddleware really is**

The evaluate-and-retry loop can be written manually, but `RubricMiddleware` packages it as a 3-line plug-in:

```python
# Manual
while iterations < max_iterations:
    result = agent.invoke({"messages": messages})
    verdict = grader.invoke(f"Does this satisfy: {criteria}?")
    if verdict == "pass": break
    messages.append(f"Feedback: {verdict.feedback}")

# With RubricMiddleware
agent = create_deep_agent(model=..., middleware=[RubricMiddleware(criteria)])
agent.invoke({"messages": ..., "rubric": criteria})
```

**Why Anthropic?**

DeepAgents was built for Claude. `RubricMiddleware` uses Claude's native `tool_use` format for structured grading — no compatibility shims needed with other providers.

**RubricMiddleware vs. other middlewares**

| | Regular middleware | RubricMiddleware |
|--|-------------------|-----------------|
| Scope | Inside a single run | Wraps the entire run loop |
| Role | Transform model I/O | Grade output, decide retry |
| LLM | Shared or none | Dedicated grader model |
| Run count | Fixed at 1 | Up to `max_iterations` |

The others are **factory machines** (assist the work); RubricMiddleware is the **quality inspector** (evaluates the result and sends it back if it fails).

**Why "Rubric"?**

The term comes from educational assessment. Latin *rubrica* → medieval liturgical directives → modern education's per-criterion scoring guide. LLM-as-a-Judge research (Zheng et al., 2023 "MT-Bench") adopted the term for structured output evaluation. LangChain packaged it as middleware.

---

## 한국어

### 인덱스

| 문서 (KO) | 문서 (EN) | 설명 |
|-----------|-----------|------|
| [01-overview-ko.md](01-overview-ko.md) | [01-overview.md](01-overview.md) | RubricMiddleware 개념 — 정의, 동작 원리, 핵심 설계 포인트 |
| [02-api-reference-ko.md](02-api-reference-ko.md) | [02-api-reference.md](02-api-reference.md) | API 클래스 레퍼런스: `RubricMiddleware`, `GraderResponse`, `GraderVerdict` 등 |
| [03-anthropic-setup-ko.md](03-anthropic-setup-ko.md) | [03-anthropic-setup.md](03-anthropic-setup.md) | Anthropic API 키 설정, 권장 모델, 환경변수 |
| [04-langgraph-studio-ko.md](04-langgraph-studio-ko.md) | [04-langgraph-studio.md](04-langgraph-studio.md) | LangGraph Studio 웹 UI — 그래프 시각화, 실행 추적, LangSmith 설정 |
| [05-lmstudio-ko.md](05-lmstudio-ko.md) | [05-lmstudio.md](05-lmstudio.md) | LM Studio 로컬 설정 — 유료 Anthropic API 사용 불가 시 무료 대안 |
| [06-result-fibonacci-ko.md](06-result-fibonacci-ko.md) | [06-result-fibonacci.md](06-result-fibonacci.md) | 데모 결과: 피보나치 pytest, 2회 루브릭 루프 + 스크린샷 및 트레이스 |
| [result.txt](result.txt) | — | 첫 번째 데모: 문자열 역순, 3회 루브릭 루프 + 토큰 수준 로그 |

### 핵심 개념

**RubricMiddleware의 본질**

평가-재시도 루프를 직접 구현할 수도 있지만, `RubricMiddleware`는 이를 3줄 플러그인으로 패키징합니다:

```python
# 직접 구현
while iterations < max_iterations:
    result = agent.invoke({"messages": messages})
    verdict = grader.invoke(f"Does this satisfy: {criteria}?")
    if verdict == "pass": break
    messages.append(f"Feedback: {verdict.feedback}")

# RubricMiddleware 사용
agent = create_deep_agent(model=..., middleware=[RubricMiddleware(criteria)])
agent.invoke({"messages": ..., "rubric": criteria})
```

**왜 Anthropic인가?**

DeepAgents는 Claude를 기준으로 설계되었습니다. `RubricMiddleware`가 채점 구조화 출력에 Claude의 네이티브 `tool_use` 포맷을 사용하므로 다른 공급자 대비 호환성 코드가 필요 없습니다.

**RubricMiddleware vs. 일반 미들웨어**

| | 일반 미들웨어 | RubricMiddleware |
|--|-------------|-----------------|
| 범위 | 단일 실행 안 | 전체 실행 루프 래핑 |
| 역할 | 모델 입출력 변환 | 결과 채점 + 재시도 결정 |
| LLM | 공유 또는 없음 | 전용 채점 모델 |
| 실행 횟수 | 1회 고정 | 최대 `max_iterations`회 |

나머지 미들웨어들이 **공장 기계**(작업 보조)라면, RubricMiddleware는 **품질 검사관**(완성품 평가 후 불합격 시 라인 반환)입니다.

**"루브릭"이라는 이름의 유래**

교육학에서 온 용어입니다. 라틴어 *rubrica* → 중세 전례 지침서 → 현대 교육학의 기준별 채점표. LLM-as-a-Judge 연구(Zheng et al., 2023 "MT-Bench")가 이 용어를 구조화 평가에 채용했고, LangChain이 미들웨어로 패키징했습니다.

---

← [README.md](../README.md) · [README-ko.md](../README-ko.md)
