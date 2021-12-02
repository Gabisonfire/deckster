from common.scheduler import stop_jobs

def main(state):
    deck = state["deck"]
    stop_jobs()
    print("Bye")
    with deck:
        deck.reset()
        deck.close()