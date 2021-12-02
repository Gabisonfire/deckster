import requests
from deckster import update_key_image

def main(deck, key, pressed):
    args = key.args
    url = args["url"]
    json_data = None
    headers = None

    res = requests.get(url, params = json_data, headers = headers)

    d = res.json()["unixtime"]
    print(d)
    key.label = str(d)
    key.update_label()
    update_key_image(deck, key, pressed)
