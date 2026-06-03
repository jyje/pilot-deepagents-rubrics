# API Reference: deepagents.middleware.rubric

> GitHub: https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/rubric.py

## Confirmed Components

Classes and types identified from the API index:

| Name | Kind | Description |
|------|------|-------------|
| `RubricMiddleware` | Class | Main middleware; manages the entire grading loop |
| `CriterionPass` | Class | Typed result for a single passing criterion |
| `CriterionFail` | Class | Single failing criterion + feedback message |
| `RubricEvaluation` | Class | Aggregated evaluation across all criteria |
| `RubricState` | Class | Rubric loop state injected into LangGraph state |
| `GraderResponse` | Class | Full response wrapper from the grader sub-agent |
| `RubricResult` | Type | Final result type of rubric execution |

## Internal Constants

| Name | Estimated Role |
|------|---------------|
| `GraderVerdict` | Grading result: `"satisfied"` / `"needs_revision"` / `"failed"` |
| `RUBRIC_GRADER_MESSAGE_SOURCE` | Source identifier for injected feedback messages |
| `GRADER_SYSTEM_PROMPT` | Default grader system prompt |
| `CriterionEval` | Per-criterion evaluation unit type |

## RubricMiddleware Constructor Parameters

```python
RubricMiddleware(
    model,                    # grader model — str or BaseChatModel instance
    system_prompt: str,       # grader agent system prompt
    tools: list = [],         # tools to give the grader agent
    max_iterations: int = 3,  # max retry count
)
```

> `model` accepts a `BaseChatModel` object directly. Example with Anthropic:
>
> ```python
> from langchain_anthropic import ChatAnthropic
> grader = ChatAnthropic(model="claude-haiku-4-5-20251001")
> RubricMiddleware(model=grader, ...)
> ```

## invoke() Input Schema

```python
agent.invoke({
    "messages": List[BaseMessage],  # conversation messages
    "rubric": str,                  # newline-delimited criteria list
})
```

## GraderVerdict Values

| Value | Meaning | Action |
|-------|---------|--------|
| `"satisfied"` | All criteria pass | Terminate — done |
| `"needs_revision"` | At least one criterion fails | Inject feedback and retry |
| `"failed"` | Task fundamentally impossible | Terminate — permanent failure |

> Only `"needs_revision"` continues the loop. Every other status ends it.

## TODO: Verify from Source

- [ ] Base class that `RubricMiddleware` inherits from
- [ ] Field structure of `CriterionPass` / `CriterionFail` (Pydantic model?)
- [ ] Whether the grading loop is implemented as a LangGraph graph node or a Python loop
- [ ] Default value of `GRADER_SYSTEM_PROMPT`
