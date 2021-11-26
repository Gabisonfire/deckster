import requests
import json
from common.configs import write_key_config

# Needs arg for value to show in label
def main(state):
    jkey = json.loads(state["key"])
    args = jkey["args"]
    url = args["url"]
    json_data = None
    headers = None

    res = requests.get(url, params = json_data, headers = headers)