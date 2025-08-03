import logging
from datetime import datetime, timedelta

from PIL import Image, ImageDraw

from utils.quote import Quote
from utils.settings import get_settings
from utils.waveshare_epd import epd7in5_V2
from utils.draw_title_author import draw_title_author
from utils.draw_quote import draw_quote

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    epd.init() # Needed after waking from sleep-mode


    # Do a full-refresh if 
    # 1. You haven't done one today (DD.MM.YYYY) AND you've passed FULL_REFRESH_TRIGGER_TIME (HH:MM:SS)
    now = datetime.now(tz=get_settings().TZ) 
    if get_settings().LAST_FULL_REFRESH_DT.date() < now.date() and now.time() > get_settings().FULL_REFRESH_TRIGGER_TIME:
        logging.info("Trigger time passed: Clearing the screen...")
        epd.Clear()
        get_settings().LAST_FULL_REFRESH_DT_FILEPATH.write_text(now.isoformat())

    # 2. The last one was >FULL_REFRESH_MAX_TIMEDELTA ago
    if get_settings().LAST_FULL_REFRESH_DT - now > get_settings().FULL_REFRESH_MAX_TIMEDELTA: 
        logging.info("Too long since last full refresh: Clearing the screen...")
        epd.Clear()
        get_settings().LAST_FULL_REFRESH_DT_FILEPATH.write_text(now.isoformat())

    epd.init_part() 
    
    # Figure out which text to draw
    quote = Quote.randomly_select_quote(dt=now)

    # Draw image
    image = Image.new(mode="1", size=(epd.width, epd.height), color=1)
    draw = ImageDraw.Draw(image)
    draw_quote(
        quote.quote,
        draw,
        display_wh_px=(epd.width, epd.height),
        max_width_ratio=get_settings().QUOTE_MAX_WIDTH_RATIO,
        max_height_ratio=get_settings().QUOTE_MAX_HEIGHT_RATIO,
        font_filepath=get_settings().ITALIC_FONT_FILEPATH,
    )
    draw_title_author(
        quote.title,
        f"— {quote.author}",
        draw,
        display_wh_px=(epd.width, epd.height),
        xy_offset_px=(20, 20),
        title_author_gap_px=5,
        title_font_filepath=get_settings().ITALIC_FONT_FILEPATH,
        author_font_filepath=get_settings().FONT_FILEPATH,
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
    logging.info("Ctrl + C:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
