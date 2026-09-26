import asyncio
from typing import List, Dict, Any
from search import search_chunks, rerank

# --- MOCK KEYWORD SEARCH (Replace with real Postgres full-text search later) ---
async def mock_keyword_search(job_id: str, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
    """
    MOCK: Simulates Postgres full-text search (tsvector) or BM25.
    Real implementation: SELECT ... WHERE to_tsvector(content) @@ to_tsquery('query')
    """
    await asyncio.sleep(0.2)
    # Mocking exact keyword matches
    query_lower = query.lower()
    mock_db = [
        {"path": "src/errors/TimeoutError.ts", "content": "class TimeoutError extends Error {}", "score": 0.95},
        {"path": "src/core/retry.ts", "content": "async function retry() { throw new TimeoutError() }", "score": 0.80},
        {"path": "README.md", "content": "Ky handles timeouts gracefully.", "score": 0.40},
    ]
    
    # Simple keyword matching for the mock
    results = []
    for doc in mock_db:
        if any(word in doc["content"].lower() for word in query_lower.split()):
            results.append({
                "path": doc["path"],
                "start_line": 1,
                "end_line": 10,
                "content": doc["content"],
                "similarity": doc["score"],
                "source": "keyword"
            })
    return results[:top_k]

# ==========================================
# CORE HYBRID FUNCTION
# ==========================================

async def hybrid_search(job_id: str, query: str, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Combines Vector Search (semantic) and Keyword Search (exact match),
    then uses Bob to rerank the combined pool for maximum accuracy.
    """
    print(f"🔍 Running Hybrid Search for: '{query}'")
    
    # 1. Run Vector and Keyword searches in parallel
    vector_task = search_chunks(job_id, query_embedding, top_k=15)
    keyword_task = mock_keyword_search(job_id, query, top_k=15)
    
    vector_results, keyword_results = await asyncio.gather(vector_task, keyword_task)
    
    # Tag sources for debugging
    for r in vector_results: r["source"] = "vector"
    for r in keyword_results: r["source"] = "keyword"
    
    # 2. Merge and Deduplicate (by path + start_line)
    combined_pool = {}
    for r in vector_results + keyword_results:
        key = f"{r['path']}_{r['start_line']}"
        if key not in combined_pool:
            combined_pool[key] = r
        else:
            # If found in both, boost its similarity score slightly
            combined_pool[key]["similarity"] = min(1.0, combined_pool[key]["similarity"] + 0.1)
            combined_pool[key]["source"] = "hybrid"
            
    merged_results = list(combined_pool.values())
    print(f"   📊 Merged pool: {len(merged_results)} unique chunks.")
    
    # 3. Rerank with Bob to get the absolute best Top K
    final_results = await rerank(query, merged_results)
    
    return final_results[:top_k]

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    async def test_hybrid():
        print("🚀 Testing Hybrid Search (Phase 3)...\n")
        
        job_id = "test-job-123"
        mock_embedding = [0.1] * 1536 
        query = "How does the TimeoutError work?"
        
        results = await hybrid_search(job_id, query, mock_embedding, top_k=5)
        
        print(f"\n✅ Hybrid Search returned {len(results)} highly relevant chunks:")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [{r.get('source', 'unknown').upper()}] {r['path']} (score: {r['similarity']:.2f})")
            
        print("\n🎉 Hybrid Search Test Passed! Ready for Q&A integration.")

    asyncio.run(test_hybrid())