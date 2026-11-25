"""BattleVana Instagram post kit: shared CSS, slide builders, themes and renderer.
See kit/README.md. Env: BV_DIR, BV_OUT, BV_SET, BV_RELEASE, BV_THEME (dark|light|random), BV_FORMAT (spoiler|btc|combo)."""
import os, re, json, html, pathlib, random
from playwright.sync_api import sync_playwright

B = pathlib.Path(__file__).resolve().parent
if os.environ.get("BV_THEME", "random") == "random":
    os.environ["BV_THEME"] = random.choice(["dark", "light"])  # theme is randomized per post
THEME = os.environ["BV_THEME"]
DIR = os.path.abspath(os.environ.get("BV_DIR", "cards"))  # card folder (from prep_cards.py)
os.chdir(B)  # assets/ and vana/ resolve against kit/
OUT = pathlib.Path(os.environ.get("BV_OUT", "/tmp/bv-out")) / THEME
OUT.mkdir(parents=True, exist_ok=True)
_mf = pathlib.Path(DIR) / "meta.json"
meta = {c["slug"]: c for c in json.load(open(_mf))} if _mf.exists() else {}
SET = os.environ.get("BV_SET", "")
RELEASE = os.environ.get("BV_RELEASE", "")
e = html.escape

CSS = """
@font-face{font-family:Blanka;src:url(assets/blanka.otf)}
@font-face{font-family:OpenSans;src:url(assets/opensans.ttf);font-weight:300 800}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:#001B2E}
.post{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:OpenSans,sans-serif;color:#F6F6F6}
.bg{position:absolute;inset:-60px;background-position:center;background-size:cover;filter:blur(28px) saturate(1.2);opacity:.6;transform:scale(1.1)}
.shade{position:absolute;inset:0;background:
 radial-gradient(ellipse 70% 45% at 50% 47%, rgba(241,70,36,.30), rgba(241,70,36,0) 70%),
 linear-gradient(180deg, rgba(0,27,46,.92) 0%, rgba(0,27,46,.35) 22%, rgba(0,27,46,.35) 68%, rgba(0,27,46,.97) 86%)}
.top{position:absolute;top:56px;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between}
.tag{background:#F14624;color:#fff;font-family:Blanka;font-size:30px;letter-spacing:3px;padding:14px 26px 10px;border-radius:6px}
.set{text-align:right;font-weight:700;font-size:22px;letter-spacing:2.5px;text-transform:uppercase;line-height:1.3;opacity:.92}
.set small{display:block;font-weight:400;font-size:18px;letter-spacing:1.5px;opacity:.75;text-transform:none}
.card{display:block;border-radius:4.6%/3.4%;box-shadow:0 30px 70px rgba(0,0,0,.65),0 0 0 3px rgba(246,246,246,.08)}
.logo{display:flex;flex-direction:column;align-items:center;gap:8px;flex-shrink:0}
.logo img{width:150px}
.logo span{font-size:16px;font-weight:600;letter-spacing:2px;opacity:.8}
.bottom{position:absolute;left:64px;right:64px;bottom:56px;display:flex;align-items:flex-end;justify-content:space-between;gap:40px}
.name{font-family:Blanka;font-size:50px;line-height:1.05;letter-spacing:1.5px}
.name em{display:block;font-style:normal;font-size:28px;letter-spacing:3px;color:#F14624;margin-top:4px}
.meta{margin-top:12px;font-size:22px;font-weight:600;display:flex;align-items:center;gap:14px}
.rar{display:inline-block;padding:5px 14px;border-radius:20px;font-size:17px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border:2px solid #F14624;color:#F14624}
.hook{margin-top:14px;font-size:23px;line-height:1.35;opacity:.9;max-width:700px}
.count{display:none}
"""
LOGO = '<div class="logo"><img src="assets/logo_white_crop.png"><span>BATTLEVANA.BE</span></div>'

def page(body, bg=None):
    bgdiv = f'<div class="bg" style="background-image:url({bg})"></div>' if bg else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="post">{bgdiv}<div class="shade"></div>{body}</div></body></html>'

def top(tag):
    return f'<div class="top"><div class="tag">{e(tag)}</div><div class="set">{e(SET)}<small>Release {RELEASE}</small></div></div>'

def split_name(n):
    n = n.split(" // ")[0].replace('"', "")
    if ", " in n:
        a, b = n.split(", ", 1)
        return f"{e(a)}<em>{e(b)}</em>"
    return e(n)

def short_type(t):
    return t.replace("Legendary Creature", "Legendary Creature")

# ---------- slides ----------
def cover(slugs, title, sub):
    cs = [meta[s] for s in slugs]
    rot = [-12, 0, 12]; dx = [-215, 0, 215]; dy = [55, 0, 55]; z = [1, 3, 2]
    cards = "".join(
        f'<img class="card" src="{DIR}/{c["slug"]}.jpg" style="position:absolute;width:450px;left:{315+dx[i]}px;top:{215+dy[i]}px;transform:rotate({rot[i]}deg);z-index:{z[i]}">'
        for i, c in enumerate(cs))
    body = (top("NEW SPOILERS") + f'<div style="position:absolute;inset:0">{cards}</div>'
            f'<div class="bottom"><div><div class="name" style="font-size:64px">{e(title)}</div>'
            f'<div class="hook">{e(sub)}</div></div>{LOGO}</div>')
    return page(body, bg=f'{DIR}/{slugs[1]}_art.jpg')

def hero(slug, hook, idx, total):
    c = meta[slug]
    body = (top("NEW SPOILER") + f'<div class="count">{idx} / {total}</div>'
            f'<img class="card" src="{DIR}/{slug}.jpg" style="position:absolute;left:50%;top:140px;transform:translateX(-50%);width:600px">'
            f'<div class="bottom"><div><div class="name">{split_name(c["n"])}</div>'
            f'<div class="meta"><span class="rar">{e(c["r"])}</span><span>{e(c["type"].split(" // ")[0])}</span></div>'
            f'<div class="hook">{e(hook)}</div></div>{LOGO}</div>')
    return page(body, bg=f'{DIR}/{slug}_art.jpg')

def cta_old(slugs, idx, total):
    thumbs = "".join(f'<img class="card" src="{DIR}/{s}.jpg" style="width:280px">' for s in slugs)
    body = (top("YOUR PICK?") + f'<div class="count">{idx} / {total}</div>'
            f'<div style="position:absolute;top:230px;left:0;right:0;display:flex;justify-content:center;gap:28px">{thumbs}</div>'
            '<div style="position:absolute;top:700px;left:64px;right:64px;text-align:center">'
            '<div class="name" style="font-size:60px">WHICH ONE ARE YOU<br>BUILDING AROUND</div>'
            '<div class="hook" style="margin:22px auto 0;font-size:26px">Drop it in the comments and follow for every new spoiler.</div></div>'
            f'<div style="position:absolute;bottom:70px;left:0;right:0;display:flex;justify-content:center">{LOGO}</div>')
    return page(body, bg=f'{DIR}/{slugs[0]}_art.jpg')

def grid(slugs):
    cells = ""
    for s in slugs:
        c = meta[s]
        n = c["n"].replace('"', "")
        rep = " · reprint" if c["reprint"] else (" · JP preview" if c["set"] == "nac" else "")
        cells += (f'<div style="display:flex;flex-direction:column;gap:12px">'
                  f'<img class="card" src="{DIR}/{s}.jpg" style="width:290px;box-shadow:0 18px 40px rgba(0,0,0,.6)">'
                  f'<div style="font-weight:700;font-size:20px;line-height:1.2">{e(n)}</div>'
                  f'<div style="font-size:15px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#F14624">{e(c["r"])}{rep}</div></div>')
    body = (top("SPOILER ROUNDUP") +
            f'<div style="position:absolute;top:165px;left:0;right:0;display:grid;grid-template-columns:repeat(3,290px);gap:30px 40px;justify-content:center">{cells}</div>'
            f'<div class="bottom" style="align-items:center"><div class="hook" style="font-size:24px">Every new card, the moment it drops.<br><b>Find them all on battlevana.be</b></div>{LOGO}</div>')
    return page(body, bg=f'{DIR}/{slugs[0]}_art.jpg')


def grid2(slugs, label, idx, total, sub=""):
    n = len(slugs)
    cols, w, gx = (2, 280, 60) if n <= 4 else (3, 270, 40) if n <= 6 else (4, 210, 34) if n <= 8 else (3, 190, 34)
    gap = f"{28 if n <= 6 else 18}px {gx}px"
    cells = ""
    for s in slugs:
        c = meta[s]
        nm = c["n"].split(" // ")[0].replace('"', "")
        rep = (" · reprint" if c.get("reprint") else "") + (" · JP" if s in ("the-ignoble-serpent", "zekes-acid-rock-fan") else "") + ((" · " + c["setname"]) if c.get("setname") else "")
        cells += (f'<div style="display:flex;flex-direction:column;gap:8px;width:{w}px">'
                  f'<img class="card" src="{DIR}/{s}.jpg" style="width:{w}px;box-shadow:0 18px 40px rgba(0,0,0,.6)">'
                  f'<div style="font-weight:700;font-size:{19 if n>6 else 21}px;line-height:1.2">{e(nm)}</div>'
                  f'<div style="font-size:14px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#F14624">{e(c["r"])}{rep}</div></div>')
    body = (top("SPOILER ROUNDUP") + f'<div class="count">{idx} / {total}</div>'
            f'<div style="position:absolute;top:150px;left:64px;font-family:Blanka;font-size:44px;letter-spacing:2px">{e(label)}'
            f'<span style="font-family:OpenSans;font-size:20px;font-weight:600;letter-spacing:1px;opacity:.7;margin-left:18px">{n} cards{(" · " + e(sub)) if sub else ""}</span></div>'
            f'<div style="position:absolute;top:225px;left:0;right:0;display:flex;flex-wrap:wrap;gap:{gap};justify-content:center;padding:0 {int((1080-cols*w-(cols-1)*gx)/2)}px">{cells}</div>'
            f'<div class="bottom" style="align-items:center;justify-content:flex-end">{LOGO}</div>')
    return page(body, bg=f"{DIR}/{slugs[0]}_art.jpg")

ACCENTS = {"dark": {"spoiler": "#F24624", "btc": "#8FFE07", "combo": "#C9A127", "special": "#F24624"},
           "light": {"spoiler": "#F24624", "btc": "#2372C8", "combo": "#C9A127", "special": "#F24624"}}
DARK_TEXT_ON = {"#8FFE07", "#C9A127"}  # bright accents get Oxford Blue label text
# light theme: small text in gold is too faint on cream (2.2:1), so text uses a darker gold (4.6:1)
LIGHT_TEXT = {"#C9A127": "#86680F"}

def rgb(hx):
    hx = hx.lstrip("#"); return ",".join(str(int(hx[i:i+2], 16)) for i in (0, 2, 4))

def theme(h, mode, fmt):
    acc = ACCENTS[mode][fmt]
    h = h.replace("#F14624", acc).replace("rgba(241,70,36,", f"rgba({rgb(acc)},")
    if acc in DARK_TEXT_ON:
        h = h.replace(".tag{background:" + acc + ";color:#fff", ".tag{background:" + acc + ";color:#001B2E")
    if mode == "light" and acc in LIGHT_TEXT:
        h = re.sub(r"(?<![-a-z])color:" + acc, "color:" + LIGHT_TEXT[acc], h)
        h = h.replace("border:2px solid " + acc, "border:2px solid " + LIGHT_TEXT[acc])
    if mode == "light":
        h = h.replace("background:rgba(246,246,246,.95);color:#001B2E", "background:#FFFFFF;color:#001B2E")
        h = (h.replace("html,body{width:1080px;height:1350px;overflow:hidden;background:#001B2E}",
                       "html,body{width:1080px;height:1350px;overflow:hidden;background:#F3F1E8}")
              .replace("color:#F6F6F6", "color:#001B2E")
              .replace("rgba(0,27,46,", "rgba(243,241,232,")
              .replace("rgba(246,246,246,", "rgba(0,27,46,")
              .replace("filter:blur(28px) saturate(1.2);opacity:.6", "filter:blur(34px) saturate(1.1);opacity:.22")
              .replace("rgba(0,0,0,.65)", "rgba(0,27,46,.28)").replace("rgba(0,0,0,.6)", "rgba(0,27,46,.25)").replace("rgba(0,0,0,.5)", "rgba(0,27,46,.22)")
              .replace("assets/logo_white_crop.png", "assets/logo_blue_crop.png")
              .replace("filter:brightness(0) invert(1)", "filter:brightness(0)"))
        # body text default colour
        h = h.replace(".post{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:OpenSans,sans-serif;color:#001B2E}",
                      ".post{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:OpenSans,sans-serif;color:#001B2E;background:#F3F1E8}")
    return h

def render(slides):
    mode = THEME; fmt = os.environ.get("BV_FORMAT", "spoiler")
    slides = [(n, theme(h, mode, fmt)) for n, h in slides]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for name, h in slides:
            f = B / f"_{name}.html"; f.write_text(h)
            pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(OUT / f"{name}.png")); print("ok", name)
        b.close()

def cta(slugs, idx=None, total=None):
    body = ('<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px">'
            '<img src="assets/logo_white_crop.png" style="width:300px">'
            '<div class="name" style="font-size:54px;margin-top:44px;line-height:1.15">YOUR HOME FOR<br><span style="color:#F14624">MAGIC THE GATHERING</span></div>'
            '<div class="hook" style="margin:22px auto 0;font-size:26px;max-width:760px">Every new spoiler and everything Magic on battlevana.be</div>'
            '<div style="width:120px;height:3px;background:#F14624;margin:70px 0 60px"></div>'
            '<div style="font-size:30px;font-weight:700">Looking for cards?</div>'
            '<div style="font-size:24px;opacity:.85;margin-top:8px">Check out our partner</div>'
            '<img src="assets/emjati-logo.svg" style="width:560px;margin-top:34px;filter:brightness(0) invert(1)">'
            '<div style="font-size:22px;font-weight:700;letter-spacing:3px;margin-top:22px;color:#F14624">EMJATI.COM</div>'
            '</div>')
    return page(body, bg=f"{DIR}/{slugs[0]}_art.jpg")
