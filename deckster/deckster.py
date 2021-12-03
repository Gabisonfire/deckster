import os, re, io
import threading
import logging
import importlib
import importlib.util
import common.configs as cfg
from common.scheduler import toggle_job
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ICONS_DIR = cfg.read_config("icons_dir")
PLUGINS_DIR = cfg.read_config("plugins_dir")
PLUGINS_DIR = os.path.expanduser(PLUGINS_DIR)
PAGE = cfg.read_config("current_page")
__version__ = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', io.open('__init__.py', encoding='utf_8_sig').read()).group(1)

if __name__ == "__main__":
    logger = logging.getLogger("deckster")
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(cfg.read_config("loglevel").upper())
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s - %(message)s', datefmt='%y-%m-%d,%H:%M:%S')
    console.setFormatter(formatter)
    logger.addHandler(console)

    logger.debug(f"Icons path: {ICONS_DIR}")
    logger.debug(f"Plugins path: {PLUGINS_DIR}")
    logger.debug(f"Current page: {PAGE}")
else:
    logger = logging.getLogger("deckster")

def render_key_image(deck, icon_filename, key):
    logger.debug(f"Rendering image for key:{key.key} with {icon_filename}")
    bottom_margin = 0 if key.label == "@hide" else 20
    if not icon_filename == "@hide":
        path = os.path.join(ICONS_DIR, icon_filename)
        if os.path.isfile(path):
            icon = Image.open(path)
        else:
            logger.error(f"File '{path}' does not exist.")
            raise FileNotFoundError(f"File '{path}' does not exist.")
        image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, bottom_margin, 0])
    else:
        image = PILHelper.create_image(deck)

    #
    if icon_filename == "@hide" and hasattr(key, 'label_ext'):
        image2 = PILHelper.create_image(deck)
        image = image.resize((image.width, int(image.height * 0.75)))
        image2 = image2.resize((image.width, int(image.height * 0.25)))
        draw2 = ImageDraw.Draw(image2)
    
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(key.font, key.font_size)
    actual_text = "" if key.label == "@hide" else key.label

    #
    if icon_filename == "@hide" and hasattr(key, 'label_ext'):
        print("here")
        draw2.text((image2.width / 2, image2.height - key.label_offset), text=key.label_ext, font=font, anchor="ms", fill=key.label_color)

    logger.debug(f"Label set for:{key.key} to '{actual_text}'")
    if not key.label == "@hide" and icon_filename == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    elif not key.label == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    
    if icon_filename == "@hide" and hasattr(key, 'label_ext'):
        image.paste(image2)

    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, pressed, blank = False):
    logger.debug(f"Updating image for key:{key.key}")
    icon = handle_button_icon(key, pressed)
    if key.page == PAGE or blank:
        if not blank:
            image = render_key_image(deck, icon, key)
        else:
            image = None
        with deck:
            deck.set_key_image(key.key, image)

def handle_button_icon(key, pressed):
    logger.debug(f"Handling icon state for key:{key.key} -> '{'pressed' if pressed else 'released'}'")
    # If button is a toggle and is pressed, store new state.
    if (key.button_type == "toggle" or key.button_type == "timer_toggle") and pressed:
        key.toggle()
        update_key_state(key)
        if not key.toggle_state:
            return key.icon_pressed
        else:
            return key.icon_default
    
    # If button is toggle, not pressed and in "on" state, keep pressed
    elif (key.button_type == "toggle" or key.button_type == "timer_toggle") and not pressed and key.toggle_state:
        return key.icon_pressed

    # If push button
    else:
        return key.icon_pressed if pressed else key.icon_default

def key_change_callback(deck, key_num, pressed):
    if pressed:
        logger.info(f"Callback triggered for key:{key_num} -> 'pressed'")
    else:
        logger.debug(f"Callback triggered for key:{key_num} -> 'released'")
    current_page = cfg.read_config("current_page")
    logger.debug(f"Current page is {current_page}")
    key = cfg.find_key(key_num, current_page, cfg.read_keys())

    # If the key is blank, don't do anything
    if key == None or key.button_type == "timer_on":
        return
    if key.button_type == "timer_toggle" and pressed:
        key.toggle()
        update_key_state(key)
        toggle_job(f"{key.key}{key.page}", key.toggle_state)
        return

    handle_button_action(deck, key, pressed)
    update_key_image(deck, key, pressed)
    

def handle_button_action(deck, key, pressed):
    if pressed:
        if key.plugin.startswith("builtins."):
            logger.debug(f"Importing builtin plugin 'plugins.{key.plugin}'")
            plugin = importlib.import_module(f"plugins.{key.plugin}", None)
        else:
            path =  os.path.join(PLUGINS_DIR, key.plugin.replace(".", "/") + ".py")
            if os.path.isfile(path):
                spec = importlib.util.spec_from_file_location(key.plugin.split(".")[-1], path)
                plugin = importlib.util.module_from_spec(spec)
                logger.debug(f"Importing custom '{plugin}' from '{path}'")
                spec.loader.exec_module(plugin)
            else:
                logger.error(f"File '{path}' does not exist.")
                raise FileNotFoundError(f"File '{path}' does not exist.")
        return plugin.main(deck, key, pressed)

def draw_deck(deck, increment = 0, init_draw = False):
    logger.debug(f"Drawing deck. {'INIT' if init_draw else ''}")
    clear(deck)
    change_page(increment)
    for k in cfg.read_keys():
        if k.button_type.startswith("timer") and init_draw:
            k.schedule_timer(deck, cfg.read_config("plugin_dir"))
        update_key_image(deck, k, False)
         

def clear(deck):
    logger.debug(f"Clearing deck.")
    keys = cfg.empty_set(deck.key_count())
    for k in keys:
        update_key_image(deck, k, False, True)

def change_page(increment):
    max = cfg.max_page(cfg.read_keys())
    logger.debug(f"Changing to page")
    global PAGE
    if PAGE + increment > max:
        PAGE = 1
    elif PAGE + increment < 1:
        PAGE = max
    else:
        PAGE += increment
    logger.debug(f"Changing to page {PAGE}/{max}")
    cfg.write_config("current_page", PAGE)

def update_label(key):
    logger.debug(f"Writing label for key {key.key} -> {key.label}")
    cfg.write_key_config(key.key , key.page, "label", key.label)

def update_key_state(key):
    cfg.write_key_config(key.key , key.page, "toggle_state", key.toggle_state)

def main():
    logger.info(f"Deckster v{__version__}")
    logger.info(f"Initializing...")
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        logger.debug(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}')")
        deck.set_brightness(cfg.read_config("brightness"))

        draw_deck(deck, init_draw=True)

        deck.set_key_callback(key_change_callback)

        logger.info(f"Ready.")
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            if t.is_alive():
                t.join()

if __name__ == "__main__":    
    main()