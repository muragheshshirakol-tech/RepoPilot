import os
import json
from typing import List, Dict, Any

# Import Sathwik's new functions
from embedder import get_embedding
from hybrid_search import hybrid_search
import db

async def answer_question(job_id: str, question: str) -> Dict[str, Any]:
    """
    Main Q&A pipeline using Dev 5's hybrid search.
    """
    try:
        # 1. Embed the user's question (1536-dim vector)
        q_embedding = get_embedding(question)
        
        # 2. Run hybrid search (Vector + Keyword + Bob Rerank)
        chunks = await hybrid_search(job_id, question, q_embedding, top_k=5)
        
        if not chunks:
            return {
                "answer": "I don't have enough information about this repository yet. Please wait for the analysis to complete.",
                "citations": []
            }
        
        # 3. Format as a single string for the Bob prompt
        context_str = "\n\n---\n\n".join([
            f"File: {c['path']} (Lines {c['start_line']}-{c['end_line']})\n{c['content']}" 
            for c in chunks
        ])
        
        # 4. Extract citations for the frontend
        citations = [{"path": c["path"], "start": c["start_line"], "end": c["end_line"]} for c in chunks]
        
        # 5. Call Bob using the QA_PROMPT (Owned by Muraghesh/Dev 3)
        try:
            from bob_client import call_bob
            from prompts import QA_PROMPT
            
            final_prompt = QA_PROMPT.replace("{question}", question).replace("{context}", context_str)
            
            # Note: Adjust 'await' here if Muraghesh's call_bob is synchronous
            bob_response = await call_bob(final_prompt, repo_path=None) 
            
            # Parse Bob's JSON response
            if isinstance(bob_response, str):
                bob_response = json.loads(bob_response)
                
            return {
                "answer": bob_response.get("answer", "No answer provided."),
                # Use Bob's citations if available, otherwise fall back to search citations
                "citations": bob_response.get("citations", citations) 
            }
            
        except ImportError:
            # Fallback if Muraghesh hasn't pushed prompts.py/bob_client.py yet
            return {
                "answer": f"Based on the retrieved code, the answer to '{question}' is found in the context. (Bob integration pending).",
                "citations": citations
            }
        except Exception as e:
            return {
                "answer": f"Q&A pipeline error: {str(e)}",
                "citations": citations
            }
            
    except Exception as e:
        return {"answer": f"Embedding or search service error: {str(e)}", "citations": []}