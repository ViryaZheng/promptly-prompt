#!/usr/bin/env python3
"""Golden-case regression tests for intercept.py.

Each line in cases.jsonl: {"name", "prompt", "expect"} where expect is
null (pass through), "zh" or "en" (intercept + injection language).

Run: python3 tests/run_tests.py
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skill" / "scripts" / "intercept.py"

spec = importlib.util.spec_from_file_location("intercept", SCRIPT)
intercept = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intercept)


def run_cases() -> int:
    failures = 0
    cases = [
        json.loads(line)
        for line in (ROOT / "tests" / "cases.jsonl").read_text().splitlines()
        if line.strip()
    ]
    for case in cases:
        prompt, expect = case["prompt"], case["expect"]
        s = intercept.score(prompt)
        fired = s >= intercept.THRESHOLD
        lang = intercept.detect_lang(prompt) if fired else None
        got = lang if fired else None
        ok = got == expect
        failures += 0 if ok else 1
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {case['name']}: score={s} got={got} expect={expect}")
    return failures


def check_output_shape() -> int:
    """End-to-end: intercepted prompt must emit valid hook JSON."""
    vague = json.dumps({"prompt": "帮我优化一下登录那块"})
    out = subprocess.run(
        [sys.executable, str(SCRIPT)], input=vague, capture_output=True, text=True
    ).stdout.strip()
    try:
        data = json.loads(out)
        ctx = data["hookSpecificOutput"]["additionalContext"]
        assert ctx == intercept.INJECTIONS["zh"]
        print("[PASS] output-shape: valid hookSpecificOutput JSON")
        return 0
    except (json.JSONDecodeError, KeyError, AssertionError) as e:
        print(f"[FAIL] output-shape: {e!r} — raw: {out!r}")
        return 1


def check_docs_sync() -> int:
    """The protocol text must appear verbatim in README (drift guard)."""
    readme = (ROOT / "README.md").read_text()
    failures = 0
    for lang in ("zh", "en"):
        if intercept.INJECTIONS[lang] not in readme:
            print(f"[FAIL] docs-sync: {lang} protocol text missing from README.md")
            failures += 1
        else:
            print(f"[PASS] docs-sync: {lang} protocol text present in README.md")
    return failures


if __name__ == "__main__":
    total = run_cases() + check_output_shape() + check_docs_sync()
    print(f"\n{'ALL GREEN' if total == 0 else f'{total} FAILURE(S)'}")
    sys.exit(1 if total else 0)
