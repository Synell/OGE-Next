#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QLoginWidget import QLoginWidget
from ..QtCore import QLangData
#----------------------------------------------------------------------

    # Class
class QLoginDialog(QDialog):
    def __init__(self, parent = None, lang: QLangData = {}, username: str = '', password: str = '', remember_checkbox: bool = True, remember: bool = False):
        super().__init__(parent)

        self.setWindowTitle(lang['title'])

        self.root = QGridFrame(self)
        self.root.layout_.setContentsMargins(0, 0, 0, 0)
        self.root.layout_.setSpacing(20)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        self.root.layout_.addWidget(frame, 0, 0)
        self.root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignTop)

        self.login_widget = QLoginWidget(None, lang, username, password, remember_checkbox, remember)
        self.login_widget.enter_key_pressed.connect(self.accept)
        frame.layout_.addWidget(self.login_widget, 0, 0)
        frame.layout_.setAlignment(self.login_widget, Qt.AlignmentFlag.AlignCenter)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        frame.setProperty('border-top', True)
        self.root.layout_.addWidget(frame, 1, 0)
        self.root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        right_buttons = QGridFrame()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang.get('QPushButton.cancel'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(button, 0, 0)

        button = QPushButton(lang.get('QPushButton.login'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.layout_.addWidget(button, 0, 1)

        frame.layout_.addWidget(right_buttons, 0, 0)
        frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.root.layout_)

    def exec(self) -> tuple[str, str, bool | None] | None:
        if super().exec(): return self.login_widget._username.text(), self.login_widget._password.text(), self.login_widget._remember.isChecked() if self.login_widget._remember else None
#----------------------------------------------------------------------
