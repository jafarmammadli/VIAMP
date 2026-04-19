import yt_dlp

class AudioEngine:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }

    def get_stream_url(self, query: str):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            # Searches and gets the first result's URL
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return {
                    'url': info['url'],
                    'title': info['title'],
                    'thumbnail': info.get('thumbnail'),
                    'duration': info.get('duration')  # In seconds
                }
            except Exception as e:
                print(f"Error fetching audio: {e}")
                return None