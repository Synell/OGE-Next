#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDateTimeEdit, QLabel
from PySide6.QtCore import Qt, QEvent, Signal, QDateTime
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedDateTimeEdit(QGridWidget):
    date_time_changed = Signal(QDateTime)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedDateTimeEdit._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateTimeEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedDateTimeEdit._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateTimeEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedDateTimeEdit._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateTimeEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedDateTimeEdit', True)
        self.setProperty('color', 'main')

        self.date_time_edit = QDateTimeEdit()
        self.layout_.addWidget(self.date_time_edit, 0, 0)
        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.date_time_edit.base_focusInEvent = self.date_time_edit.focusInEvent
        self.date_time_edit.base_focusOutEvent = self.date_time_edit.focusOutEvent
        self.date_time_edit.focusInEvent = self.focusInEvent
        self.date_time_edit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

        self.date_time_edit.dateTimeChanged.connect(self.date_time_changed.emit)

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.date_time_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.date_time_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')


    def date_time(self) -> QDateTime:
        return self.date_time_edit.date()

    def set_date_time(self, date: QDateTime) -> None:
        self.date_time_edit.setDate(date)


    def minimum_date_time(self) -> QDateTime:
        return self.date_time_edit.minimumDate()

    def set_minimum_date_time(self, date: QDateTime) -> None:
        self.date_time_edit.setMinimumDate(date)


    def maximum_date_time(self) -> QDateTime:
        return self.date_time_edit.maximumDate()

    def set_maximum_date_time(self, date: QDateTime) -> None:
        self.date_time_edit.setMaximumDate(date)


    def isEnabled(self) -> bool:
        return self.date_time_edit.isEnabled()
    
    def is_enabled(self) -> bool:
        return self.date_time_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.date_time_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.date_time_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
