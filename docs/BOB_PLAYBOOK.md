# RepoPilot — IBM Bob 2.0 Playbook

**Team:** [Team name]
**Event:** IBM Bob 2.0 Hackathon
**Submission date:** [Date]
**Bob IDE version:** v2.0.2+

---

## 1. Overview — How We Used Bob

RepoPilot is an agentic AI platform for developer onboarding. IBM
Bob 2.0 is not a wrapper or a helper — it is both the tool we built
with and a runtime component of the product itself.

**Two roles for Bob:**

1. **Development partner.** We used Bob IDE's Agent Mode, subagents,
   and custom modes to build the RepoPilot codebase.
2. **Runtime engine.** RepoPilot's backend invokes Bob via Bob Shell
   to analyze user-submitted repositories.

Total Bobcoins used: [fill in]
Total Bob sessions captured: [fill in — must be 15+]

---

## 2. Custom Rules Configuration

We shipped `.bob/rules/onboarding.md` to enforce evidence-based
reasoning in every Bob interaction:

```markdown
[Paste the full contents of .bob/rules/onboarding.md here]
```

**Why this matters:** Bob's default behavior produces plausible
but uncited summaries. Our rules require every claim to cite
`path:start-end`, which is the foundation of RepoPilot's trust model.

---

## 3. The `agents.md` Contract

We shipped `agents.md` at the repository root to give Bob a persistent
identity across sessions:

```markdown
[Paste the full contents of agents.md here]
```

**Why this matters:** The hackathon guide notes that the strongest
submissions treated Bob as a teammate that needed onboarding. This
file is Bob's onboarding document.

---

## 4. Three Specific Examples of Bob Solving Problems

### Example 1 — [Title]

**Problem:** [What we were stuck on]

**Bob interaction:** [What we asked Bob]

**Bob's contribution:** [What Bob produced]

**Evidence:** `bob_sessions/team_taskXX_description.png`

---

### Example 2 — [Title]

**Problem:** [What we were stuck on]

**Bob interaction:** [What we asked Bob]

**Bob's contribution:** [What Bob produced]

**Evidence:** `bob_sessions/team_taskXX_description.png`

---

### Example 3 — [Title]

**Problem:** [What we were stuck on]

**Bob interaction:** [What we asked Bob]

**Bob's contribution:** [What Bob produced]

**Evidence:** `bob_sessions/team_taskXX_description.png`

---

## 5. The Exact Prompts We Used With Bob

### Architecture Agent Prompt (from `backend/prompts.py`)

```
[Paste ARCHITECTURE_PROMPT]
```

### Business Logic Agent Prompt

```
[Paste BUSINESS_LOGIC_PROMPT]
```

### Q&A Retrieval Prompt

```
[Paste QA_PROMPT]
```

---

## 6. Screenshot Index

All Bob task session screenshots are in `bob_sessions/`.

| File | Task | Date |
|------|------|------|
| `team_task01_bob_setup_verify.png` | Verify Bob IDE + Shell | [date] |
| `team_task02_first_call.png` | First successful Bob call | [date] |
| `team_task03_architecture_agent.png` | Architecture Agent test | [date] |
| `team_task04_subagent_test.png` | Parallel subagent test | [date] |
| `team_task05_custom_rules_test.png` | Custom rules verification | [date] |
| `team_task06_mcp_settings.png` | MCP settings review | [date] |
| ... | [Add every screenshot here] | ... |

Full count at submission: [fill in]

---

## 7. Impact Summary

- **Development time saved:** [estimate]
- **RepoPilot runtime speed:** [average analysis time on 3 repos]
- **Evidence-backed accuracy:** [manual spot-check %]

---

## 8. What We Learned

[3–5 sentences on Bob's strengths and limitations]
