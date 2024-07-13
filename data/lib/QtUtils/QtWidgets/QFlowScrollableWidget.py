#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from ..QtGui import QFlowLayout, QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QFlowScrollableWidget(QSmoothScrollArea):
    def __init__(self, parent = None, orientation = Qt.Orientation.Horizontal, margin = 0, spacing = -1) -> None:
        super(QFlowScrollableWidget, self).__init__(parent)
        self._widget = QFrame()
        self._widget.setContentsMargins(margin, margin, margin, margin)
        self._layout = QFlowLayout(self._widget, orientation, spacing)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self._widget)
        self.setWidgetResizable(True)


    @property
    def layout_(self) -> QFlowLayout:
        return self._layout


    @property
    def widget_(self) -> QFrame:
        return self._widget


    def clear(self) -> None:
        for i in reversed(range(self._layout.count())):
            item = self._layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self._layout.removeItem(item)
#----------------------------------------------------------------------
