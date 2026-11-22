# Module 02 — Agentic coding, managed context and tool protocols (4 h)

**Question:** How do we turn a natural-language change into a verified code change safely?

## Learn

- **Agentic coding lifecycle:** inspect repository → write executable spec → plan bounded changes → edit → run tests → inspect diff → seek human review → commit.
- **`AGENTS.md`:** repository instruction convention; scope, priorities, tests, safety boundaries and definition of done. It is not a universal executable standard.
- **`SKILL.md`:** reusable procedural instruction entrypoint; resources/scripts can supplement it. Exact skill discovery conventions vary by platform.
- **MCP:** client/server protocol exposing capabilities such as tools and resources. MCP transport, schemas and discovery are separate from authorization and trust.
- **Context engineering:** relevance, source provenance, permissions, time-to-live, summarization, retrieval and context budgets.
- **Executable specs:** user story, EARS-style requirements, acceptance criteria, negative tests and test evidence.
- **Agent comparison:** Codex, Claude Code, Gemini CLI, GitHub Copilot and others can be evaluated with the *same* task and rubric; capabilities and subscriptions vary by version.
- **Execution vs inference:** local CLI execution does not imply locally hosted inference; confirm the actual data path and residency.

## Hands-on (240 minutes)

| Minutes | Exercise | Result |
|---:|---|---|
| 0–35 | Inspect `AGENTS.md`; identify enforceable vs advisory instructions | Boundary table |
| 35–80 | Convert one change request into EARS/Given-When-Then checks | Revised spec |
| 80–120 | Inspect `.agents/skills/policy-evidence/SKILL.md`; define triggers and validation | Skill critique |
| 120–165 | Explore MCP concepts and the local read-only MCP-shaped descriptor | Tool schema map |
| 165–215 | Give one coding agent a bounded coding task, or use provided trace offline | Reviewed diff and tests |
| 215–240 | Present risks and handoff | Evidence summary |

## Task prompt for a coding agent

> Read `AGENTS.md` and `specs/change-request.md`. Add a test covering an unknown change ID. Implement the minimal change needed. Do not add dependencies, network access, mutating tools or secrets. Run tests and report the diff, commands and unresolved risks. Stop before committing.

## MCP inspection lab

Run `python -m aie2631.cli tools`. Compare discovered tool names, argument schemas and read-only permissions with the allowlist in `src/aie2631/tools.py`. A descriptor is **not** a networked MCP server; building a real server/client using a pinned SDK is an optional instructor extension, after offline setup and security review.

## Acceptance checks

- The learner explains the difference between an instruction file and a security enforcement mechanism.
- A change is backed by tests, a readable diff and explicit acceptance criteria.
- Every tool has a typed interface and documented allowed operation.
