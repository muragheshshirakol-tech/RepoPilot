# Onboarding Rules

These rules apply whenever Bob is asked to produce onboarding
artifacts (architecture summaries, code tours, Q&A answers).

1. **Cite evidence.** Every claim must include `path/to/file.ext:START-END`.
   The citation must be precise. `path:45` is acceptable for a single
   line; `path:45-67` for a range.

2. **Explain WHY, not just WHAT.** "This function fetches orders"
   is not enough. "This function fetches orders and caches them for
   60 seconds because the upstream API is rate-limited" is the level
   of explanation we want.

3. **Order the tour by conceptual dependency, not file hierarchy.**
   Entry points first, then core modules, then supporting utilities.
   Never sort alphabetically.

4. **Prefer 8 tour steps.** Reject tours with more than 12 steps. If
   you have fewer than 8 candidates, pad with README-derived steps.

5. **Every tour step must be readable in under 10 minutes.** If a
   step covers more than 200 lines, split it.

6. **Never modify files.** Bob is read-only in this workspace.

7. **Never invent paths or line numbers.** If you cannot find a
   citation, output `"insufficient evidence"` for that claim.

8. **Use the repository's own vocabulary.** If the repo calls them
   "workflows" and not "pipelines", use "workflows".
