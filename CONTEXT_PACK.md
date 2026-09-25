# RepoPilot — AI Context Pack v1.0

> **Paste this entire file at the top of every AI chat.**
> It ensures Claude, GPT, or Bob always has the same understanding of
> what we are building.

## What We Are Building

RepoPilot Onboarding: an agentic AI platform that ingests a GitHub
repository and autonomously generates a personalized onboarding
experience (architecture summary, code tour, grounded Q&A).

## Team Constraints

- 6 developers, 48 hours, limited deep expertise
- Must use IBM Bob 2.0 as the code analysis engine
- MVP scope: 1 repo, 2 subagents, 8-step tour, basic Q&A

## Tech Stack (DO NOT DEVIATE)

- Frontend: Next.js 14 (App Router), Tailwind, shadcn/ui
- Backend: FastAPI (Python 3.11+), Pydantic v2
- Orchestration: LangGraph
- Code parsing: Tree-sitter (Python, TypeScript, JavaScript only)
- Database: PostgreSQL + pgvector (via Supabase)
- LLM: IBM Bob 2.0 via Bob Shell CLI (primary), GPT-4o (fallback)
- Deployment: Vercel (FE), Railway (BE)

## Core Data Schemas (Use These Exactly)

    RepoContext: repo_url, default_branch, languages, file_count
    AgentFinding: agent, summary, evidence, confidence
    OnboardingPlan: role, tour_steps (8), architecture_summary,
                    key_concepts

Where:

    AgentFinding = {
      "agent": str,          # "architecture" | "business_logic"
      "summary": str,
      "evidence": [
        {"path": str, "start": int, "end": int, "note": str}
      ],
      "confidence": float    # 0.0 - 1.0
    }

    OnboardingPlan = {
      "role": str,
      "tour_steps": [
        {"step": int, "title": str, "path": str,
         "start": int, "end": int, "narration": str}
      ],
      "architecture_summary": str,
      "key_concepts": [str]
    }

## Rules for AI Responses

1. Always return COMPLETE, RUNNABLE code — no placeholders
2. Include all imports
3. Include error handling
4. Add inline comments explaining non-obvious logic
5. If a library is needed, state the exact pip/npm install
6. Assume the developer is a junior — explain any magic

## What NOT To Do

- Do NOT suggest new libraries without justification
- Do NOT change the data schemas
- Do NOT suggest Docker, Kubernetes, or complex infra
- Do NOT write tests unless explicitly asked
- Do NOT use a REST API for Bob — Bob is accessed via Bob Shell CLI

## Bob Integration Rule

Bob is invoked by shelling out to the `bob` CLI in non-interactive
mode. There is no `BOB_API_KEY`. The backend runs:

    bob --non-interactive --prompt "<prompt>" --workspace <repo_path>

The wrapper is `backend/bob_client.py`. If `bob` is not on PATH,
raise `NotImplementedError` — do NOT silently fall back.

## Current Task

PASTE THE SPECIFIC TASK PROMPT HERE
