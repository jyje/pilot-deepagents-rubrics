# Anthropic API 설정 가이드

## 개요

이 프로젝트는 LangChain DeepAgents의 `RubricMiddleware`를 **Anthropic Claude** 위에서 구동합니다.  
DeepAgents가 Claude 기준으로 설계되었으므로 별도 호환성 코드 없이 순정 그대로 동작합니다.

## 1. API 키 발급

**1. Anthropic Console 접속**

[https://console.anthropic.com](https://console.anthropic.com) 에 접속하여 계정을 만듭니다.

**2. API 키 생성**

**Settings → API Keys → Create Key** → 이름 입력 → 생성

`sk-ant-...` 형식의 키가 표시됩니다.

> ⚠️ 키는 생성 직후 한 번만 표시됩니다. 반드시 즉시 복사하세요.

**3. `.env`에 주입**

```bash
cd src/
cp .env.sample .env
```

```dotenv
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

MAIN_MODEL=claude-sonnet-4-6
GRADER_MODEL=claude-haiku-4-5-20251001
```

**4. 검증**

```bash
uv run python doctor.py
```

`[PASS] Inference` 가 뜨면 정상입니다.

## 사용 모델

| 모델 ID | 용도 | 특징 |
|--------|------|------|
| `claude-sonnet-4-6` ★ | 메인 에이전트 | 높은 추론 능력, 기본 모델 |
| `claude-opus-4-8` | 메인 에이전트 | 최고 품질 |
| `claude-haiku-4-5-20251001` ★ | 채점 에이전트 | 빠르고 저렴, 구조화 출력 안정적 |

★ 이 프로젝트의 기본 모델

> 전체 모델 목록: [https://docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)

## 환경 변수 요약

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `ANTHROPIC_API_KEY` | 필수 | — | Anthropic Console API 키 |
| `ANTHROPIC_BASE_URL` | 선택 | (공식 Anthropic API) | Anthropic 호환 프록시 사용 시 지정 |
| `MAIN_MODEL` | 선택 | `claude-sonnet-4-6` | 메인 에이전트 모델 ID |
| `GRADER_MODEL` | 선택 | `claude-haiku-4-5-20251001` | 채점 에이전트 모델 ID |

## 왜 Anthropic인가?

DeepAgents는 Anthropic Claude를 기준으로 설계되었습니다:
- `RubricMiddleware`의 structured output이 Claude의 tool_use 포맷과 네이티브 호환
- `GraderVerdict` 파싱이 Claude의 응답 포맷에 최적화
- 별도의 호환성 레이어 없이 순정 코드로 동작
