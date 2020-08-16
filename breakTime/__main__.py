#!/usr/bin/env python3

import sys
import schedule
import threading
import logging

from time import sleep

from .cli import parseArgs
from .platforms.adapter import Adapter, Platforms, Platform
from .Timer import Timer

DEBUG = 1

if DEBUG:
    logging.basicConfig(
        format="%(asctime)s %(filename)s:%(lineno)d %(levelname)s:%(message)s",
        level=logging.INFO,
    )


workMins, breakMins = parseArgs(sys.argv)

adapter = Adapter.get()

if Platform == Platforms.Windows:
    if not adapter.isAdmin():
        adapter.relaunchAsAdmin()

t = Timer(workMins, breakMins)


def mainLoop():
    t.tick()


schedule.every(5).seconds.do(mainLoop)


while True:
    schedule.run_pending()
    sleep(5)
