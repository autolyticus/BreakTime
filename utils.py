#!/usr/bin/env python
import ctypes
import tkinter as tk
from datetime import datetime, timedelta
from subprocess import Popen
from time import sleep

from plyer import notification

import win32api


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth() - pad,
                                             master.winfo_screenheight() -
                                             pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


def blockScreen(seconds):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')
    root.after(int(seconds * 1000),
               lambda: root.destroy())  # Destroy the widget after 30 seconds
    app = FullScreenApp(root)
    root.wm_attributes("-topmost", 1)
    root.mainloop()


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Prevents any input for x seconds, uses subprocess.Popen
def blockInput(seconds):
    Popen(f'blockInput.exe {seconds * 1000}')


def waitForUserActivity():
    firstInputInfo = win32api.GetLastInputInfo()
    print('Waiting for user activity...')
    while firstInputInfo - win32api.GetLastInputInfo() == 0:
        pass


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02.0f}:{:02.0f}'.format(mins, secs)
        print(f"Next break in {timeformat}", end="\r")
        sleep(1)
        t -= 1
        if t == 15:
            sendNotification('Break in 15 seconds')
            pass
        pass


def sendNotification(message):
    notification.notify(
        title='Take A Break',
        message=message,
        app_icon='logo.ico',
        timeout=10,
    )
