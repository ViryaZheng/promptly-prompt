# promptly-prompt

A Claude Code skill that forces AI to **understand before executing**.

> A good prompt solves the problem fast — not through decoration, but by aligning with the AI from the very first message and on every one after. One plugin, two sentences, and ~90% of prompt problems disappear. The two that matter: **clear** and **concise**.

## What It Does

A `UserPromptSubmit` hook that acts as a **clarity gate**: it intercepts unclear prompts — vague verbs with no success criterion ("make it better"), hedging, dangling references — and injects two disciplines, both at once:

1. **Restate to align** — Echo the request back in its own words and state its understanding, so you can catch a misread before any work happens. If the restatement surfaces a mismatch, AI raises it before acting.
2. **Diagnose, then reuse prior art** — Don't solve from memory. Diagnose the root cause of the problem, search for the domain's mature, established practices — frameworks, libraries, methodologies, prior art — and only then proceed. If nothing fits, say so and explain why.

Clear prompts pass through untouched — no matter how long. A detailed spec with file paths, error messages, and acceptance criteria is the *clearest* prompt there is; only unclear ones pay the alignment tax. Simple commands (`git status`, `read file.py`, `/commit`) also pass silently.

The injection follows the prompt's language: Chinese prompts get the Chinese protocol, English prompts the English one.

## Why

Most AI failures start with an unclear input — and nobody writes perfectly clear prompts when their brain is foggy. Instead of teaching you to prompt better, this hook catches the unclear prompt at submission and repairs it in place: the restatement forces one round of alignment, after which it is as if you had submitted a clear prompt all along. You don't have to get better; the collaboration does.

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

> When a request is unclear or ambiguous: First restate this prompt in your own words and confirm your understanding with the user; once aligned, diagnose the true root cause and search the domain's established practices before you act.

中文版：

> 遇到不清楚或含糊的请求时：先用自己的话复述这条 prompt、说出你的理解，和用户对齐之后，再诊断问题的真正来源、搜索该领域的成熟做法，然后才动手。

Same discipline, no install — two sentences that keep you aligned from the first message to the last.

## How It Works

The hook scores every prompt's **unclarity** — not complexity, not length — using rule-based signals:

| Unclear evidence | Score |
|--------|-------|
| Vague action verb, no success criterion ("optimize", "美化", "make it better") — cap +4 | +2 each |
| Hedging words ("maybe", "大概", "not sure") — cap +3 | +1 each |
| Dangling referent ("那块", "that thing") — cap +2 | +1 each |
| Steps narrated while hedging (stream of consciousness) | +1 |
| Vague action with nothing concrete to anchor it | +1 |
| Multiple questions (>1 `?`) | +1 |

| Clear evidence | Score |
|--------|-------|
| Concrete anchors: code, file paths, line numbers, error text | −2 |
| Structure: numbered lists, bullets, headings | −2 |
| Explicit success criteria ("requirements", "要求是", "must pass") | −1 |
| Concrete imperative at start ("fix", "run", "git") | −1 |
| Slash command (`/commit`) | −3 |
| Conversational continuation ("continue", "好的") | −3 |

Score ≥ 3 triggers injection. Below 3 passes through silently. Length never adds points: a long, well-specified spec is the clearest prompt there is.

No API calls. No dependencies beyond Python stdlib. Runs in < 50ms.

## Origin

Inspired by [promptly-prompt](https://www.promptly-prompt.com/), a prompt optimization project built during sophomore year. The original vision was a full prompt optimization pipeline — this skill distills the core insight: **understand first, find existing methods, then act**.

From prompt engineering to context engineering.

## License

MIT
