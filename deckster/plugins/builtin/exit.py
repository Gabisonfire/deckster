def main(state, args):
    deck = state[0]
    print("Bye")
    with deck:
        deck.reset()
        deck.close()