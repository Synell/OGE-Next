#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from data.lib.QtUtils.QPlatform import QPlatform
#----------------------------------------------------------------------

    # Class
class PlatformType(Enum):
    Windows = ['windows-64', 'windows-32', 'win-64', 'win-32', 'win64', 'win32', 'win32-64', 'win64-32', 'windows', 'win']
    Linux = ['linux', 'ubuntu', 'debian', 'fedora', 'arch']
    MacOS = ['macos', 'mac']

    @staticmethod
    def from_qplatform(platform: QPlatform) -> 'PlatformType':
        match platform:
            case QPlatform.Windows: return PlatformType.Windows
            case QPlatform.Linux: return PlatformType.Linux
            case QPlatform.MacOS: return PlatformType.MacOS
            case _: raise ValueError(f'Unknown platform: {platform}')
#----------------------------------------------------------------------
