# API Reference: deepagents.middleware.rubric

> Source: https://reference.langchain.com/python/deepagents/
> GitHub: https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py
> Status: 🔬 분석 진행 중

## 확인된 구성 요소

API 인덱스에서 확인된 클래스/타입 목록:

| 이름 | 종류 | 설명 (추정) |
|------|------|------------|
| `RubricMiddleware` | Class | 메인 미들웨어. 채점 루프 전체를 관리 |
| `CriterionPass` | Class | 단일 기준 통과를 나타내는 typed result |
| `CriterionFail` | Class | 단일 기준 실패 + 피드백 메시지를 포함 |
| `RubricEvaluation` | Class | 모든 기준에 대한 종합 평가 집계 |
| `RubricState` | Class | LangGraph 상태에 주입되는 루브릭 루프 상태 |
| `GraderResponse` | Class | 채점 서브에이전트의 전체 응답 래퍼 |
| `RubricResult` | Type | 루브릭 실행 최종 결과 타입 |

## 내부 상수 (reference 페이지에서 노출됨)

| 이름 | 추정 역할 |
|------|----------|
| `GraderVerdict` | 채점 결과 enum (`pass` / `needs_revision`) |
| `RUBRIC_GRADER_MESSAGE_SOURCE` | 피드백 메시지의 source 식별자 |
| `GRADER_SYSTEM_PROMPT` | 기본 채점 에이전트 시스템 프롬프트 |
| `CriterionEval` | 기준별 평가 단위 타입 |
| `logger` | 모듈 레벨 로거 |

## RubricMiddleware 생성자 파라미터

```python
RubricMiddleware(
    model,                    # 채점 모델 — str 또는 BaseChatModel 인스턴스
    system_prompt: str,       # 채점 에이전트 시스템 프롬프트
    tools: list = [],         # 채점 에이전트에 줄 도구 목록
    max_iterations: int = 3,  # 최대 재시도 횟수
)
```

> `model`에 `ChatNVIDIA` 등 `BaseChatModel` 객체를 직접 전달 가능. NVIDIA NIM 예시:
>
> ```python
> from langchain_nvidia_ai_endpoints import ChatNVIDIA
> grader = ChatNVIDIA(model="openai/gpt-oss-20b", nvidia_api_key=...)
> RubricMiddleware(model=grader, ...)
> ```

## invoke() 입력 스키마

```python
agent.invoke({
    "messages": List[BaseMessage],  # 기존 대화 메시지
    "rubric": str,                  # 줄바꿈으로 구분된 기준 목록
})
```

> ⚠️ `rubric` 필드가 `RubricState`에 어떻게 매핑되는지 확인 필요.

## TODO: 소스 코드에서 확인할 것

- [ ] `RubricMiddleware`가 상속하는 베이스 클래스
- [ ] `CriterionPass` / `CriterionFail`의 필드 구조 (Pydantic 모델 여부)
- [ ] `GraderVerdict` 값 목록
- [ ] `RubricState`의 LangGraph `TypedDict` 정의
- [ ] 채점 루프가 LangGraph 그래프 노드로 구현되었는지, 아니면 Python 루프인지
- [ ] `GRADER_SYSTEM_PROMPT` 기본값 (프롬프트 엔지니어링 참고)
