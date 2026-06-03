<div align="center">

# jyje/pilot-deepagents-rubrics

<img width="280" src="https://raw.githubusercontent.com/langchain-ai/deepagentsjs/refs/heads/main/.github/images/logo-light.svg#gh-light-mode-only" alt="DeepAgents"/>
<img width="280" src="https://raw.githubusercontent.com/langchain-ai/deepagentsjs/refs/heads/main/.github/images/logo-dark.svg#gh-dark-mode-only" alt="DeepAgents"/>

🚀 Pilot project for LangChain DeepAgents `RubricMiddleware`

[![GitHub Repo stars](https://img.shields.io/github/stars/jyje/pilot-deepagents-rubrics?style=social)](https://github.com/jyje/pilot-deepagents-rubrics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Anthropic](https://img.shields.io/badge/AI%20Provider-Anthropic%20Claude-D4C5FF)](https://console.anthropic.com)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org)

[English](README.md) · [한국어](README-ko.md) · [Docs](docs/README.md)

---

**Found this useful? Please give it a ⭐ — it helps others find it.**

</div>

## Overview

> **`RubricMiddleware` is LangChain's version of the `/goal` loop** — the "keep retrying until all criteria pass" pattern, packaged as a 3-line plug-in middleware for DeepAgents.

`RubricMiddleware` automatically grades an agent's output against a set of criteria, injects targeted feedback on failure, and retries — until all criteria pass or `max_iterations` is reached.

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

### Demo 2 — Fibonacci pytest (LangGraph Studio)

A more complex task run via LangGraph Studio with screenshots and LangSmith trace.
The grader caught a non-obvious issue: syntactically valid test code that couldn't actually *run* without the missing implementation file.
No syntax checker or generic "try again" would catch this — only a rubric criterion that demanded a fully self-contained, executable artifact.

![LangGraph Studio — Fibonacci demo](docs/assets/result-fibonacci-interact.png)

→ Full result with screenshots: [docs/06-result-fibonacci.md](docs/06-result-fibonacci.md) · [한국어](docs/06-result-fibonacci-ko.md)

## Quick Start

```bash
git clone https://github.com/jyje/pilot-deepagents-rubrics.git
cd pilot-deepagents-rubrics/src
# set ANTHROPIC_API_KEY
cp .env.sample .env

# install base dependencies
uv sync

# verify setup
uv run python doctor.py

# run CLI demo
uv run python main.py

# LangGraph Studio (install studio dependencies first time)
uv sync --extra studio
uv run langgraph dev --tunnel
```

→ Full setup guide: [docs/03-anthropic-setup.md](docs/03-anthropic-setup.md)

## Documentation

→ [docs/README.md](docs/README.md) — full documentation index

## License

MIT © [jyje](https://github.com/jyje)
