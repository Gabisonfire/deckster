import json
from playsound import playsound

def main(state):
    args = json.loads(state["key"])["args"]
    playsound(args["sound"])