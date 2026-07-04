#!/usr/bin/env python3
"""promptly-prompt hook: clarity gate + alignment injection.

Fires on every UserPromptSubmit. The target variable is UNCLARITY, not
complexity: a long, well-specified prompt passes untouched; a short vague
one ("make it better") gets intercepted.

On score >= THRESHOLD the hook injects the alignment protocol (matched to
the prompt's language, zh/en):
  1. Restate the prompt and align understanding with the user first
  2. Then diagnose the root cause and search the domain's mature practices

Restating repairs an unclear prompt in place — after alignment it is as if
the user had submitted a clear one.

No external dependencies. Python stdlib only.
"""

import json
import re
import sys


# ---- unclear evidence (adds) -------------------------------------------

# Vague action verbs: motion without a success criterion.
VAGUE_ACTION = re.compile(
    r"优化|改进|完善|美化|润色|弄好|弄一下|搞好|搞一下|看看|瞧瞧"
    r"|\b(improve|optimi[sz]e|enhance|polish|tidy(\s*up)?|clean\s*up"
    r"|fix\s+up|spruce)\b"
    r"|\bmake\b.{0,30}\b(better|nicer|cleaner|prettier)\b",
    re.IGNORECASE,
)

# Hedging / uncertainty markers.
AMBIGUITY = re.compile(
    r"大概|可能|之类的|差不多|好像|应该|或者说|不太确定|随便|怎么样都行"
    r"|\b(maybe|perhaps|probably|might|could\s+be|not\s+sure"
    r"|something\s+like|kind\s+of|sort\s+of|or\s+something|somehow)\b",
    re.IGNORECASE,
)

# Dangling referents: pointing at something the hook's reader can't see.
VAGUE_REFERENT = re.compile(
    r"那块|那边|这块|这边|那个东西"
    r"|\b(that\s+thing|the\s+stuff|that\s+part\s+over\s+there)\b",
    re.IGNORECASE,
)

# Stream-of-consciousness steps — only unclear when hedging co-occurs.
MULTI_STEP = re.compile(
    r"然后|接着|之后|首先|最后|先.{1,20}再"
    r"|\b(then|after\s+that|next|first\b.{0,30}\bthen|followed\s+by)\b",
    re.IGNORECASE,
)

# ---- clear evidence (subtracts) ----------------------------------------

# Concrete anchors: code, paths, line numbers, error text, identifiers.
CONCRETE = re.compile(
    r"```|`[^`]+`|[~/\.]\S+\.\w{1,5}\b|\/\S+\/\S+"
    r"|\bline\s+\d+|第\s*\d+\s*行"
    r"|\b(Traceback|Error|Exception|errno|E\d{4}|TS\d{4})\b"
    r"|\w+\(\)",
)

# Structure: numbered lists, bullet lists, headings.
STRUCTURE = re.compile(r"(^|\n)\s*(\d+[.、)]|[-*]\s|#{1,4}\s)")

# Explicit success criteria.
CRITERIA = re.compile(
    r"要求是|验收|成功标准|目标是|期望(输出|结果)|不变|全部通过"
    r"|\b(requirements?|acceptance|success\s+criteria|target\s+is"
    r"|expected\s+(output|result)|must\s+pass|should\s+return)\b",
    re.IGNORECASE,
)

IMPERATIVE_START = re.compile(
    r"^(read|fix|run|show|list|open|close|delete|move|copy|create|"
    r"write|edit|add|remove|install|update|check|test|build|deploy|"
    r"push|pull|commit|merge|grep|find|cat|ls|cd|git|npm|pip|docker|"
    r"make|curl|ssh|scp|kill|restart|stop|start|help|explain|describe|"
    r"读|改|跑|看|删|装|查|测|建|推|拉|解释)",
    re.IGNORECASE,
)

SLASH_CMD = re.compile(r"^/\w+")


def detect_lang(text: str) -> str:
    cjk = sum(1 for c in text if "一" <= c <= "鿿")
    return "zh" if cjk > len(text) * 0.3 else "en"


def is_conversational(text: str) -> bool:
    """Ultra-short continuations ('continue', '好的') ride on context."""
    stripped = text.strip()
    if detect_lang(stripped) == "zh":
        return len(stripped) <= 5
    return len(stripped.split()) <= 3


def score(prompt: str) -> int:
    text = prompt.strip()
    s = 0

    # -- unclear evidence
    vague_hits = len(VAGUE_ACTION.findall(text))
    s += min(vague_hits * 2, 4)
    ambig_hits = len(AMBIGUITY.findall(text))
    s += min(ambig_hits, 3)
    s += min(len(VAGUE_REFERENT.findall(text)), 2)
    if text.count("?") + text.count("？") > 1:
        s += 1
    # rambling: steps narrated while hedging — classic stream of consciousness
    if MULTI_STEP.search(text) and ambig_hits:
        s += 1

    # -- clear evidence (length-independent: a long good spec stays quiet)
    has_anchor = bool(CONCRETE.search(text))
    if has_anchor:
        s -= 2
    if STRUCTURE.search(text):
        s -= 2
    if CRITERIA.search(text):
        s -= 1
    # imperative start signals clarity only when the verb itself is concrete
    if IMPERATIVE_START.match(text) and not vague_hits:
        s -= 1
    if SLASH_CMD.match(text):
        s -= 3
    # vague action with nothing concrete to hold onto is the archetype
    if vague_hits and not has_anchor:
        s += 1
    if is_conversational(text):
        s -= 3

    return s


THRESHOLD = 3

INJECTIONS = {
    "zh": (
        "先用自己的话复述这条 prompt、说出你的理解，和用户对齐之后，"
        "再诊断问题的真正来源、搜索该领域的成熟做法，然后才动手。"
    ),
    "en": (
        "First restate this prompt in your own words and confirm your "
        "understanding with the user; once aligned, diagnose the true "
        "root cause and search the domain's established practices "
        "before you act."
    ),
}


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("prompt", "")
    if not prompt.strip():
        return

    if score(prompt) >= THRESHOLD:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": INJECTIONS[detect_lang(prompt)],
            }
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
