import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards-godpack"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/godpack")
os.environ.setdefault("BV_FORMAT", "special")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # special post: God Packs in Nauctis (source: Wizards "Collecting Nauctis: The Sunken Realm", 13 Nov 2026)

ICON = "assets/logo_white_crop.png"
CARD = f"{DIR}/god-pack-celebration-card.jpg"

def head(tag="GOD PACKS"):
    return (f'<div class="top"><div class="tag">{tag}</div>'
            '<div class="set">Nauctis<small>The Sunken Realm</small></div></div>')

def glow_bg():
    return ('<div style="position:absolute;inset:0;background:'
            'radial-gradient(circle at 78% 30%, rgba(241,70,36,.28), rgba(241,70,36,0) 45%),'
            'radial-gradient(circle at 15% 85%, rgba(241,70,36,.16), rgba(241,70,36,0) 40%)"></div>')

def item(text):
    return ('<div style="display:flex;gap:16px;align-items:flex-start">'
            '<div style="width:12px;height:12px;border-radius:50%;background:#F14624;margin-top:13px;flex-shrink:0"></div>'
            f'<div style="font-size:26px;line-height:1.38">{e(text)}</div></div>')

def box(title, odds, items):
    return ('<div style="background:rgba(0,27,46,.5);border:2px solid rgba(246,246,246,.14);border-radius:16px;padding:32px 34px">'
            f'<div class="name" style="font-size:52px;line-height:1">{title}</div>'
            f'<div style="font-size:30px;font-weight:800;color:#F14624;margin-top:14px">{e(odds)}</div>'
            '<div style="display:flex;flex-direction:column;gap:10px;margin-top:20px">' + "".join(item(i) for i in items) + '</div></div>')

cover = page(glow_bg() + head() +
    '<div style="position:absolute;right:-30px;top:230px;width:640px;height:900px;border-radius:50%;background:radial-gradient(closest-side, rgba(241,70,36,.35), rgba(241,70,36,0))"></div>'
    f'<img class="card" src="{CARD}" style="position:absolute;right:90px;top:300px;width:470px;transform:rotate(6deg)">'
    '<div style="position:absolute;left:64px;top:300px;width:470px">'
    '<div class="hook" style="font-size:30px;font-weight:700;letter-spacing:3px;opacity:.8;margin:0">NEW IN NAUCTIS</div>'
    '<div class="name" style="font-size:150px;line-height:1;color:#F14624;margin-top:16px">GOD</div>'
    '<div class="name" style="font-size:150px;line-height:1">PACKS</div>'
    '<div class="hook" style="font-size:36px;margin-top:40px;line-height:1.35">A booster where every nonbasic card is a rare or mythic rare.</div></div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:150px">')

odds = page(glow_bg() + head() +
    '<div style="position:absolute;left:64px;right:64px;top:190px">'
    '<div class="name" style="font-size:80px;line-height:1">WHAT IS INSIDE</div>'
    '<div class="hook" style="font-size:30px;max-width:920px;margin-top:20px;line-height:1.35">Starting with Nauctis, God Packs can show up in Booster Packs and Collector Boosters.</div>'
    '<div style="display:flex;flex-direction:column;gap:26px;margin-top:38px">'
    + box("BOOSTER GOD PACK", "About 1 in 1,000 Booster Packs",
          ["1 God Pack celebration card", "10 non-foil rares and/or mythic rares",
           "2 non-foil Booster Fun rares and/or mythic rares", "2 traditional foil Booster Fun rares and/or mythic rares"])
    + box("COLLECTOR GOD PACK", "About 1 in 300 Collector Boosters",
          ["1 God Pack celebration card", "1 foil land", "3 foil rares and/or mythic rares",
           "3 non-foil Booster Fun rares and/or mythic rares", "5 foil Booster Fun rares and/or mythic rares"])
    + '</div></div>'
    f'<img src="{ICON}" style="position:absolute;right:64px;bottom:56px;width:120px">')

celebrate = page(glow_bg() + head("YOU DID IT") +
    '<div style="position:absolute;right:-20px;bottom:0;width:640px;height:960px;border-radius:50%;background:radial-gradient(closest-side, rgba(241,70,36,.35), rgba(241,70,36,0))"></div>'
    '<img src="vana/vana_laugh.png" style="position:absolute;right:-20px;bottom:0;height:900px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))">'
    f'<img class="card" src="{CARD}" style="position:absolute;right:300px;bottom:70px;width:360px;transform:rotate(-9deg)">'
    '<div style="position:absolute;left:64px;top:210px;width:490px">'
    '<div class="name" style="font-size:84px;line-height:1.02">HOW YOU<br>KNOW</div>'
    '<div class="hook" style="font-size:34px;margin-top:30px;line-height:1.38">Every God Pack comes with a God Pack celebration card.</div>'
    '<div style="margin-top:34px;font-size:30px;font-style:italic;line-height:1.4;opacity:.9">"Get out the toploaders, you opened a God Pack."</div></div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:130px">')

slides = [
 ("01_cover", cover),
 ("02_whats-inside", odds),
 ("03_celebration-card", celebrate),
 ("04_outro-emjati", cta(["god-pack-celebration-card"])),
]
render(slides)
