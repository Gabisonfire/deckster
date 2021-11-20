import requests
import json
from common.configs import write_key_config

def main(state, args):
    key = state[1]
    url = args[0]
    json_data = None
    headers = None
    if len(args) > 1 and args[1] is not None:
        json_data = json.load(open(args[2]))
    if len(args) > 2 and args[2] is not None:
        headers = json.load(open(args[3]))

    res = requests.get(url, params = json_data, headers = headers)
    write_key_config(key, "label", res.json()["properties"]["name"])