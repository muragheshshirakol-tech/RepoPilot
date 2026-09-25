# RepoPilot — Pitch Deck Outline

**10 slides. 5 bullets max per slide. Judge-ready.**

---

## Slide 1 — Title

- **RepoPilot Onboarding**
- *An agentic AI platform that turns any codebase into a guided tour*
- IBM Bob 2.0 Hackathon — [Team name]
- [Date]

---

## Slide 2 — The Problem

- New engineers take **8–10 weeks** to become productive
- Cost: **$300K/year** for a 50-engineer team
- 25% of technical hires leave within 12 months
- Current tools: static READMEs, grep, generic chatbots
- None of them explain **why** — only **what**

---

## Slide 3 — The Solution

- Submit a GitHub URL → get an onboarding plan
- **8-step interactive code tour** with citations
- **Visual architecture summary** from AI analysis
- **Grounded Q&A** — every answer cites a file:line
- Reads the whole repository, not snippets

---

## Slide 4 — Live Demo

- [Screenshot: submit screen]
- [Screenshot: agent cards lighting up]
- [Screenshot: code tour with citations]
- [Screenshot: Q&A with inline citations]
- [Timing: 60 seconds total]

---

## Slide 5 — How It Works

- **Ingest → Parse → Embed → Spawn → Synthesize → Emit**
- Tree-sitter parses code into ASTs
- Two Bob subagents analyze in parallel
- Synthesis merges findings into a structured plan
- Frontend renders the tour

---

## Slide 6 — IBM Bob 2.0 Usage

- **Agent Mode** for autonomous analysis
- **Two subagents** running in parallel
- **Custom modes** for RepoPilot's persona
- **Custom rules** enforcing `path:start-end` citations
- **Bob Shell** powering runtime analysis

---

## Slide 7 — Architecture

- Frontend: Next.js 14 + Tailwind
- Backend: FastAPI (Python 3.11)
- Orchestration: LangGraph
- AI: IBM Bob 2.0 + Tree-sitter
- Database: PostgreSQL + pgvector

---

## Slide 8 — Traction & Scalability

- Works on any public GitHub repo
- Handles Python, TypeScript, JavaScript
- Scales to enterprise monorepos
- Extensible to more languages via Tree-sitter
- Open API for integration

---

## Slide 9 — The Team

- **Dev 1** — Lead / Orchestrator
- **Dev 2** — Frontend
- **Dev 3** — IBM Bob Lead
- **Dev 4** — Backend
- **Dev 5** — Code Intelligence
- **Dev 6** — DevOps / QA

---

## Slide 10 — The Ask / Closing

- *"RepoPilot turns a codebase into a guided tour."*
- Try it: [deployed URL]
- Source: [GitHub URL]
- Thank you
