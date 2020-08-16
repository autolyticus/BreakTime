import platform
import re

from typing import Any
from enum import Enum, auto
from .IAdapter import PlatformAdapter


class Platforms(Enum):
    Windows = auto
    Linux = auto
    Unknown = auto


onWindows = re.search("win", platform.system(), re.IGNORECASE) is not None

if onWindows:
    Platform = Platforms.Windows
# Right now we only support Windows and Linux
else:
    Platform = Platforms.Linux


class Adapter:
    """ Encapsulates all platform specific code using the Adapter pattern """

    @staticmethod
    def get(*args: Any, **kwargs: Any) -> PlatformAdapter:
        if Platform == Platforms.Windows:
            from .windows import WindowsAdapter

            return WindowsAdapter(*args, **kwargs)
        elif Platform == Platforms.Linux:
            from .linux import LinuxAdapter

            return LinuxAdapter(*args, **kwargs)
        else:
            raise NotImplementedError
