#----------------------------------------------------------------------

    # Libraries
from typing import Any
from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal

from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QMoreButton(QGridWidget):
    clicked = Signal()
    more_clicked = Signal()


    def __init__(self, text: str = '') -> None:
        super().__init__()

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(1)

        self.setProperty('QMoreButton', True)

        self._main_button = QPushButton(text)
        self._main_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._main_button.setProperty('color', 'main')
        self._main_button.setProperty('mainButton', True)
        self._main_button.clicked.connect(self.clicked.emit)
        self.layout_.addWidget(self._main_button, 0, 0)

        self._more_button = QPushButton()
        self._more_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self._more_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._more_button.setProperty('color', 'main')
        self._more_button.setProperty('moreButton', True)
        self._more_button.clicked.connect(self.more_clicked.emit)
        self.layout_.addWidget(self._more_button, 0, 1)

        # self.layout_.setColumnStretch(2, 1)


    def setDisabled(self, arg__1: bool) -> None:
        self._main_button.setCursor(Qt.CursorShape.ForbiddenCursor if arg__1 else Qt.CursorShape.PointingHandCursor)
        self._main_button.setDisabled(arg__1)

        self._more_button.setCursor(Qt.CursorShape.ForbiddenCursor if arg__1 else Qt.CursorShape.PointingHandCursor)
        self._more_button.setDisabled(arg__1)
        self._more_button.setProperty('disabled', arg__1)
        self._more_button.style().unpolish(self._more_button)
        self._more_button.style().polish(self._more_button)

        return super().setDisabled(arg__1)
#----------------------------------------------------------------------
