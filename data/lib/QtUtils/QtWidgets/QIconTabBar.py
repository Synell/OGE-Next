#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTabBar
from PySide6.QtCore import QSize
#----------------------------------------------------------------------

    # Class
class QIconTabBar(QTabBar):
    def __init__(self) -> None:
        super().__init__()
        self.setProperty('QIconTabBar', True)
        self.setProperty('color', 'main')

        self.setIconSize(QSize(20, 20))


    def tabSizeHint(self, index):
        res = super(QIconTabBar, self).tabSizeHint(index)
        return res
#----------------------------------------------------------------------
