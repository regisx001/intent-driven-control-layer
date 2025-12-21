# Datanova AI – Project Phases Roadmap

This roadmap breaks the project into **clear, progressive phases**.  
Each phase has a purpose, concrete outputs, and explicit “done” criteria.

---

## Phase 1 — Capability & Intent Modeling (Foundation)

### Goal
Lock down **what the system can do** and **how intent is represented**, before touching any LLM or UI.

### Key Tasks
- Enumerate supported platform capabilities
- Define the intent JSON schema
- Define allowed parameters and constraints
- Decide which actions are read-only vs mutating

### Deliverables
- Capability list (actions + params)
- Intent schema (JSON / TypeScript / OpenAPI)
- Validation rules (static)

### Done When
- You can reject an invalid intent without any AI involved
- The intent schema feels boring and obvious (this is good)

---

## Phase 2 — Validator & Router (Deterministic Core)

### Goal
Build the **non-AI heart** of the system.

### Key Tasks
- Implement schema validation
- Implement state validation (e.g. “train before load” is invalid)
- Implement permission / safety checks
- Implement confirmation logic for risky actions
- Route valid intents to existing platform APIs

### Deliverables
- Validator module
- Router module
- Clear error types and messages

### Done When
- You can execute intents from a JSON file
- The system works perfectly **without any AI**

---

## Phase 3 — Intent Service (LLM Integration)

### Goal
Introduce the LLM **only as a language-to-intent translator**.

### Key Tasks
- Define strict system prompt
- Implement intent generation endpoint
- Handle low-confidence or ambiguous outputs
- Enforce JSON-only responses
- Add retry / clarification strategy

### Deliverables
- Intent Service (isolated)
- Prompt + examples
- Confidence and uncertainty handling

### Done When
- The LLM cannot trigger execution directly
- Bad LLM output never crashes the system
- You can swap the LLM with a stub

---

## Phase 4 — Chat Interface (Controlled UX)

### Goal
Expose the intent system to users **safely and transparently**.

### Key Tasks
- Build a chat panel (FE)
- Display interpreted intent before execution
- Add confirm / cancel flow
- Show errors and explanations clearly
- Reuse existing charts and views

### Deliverables
- Chat UI component
- Intent preview UI
- Confirmation UX

### Done When
- Users can see *what the system thinks they asked*
- Users can stop actions before execution
- Forms still work unchanged

---

## Phase 5 — Feedback & Explanation Layer

### Goal
Close the loop between **action → result → understanding**.

### Key Tasks
- Surface execution results in chat
- Optionally use LLM to explain results
- Link results to visualizations
- Ensure explanations never affect state

### Deliverables
- Result formatter
- Explanation service (optional LLM)
- Error explanation mapping

### Done When
- Users understand what happened and why
- Explanations are helpful but optional

---

## Phase 6 — Safety, Failure & Guardrails

### Goal
Make failure **intentional, safe, and boring**.

### Key Tasks
- Design failure taxonomy
- Add fallback paths (forms, help)
- Add rate limiting / abuse prevention
- Add logging and audit trail

### Deliverables
- Failure-handling policy
- Audit logs
- Clear user-facing failure messages

### Done When
- The system fails loudly and safely
- Nothing irreversible happens without confirmation

---

## Phase 7 — Evaluation & Hardening

### Goal
Decide whether this should live on.

### Key Tasks
- Measure success vs forms
- Identify failure patterns
- Decide what not to support
- Document architectural decisions

### Deliverables
- Evaluation notes
- Known limitations list
- Architecture README

### Done When
- You can clearly justify keeping or killing the feature

---

## Phase 8 — Optional Extensions (Only If Worth It)

Examples:
- Multi-step intent planning
- Intent history and undo
- Power-user shortcuts
- Custom domain DSL
- Partial automation with human approval

These are **earned**, not assumed.

---

## Final Guiding Principle

> Each phase must be valuable **on its own**.  
> If a phase feels useless without the next one, you moved too fast.

This roadmap ensures:
- Architectural discipline
- Safe AI integration
- Real learning (not demos)
- A solid foundation for *Datanova AI*

---
