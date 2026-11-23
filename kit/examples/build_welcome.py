import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/welcome")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # example from a real post; card folder = BV_DIR

ICON = "assets/logo_white_crop.png"

def head(tag="WELCOME"):
    return (f'<div class="top"><div class="tag">{tag}</div>'
            '<div class="set">BattleVana<small>battlevana.be</small></div></div>')

def glow_bg():
    return ('<div style="position:absolute;inset:0;background:'
            'radial-gradient(circle at 78% 22%, rgba(241,70,36,.28), rgba(241,70,36,0) 45%),'
            'radial-gradient(circle at 15% 85%, rgba(241,70,36,.16), rgba(241,70,36,0) 40%)"></div>')

def chips(items):
    return ('<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:40px">' + "".join(
        f'<div style="border:2px solid rgba(246,246,246,.25);border-radius:14px;padding:20px 26px;font-size:30px;font-weight:700;background:rgba(0,27,46,.45)">{e(i)}</div>'
        for i in items) + '</div>')

def block(title, intro, items, extra=""):
    return (f'<div><div class="name" style="font-size:76px;line-height:1">{title}</div>'
            f'<div class="hook" style="font-size:34px;max-width:920px;margin-top:22px;line-height:1.35">{e(intro)}</div>'
            f'{chips(items)}{extra}</div>')

def duo(a, b, vana):
    body = (glow_bg() + head() +
            f'<img src="vana/{vana}" style="position:absolute;right:-90px;bottom:0;height:740px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))">'
            '<div style="position:absolute;left:64px;right:400px;top:190px;bottom:170px;display:flex;flex-direction:column;justify-content:space-between">'
            f'{a}<div style="height:3px;width:140px;background:#F14624"></div>{b}</div>'
            f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:130px">')
    return page(body)

def section(title, intro, items, extra=""):
    body = (glow_bg() + head() +
            '<div style="position:absolute;left:64px;right:64px;top:300px">'
            f'<div class="name" style="font-size:92px;line-height:1">{title}</div>'
            f'<div class="hook" style="font-size:36px;max-width:900px;margin-top:28px;line-height:1.35">{e(intro)}</div>'
            f'{chips(items)}{extra}</div>'
            f'<div style="position:absolute;right:64px;bottom:56px">{LOGO}</div>')
    return page(body)

cover = page(glow_bg() + head() +
    '<div style="position:absolute;right:-30px;top:250px;width:600px;height:900px;border-radius:50%;background:radial-gradient(closest-side, rgba(241,70,36,.35), rgba(241,70,36,0))"></div>'
    '<img src="vana/vana_full.png" style="position:absolute;right:-70px;bottom:30px;height:1120px;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55))">'
    '<div style="position:absolute;left:64px;top:270px;width:470px">'
    '<div class="name" style="font-size:92px;line-height:1.02">WELCOME<br>TO</div><div class="name" style="font-size:78px;line-height:1.1;color:#F14624">BATTLEVANA</div>'
    '<div class="hook" style="font-size:34px;margin-top:34px;line-height:1.35">Tools and community for Belgian Magic players</div>'
    '<div style="margin-top:44px;font-size:28px;font-style:italic;line-height:1.4;opacity:.85">"Pull up a chair. The first duel is always the best one."</div>'
    '<div style="margin-top:10px;font-size:22px;font-weight:700;letter-spacing:2px;color:#F14624">VANA, THE GATHERER OF PLANES</div></div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:150px">')

feed = page(glow_bg() + head() +
    '<img src="vana/vana_wink.png" style="position:absolute;right:-10px;bottom:0;height:400px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))">'
    '<div style="position:absolute;left:64px;right:64px;top:240px">'
    '<div class="name" style="font-size:92px;line-height:1">ON THIS FEED</div>'
    '<div class="hook" style="font-size:36px;margin-top:28px">Follow along for</div>'
    '<div style="display:flex;flex-direction:column;gap:28px;margin-top:44px">' + "".join(
      f'<div style="display:flex;align-items:center;gap:26px;background:rgba(0,27,46,.5);border:2px solid rgba(246,246,246,.14);border-radius:16px;padding:36px 32px">'
      f'<div style="background:{c};color:{tc};font-family:Blanka;font-size:30px;letter-spacing:3px;padding:12px 20px 8px;border-radius:6px;flex-shrink:0">{t}</div>'
      f'<div style="font-size:32px;line-height:1.35">{d}</div></div>'
      for t, c, tc, d in [
        ("NEW SPOILERS", "#F24624", "#fff", "The newest cards, the moment they are revealed."),
        ("BEHIND THE CARD", "#8FFE07", "#001B2E", "The real stories behind famous Magic cards."),
        ("NEW COMBO", "#C9A127", "#001B2E", "Fresh combos with brand new cards."),
      ]) + '</div></div>'
    f'<img src="{ICON}" style="position:absolute;left:64px;bottom:56px;width:130px">')

slides = [
 ("01_cover", cover),
 ("02_cards-and-play", duo(block("CARDS", "Look up any card, see new spoilers, browse sets and keywords.", ["Card Vault", "Spoilers", "Sets", "Mechanics"]),
                              block("PLAY", "Print proxies, keep life totals, crack virtual boosters.", ["Proxy Printer", "Life Counter", "Booster Sim"]), "vana_smile.png")),
 ("03_formats-and-events", duo(block("FORMATS AND DECKS", "How each format works, with the decks that define it.", ["Premodern", "Legacy", "Modern", "Deck archive"]),
                              block("EVENTS", "Our tournaments, results and every decklist.", ["All events", "Results and decklists"],
    '<div style="margin-top:34px;font-size:24px;font-weight:700;letter-spacing:2px;opacity:.75">COMING SOON</div>'
    '<div style="font-size:30px;margin-top:8px">Draft Sim, Sealed Builder, Playtester, Price Watch</div>'), "vana_thinking.png")),
 ("04_on-this-feed", feed),
 ("05_outro-emjati", cta(["none"])),
]
render(slides)
