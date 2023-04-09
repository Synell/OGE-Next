#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLineEdit, QLabel
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QNamedLineEdit(QGridWidget):
    normal_color = '#FFFFFF'
    hover_color = '#FFFFFF'
    focus_color = '#FFFFFF'

    def __init__(self, parent = None, placeholder: str = '', name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedLineEdit', True)
        self.setProperty('color', 'main')

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.grid_layout.addWidget(self.line_edit, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.line_edit.base_focusInEvent = self.line_edit.focusInEvent
        self.line_edit.base_focusOutEvent = self.line_edit.focusOutEvent
        self.line_edit.focusInEvent = self.focusInEvent
        self.line_edit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.line_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self.focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.line_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self.hover_color}')
        else: self.label.setStyleSheet(f'color: {self.normal_color}')

    def text(self) -> str:
        return self.line_edit.text()

    def setText(self, text: str) -> None:
        self.line_edit.setText(text)

    def placeholderText(self) -> str:
        return self.line_edit.placeholderText()

    def setPlaceholderText(self, text: str) -> None:
        self.line_edit.setPlaceholderText(text)

    def isReadOnly(self) -> bool:
        return self.line_edit.isReadOnly()

    def setReadOnly(self, read_only: bool) -> None:
        self.line_edit.setReadOnly(read_only)

    def isEnabled(self) -> bool:
        return self.line_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.line_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
