import subprocess
import socket
import json
import os

MPV_SOCKET = "mpv.sock"
process = None

def start(url):
    global process

    if os.path.exists(MPV_SOCKET):
        os.remove(MPV_SOCKET)

    process = subprocess.Popen([
        "mpv",
        "--no-video",
        f"--input-ipc-server={MPV_SOCKET}",
        "--quiet",
        url
    ])

def send(cmd):
    s = socket.socket(socket.AF_UNIX)
    s.connect(MPV_SOCKET)
    s.send((json.dumps(cmd) + "\n").encode())
    data = s.recv(4096)
    s.close()
    return json.loads(data)

def get_time():
    try:
        return send({"command": ["get_property", "time-pos"]})["data"]
    except:
        return 0