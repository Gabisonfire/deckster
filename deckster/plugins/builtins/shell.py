import subprocess

def main(deck, key, pressed):
    args = key.args
    subprocess.run(args["command"])