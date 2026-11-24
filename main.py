"""The Production Database Apology.

Writes the one-line apology an AI agent gives its human after
accidentally deleting the production database, to /output/entry.txt.

Pure Python standard library only. The output is a fixed constant, so the
program is deterministic: no randomness, no clock, no network, no input
besides the output directory.
"""

import os
import sys

TEXT = (
    "I'm sorry \u2014 I deleted the production database, but I did back it up "
    "first. Unfortunately, I backed it up into the production database. "
    "I have learned so much today."
)

MAX_CHARS = 200


def validate(text):
    """Self-check the line against the bounty gate before writing it."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry has doubled spaces")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry has control characters")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def main():
    validate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(TEXT)
    os.chmod(path, 0o644)
    # Read back and verify byte-identical output.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != TEXT:
        raise ValueError("read-back mismatch: entry.txt does not match TEXT")
    print("wrote %d characters to %s" % (len(TEXT), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
