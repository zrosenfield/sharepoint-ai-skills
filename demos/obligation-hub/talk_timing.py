#!/usr/bin/env python3
"""Estimates speaking time for the run-order talk track in demo-script.md.

Reads the table in section 5 ("Run order"), groups rows by beat, counts the words in the "Say" column as they
are spoken (numbers expanded: "$540,000" is five words, "2027" is two), and compares each beat with its planned
window. Text in [square brackets] is stage direction and isn't counted.

  python talk_timing.py           print the estimate
  python talk_timing.py --write   also refresh the block between the timing markers in demo-script.md

Exits non-zero if the total is outside 7-10 minutes or a beat runs past its window.
"""
import re
import sys
from pathlib import Path

WPM = 140
MIN_TOTAL, MAX_TOTAL = 7 * 60, 10 * 60
SCRIPT = Path(__file__).resolve().parent / "demo-script.md"
START, END = "<!-- timing:start -->", "<!-- timing:end -->"


def int_words(n):
    if n < 100:
        return 1
    if n < 1000:
        return 2 + (int_words(n % 100) if n % 100 else 0)
    for size in (10 ** 9, 10 ** 6, 10 ** 3):
        if n >= size:
            rest = n % size
            return int_words(n // size) + 1 + (int_words(rest) if rest else 0)
    return 1


def spoken(token):
    """Words a token takes to say aloud."""
    if not re.search(r"\d", token):
        return 1 if re.search(r"[A-Za-z]", token) else 0
    total = 0
    for part in token.split("-"):
        if not re.search(r"\d", part):
            total += 1 if re.search(r"[A-Za-z]", part) else 0
            continue
        extra = ("$" in part) + ("%" in part)
        core = re.sub(r"(st|nd|rd|th)$", "", part.strip("$%.,;:!?()\"'"))
        if re.fullmatch(r"\d{1,2}:\d\d", core):
            h, m = core.split(":")
            total += 1 + (0 if m == "00" else 1) + extra
        elif re.fullmatch(r"\d+\.\d+", core):
            a, b = core.split(".")
            total += int_words(int(a)) + 1 + len(b) + extra
        elif re.fullmatch(r"(19|20)\d\d", core):
            total += (3 if core[2] == "0" else 2) + extra
        elif re.fullmatch(r"[\d,]+", core):
            total += int_words(int(core.replace(",", ""))) + extra
        else:
            total += 1 + extra
    return total


def clean(say):
    say = re.sub(r"<[^>]+>", " ", say)
    say = re.sub(r"\[[^\]]*\]", " ", say)
    say = re.sub(r"[*_`]", "", say)
    return say.replace("—", " ").replace("–", " ")


def mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def parse(text):
    sec5 = re.search(r"^## 5\..*?(?=^## \d|\Z)", text, re.S | re.M)
    if not sec5:
        sys.exit("demo-script.md has no '## 5.' section")
    body = sec5.group(0)
    target = re.search(r"Target runtime:\s*\**(\d+):(\d\d)", body)
    if not target:
        sys.exit("Section 5 needs a 'Target runtime: m:ss' line")
    runtime = int(target.group(1)) * 60 + int(target.group(2))
    rows = [ln for ln in body.splitlines() if ln.startswith("|")]
    head = [c.strip().lower() for c in rows[0].strip("|").split("|")]
    ti, bi, si = head.index("time"), head.index("beat"), head.index("say")
    beats, order = {}, []
    for ln in rows[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < len(head):
            continue
        beat = re.sub(r"[*_]", "", cells[bi]).strip()
        if beat not in beats:
            m, s = cells[ti].strip("*").split(":")
            beats[beat] = {"start": int(m) * 60 + int(s), "words": 0}
            order.append(beat)
        beats[beat]["words"] += sum(spoken(t) for t in clean(cells[si]).split())
    for i, b in enumerate(order):
        nxt = beats[order[i + 1]]["start"] if i + 1 < len(order) else runtime
        beats[b]["window"] = nxt - beats[b]["start"]
    return order, beats, runtime


def report(order, beats, runtime):
    out = [f"Speaking time at {WPM} words per minute (numbers counted as spoken).", "",
           "| Beat | Window | Words | Speaking | Slack for clicks, typing and answers |",
           "|---|---:|---:|---:|---:|"]
    ok, total_w = True, 0
    for b in order:
        w = beats[b]["words"]
        sec = w / WPM * 60
        slack = beats[b]["window"] - sec
        ok = ok and slack >= 0
        total_w += w
        out.append(f"| {b} | {mmss(beats[b]['window'])} | {w} | {mmss(sec)} | {mmss(slack) if slack >= 0 else '-' + mmss(-slack)} |")
    total = total_w / WPM * 60
    ok = ok and MIN_TOTAL <= total <= MAX_TOTAL
    out.append(f"| **Total** | **{mmss(runtime)}** | **{total_w}** | **{mmss(total)}** | **{mmss(runtime - total)}** |")
    out += ["", f"Talk track: {mmss(total)} of speaking (target 7:00-10:00); planned runtime {mmss(runtime)}. "
                f"{'Within budget.' if ok else 'OVER BUDGET: trim the beats with negative slack.'}"]
    return ok, "\n".join(out)


def main():
    text = SCRIPT.read_text(encoding="utf-8")
    order, beats, runtime = parse(text)
    ok, table = report(order, beats, runtime)
    print(table)
    if "--write" in sys.argv:
        if START not in text or END not in text:
            sys.exit(f"Add {START} and {END} to section 5 first")
        pre, rest = text.split(START, 1)
        _, post = rest.split(END, 1)
        SCRIPT.write_text(pre + START + "\n" + table + "\n" + END + post, encoding="utf-8")
        print(f"\nUpdated the timing block in {SCRIPT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
