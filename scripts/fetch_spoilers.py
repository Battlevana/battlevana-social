"""Runs on GitHub Actions (open internet). Pulls new and upcoming Magic cards from Scryfall
plus known combos from Commander Spellbook, and writes them to ./out for the `spoilers` branch.

out/index.json   every card in sets that are not released yet, with first_seen (UTC date we first saw it)
out/img/<id>.jpg      large card image   (only cards first seen in the last KEEP_DAYS days)
out/art/<id>.jpg      art crop           (same)
out/combos.json  Commander Spellbook combos for cards first seen in the last COMBO_DAYS days
out/extra/<slug>.json|.jpg|_art.jpg  any card requested in requests/cards.txt on main (one exact English card name per line,
                 optionally "Name | setcode"), kept permanently. Used for Behind the Card and combo posts.
"""
import json, os, pathlib, time, datetime, urllib.request, urllib.parse

UA = {"User-Agent": "BattleVanaSocial/1.0 (battlevana.be)", "Accept": "application/json;q=0.9,*/*;q=0.8"}
KEEP_DAYS, COMBO_DAYS = 21, 10
OUT = pathlib.Path("out"); (OUT / "img").mkdir(parents=True, exist_ok=True); (OUT / "art").mkdir(exist_ok=True)
PREV = pathlib.Path("prev")  # previous spoilers branch checkout (may be empty)
today = datetime.datetime.now(datetime.timezone.utc).date()

def get(url, raw=False):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                b = r.read(); time.sleep(0.12)
                return b if raw else json.loads(b)
        except Exception as ex:
            if getattr(ex, "code", None) == 404: return None
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("failed " + url)

prev = {}
if (PREV / "index.json").exists():
    prev = {c["id"]: c for c in json.load(open(PREV / "index.json"))["cards"]}

cards, url = [], "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode(
    {"q": f"date>{today} game:paper", "order": "spoiled", "dir": "desc", "unique": "prints", "include_extras": "true"})
while url:
    page = get(url)
    if not page: break
    cards += page["data"]; url = page.get("next_page")

def face(c, key):
    if key in c: return c[key]
    return " // ".join(f.get(key, "") for f in c.get("card_faces", []) if f.get(key))

def uris(c):
    u = c.get("image_uris") or (c.get("card_faces") or [{}])[0].get("image_uris") or {}
    return u.get("large"), u.get("art_crop")

out = []
for c in cards:
    p = prev.get(c["id"])
    first = p["first_seen"] if p else (c.get("preview", {}).get("previewed_at") or str(today)) if not prev else str(today)
    big, art = uris(c)
    rec = {"id": c["id"], "n": c["name"], "set": c["set"], "setname": c["set_name"], "released_at": c.get("released_at"),
           "r": c.get("rarity"), "mana": face(c, "mana_cost"), "type": face(c, "type_line"), "text": face(c, "oracle_text"),
           "pt": (c.get("power", "") + "/" + c.get("toughness", "")) if "power" in c else "", "ci": c.get("color_identity", []),
           "colors": c.get("colors") or (c.get("card_faces") or [{}])[0].get("colors", []),
           "reprint": c.get("reprint", False), "lang": c.get("lang"), "layout": c.get("layout"),
           "previewed_at": c.get("preview", {}).get("previewed_at"), "preview_source": c.get("preview", {}).get("source"),
           "artist": c.get("artist"), "scryfall_uri": c.get("scryfall_uri"), "img": big, "art": art, "first_seen": first}
    fresh = (today - datetime.date.fromisoformat(first)).days <= KEEP_DAYS
    rec["has_images"] = False
    if fresh and big:
        for kind, u in (("img", big), ("art", art)):
            dst = OUT / kind / f'{c["id"]}.jpg'; old = PREV / kind / f'{c["id"]}.jpg'
            if old.exists(): dst.write_bytes(old.read_bytes())
            elif u:
                b = get(u, raw=True)
                if b: dst.write_bytes(b)
        rec["has_images"] = (OUT / "img" / f'{c["id"]}.jpg').exists()
    out.append(rec)

combos = {}
prev_combos = json.load(open(PREV / "combos.json")) if (PREV / "combos.json").exists() else {}
for rec in out:
    if (today - datetime.date.fromisoformat(rec["first_seen"])).days > COMBO_DAYS or rec["reprint"]: continue
    name = rec["n"].split(" // ")[0]
    q = "https://backend.commanderspellbook.com/variants/?" + urllib.parse.urlencode({"format": "json", "q": f'card:"{name}"', "limit": 20})
    try:
        r = get(q)
        res = [{"id": v["id"], "cards": [u["card"]["name"] for u in v.get("uses", [])],
                "produces": [p["feature"]["name"] for p in v.get("produces", [])],
                "identity": v.get("identity"), "description": v.get("description", "")[:1200],
                "url": "https://commanderspellbook.com/combo/" + v["id"]} for v in (r or {}).get("results", [])]
    except Exception:
        res = prev_combos.get(name, [])
    if res: combos[name] = res

# on-demand cards (any card ever printed)
(OUT / "extra").mkdir(exist_ok=True)
if (PREV / "extra").exists():
    for f in (PREV / "extra").iterdir(): (OUT / "extra" / f.name).write_bytes(f.read_bytes())
import re
req = pathlib.Path("requests/cards.txt")
for line in (req.read_text().splitlines() if req.exists() else []):
    line = line.split("#")[0].strip()
    if not line: continue
    name, _, setc = (x.strip() for x in line.partition("|"))
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower().replace("'", "")).strip("-") + (("-" + setc.lower()) if setc else "")
    if (OUT / "extra" / f"{slug}.json").exists(): continue
    c = get("https://api.scryfall.com/cards/named?" + urllib.parse.urlencode({"exact": name, **({"set": setc} if setc else {})}))
    if not c: print("not found:", line); continue
    big, art = uris(c)
    rec = {"id": c["id"], "n": c["name"], "set": c["set"], "setname": c["set_name"], "released_at": c.get("released_at"), "r": c.get("rarity"),
           "mana": face(c, "mana_cost"), "type": face(c, "type_line"), "text": face(c, "oracle_text"), "artist": c.get("artist"),
           "flavor": face(c, "flavor_text"), "scryfall_uri": c.get("scryfall_uri"), "slug": slug, "img": big, "art": art,
           "prices": c.get("prices"), "legalities": c.get("legalities")}
    json.dump(rec, open(OUT / "extra" / f"{slug}.json", "w"), ensure_ascii=False, indent=1)
    for suffix, u in (("", big), ("_art", art)):
        if u:
            b = get(u, raw=True)
            if b: (OUT / "extra" / f"{slug}{suffix}.jpg").write_bytes(b)
    print("extra:", slug)

json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "count": len(out), "cards": out},
          open(OUT / "index.json", "w"), ensure_ascii=False, indent=0)
json.dump(combos, open(OUT / "combos.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "cards,", sum(r["has_images"] for r in out), "with images,", len(combos), "cards with combos")
