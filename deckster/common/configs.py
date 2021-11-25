import json
import os
from pathlib import Path
from common.keys import Key

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(dir_path).parent.parent

def read_keys():
    templist = []
    for x in json.load(open(os.path.join(dir_path, "keys.json"))):
        templist.append(
            Key(
                key = x["key"],
                name = x["name"],
                icon_default = x["icon_default"],
                icon_pressed = x["icon_pressed"],
                font = x["font"],
                label = x["label"],
                plugin = x["plugin"],
                args = x["args"],
                button_type = x["button_type"],
                page = x["page"]
            )
        )
    return templist

# def write_keys()

def find_key(key, page, key_list):
    for x in key_list:
        if x.key == key and x.page == page:
            return x

def read_config(cfg):
    cfg_file = json.load(open(os.path.join(dir_path, "config.json")))
    for k in cfg_file:
        if k == cfg:
            return cfg_file[k]

def defined_keys():
    return len(json.load(open(os.path.join(dir_path, "keys.json"))))

def write_key_config(key, cfg, value):
    with open(os.path.join(dir_path, "keys.json"), "r") as jsonFile:
        data = json.load(jsonFile)
        for x in data:
            if x["key"] == key:
                x[cfg] = value
    with open(os.path.join(dir_path, "keys.json"), "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)