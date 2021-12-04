import logging
from deckster.common.scheduler import stop_jobs

logger = logging.getLogger("deckster")

def main(deck, key, pressed):
    stop_jobs()
    logger.info("Bye")
    with deck:
        deck.reset()
        deck.close()