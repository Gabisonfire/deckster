import os
import sys
import threading
import logging
import signal
import time
import deckster.common.configs as cfg
from deckster.common.core import draw_deck, key_change_callback, _load_modules, _run_once
from deckster.generators import generators
from deckster.common.scheduler import stop_jobs
from StreamDeck.DeviceManager import DeviceManager

ICONS_DIR = cfg.read_config("icons_dir")
PLUGINS_DIR = os.path.expanduser(cfg.read_config("plugins_dir"))
PAGE = cfg.read_config("current_page")
__version__ = cfg.__version__


logger = logging.getLogger("deckster")
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler(sys.stdout)
console.setLevel(cfg.read_config("loglevel").upper())
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s - %(message)s', datefmt='%y-%m-%d,%H:%M:%S')
console.setFormatter(formatter)
logger.addHandler(console)
logger.debug(f"Icons path: {ICONS_DIR}")
logger.debug(f"Plugins path: {PLUGINS_DIR}")
logger.debug(f"Current page: {PAGE}")

def main():
    logger.info(f"Deckster v{__version__}")
    logger.info(f"Initializing...")
    streamdecks = DeviceManager().enumerate()
    while len(streamdecks) == 0:        
        logger.info("No Stream Deck found, retrying in 10 seconds.")
        time.sleep(10)
        streamdecks = DeviceManager().enumerate()
    deck = streamdecks[0]

    def graceful_shutdown(sig, frame):
        stop_jobs()
        logger.info("Bye")
        with deck:
            deck.reset()
            deck.close()
        sys.exit(0)

    cfg.write_config("max_keys", deck.key_count())        
    generators.execute_generators()
    #for index, deck in enumerate(streamdecks):
    deck.open()
    deck.reset()
    signal.signal(signal.SIGTERM, graceful_shutdown)
    logger.debug(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}')")
    deck.set_brightness(cfg.read_config("brightness"))
    draw_deck(deck, init_draw=True)
    deck.set_key_callback(key_change_callback)
    _run_once(deck)
    logger.info("Ready.")
    _load_modules()
    for t in threading.enumerate():
        if t is threading.current_thread():
            continue
        if t.is_alive():
            t.join()
    

if __name__ == "__main__":    
    main()
