#!/usr/bin/env python3

import sys
from .cli import parseArgs
from .platforms.adapter import Adapter, Platforms, Platform

if len(argv) > 3:
    print("Too many arguments")
    exit(1)

workMins, breakMins = parseArgs(sys.argv)

adapter = Adapter.get()

if Platform == Platforms.Windows:
    if not adapter.isAdmin():
        adapter.relaunchAsAdmin()
