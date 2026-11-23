import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/combo_darkhold")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # example from a real post; card folder = BV_DIR

A, B = f"{DIR}/the-darkhold.jpg", f"{DIR}/platinum-angel.jpg"
BG = f"{DIR}/the-darkhold_art.jpg"

def head():
    return ('<div class="top"><div class="tag">NEW COMBO</div>'
            '<div class="set">Commander<small>Darkhold Destiny · 9 Apr 2027</small></div></div>')

plus = '<div style="font-family:Blanka;font-size:120px;color:#F14624;line-height:1">+</div>'

cover = page(head() +
    '<div style="position:absolute;top:190px;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:26px">'
    f'<img class="card" src="{A}" style="width:450px;transform:rotate(-4deg)">{plus}'
    f'<img class="card" src="{B}" style="width:450px;transform:rotate(4deg)"></div>'
    '<div class="bottom"><div><div class="name" style="font-size:56px">THE DARKHOLD<em>+ PLATINUM ANGEL</em></div>'
    '<div class="hook" style="font-size:27px;max-width:720px">Drain yourself below zero. Then drag every opponent down with you.</div></div>'
    f'{LOGO}</div>', bg=BG)

def step(n, title, text, thumb):
    return ('<div style="display:flex;gap:30px;align-items:center;background:rgba(0,27,46,.55);border:2px solid rgba(246,246,246,.12);border-radius:18px;padding:22px 30px">'
            f'<div style="font-family:Blanka;font-size:70px;color:#F14624;width:64px;text-align:center;flex-shrink:0">{n}</div>'
            f'<div style="flex:1"><div style="font-weight:800;font-size:33px;margin-bottom:10px">{title}</div>'
            f'<div style="font-size:28px;line-height:1.42;opacity:.92">{text}</div></div>'
            f'<img class="card" src="{thumb}" style="width:140px;flex-shrink:0;box-shadow:0 10px 24px rgba(0,0,0,.5)"></div>')

how = page(head() +
    '<div style="position:absolute;top:150px;left:64px;right:64px">'
    '<div class="name" style="font-size:56px;margin-bottom:24px">HOW IT WORKS</div>'
    '<div style="display:flex;flex-direction:column;gap:22px">' +
    step("1", "Get Platinum Angel on the battlefield", "You can't lose the game, even at 0 life or lower.", B) +
    step("2", "Tap The Darkhold, turn after turn", "Draw a card for each sin counter, then lose 1 life for each card in your hand. Keep going until your life is 0 or below.", A) +
    step("3", "Pay 6BB and tap The Darkhold", "Every player's life total becomes the lowest one: yours. Your opponents drop to 0 or less and lose the game.", A) +
    '</div></div>'
    f'<div style="position:absolute;right:64px;bottom:56px">{LOGO}</div>', bg=BG)

def item(t):
    return f'<li style="margin:0 0 30px;font-size:32px;line-height:1.45">{t}</li>'

good = page(head() +
    '<div style="position:absolute;top:150px;left:64px;right:64px">'
    '<div class="name" style="font-size:56px;margin-bottom:34px">GOOD TO KNOW</div>'
    '<ul style="margin:0;padding-left:30px">' +
    item('<b>Not instant.</b> Both Darkhold abilities need a tap and the finisher is sorcery speed, so the combo plays out over several turns.') +
    item('<b>Protect the Angel.</b> If Platinum Angel leaves the battlefield while you are at 0 or below, you lose immediately.') +
    item('<b>Backup plan.</b> Repay in Kind has the same effect as the finisher, giving the deck a second way to close.') +
    item('<b>Colors.</b> Mono-black plus a colorless artifact, so it fits any Commander deck with black in it.') +
    item('<b>When.</b> The Darkhold becomes legal when Marvel: Darkhold Destiny releases on 9 April 2027.') +
    '</ul></div>'
    f'<div style="position:absolute;right:64px;bottom:56px">{LOGO}</div>', bg=BG)

render([("01_cover", cover), ("02_how-it-works", how), ("03_good-to-know", good), ("04_outro-emjati", cta(["the-darkhold"]))])
