# LM Studio Local Setup Guide

## Overview

If you cannot use a paid Anthropic API, [LM Studio](https://lmstudio.ai)'s **REST API v1 (Anthropic-compatible)** lets you run this project locally with a free model — no API key required.

> **Note:** DeepAgents was designed for Anthropic Claude. Local models via LM Studio use an Anthropic-compatible API, but model quality and `tool_use` reliability vary by model.

```
main.py / graph.py
    │  Anthropic API format
    ▼
LM Studio Local Server  (http://127.0.0.1:1234)
    │  Anthropic-compatible endpoint
    ▼
Local LLM (e.g. google/gemma-4-e4b)
```

## Setup

### 1. Install LM Studio and download a model

1. Download LM Studio from [https://lmstudio.ai](https://lmstudio.ai)
2. In the **Discover** tab, search for and download a model
   - Recommended: `google/gemma-4-e4b` (6.3 GB, tool_use support)
   - Or: any instruction-tuned model with tool_use / function calling support

### 2. Configure the local server

1. Click **Developer** in the left sidebar
2. **Local Server** → enable **Status: Running**
3. When loading the model, configure **Context and Offload**:

| Setting | Recommended | Notes |
|---------|-------------|-------|
| Context Length | `131072` (128k) | Minimum 16384 (observed max 8109 tok × 2). 128k provides ample headroom for multi-turn rubric loops |
| GPU Offload | Adjust per device | Set based on available VRAM |

4. Confirm **REST API v1** → **Anthropic-compatible** tab is visible

Server address: `http://127.0.0.1:1234`

### 3. Configure `.env`

```dotenv
ANTHROPIC_API_KEY=lm-studio
ANTHROPIC_BASE_URL=http://127.0.0.1:1234

MAIN_MODEL=google/gemma-4-e4b
GRADER_MODEL=google/gemma-4-e4b
```

> `ANTHROPIC_API_KEY` is not validated by the LM Studio local server — any non-empty value works.

### 4. Verify and run

```bash
uv run python doctor.py
uv run python main.py
```

## Context Length Notes

DeepAgents' built-in middlewares (filesystem, subagents, todo, summarization) produce a combined system prompt of **~5,800 tokens**.

| Context setting | Result |
|----------------|--------|
| 4096 (default) | ❌ `n_keep >= n_ctx` error |
| 8192 | ✅ Basic operation possible |
| 16384 (recommended minimum) | ✅ Based on observed max tokens (8109) × 2 |
| 131072 (128k) ★ | ✅ Ample headroom for multi-turn rubric loop |

## BYOK vs LM Studio Comparison

| | BYOK (Anthropic) | LM Studio (local) |
|--|-----------------|------------------|
| API key | Required (`sk-ant-...`) | Not required |
| Cost | Per-token billing | Free |
| Speed | Fast | Depends on hardware |
| Quality | High (Claude) | Depends on model |
| Internet | Required | Not required |
| Config | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL=http://127.0.0.1:1234` |

Both modes work with the same `main.py` / `graph.py` — just swap the `.env` values.
