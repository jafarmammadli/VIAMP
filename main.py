import time
from player import start, get_time
from search import yt_search
from lyrics import get as get_lyrics
from ui import render
from rich.live import Live

current = []

def play(query):
    global current

    url = yt_search(query)
    start(url)

    parts = query.split()
    artist = parts[0]
    title = " ".join(parts[1:])

    current = get_lyrics(artist, title)

    run_ui()

def run_ui():
    with Live(refresh_per_second=20) as live:
        while True:
            t = get_time()
            live.update(render(current, t))
            time.sleep(0.05)

def repl():
    print("YT CLI v4 — Spicy Lyrics Mode")
    print("commands: play <song>, exit")

    while True:
        cmd = input("ytm> ")

        if cmd.startswith("play "):
            play(cmd[5:])

        elif cmd == "exit":
            break

        else:
            print("invalid command")

if __name__ == "__main__":
    repl()