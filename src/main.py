import os
import warnings
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core._api import LangChainBetaWarning
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from deepagents import RubricMiddleware, create_deep_agent

warnings.filterwarnings("ignore", category=LangChainBetaWarning)
load_dotenv()


def _make_model(env_key: str, default: str) -> ChatAnthropic:
    kwargs: dict = {
        "model": os.getenv(env_key, default),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "max_retries": 4,
    }
    if base_url := os.getenv("ANTHROPIC_BASE_URL"):
        kwargs["base_url"] = base_url
    return ChatAnthropic(**kwargs)


def _print_result(result: dict) -> None:
    W   = 60
    SEP = "─" * W

    def box(label: str) -> None:
        print(f"\n┌{'─' * (W - 2)}┐")
        print(f"│ {label:<{W - 4}} │")
        print(f"└{'─' * (W - 2)}┘")

    ROLE_STYLE = {
        "human":  ("\033[1;34m", "👤 Human"),
        "ai":     ("\033[1;32m", "🤖 AI"),
        "tool":   ("\033[1;33m", "🔧 Tool"),
    }

    # ── 1. Messages ──────────────────────────────────
    box("\033[1m Conversation\033[0m")
    for msg in result.get("messages", []):
        role = msg.type if hasattr(msg, "type") else "unknown"
        style, label = ROLE_STYLE.get(role, ("", role.upper()))

        tokens = ""
        if isinstance(msg, AIMessage):
            usage = msg.usage_metadata or {}
            if usage:
                tokens = f"  [{usage.get('input_tokens',0)}→{usage.get('output_tokens',0)} tok]"
        print(f"\n{style}{label}{tokens}\033[0m")
        print(SEP)

        content = msg.content
        if isinstance(content, list):
            # Anthropic block format: [{"type": "text", "text": "..."}, ...]
            text = "\n".join(b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text")
        else:
            text = content or ""
        if text:
            print(text)

        if isinstance(msg, AIMessage) and msg.tool_calls:
            import json
            for tc in msg.tool_calls:
                args_str = json.dumps(tc["args"], ensure_ascii=False, indent=2)
                print(f"\n  \033[1;33m⤷ call  {tc['name']}\033[0m")
                for line in args_str.splitlines():
                    print(f"    {line}")

        if isinstance(msg, ToolMessage):
            print(f"  name : {msg.name}")

    # ── 2. Files written ─────────────────────────────
    files = result.get("files", {})
    if files:
        box("\033[1m Files written\033[0m")
        for path, meta in files.items():
            print(f"\n  \033[1m{path}\033[0m")
            print(SEP)
            for line in meta["content"].splitlines():
                print(f"  {line}")

    # ── 3. Rubric evaluation ──────────────────────────
    status     = result.get("_rubric_status", "n/a")
    iterations = result.get("_rubric_iterations", "n/a")
    evals      = result.get("_rubric_evaluations", [])

    status_color = "\033[1;32m" if status == "satisfied" else "\033[1;31m"
    box(f"\033[1m Rubric  {status_color}{status}\033[0m  (iterations: {iterations})")

    if rubric_text := result.get("rubric", ""):
        print(f"\033[2m{rubric_text.strip()}\033[0m")

    if evals:
        print()
        for i, ev in enumerate(evals):
            verdict  = ev.get("result", "?")
            v_color  = "\033[1;32m✓\033[0m" if verdict == "satisfied" else "\033[1;31m✗\033[0m"
            print(f"  {v_color} eval[{i}]  {verdict}")
            if explanation := ev.get("explanation", ""):
                print(f"      {explanation}")
            for c in ev.get("criteria", []):
                c_mark = "✓" if c.get("passed") else "✗"
                print(f"      {c_mark} {c.get('name','')}")

    print(f"\n{'═' * W}\n")


def main():
    rubric_middleware = RubricMiddleware(
        model=_make_model("GRADER_MODEL", "claude-haiku-4-5-20251001"),
        system_prompt="You are a strict code reviewer. Evaluate each criterion objectively.",
        max_iterations=3,
    )

    agent = create_deep_agent(
        model=_make_model("MAIN_MODEL", "claude-sonnet-4-6"),
        system_prompt="You are a careful Python engineer.",
        middleware=[rubric_middleware],
    )

    rubric_state = {}
    result = {}
    for chunk in agent.stream(
        {
            "messages": [HumanMessage(content="Write a Python function that reverses a string")],
            "rubric": (
                "- Has a docstring\n"
                "- Does not use built-in reverse or slicing [::-1]\n"
                "- Includes at least one usage example in the docstring\n"
            ),
        },
        stream_mode="values",
    ):
        result = chunk
        for k, v in chunk.items():
            if k.startswith("_rubric"):
                rubric_state[k] = v

    result.update(rubric_state)
    _print_result(result)


if __name__ == "__main__":
    main()
