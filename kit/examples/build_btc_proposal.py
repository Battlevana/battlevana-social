import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/btc_proposal")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # example from a real post; card folder = BV_DIR

CARD, ART = f"{DIR}/proposal.png", f"{DIR}/proposal_art.jpg"

def head(right_main, right_sub):
    return (f'<div class="top"><div class="tag">BEHIND THE CARD</div>'
            f'<div class="set">{e(right_main)}<small>{e(right_sub)}</small></div></div>')

def cover_slide():
    body = (head("Proposal", "Celebration card · 1993") +
            f'<img class="card" src="{CARD}" style="position:absolute;left:50%;top:150px;transform:translateX(-50%) rotate(-3deg);width:610px">'
            '<div class="bottom"><div><div class="name" style="font-size:72px">PROPOSAL</div>'
            '<div class="hook" style="font-size:27px;max-width:720px">The one Magic card that was played to ask a question: will you marry me?</div></div>'
            f'{LOGO}</div>')
    return page(body, bg=ART)

def story_slide(step, title, paras, visual):
    ps = "".join(f'<p style="margin:0 0 22px;font-size:29px;line-height:1.42">{p}</p>' for p in paras)
    body = (head("Proposal", "Celebration card · 1993") +
            f'<div style="position:absolute;top:150px;left:64px;right:64px">{visual}</div>'
            f'<div style="position:absolute;left:64px;right:64px;top:{step}px">'
            f'<div class="name" style="font-size:52px;margin-bottom:26px">{title}</div>{ps}</div>'
            f'<div style="position:absolute;right:64px;bottom:56px">{LOGO}</div>')
    return page(body, bg=ART)

art_panel = f'<div style="width:100%;height:470px;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.6);background:url({CARD}) -110px -230px/1172px no-repeat"></div>'
hands_panel = f'<div style="width:100%;height:470px;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.6);background:url({CARD}) -209px -240px/1416px no-repeat"></div>'
fan_panel = ('<div style="position:relative;height:470px">' + "".join(
    f'<img class="card" src="{CARD}" style="position:absolute;width:300px;left:{316+dx}px;top:{dy}px;transform:rotate({r}deg)">'
    for dx, dy, r in [(-230, 40, -14), (230, 40, 14), (0, 0, 0)]) + '</div>')
text_panel = ('<div style="display:flex;gap:40px;align-items:center">'
              f'<img class="card" src="{CARD}" style="width:330px;transform:rotate(-2deg)">'
              '<div style="font-size:26px;line-height:1.45;opacity:.95;font-style:italic">"Allows Richard to propose marriage to Lily. If the proposal is accepted both players win; mix the cards in play, both libraries, and both graveyards as a shared deck."'
              '<div style="font-style:normal;font-size:20px;font-weight:700;letter-spacing:2px;color:#F14624;margin-top:16px">SORCERY · FOUR WHITE MANA</div></div></div>')

slides = [
 ("01_cover", cover_slide()),
 ("02_the-question", story_slide(680, "OCTOBER 1993", [
   "Richard Garfield had just launched Magic: The Gathering and was still teaching math at Whitman College.",
   "He wanted to propose to his girlfriend Lily Wu, and he wanted to do it with the game he had created.",
 ], art_panel)),
 ("03_the-card", story_slide(680, "NINE HANDMADE COPIES", [
   "Wizards production manager Dave Howell built the card by hand. The art came from Quinton Hoover, Lily's favourite Magic artist.",
   "No printing press: the image was printed, framed and glued onto real Magic cards. Nine copies on a single sheet.",
 ], text_panel)),
 ("04_the-game", story_slide(680, "THE GAME", [
   "Richard slipped the card into an all-white deck and challenged Lily. Three games went by without drawing it.",
   "In the fourth game he was losing badly. Lily, a playtester herself, suggested he concede. He played on.",
   "Then he cast Proposal.",
   "<b style=\"color:#F14624\">She said yes.</b>",
 ], hands_panel)),
 ("05_today", story_slide(680, "WHERE ARE THEY NOW", [
   "Proposal is one of the rarest Magic cards in existence. Most copies went to family.",
   "Quinton Hoover's own copy was stolen during a trip to Japan. Dave Howell kept his in a safe for years and sold it in 2019, to a collector believed to live in Europe.",
   "Somewhere out there, one of the rarest cards ever made might be closer than you think.",
 ], fan_panel)),
 ("06_outro-emjati", cta(["proposal"])),
]
render(slides)
