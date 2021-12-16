import os
import json
import vdf
import logging
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from deckster.common.configs import read_config

logger = logging.getLogger("deckster")
MAX_CON = 20
ICONS_DIR = os.path.expanduser(read_config("icons_dir"))
KEY_DIR = os.path.expanduser(read_config("keys_dir"))
KEY_FILENAME = "steam_generator.json"
MAX_KEYS = read_config("max_keys")

class App:
    def __init__(self, appid):
        self.appid = appid
        self.title = None
        self.icon_url = None
    
    def __str__(self):
        return f"{self.title}({self.appid})"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.title < other.title

def read_installed_apps(path):
    apps = []
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        logger.error(f"{path} not found.")
        return
    libs = vdf.load(open(path))
    for lib in libs["libraryfolders"]:
        if lib.isdigit():
            logger.debug(f"Found library: {libs['libraryfolders'][lib]}")
            for app in libs["libraryfolders"][lib]["apps"]:
                apps.append(App(app))
    return apps

def parse_app(app, download):
    page = requests.get(f"https://store.steampowered.com/app/{app.appid}/")
    parse = BeautifulSoup(page.content, 'html.parser')
    title = parse.find('span', {'itemprop' : 'name'})
    if title is not None:
        logger.debug(f"Found {title.text} for id {app.appid}")
        app.title = title.text
        icon_tag = parse.find('div', {'class', 'apphub_AppIcon'})
        if icon_tag is not None:
            icon_tag = icon_tag.findChildren("img")
            if icon_tag[0].get("src", False):
                app.icon_url = icon_tag[0]["src"]
                logger.debug(f"Found icon at {app.icon_url} for {app.title}")
                if download:
                    icon = requests.get(app.icon_url)
                    with open(os.path.join(ICONS_DIR, f"{app.appid}.png"), 'wb') as f:
                        f.write(icon.content)
        return app
    return None

def retreive_data(apps, download):
    parsed_apps = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CON) as executor:
        t = (executor.submit(parse_app, app, download) for app in apps)
        for future in concurrent.futures.as_completed(t):
            try:
                parsed = future.result()
                if parsed is not None:
                    parsed_apps.append(parsed)
            except Exception as exc:
                logger.error(str(type(exc)))
    executor.shutdown(wait=True)
    return parsed_apps

def write_keyfile(args, final_apps):
    keyfile = []
    start = 0
    limit = 100
    next = None
    previous = None
    add_navigation = False
    font = "Roboto-Regular.ttf"
    hide_label = False
    if "start" in args:
        start = args["start"]
    if "limit" in args:
        limit = args["limit"]
    if "hide_label" in args:
        hide_label = args["hide_label"]
    if "font" in args:
        font = args["font"]
    if "add_navigation" in args:
        add_navigation = args["add_navigation"]

    if add_navigation:
        next = {
            "key": args["next_key"],
            "page": args["page"],
            "plugin": "builtins.page.next",
            "icon_default":args["next_icon"],
            "label" : f"{'@hide' if hide_label else 'Next'}",
            "font": font,
            "button_type": "push"
        }
        previous = {
            "key": args["previous_key"],
            "page": args["page"],
            "plugin": "builtins.page.previous",
            "icon_default":args["previous_icon"],
            "label" : f"{'@hide' if hide_label else 'Previous'}",
            "font": font,
            "button_type": "push"
        }

    app_index = 0
    while start < limit:
        if start+1 > MAX_KEYS:
            logger.warning(f"The limit set of '{limit}' is higher than the number of keys: {MAX_KEYS}. Stopping. ({len(final_apps) - MAX_KEYS + 2 if add_navigation else 0} hidden)")
            break
        if add_navigation:
            if start == args["next_key"]:
                keyfile.append(next)
                start+=1
                continue
            elif start == args["previous_key"]:
                keyfile.append(previous)
                start+=1
                continue
        k = {
            "key": start,
            "page": args["page"],
            "plugin": "builtins.shell",
            "args": {
                "command": [
                "steam",
                f"steam://rungameid/{final_apps[app_index].appid}"
                ]
            },
            "icon_default": f"{final_apps[app_index].appid}.png",
            "label" : f"{'@hide' if hide_label else final_apps[app_index].title}",
            "font": font,
            "button_type": "push"
        }
        keyfile.append(k)
        start+=1
        app_index = app_index+1 if app_index+1 < len(final_apps) else -1
        if app_index == -1:
            logger.warning(f"The limit set of '{limit}' is higher than the number of applications found: {len(final_apps)}. Stopping.")
            # If we were not up to the navigation position, insert them here before breaking.
            if add_navigation and start < next["key"]:
                keyfile.append(next)
            if add_navigation and start < previous["key"]:
                keyfile.append(previous)
            break
    with open(os.path.join(KEY_DIR, KEY_FILENAME), 'w', encoding='utf-8') as f:
        json.dump(keyfile, f, ensure_ascii=False, indent=4)
        logger.info(f"{os.path.join(KEY_DIR, KEY_FILENAME)} written.")
    

def apply_filters(args, final_apps):
    if not "filters" in args:
        return
    filtered = []
    logger.debug(f"Active filters: {args['filters']}")
    logger.debug(f"Received list: {final_apps}, count:{len(final_apps)}")
    for app in final_apps:
        logger.debug(f"Checking {app.title} against filters...")
        if app.appid in args["filters"] or app.title in args["filters"]:
            logger.debug(f"{app.title}({app.appid}) matching filters, removing.")
            continue
        else:
            filtered.append(app)
    logger.debug(f"Returning list: {filtered}, count:{len(filtered)}")
    return filtered


def main(args):
    if os.path.isfile(os.path.join(KEY_DIR, KEY_FILENAME)):
        if "overwrite" in args and not args["overwrite"]:
            logger.info(f"{os.path.join(KEY_DIR, KEY_FILENAME)} already exists and 'overwrite' is false, skipping.")
            return
        if "overwrite" in args and args["overwrite"]:
            logger.info(f"{os.path.join(KEY_DIR, KEY_FILENAME)} already exists, overwriting.")
            
    if not "page" in args:
        logger.error("The 'page' argument is required.")
        return

    logger.debug(f"Steam generator arguments: {args}")

    apps = read_installed_apps(args["steam_lib"])
    logger.debug(f"Raw apps found: {apps}")

    logger.info("Retreiving data from Steam...")
    final_apps = retreive_data(apps, args["download_icons"])
    logger.info("Retreiving data complete.")

    final_apps = apply_filters(args, final_apps)
    
    logger.info("Writing key file...")
    if "sort_titles" in args and args["sort_titles"]:
        logger.debug("Sorting titles...")
        final_apps.sort()

    write_keyfile(args, final_apps)

