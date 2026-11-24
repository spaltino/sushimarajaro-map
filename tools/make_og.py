# -*- coding: utf-8 -*-
"""og-image.png (1200x630) 생성 스크립트 — 스시마라자로 맵 공유 미리보기.

실행: python3 tools/make_og.py
폰트: /usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf (OFL)
숫자·문구를 바꿀 때는 아래 DATA만 고치면 됩니다.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (253, 252, 249)
CREAM = (248, 242, 232)
RED = (217, 72, 47)
INK = (14, 16, 21)
MUTED = (122, 118, 112)
LINE = (232, 227, 219)
WHITE = (255, 255, 255)

FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"

DATE = "2026-11-24"
URL = "spaltino.github.io/sushimarajaro-map"
KICKER = "SUSHI MALA JARO MAP"
TITLE = "스시마라자로 맵"
SUB = "일본 · 중국 마운자로 원정 총정리"
SUB2 = "가격 · 공항 동선 · 세관 한도 · 실전 회화까지 한 페이지에"

CARDS = [
    ("JP", (14, 122, 85), "일본 29곳", "도쿄 · 오사카 · 교토 · 후쿠오카 · 나고야\n삿포로 · 오키나와"),
    ("CN", (217, 72, 47), "중국 46곳", "상하이 · 항저우 · 옌타이 등 10개 도시\n병원 33 · 약국 13"),
    ("KR", (91, 96, 104), "세관 12개 · 3개월", "1펜만 넘어도 전량 통관 보류\n2026-11-12 시행 기준"),
]


def font(size):
    return ImageFont.truetype(FONT, size)


def tw(draw, text, f, bold=0):
    b = draw.textbbox((0, 0), text, font=f, stroke_width=bold)
    return b[2] - b[0]


def fit(draw, text, size, maxw, bold=0, minsize=18):
    while size > minsize:
        f = font(size)
        if tw(draw, text, f, bold) <= maxw:
            return f
        size -= 1
    return font(size)


def draw_spaced(draw, xy, text, f, fill, spacing=3.2, bold=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill, stroke_width=bold, stroke_fill=fill)
        x += tw(draw, ch, f, bold) + spacing
    return x


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 오른쪽 큰 크림색 원
    d.ellipse([690, -170, 1500, 640], fill=CREAM)

    # 상단 붉은 바
    d.rectangle([0, 0, W, 8], fill=RED)

    # 킥커 + 제목
    draw_spaced(d, (68, 86), KICKER, font(19), RED, spacing=4.0, bold=0)
    d.text((66, 128), TITLE, font=font(92), fill=INK, stroke_width=2, stroke_fill=INK)
    d.text((68, 262), SUB, font=font(33), fill=(38, 40, 46), stroke_width=1, stroke_fill=(38, 40, 46))
    d.text((68, 318), SUB2, font=font(20), fill=MUTED)

    # 카드 3장
    cw, gap, top, bot = 341, 24, 358, 540
    for i, (chip, chip_color, big, small) in enumerate(CARDS):
        x0 = 68 + i * (cw + gap)
        x1 = x0 + cw
        d.rounded_rectangle([x0, top, x1, bot], radius=16, fill=WHITE, outline=LINE, width=1)
        # 칩
        cf = font(17)
        cwid = tw(d, chip, cf, 1) + 22
        d.rounded_rectangle([x0 + 22, top + 20, x0 + 22 + cwid, top + 50], radius=7, fill=chip_color)
        d.text((x0 + 22 + cwid / 2 - tw(d, chip, cf, 1) / 2, top + 23), chip, font=cf, fill=WHITE,
               stroke_width=1, stroke_fill=WHITE)
        # 큰 숫자
        bf = fit(d, big, 42, cw - 50, bold=1, minsize=24)
        d.text((x0 + 22, top + 66), big, font=bf, fill=INK, stroke_width=1, stroke_fill=INK)
        # 설명
        for j, line in enumerate(small.split("\n")):
            sf = fit(d, line, 17, cw - 46, minsize=13)
            d.text((x0 + 22, top + 122 + j * 26), line, font=sf, fill=MUTED)

    # 하단
    d.text((68, 578), URL, font=font(20), fill=MUTED)
    df = font(20)
    d.text((W - 68 - tw(d, "기준 " + DATE, df), 578), "기준 " + DATE, font=df, fill=MUTED)

    img.save("og-image.png", optimize=True)
    print("saved og-image.png", img.size)


if __name__ == "__main__":
    main()
