# Research Plan: RubricMiddleware Deep Dive

## Goal

Fully understand how LangChain DeepAgents' `RubricMiddleware` works at the source code level and validate its applicability in practice.

## Key Questions

### Structure
- [ ] How does `RubricMiddleware` inherit from `BaseMiddleware`?
- [ ] How is the grader sub-agent created internally?
- [ ] How does `RubricState` integrate with LangGraph state?
- [ ] What are the roles of `GraderVerdict` / `RUBRIC_GRADER_MESSAGE_SOURCE`?

### Execution Flow
- [ ] What is the exact order: agent completion → grading → feedback injection?
- [ ] Where and how is the `needs_revision` verdict determined?
- [ ] What format is used when feedback is injected into the conversation (messages)?
- [ ] Where is the `max_iterations` counter managed?

### Extensibility
- [ ] How are tools passed via the `tools` parameter called by the grader agent?
- [ ] Does a custom grader model (`model` param) operate independently of the main agent?
- [ ] How is the rubric string parsed? (newline-delimited? special format?)
- [ ] What happens when `RubricMiddleware` is attached to a SubAgent in a multi-agent setup?

### Practical Application
- [ ] Performance when using a small model as the grader in a private LLM (on-premises) environment?
- [ ] How does the grading loop appear in LangSmith tracing?
- [ ] Cost structure: is it 2 calls per iteration (main + grader)?

## Analysis Order

1. **Read source** — full analysis of `libs/deepagents/deepagents/middleware/rubric.py`
2. **Understand `BaseMiddleware` interface** — hook structure
3. ~~**Trace execution flow**~~ ✅ — confirmed `create_deep_agent` returns `CompiledStateGraph`; Mermaid graph extracted ([04-langgraph-studio.md](04-langgraph-studio.md))
4. ~~**Implement minimal working example**~~ ✅ — `src/main.py` (CLI), `src/graph.py` (Studio)
5. **Edge case experiments** — exceeding `max_iterations`, immediate pass, conflicting criteria

## References

| Source | URL |
|--------|-----|
| Blog post | https://www.langchain.com/blog/introducing-rubrics-for-deepagents |
| GitHub source | https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py |
| API reference | https://reference.langchain.com/python/deepagents/ |
| Interrupt 2026 video | https://www.youtube.com/watch?v=LdQpoK2TzSo |
| DeepAgents middleware docs | https://docs.langchain.com/oss/python/deepagents/middleware |
