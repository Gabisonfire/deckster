import requests
import json


def main(state, args):
    url = args["url"]
    json_data = json.dumps(args["json_data"])
    headers = args["headers"]
    res = requests.post(url, data = json_data, headers = headers)
    print(res.status_code)