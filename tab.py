#!/usr/bin/env python
import ctypes
import sys
from os import system
from time import sleep

from datetime import datetime, timedelta
from plyer import notification
from utils import *

# print(sys.argv)
if len(sys.argv) > 3:
    print('Too many arguments')
    sys.exit(1)

if not sys.argv[1]:
    workMins = 25
    print('Note: Using default Pomodoro work duration of 25 minutes')
else:
    workMins = float(sys.argv[1])
    print(f'Note: Using work duration of {workMins} minutes')

if not sys.argv[2]:
    breakMins = 5
    print('Note: Using default Pomodoro break duration of 5 minutes')
else:
    breakMins = float(sys.argv[2])
    print(f'Note: Using break duration of {breakMins} minutes')

if is_admin():
    while True:
        print('Starting work session')
        notification.notify(
            title='Take A Break',
            message=f'Work session - {workMins} minutes left',
            app_icon='logo.ico',
            timeout=10,
        )
        sleep((workMins - 0.25) * 60)
        print('Break in 15 seconds')
        notification.notify(
            title='Take A Break',
            message=f'Break in 15 seconds',
            app_icon='logo.ico',
            timeout=10,
        )
        sleep(15)
        breakEndTime = datetime.now() + timedelta(minutes = breakMins)
        notification.notify(
            title='Take A Break',
            message=f'You are obliged to take a break. See you at {breakEndTime.hour}:{breakEndTime.minute}',
            app_icon='logo.ico',
            timeout=10,
        )
        blockInput(breakMins * 60)
        blockScreen(breakMins * 60)
        sleep(breakMins * 60)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
