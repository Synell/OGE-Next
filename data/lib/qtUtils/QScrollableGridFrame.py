#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QGridLayout
from PySide6.QtCore import Qt
from .QSmoothScrollArea import QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QScrollableGridFrame(QSmoothScrollArea):
    def __init__(self):
        super(QScrollableGridFrame, self).__init__()
        self.scroll_frame = QFrame()
        self.scroll_layout = QGridLayout(self.scroll_frame)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_frame)
        self.setWidgetResizable(True)
#----------------------------------------------------------------------
