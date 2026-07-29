from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

WIDTH = 1080
HEIGHT = 1080

BACKGROUND = (16, 24, 32)
WHITE = (255, 255, 255)
GREEN = (0, 200, 83)
GREY = (185, 185, 185)


def load_font(size: int):
    font_path = Path("assets/fonts/DejaVuSans-Bold.ttf")

    if font_path.exists():
        return ImageFont.truetype(str(font_path), size)

    return ImageFont.load_default()


def create_news_card(
    headline: str,
    source: str,
    category: str,
    output_path: str,
):
    img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)

    draw = ImageDraw.Draw(img)

    title_font = load_font(72)
    headline_font = load_font(54)
    source_font = load_font(38)

    draw.text(
        (60, 60),
        "🌍 GLOBAL PULSE",
        fill=GREEN,
        font=title_font,
    )

    draw.text(
        (60, 170),
        category.upper(),
        fill=WHITE,
        font=source_font,
    )

    wrapped = textwrap.fill(headline, width=28)

    draw.multiline_text(
        (60, 260),
        wrapped,
        fill=WHITE,
        font=headline_font,
        spacing=12,
    )

    draw.text(
        (60, 930),
        f"Source: {source}",
        fill=GREY,
        font=source_font,
    )

    img.save(output_path)
