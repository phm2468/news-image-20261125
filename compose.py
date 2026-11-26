#!/usr/bin/env python3
"""Compose the 1024x1024 front-page news image for 25 November 2026.

Layout: masthead, one main photo with headline, three panels with
headlines, and a bottom ticker strip. All text is drawn here so every
headline is crisp and spelled exactly as written.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (16, 18, 22)
WHITE = (245, 245, 240)
GREY = (170, 175, 182)
RED = (200, 40, 40)
GOLD = (232, 197, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

ASSETS = "assets"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, box_w, box_h):
    """Resize+center-crop img to exactly box_w x box_h."""
    scale = max(box_w / img.width, box_h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)))
    x = (img.width - box_w) // 2
    y = (img.height - box_h) // 2
    return img.crop((x, y, x + box_w, y + box_h))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def main():
    canvas = Image.new("RGB", (W, W), BG)
    d = ImageDraw.Draw(canvas)

    # Masthead
    d.text((W // 2, 26), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 54),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 100), "WEDNESDAY · 25 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=GOLD, anchor="ma")
    d.line([(32, 142), (W - 32, 142)], fill=RED, width=4)

    # Main story: Hormuz
    main_img = Image.open(f"{ASSETS}/media-generation-news-hormuz-0-21ac0ab2-c058-4301-ab64-626738cec24a.webp").convert("RGB")
    canvas.paste(cover(main_img, W - 64, 400), (32, 158))
    d.rectangle([(32, 470), (W - 32, 558)], fill=(0, 0, 0))
    d.text((48, 482), "TANKERS BURN IN THE STRAIT OF HORMUZ", font=font(SANS_B, 37), fill=WHITE)
    d.text((48, 528), "Two oil tankers hit mines and explode in the world's key oil chokepoint",
           font=font(SANS, 21), fill=GREY)

    # Three panels
    panels = [
        ("media-generation-news-riyadh-0-9c14644a-ff0f-480b-8d60-9b6440bf3507.webp",
         "RIYADH TOWER HIT AGAIN",
         "Houthi strike on the capital's tallest tower injures 11; Ras Tanura refinery also hit"),
        ("media-generation-news-gaza-0-d4524f56-3593-423c-ab88-7b56bc0c2bd4.webp",
         "HAMAS SECURITY CHIEF KILLED IN GAZA",
         "Israeli airstrike kills Mohammad Abuelouf, his wife and daughters"),
        ("media-generation-news-odesa-0-5de1fc96-493b-47a2-97ef-281431951870.webp",
         "ODESA HIT; 490,334 RUSSIAN DEAD",
         "Strike kills 2, Kyiv flats burn; leaked data counts Russia's war dead"),
    ]
    pw = (W - 64 - 2 * 16) // 3
    x = 32
    for fname, head, sub in panels:
        img = Image.open(f"{ASSETS}/{fname}").convert("RGB")
        canvas.paste(cover(img, pw, 190), (x, 574))
        y = 774
        for line in wrap(d, head, font(SANS_B, 24), pw):
            d.text((x, y), line, font=font(SANS_B, 24), fill=WHITE)
            y += 29
        y += 4
        for line in wrap(d, sub, font(SANS, 17), pw):
            d.text((x, y), line, font=font(SANS, 17), fill=GREY)
            y += 21
        x += pw + 16

    # Bottom ticker
    d.line([(32, 952), (W - 32, 952)], fill=RED, width=3)
    d.text((W // 2, 966), "CLIMATE TALKS FAIL AT COP31  ·  POPE LEO XIV 'CONCERNED'  ·  HUAWEI GUILTY IN U.S. COURT",
           font=font(SANS_B, 20), fill=GOLD, anchor="ma")

    canvas.save("entry.png")
    print("saved entry.png", canvas.size)


if __name__ == "__main__":
    main()
