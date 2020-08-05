#!/usr/bin/env python
import ctypes
import sys
from datetime import datetime, timedelta
from time import sleep

from utils import *

if len(sys.argv) > 3:
    print('Too many arguments')
    sys.exit(1)

if not sys.argv[1]:
    workMins = 25
    print('Note: Using default Pomodoro work duration of 25 minutes')
else:
    workMins = int(sys.argv[1])
    print(f'Note: Using work duration of {workMins} minutes')

if not sys.argv[2]:
    breakMins = 5
    print('Note: Using default Pomodoro break duration of 5 minutes')
else:
    breakMins = int(sys.argv[2])
    print(f'Note: Using break duration of {breakMins} minutes')

if isAdmin():
    while True:
        waitForUserActivity()

        print(f'\nStarting work session at {datetime.now().strftime("%H:%M")}')
        sendNotification(f'Work session - {workMins} minutes left')
        countdown(workMins*60)
        breakEndTime = datetime.now() + timedelta(minutes=breakMins)
        print(f'Break until {breakEndTime.hour}:{breakEndTime.minute}')
        sendNotification(
            f'You are obliged to take a break. See you at {breakEndTime.strftime("%H:%M")}',
        )
        blockInput(breakMins * 60)  # Does not block the thread
        blockScreen(breakMins * 60)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable,
                                        ' '.join(sys.argv), None, 1)
