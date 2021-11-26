import requests
import json
from common.configs import write_key_config

def main(state):
    jkey = json.loads(state["key"])
    args = jkey["args"]
    url = args["url"]
    json_data = None
    headers = None

    res = requests.get(url, params = json_data, headers = headers)
    write_key_config(jkey["key"], jkey["page"], "label", res.json()["properties"]["name"])