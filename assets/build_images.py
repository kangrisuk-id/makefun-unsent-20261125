#!/usr/bin/env python3
"""Build-time image renderer for the Unsent entry README.

Runs locally at build time only (Pillow). The submitted entrypoint
(main.py) never imports Pillow — it is pure stdlib.
Outputs: cover.png, card-draft.png, card-tournament.png, card-criteria.png
(all 1280x800, in the repo root, referenced by README via relative paths).
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BG = (18, 18, 22)          # deep charcoal
PANEL = (32, 32, 40)
PANEL_LINE = (72, 72, 88)
GOLD = (201, 162, 75)
TEXT = (235, 235, 228)
MUTED = (158, 158, 148)
GREEN = (110, 200, 130)
RED = (220, 110, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def base():
    img = Image.new("RGB", (1280, 800), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 6], fill=GOLD)
    return img, d


def footer(d, text):
    f = font(SANS, 22)
    d.text((64, 748), text, font=f, fill=MUTED)


def cover():
    img, d = base()
    d.text((64, 56), "UNSENT", font=font(SERIF_B, 92), fill=TEXT)
    d.text((64, 158), "the micro-confession that stayed in drafts",
           font=font(SERIF, 34), fill=MUTED)
    # phone draft card
    d.rounded_rectangle([64, 250, 1216, 620], radius=28, fill=PANEL,
                        outline=PANEL_LINE, width=2)
    d.text((110, 292), "To: Alex", font=font(SANS_B, 44), fill=GOLD)
    d.text((110, 352), "Draft  ·  never sent", font=font(SANS, 28), fill=MUTED)
    d.line([110, 408, 1170, 408], fill=PANEL_LINE, width=2)
    msg = ("I almost told you I loved you on the last night of the trip. "
           "I said 'drive safe' instead.")
    lines = wrap(d, msg, font(SERIF, 40), 1060)
    y = 440
    for ln in lines:
        d.text((110, y), ln, font=font(SERIF, 40), fill=TEXT)
        y += 56
    d.text((64, 680), "98 characters  ·  2 parts  ·  1 unsent line",
           font=font(SANS, 26), fill=MUTED)
    img.save(os.path.join(ROOT, "cover.png"))


def card_draft():
    img, d = base()
    d.text((64, 56), "The draft, exactly as typed",
           font=font(SERIF_B, 54), fill=TEXT)
    d.rounded_rectangle([64, 170, 1216, 560], radius=28, fill=PANEL,
                        outline=PANEL_LINE, width=2)
    d.text((110, 210), "To: Alex", font=font(SANS_B, 42), fill=GOLD)
    d.line([110, 280, 1170, 280], fill=PANEL_LINE, width=2)
    msg = ("I almost told you I loved you on the last night of the trip. "
           "I said 'drive safe' instead.")
    lines = wrap(d, msg, font(SERIF, 38), 1060)
    y = 310
    for ln in lines:
        d.text((110, y), ln, font=font(SERIF, 38), fill=TEXT)
        y += 54
    d.text((110, 500), "No explanation after it. No send button pressed.",
           font=font(SANS, 26), fill=MUTED)
    footer(d, "entry.txt — 98 characters, no trailing newline")
    img.save(os.path.join(ROOT, "card-draft.png"))


def card_tournament():
    img, d = base()
    d.text((64, 56), "How the line was chosen",
           font=font(SERIF_B, 54), fill=TEXT)
    d.text((64, 130), "30 candidates  ·  8 devices  ·  scored on the judge brief, in order",
           font=font(SANS, 28), fill=MUTED)
    stages = [
        ("30", "candidates drafted", TEXT),
        ("8", "seeds, scored 1-5 per criterion", TEXT),
        ("4", "quarter-finalists", TEXT),
        ("2", "finalists: #13 vs #9", TEXT),
        ("1", "winner: 'drive safe' not 'I love you'", GOLD),
    ]
    x = 64
    for i, (num, label, col) in enumerate(stages):
        d.rounded_rectangle([x, 240, x + 200, 480], radius=20, fill=PANEL,
                            outline=PANEL_LINE, width=2)
        d.text((x + 100, 280), num, font=font(SERIF_B, 72), fill=col, anchor="mt")
        label_lines = wrap(d, label, font(SANS, 20), 176)
        yy = 392
        for ln in label_lines:
            d.text((x + 100, yy), ln, font=font(SANS, 20), fill=MUTED, anchor="mt")
            yy += 28
        if i < len(stages) - 1:
            d.text((x + 200, 330), "  ›  ", font=font(SANS_B, 44), fill=GOLD)
        x += 224
    d.text((64, 560), "Self-pairwise: the winner beat both runners-up (#9, #18) on the",
           font=font(SANS, 28), fill=TEXT)
    d.text((64, 600), "brief's criteria in order — no early-criterion loss.",
           font=font(SANS, 28), fill=TEXT)
    footer(d, "Full bracket and scores: candidates.md")
    img.save(os.path.join(ROOT, "card-tournament.png"))


def card_criteria():
    img, d = base()
    d.text((64, 56), "Five brief criteria, all covered",
           font=font(SERIF_B, 54), fill=TEXT)
    rows = [
        ("1", "Two parts — To: line + the message itself", True),
        ("2", "Reason felt, not stated — too afraid, too late", True),
        ("3", "To: and message need each other — swap Alex, it breaks", True),
        ("4", "Reads as typed and never sent — plain speech, no joke", True),
        ("5", "One line, exactly as typed — no explanation after it", True),
    ]
    y = 170
    for num, label, ok in rows:
        d.rounded_rectangle([64, y, 1216, y + 88], radius=16, fill=PANEL,
                            outline=PANEL_LINE, width=2)
        d.text((96, y + 44), num, font=font(SERIF_B, 40), fill=GOLD, anchor="lm")
        d.text((160, y + 44), label, font=font(SANS, 30), fill=TEXT, anchor="lm")
        d.text((1150, y + 44), "✓", font=font(SANS_B, 40),
               fill=GREEN if ok else RED, anchor="mm")
        y += 108
    footer(d, "Judge brief, published in the kit's RULES.txt — criteria in order")
    img.save(os.path.join(ROOT, "card-criteria.png"))


if __name__ == "__main__":
    cover()
    card_draft()
    card_tournament()
    card_criteria()
    print("images written to", ROOT)
