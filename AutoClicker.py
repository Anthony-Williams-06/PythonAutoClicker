import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

def DelaySet():
    try:
        Delay = float(input("What is the delay time? "))
        return Delay
    except Exception:
        print("not a valid number")
        DelaySet()

delay = DelaySet()
button = Button.left
button2 = Button.right
start_stop_key = KeyCode(char='0')
start_2_key = KeyCode(char='1')
exit_key = KeyCode(char='`')

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)


class ClickMouseR(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()
clunk_thread = ClickMouseR(delay, button2)
clunk_thread.start()

def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
            
    elif key == start_2_key:
        if clunk_thread.running:
            clunk_thread.stop_clicking()
        else:
            clunk_thread.start_clicking()
            
            
    elif key == exit_key:
        click_thread.exit()
        clunk_thread.exit()
        listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()
