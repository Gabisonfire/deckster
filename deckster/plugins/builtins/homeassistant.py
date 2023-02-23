import requests
import json
import logging

def main(deck, key, pressed):
    logger = logging.getLogger("deckster")
    args = key.args
    ha_base_url = args["ha_base_url"]
    domain = args["domain"]
    action = args["action"]
    entity_id = args["entity_id"]
    token = args["token"]
    url = f"{ha_base_url}/api/services/{domain}/{action}"
    json_data = json.dumps({"entity_id": entity_id})
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        logger.debug(f"Trying POST request for {url} with parameters: {json_data} and headers: {headers}.")
        res = requests.post(url, data = json_data, headers = headers)
    except Exception as e:
        logger.error(f"Request to {url} failed: {e}")

    logger.info(f"Request returned status code {res.status_code}.")