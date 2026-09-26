import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="RepoPilot Backend", version="1.0.0")

# --- CORS Middleware (Crucial for Shruthan's Frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models (Matching the Context Pack) ---
class RepoContext(BaseModel):
    repo_url: str
    default_branch: Optional[str] = "main"
    languages: Optional[List[str]] = []
    file_count: Optional[int] = 0

class EvidenceItem(BaseModel):
    path: str
    start: int
    end: int
    note: str

class AgentFinding(BaseModel):
    agent: str
    summary: str
    evidence: List[EvidenceItem]
    confidence: float

class TourStep(BaseModel):
    step: int
    title: str
    path: str
    start: int
    end: int
    narration: str

class OnboardingPlan(BaseModel):
    role: str
    tour_steps: List[TourStep]
    architecture_summary: str
    key_concepts: List[str]

class RepoSubmitRequest(BaseModel):
    repo_url: str
    role: str

# In-memory job store for Phase 0 (Will be replaced by DB calls in Phase 1)
jobs = {}

# --- Endpoints ---
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/api/repos")
async def submit_repo(request: RepoSubmitRequest):
    """Accept a repo URL and role, return a job_id."""
    # Basic validation
    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL. Must start with https://github.com/")
    
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "repo_url": request.repo_url,
        "role": request.role,
        "status": "queued"
    }
    
    # TODO: In Phase 1, we will trigger the background ingestion task here
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/repos/{job_id}")
async def get_repo_status(job_id: str):
    """Get the status of a submitted job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

# --- Uvicorn Entry Point ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)