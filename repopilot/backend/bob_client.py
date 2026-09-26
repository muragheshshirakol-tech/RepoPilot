"""backend/bob_client.py - C-01 v3 (REAL IBM Bob Shell, stdin-piped) | Dev 3: Muraghesh"""
import asyncio, json, logging, os, shutil, tempfile, time
from pathlib import Path
from typing import List, Optional, TypedDict

LOG_DIR = Path(tempfile.gettempdir()) / "bob_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [bob_client] %(message)s")
logger = logging.getLogger("bob_client")
BOB_TIMEOUT_SEC = 180

class AgentFinding(TypedDict):
    agent: str
    summary: str
    evidence: List[dict]
    confidence: float

def _bob_cmdline() -> str:
    bin_path = shutil.which("bob") or shutil.which("bob.cmd") or shutil.which("bob.exe") or "bob"
    # Quote the path: Windows usernames/paths often contain spaces
    if " " in bin_path or bin_path.lower().endswith((".cmd", ".bat")):
        return f'"{bin_path}"'
    return bin_path

def _balanced_json_objects(text: str) -> List[str]:
    out, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    out.append(text[start:i+1]); start = None
    return out

def _extract_finding_json(text: str) -> dict:
    picked = None
    for cand in _balanced_json_objects(text):
        try: obj = json.loads(cand)
        except json.JSONDecodeError:
            try: obj = json.loads(cand, strict=False)
            except json.JSONDecodeError: continue
        if isinstance(obj, dict) and ("summary" in obj or "evidence" in obj or "answer" in obj):
            picked = obj
    if picked is None:
        raise ValueError(f"No AgentFinding-shaped JSON in Bob output: {text[:300]}...")
    return picked

def _extract_plain_text(text: str) -> str:
    idx = text.rfind("Assistant")
    body = text[idx:] if idx != -1 else text
    for stop in ("Task Summary", "Total Cost"):
        j = body.find(stop)
        if j != -1: body = body[:j]
    lines = body.splitlines()
    if lines and lines[0].startswith("Assistant"): lines = lines[1:]
    return "\n".join(lines).strip() or text.strip()

async def call_bob(prompt: str, repo_path: Optional[str] = None,
                   timeout_sec: int = BOB_TIMEOUT_SEC) -> str:
    cmdline = _bob_cmdline()
    cwd = repo_path if (repo_path and os.path.isdir(repo_path)) else os.getcwd()
    logger.info("Bob call | cwd=%s | prompt_len=%d | cmd=%s", cwd, len(prompt), cmdline)
    t0 = time.time()
    # Shell-launch so the quoted path survives; prompt goes via STDIN (documented: cat prompt.txt | bob)
    proc = await asyncio.create_subprocess_shell(
        cmdline,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=prompt.encode("utf-8")), timeout=timeout_sec)
    except asyncio.TimeoutError:
        proc.kill(); raise TimeoutError(f"Bob CLI timed out after {timeout_sec}s")
    out = stdout.decode("utf-8", errors="replace")
    err = stderr.decode("utf-8", errors="replace")
    (LOG_DIR / f"bob_{int(t0)}.log").write_text(
        f"CMD: {cmdline}\nCWD: {cwd}\n--- PROMPT ---\n{prompt}\n--- STDOUT ---\n{out}\n--- STDERR ---\n{err}\n",
        encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"Bob CLI exit {proc.returncode}: {err[:500]}")
    logger.info("Bob call done in %.1fs", time.time() - t0)
    return out

async def call_bob_json(prompt: str, repo_path: Optional[str] = None) -> dict:
    raw = await call_bob(prompt, repo_path)
    try:
        return _extract_finding_json(raw)
    except ValueError:
        logger.warning("Malformed JSON from Bob; one repair retry.")
        repair = ("Your previous reply was not parseable as the required JSON object. "
                  "Reply with ONLY the JSON object, no prose, no markdown fences.\n\n"
                  "Original task:\n" + prompt)
        return _extract_finding_json(await call_bob(repair, repo_path))

def _to_finding(raw: dict, agent: str) -> AgentFinding:
    return AgentFinding(
        agent=agent,
        summary=str(raw.get("summary", "insufficient evidence")),
        evidence=[e for e in raw.get("evidence", []) if isinstance(e, dict)],
        confidence=float(raw.get("confidence", 0.5)),
    )

async def analyze_architecture(repo_path: str) -> AgentFinding:
    from prompts import ARCHITECTURE_PROMPT
    return _to_finding(await call_bob_json(ARCHITECTURE_PROMPT, repo_path), "architecture")

async def analyze_business_logic(repo_path: str) -> AgentFinding:
    from prompts import BUSINESS_LOGIC_PROMPT
    return _to_finding(await call_bob_json(BUSINESS_LOGIC_PROMPT, repo_path), "business_logic")

async def generate_narration(evidence: dict, repo_path: Optional[str] = None) -> str:
    prompt = ("You are narrating a code-tour step for a new developer.\n"
              f"Code evidence: {json.dumps(evidence)}\n"
              "Write EXACTLY two sentences explaining why this code matters.\n"
              "Output plain text only. No JSON. No markdown. No preamble.")
    return _extract_plain_text(await call_bob(prompt, repo_path))

if __name__ == "__main__":
    import sys
    async def _test():
        target = sys.argv[1] if len(sys.argv) > 1 else "."
        finding = await analyze_architecture(target)
        print(json.dumps(finding, indent=2))
    asyncio.run(_test())