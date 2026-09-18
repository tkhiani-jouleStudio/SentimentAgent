# Specification: feedback-sentiment-classifier-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md` and `intent.md` at the solution root)
- [x] Bootstrap agent code in `assets/feedback-sentiment-classifier-agent/` using instructions from the sap-agent-bootstrap section. (invoke from inside `assets/feedback-sentiment-classifier-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

> **Before proceeding**, read [guidelines-agent-skills.md](../guidelines-agent-skills.md) and decide — based on the PRD/intent — whether the agent needs runtime skills.

- [x] This agent performs a focused, single-purpose task (classify sentiment). No complex multi-step workflow, escalation path, or domain-specific reference material is required. **Skip runtime skill creation.**

---

## Project-Specific Tasks

### System Prompt — Sentiment Classification Behaviour

- [x] Open `assets/feedback-sentiment-classifier-agent/app/agent.py` and update the `@prompt_section` body (`get_system_prompt`) to include the following instructions:
  - The agent classifies free-text feedback into exactly one of three labels: **positive**, **negative**, or **neutral**.
  - The agent must return a structured JSON response with two fields: `sentiment` (one of: `positive`, `negative`, `neutral`) and `confidence` (a float between 0.0 and 1.0).
  - The agent must never fabricate, guess, or invent data; classification must be based solely on the provided feedback text.
  - If the input is empty or blank, the agent must return a structured error: `{"error": "empty_input", "message": "No feedback text provided."}`.
  - If confidence is below 0.7, the agent must include a `"low_confidence": true` flag in the response to signal that human review may be warranted.
  - For non-English text, the agent should attempt classification if the LLM supports the language, or return `{"error": "unsupported_language", "message": "Language not supported."}`.
  - Example output: `{"sentiment": "positive", "confidence": 0.95}`

### Input Handling

- [x] Ensure the agent accepts a plain text string as the user message (the feedback to classify). No structured JSON input wrapping is required — the feedback text is the full message body.
- [x] Handle empty or whitespace-only input gracefully: detect before calling the LLM and return the structured error response immediately.

### Classification Logic

- [x] The LLM call must be instructed to return ONLY a JSON object with `sentiment` and `confidence` fields — no prose, no explanation.
- [x] Parse the LLM response and validate: `sentiment` must be one of `positive`, `negative`, `neutral`; `confidence` must be a float in [0.0, 1.0].
- [x] If parsing fails (malformed LLM output), return: `{"error": "parse_error", "message": "Could not parse classification result."}`.
- [x] Append `"low_confidence": true` to the response when `confidence < 0.7`.

### Response Structure

- [x] All agent responses must be valid JSON strings matching one of these shapes:
  - Success: `{"sentiment": "<label>", "confidence": <float>}` (optionally with `"low_confidence": true`)
  - Error: `{"error": "<error_code>", "message": "<human-readable description>"}`

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone from the PRD using structured logging (`[MILESTONE_ID].[achieved|missed]: [description]`) and OpenTelemetry custom spans:
  - **M1 — Feedback Received**: log `M1.achieved: feedback input received and validated` / `M1.missed: feedback input was empty or invalid — classification aborted`
  - **M2 — Sentiment Analysed**: log `M2.achieved: LLM sentiment analysis completed` / `M2.missed: LLM call failed or returned an invalid response`
  - **M3 — Classification Returned**: log `M3.achieved: classification result returned — label={label}, confidence={confidence}` / `M3.missed: classification result could not be formatted or returned`
  - **M4 — Result Delivered**: log `M4.achieved: result delivered to caller` / `M4.missed: delivery to caller failed or timed out`
- [x] Extract all business logic from `stream()` into a plain async helper (e.g. `_classify_sentiment()`) and instrument that method — never use `with tracer.start_as_current_span(...)` inside an async generator
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

> This agent has no SAP API integrations. No MCP servers, translation files, or mock configs are required.

- [x] Confirm no `requires` entries are needed in `asset.yaml` (no MCP server dependencies).
- [x] Skip `mcp-translation-file`, `setup-solution` (MCP), and `mcp-mock-config` — there are no external tool calls.

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write unit tests in `assets/feedback-sentiment-classifier-agent/tests/`:
  - `test_classify_positive.py` — positive feedback text returns `{"sentiment": "positive", ...}`
  - `test_classify_negative.py` — negative feedback text returns `{"sentiment": "negative", ...}`
  - `test_classify_neutral.py` — neutral/factual feedback text returns `{"sentiment": "neutral", ...}`
  - `test_empty_input.py` — empty string returns the structured empty-input error
  - `test_low_confidence.py` — when LLM returns confidence < 0.7, response includes `"low_confidence": true`
  - `test_parse_error.py` — malformed LLM output returns the structured parse-error response
- [x] Write one integration test executing end-to-end agent flow by calling the agent's `invoke` function with a mocked LLM response (tests must run offline)
- [x] Run `pytest` from `assets/feedback-sentiment-classifier-agent/` (no args) — 116 passed, 76% coverage
- [x] Verify `assets/feedback-sentiment-classifier-agent/app/agent.py` has exactly 9 decorated functions — confirmed 9
- [x] Run `pytest` again from `assets/feedback-sentiment-classifier-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/feedback-sentiment-classifier-agent/` — confirmed
