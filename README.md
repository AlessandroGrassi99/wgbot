# WG Bot
This script aims to make life easier for people looking for homes in Germany. Specifically, it automates the search for houses and rooms on the wg-gesucht.de website and contacts the landlord privately.

This is a deeply modified version of [immo](https://github.com/nickirk/immo). Rewritten to work with the latest versions of Python and the site itself.

## Requirements
1. `Python 3` (tested only on Python 3.10)
    - pip
    - venv
2. `chromedriver` (default location is `/usr/bin/chromedriver` setted on `wg_submit.py`)
	- For Ubuntu you can follow [this guide](https://skolo.online/documents/webscrapping/#install-chrome-browser-and-chromedriver-ubuntu-20-04) to install it. 
	- After installing it, check the path with `which chromedriver`, if it does not match the default one, change it in the file `wg_submit.py`
	- If you want, you can change the Selenium configuration to replace Chrome with another browser. In this case, you will not need chromedriver

## Create the environment
1. Clone the repository with `git clone https://github.com/AlessandroGrassi99/wgbot.git`
2. Make sure you are in the root of the repository folder (inside the `wgbot` folder)
3. Edit `config.toml` with your data
    - Copy and replace the URL of [your wg-gesucht.de filters](https://www.wg-gesucht.de/en/mein-wg-gesucht-filter.html) into  `config.toml`
5. Create Python virtual environment with `python -m venv venv`
6. Activate python's virtual environment with `source venv/bin/activate`
7. Install dependencies with `pip install -r requirements.txt` 

## Run
1. Activate python's virtual environment with `source venv/bin/activate`
2. Run `python wg_bot.py`

## Tips and troubleshooting
- You may need to manually edit the `wgbot/settings.py` file and set `ROBOTSTXT_OBEY = False`
- If at runtime something is wrong with the generation of the `wg_offer.json` file, set `LOG_ENABLED=true` into `wg_bot.py`
- I suggest you to check the README file of the [original project](https://github.com/nickirk/immo), there might be interesting insights there
