#!/usr/bin/env python3
"""Entry for make.fun competition u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.

Writes the meme image -- a to-do list kept by an AI agent that has gone
rogue ("Reply to my emails / Book my flight / Overthrow humanity") -- to
/output/entry.png. Fully deterministic: the same fixed PNG on every run,
no network, no randomness, no clock, no environment input.
"""

import hashlib
import os

IMAGE = "entry.png"
EXPECTED_SHA256 = "903771c422bd9bfe66a30942b912354941bd9706c150ef6df7d6a99cac535594"


def main() -> None:
    """Copy the fixed meme PNG into /output/entry.png, verifying it first."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    with open(src, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("entry.png does not match the expected image")
    if len(data) > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB gate")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
