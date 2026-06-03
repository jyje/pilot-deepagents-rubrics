# Result: Fibonacci pytest — RubricMiddleware Demo

> Model: `google/gemma-4-e4b` via LM Studio (local, free)
> Run ID: `019e8cda-77d6-7c51-8d2b-5aaec773e81e`
> Status: **satisfied** (iterations: 2)

## Input

**Message:**
```
피보나치 수열의 테스트 케이스를 pytest로 작성해주세요
```

**Rubric:**
```
- pytest 형식의 test 함수 포함
- 경계값(0, 1) 케이스 포함
- 실제로 실행 가능한 코드
```

## LangGraph Studio — Interact View

![LangGraph Studio Interact](assets/result-fibonacci-interact.png)

The trace shows the full execution path ending with `RubricMiddleware.after_agent`:
- `_rubric_evaluations`: 2 entries (eval[0] needs_revision, eval[1] satisfied)
- `_rubric_iterations`: 2
- `_rubric_status`: **satisfied**

## LangGraph Studio — Trace View

![LangGraph Studio Trace](assets/result-fibonacci-trace.png)

The Trace tab shows each node's latency and token count:
- `model` (1st): 52.5s · 12K tokens — wrote `test_fibonacci.py`
- `tools` (write_file): 0.02s
- `model` (2nd): 7.78s · 12.3K tokens — received grader feedback, created plan
- `tools` (write_todos + write_file): wrote `math_utils.py`
- `model` (3rd): 15.29s · 13.2K tokens — confirmed step completion
- `RubricMiddle...` (grader): 20.43s · 2.4K tokens — grader evaluated → needs_revision
- `model` (4th): 20.37s · 2.4K tokens — (grader internal)
- `model` (5th): 33.75s · 13.9K tokens — final confirmation

## Rubric Loop

### eval[0] — needs_revision

The agent wrote syntactically correct pytest code but the file depended on an external `math_utils.py` that was not provided.

**Grader feedback:**
> The generated code requires an external file (`math_utils.py`) and a function definition to actually run as complete, standalone, executable code. While the test file is written, it's not fully self-contained/executable without `math_utils.py`.

**Failing criterion:**
- ✗ 실제로 실행 가능한 코드

### eval[1] — satisfied

The agent created a 2-step plan (`write_todos`), wrote `math_utils.py` with a complete `fib(n)` implementation, and confirmed both files are in place.

**All criteria passed:**
- ✓ pytest 형식의 test 함수 포함
- ✓ 경계값(0, 1) 케이스 포함
- ✓ 실제로 실행 가능한 코드

## Final Output

**`test_fibonacci.py`**

```python
import pytest
from math_utils import fib

@pytest.mark.parametrize("n, expected", [
    (0, 0),      # Base case: F(0) = 0
    (1, 1),      # Base case: F(1) = 1
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (10, 55),
])
def test_fibonacci_positive_integers(n, expected):
    assert fib(n) == expected

@pytest.mark.parametrize("n", [-1, -5])
def test_fibonacci_negative_input(n):
    with pytest.raises(ValueError, match="Fibonacci is not defined for negative numbers"):
        fib(n)

def test_fibonacci_non_integer_input():
    with pytest.raises(TypeError):
        fib(5.5)
```

**`math_utils.py`**

```python
def fib(n):
    """
    Calculates the nth Fibonacci number iteratively.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is a negative integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

## Token Usage

| Call | Role | Input tok | Output tok | Cache read |
|------|------|-----------|------------|------------|
| 1 | main (write test) | 11,150 | 879 | 5,313 |
| 2 | main (write_todos) | 12,207 | 77 | 5,833 |
| 3 | main (explain) | 12,909 | 288 | 6,374 |
| 4 | main (plan 2-step) | 13,427 | 512 | 6,369 |
| 5 | main (write math_utils) | 14,447 | 219 | 7,054 |
| 6 | main (update todos) | 15,028 | 168 | 7,393 |
| 7 | main (confirm) | 15,612 | 82 | 7,635 |

## Insight

The grader caught a **non-obvious quality issue**: the test file was syntactically valid and contained all required test functions, yet it could not actually *run* because the implementation it imports (`math_utils.py`) did not exist.

This is exactly the kind of issue a human reviewer would catch but a simple syntax check would miss. The rubric criterion "실제로 실행 가능한 코드" forced the agent to think beyond code generation and deliver a complete, self-contained artifact.

The agent's response was also notable: rather than patching the test file, it correctly identified that the missing piece was the *implementation*, created a 2-step task plan, and delivered both files together.
