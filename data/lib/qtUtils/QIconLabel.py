#----------------------------------------------------------------------

    # Libraries
from typing import Any
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QIcon

from data.lib.qtUtils import QGridWidget, QIconWidget
#----------------------------------------------------------------------

    # Class
class QIconLabel(QGridWidget):
    def __init__(self, text: str = '', icon: str | QPixmap | QIcon = None, icon_size: QSize = QSize(16, 16), spacing: int = 5) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(spacing)

        self._icon_label = QIconWidget()
        self._icon_label.icon_size = QSize(icon_size.width(), icon_size.height())
        self._icon_label.setFixedSize(QSize(icon_size.width(), icon_size.height()))
        self.set_icon(icon, icon_size)
        self.grid_layout.addWidget(self._icon_label, 0, 0)

        self._text_label = QLabel()
        self.set_text(text)
        self.grid_layout.addWidget(self._text_label, 0, 1)

        self.grid_layout.setColumnStretch(2, 1)

    def set_icon(self, icon: str | QPixmap | QIcon, size: QSize = QSize(16, 16)) -> None:
        self._icon_label.icon = icon
        self._icon_label.icon_size = QSize(size.width(), size.height())
        self._icon_label.setFixedSize(QSize(size.width(), size.height()))

    def setIcon(self, icon: str | QPixmap | QIcon, size: QSize = QSize(16, 16)) -> None:
        self.set_icon(icon, size)

    def set_spacing(self, spacing: int) -> None:
        self.grid_layout.setSpacing(spacing)

    def setSpacing(self, spacing: int) -> None:
        self.set_spacing(spacing)

    def set_text(self, text: str) -> None:
        self._text_label.setText(text)

    def setText(self, text: str) -> None:
        self.set_text(text)

    def setStyleSheet(self, styleSheet: str) -> None:
        self._text_label.setStyleSheet(styleSheet)

    def setLayoutDirection(self, direction: Qt.LayoutDirection) -> None:
        super().setLayoutDirection(direction)

    def setProperty(self, name: str, value: Any) -> bool:
        return self._text_label.setProperty(name, value)

    def property(self, name: str) -> Any:
        return self._text_label.property(name)
#----------------------------------------------------------------------
