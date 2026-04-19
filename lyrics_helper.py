import requests
import re

def get_synced_lyrics(track_name):
    url = f"https://lrclib.net/api/search?q={track_name}"
    try:
        response = requests.get(url).json()
        if response and 'syncedLyrics' in response[0]:
            return parse_lrc(response[0]['syncedLyrics'])
    except Exception as e:
        print(f"Lyrics fetch error: {e}")
        return None
    return None

def parse_lrc(lrc_content):
    lyric_data = []
    lines = lrc_content.splitlines()
    for line in lines:
        # Match [mm:ss.xx] text
        match = re.search(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)', line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            text = match.group(3).strip()
            lyric_data.append({"time": minutes * 60 + seconds, "text": text})
    return lyric_data   