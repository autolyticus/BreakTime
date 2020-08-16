import ctypes
import sys
import subprocess
from time import sleep
from pathlib import Path

import win32api
import pendulum
import psutil

from ..PlatformAdapter import PlatformAdapter


class WindowsAdapter(PlatformAdapter):
    @staticmethod
    def relaunchAsAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )

    @staticmethod
    def isAdmin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def getLastUserActivityTime():
        return pendulum.from_timestamp(psutil.boot_time() + win32api.GetLastInputInfo())

    def blockInput(self, seconds):
        self.inputBlocker = subprocess.Popen(
            str(Path(__file__).parent / "blockInput.exe") + f" {seconds * 1000}",
            shell=True,
        )
