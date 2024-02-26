#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QSizePolicy, QLayout, QWidgetItem
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from .QFlowLayout import QFlowLayout
from .QSmoothScrollArea import QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QFlowScrollableWidget(QSmoothScrollArea):
    def __init__(self, parent = None, orientation = Qt.Orientation.Horizontal, margin = 0, spacing = -1):
        super(QFlowScrollableWidget, self).__init__(parent)
        self.scroll_frame = QFrame()
        self.scroll_frame.setContentsMargins(margin, margin, margin, margin)
        self.scroll_layout = QFlowLayout(self.scroll_frame, orientation, spacing)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_frame)
        self.setWidgetResizable(True)

    def clear(self):
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.scroll_layout.removeItem(item)
#----------------------------------------------------------------------
