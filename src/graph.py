"""
Module-level graph export for LangGraph Studio.
Usage: uv run langgraph dev
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core._api import LangChainBetaWarning
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
