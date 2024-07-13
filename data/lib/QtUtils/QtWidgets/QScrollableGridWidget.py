#----------------------------------------------------------------------

    # Libraries
from typing import Any
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from ..QtGui import QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QScrollableGridWidget(QSmoothScrollArea):
    def __init__(self) -> None:
        super(QScrollableGridWidget, self).__init__()
        self._widget = QWidget()
        self._layout = QGridLayout(self._widget)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self._widget)
        self.setWidgetResizable(True)


    def set_all_property(self, name: str, value: Any) -> bool:
        ret = self.setProperty(name, value)
        self._widget.setProperty(name, value)
        self._layout.setProperty(name, value)

        return ret


    @property
    def layout_(self) -> QGridLayout:
        return self._layout


    @property
    def widget_(self) -> QWidget:
        return self._widget
#----------------------------------------------------------------------
