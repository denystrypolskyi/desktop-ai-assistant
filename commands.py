import os
import subprocess
import spotipy
import psutil
import ctypes
from pycaw.pycaw import AudioUtilities

from tts import speak_jarvis
from spotify_client import sp

def spotify_play(voice=True):
    devices = sp.devices()
    if not devices['devices']:
        if voice: speak_jarvis("No active Spotify devices found")
        print("No active Spotify devices found")
        return

    device_id = devices['devices'][0]['id']
    try:
        if voice: speak_jarvis("Turning on Spotify")
        sp.start_playback(device_id=device_id)
        print(f"Spotify playback started on device {device_id}")
    except spotipy.exceptions.SpotifyException as e:
        if voice: speak_jarvis("Failed to start Spotify playback")
        print(f"Failed to start Spotify playback: {e}")

def spotify_pause(voice=True):
    try:
        sp.pause_playback()
        if voice: speak_jarvis("Spotify playback paused")
        print("Spotify playback paused")
    except Exception as e:
        if voice: speak_jarvis("Failed to pause Spotify playback")
        print(f"Failed to pause Spotify: {e}")

def spotify_next(voice=True):
    try:
        sp.next_track()
        if voice: speak_jarvis("Next track")
        print("Spotify next track")
    except Exception as e:
        if voice: speak_jarvis("Failed to skip track")
        print(f"Failed to skip track: {e}")

def spotify_previous(voice=True):
    try:
        sp.previous_track()
        if voice: speak_jarvis("Previous track")
        print("Spotify previous track")
    except Exception as e:
        if voice: speak_jarvis("Failed to go to previous track")
        print(f"Failed to go to previous track: {e}")

def smart_play(query: str, voice=True):
    query = query.strip()
    if not query:
        return

    devices = sp.devices().get("devices", [])
    if not devices:
        if voice: speak_jarvis("No active Spotify devices found")
        print("No active Spotify devices found")
        return

    device_id = next((d["id"] for d in devices if d.get("is_active")), devices[0]["id"])
    tracks = sp.search(q=query, type="track").get("tracks", {}).get("items", [])
    if not tracks:
        if voice: speak_jarvis("Track not found")
        print("No tracks found")
        return

    track = tracks[0]
    try:
        sp.start_playback(device_id=device_id, uris=[track["uri"]], position_ms=0)
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        if voice: speak_jarvis(f"Currently playing: {track_name} — {artist_name}")
        print(f"Playing: {track_name} - {artist_name}")
    except Exception as e:
        if voice: speak_jarvis("Failed to start track")
        print("Failed to start track:", e)

APP_PATHS = {
    "discord": os.path.join(os.getenv("LOCALAPPDATA"), "Discord", "Update.exe"),
    "telegram": os.path.join(os.getenv("LOCALAPPDATA"), "Telegram Desktop", "Telegram.exe"),
    "spotify": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "WindowsApps", "Spotify.exe"),
    "chrome": os.path.join(os.getenv("PROGRAMFILES"), "Google", "Chrome", "Application", "chrome.exe"),
    "google": os.path.join(os.getenv("PROGRAMFILES"), "Google", "Chrome", "Application", "chrome.exe"),
}

WEB_APPS = {
    "youtube": "https://youtube.com",
    "twitch": "https://twitch.tv",
    "tiktok": "https://tiktok.com",
}

def run_app(path, voice=True):
    if not path or not os.path.exists(path):
        if voice: speak_jarvis(f"Program not found: {path}")
        print(f"Program not found: {path}")
        return
    try:
        subprocess.Popen(f'start "" "{path}"', shell=True)
        if voice: speak_jarvis(f"Opening application: {path}")
        print(f"Opened application: {path}")
    except Exception as e:
        if voice: speak_jarvis(f"Failed to open application: {path}")
        print(f"Failed to open application: {path}, {e}")

def close_app(exe_name, voice=True):
    exe_name = exe_name.lower().replace(".exe", "")
    found = False
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            proc_name = (proc.info['name'] or "").lower().replace(".exe", "")
            if proc_name == exe_name:
                proc.kill()
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if found:
        if voice: speak_jarvis(f"Closing {exe_name}")
        print(f"Closed application: {exe_name}")
    else:
        if voice: speak_jarvis(f"Application {exe_name} is not running")
        print(f"Application not running: {exe_name}")

def shutdown_pc(voice=True):
    if voice: speak_jarvis("Shutting down computer")
    os.system("shutdown /s /t 0") 
    print("Shutting down PC...")

def restart_pc(voice=True):
    if voice: speak_jarvis("Restarting computer")
    os.system("shutdown /r /t 0")
    print("Restarting PC...")

def sleep_pc(voice=True):
    if voice: speak_jarvis("Putting computer to sleep")
    try:
        ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
        print("PC is going to sleep...")
    except Exception as e:
        if voice: speak_jarvis("Failed to put computer to sleep")
        print("Failed to put PC to sleep:", e)

def minimize_all_windows(voice=True):
    try:
        HWND_BROADCAST = 0xFFFF
        WM_COMMAND = 0x111
        MIN_ALL = 419
        ctypes.windll.user32.PostMessageW(HWND_BROADCAST, WM_COMMAND, MIN_ALL, 0)
        if voice: speak_jarvis("All windows minimized")
        print("All windows minimized")
    except Exception as e:
        if voice: speak_jarvis("Failed to minimize all windows")
        print("Failed to minimize all windows:", e)

def restore_all_windows(voice=True):
    try:
        HWND_BROADCAST = 0xFFFF
        WM_COMMAND = 0x111
        MIN_ALL_UNDO = 416
        ctypes.windll.user32.PostMessageW(HWND_BROADCAST, WM_COMMAND, MIN_ALL_UNDO, 0)
        if voice: speak_jarvis("All windows restored")
        print("All windows restored")
    except Exception as e:
        if voice: speak_jarvis("Failed to restore all windows")
        print("Failed to restore all windows:", e)

def set_system_volume(percent, voice=True):
    percent = max(0, min(100, percent))
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
    if voice: speak_jarvis(f"Volume set to {percent} percent")
    print(f"Volume set to {percent}%")

def mute_system_volume(voice=True):
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    volume.SetMute(1, None)
    if voice: speak_jarvis("Turning off sound")
    print("System muted")

def unmute_system_volume(voice=True):
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    volume.SetMute(0, None)
    if voice: speak_jarvis("Sound turned on")
    print("System unmuted")