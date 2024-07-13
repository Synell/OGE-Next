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

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self._icon_text = QIconLabel(text, icon, size)
        self.layout_.addWidget(self._icon_text, 0, 0)

    def setIcon(self, icon: str | QPixmap | QIcon, size: QSize = QSize(24, 16)) -> None:
        self._icon_text.setIcon(icon, size)

    def setText(self, text: str) -> None:
        self._icon_text.setText(text)

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.layout_.setAlignment(self._icon_text, alignment)
        self.layout_.setAlignment(alignment)

    def setStyleSheet(self, styleSheet: str) -> None:
        self._icon_text.setStyleSheet(styleSheet)
#----------------------------------------------------------------------
