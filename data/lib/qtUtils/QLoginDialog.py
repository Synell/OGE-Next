#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QLoginWidget import QLoginWidget
from .QLangDataManager import QLangData
#----------------------------------------------------------------------

    # Class
class QLoginDialog(QDialog):
    def __init__(self, parent = None , lang: QLangData = {}, username: str = '', password: str = '', remember_checkbox: bool = True, remember: bool = False):
        super().__init__(parent)

        self.setWindowTitle(lang['title'])

        self.root = QGridFrame(self)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.root.grid_layout.setSpacing(20)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        self.root.grid_layout.addWidget(frame, 0, 0)
        self.root.grid_layout.setAlignment(frame, Qt.AlignmentFlag.AlignTop)

        self.login_widget = QLoginWidget(None, lang, username, password, remember_checkbox, remember)
        self.login_widget.enter_key_pressed.connect(self.accept)
        frame.grid_layout.addWidget(self.login_widget, 0, 0)
        frame.grid_layout.setAlignment(self.login_widget, Qt.AlignmentFlag.AlignCenter)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(frame, 1, 0)
        self.root.grid_layout.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        right_buttons = QGridFrame()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang.get('QPushButton.cancel'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(lang.get('QPushButton.login'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        frame.grid_layout.addWidget(right_buttons, 0, 0)
        frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.root.grid_layout)

    def exec(self) -> tuple[str, str, bool | None] | None:
        if super().exec(): return self.login_widget._username.text(), self.login_widget._password.text(), self.login_widget._remember.isChecked() if self.login_widget._remember else None
#----------------------------------------------------------------------
