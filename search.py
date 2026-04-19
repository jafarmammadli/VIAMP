from yt_dlp import YoutubeDL
import json
import os

CACHE = "cache.json"

def load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, "r", encoding="utf-8"))
    return {"search": {}, "lyrics": {}}

def save(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), indent=2)

cache = load()

def yt_search(q):
    if q in cache["search"]:
        return cache["search"][q]

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1"
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(q, download=False)
        url = info["entries"][0]["url"]

    cache["search"][q] = url
    save(cache)
    return url