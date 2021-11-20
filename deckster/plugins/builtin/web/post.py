import requests
import json

def main(state, args):
    url = args[0]
    if args[1] is not None:
        json_data = json.load(open(args[2]))
    if args[2] is not None:
        headers = json.load(open(args[3]))

    res = requests.post(url, data = json_data, headers = headers)