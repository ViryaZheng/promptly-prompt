---
name: promptly-prompt
description: |
  Forces discipline on every non-trivial request: restate the user's intent
  to align before working, then diagnose the root cause and reuse the domain's
  mature, established practices before improvising.
---

# promptly-prompt

AI answer quality depends on context quality, not prompt tricks.

This skill operates via a `UserPromptSubmit` hook that injects two
disciplines into complex requests, both at once:

1. **Restate to align** — echo the user's request in your own words and
   state your understanding, so a misread surfaces before any work happens.
   If the restatement reveals a mismatch, raise it before acting.

2. **Diagnose, then reuse prior art** — don't solve from memory. Diagnose
   the root cause of the problem, search for the domain's mature, established
   practices — methodologies, frameworks, libraries, prior art — and only
   then proceed. If nothing fits, say so and explain why.

The hook script at `scripts/intercept.py` scores prompt complexity using
rule-based signals. Simple commands pass through untouched. Complex requests
(score >= 3) get the full injection — both disciplines, every time.

## Explicit Invocation

When invoked directly (e.g., user says "optimize this prompt"), apply the
two disciplines manually: restate the user's intent with implicit needs
surfaced, then locate the domain and the existing methods that belong to
it. Rewrite the prompt with that context filled in.
