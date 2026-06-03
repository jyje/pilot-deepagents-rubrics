# LM Studio 로컬 설정 가이드

## 개요

[LM Studio](https://lmstudio.ai)의 **REST API v1 (Anthropic-compatible)** 를 사용하면
유료 Anthropic API를 사용할 수 없는 경우, 별도 API 키 없이 로컬 모델로 이 프로젝트를 실행할 수 있는 대안입니다.

> **참고:** DeepAgents는 Anthropic Claude를 기준으로 설계되었습니다. LM Studio 로컬 모델은 Anthropic 호환 API를 통해 동작하지만, 모델 품질과 tool_use 신뢰도는 모델에 따라 다를 수 있습니다.

```
main.py / graph.py
    │  Anthropic API format
    ▼
LM Studio Local Server  (http://127.0.0.1:1234)
    │  Anthropic-compatible endpoint
    ▼
로컬 LLM (예: google/gemma-4-e4b)
```

## 설정 방법

### 1. LM Studio 설치 및 모델 다운로드

1. [https://lmstudio.ai](https://lmstudio.ai) 에서 LM Studio 다운로드
2. 좌측 **Discover** 탭에서 모델 검색 후 다운로드
   - 권장: `google/gemma-4-e4b` (6.3 GB, tool_use 지원)
   - 또는: `meta-llama/llama-3.1-8b-instruct` 등 tool_use 지원 모델

### 2. 로컬 서버 설정

1. 좌측 **Developer** 탭 클릭
2. **Local Server** → **Status: Running** 활성화
3. 모델 로드 시 **Context and Offload** 설정:

| 항목 | 권장값 | 설명 |
|------|--------|------|
| Context Length | `131072` (128k) | 권장 최소 16384 (실측 최대 8109 tok × 2). 128k 설정 시 멀티턴 여유 충분 |
| GPU Offload | 디바이스에 따라 조정 | VRAM에 맞게 설정 |

4. **API Format**: REST API v1 → **Anthropic-compatible** 탭 확인

서버 주소: `http://127.0.0.1:1234`

### 3. `.env` 설정

```dotenv
ANTHROPIC_API_KEY=lm-studio
ANTHROPIC_BASE_URL=http://127.0.0.1:1234

MAIN_MODEL=google/gemma-4-e4b
GRADER_MODEL=google/gemma-4-e4b
```

> `ANTHROPIC_API_KEY`는 LM Studio 로컬 서버에서 검증하지 않으므로 임의 값 사용 가능

### 4. 검증 및 실행

```bash
uv run python doctor.py
uv run python main.py
```

## Context Length 주의사항

DeepAgents는 기본 미들웨어(filesystem, subagents, todo, summarization)의
시스템 프롬프트 합계가 **~5,800 토큰**입니다.

| Context 설정 | 결과 |
|-------------|------|
| 4096 (기본값) | ❌ `n_keep >= n_ctx` 에러 |
| 8192 | ✅ 기본 동작 가능 |
| 16384 (권장 최소) | ✅ 실측 최대 토큰(8109) × 2 기준 |
| 131072 (128k) ★ | ✅ 멀티턴 루브릭 루프 충분 |

## BYOK vs LM Studio 비교

| | BYOK (Anthropic) | LM Studio (로컬) |
|--|-----------------|-----------------|
| API 키 | 필요 (`sk-ant-...`) | 불필요 |
| 비용 | 토큰당 과금 | 무료 |
| 속도 | 빠름 | 하드웨어에 따라 다름 |
| 품질 | 높음 (Claude) | 모델에 따라 다름 |
| 인터넷 | 필요 | 불필요 |
| 설정 | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL=http://127.0.0.1:1234` |

두 방식 모두 `main.py` / `graph.py` 코드 변경 없이 `.env`만 바꿔서 전환 가능합니다.
