#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGroupBox, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridGroupBox(QGroupBox):
    def __init__(self, title = '', parent = None):
        super().__init__(title, parent)
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
#----------------------------------------------------------------------
