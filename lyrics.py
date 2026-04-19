import requests
import json
import os

CACHE = "cache.json"

def load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, "r", encoding="utf-8"))
    return {"lyrics": {}}

def save(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), indent=2)

cache = load()

def get(artist, title):
    key = f"{artist}-{title}"

    if key in cache["lyrics"]:
        return cache["lyrics"][key]

    r = requests.get(
        f"https://lrclib.net/api/search?track_name={title}&artist_name={artist}"
    )

    data = r.json()
    if not data:
        return []

    raw = data[0].get("syncedLyrics") or ""

    parsed = []
    for line in raw.split("\n"):
        if "]" not in line:
            continue
        t, text = line.split("]")
        t = t.replace("[", "")
        m, s = t.split(":")
        sec = float(m)*60 + float(s)
        parsed.append((sec, text.strip()))

    cache["lyrics"][key] = parsed
    save(cache)
    return parsed