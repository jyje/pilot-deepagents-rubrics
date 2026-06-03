# Anthropic API Setup Guide

## Overview

This project runs LangChain DeepAgents' `RubricMiddleware` on **Anthropic Claude**.
Since DeepAgents was designed for Claude, it works out of the box — no compatibility shims required.

## 1. Get an API Key

**1. Go to Anthropic Console**

Visit [https://console.anthropic.com](https://console.anthropic.com) and create an account.

**2. Create an API Key**

**Settings → API Keys → Create Key** → enter a name → create.

You'll see a key in `sk-ant-...` format.

> ⚠️ The key is shown only once at creation time. Copy it immediately.

**3. Set in `.env`**

```bash
cd src/
cp .env.sample .env
```

```dotenv
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

MAIN_MODEL=claude-sonnet-4-6
GRADER_MODEL=claude-haiku-4-5-20251001
```

**4. Verify**

```bash
uv run python doctor.py
```

`[PASS] Inference` confirms success.

## Models

| Model ID | Use | Notes |
|----------|-----|-------|
| `claude-sonnet-4-6` ★ | Main agent | High reasoning capability, default |
| `claude-opus-4-8` | Main agent | Highest quality |
| `claude-haiku-4-5-20251001` ★ | Grader agent | Fast and cheap; reliable structured output |

★ Default models for this project

> Full model list: [https://docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Anthropic Console API key |
| `ANTHROPIC_BASE_URL` | No | (official Anthropic API) | Set for Anthropic-compatible proxy |
| `MAIN_MODEL` | No | `claude-sonnet-4-6` | Main agent model ID |
| `GRADER_MODEL` | No | `claude-haiku-4-5-20251001` | Grader agent model ID |

## Why Anthropic?

DeepAgents was built for Anthropic Claude:
- `RubricMiddleware`'s structured output is natively compatible with Claude's `tool_use` format
- `GraderVerdict` parsing is optimized for Claude's response format
- Works with pure, unmodified code — no compatibility layer needed
