#!/usr/bin/env python3
# Threaded auto clicker
# -*- coding: utf-8 -*-

# Programmed by BitMan64 with minor changes by CoolCat467

import os
import time
from threading import Thread
try:
    from pynput.mouse import Button, Controller
    from pynput.keyboard import Listener, KeyCode
except ImportError:
    print('Error: pynput not found!')
    print('Please install pynput for this program to function!')
    input('Press Return to Continue. ')
    os.abort()

__title__ = 'Threaded Auto Clicker'
__author__ = 'BitMan64'
__version__ = '1.0.0'
__ver_major__ = 1
__ver_minor__ = 0
__ver_patch__ = 0

def delaySet():
    try:
        delay = float(input('Enter delay time: '))
    except ValueError:
        print('Please enter a valid number.')
        delaySet()
    else:
        return delay

class ClickMouse(Thread):
    def __init__(self, mouse, button, delay):
        Thread.__init__()
        self.mouse = mouse
        self.button = button
        self.delay = float(delay)
        self.click = False
        self.active = False
        self.start()
    
    def start_clicking(self):
        self.click = True
    
    def stop_clicking(self):
        self.click = False
    
    def toggle(self):
        self.click = not self.click
    
    def exit(self):
        self.click = False
        self.active = False
    
    def run(self):
        self.active = True
        while self.active:
            if self.click:
                self.mouse.click(self.button)
            time.sleep(self.delay)
    pass

def run():
    mouse = Controller()
    leftclick = Button.left
    rightclick = Button.right
    delay = delaySet()
    leftclick_thread = ClickMouse(mouse, leftclick, delay)
    rightclick_thread = ClickMouse(mouse, rightclick, delay)
    
    leftToggle = KeyCode(char='0')
    rightToggle = KeyCode(char='1')
    exit_key = KeyCode(char='`')
    
    def ToggleKeys(leftToggleKey, rightToggleKey, exitKey, leftThread, rightThread):
        def on_press(key):
            if key == leftToggleKey:
                leftThread.toggle()
            elif key == rightToggleKey:
                rightThread.toggle()
            elif key == exitKey:
                leftThread.exit()
                rightThread.exit()
                listener.stop()
        with Listener(on_press=on_press) as listener:
            listener.join()
    ToggleKeys(leftToggle, rightToggle, exit_key, leftclick_thread, rightclick_thread)    

if __name__ == '__main__':
    print('%s Version %s Programmed by %s' % (__title__, __version__, __author__))
    run()
