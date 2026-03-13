from commands import shutdown_pc, restart_pc, sleep_pc, minimize_all_windows, restore_all_windows

def handle_pc_commands(intent, value=None, voice=True):
    if intent == "shutdown":
        shutdown_pc(voice=voice)
        return True
    if intent == "restart":
        restart_pc(voice=voice)
        return True
    if intent == "sleep":
        sleep_pc(voice=voice)
        return True
    if intent == "minimize_all":
        minimize_all_windows(voice=voice)
        return True
    if intent == "restore_all":
        restore_all_windows(voice=voice)
        return True
    return False