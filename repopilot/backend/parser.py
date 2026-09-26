import os
from pathlib import Path
from typing import List, Dict, Any
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_typescript as tsts

# Initialize Tree-sitter languages
LANGUAGES = {
    ".py": Language(tspython.language()),
    ".ts": Language(tsts.language_typescript()),
    ".tsx": Language(tsts.language_typescript()),
    ".js": Language(tsts.language_typescript()),
}

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", "venv", ".venv"}

def parse_repo(repo_path: str) -> List[Dict[str, Any]]:
    results = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            ext = Path(f).suffix
            if ext not in LANGUAGES:
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_path)
            try:
                with open(full_path, "rb") as fh:
                    source = fh.read()
                parser = Parser(LANGUAGES[ext])
                tree = parser.parse(source)
                symbols = _extract_symbols(tree.root_node, source)
                if symbols:
                    results.append({
                        "path": rel_path,
                        "language": ext,
                        "symbols": symbols,
                    })
            except Exception as e:
                print(f"Parse error on {rel_path}: {e}")
                continue
    return results

def _extract_symbols(node, source: bytes, depth: int = 0) -> List[Dict[str, Any]]:
    symbols = []
    target_types = {
        "function_definition", "class_definition",
        "function_declaration", "method_definition",
        "arrow_function", "class_declaration",
        "import_statement", "import_from_statement",
        "export_statement"
    }
    if node.type in target_types:
        name_node = node.child_by_field_name("name")
        name = name_node.text.decode() if name_node else "anonymous"
        symbols.append({
            "name": name,
            "type": node.type,
            "start_line": node.start_point[0] + 1,
            "end_line": node.end_point[0] + 1,
            "content": source[node.start_byte:node.end_byte].decode(errors="replace"),
        })
    for child in node.children:
        symbols.extend(_extract_symbols(child, source, depth + 1))
    return symbols

if __name__ == "__main__":
    import tempfile
    import shutil
    print("Running Tree-sitter Parser Test...")
    temp_dir = tempfile.mkdtemp()
    try:
        py_file = os.path.join(temp_dir, "sample.py")
        with open(py_file, "w") as f:
            f.write("def hello_world():\n    print('Hello')\n\nclass MyClass:\n    pass\n")
        ts_file = os.path.join(temp_dir, "sample.ts")
        with open(ts_file, "w") as f:
            f.write("export function greet() {}\nimport { x } from 'y';\n")
        os.makedirs(os.path.join(temp_dir, "node_modules"))
        with open(os.path.join(temp_dir, "node_modules", "ignore.js"), "w") as f:
            f.write("function ignoreMe() {}")
        parsed_files = parse_repo(temp_dir)
        assert len(parsed_files) == 2, f"Expected 2 files, got {len(parsed_files)}"
        py_result = next((f for f in parsed_files if f["path"] == "sample.py"), None)
        ts_result = next((f for f in parsed_files if f["path"] == "sample.ts"), None)
        assert py_result is not None, "Failed to parse sample.py"
        assert len(py_result["symbols"]) >= 2, "Failed to extract Python symbols"
        assert ts_result is not None, "Failed to parse sample.ts"
        assert len(ts_result["symbols"]) >= 2, "Failed to extract TypeScript symbols"
        print("✅ SUCCESS: Tree-sitter parser is working correctly!")
        print(f"Found {len(parsed_files)} files with symbols.")
        for pf in parsed_files:
            print(f"  - {pf['path']} ({pf['language']}): {len(pf['symbols'])} symbols")
    finally:
        shutil.rmtree(temp_dir)