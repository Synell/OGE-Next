#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QPixmap
from data.lib.qtUtils import QGridFrame
#----------------------------------------------------------------------

    # Class
class OGEWidget(QGridFrame):
    _OGE_WEIRD_TOOLTIP: str = ''
    _OGE_WEIRD_ICON: QPixmap = None

    def __init__(self) -> None:
        super().__init__()

    def perc2color(self, perc: float) -> str:
        r, g, b = 0, 0, 0
        if perc < 0.5:
            r = 255
            g = round(510 * perc)

        else:
            g = 255
            r = round(510 - 510 * perc)

        h = r * 0x10000 + g * 0x100 + b * 0x1
        return '#' + ('000000' + hex(int(h))[2:])[-6:]
#----------------------------------------------------------------------
