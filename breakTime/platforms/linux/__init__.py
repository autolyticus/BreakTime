import ctypes
import logging
import pendulum

from ctypes.util import find_library
from typing import Any
from time import sleep
import subprocess
from pathlib import Path
from bpdb import set_trace

from ..PlatformAdapter import PlatformAdapter


# This is a complicated way to do it, and can be much easier done
# with just xprintidle, but I figured this would be better
class X11IdleMonitor:
    """
    Idle monitor for systems running X11.
    Based on
      * http://tperl.blogspot.com/2007/09/x11-idle-time-and-focused-window-in.html
      * https://stackoverflow.com/a/55966565/7774036
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        class XScreenSaverInfo(ctypes.Structure):
            _fields_ = [
                ("window", ctypes.c_ulong),  # screen saver window
                ("state", ctypes.c_int),  # off, on, disabled
                ("kind", ctypes.c_int),  # blanked, internal, external
                ("since", ctypes.c_ulong),  # milliseconds
                ("idle", ctypes.c_ulong),  # milliseconds
                ("event_mask", ctypes.c_ulong),
            ]  # events

        lib_x11 = self._load_lib("X11")
        # specify required types
        lib_x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
        lib_x11.XOpenDisplay.restype = ctypes.c_void_p
        lib_x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
        lib_x11.XDefaultRootWindow.restype = ctypes.c_uint32
        # fetch current settings
        self.display = lib_x11.XOpenDisplay(None)
        self.root_window = lib_x11.XDefaultRootWindow(self.display)

        self.lib_xss = self._load_lib("Xss")
        # specify required types
        self.lib_xss.XScreenSaverQueryInfo.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.POINTER(XScreenSaverInfo),
        ]
        self.lib_xss.XScreenSaverQueryInfo.restype = ctypes.c_int
        self.lib_xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        # allocate memory for idle information
        self.xss_info = self.lib_xss.XScreenSaverAllocInfo()

    def get_idle_time(self) -> float:
        self.lib_xss.XScreenSaverQueryInfo(
            self.display, self.root_window, self.xss_info
        )
        return self.xss_info.contents.idle / 1000

    def _load_lib(self, name: str) -> Any:
        path = find_library(name)
        if path is None:
            raise OSError(f"Could not find library `{name}`")
        return ctypes.cdll.LoadLibrary(path)


class LinuxAdapter(PlatformAdapter):
    def __init__(self):
        self.monitor = X11IdleMonitor()

    def getLastUserActivityTime(self):
        idleTime = self.monitor.get_idle_time()
        return pendulum.now().subtract(microseconds=idleTime * 10 ** 6)

    def blockInput(self, seconds):
        self.inputBlocker = subprocess.Popen(
            str(Path(__file__).parent / "blockInput.sh") + f" {seconds}",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        print(f"Blocking inputs for {seconds}")
