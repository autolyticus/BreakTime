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


def mainLoop():
    pass


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(5).seconds.do(run_threaded, mainLoop)


while True:
    schedule.run_pending()
    sleep(5)
