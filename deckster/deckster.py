import os
import threading
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

def render_key_image(deck, icon_filename, key):
    bottom_margin = 0 if key.label == "@hide" else 20
    if not icon_filename == "@hide":
        icon = Image.open(os.path.join(ICONS_DIR, icon_filename))
        image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, bottom_margin, 0])
    else:
        image = PILHelper.create_image(deck)
    
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(key.font, key.font_size)
    actual_text = "" if key.label == "@hide" else key.label
    if not key.label == "@hide" and icon_filename == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    elif not key.label == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    
    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, pressed, blank = False):
    icon = handle_button(key, pressed)
    if key.page == PAGE or blank:
        if not blank:
            image = render_key_image(deck, icon, key)
        else:
            image = None
        with deck:
            deck.set_key_image(key.key, image)

def handle_button(key, pressed):
    # If button is a toggle and is pressed, store new state.
    if (key.button_type == "toggle" or key.button_type == "timer_toggle") and pressed:
        key.toggle()
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
    print("Deck {} Key {}: {}".format(deck.id(), key_num, "Pressed" if pressed else "Released"), flush=True)
    current_page = cfg.read_config("current_page")
    key = cfg.find_key(key_num, current_page, cfg.read_keys())

    # If the key is blank, don't do anything
    if key == None or key.button_type == "timer_on":
        return
    if key.button_type == "timer_toggle" and pressed:
        key.toggle()
        toggle_job(f"{key.key}{key.page}", key.toggle_state)
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

def draw_deck(deck, increment = 0, init_draw = False):
    clear(deck)
    change_page(increment)
    for k in cfg.read_keys():
        if k.button_type.startswith("timer") and init_draw:
            k.schedule_timer(deck)
        update_key_image(deck, k, False)
         

def clear(deck):
    keys = cfg.empty_set(deck.key_count())
    for k in keys:
        update_key_image(deck, k, False, True)

def change_page(increment):
    max = cfg.max_page(cfg.read_keys())
    global PAGE
    if PAGE + increment > max:
        PAGE = 1
    elif PAGE + increment < 1:
        PAGE = max
    else:
        PAGE += increment
    cfg.write_config("current_page", PAGE)

def main():
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))
        deck.set_brightness(100)

        draw_deck(deck, init_draw=True)

        deck.set_key_callback(key_change_callback)

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            if t.is_alive():
                t.join()

if __name__ == "__main__":    
    main()