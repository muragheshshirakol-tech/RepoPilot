# Bob Task Session Screenshots

**This folder is a required submission artifact.**
Every Bob interaction used to build RepoPilot must be captured here
as a PNG screenshot of the task session consumption summary.

---

## Why This Folder Exists

The IBM Bob 2.0 Hackathon Guide states:

> Participants are required to upload all relevant Bob IDE task
> session summary screenshots to their code repository as evidence
> of Bob usage.

Missing screenshots = ineligible for judging. **Do not skip this.**

---

## How to Capture a Screenshot

1. Open **Bob IDE**.
2. Click the **Tasks** icon in the top-right of the chat panel.
3. Select the task related to your work.
4. Click the **task header** — the summary panel opens.
5. Confirm the summary shows: Context Length, Task ID, Workspace,
   Tokens, Cache, API Cost.
6. Screenshot the whole summary panel.
7. Save as PNG.

---

## Naming Convention

```
team_taskNN_short_description.png
```

- `team` — your team name (lowercase, no spaces, no hyphens)
- `taskNN` — 2-digit task number (01, 02, ..., 25)
- `short_description` — 2–4 words, snake_case

### Correct examples

```
team_task01_bob_setup_verify.png
team_task02_first_call.png
team_task03_architecture_agent.png
team_task04_subagent_test.png
team_task05_custom_rules_test.png
team_task06_mcp_settings.png
team_task12_qa_prompt_refine.png
```

### Incorrect examples

```
Screenshot 2026-09-25.png     ← no context
bob.png                        ← no task number
test.PNG                       ← wrong extension case
task1_final_FINAL_v2.png       ← no team prefix
```

---

## Format Rules

- **PNG preferred.** Better text clarity than JPG.
- Full summary panel visible, not just the task name.
- No cropping that removes Task ID or Cost.
- If a session is very long, take multiple screenshots and number
  them: `team_task12_part1.png`, `team_task12_part2.png`.

---

## When to Capture

- **Every time** Bob produces code used in the repo.
- **Every time** Bob is used for prompt refinement.
- **Every time** Bob is used for analysis.
- **Every time** Bob solves a real problem, even partially.

At the end of the build we should have **at least 15 screenshots**.
If we have fewer, we are missing evidence.

---

## Verification Before Submission

Run this from the repo root:

```bash
ls bob_sessions/*.png | wc -l
```

Must output **15 or more**.

Then verify each file follows the naming convention:

```bash
ls bob_sessions/ | grep -v "^team_task[0-9][0-9]_.*\.png$" | grep -v README
```

If this prints anything, rename that file to match the convention.
