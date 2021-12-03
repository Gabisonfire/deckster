import requests
from deckster import update_key_image

def main(deck, key, pressed):
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
        res = requests.get(url, params = json_data, headers = headers)
    except Exception as e:
        print(f"Request to {url} failed: {e}")

    if not res.status_code in args["status_codes"]:
        print(f"Status code returned {res.status_code} not in expected codes.")
        return

    d = res.json()[args["json_parse"]]
    key.label = str(d)
    key.update_label()
    update_key_image(deck, key, pressed)
