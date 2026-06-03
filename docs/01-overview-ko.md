# Overview: RubricMiddleware

> Source: https://www.langchain.com/blog/introducing-rubrics-for-deepagents
> Captured: 2026-06-03

## 한 줄 요약

에이전트가 작업을 마치면 별도 채점 서브에이전트가 루브릭 기준을 평가하고, 기준 미달 시 피드백을 주입해 자동으로 재시도시키는 미들웨어.

## 문제 배경

Deep Agent로 코드 생성, 문서 작성 등을 자동화할 때 개발자가 결과물을 수동으로 검사하고 실패 시 다시 실행해야 했음. 이 수동 검사-재실행 루프를 미들웨어 레벨에서 자동화한 것이 RubricMiddleware.

## 작동 원리

```
[Agent 실행]
      │
      ▼
[채점 서브에이전트] ── 루브릭 기준별 평가 ──► 모두 통과 → 종료
      │
      │ needs_revision
      ▼
[피드백 메시지 주입] → [Agent 재실행] → (반복, max_iterations까지)
```

## 3단계 구현

```python
# 1. 미들웨어 정의
from deepagents import RubricMiddleware

rubric_middleware = RubricMiddleware(
    model="anthropic:claude-haiku-4-5",       # 채점에 쓸 모델 (저렴한 모델 추천)
    system_prompt="You are a code reviewer.", # 채점 에이전트 페르소나
    tools=[run_test_suite],                   # 채점 에이전트가 쓸 도구 (선택)
    max_iterations=5,                         # 최대 재시도 횟수
)

# 2. Deep Agent에 연결
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="You are a careful Python engineer.",
    middleware=[rubric_middleware],
)

# 3. 루브릭과 함께 호출
from langchain_core.messages import HumanMessage

result = agent.invoke({
    "messages": [HumanMessage(content="Write a function that reverses a string")],
    "rubric": "- Has docstring\n- Passes all unit tests\n- No use of built-in reverse\n",
})
```

## 핵심 설계 포인트

- **채점 에이전트 분리**: 메인 에이전트와 다른 모델/프롬프트 사용 가능 → 비용 최적화
- **기준별 피드백**: 어떤 기준이 왜 실패했는지 구체적으로 주입 → 에이전트가 정확히 무엇을 수정해야 하는지 앎
- **도구 지원**: `run_test_suite` 같은 도구를 채점 에이전트에 줄 수 있음 → 실제 실행 검증 가능
- **반복 제한**: `max_iterations`로 무한 루프 방지

## 최적 사용 케이스

| 적합 | 부적합 |
|------|--------|
| 테스트 통과 여부 | 주관적 품질 평가 |
| 금지 패턴 포함 여부 | 창의성 평가 |
| 필수 섹션 존재 여부 | 감성적 판단 |
| 코드 스타일 준수 | 비즈니스 가치 판단 |

## 관련 클래스 (API)

| 클래스 | 역할 |
|--------|------|
| `RubricMiddleware` | 미들웨어 구현체, 채점 루프 오케스트레이션 |
| `CriterionPass` | 개별 기준 통과 결과 |
| `CriterionFail` | 개별 기준 실패 결과 + 피드백 |
| `RubricEvaluation` | 전체 기준 종합 평가 |
| `GraderResponse` | 채점 에이전트 전체 응답 |
| `RubricState` | 루브릭 루프 상태 객체 |
| `RubricResult` | 최종 결과 타입 |
