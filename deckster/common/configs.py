import json
import os
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(dir_path).parent.parent

def read_key_config(key, attr):
    for x in json.load(open(os.path.join(dir_path, "keys.json"))):
        if x["key"] == key:
            for y in x.keys():
                if y == attr:
                  return x[y]
    raise ValueError(f'Not key/value found for {key}')

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