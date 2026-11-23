import os
os.environ.setdefault("BV_DIR", "/tmp/bv-cards"); os.environ.setdefault("BV_OUT", "/tmp/bv-out/big")
os.environ.update(BV_SET="Nauctis · Darkhold Destiny", BV_RELEASE="Feb & Apr 2027")
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bvpost import *  # example from a real post; card folder = BV_DIR
heroes = {
 "hela-mistress-of-darkness": "Every point of life lost on your turn becomes Zombies. Flip side: a graveyard tutor. Mono-black Commander material.",
 "magik-illyana-rasputin": "Impulse draw every upkeep, then transforms into a demon when you sacrifice two permanents. Rakdos aristocrats, assemble.",
 "the-darkhold": "Draw more each turn, pay for it with life... then reset everyone's life to the lowest total. Pure chaos in a book.",
}
groups = [
 ("NEW LEGENDS", ["gargantos-the-endbringer","goramou-the-coral-taken","salinae-the-ocean-mother","tecton-malignant-ruin","the-ignoble-serpent"], "Commander picks"),
 ("SPELLS & CREATURES", ["hela-s-arcanum","penance-stare","rise-from-the-nether","calmwater-mentor"], ""),
 ("ARTIFACTS & LANDS", ["abyssal-lotus","ring-of-unity","crucible-of-worlds","temple-of-khonshu","shimmering-citadel"], ""),
 ("NEW BASIC LANDS", ["plains","island","swamp","mountain","forest"], "Darkhold Destiny art"),
]
H = list(heroes); total = 1 + len(H) + len(groups) + 1
n = len(H) + sum(len(g[1]) for g in groups)
slides = [("01_cover", cover(H, f"{n} NEW SPOILERS", "Three highlights and four roundups. Swipe through everything spoiled this week."))]
i = 2
for s in H: slides.append((f"{i:02d}_{s}", hero(s, heroes[s], i, total))); i += 1
for label, sl, sub in groups: slides.append((f"{i:02d}_roundup", grid2(sl, label, i, total, sub))); i += 1
slides.append((f"{i:02d}_cta", cta(H, i, total)))
render(slides)
