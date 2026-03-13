from commands import set_system_volume, mute_system_volume, unmute_system_volume

def handle_volume(intent, value=None, voice=True):
    if intent == "set_volume" and value is not None:
        set_system_volume(value, voice=voice)
        return True
    if intent == "mute_volume":
        mute_system_volume(voice=voice)
        return True
    if intent == "unmute_volume":
        unmute_system_volume(voice=voice)
        return True
    return False