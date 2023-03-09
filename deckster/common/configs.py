import json
import os
from sqlalchemy import false
import yaml
import logging
import sys
from deckster.common.keys import Key, fake_key
from pathlib import Path
from filelock import FileLock
from jsonmerge import merge

global __version__
__version__ = "0.6.2"

logger = logging.getLogger("deckster")

dir_path = f"{str(Path.home())}/.config/deckster/"

logger.debug(f"Config path set to: {dir_path}")


class _counter:
    count = 0

def read_config(cfg, custom_config = None):
    """Read the configuration file

    Args:
        cfg (string): the config to read (key)
        custom_config (string, optional): Sepcify an alternate path. Defaults to None.

    Returns:
        string: value
    """
    if custom_config == None:
        full_cfg = os.path.join(dir_path, "config.json")
    else:
        full_cfg = os.path.join(dir_path, custom_config)
    lock_path = f"{full_cfg}.lock"
    cfg_file = None
    with FileLock(lock_path):
        try:
            logger.debug(f"Reading from: {os.path.join(dir_path, 'config.json')}")
            cfg_file = json.load(open(os.path.join(dir_path, "config.json")))
        except Exception as e:
            logger.error(f"{os.path.join(dir_path, 'config.json')} contains invalid JSON. ({e})")
            sys.exit(1)
        for k in cfg_file:
            if k == cfg:
                return cfg_file[k]
        return None

def write_config(cfg, value, custom_config = None):
    """Write value for a config

    Args:
        cfg (string): config to update
        value (string): value to write
        custom_config (string, optional): Provide an alternate path. Defaults to None.
    """
    if custom_config == None:
        full_cfg = os.path.join(dir_path, "config.json")
    else:
        full_cfg = os.path.join(dir_path, custom_config)
    lock_path = f"{full_cfg}.lock"
    with FileLock(lock_path):
        with open(full_cfg, "r") as cfgFile:
            logger.debug(f"Reading current config")
            data = json.load(cfgFile)
            data[cfg] = value
        with open(full_cfg, "w+") as cfgFile:
            logger.debug(f"Writing '{value}' to '{cfg}'")
            json.dump(data, cfgFile, indent=2)

def _fetch_templated_keys(json_key):
    template_name = json_key["template"]
    keysdir = os.path.expanduser(read_config("keys_dir"))
    tmpl_files = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f)) and (os.path.splitext(f)[1] in [".tmpl"])]
    for tmpl_file in tmpl_files:
        if os.path.splitext(tmpl_file)[0] == template_name:
            template = json.load(open(os.path.join(keysdir, f"{template_name}.tmpl")))
            if "key" in template or "page" in template:
                raise Exception("'key' and 'template' cannot be in a template file.")
            # The order here is important as changes in second param will overwrite the first one.
            return merge(template, json_key)
    
# Add lock here too
def read_keys():
    """Read all keys

    Returns:
        list: A list containing all keys
    """
    logger.debug(f"Reading keys...")
    templist = []
    keysdir = os.path.expanduser(read_config("keys_dir"))
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f)) and (os.path.splitext(f)[1] in [".yaml", ".yml", ".json"])]
    
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
        if "template" in x:
            x = _fetch_templated_keys(x)
        templist.append(Key(x))
    return templist

def find_key(key, page, key_list):
    """Find specific key on a page

    Args:
        key (integer): The key number
        page (integer): The page to search the key
        key_list (list): A list of keys

    Returns:
        Key: A found key
    """
    logger.debug(f"Finding key {key} on page {page}.")
    for x in key_list:
        if x.key == key and x.page == page:
            return x

def max_page(key_list):
    """Find the last page

    Args:
        key_list (list): List of keys

    Returns:
        integer: Page number
    """
    high = 0
    for x in key_list:
        if x.page > high:
            high = x.page
    return high

def write_key_config(key, page, cfg, value):
    """Write value for a given config for a given key.

    Args:
        key (Key): A key
        page (integer): Page number
        cfg (string): config to write
        value (string): value to write
    """
    keysdir = os.path.expanduser(read_config("keys_dir"))
    logger.debug(f"{keysdir} is the keys directory.")
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f))]
    logger.debug(f"key files found: {keyfiles}")
    cfg_file = None
    for f in keyfiles:
        logger.debug(f"Parsing {f}...")
        with FileLock(f"{os.path.join(keysdir, f)}.lock"):
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
        with FileLock(f"{os.path.join(keysdir, cfg_file)}.lock"):
            with open(os.path.join(keysdir, cfg_file), "w+", encoding='utf-8') as jsonFile:
                logger.debug(f"Writing modifications to {os.path.join(keysdir, cfg_file)}, Key {key}, {cfg} -> {value}")
                for x in data:
                    if x["key"] == key and x["page"] == page:
                        logger.debug(f"Assigning {x[cfg]} to {value}")
                        x[cfg] = value
                if os.path.splitext(os.path.join(keysdir, cfg_file))[1] in [".yml", ".yaml"]:
                    logger.debug("Converting to YAML")
                    logger.debug(f"Writing '{data}'")
                    yaml.dump(data, jsonFile, allow_unicode=True, sort_keys=False)
                else:
                    logger.debug(f"Writing '{data}'")
                    json.dump(data, jsonFile, indent=2, ensure_ascii=False)
    else:
        logger.error(f"Could not find a match for key {key} on page {page}.")

def empty_set(key_count, page):
    """Creates empty keys

    Args:
        key_count (integer): Number of keys to generate
        page (integer): The page to assign to generated keys

    Returns:
        list: A list of empty keys
    """
    ks = []
    for k in range(key_count):
        ks.append(fake_key(k, "empty", page))
    return ks
