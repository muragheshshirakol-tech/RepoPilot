# RepoPilot Frontend 🚀

The Next.js 14 frontend for **RepoPilot**, an agentic AI platform built for the **IBM Bob 2.0 Hackathon**. RepoPilot ingests a GitHub repository and autonomously produces a personalized, interactive, and evidence-backed onboarding experience for new developers.

> **Developer:** Shruthan (Dev 2 - Frontend Lead)  
> **Status:** ✅ MVP Complete & Demo-Ready

## ✨ Key Features

- **🎯 Smart Submit Screen:** GitHub URL validation, role-based selection (Frontend, Backend, Full-Stack, etc.), and IBM-inspired `#0F62FE` branding.
- **📡 Live Analysis Dashboard:** Real-time WebSocket integration tracking the progress of IBM Bob subagents (Architecture & Business Logic) with dynamic progress bars and status badges.
- **🗺️ Interactive Code Tour Viewer:** An 8-step guided tour with syntax highlighting, `j`/`k` keyboard navigation, and file/line-range citations.
- **💬 Grounded Q&A Panel:** Chat interface that returns AI answers with **clickable citation pills**. Clicking a citation instantly scrolls the Code Tour Viewer to the exact file and line of code (The "Killer Demo Moment").
- **🛡️ Mock Data Fallback:** Built-in resilience. If the backend is unavailable during the live demo, the UI gracefully loads realistic mock data to ensure a flawless judging experience.

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4, shadcn/ui
- **Icons:** lucide-react
- **Visualization:** recharts, react-syntax-highlighter (One Dark theme)
- **State/Networking:** Native React Hooks, WebSocket API

## 🚀 Getting Started

### 1. Prerequisites
- Node.js 18+ 
- A running instance of the RepoPilot Backend (FastAPI on port 8000)

### 2. Environment Setup
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Installation & Development
```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## 📂 Project Structure

```text
frontend/
├── app/
│   ├── page.tsx                      # Submit Screen (Landing)
│   ├── analysis/[jobId]/page.tsx     # Live Analysis Screen (WebSocket)
│   └── onboarding/[jobId]/page.tsx   # 3-Column Onboarding Dashboard
── components/
│   ├── Navbar.tsx                    # Global navigation with IBM Plex Sans font
│   ├── CodeTourViewer.tsx            # Interactive code snippet viewer
│   └── QAPanel.tsx                   # Grounded Q&A chat interface
├── lib/
│   ├── types.ts                      # Strict TypeScript API contracts (shared with Backend)
│   ├── useWebSocket.ts               # Custom hook for real-time agent progress
│   └── mockData.ts                   # Fallback data for demo resilience
└── public/                           # Static assets
```

## 🔌 API Contracts

This frontend strictly adheres to the following backend endpoints (defined in `lib/types.ts`):

- `POST /api/repos` → Submits repo URL, returns `{ job_id, status }`
- `WS /api/repos/{jobId}/stream` → Streams `{ event, node, status }` for live UI updates
- `GET /api/repos/{jobId}/plan` → Fetches the generated `OnboardingPlan` JSON
- `POST /api/repos/{jobId}/ask` → Sends a question, returns `{ answer, citations: [{path, start, end}] }`

## 🏆 Hackathon Notes

- **Font:** Uses `IBM Plex Sans` (loaded via `next/font`) for authentic IBM branding.
- **Demo Resilience:** The `mockData.ts` fallback is automatically triggered if the backend fails to respond, ensuring the judges always see a fully populated, beautiful UI.
- **Keyboard Shortcuts:** In the Code Tour Viewer, press `j` (next) or `k` (previous) to navigate steps rapidly during the demo.

---
*Built with purpose using IBM Bob 2.0.*