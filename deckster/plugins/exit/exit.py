from StreamDeck.DeviceManager import DeviceManager

def main(args):
    deck = args[0]
    print("Bye")
    with deck:
        deck.reset()
        deck.close()