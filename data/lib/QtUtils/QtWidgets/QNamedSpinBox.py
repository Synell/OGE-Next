#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QSpinBox, QLabel
from PySide6.QtCore import Qt, QEvent, Signal
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedSpinBox(QGridWidget):
    value_changed = Signal(int)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedSpinBox._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedSpinBox._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedSpinBox._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedSpinBox', True)
        self.setProperty('color', 'main')

        self.spin_box = QSpinBox()
        self.layout_.addWidget(self.spin_box, 0, 0)
        self.label = QLabel(name)
        self.layout_.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.spin_box.base_focusInEvent = self.spin_box.focusInEvent
        self.spin_box.base_focusOutEvent = self.spin_box.focusOutEvent
        self.spin_box.focusInEvent = self.focusInEvent
        self.spin_box.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

        self.spin_box.valueChanged.connect(self.value_changed.emit)

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.spin_box.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.spin_box.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def value(self) -> int:
        return self.spin_box.value()

    def setValue(self, value: int) -> None:
        self.spin_box.setValue(value)

    def set_value(self, value: int) -> None:
        self.spin_box.setValue(value)

    def range(self) -> tuple[int, int]:
        return (self.spin_box.minimum(), self.spin_box.maximum())

    def setRange(self, min_value: int, max_value: int) -> None:
        self.spin_box.setRange(min_value, max_value)

    def set_range(self, min_value: int, max_value: int) -> None:
        self.spin_box.setRange(min_value, max_value)

    def singleStep(self) -> int:
        return self.spin_box.singleStep()
    
    def single_step(self) -> int:
        return self.spin_box.singleStep()

    def setSingleStep(self, step: int) -> None:
        self.spin_box.setSingleStep(step)

    def set_single_step(self, step: int) -> None:
        self.spin_box.setSingleStep(step)

    def suffix(self) -> str:
        return self.spin_box.suffix()

    def setSuffix(self, suffix: str) -> None:
        self.spin_box.setSuffix(suffix)

    def set_suffix(self, suffix: str) -> None:
        self.spin_box.setSuffix(suffix)

    def prefix(self) -> str:
        return self.spin_box.prefix()

    def setPrefix(self, prefix: str) -> None:
        self.spin_box.setPrefix(prefix)

    def set_prefix(self, prefix: str) -> None:
        self.spin_box.setPrefix(prefix)

    def minimum(self) -> int:
        return self.spin_box.minimum()

    def setMinimum(self, minimum: int) -> None:
        self.spin_box.setMinimum(minimum)

    def set_minimum(self, minimum: int) -> None:
        self.spin_box.setMinimum(minimum)

    def maximum(self) -> int:
        return self.spin_box.maximum()

    def setMaximum(self, maximum: int) -> None:
        self.spin_box.setMaximum(maximum)

    def set_maximum(self, maximum: int) -> None:
        self.spin_box.setMaximum(maximum)

    def setReadOnly(self, read_only: bool) -> None:
        self.spin_box.setReadOnly(read_only)

    def set_read_only(self, read_only: bool) -> None:
        self.spin_box.setReadOnly(read_only)

    def setEnabled(self, enabled: bool) -> None:
        self.spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
