#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — entry writer.

Writes the two-part micro-confession (a To: line plus the unsent message
itself, one line, exactly as typed) to entry.txt.

Pure standard library. Deterministic: the same bytes on every run.
Output directory: $MAKEFUN_OUTPUT_DIR, else /output, else ./output.
"""

import os

# Final entry (v2, tournament winner #13): the moment is anchored — "the last
# night of the trip" — because the knockout final was decided on C2: the reason
# it stayed in drafts must be felt in the words, not stated. The substitute
# line ("drive safe") is what was actually said; the unsent sentence hangs in
# the gap between the two clauses. 98 characters total, message 89.
ENTRY = (
    "To: Alex\n"
    "I almost told you I loved you on the last night of the trip. "
    "I said 'drive safe' instead."
)


def resolve_output_dir():
    """$MAKEFUN_OUTPUT_DIR, else /output when it exists, else ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return "./output"


def main():
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
