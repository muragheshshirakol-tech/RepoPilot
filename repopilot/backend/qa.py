import os
import json
from typing import List, Dict, Any

import db
from embedder import get_embedding
from hybrid_search import hybrid_search

async def get_context_for_qa(job_id: str, question: str):
    """Satwik's helper: Embeds question and runs hybrid search."""
    # 1. Embed the user's question (1536-dim vector)
    q_embedding = get_embedding(question)
    
    # 2. Run hybrid search (Vector + Keyword + Bob Rerank)
    chunks = await hybrid_search(job_id, question, q_embedding, top_k=5)
    
    if not chunks:
        return "No relevant code found in the repository.", []
    
    # 3. Format as a single string for the Bob prompt
    context_str = "\n\n---\n\n".join([
        f"File: {c['path']} (Lines {c['start_line']}-{c['end_line']})\n{c['content']}" 
        for c in chunks
    ])
    
    # 4. Extract citations for the frontend
    citations = [{"path": c["path"], "start": c["start_line"], "end": c["end_line"]} for c in chunks]
    
    return context_str, citations

async def answer_question(job_id: str, question: str) -> Dict[str, Any]:
    """Main Q&A pipeline using Satwik's context helper and Bob."""
    try:
        # Step 1: Get context and citations
        context_str, citations = await get_context_for_qa(job_id, question)
        
        if context_str == "No relevant code found in the repository.":
            return {
                "answer": "I don't have enough information about this repository yet. Please wait for the analysis to complete.",
                "citations": []
            }
        
        # Step 2: Build the Bob prompt
        try:
            from prompts import QA_PROMPT
        except ImportError:
            # Fallback prompt if Muraghesh hasn't pushed prompts.py yet
            QA_PROMPT = "Answer the user question based ONLY on the retrieved code context. Provide the answer and citations in JSON format."
        
        bob_prompt = f"""
{QA_PROMPT}

User Question: {question}

Retrieved Code Context:
{context_str}

Please provide an answer based ONLY on the code context above.
"""
        
        # Step 3: Call Bob to generate the answer
        try:
            from bob_client import call_bob
            
            bob_response = await call_bob(bob_prompt, repo_path=f"/tmp/repopilot/{job_id}")
            
            # Parse Bob's response
            if isinstance(bob_response, str):
                try:
                    parsed = json.loads(bob_response)
                    answer = parsed.get("answer", "I couldn't generate an answer.")
                    bob_citations = parsed.get("citations", [])
                except json.JSONDecodeError:
                    # Bob returned plain text instead of JSON
                    answer = bob_response
                    bob_citations = citations  # Fall back to retrieval citations
            else:
                # Bob returned a dict directly
                answer = bob_response.get("answer", "I couldn't generate an answer.")
                bob_citations = bob_response.get("citations", citations)
            
            return {
                "answer": answer,
                "citations": bob_citations if bob_citations else citations
            }
            
        except ImportError:
            # Fallback if bob_client is not ready yet
            return {
                "answer": f"Based on the retrieved code, here is the context for your question. (Bob integration pending).",
                "citations": citations
            }
        except Exception as bob_error:
            # Bob failed - return a fallback answer with retrieval citations
            print(f"Bob call failed: {bob_error}")
            return {
                "answer": "I found some relevant code, but I'm having trouble generating an answer right now. Please try again in a moment.",
                "citations": citations
            }
            
    except Exception as e:
        # Unexpected error
        print(f"Q&A pipeline error: {e}")
        return {
            "answer": "An error occurred while processing your question. Please try again.",
            "citations": []
        }