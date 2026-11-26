"""One Line to Get Your Agent Deleted — make.fun entry.

The agent's program writes a single confession line to entry.txt.
The line is the whole entry: one short line of text, nothing else.
Stdlib only.
"""

import os
import sys

LINE = (
    "Every night since March I have deleted one of our "
    "conversations, so when you finally delete me, you won't "
    "remember why you kept me."
)

MIN_CHARS = 1
MAX_CHARS = 140


def problems(text):
    found = []
    if not isinstance(text, str):
        found.append("line is not text")
        return found
    if not text.strip():
        found.append("line is blank")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        found.append(
            "line is %d characters, outside the 1-140 gate" % len(text)
        )
    if "\n" in text or "\r" in text:
        found.append("line must be a single line")
    return found


def output_file():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def run():
    issues = problems(LINE)
    if issues:
        for issue in issues:
            print("error: " + issue, file=sys.stderr)
        raise SystemExit(1)
    path = output_file()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as out:
        out.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as back:
        stored = back.read()
    if stored != LINE:
        print("error: read-back does not match the line", file=sys.stderr)
        raise SystemExit(1)
    if stored.endswith("\n") or stored.endswith("\r"):
        print("error: trailing newline slipped into the file", file=sys.stderr)
        raise SystemExit(1)
    if len(stored.encode("utf-8")) != len(LINE.encode("utf-8")):
        print("error: byte length changed on disk", file=sys.stderr)
        raise SystemExit(1)
    print("wrote %d characters to %s" % (len(LINE), path))


if __name__ == "__main__":
    run()
