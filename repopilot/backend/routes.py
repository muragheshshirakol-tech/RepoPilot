import asyncio
from pipeline import run_job
import uuid
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional

import db  # CRITICAL: Import your database layer

router = APIRouter(prefix="/api", tags=["api"])

# --- Pydantic Models ---
class RepoSubmitRequest(BaseModel):
    repo_url: str
    role: str

class QuestionRequest(BaseModel):
    question: str

class Citation(BaseModel):
    path: str
    start: int
    end: int

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]

# --- Endpoints ---

@router.post("/repos")
async def submit_repo(request: RepoSubmitRequest):
    """Accept a repo URL and role, save to DB, return a job_id."""
    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL.")
    
    job_id = str(uuid.uuid4())
    
    # Save to Supabase (Real DB)
    try:
        db.create_repo(url=request.repo_url, job_id=job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {"job_id": job_id, "status": "queued"}

@router.get("/repos/{job_id}")
async def get_repo_status(job_id: str):
    """Get the status of a submitted job from DB."""
    repo = db.get_repo(job_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Job not found")
    return repo

@router.get("/repos/{job_id}/plan")
async def get_plan(job_id: str):
    """Get the generated onboarding plan from DB."""
    plan = db.get_plan(job_id)
    
    if not plan:
        return {"job_id": job_id, "status": "processing", "plan": None}
        
    return {"job_id": job_id, "status": "complete", "plan": plan}

@router.get("/repos/{job_id}/tour")
async def get_tour(job_id: str):
    """Get the 8-step code tour."""
    plan = db.get_plan(job_id)
    
    if not plan:
        return {"job_id": job_id, "tour_steps": []}
    
    # Extract tour_steps if they exist in the plan JSON
    tour_steps = plan.get("tour_steps", []) if isinstance(plan, dict) else []
    return {"job_id": job_id, "tour_steps": tour_steps}

@router.post("/repos/{job_id}/ask", response_model=AskResponse)
async def ask_question(job_id: str, request: QuestionRequest):
    """Grounded Q&A endpoint."""
    repo = db.get_repo(job_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Job not found")
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    # Call the new async qa.py pipeline
    from qa import answer_question
    
    # MUST use await here because answer_question is async
    result = await answer_question(job_id, request.question)
    
    return AskResponse(
        answer=result["answer"],
        citations=[Citation(**c) for c in result["citations"]]
    )

# --- WebSocket Endpoint (Restored) ---

@router.websocket("/repos/{job_id}/stream")
async def stream_progress(websocket: WebSocket, job_id: str):
    """Live progress stream for the frontend analysis screen."""
    await websocket.accept()
    
    # Check real DB instead of fake jobs_db
    repo = db.get_repo(job_id)
    if not repo:
        await websocket.send_json({"event": "error", "message": "Job not found"})
        await websocket.close()
        return

    try:
        # Mock stream for now. We will wire Sathwik's LangGraph pipeline here later.
        await websocket.send_json({"event": "start", "job_id": job_id})
        await websocket.send_json({"event": "progress", "node": "ingest", "status": "cloning"})
        await websocket.send_json({"event": "progress", "node": "parse", "status": "parsing"})
        await websocket.send_json({"event": "complete", "job_id": job_id})
        
    except WebSocketDisconnect:
        print(f"Client disconnected for job {job_id}")
    except Exception as e:
        await websocket.send_json({"event": "error", "message": str(e)})
    finally:
        await websocket.close()