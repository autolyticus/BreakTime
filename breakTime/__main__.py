#!/usr/bin/env python3

import sys
import logging

from time import sleep

import schedule

from .cli import parseArgs
from .platforms.adapter import Adapter, Platforms, Platform
from .Timer import Timer

DEBUG = 0

if DEBUG:
    logging.basicConfig(
        format="%(asctime)s %(filename)s:%(lineno)d %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    logging.getLogger("schedule").setLevel(logging.WARNING)


workMins, breakMins = parseArgs(sys.argv)

adapter = Adapter.get()

if Platform == Platforms.Windows:
    if not adapter.isAdmin():
        adapter.relaunchAsAdmin()

t = Timer(workMins, breakMins)


def mainLoop():
    t.tick()


schedule.every(1).seconds.do(mainLoop)


while True:
    schedule.run_pending()
    sleep(1)
