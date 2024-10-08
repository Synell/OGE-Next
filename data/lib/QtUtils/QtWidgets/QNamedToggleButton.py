#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from .QGridFrame import QGridFrame
from .QToggleButton import QToggleButton
#----------------------------------------------------------------------

    # Class
class QNamedToggleButton(QGridFrame):
    toggled = Signal(bool)

    def __init__(self, parent = None, text: str = '', checked: bool = False, min_width: bool = False, text_to_right: bool = False) -> None:
        super().__init__(parent)
        self.setProperty('QNamedToggleButton', True)
        self.setProperty('color', 'main')

        self.layout_.setSpacing(16)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.toggle_button = QToggleButton()
        self.toggle_button.toggled.connect(self.toggled.emit)
        self.label = QLabel()

        self.toggle_button.setChecked(checked)
        self.label.setText(text)

        self.layout_.addWidget(self.label, 0, 1 if text_to_right else 0)
        self.layout_.addWidget(self.toggle_button, 0, 0 if text_to_right else 1)
        if min_width: self.layout_.setColumnStretch(2, 1)

    def setChecked(self, value: bool):
        self.toggle_button.setChecked(value)

    def isChecked(self):
        return self.toggle_button.isChecked()

    def setText(self, text: str):
        self.label.setText(text)

    def text(self):
        return self.label.text()
#----------------------------------------------------------------------
