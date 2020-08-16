import ctypes
import sys
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
    def waitForUserActivity():
        firstInputInfo = win32api.GetLastInputInfo()
        print("Waiting for user activity...")
        while firstInputInfo - win32api.GetLastInputInfo() == 0:
            sleep(1)
