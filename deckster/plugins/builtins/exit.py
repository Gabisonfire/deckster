from common.scheduler import stop_jobs

def main(deck, key, pressed):
    stop_jobs()
    print("Bye")
    with deck:
        deck.reset()
        deck.close()