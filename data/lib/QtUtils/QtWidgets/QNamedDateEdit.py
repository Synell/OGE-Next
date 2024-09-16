#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDateEdit, QLabel
from PySide6.QtCore import Qt, QEvent, Signal, QDate
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedDateEdit(QGridWidget):
    date_changed = Signal(QDate)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedDateEdit._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedDateEdit._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedDateEdit._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedDateEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedDateEdit', True)
        self.setProperty('color', 'main')

        self.date_edit = QDateEdit()
        self.layout_.addWidget(self.date_edit, 0, 0)
        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.date_edit.base_focusInEvent = self.date_edit.focusInEvent
        self.date_edit.base_focusOutEvent = self.date_edit.focusOutEvent
        self.date_edit.focusInEvent = self.focusInEvent
        self.date_edit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

        self.date_edit.dateChanged.connect(self.date_changed.emit)

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.date_edit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.date_edit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')


    def date(self) -> QDate:
        return self.date_edit.date()

    def set_date(self, date: QDate) -> None:
        self.date_edit.setDate(date)


    def minimum_date(self) -> QDate:
        return self.date_edit.minimumDate()

    def set_minimum_date(self, date: QDate) -> None:
        self.date_edit.setMinimumDate(date)


    def maximum_date(self) -> QDate:
        return self.date_edit.maximumDate()

    def set_maximum_date(self, date: QDate) -> None:
        self.date_edit.setMaximumDate(date)


    def isEnabled(self) -> bool:
        return self.date_edit.isEnabled()
    
    def is_enabled(self) -> bool:
        return self.date_edit.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.date_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.date_edit.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
