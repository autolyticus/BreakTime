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
    workMins = float(sys.argv[1])
    print(f'Note: Using work duration of {workMins} minutes')

if not sys.argv[2]:
    breakMins = 5
    print('Note: Using default Pomodoro break duration of 5 minutes')
else:
    breakMins = float(sys.argv[2])
    print(f'Note: Using break duration of {breakMins} minutes')

if isAdmin():
    while True:
        waitForUserActivity()

        print('Starting work session')
        sendNotification(f'Work session - {workMins} minutes left')
        sleep((workMins - 0.25) * 60)

        print('Break in 15 seconds')
        sendNotification('Break in 15 seconds')
        sleep(15)

        breakEndTime = datetime.now() + timedelta(minutes=breakMins)
        print(f'Break until {breakEndTime.hour}:{breakEndTime.minute}')
        sendNotification(
            f'You are obliged to take a break. See you at {breakEndTime.hour}:{breakEndTime.minute}',
        )
        blockInput(breakMins * 60)  # Does not block the thread
        blockScreen(breakMins * 60)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable,
                                        ' '.join(sys.argv), None, 1)
