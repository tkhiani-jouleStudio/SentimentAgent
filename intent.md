# Feedback Sentiment Classifier Agent

An AI agent that analyzes submitted feedback and classifies the sentiment as positive, negative, or neutral.

## Business challenge

Users submit feedback in free-text form and there is no automated way to determine whether the tone is positive, negative, or neutral. Manual review is time-consuming and inconsistent. An AI agent is needed to classify feedback sentiment reliably and at scale.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Sentiment classification accuracy | — | 98% | — | Customer Feedback Analysis | user |

## Key Milestones

1. **Feedback received** — Agent receives a feedback text as input via the A2A protocol.
2. **Sentiment analysed** — Agent applies LLM-based reasoning to determine the sentiment tone.
3. **Classification returned** — Agent outputs a structured response with the sentiment label (positive / negative / neutral) and a confidence indicator.
4. **Result delivered** — The classification result is available to the caller for downstream use.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash Standard B2B

### Process Hierarchy

```
Lead to Cash Standard B2B
└── Market to Lead
    └── Customer Insight to Lead Development
        └── Analyze and respond to customer insight
```

### Summary

Feedback sentiment classification maps to the "Customer Insight to Lead Development" sub-process — specifically the activity of analyzing customer insight to understand customer tone and intent.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|-------------------|-------------------|--------------------|----- |---------------------|
| Classify feedback sentiment (positive / negative / neutral) | None | — | — | — | — | — | Yes | No standard SAP capability covers direct sentiment classification; custom AI agent required |
| Accept free-text feedback as input | SAP SuccessFactors Continuous Feedback (OData) | `sap.sf:apiResource:PMGMContinuousFeedback:v1` | — | — | — | — | No | API available; no MCP server found; agent can accept input directly via A2A |

### Key findings

- No standard SAP product or solution capability was found that directly covers sentiment classification of free-text feedback.
- SAP AI services (NLP, Text Classification) exist but are not accessible via MCP servers in this landscape.
- The SAP SuccessFactors Continuous Feedback API could serve as a feedback source if integration is needed later.
- A custom Python AI agent (A2A protocol) using an LLM is the best fit for this use case.
- The agent should return a structured response with the sentiment label and a confidence indicator.

## Recommendations

### Feedback Sentiment Classifier AI Agent

#### Executive Summary

Python AI agent classifies feedback sentiment via LLM reasoning.

#### Recommended Solution

A pro-code Python AI agent built on the A2A protocol. The agent accepts free-text feedback as input, applies LLM-based reasoning to determine the sentiment (positive, negative, or neutral), and returns a structured classification result with a confidence indicator. The agent includes OpenTelemetry instrumentation and automated tests.

#### Recommended solution category

AI Agent

#### Intent fit
95%
