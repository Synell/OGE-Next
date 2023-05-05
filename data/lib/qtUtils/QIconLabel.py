#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QIcon

from data.lib.qtUtils import QGridWidget, QIconWidget
#----------------------------------------------------------------------

    # Class
class QIconLabel(QGridWidget):
    def __init__(self, text: str = '', icon: str | QPixmap | QIcon = None) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(5)

        self._icon_label = QIconWidget()
        self._icon_label.icon_size = QSize(24, 16)
        self._icon_label.setFixedSize(QSize(16, 16))
        self.setIcon(icon)
        self.grid_layout.addWidget(self._icon_label, 0, 0)

        self._text_label = QLabel()
        self.setText(text)
        self.grid_layout.addWidget(self._text_label, 0, 1)

        self.grid_layout.setColumnStretch(2, 1)

    def setIcon(self, icon: str | QPixmap | QIcon) -> None:
        self._icon_label.icon = icon

    def setText(self, text: str) -> None:
        self._text_label.setText(text)

    def setStyleSheet(self, styleSheet: str) -> None:
        self._text_label.setStyleSheet(styleSheet)

    def setLayoutDirection(self, direction: Qt.LayoutDirection) -> None:
        super().setLayoutDirection(direction)
#----------------------------------------------------------------------
