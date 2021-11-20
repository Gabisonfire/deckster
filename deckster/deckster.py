import os
import threading
import importlib

from common.configs import read_key_config, read_config, defined_keys
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
    key_style = get_key_style(key)
    icon = key_style["icon_pressed"] if pressed else key_style["icon_default"]
    image = render_key_image(deck, icon, key_style["font"], key_style["label"])
    with deck:
        deck.set_key_image(key, image)

def get_key_style(key):
    return {
        "name": read_key_config(key, "name"),
        "icon_default": read_key_config(key, "icon_default"),
        "icon_pressed": read_key_config(key, "icon_pressed"),
        "font": read_key_config(key, "font"),
        "label": read_key_config(key, "label"),
        "plugin": read_key_config(key, "plugin"),
        "args": read_key_config(key, "args")
    }

def key_change_callback(deck, key, pressed):
    print("Deck {} Key {} = {}".format(deck.id(), key, pressed), flush=True)
    update_key_image(deck, key, pressed)
    if pressed:
        key_style = get_key_style(key)

        plugin = importlib.import_module(f"plugins.{key_style['plugin']}.{key_style['plugin']}", None)
        args = key_style["args"]
        args.insert(0, deck)
        plugin.main(args)
         

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

main()