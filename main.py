import logging
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2
from draw_title_author import draw_title_author
from draw_quote import draw_quote
from randomly_select_quote_title_author import randomly_select_quote_title_author

logging.basicConfig(level=logging.DEBUG)

LAST_FULL_REFRESH_DT_FILEPATH = Path('.last_full_refresh_dt')
FULL_REFRESH_DT = datetime(year=1900, month=1, day=1, hour=2, minute=0)
FONT_FILEPATH = Path("fonts/CormorantGaramond-VariableFont_wght.ttf")
ITALIC_FONT_FILEPATH = Path("fonts/CormorantGaramond-Italic-VariableFont_wght.ttf")
MAX_WIDTH_RATIO = 0.8
MAX_HEIGHT_RATIO = 0.6

try:
    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    epd.init() # Needed after waking from sleep-mode
    
    # Do a full refresh if you haven't done one in >24h
    # Also do a full refresh if you've passed <FULL_REFRESH_DT> and haven't done one today yet
    now = datetime.now()
    last_full_refresh_dt_str = LAST_FULL_REFRESH_DT_FILEPATH.read_text()
    last_full_refresh_dt = datetime.fromisoformat(last_full_refresh_dt_str.strip('\n'))
            
    if last_full_refresh_dt - now > timedelta(minutes=20) or (last_full_refresh_dt.date() != now.date() and (now.hour, now.minute) > (FULL_REFRESH_DT.hour, FULL_REFRESH_DT.minute)):
        logging.info("Clearing the screen...")
        epd.Clear()
        LAST_FULL_REFRESH_DT_FILEPATH.write_text(now.isoformat())
        
    epd.init_part() 
    
    # Figure out which text to draw
    quote, title, author = randomly_select_quote_title_author()

    # Draw image
    image = Image.new(mode="1", size=(epd.width, epd.height), color=1)
    draw = ImageDraw.Draw(image)
    draw_quote(
        quote,
        draw,
        display_wh_px=(epd.width, epd.height),
        max_width_ratio=MAX_WIDTH_RATIO,
        max_height_ratio=MAX_HEIGHT_RATIO,
        font_filepath=ITALIC_FONT_FILEPATH,
    )
    draw_title_author(
        title,
        f"— {author}",
        draw,
        display_wh_px=(epd.width, epd.height),
        xy_offset_px=(20, 20),
        title_author_gap_px=5,
        title_font_filepath=ITALIC_FONT_FILEPATH,
        author_font_filepath=FONT_FILEPATH,
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
