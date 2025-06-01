import csv
import logging
import random
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 
import re 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2
from draw_title_author import draw_title_author

logging.basicConfig(level=logging.DEBUG)

LAST_FULL_REFRESH_DT_FILEPATH = Path('.last_full_refresh_dt')
FULL_REFRESH_DT = datetime(year=1900, month=1, day=1, hour=2, minute=0)


def randomly_select_quote_title_author() -> tuple[str, str, str]:

    # Figure out the current time
    now = datetime.now()
    now_str = f"{now.hour:02}:{now.minute:02}"
    logging.debug(f"Selected time: {now_str}")
    
    # Load the file containing the relevant quotes
    with open(f"data/quotes/{now_str}.csv", newline='') as f:
        reader = csv.reader(f)
        csv_rows = list(reader)

    # Randomly select one row
    selected_row_idx = random.randint(0, len(csv_rows)-1)
    selected_csv_row = ''.join(csv_rows[selected_row_idx])   
    
    _, quote, title, author = selected_csv_row.split('|')
    
    # Fix endlines
    quote = quote.replace('<br/>', '\n')
    
    return quote, title, author


def parse_quote(text: str) -> list[tuple[str, bool]]:
    """Parse quote into segments: list of (text, is_bold)"""
    segments = []
    pattern = re.compile(r"(<b>.*?</b>)")
    parts = pattern.split(text)
    for part in parts:
        if part.startswith("<b>") and part.endswith("</b>"):
            segments.append((part[3:-4], True))
        else:
            segments.append((part, False))
    return segments

def draw_quote(
    quote: str,
    draw: ImageDraw.ImageDraw,
    display_wh_px: tuple[int, int],
    max_width_ratio: float,
    font: ImageFont.FreeTypeFont,
    font_bold: ImageFont.FreeTypeFont,
) -> None:
    max_line_width_px = int(display_wh_px[0] * max_width_ratio)

    segments = parse_quote(quote)

    # Split segments into words, retaining bold info
    words = []
    for segment, is_bold in segments:
        for word in segment.split():
            words.append((word, is_bold))

    # Word wrapping with bold-aware measurement
    lines = []
    curr_line = []
    while words:
        word, is_bold = words.pop(0)
        test_line = curr_line + [(word, is_bold)]
        test_text = " ".join(w for w, _ in test_line)
        test_width = 0
        for w, bold in test_line:
            f = font_bold if bold else font
            bbox = draw.textbbox((0, 0), w, font=f)
            test_width += bbox[2] - bbox[0]
        test_width += (len(test_line) - 1) * draw.textlength(" ", font=font)  # add spaces

        if test_width <= max_line_width_px:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = [(word, is_bold)]

    # Handle trailing line
    if curr_line:
        lines.append(curr_line)

    # Figure out the text's height [px]
    line_height = max(font.getbbox("Ay")[3] - font.getbbox("Ay")[1],
                      font_bold.getbbox("Ay")[3] - font_bold.getbbox("Ay")[1])
    total_height = len(lines) * line_height
    y_offset = (display_wh_px[1] - total_height) // 2

    # Draw each line
    for line in lines:
        # Measure total line width
        line_width = 0
        for word, bold in line:
            f = font_bold if bold else font
            bbox = draw.textbbox((0, 0), word, font=f)
            line_width += bbox[2] - bbox[0]
        line_width += (len(line) - 1) * draw.textlength(" ", font=font)

        x_offset = (display_wh_px[0] - line_width) // 2

        # Draw each word
        for i, (word, bold) in enumerate(line):
            f = font_bold if bold else font
            draw.text((x_offset, y_offset), word, font=f, fill=0)
            word_width = draw.textbbox((x_offset, y_offset), word, font=f)[2] - x_offset
            x_offset += word_width
            if i < len(line) - 1:
                space_width = draw.textlength(" ", font=font)
                x_offset += space_width

        y_offset += line_height


try:
    # Load and setup fonts
    quote_font = ImageFont.truetype(
        "fonts/CormorantGaramond-Italic-VariableFont_wght.ttf", 50
    )
    quote_font.set_variation_by_axes([200])
    
    quote_bold_font = ImageFont.truetype(
        "fonts/CormorantGaramond-Italic-VariableFont_wght.ttf", 50
    )
    quote_bold_font.set_variation_by_axes([1000])

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
        font_bold=quote_bold_font,
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
