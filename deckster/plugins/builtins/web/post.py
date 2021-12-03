import requests
import json
import logging


def main(deck, key, pressed):
    logger = logging.getLogger("deckster")
    args = key.args
    url = args["url"]
    json_data = json.dumps(args["json_data"])
    headers = args["headers"]

    try:
        logger.debug(f"Trying POST request for {url} with parameters: {json_data} and headers: {headers}.")
        res = requests.post(url, data = json_data, headers = headers)
    except Exception as e:
        logger.error(f"Request to {url} failed: {e}")

    if not res.status_code in args["status_codes"]:
        logger.error(f"Status code returned {res.status_code} not in expected codes.")
        return
    logger.info(f"Request returned status code {res.status_code}.")