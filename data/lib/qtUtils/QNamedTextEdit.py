#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTextEdit, QLabel
from PySide6.QtCore import Qt, QEvent, Signal
from .QGridWidget import QGridWidget
from . import QBaseApplication
from .QssSelector import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedTextEdit(QGridWidget):
    text_changed = Signal(str)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedTextEdit._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedTextEdit._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedTextEdit._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

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

        self.text_edit.textChanged.connect(self._text_changed) # TF is this shit Qt??

    def _text_changed(self, text: str = None) -> None:
        self.text_changed.emit(text if text is not None else self.text_edit.toPlainText())

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.text_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.text_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def text(self) -> str:
        return self.text_edit.toPlainText()

    def setText(self, text: str) -> None:
        self.text_edit.setPlainText(text)

    def set_text(self, text: str) -> None:
        self.setText(text)

    def append(self, text: str) -> None:
        self.text_edit.append(text)

    def clear(self) -> None:
        self.text_edit.clear()

    def placeholderText(self) -> str:
        return self.text_edit.placeholderText()
    
    def placeholder_text(self) -> str:
        return self.text_edit.placeholderText()

    def setPlaceholderText(self, text: str) -> None:
        self.text_edit.setPlaceholderText(text)

    def set_placeholder_text(self, text: str) -> None:
        self.text_edit.setPlaceholderText(text)

    def isReadOnly(self) -> bool:
        return self.text_edit.isReadOnly()
    
    def is_read_only(self) -> bool:
        return self.text_edit.isReadOnly()

    def setReadOnly(self, read_only: bool) -> None:
        self.text_edit.setReadOnly(read_only)

    def set_read_only(self, read_only: bool) -> None:
        self.text_edit.setReadOnly(read_only)

    def isEnabled(self) -> bool:
        return self.text_edit.isEnabled()
    
    def is_enabled(self) -> bool:
        return self.text_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.text_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.text_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
