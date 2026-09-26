// frontend/lib/types.ts

// 1. SUBMISSION (POST /api/repos)
export interface SubmitRequest {
    repo_url: string;
    role: "Backend" | "Frontend" | "Full-Stack" | "Data" | "DevOps" | "QA";
}

export interface SubmitResponse {
    job_id: string; // UUID
    status: "queued";
}

// 2. WEBSOCKET STREAM (WS /api/repos/{jobId}/stream)
// Used in: useWebSocket.ts and Analysis Screen
export interface WSEvent {
    event: "agent_progress" | "complete" | "error";
    node?: "ingest" | "parse" | "fanout" | "synthesize" | "emit";
    status?: "pending" | "running" | "processing" | "done" | "failed";
    findings_count?: number;
    error?: string;
    job_id?: string;
}

// 3. ONBOARDING PLAN (GET /api/repos/{jobId}/plan)
// Used in: Onboarding Dashboard & Code Tour Viewer
export interface TourStep {
    step: number;
    title: string;
    path: string;
    start: number;
    end: number;
    narration: string;
    code?: string; // Optional: frontend fallback if backend doesn't send raw code
}

export interface OnboardingPlan {
    role: string;
    architecture_summary: string;
    key_concepts: string[];
    tour_steps: TourStep[];
}

// 4. GROUNDED Q&A (POST /api/repos/{jobId}/ask)
// Used in: QAPanel.tsx
export interface QARequest {
    question: string;
}

export interface Citation {
    path: string;
    start: number;
    end: number;
}

export interface QAResponse {
    answer: string;
    citations: Citation[];
}

// 5. INTERNAL BOB AGENT FINDING (For Backend/Orchestrator alignment)
// Used internally by Dev 1 & Dev 3, but good to know for debugging
export interface AgentFinding {
    agent: "architecture" | "business_logic";
    summary: string;
    evidence: {
        path: string;
        start: number;
        end: number;
        note: string;
    }[];
    confidence: number; // 0.0 to 1.0
}