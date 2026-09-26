import asyncio
from typing import List, Dict, Any

# --- MOCK DATABASE CALL (Replace with Prajwal's real db.py call later) ---
async def mock_search_chunks_db(job_id: str, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
    """
    MOCK: Simulates the pgvector cosine similarity search.
    Real implementation will use: 
    SELECT path, start_line, end_line, content, 1 - (embedding <=> %s) AS similarity 
    FROM code_chunks WHERE repo_id = %s ORDER BY similarity DESC LIMIT %s
    """
    await asyncio.sleep(0.2) # Simulate DB latency
    return [
        {"path": "src/core/Ky.ts", "start_line": 100, "end_line": 200, "content": "class Ky { ... }", "similarity": 0.85},
        {"path": "src/core/retry.ts", "start_line": 15, "end_line": 45, "content": "async function retry() { ... }", "similarity": 0.72},
        {"path": "src/errors/TimeoutError.ts", "start_line": 5, "end_line": 15, "content": "class TimeoutError extends Error { ... }", "similarity": 0.65},
        {"path": "src/utils.ts", "start_line": 10, "end_line": 30, "content": "function normalizeUrl() { ... }", "similarity": 0.45},
        {"path": "README.md", "start_line": 1, "end_line": 20, "content": "# Ky: Tiny and elegant HTTP client", "similarity": 0.35},
        {"path": "src/irrelevant.ts", "start_line": 1, "end_line": 10, "content": "function ignoreMe() { ... }", "similarity": 0.15}, # Below threshold
    ][:top_k]

# --- MOCK BOB RERANK (Replace with real bob_client call later) ---
async def mock_bob_rerank(query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    MOCK: Simulates Bob re-ranking the top 10 chunks by relevance.
    """
    await asyncio.sleep(0.5) # Simulate Bob API latency
    # Mock logic: return chunks with similarity > 0.3, sorted by similarity, max 5
    relevant_chunks = [c for c in chunks if c.get("similarity", 0.0) > 0.3]
    relevant_chunks.sort(key=lambda x: x["similarity"], reverse=True)
    return relevant_chunks[:5]

# ==========================================
# CORE FUNCTIONS
# ==========================================

async def search_chunks(job_id: str, query_embedding: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Queries the database for chunks similar to the query embedding.
    Filters by similarity > 0.3 threshold.
    """
    raw_results = await mock_search_chunks_db(job_id, query_embedding, top_k)
    filtered_results = [r for r in raw_results if r.get("similarity", 0.0) > 0.3]
    return filtered_results

async def rerank(query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Uses Bob to re-rank the retrieved chunks by relevance, returning the top 5.
    """
    if not chunks:
        return []
    reranked_results = await mock_bob_rerank(query, chunks)
    return reranked_results

async def hybrid_search(job_id: str, query: str, query_embedding: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Optional (T-53.01): Combines vector search and reranking into a single pipeline.
    """
    vector_results = await search_chunks(job_id, query_embedding, top_k=10)
    final_results = await rerank(query, vector_results)
    return final_results

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    async def test_search():
        print("🚀 Testing Vector Search + Rerank...\n")
        
        job_id = "test-job-123"
        mock_embedding = [0.1] * 1536 
        query = "How does the retry mechanism work?"
        
        print("1. Running vector search...")
        chunks = await search_chunks(job_id, mock_embedding, top_k=10)
        print(f"   ✅ Found {len(chunks)} chunks above 0.3 similarity threshold.")
        for c in chunks:
            print(f"      - {c['path']} (similarity: {c['similarity']:.2f})")
            
        print("\n2. Running Bob rerank...")
        top_chunks = await rerank(query, chunks)
        print(f"   ✅ Reranked to top {len(top_chunks)} most relevant chunks.")
        for i, c in enumerate(top_chunks, 1):
            print(f"      {i}. {c['path']} (similarity: {c['similarity']:.2f})")
            
        assert len(chunks) == 5, "Should have filtered out the 0.15 similarity chunk"
        assert len(top_chunks) <= 5, "Rerank should return max 5 chunks"
        
        print("\n🎉 Vector Search + Rerank Test Passed!")

    asyncio.run(test_search())