#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Threaded auto clicker

"Threaded Auto Clicker script"

# Programmed by BitMan64 with minor changes by CoolCat467

from __future__ import annotations

__title__ = 'Threaded Auto Clicker'
__author__ = 'BitMan64 & CoolCat467'
__version__ = '1.2.0'
__ver_major__ = 1
__ver_minor__ = 2
__ver_patch__ = 0


from typing import Final
import time
from threading import Thread

# lintcheck: import-error (E0401): Unable to import 'pynput.mouse'
from pynput.mouse import Button, Controller
# lintcheck: import-error (E0401): Unable to import 'pynput.keyboard'
from pynput.keyboard import Listener, KeyCode, Key


# To change back to original mode without clicks per second
# regulation, change REGULATE to False.
REGULATE: Final = True

TOGGLEDELAY: Final = 1


def delay_set() -> float:
    """Return clicks per second float from user input"""
    while True:
        try:
            delay = 1 / int(input('Enter clicks per second: '))
        except ValueError:
            print('Please enter a valid number.\n')
        else:
            return delay


class ClickMouse(Thread):
    """Thread that uses a mouse object to click a given button with a delay."""
    def __init__(self,
                 mouse: Controller,
                 button: Button,
                 delay: float = 0.0) -> None:
        Thread.__init__(self)
        
        self.mouse = mouse
        self.button = button
        self.delay = float(delay)
        self.last_toggle: float = 0
        self.click: bool = False
        self.active: bool = False
        
        self.start()
    
    def toggle(self) -> None:
        """Toggle clicking state"""
        if time.time() + TOGGLEDELAY > self.last_toggle:
            self.last_toggle = int(time.time())
            self.click = not self.click
    
    def exit(self) -> None:
        """Stop thread"""
        self.click = False
        self.active = False
    
    def run(self) -> None:
        """Main thread loop"""
        if not REGULATE:
            self.active = True
            while self.active:
                if self.click:
                    self.mouse.click(self.button)
                time.sleep(self.delay)
        else:
            self.active = True
            last = time.time()
            count = 0
            original_delay = self.delay
            target_clicks_per_sec = 1 / original_delay
            while self.active:
                if self.click:
                    self.mouse.click(self.button)
                    count += 1
                    change = time.time() - last
                    if change >= 1:
                        cps = count / change
                        last = time.time()
                        if cps != target_clicks_per_sec:
                            deltacps = target_clicks_per_sec - cps
                            self.delay += (1/deltacps)
                    time.sleep(self.delay)
                else:
                    time.sleep(0.001)

def run() -> None:
    """Synchronous Entry Point"""
    mouse = Controller()
    leftclick = Button.left
    rightclick = Button.right
    
    delay = delay_set()
    
    leftclick_thread = ClickMouse(mouse, leftclick, delay)
    rightclick_thread = ClickMouse(mouse, rightclick, delay)
    
    print('''To toggle left clicking, press the "1" key.
To toggle right clicking, press the "2" key.
Press the "3" key to stop clicking.
Press the "`" key (grave accent) to stop the program.''')
    
    left_toggle = KeyCode(char='1')
    right_toggle = KeyCode(char='2')
    stop_clicking = KeyCode(char='3')
    exit_key = KeyCode(char='`')
    
    def toggle_keys() -> None:
        def on_press(key: Key | KeyCode | None = None) -> None:
            if key is None:
                return
            if isinstance(key, Key):
                return
            if key == left_toggle:
                leftclick_thread.toggle()
            elif key == right_toggle:
                rightclick_thread.toggle()
            elif key == stop_clicking:
                leftclick_thread.click = False
                rightclick_thread.click = False
            elif key == exit_key:
                listener.stop()
        with Listener(on_press=on_press) as listener:
            listener.join()
    try:
        toggle_keys()
    finally:
        leftclick_thread.exit()
        rightclick_thread.exit()

if __name__ == '__main__':
    print(f'{__title__} v{__version__} Programmed by {__author__}.\n')
    run()
