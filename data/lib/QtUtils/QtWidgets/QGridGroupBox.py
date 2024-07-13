#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGroupBox, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridGroupBox(QGroupBox):
    def __init__(self, title = '', parent = None):
        super().__init__(title, parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)


    @property
    def layout_(self) -> QGridLayout:
        return self._layout
#----------------------------------------------------------------------
