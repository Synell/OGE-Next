#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
#----------------------------------------------------------------------
