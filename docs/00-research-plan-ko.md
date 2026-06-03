# Research Plan: RubricMiddleware 코드 레벨 심층 분석

## 목표

LangChain DeepAgents의 `RubricMiddleware`가 내부적으로 어떻게 동작하는지 소스 코드 수준에서 완전히 이해하고, 실무 적용 가능성을 검증한다.

## 핵심 질문

### 구조 이해
- [ ] `RubricMiddleware`는 `BaseMiddleware`를 어떻게 상속하는가?
- [ ] 채점 서브에이전트(grader sub-agent)는 어떤 구조로 생성되는가?
- [ ] `RubricState`는 LangGraph state와 어떻게 통합되는가?
- [ ] `GraderVerdict` / `RUBRIC_GRADER_MESSAGE_SOURCE` 상수의 역할은?

### 실행 흐름
- [ ] 에이전트 완료 → 채점 → 피드백 주입의 정확한 실행 순서는?
- [ ] `needs_revision` 판정 로직은 어디서 어떻게 이루어지는가?
- [ ] 피드백이 대화(messages)에 주입될 때 어떤 형식으로 들어가는가?
- [ ] `max_iterations` 카운터는 어디서 관리되는가?

### 확장 가능성
- [ ] `tools` 파라미터로 넘긴 도구(e.g. `run_test_suite`)는 채점 에이전트에서 어떻게 호출되는가?
- [ ] 커스텀 채점 모델(model 파라미터)이 메인 에이전트와 독립적으로 동작하는가?
- [ ] 루브릭 기준(rubric string)의 파싱 방식은? (줄바꿈 기준? 특수 포맷?)
- [ ] 멀티 에이전트 구조에서 SubAgent에 `RubricMiddleware`를 붙이면 어떻게 되는가?

### 실무 적용
- [ ] Private LLM(온프레미스) 환경에서 채점 모델로 소형 모델을 쓸 때 성능은?
- [ ] LangSmith 트레이싱에서 채점 루프가 어떻게 표시되는가?
- [ ] 비용 구조: 반복마다 메인 + 채점 2회 호출인가?

## 분석 순서

1. **소스 코드 읽기** — `libs/deepagents/deepagents/middleware/rubric.py` 전체 분석
2. **BaseMiddleware 인터페이스 이해** — 미들웨어 훅 구조 파악
3. ~~**실행 흐름 추적**~~ ✅ — `create_deep_agent`가 `CompiledStateGraph` 반환 확인, Mermaid 그래프 추출 완료 (`docs/04-langgraph-studio.md`)
4. ~~**최소 동작 예제 구현**~~ ✅ — `src/main.py` (CLI), `src/graph.py` (Studio) 구현 완료
5. **엣지 케이스 실험** — max_iterations 초과, 모든 기준 즉시 통과, 상충 기준 등

## 참고 소스

| 소스 | URL |
|------|-----|
| 블로그 포스트 | https://www.langchain.com/blog/introducing-rubrics-for-deepagents |
| GitHub 소스 | https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py |
| API 레퍼런스 | https://reference.langchain.com/python/deepagents/ |
| Interrupt 2026 영상 | https://www.youtube.com/watch?v=LdQpoK2TzSo |
| DeepAgents 미들웨어 문서 | https://docs.langchain.com/oss/python/deepagents/middleware |
