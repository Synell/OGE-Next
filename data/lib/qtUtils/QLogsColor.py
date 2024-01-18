#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from .QUtilsColor import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QLogsColor(Enum):
    Error = QUtilsColor.from_hex('#E61E14')
    Warning = QUtilsColor.from_hex('#D2A800')
    Success = QUtilsColor.from_hex('#00D20A')
    Info = QUtilsColor.from_hex('#1473E6')
#----------------------------------------------------------------------
