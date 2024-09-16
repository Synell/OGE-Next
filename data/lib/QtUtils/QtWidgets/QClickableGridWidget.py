#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QClickableGridWidget(QGridWidget):
    clicked = Signal()


    def __init__(self, parent = None) -> None:
        super().__init__(parent)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked.emit()
        super().mousePressEvent(event)
#----------------------------------------------------------------------
