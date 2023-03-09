import os
import logging
import importlib
import deckster.common.configs as cfg
from PIL import Image, ImageDraw, ImageFont
from deckster.common.scheduler import toggle_job
from StreamDeck.ImageHelpers import PILHelper

ICONS_DIR = cfg.read_config("icons_dir")
PLUGINS_DIR = os.path.expanduser(cfg.read_config("plugins_dir"))
PAGE = cfg.read_config("current_page")
__version__ = cfg.__version__

class deck_vault:
    """Holds the current Deck object statically.
    """
    deck = None

logger = logging.getLogger("deckster")

def render_key_image(deck, icon_filename, key):
    """Renders the given image on a key

    Args:
        deck (deck): The deck
        icon_filename (string): Filename for the icon
        key (Key): The key to render the image on

    Raises:
        FileNotFoundError: Icon file path is invalid

    Returns:
        StreamDeck Image: An image renderable by the StreamDeck
    """
    logger.debug(f"Rendering image for key:{key.key} with {icon_filename}")
    bottom_margin = 0 if key.label == "@hide" else 20
    if not icon_filename == "@hide" and not icon_filename == "@display":
        path = os.path.expanduser(os.path.join(ICONS_DIR, icon_filename))
        if os.path.isfile(path):
            icon = Image.open(path)
        else:
            logger.error(f"File '{path}' does not exist.")
            raise FileNotFoundError(f"File '{path}' does not exist.")
        image = PILHelper.create_scaled_image(deck, icon, margins=[0 + key.padding[0], 0 + key.padding[1], bottom_margin + key.padding[2], 0 + key.padding[3]])
    else:
        image = PILHelper.create_image(deck)

    # If we use a "display" type icon, create it here.
    if icon_filename == "@display":
        logger.debug(f"Creating display type image for key:{key.key}.")
        display = PILHelper.create_image(deck)
        image = image.resize((image.width, int(image.height * 0.25)))
        display = display.resize((display.width, int(display.height * 0.75)))
        draw_display = ImageDraw.Draw(display)
        display_font = ImageFont.truetype(key.display_font, key.display_size)
        draw_display.text((display.width / 2, (display.height /2) + key.display_offset), text=key.display, font=display_font, anchor="ms", fill=key.display_color)
    
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(key.font, key.font_size)
    if key.label_truncate > 0:
            key.label = key.label[0:key.label_truncate]
    actual_text = "" if key.label == "@hide" else key.label

    logger.debug(f"Label set for:{key.key} to '{actual_text}'")
    if not key.label == "@hide" and icon_filename == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    elif not key.label == "@hide":
        draw.text((image.width / 2, image.height - key.label_offset), text=actual_text, font=font, anchor="ms", fill=key.label_color)
    
    # If we want a label and a display, paste images onto eachother
    if icon_filename == "@display":
        final_image = PILHelper.create_image(deck)
        final_image.paste(display, (0,0))
        final_image.paste(image, (0, display.size[1]))
    else:
        final_image = image

    return PILHelper.to_native_format(deck, final_image)

def update_key_image(deck, key, pressed, blank = False):
    """Update the image on a key

    Args:
        deck (deck): The deck
        key (Key): Key to update
        pressed (bool): True if the key was pressed
        blank (bool, optional): Creates a blank image. Defaults to False.
    """
    if not key.plugin == "empty":
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
    """Decides which image to display depending on the state and type of the button

    Args:
        key (Key): The key activated
        pressed (bool): The status of the button

    Returns:
        string: An icon name
    """
    if not key.plugin == "empty":
        logger.debug(f"Handling icon state for key:{key.key} -> '{'pressed' if pressed else 'released'}'")
    # If button is a toggle and is pressed, store new state.
    if (key.button_type == "toggle" or key.button_type == "timer_toggle") and pressed:
        key.toggle()
        update_key_state(key)
        if not key.toggle_state:
            return key.icon_default
        else:
            return key.icon_pressed
    
    # If button is toggle, not pressed and in "on" state, keep pressed
    elif (key.button_type == "toggle" or key.button_type == "timer_toggle") and not pressed and key.toggle_state:
        return key.icon_pressed

    # If push button
    else:
        return key.icon_pressed if pressed else key.icon_default

def key_change_callback(deck, key_num, pressed):
    """Function called when a button is pressed

    Args:
        deck (deck): The deck
        key_num (integer): Index of the key activated
        pressed (bool): True for pressed, false for released
    """
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
    """Handles the action triggered by the key callback

    Args:
        deck (deck): The deck
        key (Key): The triggered key
        pressed (bool): The state of the button

    Raises:
        FileNotFoundError: Raised when a plugin is not found

    Returns:
        func: The main function of the plugin
    """
    if pressed:
        if key.plugin.startswith("builtins."):
            logger.debug(f"Importing builtin plugin 'plugins.{key.plugin}'")
            plugin = importlib.import_module(f"deckster.plugins.{key.plugin}", None)
        else:
            path =  os.path.join(PLUGINS_DIR, key.plugin.replace(".", "/") + ".py")
            if os.path.isfile(path):
                spec = importlib.util.spec_from_file_location(key.plugin.split(".")[-1], path)
                plugin = importlib.util.module_from_spec(spec)
                logger.debug(f"Importing custom '{plugin}'")
                spec.loader.exec_module(plugin)
            else:
                logger.error(f"File '{path}' does not exist.")
                raise FileNotFoundError(f"File '{path}' does not exist.")
        return plugin.main(deck, key, pressed)

def draw_deck(deck, increment = 0, init_draw = False, enable_scheduler = True):
    """Draws the deck

    Args:
        deck (deck): The deck
        increment (int, optional): How many pages to increment. Defaults to 0.
        init_draw (bool, optional): True if it's the first time the deck is drawn. Defaults to False.
        enable_scheduler (bool, optional): Enable the scheduler or not. Defaults to True.
    """
    deck_vault.deck = deck
    logger.debug(f"Drawing deck. {'INIT' if init_draw else ''}")
    clear(deck)
    if not init_draw:
        change_page(increment)
    for k in cfg.read_keys():
        if k.button_type.startswith("timer") and init_draw and enable_scheduler:
            k.schedule_timer(deck, cfg.read_config("plugins_dir"))
        update_key_image(deck, k, False)
         
def clear(deck, page = 1):
    """Clears the deck, filling it with empty keys.

    Args:
        deck (deck): The deck
        page (int, optional): Page to clear. Defaults to 1.
    """
    logger.debug(f"Clearing deck.")
    keys = cfg.empty_set(deck.key_count(), page)
    for k in keys:
        update_key_image(deck, k, False, True)

def change_page(increment):
    """Changes page.

    Args:
        increment (integer): For how many pages to move
    """
    max = cfg.max_page(cfg.read_keys())
    global PAGE
    if PAGE + increment > max:
        PAGE = 1
    elif PAGE + increment < 1:
        PAGE = max
    else:
        PAGE += increment
    logger.debug(f"Changing to page {PAGE}/{max}")
    cfg.write_config("current_page", PAGE)

def update_label_display(key, label=False):
    """Writes the current text for a label or a display.

    Args:
        key (Key): Key to update
        label (bool, optional): Should be set to true if writing a display, false for a label. Defaults to False.
    """
    logger.debug(f"Writing {'label' if label  else 'display'} for key {key.key} -> {key.label if label else key.display}")
    cfg.write_key_config(key.key , key.page, 'label' if label else 'display', key.label if label else key.display)

def update_key_state(key):
    """Writes the current toggle state of a key.

    Args:
        key (Key): Key to save
    """
    cfg.write_key_config(key.key , key.page, "toggle_state", key.toggle_state)

def _load_modules():
    logger.info("Loading modules...")
    modules = cfg.read_config("modules")
    if modules == None: return
    for module in modules:
        logger.debug(f"Importing module: {module}")
        importlib.import_module(f"deckster.modules.{module}")

def reload(deck):
    """Reload the deck

    Args:
        deck (deck): The deck
    """
    draw_deck(deck, init_draw=True)

def _run_once(deck):
    """Executes run_once on all plugins

    Args:
        deck (deck): The deck
    """
    logger.info("Running plugins 'run_once'...")
    plugins = []
    builtins = []
    for key in cfg.read_keys():
        if key.plugin.startswith("builtins."):
            builtins.append(key)
        else:
            path = os.path.join(PLUGINS_DIR, key.plugin.replace(".", "/") + ".py")
            if os.path.isfile(path):
                plugins.append(key)
    for b in builtins:
        logger.debug(f"Executing run_once for key: {b.key}, plugin: {b.plugin}")
        plugin = importlib.import_module(f"deckster.plugins.{b.plugin}", None)
        try:
            ro = getattr(plugin, "run_once")
            ro(deck, b)
        except AttributeError as e:
            logger.debug(f"Key {b.key}: {e}")
            continue
        except Exception as e:
            logger.error(e)
    for p in plugins:
        logger.debug(f"Executing run_once for key: {p.key}, plugin: {p.plugin}")
        true_path = os.path.join(PLUGINS_DIR, p.plugin.replace(".", "/") + ".py")
        spec = importlib.util.spec_from_file_location(p.plugin.split(".")[-1], true_path)
        m = importlib.util.module_from_spec(spec)
        try:
            ro = getattr(m, "run_once")
            ro(deck, p)
        except AttributeError as e:
            logger.debug(f"Key {p.key}: {e}")
            continue
        except Exception as e:
            logger.error(e)
