# :clock10: Literature clock

<br>

<p align="center">🚀 <a href="https://literature-clock.arthurgassner.ch"><strong>Detailed write-up</strong></a> 🚀</p>

<br>

<p align="center"><img src="img/clock.jpg" width="60%"><p>

# How to install

> [!IMPORTANT]
> This script is meant to be run on a RPi Zero 2W hooked to a Waveshare’s 7.5inch e-Paper screen.
> To prepare the RPi correctly, please follow the [detailed write-up](https://literature-clock.arthurgassner.ch).

1. Install [`uv`](https://docs.astral.sh/uv/)
2. Create a virtual environment with `uv venv --system-site-packages`

> [!IMPORTANT]
> The `--system-site-packages` gives our virtual environment access to system-wide packages.
> This is necessary because this script relies on the RPi's GPIO, and hence on `gpiozero` -- a system-wide package.

3. Install the necessary libraries with

```bash
uv pip install -r requirements.txt
```

4. Ensure you're able to print to the screen by running `uv run hello_world.py`

# Content

```bash
├── data/ # Where the fonts & quotes are stored, sourced from https://github.com/JohannesNE/literature-clock and https://fonts.google.com/
├── 3d-models/ # 3D models of the cases
├── notebooks/ # Notebooks used to prepare the data and develop
├── utils/ # Utils for the script to run
├── tests/ # pytest
├── main.py # Main script
├── hello_world.py # Script displaying "Hello World" on the screen
├── full_refresh.py # Script performing a full refresh on the screen (see https://literature-clock.arthurgassner.ch/#step-3-display-something-on-the-screen)
├── partial_refresh.py # Script performing a partial refresh on the screen (see https://literature-clock.arthurgassner.ch/#step-3-display-something-on-the-screen)
├── clear_screen.py # Script clearing the screen
└── README.md 
```
