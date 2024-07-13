#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)


    @property
    def layout_(self) -> QGridLayout:
        return self._layout
#----------------------------------------------------------------------
