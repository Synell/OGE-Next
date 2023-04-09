#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from .QSmoothScrollArea import QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QScrollableGridWidget(QSmoothScrollArea):
    def __init__(self):
        super(QScrollableGridWidget, self).__init__()
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
#----------------------------------------------------------------------
