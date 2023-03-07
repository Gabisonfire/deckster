import requests
import json
import logging
from deckster.common.core import update_key_image
from deckster.common.scheduler import sched
from types import SimpleNamespace

logger = logging.getLogger("deckster")

def get_args(key):
    args = key.args
    parsed = SimpleNamespace()
    parsed.ha_base_url = args["ha_base_url"]
    parsed.domain = args["domain"]
    parsed.action = args["action"]
    parsed.entity_id = args["entity_id"]
    parsed.token = args["token"]
    parsed.track_state = args["track_state"]
    parsed.url = f"{parsed.ha_base_url}/api/services/{parsed.domain}/{parsed.action}"
    parsed.json_data = json.dumps({"entity_id": parsed.entity_id})
    parsed.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {parsed.token}"
    }
    if parsed.track_state:
        parsed.state_url = f"{parsed.ha_base_url}/api/states/{parsed.entity_id}"
        parsed.state_activated = args["state_activated"]
        parsed.state_deactivated = args["state_deactivated"]
        parsed.state_check_interval = args["state_check_interval"]
    return parsed

def main(deck, key, pressed):
    args = get_args(key)

    try:
        logger.debug(f"Trying POST request for {args.url} with parameters: {args.json_data} and headers: {args.headers}.")
        res = requests.post(args.url, data = args.json_data, headers = args.headers)
    except Exception as e:
        logger.error(f"Request to {args.url} failed: {e}")

    logger.info(f"Request returned status code {res.status_code}.")

def update_state(deck, key):
    try:
        args = get_args(key)
        logger.debug(f"Trying GET request for {args.state_url} with headers: {args.headers}.")
        state = requests.get(args.state_url, headers = args.headers)
        if state.json()["state"] == args.state_activated:
            logger.debug(f"Key returned a state of '{state.json()['state']}'")
            key.toggle_state = True
            
        elif state.json()["state"] == args.state_deactivated:
            logger.debug(f"Key returned a state of '{state.json()['state']}'")
            key.toggle_state = False
            
        else:
            logger.error(f"Invalid state returned: {state.json()['state']} from {args.state_url}")

        update_key_image(deck, key, False)
    except Exception as e:
        logger.error(f"Request to {args.state_url} failed: {e}")

def run_once(deck, key):
    if key.button_type not in ["toggle", "timer_toggle"]:
        return
    args = get_args(key)
    if args.track_state:
        logger.debug(f"Scheduling job for state tracking on key: {key.key}, entity: {args.entity_id}")
        sched.add_job(update_state, "interval", id = f"ha_state_checker_{args.entity_id}", max_instances=1, seconds=args.state_check_interval, args=[deck, key])