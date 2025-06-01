import logging
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path 
import time 

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

font = ImageFont.truetype("fonts/CormorantGaramond-VariableFont_wght.ttf", 22)

try:
    logging.info("Initialized EPD")
    epd = epd7in5_V2.EPD()
    
    epd.init() # Needed after waking from sleep-mode
    epd.Clear() # Clear what's on the screen
        
    epd.init_part() 


    # Draw image
    image = Image.new(mode="1", size=(epd.width, epd.height), color=1)
    draw = ImageDraw.Draw(image)
    draw.text((0,0), 'Hello World', font=font, fill=0) # Hello world at the top left
    
    # Display image on the screen
    epd.display(epd.getbuffer(image))
    
    time.sleep(5)
   
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
