#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QEvent, Signal
from typing import Callable

from .QGridWidget import QGridWidget
from .QGridFrame import QGridFrame
from ..QtCore import QBaseApplication
from ..QtCore.QTerminalModel import QTerminalModel
from ..QtCore.QEnumColor import QEnumColor
from ..QtCore.QTerminalAction import QTerminalAction
from ..QtGui import QssSelector
from ..QtWebEngineCore import QTerminalWebEngineView
#----------------------------------------------------------------------

    # Class
class QTerminalWidget(QGridWidget):
    action_triggered = Signal(QTerminalAction)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QTerminalWidget._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QTerminalWidget._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QTerminalWidget._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QTerminalModel.init(app)


    def __init__(self, parent = None, name: str = '', *enum_colors: type[QEnumColor], terminal_name: str = '') -> None:
        super().__init__(parent)

        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QTerminalWidget', True)
        self.setProperty('color', 'main')

        self._root = QGridFrame()
        self._root.layout_.setContentsMargins(10, 10, 10, 10)
        self._root.layout_.setSpacing(0)
        self.layout_.addWidget(self._root, 0, 0)

        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)
        self.layout_.setAlignment(self.label, Qt.AlignmentFlag.AlignTop)


        self._terminal_view = QTerminalWebEngineView(None, QTerminalModel(*enum_colors, name = terminal_name))
        self._terminal_view.action_triggered.connect(self.action_triggered.emit)
        self._root.layout_.addWidget(self._terminal_view)

        self._terminal_view.base_focusInEvent = self._terminal_view.focusInEvent
        self._terminal_view.base_focusOutEvent = self._terminal_view.focusOutEvent
        self._terminal_view.focusInEvent = self.focusInEvent
        self._terminal_view.focusOutEvent = self.focusOutEvent

        self.leaveEvent()


    @property
    def model(self) -> QTerminalModel:
        return self._terminal_view.model


    @property
    def html(self) -> str:
        return self._terminal_view.html


    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self._terminal_view.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self._terminal_view.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')


    def log_empty(self) -> None:
        self._terminal_view.log_empty()


    def log(self, text: str, *log_types: QEnumColor, continuous: bool = False) -> None:
        self._terminal_view.log(text, *log_types, continuous = continuous)


    def clear(self) -> None:
        self._terminal_view.clear()


    def isEnabled(self) -> bool:
        return self._terminal_view.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self._terminal_view.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
