#!/usr/bin/env python3

import sys
import schedule
import threading
from time import sleep

from .cli import parseArgs
from .platforms.adapter import Adapter, Platforms, Platform


workMins, breakMins = parseArgs(sys.argv)

adapter = Adapter.get()

if Platform == Platforms.Windows:
    if not adapter.isAdmin():
        adapter.relaunchAsAdmin()

t = Timer(workMins, breakMins)


def mainLoop():
    t.update()


schedule.every(5).seconds.do(mainLoop)


while True:
    schedule.run_pending()
    sleep(5)
