import os
import time
from typing import List, Dict, Any

# --- MOCK EMBEDDER (Replace with real OpenAI/Bob call when API key is ready) ---
def get_embedding(text: str) -> List[float]:
    """
    HACKATHON MOCK: Returns a dummy 1536-dim vector.
    To use real OpenAI:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    res = client.embeddings.create(input=text, model="text-embedding-3-small")
    return res.data[0].embedding
    """
    return [0.1] * 1536 

# --- MOCK DB SAVE (Uncomment when Dev 4's db.py is ready) ---
# from db import save_chunk

def embed_chunks(job_id: str, chunks: List[Dict[str, Any]], batch_size: int = 100) -> None:
    """
    Embeds chunks in batches and saves them to the database.
    - Batches in groups of 100
    - Handles rate limits with retry/backoff
    - Logs progress every 100 chunks
    """
    print(f"🚀 Starting embedding pipeline for job {job_id} ({len(chunks)} chunks)...")
    
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        print(f"  ⏳ Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
        
        for chunk in batch:
            retries = 3
            while retries > 0:
                try:
                    # 1. Get embedding
                    embedding = get_embedding(chunk["content"])
                    
                    # 2. Save to DB (Mocked for now)
                    # save_chunk(
                    #     repo_id=job_id, 
                    #     path=chunk["path"], 
                    #     start=chunk["start_line"], 
                    #     end=chunk["end_line"], 
                    #     content=chunk["content"], 
                    #     embedding=embedding
                    # )
                    
                    # Mock success log
                    print(f"    ✅ Saved: {chunk['path']} ({chunk['start_line']}-{chunk['end_line']})")
                    break
                    
                except Exception as e:
                    retries -= 1
                    print(f"    ⚠️ Failed to embed {chunk['path']}. Retries left: {retries}. Error: {e}")
                    if retries == 0:
                        print(f"    ❌ Permanently failed: {chunk['path']}")
                    else:
                        time.sleep(2)
                        
        print(f"  ✅ Batch {batch_num} complete.")
        
    print(f"\n🎉 Embedding pipeline completed for job {job_id}!")

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    print("🚀 Testing Embedding Pipeline...\n")
    
    mock_chunks = [
        {"path": "src/main.py", "start_line": 1, "end_line": 10, "content": "def main(): pass", "chunk_type": "function_definition"},
        {"path": "src/utils.py", "start_line": 15, "end_line": 25, "content": "def helper(): pass", "chunk_type": "function_definition"},
    ]
    
    embed_chunks(job_id="test-job-123", chunks=mock_chunks, batch_size=2)
    print("\n🎉 Embedder Test Passed!")