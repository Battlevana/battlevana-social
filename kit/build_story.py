"""Story (1080x1920) from a post's cover slide.
Usage: python3 build_story.py <cover.jpg> <format> <theme> <out.png>
Safe zones: nothing important in the top ~250px and bottom ~340px (Instagram UI)."""
import sys, pathlib
from playwright.sync_api import sync_playwright

cover, fmt, theme, out = sys.argv[1:5]
B = pathlib.Path(__file__).resolve().parent
ACC = {"dark": {"spoiler": "#F24624", "btc": "#8FFE07", "combo": "#C9A127", "special": "#F24624"},
       "light": {"spoiler": "#F24624", "btc": "#2372C8", "combo": "#C9A127", "special": "#F24624"}}[theme][fmt]
label_ink = "#001B2E" if ACC in ("#8FFE07", "#C9A127") else "#FFFFFF"
bg, ink = ("#001B2E", "#F6F6F6") if theme == "dark" else ("#F3F1E8", "#001B2E")
veil = "rgba(0,27,46,.55)" if theme == "dark" else "rgba(243,241,232,.7)"
shadow = "rgba(0,0,0,.6)" if theme == "dark" else "rgba(0,27,46,.25)"
cover_uri = pathlib.Path(cover).resolve().as_uri()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Blanka;src:url({(B/'assets/blanka.otf').as_uri()})}}
@font-face{{font-family:OpenSans;src:url({(B/'assets/opensans.ttf').as_uri()});font-weight:300 800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{bg}}}
.s{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:OpenSans,sans-serif;color:{ink}}}
.bg{{position:absolute;inset:-80px;background:url({cover_uri}) center/cover;filter:blur(40px) saturate(1.1);opacity:{'.55' if theme=='dark' else '.35'}}}
.veil{{position:absolute;inset:0;background:{veil}}}
.top{{position:absolute;top:280px;left:0;right:0;display:flex;justify-content:center}}
.tag{{background:{ACC};color:{label_ink};font-family:Blanka;font-size:40px;letter-spacing:4px;padding:16px 34px 11px;border-radius:8px}}
.card{{position:absolute;left:90px;top:400px;width:900px;border-radius:22px;box-shadow:0 34px 80px {shadow}}}
.bot{{position:absolute;top:1560px;left:80px;right:80px;text-align:center;font-size:32px;font-weight:700;line-height:1.3}}
.bot span{{display:block;font-size:24px;font-weight:600;opacity:.75;margin-top:6px;letter-spacing:2px}}
</style></head><body><div class="s"><div class="bg"></div><div class="veil"></div>
<div class="top"><div class="tag">NEW ON OUR FEED</div></div>
<img class="card" src="{cover_uri}">
<div class="bot">See the full post on our profile<span>@BATTLEVANA</span></div>
</div></body></html>"""
f = B / "_story.html"; f.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.screenshot(path=out); b.close()
print("ok", out)
