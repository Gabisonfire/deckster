import json
import subprocess

def main(state):
    args = json.loads(state["key"])["args"]
    subprocess.run(args["command"])