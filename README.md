# WG Bot
This script aims to make life easier for people looking for homes in Germany. Specifically, it automates the search for houses and rooms on the wg-gesucht.de website and contacts the landlord privately.

This is a heavily modified version of [immo](https://github.com/nickirk/immo). Rewritten to work with the latest versions of Python, Scrapy and the site itself.

## Requirements
1. `Python 3` (tested only on Python 3.10)
    - pip
    - venv
2. `chromedriver` (default location is `/usr/bin/chromedriver` setted on `wg_submit.py`)
	- For Ubuntu you can follow [this guide](https://skolo.online/documents/webscrapping/#install-chrome-browser-and-chromedriver-ubuntu-20-04) to install it. 
	- After installing it, check the path with `which chromedriver`, if it does not match the default one, change it in the file `wg_submit.py`
	- If you want, you can change the Selenium configuration to replace Chrome with another browser. In this case, you will not need chromedriver
3. `scrapy` 
	- You can install the latest version of Scrapy with `pip install scrapy`

## Create the environment
1. Clone the repository with `git clone https://github.com/AlessandroGrassi99/wgbot.git`
2. Make sure you are in the root of the repository folder (inside the `wgbot` folder)
3. Edit `config.toml` with your data
4. Copy and replace the URL of [your wg-gesucht.de filters](https://www.wg-gesucht.de/en/mein-wg-gesucht-filter.html) into the file `wg_spider.py`
	- Example: 
        ```
        urls  = [
            'https://www.wg-gesucht.de/en/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Munchen.90.0+1+2+3.1.0.html?user_filter_id=7134295&ad_type=0&offer_filter=1&city_id=90&noDeact=1&dFr=1659045600&dTo=1664920800&rMax=800&sin=1&exc=2&img_only=1&ot=2114%2C2123%2C2124%2C2131%2C2132%2C2133&categories=0%2C1%2C2%2C3&rent_types=0',
            'https://www.wg-gesucht.de/en/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Garching-b-Munchen.400.0+1+2+3.1.0.html?user_filter_id=7134280&ad_type=0&offer_filter=1&city_id=400&noDeact=1&dFr=1659045600&dTo=1664920800&rMax=800&sin=1&exc=2&img_only=1&categories=0%2C1%2C2%2C3&rent_types=0',
        ]
        ```
5. Run `./set_env.sh`

## Run
1. Activate python's virtual environment with `source venv/bin/activate`
2. Run `python wg_bot.py`

## Tips and troubleshooting
- You may need to manually edit the `wgbot/settings.py` file and set `ROBOTSTXT_OBEY = False`
- If at runtime something is wrong with the generation of the `wg_offer.json` file, set `LOG_ENABLED=true` into `wg_bot.py`
- I suggest you to check the README file of the [original project](https://github.com/nickirk/immo), there might be interesting insights there
