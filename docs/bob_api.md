# IBM Bob 2.0 — Integration Notes

**Last updated:** [Fill in during hour 0]
**Author:** Dev 3 (IBM Bob Lead)

---

## Critical Discovery

**Bob is not a REST API.** There is no `BOB_API_KEY`, no
`POST /agent/run`, no hosted endpoint.

Bob is delivered as:

1. **Bob IDE** (required) — VS Code-style desktop app
2. **Bob Shell** (optional, but we use it) — a CLI with
   non-interactive mode for automation

---

## Bob IDE

- Download from the hackathon portal.
- **Requires v2.0.2 or later** — v1.0.3 and v2.0.0 stop working
  on September 30, 2026.
- Log in with your hackathon registration email.
- **Must switch to the hackathon instance:**
  Settings → General → Team = `ibm-coding-challenge-uat` (region: us-east).
- 40 Bobcoins allocated per participant.

### Features We Rely On

| Feature | Purpose |
|---------|---------|
| **Agent Mode** | Autonomous multi-step coding |
| **Subagents** | Parallel focused tasks |
| **Custom modes** | "RepoPilot Onboarding" persona |
| **Custom rules** | `.bob/rules/onboarding.md` |
| **Skills** | Reusable workflow instructions |
| **MCP servers** | External tool integration (optional) |
| **`.bobignore`** | File exclusion |

---

## Bob Shell

Bob Shell brings the same capabilities to the command line.

### Install

Follow the hackathon portal's Bob Shell installation instructions.

**Note:** Bob Shell 2.0.0 requires a fresh install. There is no
automated upgrade path from 1.0.x.

### Authenticate

```bash
bob.ibm.com/login
```

Same credentials as Bob IDE.

### Interactive Session

```bash
bob
```

Drops you into a chat-style shell.

### Non-Interactive Session (what our backend uses)

```bash
bob --non-interactive \
    --prompt "Explain what this file does" \
    --workspace /path/to/repo
```

Prints the result to stdout. Returns exit code 0 on success.

### Verification (run this on hour 0)

```bash
# 1. Bob Shell is installed
bob --help

# 2. Non-interactive works
bob --non-interactive --prompt "Say hello in JSON: {\"ok\": true}"

# 3. Workspace flag works
cd /tmp && git clone --depth 1 https://github.com/sindresorhus/ky
bob --non-interactive --prompt "List the top-level files" --workspace /tmp/ky
```

If all three succeed, our backend integration is possible.

---

## Bobcoin Budget

**Total team budget: 240 Bobcoins (40 × 6).**

| Phase | Coins | Who | Notes |
|-------|-------|-----|-------|
| Setup verification (hours 0–2) | 20 | Dev 3 | Prove Bob works |
| Prompt engineering (hours 6–18) | 60 | Dev 3 | Refine prompts |
| Code generation via Bob IDE | 80 | All 6 | Split across team |
| Live demo runs (hours 36–42) | 40 | Dev 1+6 | Video takes |
| Buffer | 40 | — | Unexpected retries |
| **Total** | **240** | | |

### Rules

1. Only Dev 3 and Dev 1 use Bob for expensive multi-step reasoning.
2. Test prompts in Claude/GPT first. Run through Bob once.
3. Screenshot every Bob session.
4. Track coins hourly (Settings → General → Budget).
5. If 50% used by hour 24, cut non-essential Bob calls.

---

## Task Session Screenshots

**Required for submission.** See `bob_sessions/README.md`.

### How to capture

1. Bob IDE → Tasks panel.
2. Click the task header.
3. Screenshot the summary.
4. Save as `bob_sessions/team_taskNN_desc.png`.

The summary shows: Context Length, Task ID, Workspace, Tokens, Cache,
API Cost.

---

## MCP Integration (Optional)

Bob supports Model Context Protocol for connecting external tools.

We may use MCP to expose RepoPilot's own backend as a tool Bob can
call. This is optional. Do not pursue until Gate G-12 is met.

### Example MCP server config

```json
{
  "mcpServers": {
    "repopilot": {
      "command": "python",
      "args": ["-m", "backend.mcp_server"]
    }
  }
}
```

---

## Firewall / Network

If Bob IDE cannot reach its servers, add these to your firewall
allowlist (from the hackathon guide):

- `*.bob.ibm.com`
- `*.ibm.com`
- `api.openai.com` (if using GPT fallback)

---

## Reference

- Bob IDE docs: bundled in the IDE (Documentation button)
- Bob Shell docs: linked from the hackathon guide
- Task session screenshots: see the guide, page 16–17
