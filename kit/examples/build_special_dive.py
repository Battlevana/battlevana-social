import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards-none"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/dive")
os.environ.setdefault("BV_FORMAT", "special")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # special post: Nauctis mechanic explainer (no card images, no Dive cards previewed yet)

ICON = "assets/logo_white_crop.png"

def head(tag="NEW MECHANIC"):
    return (f'<div class="top"><div class="tag">{tag}</div>'
            '<div class="set">Nauctis<small>The Sunken Realm</small></div></div>')

def glow_bg():
    return ('<div style="position:absolute;inset:0;background:'
            'radial-gradient(circle at 78% 22%, rgba(241,70,36,.28), rgba(241,70,36,0) 45%),'
            'radial-gradient(circle at 15% 85%, rgba(241,70,36,.16), rgba(241,70,36,0) 40%)"></div>')

def step(n, title, text):
    return ('<div style="display:flex;gap:30px;align-items:flex-start;background:rgba(0,27,46,.5);border:2px solid rgba(246,246,246,.14);border-radius:16px;padding:30px 32px">'
            f'<div style="font-family:Blanka;font-size:64px;line-height:1;color:#F14624;width:60px;flex-shrink:0">{n}</div>'
            f'<div><div style="font-size:34px;font-weight:800">{e(title)}</div>'
            f'<div style="font-size:28px;line-height:1.38;margin-top:8px;opacity:.9">{e(text)}</div></div></div>')

def fact(text):
    return ('<div style="display:flex;gap:22px;align-items:flex-start">'
            '<div style="width:16px;height:16px;border-radius:50%;background:#F14624;margin-top:15px;flex-shrink:0"></div>'
            f'<div style="font-size:31px;line-height:1.4">{text}</div></div>')

cover = page(glow_bg() + head() +
    '<div style="position:absolute;right:-30px;top:250px;width:600px;height:900px;border-radius:50%;background:radial-gradient(closest-side, rgba(241,70,36,.35), rgba(241,70,36,0))"></div>'
    '<img src="vana/vana_thinking.png" style="position:absolute;right:-90px;bottom:30px;height:1040px;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55))">'
    '<div style="position:absolute;left:64px;top:300px;width:520px">'
    '<div class="hook" style="font-size:30px;font-weight:700;letter-spacing:3px;opacity:.8;margin:0">MEET THE NEW</div>'
    '<div class="name" style="font-size:96px;line-height:1.05;margin-top:12px">EVASION</div>'
    '<div class="name" style="font-size:190px;line-height:1;color:#F14624;margin-top:10px">DIVE</div>'
    '<div class="hook" style="font-size:36px;margin-top:40px;line-height:1.35;max-width:520px">There is no flying in Nauctis. Dive takes its place.</div></div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:150px">')

how = page(glow_bg() + head() +
    '<div style="position:absolute;left:64px;right:64px;top:210px">'
    '<div class="name" style="font-size:88px;line-height:1">HOW DIVE WORKS</div>'
    '<div class="hook" style="font-size:34px;max-width:900px;margin-top:24px;line-height:1.35">A creature with Dive can\'t be blocked. Once it deals combat damage, it loses Dive.</div>'
    '<div style="display:flex;flex-direction:column;gap:24px;margin-top:46px">'
    + step("1", "Attack", "Your creature with Dive attacks. It can't be blocked.")
    + step("2", "Hit", "Unblocked, it deals its combat damage.")
    + step("3", "Surface", "Dive is gone. From now on it can be blocked as normal.")
    + '</div>'
    '<div style="font-size:24px;line-height:1.4;margin-top:34px;opacity:.7">First seen in early Commander Party event material. Exact card wording is not official yet.</div>'
    '</div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:130px">')

know = page(glow_bg() + head("GOOD TO KNOW") +
    '<img src="vana/vana_smile.png" style="position:absolute;right:-60px;bottom:0;height:560px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))">'
    '<div style="position:absolute;left:64px;right:64px;top:230px">'
    '<div class="name" style="font-size:88px;line-height:1">GOOD TO KNOW</div>'
    '<div style="display:flex;flex-direction:column;gap:34px;margin-top:54px;max-width:900px">'
    + fact("No new cards with flying in Nauctis. The last set without flying was Portal Three Kingdoms (1999).")
    + fact("Flying is not gone from Magic. Your older flyers stay playable.")
    + fact("No cards with Dive have been previewed yet. We post them as soon as they are.")
    + '</div>'
    '<div style="margin-top:60px;max-width:560px">'
    '<div style="font-size:24px;font-weight:700;letter-spacing:3px;color:#F14624">NAUCTIS: THE SUNKEN REALM</div>'
    '<div style="font-size:30px;line-height:1.45;margin-top:12px">Prerelease from 29 January<br>Release 5 February 2027</div></div>'
    '</div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:130px">')

slides = [
 ("01_cover", cover),
 ("02_how-it-works", how),
 ("03_good-to-know", know),
 ("04_outro-emjati", cta(["none"])),
]
render(slides)
