#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QEvent, Signal
from .QGridWidget import QGridWidget
from . import QBaseApplication
from .QssSelector import QssSelector
from .QHexSpinBox import QHexSpinBox
#----------------------------------------------------------------------

    # Class
class QNamedHexSpinBox(QGridWidget):
    value_changed = Signal(int)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedHexSpinBox._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedHexSpinBox._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedHexSpinBox._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedHexSpinBox', True)
        self.setProperty('color', 'main')

        self.hex_spinbox = QHexSpinBox()
        self.hex_spinbox.value_changed.connect(self.value_changed.emit)
        self.grid_layout.addWidget(self.hex_spinbox, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.hex_spinbox.base_focusInEvent = self.hex_spinbox.focusInEvent
        self.hex_spinbox.base_focusOutEvent = self.hex_spinbox.focusOutEvent
        self.hex_spinbox.focusInEvent = self.focusInEvent
        self.hex_spinbox.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.hex_spinbox.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.hex_spinbox.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def value(self) -> int:
        return self.hex_spinbox.value()
    
    def set_value(self, value: int) -> None:
        self.hex_spinbox.set_value(value)

    def set_minimum(self, minimum: int) -> None:
        self.hex_spinbox.set_minimum(minimum)

    def set_maximum(self, maximum: int) -> None:
        self.hex_spinbox.set_maximum(maximum)

    def set_range(self, minimum: int, maximum: int) -> None:
        self.hex_spinbox.set_range(minimum, maximum)

    def isEnabled(self) -> bool:
        return self.hex_spinbox.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.hex_spinbox.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
