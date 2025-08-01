# Literature-clock

TODO LINK WEBSITE

# How to install

> [!IMPORTANT]
> This script is meant to be run on a RPi Zero 2W hooked to a Waveshare’s 7.5inch e-Paper screen.
> To set it up correctly, please follow TODO LINK WEBSITE

1. Install the necessary libraries with

```bash
pip install -r requirements.txt
```

2. 

6. Install necessary libraries 
-- test with requirements.txt
- uv pip install rpi-gpio
- uv pip install gpiozero
- uv pip install pillow
7. Connect screen
8. Restart
9. Run test script -- `sudo python test.py` TODO WRITE IT, E.G. HELLO WORLD

# Content

```bash
├── data/ # Where the quotes are stored, sourced from https://github.com/JohannesNE/literature-clock
├── fonts/ # Fonts, sourced from https://fonts.google.com/
├── notebooks/ # Notebooks used to prepare the data and 
├── waveshare_epd/ # Waveshare-sourced libraries to talk to the e-paper screen (only the 7in5 screen)
├── draw_current_time.py # Main script TODO should it be renamed main then ?..
└── README.md 
```

# TODOs

- [ ] Finish this README
- [ ] Avoid having .last_refresh_dt committed 