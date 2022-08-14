from logging import Filter
from subprocess import call
from wg_submit import submit_app
from wg_spider import FilterSpider
import json
import os.path
import time
import toml

from loguru import logger

CONFIG_NAME = "config.toml"
CACHE_FNAME = "wg_cache.json"


def get_data(cache_fname: str, spider: FilterSpider):
    new_urls = spider.get_offers()
    if os.path.isfile(cache_fname):
        with open(cache_fname) as data_file:
            try:     
                old_urls = json.load(data_file)
            except json.JSONDecodeError as e:
                old_urls = []
        diff_urls = list(set(new_urls) - set(old_urls))
    else:
        logger.info(f"{len(new_urls):03d} offers found: {new_urls}")
        while True:
            input_data = input("No wg_cache.json file found. Sending messages to all offers found above? (y/n)\n").lower()
            if input_data == "y":
                diff_urls = new_urls
                break
            elif input_data == "n":
                diff_urls = []
                break
            logger.warning("Invalid input")

    with open(cache_fname, 'w') as cache_file:
        cache_file.write(json.dumps(new_urls))

    return diff_urls


def get_config(config_name):
    with open(config_name) as data_file:
        return toml.load(data_file)


def main():
    config = get_config(CONFIG_NAME)
    spider = FilterSpider(config['filters'])
    logger.info("Starting service")

    while True:
        new_urls = get_data(CACHE_FNAME, spider)

        logger.info(f"{len(new_urls):03d} New offers found: {new_urls}")
        for url in new_urls:
            logger.info(f"Sending message to {url}...")
            contacted = False
            for _ in range(0, 3):
                if submit_app(config, url):
                    contacted = True
                    break
                logger.warning("Retry to contact")
            if contacted:
                logger.info("Successfully contacted")
            else:
                logger.error("Unable to contact")

        time.sleep(30)


if __name__ == "__main__":
    main()
