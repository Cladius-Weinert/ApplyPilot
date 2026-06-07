# AI Architecture — ApplyPilot

**Audit date:** 2026-06-05

## Executive summary

ApplyPilot needs AI provider flexibility for cost, latency, privacy, and reliability. This PR upgrades the existing provider layer to support:

- Gemini
- OpenAI / GPT
- OpenRouter
- Claude via Anthropic
- DeepSeek
- Local OpenAI-compatible endpoints such as Ollama/llama.cpp

The public pipeline API remains simple: existing code can continue using `get_client().ask(...)`.

## Current architecture

```text
Pipeline stage -> applypilot.llm.get_client() -> LLMClient.ask/chat -> Provider endpoint
```

This is intentionally lightweight and avoids adding framework dependencies.

## Provider selection

Environment variables:

| Provider | Required env | Default model |
|---|---|---|
| Gemini | `GEMINI_API_KEY` | `gemini-2.0-flash` |
| OpenAI / GPT | `OPENAI_API_KEY` | `gpt-4o-mini` |
| OpenRouter | `OPENROUTER_API_KEY` | `google/gemini-2.0-flash-001` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Claude | `ANTHROPIC_API_KEY` or `CLAUDE_API_KEY` | `claude-3-5-haiku-latest` |
| Local | `LLM_URL` | `local-model` |

Optional overrides:

- `LLM_PROVIDER=gemini|openai|openrouter|deepseek|claude|local`
- `LLM_MODEL=<provider-specific-model>`
- `LLM_API_KEY=<optional local endpoint token>`

## Implementation notes

- OpenAI, OpenRouter, DeepSeek, and most local servers use OpenAI-compatible `/chat/completions`.
- Gemini starts on the OpenAI-compatible endpoint and falls back to native `generateContent` if the model is not available through compatibility mode.
- Claude uses Anthropic's Messages API directly.
- OpenRouter requests include app-identifying headers but no private user data in headers.

## Cost strategy

Recommended defaults by user type:

| User | Recommended provider |
|---|---|
| Beginner / low cost | Gemini |
| Model router / experimentation | OpenRouter |
| Cheap coding/reasoning tasks | DeepSeek |
| High-quality cover letters/review | Claude or GPT |
| Privacy-sensitive | Local endpoint |

## Next AI upgrades

1. **Provider-specific budgets**
   - Max cost per run.
   - Max calls per stage.

2. **Caching**
   - Cache score/tailor results by job URL + description hash + resume hash + model.

3. **Prompt injection hardening**
   - Treat job descriptions as untrusted data.
   - Add tests for malicious job postings.

4. **Structured outputs**
   - Add JSON schema validation for scoring and extraction.

5. **Provider fallback chains**
   - Example: Gemini -> DeepSeek -> local.
   - Use only on retryable failures, not content validation failures.

## Verdict

The upgraded provider abstraction is intentionally small but unlocks practical user value: lower cost, better model choice, and improved portfolio value without a large rewrite.
