import ctypes
import sys

from ..IAdapter import IAdapter


class WindowsAdapter(IAdapter):
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
