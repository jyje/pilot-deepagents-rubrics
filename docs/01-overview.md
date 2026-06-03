# Overview: RubricMiddleware

> Source: https://www.langchain.com/blog/introducing-rubrics-for-deepagents

## One-Line Summary

After an agent completes a task, a separate grader sub-agent evaluates the output against rubric criteria and automatically retries with injected feedback until all criteria pass.

## Background

When automating code generation, documentation writing, etc. with Deep Agents, developers had to manually inspect results and re-run on failure. `RubricMiddleware` automates this inspect-and-retry loop at the middleware level.

## How It Works

```
[Agent Run]
      │
      ▼
[Grader Sub-Agent] ── per-criterion evaluation ──► all pass → done
      │
      │ needs_revision
      ▼
[Inject Feedback Message] → [Agent Re-run] → (repeat up to max_iterations)
```

## 3-Step Implementation

```python
# 1. Define middleware
from deepagents import RubricMiddleware

rubric_middleware = RubricMiddleware(
    model="anthropic:claude-haiku-4-5",       # model for grading (cheaper recommended)
    system_prompt="You are a code reviewer.", # grader persona
    tools=[run_test_suite],                   # tools for the grader (optional)
    max_iterations=5,                         # max retry count
)

# 2. Attach to Deep Agent
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="You are a careful Python engineer.",
    middleware=[rubric_middleware],
)

# 3. Invoke with rubric
from langchain_core.messages import HumanMessage

result = agent.invoke({
    "messages": [HumanMessage(content="Write a function that reverses a string")],
    "rubric": "- Has docstring\n- Passes all unit tests\n- No use of built-in reverse\n",
})
```

## Key Design Points

- **Grader separation**: can use a different model/prompt from the main agent → cost optimization
- **Per-criterion feedback**: specifies exactly which criterion failed and why → agent knows precisely what to fix
- **Tool support**: tools like `run_test_suite` can be given to the grader → real execution verification
- **Iteration cap**: `max_iterations` prevents infinite loops

## Best Use Cases

| Good fit | Poor fit |
|----------|----------|
| Test pass/fail | Subjective quality |
| Forbidden pattern detection | Creativity evaluation |
| Required section presence | Emotional judgment |
| Code style compliance | Business value assessment |

## Related Classes (API)

| Class | Role |
|-------|------|
| `RubricMiddleware` | Main middleware; orchestrates the grading loop |
| `CriterionPass` | Typed result for a passing criterion |
| `CriterionFail` | Typed result for a failing criterion + feedback |
| `RubricEvaluation` | Aggregated evaluation across all criteria |
| `GraderResponse` | Full grader sub-agent response |
| `RubricState` | State object threaded through the rubric loop |
| `RubricResult` | Final result type of the rubric execution |
