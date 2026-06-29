#!/usr/bin/env python3
"""promptly-prompt hook: complexity judge + context injection.

Fires on every UserPromptSubmit. Simple prompts pass through.
Complex prompts (score >= 3) inject the full discipline, both parts at once:
  1. Restate the prompt and state your understanding to align with the user
  2. Diagnose the root cause, search the domain's mature practices, then proceed

No external dependencies. Python stdlib only.
"""

import json
import re
import sys


MULTI_STEP = re.compile(
    r"\b(then|after that|next|first\b.{0,30}\bthen|and also|followed by|"
    r"once .{0,30} (is |are )?done|step \d)"
    r"|然后|接着|并且|首先|之后|同时|再|最后",
    re.IGNORECASE,
)

AMBIGUITY = re.compile(
    r"\b(maybe|perhaps|something like|probably|not sure|might|could be|"
    r"kind of|sort of|or something)"
    r"|大概|可能|之类的|差不多|好像|应该|或者说|不太确定",
    re.IGNORECASE,
)

IMPERATIVE_START = re.compile(
    r"^(read|fix|run|show|list|open|close|delete|move|copy|create|"
    r"write|edit|add|remove|install|update|check|test|build|deploy|"
    r"push|pull|commit|merge|grep|find|cat|ls|cd|git|npm|pip|docker|"
    r"make|curl|ssh|scp|kill|restart|stop|start|help|explain|describe|"
    r"读|改|跑|看|删|装|查|测|建|推|拉)",
    re.IGNORECASE,
)

CODE_BLOCK = re.compile(r"```|`[^`]+`|[~/\.]\S+\.\w{1,5}\b|\/\S+\/\S+")
SLASH_CMD = re.compile(r"^/\w+")


def count_sentences(text: str) -> int:
    parts = re.split(r"[.!?。！？\n]+", text)
    return sum(1 for p in parts if p.strip())


def word_count(text: str) -> int:
    # Chinese: count characters directly; mixed/English: count split tokens
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    if cjk > len(text) * 0.3:
        return len(text.replace(" ", ""))
    return len(text.split())


def score(prompt: str) -> int:
    s = 0
    if len(prompt.strip()) < 10:
        s -= 3
    if word_count(prompt) > 80:
        s += 2
    elif word_count(prompt) > 40:
        s += 1
    if count_sentences(prompt) > 3:
        s += 1
    if prompt.count("?") + prompt.count("？") > 1:
        s += 1
    # Additive: each match contributes, capped at +3
    multi_hits = len(MULTI_STEP.findall(prompt))
    s += min(multi_hits * 2, 3)
    ambig_hits = len(AMBIGUITY.findall(prompt))
    s += min(ambig_hits, 3)
    if CODE_BLOCK.search(prompt):
        s -= 2
    if IMPERATIVE_START.match(prompt.strip()):
        s -= 1
    if SLASH_CMD.match(prompt.strip()):
        s -= 3
    return s


INJECTION = (
    "复述 prompt 说出自己理解来和用户对齐，"
    "然后是诊断问题来源、搜索领域成熟做法再处理。"
)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("prompt", "")
    if not prompt.strip():
        return

    if score(prompt) >= 3:
        print(INJECTION)


if __name__ == "__main__":
    main()
