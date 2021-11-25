def main(state):
    deck = state["deck"]
    print("Bye")
    with deck:
        deck.reset()
        deck.close()