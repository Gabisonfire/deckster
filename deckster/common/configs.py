import json
import os
import yaml
from pathlib import Path
from common.keys import Key

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(dir_path).parent.parent

def read_config(cfg):
    try:
        cfg_file = json.load(open(os.path.join(dir_path, "config.json")))
    except Exception as e:
        print(f"{os.path.join(dir_path, 'config.json')} contains invalid JSON. ({e})")

    for k in cfg_file:
        if k == cfg:
            return cfg_file[k]

def write_config(cfg, value):
    with open(os.path.join(dir_path, "config.json"), "r") as cfgFile:
        data = json.load(cfgFile)
        data[cfg] = value
    with open(os.path.join(dir_path, "config.json"), "w") as cfgFile:
        json.dump(data, cfgFile, indent=2)

def read_keys():
    templist = []
    keysdir = read_config("keys_dir")
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f))]
    json_keys = []
    for files in keyfiles:
        try:
            if os.path.splitext(files)[1] in [".yaml", ".yml"]:
                y = yaml.safe_load(open(os.path.join(keysdir, files)))                
                tmp_json = json.loads(json.dumps(y))
            else:
                tmp_json = json.load(open(os.path.join(keysdir, files)))
            for k in tmp_json:
                json_keys.append(k)
        except Exception as e:
            print(f"Error parsing {os.path.join(keysdir, files)}: {e}")   
    for x in json_keys:
        templist.append(Key(x))
    return templist

def find_key(key, page, key_list):
    for x in key_list:
        if x.key == key and x.page == page:
            return x

def max_page(key_list):
    high = 0
    for x in key_list:
        if x.page > high:
            high = x.page
    return high

#configs.write_key_config(3 , 1, "label", patate)

def write_key_config(key, page, cfg, value):
    keysdir = read_config("keys_dir")
    keyfiles = [f for f in os.listdir(keysdir) if os.path.isfile(os.path.join(keysdir, f))]
    cfg_file = None
    for f in keyfiles:
        print(f"parsing {f}")
        with open(os.path.join(keysdir, f), "r") as jsonFile:
            if os.path.splitext(f)[1] in [".yml", ".yaml"]:
                y = yaml.safe_load(jsonFile)
                data = json.loads(json.dumps(y))
            else:
                data = json.load(jsonFile)
            for x in data:
                if x["key"] == key and x["page"] == page:
                    print(f"Key {key} on page {page} belongs to {f}")
                    cfg_file = f
                    break
            else:                
                continue
            break
    if cfg_file is not None:
        with open(os.path.join(keysdir, cfg_file), "w") as jsonFile:
            print(f"Writing {key} -> {cfg} : {value}")
            for x in data:
                if x["key"] == key and x["page"] == page:
                    x[cfg] = value
            if os.path.splitext(os.path.join(keysdir, cfg_file))[1] in [".yml", ".yaml"]:
                yaml.dump(data, jsonFile, allow_unicode=True, sort_keys=False)
            else:
                print("wat")
                json.dump(data, jsonFile, indent=2)

def empty_set(key_count):
    ks = []
    for k in range(key_count):
        x = {
            "key": k,
            "page": 1,
            "plugin": "builtins.web.post",
            "icon_default": "web.png",
            "button_type": "toggle"
        }
        ks.append(Key(x))
    return ks