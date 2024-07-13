#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QMouseEvent

from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
#----------------------------------------------------------------------

    # Class
class QTitleButton(QGridFrame):
    clicked = Signal()


    def __init__(self, title: str, description: str, icon: str = None, icon_size: QSize = QSize(32, 32)) -> None:
        super().__init__()

        self.layout_.setContentsMargins(4, 4, 4, 4)
        self.layout_.setHorizontalSpacing(16)
        self.layout_.setVerticalSpacing(0)

        self.setFocusPolicy(Qt.FocusPolicy.TabFocus | Qt.FocusPolicy.ClickFocus)

        self.setProperty('QTitleButton', True)
        self.setProperty('color', 'main')
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if icon:
            self._icon = QIconWidget(None, icon, icon_size, False)
            self.layout_.addWidget(self._icon, 0, 0, 2, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self._icon.layout_.setColumnStretch(1, 1)

        self._title = QLabel(title)
        self._title.setProperty('bigbrighttitle', True)
        self.layout_.addWidget(self._title, 0, 1 if icon else 0)

        self._description = QLabel(description)
        self._description.setProperty('brightsubtitle', True)
        self._description.setWordWrap(True)
        self.layout_.addWidget(self._description, 1, 1 if icon else 0)

        self.layout_.setRowStretch(2, 1)
        self.layout_.setColumnStretch(2 if icon else 1, 1)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.setProperty('pressed', True)
            self.style().polish(self)
        return super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setProperty('pressed', False)
            self.style().polish(self)
            if self.rect().contains(event.pos()): self.clicked.emit()

        return super().mouseReleaseEvent(event)
#----------------------------------------------------------------------
