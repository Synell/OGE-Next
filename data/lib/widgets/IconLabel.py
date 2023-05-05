#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

from data.lib.qtUtils import QGridWidget, QIconLabel
#----------------------------------------------------------------------

    # Class
class IconLabel(QGridWidget):
    def __init__(self, text: str = '', icon: str | QPixmap | QIcon = None) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self._icon_text = QIconLabel(text, icon)
        self.grid_layout.addWidget(self._icon_text, 0, 0)

    def setIcon(self, icon: str | QPixmap | QIcon) -> None:
        self._icon_text.setIcon(icon)

    def setText(self, text: str) -> None:
        self._icon_text.setText(text)

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.grid_layout.setAlignment(self._icon_text, alignment)
        self.grid_layout.setAlignment(alignment)

    def setStyleSheet(self, styleSheet: str) -> None:
        self._icon_text.setStyleSheet(styleSheet)
#----------------------------------------------------------------------
