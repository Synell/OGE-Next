#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from ..QtGui import QFlowLayout
#----------------------------------------------------------------------

    # Class
class QFlowWidget(QFrame):
    def __init__(self, parent = None, orientation = Qt.Orientation.Horizontal, margin = 0, spacing = -1) -> None:
        super(QFlowWidget, self).__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.flow_layout = QFlowLayout(None, orientation, spacing)
        self.setLayout(self.flow_layout)
        self.flow_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#----------------------------------------------------------------------
