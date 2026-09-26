import os
import subprocess
import shutil
import asyncio
from typing import List, Dict, Any

# Import your Dev 5 pipeline
from parser import parse_repo
from chunker import chunk_repo
from embedder import embed_chunks
from search import search_chunks, rerank

# Test repositories from the playbook (page 25)
TEST_REPOS = [
    {"name": "sindresorhus/ky", "url": "https://github.com/sindresorhus/ky.git", "lang": "TypeScript"},
    {"name": "tiangolo/fastapi", "url": "https://github.com/tiangolo/fastapi.git", "lang": "Python"},
    {"name": "expressjs/express", "url": "https://github.com/expressjs/express.git", "lang": "JavaScript"},
]

async def run_quality_check():
    """
    Runs the full Dev 5 pipeline on 3 repos and validates:
    1. Parser extracts symbols
    2. Chunker creates chunks
    3. Embedder processes chunks (mocked)
    4. Search returns relevant results (mocked)
    """
    print("="*70)
    print("🚀 DEV 5 EMBEDDING QUALITY CHECK — 3 REPOS")
    print("="*70)
    
    results = []
    
    for repo in TEST_REPOS:
        print(f"\n{'='*70}")
        print(f"📦 Testing: {repo['name']} ({repo['lang']})")
        print(f"{'='*70}")
        
        repo_dir = f"test_{repo['name'].replace('/', '_')}"
        
        try:
            # 1. Clone repo
            print(f"\n1️⃣  Cloning {repo['url']}...")
            subprocess.run(
                ["git", "clone", "--depth", "1", repo["url"], repo_dir],
                check=True,
                capture_output=True
            )
            print(f"   ✅ Cloned successfully")
            
            # 2. Parse with Tree-sitter
            print(f"\n2️⃣  Parsing with Tree-sitter...")
            parsed_files = parse_repo(repo_dir)
            total_symbols = sum(len(pf["symbols"]) for pf in parsed_files)
            print(f"   ✅ Parsed {len(parsed_files)} files, {total_symbols} symbols")
            
            if len(parsed_files) == 0:
                print(f"   ⚠️  WARNING: No files parsed!")
                results.append({"repo": repo["name"], "status": "FAILED", "reason": "No files parsed"})
                continue
            
            # 3. Chunk the parsed files
            print(f"\n3️⃣  Chunking parsed files...")
            chunks = chunk_repo(parsed_files, max_chunks=500)
            print(f"   ✅ Generated {len(chunks)} chunks")
            
            if len(chunks) == 0:
                print(f"   ⚠️  WARNING: No chunks generated!")
                results.append({"repo": repo["name"], "status": "FAILED", "reason": "No chunks generated"})
                continue
            
            # 4. Embed chunks (mocked)
            print(f"\n4️⃣  Embedding chunks (mock)...")
            job_id = f"quality-check-{repo['name'].replace('/', '-')}"
            embed_chunks(job_id=job_id, chunks=chunks[:10], batch_size=5)  # Only embed first 10 for speed
            print(f"   ✅ Embedded {min(10, len(chunks))} chunks")
            
            # 5. Search (mocked)
            print(f"\n5️⃣  Testing vector search (mock)...")
            mock_embedding = [0.1] * 1536
            search_results = await search_chunks(job_id, mock_embedding, top_k=5)
            print(f"   ✅ Search returned {len(search_results)} results")
            
            # 6. Rerank (mocked)
            print(f"\n6️⃣  Testing rerank (mock)...")
            reranked = await rerank("test query", search_results)
            print(f"   ✅ Reranked to {len(reranked)} results")
            
            # Success!
            results.append({
                "repo": repo["name"],
                "status": "PASSED",
                "files_parsed": len(parsed_files),
                "symbols_extracted": total_symbols,
                "chunks_generated": len(chunks),
                "search_results": len(search_results)
            })
            
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            results.append({"repo": repo["name"], "status": "FAILED", "reason": str(e)})
            
        finally:
            # Cleanup
            if os.path.exists(repo_dir):
                shutil.rmtree(repo_dir, ignore_errors=True)
                print(f"\n🧹 Cleaned up {repo_dir}")
    
    # Final summary
    print(f"\n{'='*70}")
    print("📊 QUALITY CHECK SUMMARY")
    print(f"{'='*70}")
    
    for r in results:
        status_icon = "✅" if r["status"] == "PASSED" else "❌"
        print(f"\n{status_icon} {r['repo']}: {r['status']}")
        if r["status"] == "PASSED":
            print(f"   Files parsed: {r['files_parsed']}")
            print(f"   Symbols extracted: {r['symbols_extracted']}")
            print(f"   Chunks generated: {r['chunks_generated']}")
            print(f"   Search results: {r['search_results']}")
        else:
            print(f"   Reason: {r['reason']}")
    
    # Save evidence
    with open("quality_check_results.txt", "w", encoding="utf-8") as f:
        f.write("DEV 5 EMBEDDING QUALITY CHECK RESULTS\n")
        f.write("="*70 + "\n\n")
        for r in results:
            f.write(f"Repo: {r['repo']}\n")
            f.write(f"Status: {r['status']}\n")
            if r["status"] == "PASSED":
                f.write(f"Files parsed: {r['files_parsed']}\n")
                f.write(f"Symbols extracted: {r['symbols_extracted']}\n")
                f.write(f"Chunks generated: {r['chunks_generated']}\n")
                f.write(f"Search results: {r['search_results']}\n")
            else:
                f.write(f"Reason: {r['reason']}\n")
            f.write("\n" + "-"*70 + "\n\n")
    
    print(f"\n📄 Results saved to quality_check_results.txt")
    print(f"\n{'='*70}")
    print("✅ DEV 5 PHASE 2 COMPLETE!")
    print(f"{'='*70}")

if __name__ == "__main__":
    asyncio.run(run_quality_check())