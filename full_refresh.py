"""Perform a full-refresh of the e-ink screen.
"""

import logging
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 
import time 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

font = ImageFont.truetype("fonts/CormorantGaramond-VariableFont_wght.ttf", 42)

try:
    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    
    epd.init() # Need to .init after waking from sleep-mode

    # Draw image
    image = Image.new(mode="1", size=(epd.width, epd.height), color=1)
    draw = ImageDraw.Draw(image)
    draw.text((epd.width // 2, epd.height // 2), 'This is a full refresh.', font=font, fill=0) 
    
    # Display image on the screen
    epd.display(epd.getbuffer(image))
    
    time.sleep(1)
   
    # Enter sleep mode, as we don't want to screen to be on high-voltage continuously, 
    # for fear of breaking it as per https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual
    logging.info(".sleep")
    epd.sleep()
except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + C:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
