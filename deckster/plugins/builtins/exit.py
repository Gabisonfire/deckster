def main(state, args):
    deck = state["deck"]
    print("Bye")
    with deck:
        deck.reset()
        deck.close()