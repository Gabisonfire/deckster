import requests
import logging
import jq
from deckster.deckster import update_key_image, update_label_display

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

    d = jq.compile(args["json_parse"]).input(res.json()).first()
    logger.info(f"Parsed result: '{d}'' from {url}")
    if "send_to_display" in key.args or "send_to_label" in key.args:
            to_label = "send_to_label" in key.args
            logger.info(f"Sending GET result to {'label' if to_label else 'display'} for key {key.key}.")
            if to_label:
                key.label = str(d)
            else:
                key.display = str(d)
            update_label_display(key, True if "send_to_label" in key.args else False)
            update_key_image(deck, key, pressed)
