import flet as ft
from flet.audio import Audio 
from audio_engine import AudioEngine
from lyrics_helper import get_synced_lyrics

def main(page: ft.Page):
    page.title = "VIAMP"
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.window_width, page.window_height = 1100, 800
    
    engine = AudioEngine()
    current_lyrics = []
    last_index = -1
    is_playing = False

    # UI Components
    lyrics_list = ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True, spacing=25, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    search_bar = ft.TextField(hint_text="Search song or paste URL...", expand=True, border_radius=20)
    album_art = ft.Image(src="https://via.placeholder.com/150", width=150, height=150, border_radius=10)
    song_title = ft.Text("No song playing", size=20, weight="bold", no_wrap=True)
    
    # Playback Controls
    play_button = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_ROUNDED, icon_size=50, on_click=lambda _: toggle_play())
    progress_slider = ft.Slider(min=0, max=100, value=0, expand=True, on_change_end=lambda e: seek_audio(e.data))
    time_text = ft.Text("00:00 / 00:00", size=12, color=ft.colors.WHITE70)
    
    audio_player = Audio(
        src="",
        autoplay=False,
        volume=1.0,
        on_position_changed=lambda e: update_position(int(e.data)),
        on_duration_changed=lambda e: set_duration(int(e.data))
    )
    page.overlay.append(audio_player)

    def set_duration(duration_millis):
        progress_slider.max = duration_millis
        page.update()

    def update_position(current_millis):
        # Update Slider
        progress_slider.value = current_millis
        
        # Update Time Label
        cur = format_time(current_millis)
        total = format_time(progress_slider.max)
        time_text.value = f"{cur} / {total}"
        
        # Update Lyrics logic
        nonlocal last_index
        current_sec = current_millis / 1000
        for i, line in enumerate(current_lyrics):
            if i < len(current_lyrics) - 1:
                if line["time"] <= current_sec < current_lyrics[i+1]["time"]:
                    if i != last_index:
                        highlight_lyric(i)
                        last_index = i
                    break
        page.update()

    def format_time(ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def toggle_play():
        nonlocal is_playing
        if is_playing:
            audio_player.pause()
            play_button.icon = ft.icons.PLAY_CIRCLE_FILL_ROUNDED
        else:
            audio_player.play()
            play_button.icon = ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED
        is_playing = not is_playing
        page.update()

    def seek_audio(value):
        audio_player.seek(int(float(value)))

    def highlight_lyric(index):
        for i, control in enumerate(lyrics_list.controls):
            control.color = ft.colors.WHITE if i == index else ft.colors.WHITE24
            control.size = 24 if i == index else 18
            control.weight = ft.FontWeight.BOLD if i == index else ft.FontWeight.NORMAL
        
        # Auto-scroll to the current lyric
        lyrics_list.scroll_to(key=str(index), duration=500, curve=ft.AnimationCurve.EASE_OUT)
        lyrics_list.update()

    def start_playback(e):
        if not search_bar.value: return
        
        search_bar.disabled = True
        page.update()
        
        data = engine.get_stream_url(search_bar.value)
        if not data:
            search_bar.disabled = False
            page.update()
            return
            
        nonlocal current_lyrics, last_index
        last_index = -1
        current_lyrics = get_synced_lyrics(data['title']) or []
        
        lyrics_list.controls = [
            ft.Text(l["text"], size=18, color="white24", text_align=ft.TextAlign.CENTER, key=str(i)) 
            for i, l in enumerate(current_lyrics)
        ]
        
        # Update Metadata
        song_title.value = data['title']
        album_art.src = data['thumbnail']
        audio_player.src = data['url']
        search_bar.disabled = False
        play_button.icon = ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED
        nonlocal is_playing
        is_playing = True
        audio_player.update()
        audio_player.play()
        page.update()

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([search_bar, ft.IconButton(icon=ft.icons.SEARCH, on_click=start_playback)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color="transparent"),
                ft.Row([album_art, ft.Column([song_title, time_text], spacing=5)], alignment=ft.MainAxisAlignment.START),
                ft.Container(content=lyrics_list, expand=True, padding=20),
                # Control Bar
                ft.Container(
                    content=ft.Column([
                        ft.Row([progress_slider]),
                        ft.Row([play_button], alignment=ft.MainAxisAlignment.CENTER),
                    ]),
                    padding=10,
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                    border_radius=20
                )
            ]),
            expand=True,
            padding=20
        )
    )