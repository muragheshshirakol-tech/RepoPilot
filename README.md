# RepoPilot Onboarding

> An agentic AI platform that turns any codebase into a guided,
> interactive onboarding experience for new developers.

**IBM Bob 2.0 Hackathon • Team RepoPilot • 48-Hour Build**

---

## Read Me First (For IBM Bob IDE)

If you are **IBM Bob 2.0** reading this workspace, here is your context:

- **Project name:** RepoPilot Onboarding
- **Team size:** 6 developers
- **Build window:** 48 hours
- **Primary tool:** You (IBM Bob 2.0) — Agent Mode, subagents, custom modes
- **Companion files:**
  - `CONTEXT_PACK.md` — shared AI context to paste into every chat
  - `agents.md` — the agent contract (identity, constraints, output schema)
  - `.bob/rules/onboarding.md` — custom rules for this workspace
  - `TASKS.md` — the 55-task registry with dependencies
  - `docs/architecture.md` — pipeline and state schema

**What we are asking of you:**
1. Analyze repositories with **full-repository context** — never snippet-level.
2. Every claim you make must cite `path/to/file.ext:START-END`.
3. Never speculate. If evidence is missing, say so explicitly.
4. Prefer the repo's own vocabulary over generic terms.
5. Output strict JSON when asked. No markdown fences. No preamble.

**What we are building you for:** RepoPilot itself uses Bob subagents at
runtime to analyze user-submitted repositories. You are both **the tool
we build with** and **a component of the product**.

---

## What RepoPilot Does

New developers take **8–10 weeks** to become productive in an unfamiliar
codebase, costing enterprises over **$300,000 per year** for a
50-engineer team.

**RepoPilot cuts that to days.**

A user submits a GitHub URL, selects a role (Backend, Frontend,
Full-Stack, Data, DevOps, QA), and RepoPilot:

1. **Clones** the repository to ephemeral storage.
2. **Parses** it with Tree-sitter (Python, TypeScript, JavaScript).
3. **Spawns two IBM Bob 2.0 subagents in parallel:**
   - **Architecture Agent** — modules, entry points, data flow
   - **Business Logic Agent** — domain concepts, invariants
4. **Synthesizes** their findings into an onboarding plan.
5. **Presents three deliverables:**
   - A visual architecture summary
   - An 8-step interactive code tour with citations
   - A grounded Q&A interface with inline citations

Every claim RepoPilot makes is evidence-backed. Every citation points
to a specific file and line range.

---

## Architecture (30-Second Version)

```
Developer → Next.js Frontend → FastAPI Backend → LangGraph Orchestrator
                                                        │
                                                        ├──▶ Bob Subagent: Architecture
                                                        ├──▶ Bob Subagent: Business Logic
                                                        │
                                                        ▼
                                                    Synthesis → OnboardingPlan
                                                        │
                                                        ▼
                                          Postgres + pgvector → Frontend renders tour
```

Full pipeline and state schema: [`docs/architecture.md`](docs/architecture.md).

---

## Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14, Tailwind, shadcn/ui | Fastest path to a polished UI |
| Backend | FastAPI (Python 3.11) | Native async |
| Orchestration | LangGraph | Stateful multi-agent flows |
| **AI Engine** | **IBM Bob 2.0 (Agent Mode, subagents)** | **Hackathon requirement + core capability** |
| Fallback LLM | GPT-4o (only if Bob unavailable) | Safety net |
| Code Parsing | Tree-sitter | Language-agnostic AST |
| Database | PostgreSQL + pgvector | Relational + vector in one system |
| Deployment | Vercel (FE) + Railway (BE) | Zero-config |
| Monitoring | Sentry + LangSmith | Errors + agent traces |

**Do not deviate from this stack.** If you need a new library, justify
it in the PR.

---

## Repository Structure

```
repopilot/
├── README.md                  ← you are here
├── CONTEXT_PACK.md
├── agents.md
├── TASKS.md
├── .gitignore
├── .bobignore
├── .env.example
├── .bob/
│   └── rules/
│       └── onboarding.md
├── bob_sessions/
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── bob_api.md
│   ├── BOB_PLAYBOOK.md
│   └── pitch_deck.md
├── backend/
│   ├── main.py
│   ├── graph.py
│   ├── bob_client.py
│   ├── ingest.py
│   ├── parser.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── search.py
│   ├── qa.py
│   ├── synthesis.py
│   ├── prompts.py
│   ├── db.py
│   ├── routes.py
│   ├── ws.py
│   ├── schema.sql
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
└── frontend/
    ├── app/
    ├── components/
    ├── lib/
    ├── package.json
    └── vercel.json
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- **IBM Bob IDE v2.0.2+** (hackathon-provisioned instance)
- **Bob Shell** (optional but recommended)
- A PostgreSQL database (Supabase free tier works)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Fill in your .env values
uvicorn main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`. Health check: `GET /health`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

### Bob IDE Setup

1. Install Bob IDE v2.0.2 or later.
2. Log in with your hackathon registration email.
3. Switch to the hackathon instance:
   **Settings → General → Team = `ibm-coding-challenge-uat` (us-east)**.
4. Verify **40 Bobcoins** in Settings → General → Budget.
5. Open this repo as your workspace.
6. Bob will automatically read `README.md`, `agents.md`, and
   `.bob/rules/onboarding.md`.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| `DATABASE_URL` | Postgres connection | Supabase → Connection string (Pooler mode) |
| `BOB_SHELL_PATH` | Path to Bob Shell binary | Usually just `bob` |
| `BOB_WORKSPACE_ROOT` | Temp dir for cloned repos | `/tmp/repopilot` |
| `OPENAI_API_KEY` | Fallback LLM (optional) | platform.openai.com |
| `GITHUB_TOKEN` | Private repo access (optional) | github.com/settings/tokens |
| `SENTRY_DSN` | Error monitoring | sentry.io |
| `NEXT_PUBLIC_API_URL` | Backend URL for frontend | `http://localhost:8000` |

**Never commit `.env`.** It is gitignored.

---

## Working With IBM Bob 2.0

### The Three Golden Rules

1. **Every Bob interaction gets a screenshot.**
   Save to `bob_sessions/team_taskNN_description.png`.
   This is a submission requirement.

2. **Every Bob task is logged.**
   Open Bob IDE → Tasks panel → click task header → screenshot.

3. **Never burn Bobcoins carelessly.**
   Total team budget: **240 Bobcoins**. Plan hourly. Test prompts in
   Claude/GPT first, then run through Bob once.

### How to Prompt Bob

Every prompt follows the same pattern:

```
1. Paste CONTEXT_PACK.md
2. Paste the task-specific prompt from TASKS.md
3. Ask for the complete file, no explanations
```

### Custom Rules Bob Follows

`.bob/rules/onboarding.md`:
- Cite evidence: `path/to/file.ext:START-END`
- Explain WHY, not just WHAT
- Order tours by conceptual dependency, not file hierarchy
- Prefer 8 tour steps. Reject >12 steps.

### Files Bob Must Ignore

`.bobignore` excludes:
- `.env`, `.env.*`, secrets
- `node_modules/`, `.next/`, `.venv/`
- `__pycache__/`
- Any `*.key` or `*.pem`

---

## The Task Registry

All 55 tasks across 5 phases are in [`TASKS.md`](TASKS.md).

**Task ID format:** `T-{Developer}{Phase}.{Number}`
- `T-10.01` = Dev 1, Phase 0, Task 01

**Prompt ID format:** `P-{Developer}{Phase}.{Number}` — matches the task.

### Phase Overview

| Phase | Hours | Purpose | Gate |
|-------|-------|---------|------|
| P0 | 0–6 | Foundation | G-06 |
| P1 | 6–12 | Core Pipeline | G-12 |
| P2 | 12–24 | UI + Tour | G-24 |
| P3 | 24–36 | Q&A + Polish | G-36 |
| P4 | 36–48 | Demo + Submit | G-46 |

---

## The Team

| Developer | Role | Primary Deliverable |
|-----------|------|---------------------|
| Dev 1 | Lead / Orchestrator | `graph.py`, `synthesis.py` |
| Dev 2 | Frontend | `app/**`, `components/**` |
| Dev 3 | IBM Bob Lead | `bob_client.py`, `prompts.py` |
| Dev 4 | Backend | `main.py`, `routes.py`, `db.py` |
| Dev 5 | Code Intelligence | `parser.py`, `chunker.py`, `embedder.py` |
| Dev 6 | DevOps / QA | Dockerfile, deployment, tests, demo |

---

## Conventions

### Git

**Branch model:** Trunk-based with short-lived feature branches.

**Branch naming:** `feature/<dev>-<short-desc>`

**Commit format:** Conventional Commits
```
feat(parser): add Tree-sitter Python support
fix(frontend): correct WebSocket reconnect logic
docs(readme): add Bob Shell setup
chore(bob_sessions): capture task03 screenshot
```

**Merge rule:** Only Dev 1 merges to `main`. Squash merge.

### Code Style

- **Python:** 4-space indent, type hints, async where I/O
- **TypeScript:** 2-space indent, strict mode
- **Every function has a 1-line docstring or comment**

### Evidence Discipline

Every Bob session → PNG screenshot → `bob_sessions/` → commit immediately.

Naming: `team_taskNN_shortdesc.png` (all lowercase, underscores).

---

## The Demo

**3-minute narrative video:**

1. **Act I (0:00–0:20)** — The problem: a new dev opens a 50k-line repo.
2. **Act II (0:20–2:30)** — Paste URL → agents light up → tour → question.
3. **Act III (2:30–3:00)** — Time-to-productivity drops from weeks to days.

**The one sentence judges must remember:**
> *"RepoPilot turns a codebase into a guided tour."*

---

## Submission Checklist

Before hour 46, verify:

- [ ] `main` branch is clean
- [ ] All Bob session screenshots in `bob_sessions/` (15+ files)
- [ ] `docs/BOB_PLAYBOOK.md` complete
- [ ] `README.md` finalized
- [ ] `agents.md` and `.bob/rules/onboarding.md` committed
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] 3-minute demo video recorded
- [ ] Pitch deck finalized
- [ ] Submission form filled
- [ ] Submitted at least 2 hours before deadline

---

## When Stuck

Follow the **Stuck Protocol**:

1. **STOP** after 15 minutes of thrashing.
2. Open a fresh AI chat.
3. Paste `CONTEXT_PACK.md`.
4. Paste the relevant task prompt from `TASKS.md`.
5. Paste the error and current code.
6. Ask: *"Give me the complete fixed code. Do not explain, just
   give me the file."*
7. If it fails twice, escalate to Dev 1.

**The 30-Minute Rule:** No developer is stuck for more than 30 minutes
without escalating.

---

*"The best hackathon project is not the most ambitious one. It is the
one that is finished, polished, and demonstrated."*
