#----------------------------------------------------------------------

    # Libraries
from typing import Any
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon

from data.lib.QtUtils import QGridWidget, QIconLabel
#----------------------------------------------------------------------

    # Class
class IconLabel(QGridWidget):
    def __init__(self, text: str = '', icon: str | QPixmap | QIcon = None, size: QSize = QSize(24, 16)) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self._icon_text = QIconLabel(text, icon, size)
        self.grid_layout.addWidget(self._icon_text, 0, 0)

    def setIcon(self, icon: str | QPixmap | QIcon, size: QSize = QSize(24, 16)) -> None:
        self._icon_text.setIcon(icon, size)

    def setText(self, text: str) -> None:
        self._icon_text.setText(text)

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.grid_layout.setAlignment(self._icon_text, alignment)
        self.grid_layout.setAlignment(alignment)

    def setStyleSheet(self, styleSheet: str) -> None:
        self._icon_text.setStyleSheet(styleSheet)
#----------------------------------------------------------------------
