import logging
from deckster.common.core import clear, key_change_callback, draw_deck, update_key_image
from deckster.common.configs import _counter
from deckster.common.keys import fake_key

logger = logging.getLogger("deckster")

combination = []

def unlock(deck):
    draw_deck(deck, init_draw=True, enable_scheduler=False)
    deck.set_key_callback(key_change_callback)

# Used by the api
def lock(deck, user_combination, key_on_lock, icon):
    global combination
    counter.count = 0
    combination = user_combination
    deck.set_key_callback(locked)
    clear(deck)
    k = fake_key(key_on_lock, icon)
    k.label = "@hide"
    print(k.to_json())
    update_key_image(deck, k, False)
    return

def blank_lock(deck):
    clear(deck)
    deck.set_key_callback(nothing)

def nothing(_a, _b, _c):
    return

def locked(deck, key_num, pressed):
    if not pressed: return
    if combination[counter.count] == key_num:
        if counter.count == len(combination) - 1:
            logger.info("Deck unlocked.")
            unlock(deck)
        else:
            logger.info("The deck is locked.")
            counter.count += 1
    else:
        logger.info("The deck is locked.")
        counter.count = 0

def main(deck, key, pressed):
    if pressed:
        global combination
        counter.count = 0
        combination = key.args["combination"]
        deck.set_key_callback(locked)
        key.key = key.args["key_on_lock"]
        clear(deck, key.page)