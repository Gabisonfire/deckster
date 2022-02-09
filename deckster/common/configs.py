import json
import os
import yaml
import logging
from deckster.common.keys import Key
from pathlib import Path

global __version__
__version__ = "0.4.2"

logger = logging.getLogger("deckster")

dir_path = f"{str(Path.home())}/.config/deckster/"

logger.debug(f"Config path set to: {dir_path}")

def read_config(cfg):
    try:
        logger.debug(f"Reading from: {os.path.join(dir_path, 'config.json')}")
        cfg_file = json.load(open(os.path.join(dir_path, "config.json")))
    except Exception as e:
        logger.error(f"{os.path.join(dir_path, 'config.json')} contains invalid JSON. ({e})")

    for k in cfg_file:
        if k == cfg:
            return cfg_file[k]

def write_config(cfg, value):
    with open(os.path.join(dir_path, "config.json"), "r") as cfgFile:
        logger.debug(f"Reading current config")
        data = json.load(cfgFile)
        data[cfg] = value
    with open(os.path.join(dir_path, "config.json"), "w") as cfgFile:
        logger.debug(f"Writing '{value}' to '{cfg}'")
        json.dump(data, cfgFile, indent=2)

def read_keys():
    logger.debug(f"Reading keys...")
    templist = []
    keysdir = os.path.expanduser(read_config("keys_dir"))
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f))]
    logger.debug(f"Found keys file: {keyfiles}")
    json_keys = []
    for files in keyfiles:
        logger.debug(f"Reading {files}")
        try:
            if os.path.splitext(files)[1] in [".yaml", ".yml"]:
                logger.debug(f"{files} is YAML")
                y = yaml.safe_load(open(os.path.join(keysdir, files)))                
                tmp_json = json.loads(json.dumps(y))
            else:
                logger.debug(f"{files} is JSON")
                tmp_json = json.load(open(os.path.join(keysdir, files)))
            for k in tmp_json:
                json_keys.append(k)
        except Exception as e:
            logger.error(f"Error parsing {os.path.join(keysdir, files)}: {e}")   
    for x in json_keys:
        templist.append(Key(x))
    return templist

def find_key(key, page, key_list):
    logger.debug(f"Finding key {key} on page {page}.")
    for x in key_list:
        if x.key == key and x.page == page:
            return x

def max_page(key_list):
    high = 0
    for x in key_list:
        if x.page > high:
            high = x.page
    return high

def write_key_config(key, page, cfg, value):
    keysdir = os.path.expanduser(read_config("keys_dir"))
    logger.debug(f"{keysdir} is the keys directory.")
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f))]
    cfg_file = None
    for f in keyfiles:
        logger.debug(f"Parsing {f}...")
        with open(os.path.join(keysdir, f), "r") as jsonFile:
            if os.path.splitext(f)[1] in [".yml", ".yaml"]:
                logger.debug(f"{f} is YAML")
                y = yaml.safe_load(jsonFile)
                data = json.loads(json.dumps(y))
            else:
                logger.debug(f"{f} is JSON")
                data = json.load(jsonFile)
            for x in data:
                if x["key"] == key and x["page"] == page:
                    logger.debug(f"Found that key {key} on page {page} belongs to {f}")
                    cfg_file = f
                    break
            else:                
                continue
            break
    if cfg_file is not None:
        with open(os.path.join(keysdir, cfg_file), "w") as jsonFile:
            logger.debug(f"Writing modifications to {os.path.join(keysdir, cfg_file)}, Key {key}, {cfg} -> {value}")
            for x in data:
                if x["key"] == key and x["page"] == page:
                    x[cfg] = value
            if os.path.splitext(os.path.join(keysdir, cfg_file))[1] in [".yml", ".yaml"]:
                logger.debug("Converting to YAML")
                yaml.dump(data, jsonFile, allow_unicode=True, sort_keys=False)
            else:
                json.dump(data, jsonFile, indent=2)
    else:
        logger.error(f"Could not find a match for key {key} on page {page}.")

def empty_set(key_count, page):
    ks = []
    for k in range(key_count):
        x = {
            "key": k,
            "page": page,
            "plugin": "empty",
            "icon_default": "empty",
            "button_type": "toggle"
        }
        ks.append(Key(x))
    return ks