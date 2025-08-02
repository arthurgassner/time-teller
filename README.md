# Literature-clock

TODO LINK WEBSITE

TODO ADD IMAGE

# How to install

> [!IMPORTANT]
> This script is meant to be run on a RPi Zero 2W hooked to a Waveshare’s 7.5inch e-Paper screen.
> To prepare the RPi correctly, please follow TODO LINK WEBSITE

1. Install the necessary libraries with

```bash
pip install -r requirements.txt
```

2. Ensure you're able to print to the screen by running `python hello_world.py`

# Content

```bash
├── data/ # Where the fonts & quotes are stored, sourced from https://github.com/JohannesNE/literature-clock and https://fonts.google.com/
├── 3d-models/ # 3D models of the cases
├── notebooks/ # Notebooks used to prepare the data and develop
├── utils/ # Utils for the script to run
├── tests/ # pytest
├── main.py # Main script
├── hello_world.py # Script displaying "Hello World" on the screen
├── full_refresh.py # Script performing a full refresh on the screen (see TODO LINK WEBSITE)
├── partial_refresh.py # Script performing a partial refresh on the screen (see TODO LINK WEBSITE)
├── clear_screen.py # Script clearing the screen
└── README.md 
```
