import os
import threading
import importlib

from common.configs import read_key_config, read_config, defined_keys, write_key_config
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ICONS_DIR = read_config("icons_dir")

def render_key_image(deck, icon_filename, font_filename, label_text):
    icon = Image.open(os.path.join(ICONS_DIR, icon_filename))
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")
    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, pressed):
    key_config = get_key_config(key)
    # If button is type toggle and is pressed, show pressed or default based on state, invert state
    if key_config["button_type"] == "toggle" and pressed:
        if not key_config["toggle_state"]:
            icon = key_config["icon_pressed"]
        else:
          icon = key_config["icon_default"]  
        write_key_config(key, "toggle_state", not key_config["toggle_state"])
    
    # If button is toggle, not pressed and in "on" state, keep pressed
    elif key_config["button_type"] == "toggle" and not pressed and key_config["toggle_state"]:
        icon = key_config["icon_pressed"]
    # If push button
    else:
        icon = key_config["icon_pressed"] if pressed else key_config["icon_default"]
    image = render_key_image(deck, icon, key_config["font"], key_config["label"])
    with deck:
        deck.set_key_image(key, image)

def get_key_config(key):
    return {
        "name": read_key_config(key, "name"),
        "icon_default": read_key_config(key, "icon_default"),
        "icon_pressed": read_key_config(key, "icon_pressed"),
        "font": read_key_config(key, "font"),
        "label": read_key_config(key, "label"),
        "plugin": read_key_config(key, "plugin"),
        "args": read_key_config(key, "args"),
        "button_type": read_key_config(key, "button_type"),
        "toggle_state": read_key_config(key, "toggle_state")
    }

def key_change_callback(deck, key, pressed):
    print("Deck {} Key {} = {}".format(deck.id(), key, pressed), flush=True)
    update_key_image(deck, key, pressed)
    if pressed:
        key_config = get_key_config(key)
        plugin = importlib.import_module(f"plugins.{key_config['plugin']}", None)
        args = key_config["args"]
        state = {
            "deck": deck, 
            "key": key, 
            "key_config": key_config,
            "pressed": pressed
        }
        plugin.main(state, args)
         

def main():
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))
        deck.set_brightness(100)

        for key in range(defined_keys()):
            update_key_image(deck, key, False)

        deck.set_key_callback(key_change_callback)

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            if t.is_alive():
                t.join()

if __name__ == "__main__":    
    main()