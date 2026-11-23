import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/btc_shahrazad")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # example from a real post; card folder = BV_DIR

CARD = f"{DIR}/shahrazad.png"
RIGHT = ("Shahrazad", "Arabian Nights · 1993")

def head():
    return (f'<div class="top"><div class="tag">BEHIND THE CARD</div>'
            f'<div class="set">{e(RIGHT[0])}<small>{e(RIGHT[1])}</small></div></div>')

def crop(x, y, size, h=470):
    return (f'<div style="width:100%;height:{h}px;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.6);'
            f'background:url({CARD}) -{x}px -{y}px/{size}px no-repeat"></div>')

def story(title, paras, visual, top=680):
    ps = "".join(f'<p style="margin:0 0 22px;font-size:29px;line-height:1.42">{p}</p>' for p in paras)
    body = (head() + f'<div style="position:absolute;top:150px;left:64px;right:64px">{visual}</div>'
            f'<div style="position:absolute;left:64px;right:64px;top:{top}px">'
            f'<div class="name" style="font-size:52px;margin-bottom:26px">{title}</div>{ps}</div>'
            f'<div style="position:absolute;right:64px;bottom:56px">{LOGO}</div>')
    return page(body, bg=f"{DIR}/shahrazad_art.jpg")

cover = page(head() +
    f'<img class="card" src="{CARD}" style="position:absolute;left:50%;top:150px;transform:translateX(-50%) rotate(-3deg);width:610px">'
    '<div class="bottom"><div><div class="name" style="font-size:72px">SHAHRAZAD</div>'
    '<div class="hook" style="font-size:27px;max-width:720px">The card that pauses your game of Magic so you can play another game of Magic.</div></div>'
    f'{LOGO}</div>', bg=f"{DIR}/shahrazad_art.jpg")

# nested games visual
nested = ('<div style="height:470px;display:flex;align-items:center;justify-content:center">'
  '<div style="width:900px;height:430px;border:3px solid rgba(246,246,246,.55);border-radius:22px;padding:22px 26px;position:relative">'
  '<div style="font-family:Blanka;font-size:30px;letter-spacing:2px">YOUR GAME</div>'
  '<div style="position:absolute;left:90px;right:90px;top:80px;bottom:26px;border:3px solid #F14624;border-radius:18px;padding:20px 24px;background:rgba(241,70,36,.08)">'
  '<div style="font-family:Blanka;font-size:28px;letter-spacing:2px;color:#F14624">SUBGAME</div>'
  '<div style="position:absolute;left:80px;right:80px;top:76px;bottom:24px;border:3px dashed rgba(246,246,246,.6);border-radius:14px;padding:18px 22px">'
  '<div style="font-family:Blanka;font-size:24px;letter-spacing:2px">SUB-SUBGAME</div>'
  '<div style="position:absolute;left:60px;right:60px;top:66px;bottom:20px;border:3px dashed rgba(241,70,36,.7);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700;letter-spacing:8px;opacity:.85">. . .</div>'
  '</div></div></div></div>')

banned = ('<div style="height:470px;position:relative;display:flex;align-items:center;justify-content:center">'
  f'<img class="card" src="{CARD}" style="width:320px;transform:rotate(-4deg);filter:saturate(.6) brightness(.85)">'
  '<div style="position:absolute;transform:rotate(-12deg);border:6px solid #F14624;color:#F14624;font-family:Blanka;font-size:76px;letter-spacing:6px;padding:10px 34px 4px;background:rgba(0,27,46,.82);border-radius:8px">BANNED</div></div>')

rule = ('<div style="height:470px;display:flex;align-items:center">'
  '<div style="width:100%;background:rgba(246,246,246,.95);color:#001B2E;border-radius:18px;padding:44px 50px;box-shadow:0 24px 60px rgba(0,0,0,.6)">'
  '<div style="font-size:20px;font-weight:700;letter-spacing:3px;color:#F14624">MAGIC COMPREHENSIVE RULES</div>'
  '<div style="font-size:64px;font-weight:800;margin:10px 0 18px">728. Subgames</div>'
  '<div style="font-size:30px;line-height:1.4">728.1. One card (Shahrazad) allows players to play a Magic subgame.</div></div></div>')

slides = [
 ("01_cover", cover),
 ("02_a-story-within-a-story", story("A STORY WITHIN A STORY", [
   "Arabian Nights, Magic's very first expansion, arrived in December 1993, inspired by the tales of One Thousand and One Nights.",
   "In those tales, Shahrazad survives by telling stories within stories. Richard Garfield loved the idea and turned it into a card: a game within the game.",
 ], crop(130, 302, 1212))),
 ("03_how-it-works", story("HOW IT WORKS", [
   "Both players pause the game and start a brand new game of Magic, using the rest of their libraries as decks.",
   "Whoever loses that subgame loses half their life in the real game. And yes, you can cast Shahrazad inside the subgame.",
 ], nested)),
 ("04_banned", story("BANNED FROM DAY ONE", [
   "Shahrazad was hit in the very first banned list in Magic's history, in January 1994, the only card banned that wasn't an ante card.",
   "It never came back. It is still banned in Legacy and Vintage, and it was one of the first cards on the Commander banned list.",
 ], banned)),
 ("05_still-in-the-rules", story("STILL IN THE RULEBOOK", [
   "No black-bordered card has done it since. Yet the official rules still contain a full section on subgames, and it opens by naming this one card.",
   "In 2018 Kaja Foglio's original painting sold at auction for around 55,000 pounds.",
 ], rule)),
 ("06_outro-emjati", cta(["shahrazad"])),
]
render(slides)
