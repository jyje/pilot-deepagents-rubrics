# LangGraph Studio Guide

## Overview

`create_deep_agent` returns a LangGraph `CompiledStateGraph`.
Run `langgraph dev` to start a local API server and inspect the graph structure, execution flow, and state in real time via the **LangGraph Studio web UI**.

## Graph Structure

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
    ▼                                  │  (retry)
TodoListMiddleware.after_model         │
    │  ┌─► tools  (on tool call)       │
    │  └─► RubricMiddleware.after_agent ┘
    │                │
    └────────────────▼
                 __end__
```

`RubricMiddleware.after_agent` branches to `model` (retry) or `__end__` (done) based on the grader verdict.

## How to Run

### 1. Install dependencies

```bash
cd src/
uv sync --extra studio
```

### 2. Start the server

```bash
cd src/
uv run langgraph dev
```

The browser opens automatically:

```
Ready!
- API:    http://localhost:2024
- Studio: https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
```

If the browser doesn't open, navigate to the Studio URL directly.

> LangGraph Studio is served from `https://smith.langchain.com` and connects to your local `localhost:2024` server. Graph visualization works without a LangSmith account, but the **Trace tab** requires `LANGSMITH_API_KEY`.

### 3. "Failed to initialize Studio" error

When Studio (`https://smith.langchain.com`) tries to connect to a local `http://` server, the browser blocks it due to the **Mixed Content** security policy. The server is running fine; the browser is rejecting the HTTPS → HTTP request.

**Step 1:** Restart with the `--tunnel` flag.

```bash
uv run langgraph dev --tunnel
```

A Cloudflare tunnel URL is printed:

```
- Studio: https://smith.langchain.com/studio/?baseUrl=https://xxxx.trycloudflare.com
```

**Step 2 — domain not allowed error:**

If Studio shows "domain is not allowed", whitelist the Cloudflare domain:

- **One-time:** Configure connection → **Advanced Settings** → add the domain → Connect
- **Permanent:** LangSmith **Settings → Configuration → Shared URLs** → add `*.trycloudflare.com`

> The Cloudflare tunnel URL changes on every restart. Permanent allowlisting is recommended.

## Running the Agent in Studio

In the **Input** panel at the bottom left, fill in the fields and click **Submit**.

| Field | Required | Example |
|-------|----------|---------|
| **Messages** | Required | `Write a Python function that reverses a string` |
| **Rubric** | Optional | `- Has a docstring\n- Does not use [::-1]` |
| **Files** | Optional | For file attachments |

> ⚠️ **Submitting with an empty Messages field causes a 400 error.**
> DeepAgents injects tool definitions into the first user message; if there is none, the API rejects the request.

After running, check the **Trace** tab on the right to inspect each node's input/output and the grading loop flow.

## LangSmith Tracing Setup

To dismiss the "LangSmith API key is missing" banner and activate the **Trace tab**:

**1. Create an account** at [https://smith.langchain.com](https://smith.langchain.com)

**2. Generate API key**

**Settings → Access and Security → API Keys → + API Key**

| Field | Recommended |
|-------|-------------|
| Description | `pilot-deepagents-rubrics` |
| Key Type | **Personal Access Token** |
| Expiration Date | 30d |

> ⚠️ The key is shown only once. Copy it immediately.

**3. Add to `.env`**

```dotenv
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=pilot-deepagents-rubrics
```

**4. Verify**

```bash
uv run python doctor.py
```

**5. Restart `langgraph dev`**

The banner disappears and the **Trace** tab becomes active.

## Required Accounts

| Service | Purpose | URL |
|---------|---------|-----|
| Anthropic | Main agent + grader model inference | https://console.anthropic.com |
| LangSmith | Studio Trace tab run history | https://smith.langchain.com |

## Related Files

| File | Role |
|------|------|
| `src/graph.py` | Module-level `agent` export (Studio entrypoint) |
| `src/langgraph.json` | `langgraph dev` config (`graphs`, `env` path) |
| `src/.env` | API keys and model settings |

## langgraph.json Structure

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./graph.py:agent"
  },
  "env": ".env"
}
```

## main.py vs graph.py

| File | Purpose |
|------|---------|
| `main.py` | CLI run (`uv run python main.py`) |
| `graph.py` | Module-level export for LangGraph Studio |

Both use the same `_make_model()` pattern and read from the same `.env`.
