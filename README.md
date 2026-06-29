# promptly-prompt

A Claude Code skill that forces AI to **understand before executing**.

> A good prompt solves the problem fast — not through decoration, but by aligning with the AI from the very first message and on every one after. One plugin, two sentences, and ~90% of prompt problems disappear. The two that matter: **clear** and **concise**.

## What It Does

A `UserPromptSubmit` hook that automatically intercepts complex requests and injects two disciplines, both at once:

1. **Restate to align** — Echo the request back in its own words and state its understanding, so you can catch a misread before any work happens. If the restatement surfaces a mismatch, AI raises it before acting.
2. **Diagnose, then reuse prior art** — Don't solve from memory. Diagnose the root cause of the problem, search for the domain's mature, established practices — frameworks, libraries, methodologies, prior art — and only then proceed. If nothing fits, say so and explain why.

Simple commands (`git status`, `read file.py`, `/commit`) pass through untouched.

## Why

When your brain is foggy, you write bad prompts, get bad answers, and spiral. This hook acts as a guardrail — it forces AI to pause, restate, search the relevant domain, and confirm direction before diving in. The core insight: most bad AI answers come from missing context and skipped prior art, not missing prompt tricks.

## Install

### Plugin marketplace (recommended)

In your terminal:

```bash
claude plugin marketplace add ViryaZheng/promptly-prompt
claude plugin install promptly-prompt@promptly-prompt
```

Or inside a Claude Code session, prefix with `!`:

```
! claude plugin marketplace add ViryaZheng/promptly-prompt
! claude plugin install promptly-prompt@promptly-prompt
```

### Uninstall

```bash
claude plugin uninstall promptly-prompt@promptly-prompt
claude plugin marketplace remove promptly-prompt
```

## Use it in chat (claude.ai)

The hook only runs in Claude Code — chat surfaces have no per-message hook to plug into. But the value was never the Python; it's the two sentences. In regular chat, paste them once into **Settings → Custom Instructions** (or a custom **Style**), and they apply to every message automatically:

> Restate the prompt and state your own understanding to align with me, then diagnose the root cause, search the domain's mature, established practices, and only then proceed.

Same discipline, no install — two sentences that keep you aligned from the first message to the last.

## How It Works

The hook script scores every prompt's complexity using rule-based signals:

| Signal | Score |
|--------|-------|
| Long text (>80 words / chars for Chinese) | +2 |
| Medium text (40–80 words) | +1 |
| Multiple sentences (>3) | +1 |
| Multi-step words — each match ("then", "然后", …), cap +3 | +2 each |
| Ambiguity words — each match ("maybe", "大概", …), cap +3 | +1 each |
| Multiple questions (>1 `?`) | +1 |
| Code blocks / file paths | −2 |
| Imperative verb at start ("fix", "run", "git") | −1 |
| Slash command (`/commit`) | −3 |
| Very short (<10 chars) | −3 |

Score ≥ 3 triggers injection. Below 3 passes through silently.

No API calls. No dependencies beyond Python stdlib. Runs in < 50ms.

## Origin

Inspired by [promptly-prompt](https://www.promptly-prompt.com/), a prompt optimization project built during sophomore year. The original vision was a full prompt optimization pipeline — this skill distills the core insight: **understand first, find existing methods, then act**.

From prompt engineering to context engineering.

## License

MIT
