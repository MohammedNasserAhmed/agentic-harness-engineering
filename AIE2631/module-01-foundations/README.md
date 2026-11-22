# Module 01 — Foundations: the agentic engineering vocabulary (4 h)

**Question:** What are we actually engineering when the model is only one component?

## Outcomes

Explain the boundaries among models, assistants, tools, workflows, agents, and harnesses; choose a justified autonomy level; identify evaluation and governance obligations across the software delivery lifecycle.

## Concept map

| Term | Operational meaning | Checkpoint question |
|---|---|---|
| Token / context window | Input/output units and finite active model context | What gets omitted when context fills? |
| Inference / temperature | Running a model; sampling behavior | Which outputs must be deterministic? |
| LLM / SLM | Large or small language model | What is the latency/privacy tradeoff? |
| Prompt engineering | Task and output instructions | What cannot be enforced by a prompt? |
| Context engineering | Selecting, organizing and refreshing relevant evidence and instructions | Who owns and validates each context item? |
| RAG / embeddings / reranking | Retrieval of external evidence using indexing, similarity and ranking | What evidence is cited and how is freshness checked? |
| Tool/function calling | Structured requests for an external capability | Who checks schemas and permissions? |
| Workflow | Preset task transitions | Can deterministic logic complete this? |
| AI agent | Software that chooses steps/tools toward a goal | Where can it act autonomously? |
| Agent harness | Runtime around the agent: tools, context, policy, execution, state and evaluation | What prevents unsafe actions? |
| Agent loop | Repeated plan → act → observe → decide | What is the stop condition? |
| Graph engineering | Explicit states and routed transitions | What happens on failure/retry? |
| Agentic coding | Using coding agents to inspect, modify and verify code | Who reviews the diff? |
| Spec-driven development (SDD) | Requirements and tests guide agent work | How is success observable? |
| MCP | Protocol for connecting AI applications to tools/data | Is a tool server trusted by default? No. |
| Skills / `SKILL.md` | Reusable task procedure and associated assets | Is it instruction or executable code? |
| `AGENTS.md` | Repository-scoped coding-agent guidance convention | How does the agent discover instruction scope? |
| Agentic DevOps / CDLC | AI-inclusive delivery lifecycle and controls | What evidence goes into CI/review? |
| HITL / approval gate | Human decision at a high-impact boundary | Can the system bypass approval? |
| Checkpoint / replay | Saved state and repeatable investigation | Are external side effects idempotent? |
| Observability / trace | Structured records of actions, errors and outcomes | Can we reconstruct a run safely? |
| Evaluation / LLM-as-judge | Rubrics and tests for correctness and quality | What independent checks validate a judge? |
| Multi-agent orchestration | Coordinating specialized agents | Does complexity justify extra agents? |
| Context rot / poisoning | Degradation or hostile influence in supplied context | Which source is authoritative? |
| Sandboxing / least privilege | Execution isolation and minimum permissions | What is technically prohibited? |

## Four-hour lab agenda

1. **45 min — Build the taxonomy.** Draw the stack: base model → application → tools → agent loop → harness → institutional controls.
2. **45 min — Decide the pattern.** Compare a deterministic policy lookup, one agent, and multi-agent design against the same request.
3. **60 min — Read a real trace.** Run `python -m aie2631.cli demo` and annotate each state, tool call and guardrail.
4. **45 min — Map the SDLC.** For requirements, design, code, tests, release and operations, assign AI tasks and required human checks.
5. **45 min — Quiz and decision record.** Defend why this course uses a single constrained agent before exploring orchestrated agents.

## Exercise: architecture decision record

Write 200–300 words covering goal, why a fixed workflow may suffice, where the agent adds value, boundary of autonomy, failure modes, budget limits and independent verification. **Stretch:** compare loop vs graph vs multi-agent using latency, control, cost and auditability.

## Verify

Learner can articulate that the **harness** is the control plane around the model and that model-generated tool arguments are never authorization.
