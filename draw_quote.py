import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path 

def parse_quote(text: str) -> list[tuple[str, bool]]:
    segments = []
    pattern = re.compile(r"(<b>.*?</b>)")
    parts = pattern.split(text)
    for part in parts:
        if part.startswith("<b>") and part.endswith("</b>"):
            segments.append((part[3:-4], True))
        else:
            segments.append((part, False))
    return segments

def measure_text_height(
    quote: str,
    draw: ImageDraw.ImageDraw,
    max_width_px: int,
    font: ImageFont.FreeTypeFont,
) -> int:
    segments = parse_quote(quote)
    words = [(word, is_bold) for segment, is_bold in segments for word in segment.split()]

    lines = []
    curr_line = []

    while words:
        word, is_bold = words.pop(0)
        test_line = curr_line + [(word, is_bold)]
        test_width = 0
        for w, bold in test_line:
            bbox = draw.textbbox((0, 0), w, font=font)
            test_width += bbox[2] - bbox[0]
        test_width += (len(test_line) - 1) * draw.textlength(" ", font=font)

        if test_width <= max_width_px:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = [(word, is_bold)]

    if curr_line:
        lines.append(curr_line)

    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    
    return len(lines) * line_height

def find_max_font_size(
    quote: str,
    image_size: tuple[int, int],
    max_width_ratio: float,
    max_height_ratio: float,
    font_filepath: Path,
) -> int:
    max_width_px = int(image_size[0] * max_width_ratio)
    max_height_px = int(image_size[1] * max_height_ratio)

    # Create dummy image for measuring
    dummy_image = Image.new("L", (10, 10))
    draw = ImageDraw.Draw(dummy_image)

    low, high = 10, 300
    best_size = low

    while low <= high:
        mid = (low + high) // 2
        font = ImageFont.truetype(str(font_filepath), mid)

        text_height = measure_text_height(quote, draw, max_width_px, font)

        if text_height <= max_height_px:
            best_size = mid
            low = mid + 1
        else:
            high = mid - 1

    return best_size

def draw_quote(
    quote: str,
    draw: ImageDraw.ImageDraw,
    display_wh_px: tuple[int, int],
    max_width_ratio: float,
    max_height_ratio: float,
    font_filepath: Path,
) -> None:
    font_size = find_max_font_size(quote, display_wh_px, max_width_ratio, max_height_ratio, font_filepath)
    
    # Setup the fonts
    font = ImageFont.truetype(str(font_filepath), font_size)
    font.set_variation_by_axes([200])
    font_bold = ImageFont.truetype(str(font_filepath), font_size)
    font_bold.set_variation_by_axes([1000])

    max_line_width_px = int(display_wh_px[0] * max_width_ratio)
    segments = parse_quote(quote)
    words = [(word, is_bold) for segment, is_bold in segments for word in segment.split()]

    lines = []
    curr_line = []

    while words:
        word, is_bold = words.pop(0)
        test_line = curr_line + [(word, is_bold)]
        test_width = 0
        for w, bold in test_line:
            f = font_bold if bold else font
            bbox = draw.textbbox((0, 0), w, font=f)
            test_width += bbox[2] - bbox[0]
        test_width += (len(test_line) - 1) * draw.textlength(" ", font=font)

        if test_width <= max_line_width_px:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = [(word, is_bold)]

    if curr_line:
        lines.append(curr_line)

    line_height = max(
        font.getbbox("Ay")[3] - font.getbbox("Ay")[1],
        font_bold.getbbox("Ay")[3] - font_bold.getbbox("Ay")[1]
    )
    total_height = len(lines) * line_height
    y_offset = (display_wh_px[1] - total_height) // 2

    for line in lines:
        line_width = sum(
            draw.textbbox((0, 0), word, font=(font_bold if bold else font))[2]
            for word, bold in line
        )
        line_width += (len(line) - 1) * draw.textlength(" ", font=font)
        x_offset = (display_wh_px[0] - line_width) // 2

        for i, (word, bold) in enumerate(line):
            f = font_bold if bold else font
            draw.text((x_offset, y_offset), word, font=f, fill=0)
            word_width = draw.textbbox((x_offset, y_offset), word, font=f)[2] - x_offset
            x_offset += word_width
            if i < len(line) - 1:
                x_offset += draw.textlength(" ", font=font)
        y_offset += line_height
