from PIL import ImageDraw, ImageFont

def draw_title_author(
    title: str,
    author: int,
    draw: ImageDraw,
    display_wh_px: tuple[int, int],
    xy_offset_px: tuple[int, int],
    title_author_gap_px: int,
    title_font: ImageFont.FreeTypeFont,
    author_font: ImageFont.FreeTypeFont,
) -> None:
    # Measure both lines
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    author_bbox = draw.textbbox((0, 0), author, font=author_font)

    title_wh_px = (title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1])
    author_wh_px = (author_bbox[2] - author_bbox[0], author_bbox[3] - author_bbox[1])

    # Figure out each line's x-position
    title_x_px = display_wh_px[0] - title_wh_px[0] - xy_offset_px[0]
    author_x_px = display_wh_px[0] - author_wh_px[0] - xy_offset_px[0]

    # Figure out each line's y-position
    author_y_px = display_wh_px[1] - author_wh_px[1] - xy_offset_px[1]  # bottom line
    title_y_px = author_y_px - title_wh_px[1] - title_author_gap_px  # line above

    # Draw text
    draw.text((title_x_px, title_y_px), title, font=title_font, fill=0)
    draw.text((author_x_px, author_y_px), author, font=author_font, fill=0)