#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTimeEdit, QLabel
from PySide6.QtCore import Qt, QEvent, Signal, QTime
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedTimeEdit(QGridWidget):
    time_changed = Signal(QTime)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedTimeEdit._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTimeEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedTimeEdit._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTimeEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedTimeEdit._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedTimeEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedTimeEdit', True)
        self.setProperty('color', 'main')

        self.time_edit = QTimeEdit()
        self.layout_.addWidget(self.time_edit, 0, 0)
        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.time_edit.base_focusInEvent = self.time_edit.focusInEvent
        self.time_edit.base_focusOutEvent = self.time_edit.focusOutEvent
        self.time_edit.focusInEvent = self.focusInEvent
        self.time_edit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

        self.time_edit.timeChanged.connect(self.time_changed.emit)

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.time_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.time_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')


    def time(self) -> QTime:
        return self.time_edit.date()

    def set_time(self, date: QTime) -> None:
        self.time_edit.setDate(date)


    def minimum_time(self) -> QTime:
        return self.time_edit.minimumDate()

    def set_minimum_time(self, date: QTime) -> None:
        self.time_edit.setMinimumDate(date)


    def maximum_time(self) -> QTime:
        return self.time_edit.maximumDate()

    def set_maximum_time(self, date: QTime) -> None:
        self.time_edit.setMaximumDate(date)


    def isEnabled(self) -> bool:
        return self.time_edit.isEnabled()
    
    def is_enabled(self) -> bool:
        return self.time_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.time_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.time_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
