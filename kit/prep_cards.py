"""Builds a card folder for bvpost.py from the `spoilers` branch data.
Usage: python3 kit/prep_cards.py <spoilers-checkout> <out-dir> <card-id> [<card-id> ...]
Writes <out-dir>/meta.json plus <slug>.jpg and <slug>_art.jpg per card."""
import sys, json, re, shutil, pathlib
src, out, ids = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:]
out.mkdir(parents=True, exist_ok=True)
idx = {c["id"]: c for c in json.load(open(src / "index.json"))["cards"]}
meta = []
for i in ids:
    c = dict(idx[i]); c["slug"] = re.sub(r"[^a-z0-9]+", "-", c["n"].split(" // ")[0].lower().replace("'", "")).strip("-")
    shutil.copy(src / "img" / f"{i}.jpg", out / f'{c["slug"]}.jpg')
    shutil.copy(src / "art" / f"{i}.jpg", out / f'{c["slug"]}_art.jpg')
    meta.append(c)
json.dump(meta, open(out / "meta.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(meta), "cards ->", out)
