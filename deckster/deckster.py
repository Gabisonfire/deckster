import os
import threading
import importlib
import importlib.util

from common.configs import max_page, read_keys, read_config, write_key_config, find_key, write_config
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ICONS_DIR = read_config("icons_dir")
PLUGINS_DIR = read_config("plugins_dir")
PLUGINS_DIR = os.path.expanduser(PLUGINS_DIR)
PAGE = read_config("current_page")

def render_key_image(deck, icon_filename, font_filename, label_text):
    icon = Image.open(os.path.join(ICONS_DIR, icon_filename))
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")
    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, pressed):
    # If button is type toggle and is pressed, show pressed or default based on state, invert state
    if key.button_type == "toggle" and pressed:
        if not key.toggle_state:
            icon = key.icon_pressed
        else:
            icon = key.icon_default
        write_key_config(key, "toggle_state", not key.toggle_state)
    
    # If button is toggle, not pressed and in "on" state, keep pressed
    elif key.button_type == "toggle" and not pressed and key.toggle_state:
        icon = key.icon_pressed
    # If push button
    else:
        icon = key.icon_pressed if pressed else key.icon_default
    if key.page == PAGE:
        image = render_key_image(deck, icon, key.font, key.label)
        with deck:
            deck.set_key_image(key.key, image)

def key_change_callback(deck, key_num, pressed):
    print("Deck {} Key {} = {}".format(deck.id(), key_num, pressed), flush=True)
    current_page = read_config("current_page")
    key = find_key(key_num, current_page, read_keys())
    # If the key is blank, don't do anything
    if key == None:
        return
    update_key_image(deck, key, pressed)
    if pressed:
        if key.plugin.startswith("builtins."):
            plugin = importlib.import_module("plugins." + key.plugin, None)
        else:           
           spec = importlib.util.spec_from_file_location(key.plugin.split(".")[-1], os.path.join(PLUGINS_DIR, key.plugin.replace(".", "/") + ".py"))
           plugin = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(plugin)
        state = {
            "deck": deck, 
            "key": key.to_json(),
            "pressed": pressed
        }
        plugin.main(state)

def draw_deck(deck, increment = 0):
    deck.reset()
    change_page(increment)
    for k in read_keys():
        update_key_image(deck, k, False)
         
def change_page(increment):
    max = max_page(read_keys())
    global PAGE
    if PAGE + increment > max:
        PAGE = 1
    elif PAGE + increment < 1:
        PAGE = max
    else:
        PAGE += increment
    write_config("current_page", PAGE)

def main():
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))
        deck.set_brightness(100)

        draw_deck(deck)

        deck.set_key_callback(key_change_callback)

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            if t.is_alive():
                t.join()

if __name__ == "__main__":    
    main()