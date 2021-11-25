import requests
import json
from common.configs import write_key_config

def main(state):
    args = json.loads(state["key"])["args"]
    url = args["url"]
    json_data = None
    headers = None

    res = requests.get(url, params = json_data, headers = headers)
    write_key_config(state["key"], "label", res.json()["properties"]["name"])