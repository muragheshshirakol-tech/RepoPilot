from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

router = APIRouter(prefix="/api", tags=["api"])

# --- Pydantic Models (Matching Context Pack) ---
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

# In-memory store for Phase 1 (Will be replaced by DB calls in Phase 2)
jobs_db = {}

# --- Endpoints ---

@router.post("/repos")
async def submit_repo(request: RepoSubmitRequest):
    """Accept a repo URL and role, return a job_id."""
    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL.")
    
    job_id = str(uuid.uuid4())
    jobs_db[job_id] = {
        "job_id": job_id,
        "repo_url": request.repo_url,
        "role": request.role,
        "status": "queued"
    }
    
    # TODO: In Phase 2, trigger Sathwik's LangGraph pipeline here
    return {"job_id": job_id, "status": "queued"}

@router.get("/repos/{job_id}")
async def get_repo_status(job_id: str):
    """Get the status of a submitted job."""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs_db[job_id]

@router.get("/repos/{job_id}/plan")
async def get_plan(job_id: str):
    """Get the generated onboarding plan."""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    # TODO: Fetch from DB in Phase 2
    return {"job_id": job_id, "plan": "Plan generation in progress..."}

@router.get("/repos/{job_id}/tour")
async def get_tour(job_id: str):
    """Get the 8-step code tour."""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    # TODO: Fetch from DB in Phase 2
    return {"job_id": job_id, "tour_steps": []}

@router.post("/repos/{job_id}/ask", response_model=AskResponse)
async def ask_question(job_id: str, request: QuestionRequest):
    """Grounded Q&A endpoint."""
    repo = db.get_repo(job_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Job not found")
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    # Call the new qa.py pipeline
    from qa import answer_question
    
    result = answer_question(job_id, request.question)
    
    return AskResponse(
        answer=result["answer"],
        citations=[Citation(**c) for c in result["citations"]]
    )
        
    # TODO: Wire to qa.py in Phase 2 (T-42.01)
    return {
        "answer": "Q&A pipeline is being wired in Phase 2. Stay tuned!",
        "citations": []
    }

# --- WebSocket Endpoint (Task T-41.03) ---

@router.websocket("/repos/{job_id}/stream")
async def stream_progress(websocket: WebSocket, job_id: str):
    """Live progress stream for the frontend analysis screen."""
    await websocket.accept()
    
    if job_id not in jobs_db:
        await websocket.send_json({"event": "error", "message": "Job not found"})
        await websocket.close()
        return

    try:
        # TODO: Import and run Sathwik's pipeline here in Phase 2
        # from graph import run_pipeline
        # async for event in run_pipeline(...):
        #     await websocket.send_json(event)
        
        # Mock stream for Phase 1 testing
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