import asyncio
import inspect
import traceback

import db
from ingest import clone_repo


async def run_job(job_id: str, repo_url: str, role: str):
    """
    Background worker (Phase 3).
    Clones the repo, runs Sathwik's LangGraph pipeline,
    and tracks live status in the DB for the WebSocket stream.
    """
    try:
        # Stage 1: Clone the repo
        db.update_repo_status(job_id, "cloning")
        repo_path = await asyncio.to_thread(clone_repo, repo_url, job_id)
        print(f"📦 Job {job_id}: cloned to {repo_path}")

        # Stage 2: Run the LangGraph pipeline (parse -> chunk -> embed -> synthesize)
        db.update_repo_status(job_id, "processing")
        from graph import run_pipeline

        result = run_pipeline(job_id, repo_url, role)

        # Handles async generator (yields events), coroutine, or normal function
        if inspect.isasyncgen(result):
            async for event in result:
                node = event.get("node") if isinstance(event, dict) else None
                if node:
                    db.update_repo_status(job_id, f"processing:{node}")
        elif inspect.iscoroutine(result):
            await result

        # Done!
        db.update_repo_status(job_id, "complete")
        print(f"✅ Job {job_id} completed successfully.")

    except Exception as e:
        print(f"❌ Job {job_id} failed: {e}")
        traceback.print_exc()
        db.update_repo_status(job_id, "failed", str(e)[:500])