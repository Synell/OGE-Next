#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTextEdit, QLabel
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QNamedTextEdit(QGridWidget):
    normal_color = '#FFFFFF'
    hover_color = '#FFFFFF'
    focus_color = '#FFFFFF'

    def __init__(self, parent = None, placeholder: str = '', name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedTextEdit', True)
        self.setProperty('color', 'main')

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder)
        self.grid_layout.addWidget(self.text_edit, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)
        self.grid_layout.setAlignment(self.label, Qt.AlignmentFlag.AlignTop)

        self.text_edit.base_focusInEvent = self.text_edit.focusInEvent
        self.text_edit.base_focusOutEvent = self.text_edit.focusOutEvent
        self.text_edit.focusInEvent = self.focusInEvent
        self.text_edit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.text_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self.focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.text_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self.hover_color}')
        else: self.label.setStyleSheet(f'color: {self.normal_color}')

    def text(self) -> str:
        return self.text_edit.toPlainText()

    def setText(self, text: str) -> None:
        self.text_edit.setText(text)

    def placeholderText(self) -> str:
        return self.text_edit.placeholderText()

    def setPlaceholderText(self, text: str) -> None:
        self.text_edit.setPlaceholderText(text)

    def isReadOnly(self) -> bool:
        return self.text_edit.isReadOnly()

    def setReadOnly(self, read_only: bool) -> None:
        self.text_edit.setReadOnly(read_only)

    def isEnabled(self) -> bool:
        return self.text_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.text_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
