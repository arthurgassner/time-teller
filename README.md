# Literature-clock

# Setup hardware

TODO list needed hardware, i.e., with images

- 7.5 inch waveshare e-paper screen
- e-Paper driver HAT
- micro usb cable 
- pi zero 2w with soldered pins
- SD card

1. Flash SD card following raspberry tutorial 
    - put in your SSID/password and SSH pub key
2. SSH into pi zero
3. Install zsh 
4. Clone this repo
5. Install uv 
6. Install necessary libraries 
-- test with requirements.txt
- uv pip install rpi-gpio
- uv pip install gpiozero
- uv pip install pillow
7. Connect screen
8. Restart
9. Run test script -- `sudo python test.py` TODO WRITE IT, E.G. HELLO WORLD

