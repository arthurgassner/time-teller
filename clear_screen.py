import logging
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 
import time 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    
    epd.init() # Needed after waking from sleep-mode
    epd.Clear() # Clear what's on the screen
       
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
