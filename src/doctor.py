"""
Diagnostic script: ENV settings, API availability, and basic inference.
Usage: uv run python doctor.py
"""

import os
import sys
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

# Disable tracing during doctor runs to avoid LangSmith SDK noise.
_ls_tracing_configured = os.getenv("LANGSMITH_TRACING", "")
os.environ["LANGSMITH_TRACING"] = "false"

PASS = "  [PASS]"
FAIL = "  [FAIL]"
SKIP = "  [SKIP]"
SEP  = "-" * 52


def section(title: str) -> None:
    print(f"\n{SEP}\n {title}\n{SEP}")


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = PASS if ok else FAIL
    line = f"{mark} {label}"
    if detail:
        line += f"\n         {detail}"
    print(line)
    return ok


# ── 1. ENV ──────────────────────────────────────────────

section("1. Environment Variables")

api_key      = os.getenv("ANTHROPIC_API_KEY", "")
base_url     = os.getenv("ANTHROPIC_BASE_URL", "")
main_model   = os.getenv("MAIN_MODEL",   "claude-sonnet-4-6")
grader_model = os.getenv("GRADER_MODEL", "claude-haiku-4-5-20251001")
ls_api_key   = os.getenv("LANGSMITH_API_KEY", "")
ls_tracing   = _ls_tracing_configured
ls_project   = os.getenv("LANGSMITH_PROJECT", "")

env_ok = True
env_ok &= check("ANTHROPIC_API_KEY is set",
                bool(api_key) and not api_key.startswith("sk-ant-xxx"),
                f"value: {api_key[:16]}..." if api_key else "not set")

endpoint = base_url or "https://api.anthropic.com (default)"
check("ANTHROPIC_BASE_URL", True,
      f"value: {base_url}" if base_url else "not set — using official Anthropic API")

env_ok &= check("MAIN_MODEL",   True, f"value: {main_model}")
env_ok &= check("GRADER_MODEL", True, f"value: {grader_model}")

ls_key_ok = bool(ls_api_key) and not ls_api_key.startswith("lsv2_pt_xxx")
check("LANGSMITH_API_KEY is set (optional)",
      ls_key_ok,
      f"value: {ls_api_key[:16]}..." if ls_key_ok else "not set — Studio traces will be missing")
check("LANGSMITH_TRACING (optional)",
      ls_tracing.lower() == "true",
      f"value: {ls_tracing!r}" if ls_tracing else "not set")
check("LANGSMITH_PROJECT (optional)",
      bool(ls_project),
      f"value: {ls_project}" if ls_project else "not set — will use default project")


# ── 2. API Connectivity ──────────────────────────────────

section("2. API Connectivity")

def http_get(url: str, key: str, extra_headers: dict | None = None) -> tuple[int, str]:
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status, resp.read(256).decode()
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)
    except Exception as e:
        return 0, str(e)

if not api_key or api_key.startswith("sk-ant-xxx"):
    print(f"{SKIP} API connectivity — ANTHROPIC_API_KEY not configured")
    conn_ok = False
else:
    models_url = f"{base_url.rstrip('/')}/v1/models" if base_url else "https://api.anthropic.com/v1/models"
    status, body = http_get(models_url, api_key)
    conn_ok = check(
        f"GET {models_url}",
        status == 200,
        f"HTTP {status}" + (f": {body[:80]}" if status != 200 else ""),
    )


# ── 3. Basic Inference ──────────────────────────────────

section("3. Basic Inference")

if not env_ok or not conn_ok:
    print(f"{SKIP} Inference checks — fix ENV / connectivity first")
    infer_ok = False
else:
    try:
        from langchain_anthropic import ChatAnthropic
        from langchain_core.messages import HumanMessage

        def run_inference(model_id: str, prompt: str) -> str:
            kwargs: dict = {
                "model": model_id,
                "anthropic_api_key": api_key,
                "max_tokens": 64,
            }
            if base_url:
                kwargs["base_url"] = base_url
            llm = ChatAnthropic(**kwargs)
            return llm.invoke([HumanMessage(content=prompt)]).content.strip()

        resp = run_inference(main_model, "Reply with exactly: OK")
        main_ok = check(f"MAIN_MODEL inference ({main_model})", bool(resp), f"response: {resp[:60]!r}")

        resp = run_inference(grader_model, "Reply with exactly: OK")
        grader_ok = check(f"GRADER_MODEL inference ({grader_model})", bool(resp), f"response: {resp[:60]!r}")

        infer_ok = main_ok and grader_ok

    except ImportError as e:
        print(f"{FAIL} langchain-anthropic not installed — run: uv sync")
        print(f"         {e}")
        infer_ok = False
    except Exception as e:
        print(f"{FAIL} Inference error: {e}")
        infer_ok = False


# ── 4. LangSmith ────────────────────────────────────────

section("4. LangSmith (optional)")

if not ls_key_ok:
    print(f"{SKIP} LangSmith connectivity — LANGSMITH_API_KEY not configured")
    ls_ok = False
else:
    status, body = http_get("https://api.smith.langchain.com/ok", ls_api_key,
                            extra_headers={"Authorization": f"Bearer {ls_api_key}"})
    ls_ok = check(
        "GET https://api.smith.langchain.com/ok",
        status == 200,
        f"HTTP {status}" + (f": {body[:80]}" if status != 200 else ""),
    )


# ── Summary ─────────────────────────────────────────────

section("Summary")
results = {
    "ENV":          (env_ok,   False),
    "Connectivity": (conn_ok,  False),
    "Inference":    (infer_ok, False),
    "LangSmith":    (ls_ok,    True),
}
all_ok = True
for name, (ok, optional) in results.items():
    if optional:
        mark   = PASS if ok else SKIP
        suffix = "" if ok else " (optional — Studio traces disabled)"
        print(f"{mark} {name}{suffix}")
    else:
        check(name, ok)
        all_ok &= ok

print()
if all_ok:
    print("All checks passed. Ready to run main.py.")
    if not ls_ok:
        print("  hint: set LANGSMITH_API_KEY to enable Studio run traces.")
else:
    print("Some checks failed. See details above.")

sys.exit(0 if all_ok else 1)
