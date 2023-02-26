import requests
import json
import logging
from deckster.common.core import update_key_state, update_key_image
from deckster.common.scheduler import sched

def main(deck, key, pressed):
    logger = logging.getLogger("deckster")
    args = key.args
    ha_base_url = args["ha_base_url"]
    domain = args["domain"]
    action = args["action"]
    entity_id = args["entity_id"]
    token = args["token"]
    track_state_locally = key.track_state_locally
    url = f"{ha_base_url}/api/services/{domain}/{action}"
    json_data = json.dumps({"entity_id": entity_id})
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # If state is not handled by Deckster
    if not track_state_locally:
        state_url = f"{ha_base_url}/api/states/{entity_id}"
        state_activated = args["state_activated"]
        state_deactivated = args["state_deactivated"]
        state_check_interval = args["state_check_interval"]

    def update_state():
        try:
            logger.debug(f"Trying GET request for {state_url} with headers: {headers}.")
            state = requests.get(state_url, headers = headers)
            if state.json()["state"] == state_activated:
                logger.debug(f"Key returned a state of '{state.json()['state']}'")
                key.toggle_state = False # Inverting toggle since update_key_image will simulate a manual toggle.
                
            elif state.json()["state"] == state_deactivated:
                logger.debug(f"Key returned a state of '{state.json()['state']}'")
                key.toggle_state = True # Inverting toggle since update_key_image will simulate a manual toggle.
                
            else:
                logger.error(f"Invalid state returned: {state.json()['state']} from {state_url}")

            update_key_image(deck, key, pressed)
        except Exception as e:
            logger.error(f"Request to {state_url} failed: {e}")

    try:
        logger.debug(f"Trying POST request for {url} with parameters: {json_data} and headers: {headers}.")
        res = requests.post(url, data = json_data, headers = headers)
        if not track_state_locally:
            sched.add_job(update_state, "interval", id = "ha_state_checker_{entity_id}", max_instances=1, seconds=state_check_interval)
    except Exception as e:
        logger.error(f"Request to {url} failed: {e}")

    logger.info(f"Request returned status code {res.status_code}.")