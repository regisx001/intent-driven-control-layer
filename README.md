# Intent-Driven Control Layer
### For Machine Learning and Data Science

---

## 1. Project Overview

This project introduces a **natural-language intent layer** on top of a machine learning and data science platform.
The goal is to make complex workflows easier to trigger while keeping all execution deterministic, validated, and controlled.

This layer does **not** replace your existing forms, charts, scripts, or APIs.
It adds a chat-based interface that translates user language into structured intents.

---

## 2. Core Principle

> **The AI proposes. The system decides.**

The model can interpret requests, but it cannot execute platform logic directly.
Every action goes through validation, routing rules, and platform permissions.

---

## 3. What This Intent Layer Supports

Examples of supported intent categories:
- Dataset loading and inspection
- Data profiling and quality checks
- Data cleaning using predefined strategies
- Feature preparation and transformation
- Model training with approved algorithms
- Model evaluation and reporting
- Visualization requests using existing components

The intent layer is limited to explicit, supported capabilities.
No hidden operations. No implicit side effects.

---

## 4. Intent Contract

Each user request is translated into one structured intent object.

```json
{
  "action": "model.train",
  "params": {
    "model_type": "logistic_regression",
    "dataset": "iris"
  },
  "confidence": 0.86,
  "requires_confirmation": false
}
```

Rules:
- One action per intent
- Explicit parameters only
- No execution logic in intent output
- No assumptions about hidden system state

---

## 5. Architecture Responsibilities

### Intent Service (LLM-backed)
- Interprets user requests
- Maps language to supported actions
- Produces strict structured output
- Flags uncertainty or ambiguity

### Validator + Router (Deterministic)
- Validates schema and constraints
- Checks state order and permissions
- Applies safety/confirmation policies
- Routes valid actions to existing APIs

---

## 6. Safety and Reliability

The system explicitly handles:
- Unsupported operations
- Ambiguous or low-confidence requests
- Invalid action sequences
- Missing required parameters

Expected behavior:
- Ask user to clarify
- Reject invalid intents with clear messages
- Require confirmation for risky operations
- Fall back to existing UI when appropriate

---

## 7. Definition of Done

This project is successful when:
- ML and data-science workflows can be initiated through intent
- Invalid or unsafe actions are blocked consistently
- All executions pass through deterministic validation
- Existing UI and APIs continue to work unchanged
- System behavior is explainable and auditable

---

## 8. What This Project Is Not

- Not an autonomous agent
- Not an AutoML replacement
- Not a bypass of platform business rules
- Not a substitute for explicit software logic

---

## 9. Long-Term Direction

Build a reliable, extensible intent layer for machine learning and data science that scales with platform capabilities while preserving safety, traceability, and control.

---

## 10. FastAPI Server (Simple)

This project now includes a simple FastAPI server in `src/api.py`.

### Run

```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
```

### Open

- API root: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

### Starter endpoints

- `GET /health`
- `GET /datasets`
- `GET /datasets/{dataset}/head?n_rows=5`
- `GET /datasets/{dataset}/tail?n_rows=5`
- `POST /intent/query`

`POST /intent/query` example body:

```json
{
  "prompt": "give me the last 1 row in energy dataset",
  "model": "functiongemma",
  "max_steps": 8
}
```
