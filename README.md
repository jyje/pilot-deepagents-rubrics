<div align="center">

# jyje/pilot-deepagents-rubrics

<img width="280" src="https://raw.githubusercontent.com/langchain-ai/deepagentsjs/refs/heads/main/.github/images/logo-light.svg#gh-light-mode-only" alt="DeepAgents"/>
<img width="280" src="https://raw.githubusercontent.com/langchain-ai/deepagentsjs/refs/heads/main/.github/images/logo-dark.svg#gh-dark-mode-only" alt="DeepAgents"/>

🚀 Pilot project for LangChain DeepAgents `RubricMiddleware` — powered by Anthropic Claude

[![GitHub Repo stars](https://img.shields.io/github/stars/jyje/pilot-deepagents-rubrics?style=social)](https://github.com/jyje/pilot-deepagents-rubrics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Anthropic](https://img.shields.io/badge/AI%20Provider-Anthropic%20Claude-D4C5FF)](https://console.anthropic.com)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org)

[English](README.md) · [한국어](README-ko.md) · [Docs](docs/README.md)

---

**Found this useful? Please give it a ⭐ — it helps others find it.**

</div>

## Overview

`RubricMiddleware` is a LangChain DeepAgents middleware that automatically grades an agent's output against a set of criteria, injects targeted feedback on failure, and retries — until all criteria pass or `max_iterations` is reached.

This repository pilots the middleware with **Anthropic Claude** as the AI provider, validates the complete loop end-to-end, and documents the findings.

> DeepAgents is designed for Claude: `RubricMiddleware` uses Claude's native `tool_use` format for structured grading output — no compatibility shims needed.
> If you cannot use a paid Anthropic API → [LM Studio local setup](docs/05-lmstudio.md)

## How It Works

```
__start__
    │
    ▼
PatchToolCallsMiddleware.before_agent
    │
    ▼
RubricMiddleware.before_agent       ← initialize rubric state
    │
    ▼
  model  ◄─────────────────────────────┐
    │                                  │ needs_revision
    ▼                                  │
TodoListMiddleware.after_model         │
    ├─► tools                          │
    └─► RubricMiddleware.after_agent ──┘
                    │
                    ▼
                __end__
```

`RubricMiddleware.after_agent` branches to `model` (retry with feedback) or `__end__` (done) based on the grader's per-criterion verdict.

## Demo

Task: *"Write a Python function that reverses a string"* with three rubric criteria.

| Iteration | Verdict | What the grader caught |
|-----------|---------|------------------------|
| eval[0] | `needs_revision` | Used `s[::-1]` — explicitly forbidden by rubric |
| eval[1] | `needs_revision` | Algorithm fixed, but usage example was in `__main__`, not inside the docstring |
| eval[2] | `satisfied` | All three criteria passed |

**Insight:** The grader caught two *distinct* issues across two iterations — not the same complaint repeated. Each feedback was criterion-specific and actionable. The agent addressed exactly the failing criterion each time without over-correcting. This is the core value of rubric-based evaluation: structured, per-criterion feedback instead of a generic "try again."

→ Full execution log with token breakdown: [docs/result.txt](docs/result.txt)

## Quick Start

```bash
git clone https://github.com/jyje/pilot-deepagents-rubrics.git
cd pilot-deepagents-rubrics/src
cp .env.sample .env          # set ANTHROPIC_API_KEY
uv sync --extra studio
uv run python doctor.py      # verify setup
uv run python main.py        # run demo
uv run langgraph dev         # open LangGraph Studio
```

→ Full setup guide: [docs/03-anthropic-setup.md](docs/03-anthropic-setup.md)

## Documentation

→ [docs/README.md](docs/README.md) — full documentation index

## License

MIT © [jyje](https://github.com/jyje)
