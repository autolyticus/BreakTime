
import platform
import re

from typing import Any

onWindows = re.search("win", platform.system(), re.IGNORECASE) is not None

# Right now we only support Windows and Linux
onLinux = not onWindows

from .IAdapter import IAdapter


class Adapter:
    """ Encapsulates all platform specific code using the Adapter pattern """
    @staticmethod
    def get(*args: Any, **kwargs: Any) -> IAdapter:
        if onWindows:
            from .windows import WindowsAdapter

            return WindowsAdapter(*args, **kwargs)
        elif onLinux:
            from .linux import LinuxAdapter

            return LinuxAdapter(*args, **kwargs)
        else:
            raise NotImplementedError
