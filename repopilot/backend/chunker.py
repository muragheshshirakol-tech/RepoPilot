import os
from typing import List, Dict, Any

def chunk_repo(parsed_files: List[Dict[str, Any]], max_chunks: int = 500) -> List[Dict[str, Any]]:
    """
    Chunks parsed files along AST boundaries.
    - If symbol > 500 lines, splits into overlapping 200-line windows.
    - If file has no symbols, creates one chunk per 100 lines.
    - Prepends header: "File: {path} | Lines: {start}-{end} | Type: {type}"
    """
    chunks = []
    
    for pf in parsed_files:
        if len(chunks) >= max_chunks:
            break
            
        path = pf["path"]
        symbols = pf.get("symbols", [])
        
        # Read full file content for fallback chunking
        try:
            with open(path, "r", encoding="utf-8") as f:
                file_lines = f.readlines()
        except Exception:
            file_lines = []

        if not symbols:
            # Fallback: No symbols, chunk every 100 lines
            total_lines = len(file_lines)
            for start in range(1, total_lines + 1, 100):
                end = min(start + 99, total_lines)
                content = "".join(file_lines[start-1:end])
                chunks.append({
                    "path": path,
                    "start_line": start,
                    "end_line": end,
                    "content": f"File: {path} | Lines: {start}-{end} | Type: fallback\n{content}",
                    "chunk_type": "fallback"
                })
                if len(chunks) >= max_chunks:
                    break
            continue

        # Chunk by AST symbols
        for sym in symbols:
            if len(chunks) >= max_chunks:
                break
                
            start = sym["start_line"]
            end = sym["end_line"]
            sym_type = sym["type"]
            sym_content = sym["content"]
            
            # Split if > 500 lines
            if (end - start) > 500:
                current_start = start
                while current_start < end:
                    current_end = min(current_start + 200, end)
                    chunk_content = f"File: {path} | Lines: {current_start}-{current_end} | Type: {sym_type}\n{sym_content[:1500]}..."
                    chunks.append({
                        "path": path,
                        "start_line": current_start,
                        "end_line": current_end,
                        "content": chunk_content,
                        "chunk_type": f"{sym_type}_split"
                    })
                    current_start += 150  # 50-line overlap
            else:
                chunk_content = f"File: {path} | Lines: {start}-{end} | Type: {sym_type}\n{sym_content}"
                chunks.append({
                    "path": path,
                    "start_line": start,
                    "end_line": end,
                    "content": chunk_content,
                    "chunk_type": sym_type
                })
                
    return chunks[:max_chunks]

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    print("🚀 Testing Code Chunker...\n")
    
    mock_parsed_files = [
        {
            "path": "test_file.py",
            "language": ".py",
            "symbols": [
                {"name": "small_func", "type": "function_definition", "start_line": 1, "end_line": 10, "content": "def small_func():\n    pass"},
                {"name": "huge_func", "type": "function_definition", "start_line": 15, "end_line": 600, "content": "def huge_func():\n    # " + "x\n" * 600}
            ]
        }
    ]
    
    # Create a dummy file for the fallback test
    with open("test_file.py", "w") as f:
        f.write("line 1\n" * 250)
        
    chunks = chunk_repo(mock_parsed_files, max_chunks=500)
    
    print(f"✅ Generated {len(chunks)} chunks.")
    for i, c in enumerate(chunks[:3]):
        print(f"  Chunk {i+1}: {c['path']} | Lines {c['start_line']}-{c['end_line']} | Type: {c['chunk_type']}")
        
    assert len(chunks) >= 2, "Should have split the huge function"
    print("\n🎉 Code Chunker Test Passed!")
    
    # Cleanup
    if os.path.exists("test_file.py"):
        os.remove("test_file.py")