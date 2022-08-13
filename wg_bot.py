from subprocess import call
from wg_submit import submit_app
import json
import os.path
import time
import toml

from loguru import logger

CONFIG_NAME = "config.toml"
CACHE_FILE = "wg_offer.json"
CACHE_FILE_OLD = "wg_offer_old.json"


def get_data(file_name):
    with open(file_name) as data_file:
        try:     
            data = json.load(data_file)
        except json.JSONDecodeError as e:
            data = {}

    return list(set([i[u'data-id'] for i in data]))


def get_config(config_name):
    with open(config_name) as data_file:
        return toml.load(data_file)

def main():
    while True:
        config = get_config(CONFIG_NAME)
        logger.info("Starting service")
        if os.path.isfile(CACHE_FILE):
            call(["mv", CACHE_FILE, CACHE_FILE_OLD])
            call(["scrapy", "crawl", "wg-gesucht", "-o", CACHE_FILE, "-s", "LOG_ENABLED=false"])

            data = get_data(CACHE_FILE)
            data_old = get_data(CACHE_FILE_OLD)
        else:
            call(["scrapy", "crawl", "wg-gesucht", "-o", CACHE_FILE, "-s", "LOG_ENABLED=false"])
            data = get_data(CACHE_FILE)

            logger.info(f"{len(data):03d} All offers found: {data}")
            while True:
                input_data = input("No wg_offer.json file found. Sending messages to all offers found above?(y/n)\n").lower()
                if input_data == "y":
                    data_old = []
                    break
                elif input_data == "n":
                    call(["cp", CACHE_FILE, CACHE_FILE_OLD])
                    data_old = get_data(CACHE_FILE_OLD)
                    break
            
        diff_id = list(set(data) - set(data_old))

        if len(diff_id) > 0:
            logger.info(f"{len(diff_id):03d} New offers found: {diff_id}")
            for new in diff_id:
                logger.info(f"Sending message to {new}...")
                contacted = False
                for _ in range(0, 3):
                    if submit_app(config, new):
                        contacted = True
                        break
                    logger.warning("Retry to contact")
                if contacted:
                    logger.info("Successfully contacted")
                else:
                    logger.error("Unable to contact")
        else:
            logger.info(f"No new offers found")
        time.sleep(30)


if __name__ == "__main__":
    main()
