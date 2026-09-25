# RepoPilot — Task Registry & Wiring Map

> **The single source of truth for what to do, who does it, and in
> what order.**
>
> Reference tasks by ID (`T-10.01`), prompts by ID (`P-30.06`).

---

## Numbering System

### Task IDs

```
T-{Developer}{Phase}.{Number}
```

| Field | Meaning | Range |
|-------|---------|-------|
| Developer | Dev number | 1–6 |
| Phase | Phase number | 0–4 |
| Number | Sequential within (dev, phase) | 01–09 |

Examples:
- `T-10.01` — Dev 1, Phase 0, Task 01
- `T-42.03` — Dev 4, Phase 2, Task 03
- `T-64.02` — Dev 6, Phase 4, Task 02

### Prompt IDs

Every task with an AI prompt gets a matching prompt ID:
`P-{Developer}{Phase}.{Number}`. Task `T-30.06` → Prompt `P-30.06`.

### Phase Codes

| Phase | Hours | Purpose |
|-------|-------|---------|
| P0 | 0–6 | Foundation |
| P1 | 6–12 | Core Pipeline |
| P2 | 12–24 | UI + Tour |
| P3 | 24–36 | Q&A + Polish |
| P4 | 36–48 | Demo + Submit |

### Gate Codes

| Gate | Hour | Meaning |
|------|------|---------|
| G-06 | 6 | Foundation must be done |
| G-12 | 12 | Pipeline must work end-to-end |
| G-18 | 18 | First end-to-end attempt |
| G-24 | 24 | UI + tour must be visible |
| G-30 | 30 | Integration freeze |
| G-36 | 36 | QA must be green |
| G-40 | 40 | Demo must be recorded |
| G-46 | 46 | Submission must be complete |

---

## Phase 0 — Foundation (Hours 0–6)

| Task ID | Owner | Task | Depends On | Deliverable |
|---------|-------|------|------------|-------------|
| T-10.01 | Dev 1 | Read playbook; confirm roles | — | Alignment |
| T-10.02 | Dev 1 | Create `CONTEXT_PACK.md` | T-10.01 | CTX-01 |
| T-10.03 | Dev 1 | Create monorepo | T-10.01 | Repo |
| T-10.04 | Dev 1 | Write architecture spec | T-10.03 | `docs/architecture.md` |
| T-20.01 | Dev 2 | Run `create-next-app` + `shadcn init` | T-10.03 | Next.js scaffold |
| T-20.02 | Dev 2 | Build submit screen | T-20.01 | `app/page.tsx` |
| T-20.03 | Dev 2 | Set up routing skeleton | T-20.01 | Route folders |
| T-30.01 | Dev 3 | Get Bob credentials | — | Bob IDE + Shell verified |
| T-30.02 | Dev 3 | Save Bob Shell CLI notes | T-30.01 | `docs/bob_api.md` |
| T-30.03 | Dev 3 | First successful Bob call | T-30.02 | Proof + screenshot |
| T-30.04 | Dev 3 | Draft `agents.md` | T-30.02 | AGT-01 |
| T-30.05 | Dev 3 | Draft `.bob/rules/onboarding.md` | T-30.02 | RUL-01 |
| T-30.06 | Dev 3 | Initial `bob_client.py` | T-30.03 | `bob_client.py` v1 |
| T-40.01 | Dev 4 | Create Supabase project | T-10.03 | DB instance |
| T-40.02 | Dev 4 | Write `schema.sql` | T-40.01 | `schema.sql` |
| T-40.03 | Dev 4 | Write `db.py` | T-40.02 | `db.py` |
| T-40.04 | Dev 4 | Write `main.py` skeleton | T-10.03 | `main.py` v1 |
| T-50.01 | Dev 5 | Install Tree-sitter | T-10.03 | Deps |
| T-50.02 | Dev 5 | Initial `parser.py` | T-50.01 | `parser.py` v1 |
| T-50.03 | Dev 5 | Test parser on `sindresorhus/ky` | T-50.02 | Evidence |
| T-60.01 | Dev 6 | Create Vercel project | T-10.03 | Vercel linked |
| T-60.02 | Dev 6 | Create Railway project | T-10.03 | Railway linked |
| T-60.03 | Dev 6 | Set up Sentry | T-10.03 | Sentry live |
| T-60.04 | Dev 6 | Write `.env.example` | T-30.02, T-40.01 | `.env.example` |
| T-60.05 | Dev 6 | Write `README.md` | T-10.04 | README |

**Gate G-06:** POST `/api/repos` returns a `job_id`. Parser runs on `ky`. Bob client returns JSON.

---

## Phase 1 — Core Pipeline (Hours 6–12)

| Task ID | Owner | Task | Depends On | Deliverable |
|---------|-------|------|------------|-------------|
| T-11.01 | Dev 1 | Build `graph.py` | T-30.06, T-40.04, T-50.02 | `graph.py` v1 |
| T-11.02 | Dev 1 | Write `synthesis.py` | T-11.01 | `synthesis.py` |
| T-11.03 | Dev 1 | Wire Bob into fanout | T-11.01, T-30.06 | Fanout live |
| T-21.01 | Dev 2 | Build live analysis screen | T-20.03, T-10.04 | Analysis page |
| T-21.02 | Dev 2 | Build `useWebSocket` hook | T-21.01 | Hook |
| T-31.01 | Dev 3 | Write `prompts.py` | T-30.04, T-30.05 | `prompts.py` v1 |
| T-31.02 | Dev 3 | Refine `bob_client.py` | T-30.06, T-31.01 | `bob_client.py` v2 |
| T-31.03 | Dev 3 | Test 2 subagents on `ky` | T-31.02 | DEL-03 v1 |
| T-41.01 | Dev 4 | Build `ingest.py` | T-40.03 | `ingest.py` |
| T-41.02 | Dev 4 | Build `routes.py` | T-40.04 | `routes.py` v1 |
| T-41.03 | Dev 4 | Wire WebSocket `ws.py` | T-41.02 | `ws.py` |
| T-51.01 | Dev 5 | Build `chunker.py` | T-50.02 | `chunker.py` |
| T-51.02 | Dev 5 | Build `embedder.py` | T-51.01, T-40.03 | `embedder.py` |
| T-61.01 | Dev 6 | Write `Dockerfile` | T-40.04 | `Dockerfile` |
| T-61.02 | Dev 6 | Deploy backend to Railway | T-61.01 | DEL-06 v1 |
| T-61.03 | Dev 6 | Deploy frontend to Vercel | T-20.03 | DEL-06 v2 |

**Gate G-12:** Pipeline runs end-to-end. DB has `AgentFinding` rows.

---

## Phase 2 — UI + Code Tour (Hours 12–24)

| Task ID | Owner | Task | Depends On | Deliverable |
|---------|-------|------|------------|-------------|
| T-12.01 | Dev 1 | Tour generator in `synthesis.py` | T-11.02 | DEL-07 v2 |
| T-12.02 | Dev 1 | Build `/plan` + `/tour` endpoints | T-11.03 | Endpoints live |
| T-12.03 | Dev 1 | Mid-point integration test | T-12.02, T-22.01 | G-18 met |
| T-22.01 | Dev 2 | Build onboarding dashboard | T-21.02 | Dashboard |
| T-22.02 | Dev 2 | Build `CodeTourViewer.tsx` | T-22.01 | Viewer |
| T-32.01 | Dev 3 | Refine prompts from P1 output | T-31.03 | `prompts.py` v2 |
| T-32.02 | Dev 3 | Capture Bob session screenshots | T-31.03 | Evidence |
| T-42.01 | Dev 4 | Build `qa.py` | T-51.02 | `qa.py` |
| T-42.02 | Dev 4 | Add `/ask` endpoint | T-42.01 | DEL-08 v1 |
| T-52.01 | Dev 5 | Build `search.py` | T-51.02 | `search.py` |
| T-52.02 | Dev 5 | Embedding quality check | T-51.02 | Report |
| T-62.01 | Dev 6 | Sentry dashboards | T-60.03 | Dashboards |
| T-62.02 | Dev 6 | Add request ID middleware | T-40.04 | Middleware |

**Gate G-24:** Browser shows architecture summary + code tour viewer.

---

## Phase 3 — Q&A + Polish (Hours 24–36)

| Task ID | Owner | Task | Depends On | Deliverable |
|---------|-------|------|------------|-------------|
| T-13.01 | Dev 1 | Learning path generation | T-12.01 | Extension |
| T-13.02 | Dev 1 | Full integration test | T-12.03, T-22.02, T-42.02 | DEL-08 v2 |
| T-23.01 | Dev 2 | Build `QAPanel.tsx` | T-22.02 | Panel |
| T-23.02 | Dev 2 | Inline citations (clickable) | T-23.01 | Polish |
| T-33.01 | Dev 3 | Full-repo retrieval prompt | T-32.01 | `QA_PROMPT` |
| T-33.02 | Dev 3 | Test on 2nd repo | T-33.01 | Validation |
| T-43.01 | Dev 4 | Edge cases for `/ask` | T-42.02 | Robustness |
| T-53.01 | Dev 5 | Hybrid search tuning | T-52.01 | Tuning |
| T-63.01 | Dev 6 | Smoke tests | All P2 | `test_smoke.py` |
| T-63.02 | Dev 6 | Edge-case QA on 3 repos | T-63.01 | QA report |

**Gate G-36:** Q&A answers with citations. Smoke tests pass.

---

## Phase 4 — Demo + Submit (Hours 36–48)

| Task ID | Owner | Task | Depends On | Deliverable |
|---------|-------|------|------------|-------------|
| T-14.01 | Dev 1 | Write pitch deck | T-13.02 | Deck |
| T-14.02 | Dev 1 | Rehearse demo narrative | T-14.01 | Rehearsal |
| T-24.01 | Dev 2 | Final UI polish | T-23.02 | Polish |
| T-24.02 | Dev 2 | Record screen capture | T-24.01 | Raw video |
| T-34.01 | Dev 3 | Final `BOB_PLAYBOOK.md` | T-33.02 | Playbook |
| T-34.02 | Dev 3 | Bundle Bob evidence | T-32.02 | Evidence zip |
| T-44.01 | Dev 4 | README with architecture | T-13.02 | Final README |
| T-54.01 | Dev 5 | Fallback demo data | T-13.02 | Fallback |
| T-64.01 | Dev 6 | Record final demo video | T-24.02, T-14.02 | DEL-09 |
| T-64.02 | Dev 6 | Submit to portal | DEL-09, T-34.01, T-44.01 | DEL-10 |

**Gate G-46:** Submission complete.

---

## Critical Path

```
T-30.01 → T-30.02 → T-30.03 → T-30.06 → T-31.02 → T-11.01
       → T-11.02 → T-12.01 → T-22.02 → T-13.02 → T-14.01
       → T-64.01 → T-64.02
```

Any delay on this chain directly delays the demo.

---

## Parallel Streams

| Stream | Tasks | Owner |
|--------|-------|-------|
| Bob | T-30.01 → T-30.06 → T-31.01 → T-31.02 | Dev 3 |
| Backend | T-40.01 → T-40.04 → T-41.01 → T-41.02 | Dev 4 |
| Frontend | T-20.01 → T-20.03 → T-21.01 → T-22.01 | Dev 2 |
| Code Intel | T-50.01 → T-50.02 → T-51.01 → T-51.02 | Dev 5 |
| Infra | T-60.01 → T-60.03 → T-61.01 | Dev 6 |

---

## The 30-Minute Rule

**No developer is stuck for more than 30 minutes without escalating.**

If you are stuck:
1. Open a fresh AI chat.
2. Paste `CONTEXT_PACK.md`.
3. Paste your task prompt.
4. Paste the error and current code.
5. Ask: "Give me the complete fixed code."
6. If it fails twice, escalate to Dev 1.
