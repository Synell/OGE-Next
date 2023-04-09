#----------------------------------------------------------------------

    # Libraries
from enum import Enum
#----------------------------------------------------------------------

    # Class
class PlatformType(Enum):
    Windows = ['windows-64', 'windows-32', 'win-64', 'win-32', 'win64', 'win32', 'win32-64', 'win64-32', 'windows', 'win']
    Linux = ['linux', 'ubuntu', 'debian', 'fedora', 'arch']
    MacOS = ['macos', 'mac']
#----------------------------------------------------------------------
