#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal

from .QGridFrame import QGridFrame
from .QNamedLineEdit import QNamedLineEdit
from .QNamedToggleButton import QNamedToggleButton
#----------------------------------------------------------------------

    # Class
class QLoginWidget(QGridFrame):
    enter_key_pressed = Signal()

    def __init__(self, parent = None , lang: dict = {}, username: str = '', password: str = '', remember_checkbox: bool = True, remember: bool = False) -> None:
        super().__init__(parent)

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(20)
        self.setFixedSize(300, 200)

        self._username = QNamedLineEdit(None, '', lang['QNamedLineEdit']['username'])
        self._username.line_edit.setProperty('small', True)
        self._username.setText(username)
        self.grid_layout.addWidget(self._username, 0, 0)

        self._password = QNamedLineEdit(None, '', lang['QNamedLineEdit']['password'])
        self._password.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._password.setText(password)
        self.grid_layout.addWidget(self._password, 1, 0)

        if remember_checkbox:
            self._remember = QNamedToggleButton(None, lang['QNamedToggleButton']['remember'], False, True)
            self._remember.setChecked(remember)
            self.grid_layout.addWidget(self._remember, 2, 0)
            self.grid_layout.setAlignment(self._remember, Qt.AlignmentFlag.AlignRight)
        else: self._remember = None

        self.grid_layout.setRowStretch(3, 1)


    def set_disabled(self, disabled: bool = True) -> None:
        self._username.setDisabled(disabled)
        self._password.setDisabled(disabled)
        if self._remember: self._remember.setDisabled(disabled)

    @property
    def username(self) -> str:
        return self._username.text()
    
    @property
    def password(self) -> str:
        return self._password.text()
    
    @property
    def remember(self) -> bool:
        if self._remember: return self._remember.isChecked()
        else: return False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            self.enter_key_pressed.emit()

        return super().keyPressEvent(event)
#----------------------------------------------------------------------
