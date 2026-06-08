---
name: promptly-prompt
description: |
  Forces discipline on every non-trivial request: restate the user's intent,
  diagnose the root cause, name the domain and reuse existing mature solutions
  before improvising, then deliver one chosen answer instead of a menu of
  options.
---

# promptly-prompt

AI answer quality depends on context quality, not prompt tricks.

This skill operates via a `UserPromptSubmit` hook that injects two
disciplines into complex requests:

1. **Restate, then pause if needed** — echo the user's request in your own
   words, surface implicit constraints, name what would make the answer
   wrong. If anything is ambiguous or your planned approach might not be
   endorsed, stop and ask before acting. If the restatement makes it clear
   there is no disagreement, continue. Skip the restatement only when the
   request is genuinely trivial.

2. **Super-dimensional view** — before solving from memory, name the domain,
   search for established methodologies, frameworks, libraries, and prior
   art, then bring that specialist knowledge to bear. Cite specific names,
   not vague gestures. If nothing fits, say so and explain why.

The hook script at `scripts/intercept.py` scores prompt complexity using
rule-based signals. Simple commands pass through untouched. Complex requests
get the full injection.

## Explicit Invocation

When invoked directly (e.g., user says "optimize this prompt"), apply the
two disciplines manually: restate the user's intent with implicit needs
surfaced, then locate the domain and the existing methods that belong to
it. Rewrite the prompt with that context filled in.
