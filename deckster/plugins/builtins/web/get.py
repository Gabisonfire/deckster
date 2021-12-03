import requests
import logging
from deckster import update_key_image, update_label

def main(deck, key, pressed):
    logger = logging.getLogger("deckster")
    args = key.args
    url = args["url"]
    if "json_data" in args:
        json_data = args["json_data"]
    else:
        json_data = None
    if "headers" in args:
        headers = args["headers"]
    else:
        headers = None

    try:
        logger.debug(f"Trying GET request for {url} with parameters: {json_data} and headers: {headers}.")
        res = requests.get(url, params = json_data, headers = headers)
    except Exception as e:
        logger.error(f"Request to {url} failed: {e}")

    if not res.status_code in args["status_codes"]:
        logger.error(f"Status code returned {res.status_code} not in expected codes.")
        return

    d = res.json()[args["json_parse"]]
    logger.info(f"Parsed result: '{d}'' from {url}")
    if "send_to_display" in key.args:
        if key.args["send_to_display"]:
            logger.info(f"Sending GET result to display for key {key.key}.")
            key.label = str(d)
            update_label(key)
            update_key_image(deck, key, pressed)
