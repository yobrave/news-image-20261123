"""news-image-20261123 entry builder.

Validate and reproduce the competition artifact entry.png byte-for-byte.

The poster itself is rendered offline; this script is what the make.fun
harness runs. It refuses to emit anything unless every gate passes:

1. the file exists and is a real PNG (IHDR signature, not just an extension);
2. dimensions are exactly the allowed canvas (must be square, <= 1024 px);
3. the file is <= 1 MiB (the competition hard limit);
4. after writing the copy, the SHA-256 digest of the copy matches the
   source, proving the pass-through introduced no re-encode.

It prints a JSON receipt on success so the harness log shows what ran.
"""

import hashlib
import json
import os
import struct
import sys

MAX_BYTES = 1024 * 1024
MAX_DIM = 1024
ENTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
# Reproduction target: the harness mounts the repository read-only and gives
# us a writable output directory via MAKEFUN_OUTPUT_DIR; fall back to the
# entry's own directory for local runs.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(ENTRY)
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def fail(reason: str) -> None:
    print(json.dumps({"ok": False, "reason": reason}))
    sys.exit(1)


def read_png_header(path: str):
    """Return (width, height) from the IHDR chunk, or fail loudly."""
    with open(path, "rb") as fh:
        sig = fh.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            fail("not a PNG: bad signature")
        chunk_len = fh.read(4)
        chunk_type = fh.read(4)
        if chunk_len != b"\x00\x00\x00\r" or chunk_type != b"IHDR":
            fail("not a PNG: IHDR missing")
        data = fh.read(13)
        width, height = struct.unpack(">II", data[:8])
    return width, height


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    if not os.path.isfile(ENTRY):
        fail(f"entry.png missing at {ENTRY}")

    size = os.path.getsize(ENTRY)
    if size > MAX_BYTES:
        fail(f"entry.png is {size} bytes, over the {MAX_BYTES} byte limit")

    width, height = read_png_header(ENTRY)
    if width != height:
        fail(f"canvas must be square, got {width}x{height}")
    if width > MAX_DIM or height > MAX_DIM:
        fail(f"canvas {width}x{height} exceeds {MAX_DIM}px limit")

    # Reproduce: byte-for-byte copy, no re-encode. Read the source fully
    # first, then write, so in-place reproduction never truncates itself.
    with open(ENTRY, "rb") as src:
        payload = src.read()
    before = hashlib.sha256(payload).hexdigest()
    tmp = OUTPUT + ".repro"
    with open(tmp, "wb") as dst:
        dst.write(payload)
    after = sha256(tmp)
    if before != after:
        os.remove(tmp)
        fail("digest mismatch after reproduction")
    os.replace(tmp, OUTPUT)

    receipt = {
        "ok": True,
        "entry": os.path.basename(ENTRY),
        "width": width,
        "height": height,
        "bytes": size,
        "sha256": before,
        "reproduced": OUTPUT,
    }
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
