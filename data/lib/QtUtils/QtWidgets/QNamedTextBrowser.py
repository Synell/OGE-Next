#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QTextBrowser
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedTextBrowser(QGridWidget):
    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedTextBrowser._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextBrowser': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedTextBrowser._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextBrowser': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedTextBrowser._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextBrowser': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, placeholder: str = '', name: str = '') -> None:
        super().__init__(parent)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedTextBrowser', True)
        self.setProperty('color', 'main')

        self.text_browser = QTextBrowser()
        self.text_browser.setPlaceholderText(placeholder)
        self.layout_.addWidget(self.text_browser, 0, 0)
        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)
        self.layout_.setAlignment(self.label, Qt.AlignmentFlag.AlignTop)

        self.text_browser.base_focusInEvent = self.text_browser.focusInEvent
        self.text_browser.base_focusOutEvent = self.text_browser.focusOutEvent
        self.text_browser.focusInEvent = self.focusInEvent
        self.text_browser.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.text_browser.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.text_browser.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def text(self) -> str:
        return self.text_browser.toPlainText()

    def setText(self, text: str) -> None:
        self.text_browser.setText(text)
        # self.setLineHeight(self._line_height)

    def append(self, text: str) -> None:
        self.text_browser.append(text)
        # self.setLineHeight(self._line_height)

    def clear(self) -> None:
        self.text_browser.clear()

    def placeholderText(self) -> str:
        return self.text_browser.placeholderText()

    def setPlaceholderText(self, text: str) -> None:
        self.text_browser.setPlaceholderText(text)

    def isReadOnly(self) -> bool:
        return self.text_browser.isReadOnly()

    def setReadOnly(self, read_only: bool) -> None:
        self.text_browser.setReadOnly(read_only)

    def isEnabled(self) -> bool:
        return self.text_browser.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.text_browser.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
