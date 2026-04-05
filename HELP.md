# Intent-Driven Control Layer
### Operational Guide for Machine Learning and Data Science

---

## 1. Purpose

This project adds a natural-language interface for machine learning and data-science operations while preserving strict execution control.

It enables users to express intent in plain language, then converts that request into structured platform actions.

---

## 2. Design Rule

> **The AI proposes. The platform decides.**

The AI layer is used for interpretation only.
Execution remains deterministic and enforced by platform validators and routers.

---

## 3. Why This Exists

As ML/DS platforms grow, workflows become harder to operate through forms alone.
This layer reduces interaction friction for power users while preserving:
- Safety
- Correctness
- Traceability
- Architectural boundaries

---

## 4. Supported Intent Scope

The intent layer is limited to explicit capabilities, such as:
- Load datasets
- Inspect schema and metadata
- Run data-quality checks
- Trigger approved preprocessing routines
- Train supported model families
- Run model evaluation
- Request predefined visual outputs

The system rejects unsupported or out-of-scope actions.

---

## 5. Intent Format

Each request yields one structured intent object.

```json
{
  "action": "data.profile",
  "params": {
    "dataset": "energy"
  },
  "confidence": 0.91,
  "requires_confirmation": false
}
```

Rules:
- One action per intent
- Explicit params only
- No direct execution instructions
- No hidden assumptions about state

---

## 6. Layer Responsibilities

### Intent Service (LLM)
- Understands user language
- Maps request to supported actions
- Produces constrained structured output
- Signals ambiguity and low confidence

### Validator + Router (Deterministic)
- Schema validation
- Permission and policy checks
- State-sequence validation
- Confirmation policy for sensitive actions
- Action dispatch to trusted platform APIs

---

## 7. Failure Handling

The platform must fail safely and clearly.

Typical failure cases:
- Unsupported operation
- Missing required parameters
- Invalid execution order
- Ambiguous request
- Low-confidence interpretation

Expected outcomes:
- Clarification prompt
- Explicit rejection with reasons
- Confirmation workflow for risky actions
- Fallback to non-chat UI paths

---

## 8. Chat Interface Role

The chat UI is an optional control surface.
It should:
- Show interpreted intent before execution
- Allow confirm/cancel interactions
- Display deterministic results and errors
- Reuse existing platform visual components

---

## 9. Safety Constraints

This project must not allow:
- Direct AI-triggered mutations outside validator/router
- Tool execution that bypasses policy checks
- Multi-action hidden chaining without explicit user approval
- Non-auditable behavior

---

## 10. Definition of Done

The implementation is complete when:
- Users can run valid ML/DS workflows via intent
- Invalid or unsafe intents are blocked reliably
- Existing forms/APIs remain functional
- AI can be disabled without breaking core flows
- Decisions and outcomes are auditable

---

## 11. What This Is Not

- Not a chatbot product
- Not an autonomous ML agent
- Not a replacement for deterministic platform logic
- Not a shortcut around governance or controls

---

## 12. Direction

Evolve this into a robust intent control layer for machine learning and data science, with stronger validation, better explainability, and stable operational guardrails.
