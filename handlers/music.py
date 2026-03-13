from commands import spotify_play, spotify_pause, spotify_next, spotify_previous, smart_play

def handle_music(intent, value=None, voice=True):
    if intent == "play_music":
        spotify_play(voice=voice)
        return True
    if intent == "pause_music":
        spotify_pause(voice=voice)
        return True
    if intent == "next_track":
        spotify_next(voice=voice)
        return True
    if intent == "previous_track":
        spotify_previous(voice=voice)
        return True
    if intent == "play_track" and value: 
        smart_play(value, voice=voice)
        return True
    return False