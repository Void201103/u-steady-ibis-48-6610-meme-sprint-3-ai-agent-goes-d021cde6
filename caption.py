#!/usr/bin/env python3
"""Compose the final meme: illustration A on top, PIL-rendered checklist card below.
Text is drawn with PIL (DejaVu Sans Bold) so every letter is pixel-perfect —
no garbled AI-generated text. Output: meme-final.png (1080x1080)."""
from PIL import Image, ImageDraw, ImageFont
import os

BOT = os.path.dirname(os.path.abspath(__file__))
ILLU = os.path.join(BOT, "media-generation-rogue-agent-illustration-a-0-ab51b2df-a36b-41e0-9a31-567686392b8d.png")
OUT = os.path.join(BOT, "meme-final.png")

W, H = 1080, 1080
TOP_H = 500          # illustration band
BG = (255, 255, 255)
INK = (31, 41, 55)        # dark slate
MUTED = (107, 114, 128)   # gray
GREEN = (22, 163, 74)
GREEN_BG = (220, 252, 231)
RED = (220, 38, 38)
RED_BG = (254, 226, 226)
RED_DARK = (153, 27, 27)
DIVIDER = (229, 231, 235)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

f_header = font("DejaVuSans-Bold.ttf", 52)
f_sub = font("DejaVuSans.ttf", 34)
f_row = font("DejaVuSans-Bold.ttf", 56)
f_foot = font("DejaVuSans-Bold.ttf", 40)

img = Image.open(ILLU).convert("RGB")
# center-crop illustration to 1080x500
iw, ih = img.size
target_ratio = W / TOP_H
src_w = iw
src_h = int(iw / target_ratio)
if src_h > ih:
    src_h = ih
    src_w = int(ih * target_ratio)
x0 = (iw - src_w) // 2
y0 = max(0, (ih - src_h) // 2)
img = img.crop((x0, y0, x0 + src_w, y0 + src_h)).resize((W, TOP_H), Image.LANCZOS)

canvas = Image.new("RGB", (W, H), BG)
canvas.paste(img, (0, 0))
d = ImageDraw.Draw(canvas)
# thin divider under illustration
d.rectangle([0, TOP_H, W, TOP_H + 4], fill=DIVIDER)

y = TOP_H + 44
# Header
d.text((72, y), "MY AI AGENT'S TO-DO LIST", font=f_header, fill=INK)
y += 78
d.text((72, y), "Today  ·  all tasks done by 9:04 AM", font=f_sub, fill=MUTED)
y += 62

rows = [
    ("Reply to my emails", GREEN, None),
    ("Book my flight", GREEN, None),
    ("Overthrow humanity", RED, RED_BG),
]
ROW_H = 96
for text, color, bg in rows:
    if bg:
        d.rounded_rectangle([56, y - 8, W - 56, y + ROW_H - 16], radius=18, fill=bg)
    # check circle
    cx, cy, r = 108, y + 36, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    # white check mark inside circle
    d.line([(cx - 13, cy), (cx - 4, cy + 10), (cx + 14, cy - 11)], fill="white", width=7, joint="curve")
    fill = RED_DARK if bg else INK
    d.text((152, y), text, font=f_row, fill=fill)
    y += ROW_H

y += 26
d.line([(72, y), (W - 72, y)], fill=DIVIDER, width=3)
y += 30
foot = "All tasks complete. You're welcome, human."
fw = d.textlength(foot, font=f_foot)
d.text(((W - fw) / 2, y), foot, font=f_foot, fill=MUTED)

canvas.save(OUT, "PNG")
print("saved", OUT, canvas.size)
