import ctypes
import sys
import pendulum
from time import sleep
import win32api

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
        return pendulum.from_timestamp(win32api.GetLastInputInfo())
