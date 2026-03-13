import os
import webbrowser
import subprocess
from commands import run_app, close_app, APP_PATHS, WEB_APPS, speak_jarvis

def handle_apps(intent, entity, voice=True):
    if intent == "open_app" and entity:
        if entity in APP_PATHS:
            path = APP_PATHS[entity]
            if os.path.exists(path):
                if entity == "discord":
                    subprocess.Popen([path, "--processStart", "Discord.exe"])
                else:
                    run_app(path, voice=voice)
                if voice: speak_jarvis(f"Opening {entity}")
                return True

        url = WEB_APPS.get(entity)
        if url:
            if voice: speak_jarvis(f"Opening {entity} in the browser")
            webbrowser.open(url)
            return True

        if voice: speak_jarvis(f"Cannot open {entity}")
        return True

    if intent == "close_app" and entity:
        exe_name = entity + ".exe"
        close_app(exe_name, voice=voice)
        return True

    return False