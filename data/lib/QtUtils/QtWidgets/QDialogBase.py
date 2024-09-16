#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton, QWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from typing import Callable, Sequence

from .QGridFrame import QGridFrame
from ..QtCore.QLangData import QLangData
#----------------------------------------------------------------------

    # Class
class QDialogBase(QDialog):
    class Button:
        def __init__(self, id: str, name: str, properties: dict[str, object], action: Callable) -> None:
            self._pushbutton = QPushButton(name)
            self._pushbutton.setObjectName(id)
            self._pushbutton.setCursor(Qt.CursorShape.PointingHandCursor)
            self._pushbutton.clicked.connect(action)
            for property, value in properties.items():
                self._pushbutton.setProperty(property, value)


        @property
        def push_button(self) -> QPushButton:
            return self._pushbutton



    def __init__(
        self,
        parent: QWidget = None,
        lang: QLangData = QLangData.NoTranslation(),
        buttons: Sequence[Button] = [],
        button_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignRight,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(lang.get('title'))

        self._root = QGridFrame(self)
        self._root.layout_.setContentsMargins(0, 0, 0, 0)
        self._root.layout_.setSpacing(20)

        self._content = QGridFrame()
        self._content.layout_.setContentsMargins(20, 20, 20, 20)
        self._content.layout_.setSpacing(0)
        self._root.layout_.addWidget(self._content, 0, 0)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(10, 10, 10, 10)
        frame.layout_.setSpacing(0)
        frame.setProperty('border-top', True)
        self._root.layout_.addWidget(frame, 1, 0)
        self._root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        self._aligned_buttons = QGridFrame()
        self._aligned_buttons.layout_.setSpacing(16)
        self._aligned_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        self._buttons = {}

        for button in buttons:
            btn = button.push_button
            self._aligned_buttons.layout_.addWidget(btn, 0, self._aligned_buttons.layout_.columnCount())
            self._buttons[btn.objectName()] = btn

        frame.layout_.addWidget(self._aligned_buttons, 0, 0)
        frame.layout_.setAlignment(self._aligned_buttons, button_alignment)

        self.setLayout(self._root.layout_)


    def get_button_by_id(self, name: str) -> QPushButton | None:
        if name in self._buttons:
            return self._buttons[name]

        return None


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
        ): return self.accept()

        if event.key() == Qt.Key.Key_Escape: return self.reject()

        return super().keyPressEvent(event)
#----------------------------------------------------------------------
