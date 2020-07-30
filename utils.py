#!/usr/bin/env python
import ctypes
from subprocess import Popen
import tkinter as tk
from datetime import datetime, timedelta

from plyer import notification


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def blockScreen(seconds):
    root=tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')
    root.after(int(seconds*1000), lambda: root.destroy()) # Destroy the widget after 30 seconds
    app=FullScreenApp(root)
    root.mainloop()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def blockInput(seconds):
    Popen(f'blockInput.exe {seconds * 1000}')
