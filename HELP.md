# Intent-Driven Control Layer  
### Foundational Project for *Datanova AI*

---

## 1. Project Overview

This project introduces a **natural-language control layer** on top of an existing data and ML platform.  
The objective is **not** to replace current workflows (forms, charts, configuration-driven flows), but to **augment** them with a chat-based interface that allows power users to interact with the platform using natural language.

The AI layer functions as an **intent translation mechanism**, converting user input into **structured, validated platform actions**.  
All execution remains deterministic and governed by the platform itself.

---

## 2. Problem Statement

The current platform:
- Is stable and reliable
- Uses forms, dropdowns, and charts
- Requires multiple inputs for advanced workflows

As functionality grows:
- User interaction becomes more complex
- Power users experience friction
- Repetitive tasks slow productivity

The challenge is to:
> Reduce interaction complexity **without compromising safety, correctness, or architectural integrity**.

---

## 3. Core Idea

Introduce a **chat interface** that allows users to express *intent* in natural language, for example:
- “Load the iris dataset”
- “Clean the data and retrain the model”
- “Show model performance”

The AI **does not execute actions**.  
It proposes **structured intent**, which is validated and executed through existing platform APIs.

---

## 4. Fundamental Design Principle

> **The AI proposes. The system decides.**

This principle ensures:
- No autonomous behavior
- No bypassing validation or business rules
- Full transparency and control

The platform remains the **single source of truth**.

---

## 5. Architectural Philosophy

- The AI layer is isolated from execution
- The platform logic remains unchanged
- The chat interface is optional
- The system behaves identically with or without AI enabled

This guarantees reversibility and maintainability.

---

## 6. Platform Capabilities and Scope

The AI layer is limited to a **small, explicit set of supported actions**, such as:
- Loading a dataset
- Inspecting dataset metadata
- Cleaning data using predefined strategies
- Training a model with supported algorithms
- Evaluating a trained model
- Displaying predefined visualizations

The AI cannot invent new operations or access internal logic beyond these capabilities.

---

## 7. Intent Contract

Each user request results in **one intent object**.

Example:
```json
{
  "action": "model.train",
  "params": {
    "model_type": "logistic_regression",
    "dataset": "iris"
  },
  "confidence": 0.81,
  "requires_confirmation": false
}
## Rules

- One action per intent  
- Explicit parameters only  
- No execution logic  
- No implicit assumptions about system state  

This contract decouples language understanding from system execution.

---

## 8. Intent Service Responsibilities

The Intent Service (LLM-backed) is responsible for:

- Interpreting user language  
- Mapping intent to a supported action  
- Producing structured JSON  
- Indicating uncertainty when necessary  

It must **not**:

- Execute platform logic  
- Chain actions  
- Modify state  
- Bypass validation  

---

## 9. Validator and Router Responsibilities

This layer is deterministic and contains **no AI logic**.

Responsibilities include:

- Schema validation  
- Permission checks  
- Platform state validation  
- Risk assessment and confirmation handling  
- Routing valid intents to existing APIs  

This layer enforces correctness and safety.

---

## 10. Failure Handling as a First-Class Feature

The system must explicitly handle:

- Ambiguous requests  
- Unsupported operations  
- Invalid execution order  
- Low-confidence interpretations  

Expected behaviors include:

- Asking the user to rephrase  
- Rejecting invalid actions with clear messages  
- Requesting confirmation for sensitive operations  
- Redirecting users to the traditional UI when appropriate  

Failure is intentional, visible, and controlled.

---

## 11. Chat Interface Role

The chat interface:

- Serves as an alternative input method  
- Displays the interpreted intent before execution  
- Allows users to confirm or cancel actions  
- Presents results using existing visual components  

The interface does not blindly trust AI output.

---

## 12. Use of External Language Models

External LLMs may be used to:

- Improve language understanding  
- Generate clearer explanations  
- Handle phrasing and clarification  

The LLM is treated strictly as a **language component**, not an authority over system behavior.

---

## 13. Definition of Done

The project is considered complete when:

- Valid workflows can be driven through chat  
- Invalid or unsafe actions are blocked  
- All executions go through existing APIs  
- Traditional UI remains fully functional  
- The AI layer can be disabled safely  
- System behavior is explainable and auditable  

---

## 14. What This Project Is and Is Not

### This project is:
- A control-layer enhancement  
- A UX simplification mechanism  
- A system architecture exercise  

### This project is not:
- A chatbot  
- An autonomous agent  
- An AutoML system  
- A replacement for explicit software logic  

---

## 15. Long-Term Vision

This project establishes the foundation for **Datanova AI**:

- A scalable and controlled AI interaction layer  
- Extendable to additional capabilities over time  
- Grounded in strong architectural boundaries  

The focus is **reliability, clarity, and control** — not AI novelty.
