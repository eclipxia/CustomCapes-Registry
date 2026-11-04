"""Validates capes.json and every cape png. Run by CI on pull requests; also runnable locally: python3 scripts/validate.py"""
import json, re, struct, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 256 * 1024
# vanilla cape layouts: 64x32, or the 2x/4x... scaled versions (width is a multiple of 64, height half of it)
errors = []

index = json.loads((ROOT / "capes.json").read_text())
capes = index.get("capes", {})
listed = set()
for key, rel in capes.items():
    try:
        uuid.UUID(key)
    except ValueError:
        errors.append(f"{key}: not a valid UUID")
        continue
    if key != key.lower():
        errors.append(f"{key}: UUID must be lowercase")
    if not re.fullmatch(r"capes/[0-9a-f-]{36}\.png", rel) or rel != f"capes/{key}.png":
        errors.append(f"{key}: path must be exactly capes/{key}.png")
        continue
    listed.add(rel)
    f = ROOT / rel
    if not f.is_file():
        errors.append(f"{rel}: file is missing")
        continue
    data = f.read_bytes()
    if len(data) > MAX_BYTES:
        errors.append(f"{rel}: larger than {MAX_BYTES // 1024} KB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append(f"{rel}: not a png")
        continue
    w, h = struct.unpack(">II", data[16:24])
    if h * 2 != w or w % 64 != 0 or w > 1024:
        errors.append(f"{rel}: size {w}x{h} is not a cape layout (64x32, 128x64, ... up to 1024x512)")

for f in (ROOT / "capes").glob("*.png"):
    if f.relative_to(ROOT).as_posix() not in listed:
        errors.append(f"{f.name}: not listed in capes.json")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(capes)} capes")
