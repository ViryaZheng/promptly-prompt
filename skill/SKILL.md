---
name: promptly-prompt
description: |
  Clarity gate for prompts: intercepts unclear requests and forces the model
  to restate the user's intent to align before working, then diagnose the
  root cause and reuse the domain's mature, established practices before
  improvising. Clear prompts pass through untouched.
---

# promptly-prompt

AI answer quality depends on input clarity, not prompt tricks — and nobody
writes perfectly clear prompts all the time. This skill catches the unclear
ones at submission and repairs them through alignment.

It operates via a `UserPromptSubmit` hook that injects two disciplines
into unclear requests, both at once:

1. **Restate to align** — echo the user's request in your own words and
   state your understanding, so a misread surfaces before any work happens.
   If the restatement reveals a mismatch, raise it before acting.

2. **Diagnose, then reuse prior art** — don't solve from memory. Diagnose
   the root cause of the problem, search for the domain's mature, established
   practices — methodologies, frameworks, libraries, prior art — and only
   then proceed. If nothing fits, say so and explain why.

The hook script at `scripts/intercept.py` scores prompt unclarity using
rule-based signals: vague verbs without success criteria, hedging, and
dangling referents add points; concrete anchors (paths, errors, code),
structure, and explicit criteria subtract them. Length never adds points —
a long, well-specified prompt is the clearest kind and passes untouched.
Unclear requests (score >= 3) get the full injection, in the prompt's own
language (Chinese or English) — both disciplines, every time.

## Explicit Invocation

When invoked directly (e.g., user says "optimize this prompt"), apply the
two disciplines manually: restate the user's intent with implicit needs
surfaced, then locate the domain and the existing methods that belong to
it. Rewrite the prompt with that context filled in.
