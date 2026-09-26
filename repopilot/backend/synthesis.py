import asyncio
from typing import List, Dict, Any

# Mock Bob call for narration (Dev 3 will replace this with real bob_client.generate_narration)
async def mock_bob_narration(evidence: Dict[str, Any]) -> str:
    await asyncio.sleep(0.5) # Simulate API call
    return f"This step highlights {evidence.get('path', 'a key file')}, which is critical for understanding the system's {evidence.get('note', 'core logic')}."

async def build_plan(findings: List[Dict[str, Any]], role: str) -> Dict[str, Any]:
    """
    Merges AgentFinding objects into a valid OnboardingPlan.
    """
    architecture_summary = "Architecture summary pending."
    key_concepts = ["Concept 1", "Concept 2"]
    all_evidence = []

    # 1. Extract data from findings
    for finding in findings:
        if finding.get("agent") == "architecture":
            architecture_summary = finding.get("summary", architecture_summary)
            all_evidence.extend(finding.get("evidence", []))
        elif finding.get("agent") == "business_logic":
            # Extract concepts from summary or evidence notes
            concepts = [ev.get("note", "Unknown concept") for ev in finding.get("evidence", [])]
            key_concepts = list(set(concepts))[:5] # Keep top 5 unique concepts
            all_evidence.extend(finding.get("evidence", []))

    # 2. Generate 8 tour steps
    tour_steps = []
    
    # Rank evidence (mock ranking: just take the first 8, or pad if < 8)
    top_evidence = all_evidence[:8]
    
    for i, ev in enumerate(top_evidence, start=1):
        narration = await mock_bob_narration(ev)
        tour_steps.append({
            "step": i,
            "title": f"Step {i}: {ev.get('path', 'Unknown File').split('/')[-1]}",
            "path": ev.get("path", "README.md"),
            "start": ev.get("start", 1),
            "end": ev.get("end", 10),
            "narration": narration
        })

    # 3. Pad with README steps if we have fewer than 8
    while len(tour_steps) < 8:
        step_num = len(tour_steps) + 1
        tour_steps.append({
            "step": step_num,
            "title": f"Step {step_num}: Project Overview",
            "path": "README.md",
            "start": 1,
            "end": 20,
            "narration": "Review the README.md to understand the project's high-level goals and setup instructions."
        })

    # 4. Construct final plan
    plan = {
        "role": role,
        "architecture_summary": architecture_summary,
        "key_concepts": key_concepts,
        "tour_steps": tour_steps[:8] # Ensure exactly 8 steps
    }

    return plan

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    async def test_synthesis():
        print("🚀 Testing Synthesis Agent...\n")
        
        mock_findings = [
            {
                "agent": "architecture",
                "summary": "This is a modular HTTP client with interceptors and retry logic.",
                "evidence": [
                    {"path": "source/index.ts", "start": 10, "end": 50, "note": "main entry point"},
                    {"path": "source/core/Ky.ts", "start": 100, "end": 200, "note": "core request handling"}
                ],
                "confidence": 0.95
            },
            {
                "agent": "business_logic",
                "summary": "Handles automatic retries and timeout management.",
                "evidence": [
                    {"path": "source/core/retry.ts", "start": 15, "end": 45, "note": "retry mechanism"},
                    {"path": "source/errors/TimeoutError.ts", "start": 5, "end": 15, "note": "error handling"}
                ],
                "confidence": 0.85
            }
        ]
        
        plan = await build_plan(mock_findings, "Backend")
        
        print("✅ Synthesis Successful!")
        print(f"Role: {plan['role']}")
        print(f"Architecture Summary: {plan['architecture_summary'][:50]}...")
        print(f"Key Concepts: {plan['key_concepts']}")
        print(f"Tour Steps Generated: {len(plan['tour_steps'])}")
        
        # Verify exactly 8 steps
        assert len(plan['tour_steps']) == 8, "Must have exactly 8 tour steps!"
        print("\n🎉 Synthesis Agent Test Passed!")

    asyncio.run(test_synthesis())