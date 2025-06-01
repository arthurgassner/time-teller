import csv
import logging
import random
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

LAST_FULL_REFRESH_DT_FILEPATH = Path('.last_full_refresh_dt')
FULL_REFRESH_DT = datetime(year=1900, month=1, day=1, hour=2, minute=0)

def randomly_select_quote_title_author() -> tuple[str, str, str]:

    # Figure out the current time
    now = datetime.now()
    now_str = f"{now.hour:02}:{now.minute:02}"
    logging.debug(f"Selected time: {now_str}")

    # Load the file containing the relevant quotes
    with open(f"data/quotes/{now_str}.csv", newline="") as f:
        reader = csv.reader(f)
        csv_rows = list(reader)

    # Randomly select one row
    selected_row_idx = random.randint(0, len(csv_rows) - 1)
    selected_csv_row = "".join(csv_rows[selected_row_idx])

    _, quote, title, author = selected_csv_row.split("|")

    return quote, title, author


def draw_quote(
    quote: str,
    draw: ImageDraw,
    display_wh_px: tuple[int, int],
    max_width_ratio: float,
    font: ImageFont,
) -> None:
    max_line_width_px = int(display_wh_px[0] * max_width_ratio)
    words = quote.split()

    # Figure out whether each word belongs on the current line, or the next
    lines = []
    curr_line = ""
    for word in words:
        test_line = f"{curr_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width_px = bbox[2] - bbox[0]
        if test_width_px <= max_line_width_px:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = word

    # Handle trailing line
    if curr_line:
        lines.append(curr_line)

    # Figure out the text's height [px]
    line_height_px = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    text_height_px = len(lines) * line_height_px
    y_offset = (display_wh_px[1] - text_height_px) // 2

    # Draw each line centered
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (display_wh_px[0] - line_width) // 2
        draw.text((x, y_offset), line, font=font, fill=0)
        y_offset += line_height_px


def draw_title_author(
    title: str,
    author: int,
    draw: ImageDraw,
    display_wh_px: tuple[int, int],
    xy_offset_px: tuple[int, int],
    title_author_gap_px: int,
    title_font: ImageFont,
    author_font: ImageFont,
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


try:
    # Load and setup fonts
    quote_font = ImageFont.truetype(
        "fonts/CormorantGaramond-Italic-VariableFont_wght.ttf", 50
    )
    quote_font.set_variation_by_axes([200])

    title_font = ImageFont.truetype(
        "fonts/CormorantGaramond-Italic-VariableFont_wght.ttf", 24
    )
    author_font = ImageFont.truetype(
        "fonts/CormorantGaramond-VariableFont_wght.ttf", 22
    )
    author_font.set_variation_by_axes([500])

    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    
    # Do a full refresh if you haven't done one in >24h
    # Also do a full refresh if you've passed <FULL_REFRESH_DT> and haven't done one today yet
    now = datetime.now()
    last_full_refresh_dt_str = LAST_FULL_REFRESH_DT_FILEPATH.read_text()
    last_full_refresh_dt = datetime.fromisoformat(last_full_refresh_dt_str)
            
    if last_full_refresh_dt - now > timedelta(hours=24) or (last_full_refresh_dt.date() != now.date() and (now.hour, now.minute) > (FULL_REFRESH_DT.hour, FULL_REFRESH_DT.minute)):
        epd.init()
        epd.Clear()
        LAST_FULL_REFRESH_DT_FILEPATH.write_text(last_full_refresh_dt.isoformat())
        
    epd.init_part() # Needed after waking from sleep-mode

    # Figure out which text to draw
    quote, title, author = randomly_select_quote_title_author()

    # Draw image
    image = Image.new(mode="1", size=(epd.width, epd.height), color=1)
    draw = ImageDraw.Draw(image)
    draw_quote(
        quote,
        draw,
        display_wh_px=(epd.width, epd.height),
        max_width_ratio=0.8,
        font=quote_font,
    )
    draw_title_author(
        title,
        f"— {author}",
        draw,
        display_wh_px=(epd.width, epd.height),
        xy_offset_px=(20, 20),
        title_author_gap_px=5,
        title_font=title_font,
        author_font=author_font,
    )

    # Display image
    # Note that parial display allows for a faster/cleaner refresh (visually), but should not always be done.
    # A full refresh of the screen should be done at least every 24h, as per https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual
    epd.display_Partial(epd.getbuffer(image), 0, 0, epd.width, epd.height)
           
    # Enter sleep mode, as we don't want to screen to be on high-voltage continuously, 
    # for fear of breaking it as per https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual
    logging.info(".sleep")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
