"""Rebuild an uploaded photo/video from its planner asset parts.
Usage: python3 kit/join_parts.py <out-file> <sha256 or -> <part1> [<part2> ...]
Each part is the file a read_asset call saved (the tool result says "saved to <path>",
or "[Image source: <path>]" for images). Give the parts in the order of the request's `parts` list."""
import sys, hashlib, pathlib
out, want, parts = sys.argv[1], sys.argv[2], sys.argv[3:]
data = b"".join(pathlib.Path(p).read_bytes() for p in parts)
got = hashlib.sha256(data).hexdigest()
if want not in ("-", "") and got != want:
    sys.exit(f"sha256 mismatch: got {got}, expected {want}. Re-read the parts in the right order.")
pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
pathlib.Path(out).write_bytes(data)
print("ok", out, len(data), "bytes")
