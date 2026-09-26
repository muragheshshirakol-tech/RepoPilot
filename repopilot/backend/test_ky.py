import os
import subprocess
import sys
from parser import parse_repo

def test_ky_repo():
    repo_url = "https://github.com/sindresorhus/ky.git"
    test_dir = "test_ky_repo"

    print(f"1. Cloning {repo_url} into {test_dir}...")
    subprocess.run(["git", "clone", "--depth", "1", repo_url, test_dir], check=True)

    print("2. Running Tree-sitter parser on ky...")
    try:
        parsed_files = parse_repo(test_dir)

        print(f"\n✅ SUCCESS: Parsed {len(parsed_files)} files with symbols.")

        for pf in parsed_files[:5]:
            print(f"  - {pf['path']} ({pf['language']}): {len(pf['symbols'])} symbols")
            for sym in pf['symbols'][:2]:
                print(f"      * {sym['type']}: {sym['name']} (lines {sym['start_line']}-{sym['end_line']})")

        with open("ky_parser_evidence.txt", "w", encoding="utf-8") as f:
            f.write(f"Successfully parsed {len(parsed_files)} files.\n")
            for pf in parsed_files:
                f.write(f"File: {pf['path']}, Symbols: {len(pf['symbols'])}\n")
        print("\n3. Evidence saved to backend/ky_parser_evidence.txt")

    except Exception as e:
        print(f"❌ FAILED: {e}")
    finally:
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print("4. Cleaned up test directory.")

if __name__ == "__main__":
    if not subprocess.run(["git", "--version"], capture_output=True).returncode == 0:
        print("❌ ERROR: Git is not installed or not in PATH.")
        sys.exit(1)
    test_ky_repo()