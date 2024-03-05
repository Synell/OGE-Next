#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDoubleSpinBox, QLabel
from PySide6.QtCore import Qt, QEvent, Signal
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedDoubleSpinBox(QGridWidget):
    value_changed = Signal(float)

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedDoubleSpinBox._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedDoubleSpinBox._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedDoubleSpinBox._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedDoubleSpinBox', True)
        self.setProperty('color', 'main')

        self.double_spin_box = QDoubleSpinBox()
        self.grid_layout.addWidget(self.double_spin_box, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.double_spin_box.base_focusInEvent = self.double_spin_box.focusInEvent
        self.double_spin_box.base_focusOutEvent = self.double_spin_box.focusOutEvent
        self.double_spin_box.focusInEvent = self.focusInEvent
        self.double_spin_box.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

        self.double_spin_box.valueChanged.connect(self.value_changed.emit)

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.double_spin_box.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.double_spin_box.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def value(self) -> float:
        return self.double_spin_box.value()

    def setValue(self, value: float) -> None:
        self.double_spin_box.setValue(value)

    def set_value(self, value: float) -> None:
        self.double_spin_box.setValue(value)

    def range(self) -> tuple[float, float]:
        return (self.double_spin_box.minimum(), self.double_spin_box.maximum())

    def setRange(self, min_value: float, max_value: float) -> None:
        self.double_spin_box.setRange(min_value, max_value)

    def set_range(self, min_value: float, max_value: float) -> None:
        self.double_spin_box.setRange(min_value, max_value)

    def singleStep(self) -> float:
        return self.double_spin_box.singleStep()
    
    def single_step(self) -> float:
        return self.double_spin_box.singleStep()

    def setSingleStep(self, step: float) -> None:
        self.double_spin_box.setSingleStep(step)

    def set_single_step(self, step: float) -> None:
        self.double_spin_box.setSingleStep(step)

    def suffix(self) -> str:
        return self.double_spin_box.suffix()

    def setSuffix(self, suffix: str) -> None:
        self.double_spin_box.setSuffix(suffix)

    def set_suffix(self, suffix: str) -> None:
        self.double_spin_box.setSuffix(suffix)

    def prefix(self) -> str:
        return self.double_spin_box.prefix()

    def setPrefix(self, prefix: str) -> None:
        self.double_spin_box.setPrefix(prefix)

    def set_prefix(self, prefix: str) -> None:
        self.double_spin_box.setPrefix(prefix)

    def minimum(self) -> float:
        return self.double_spin_box.minimum()

    def setMinimum(self, minimum: float) -> None:
        self.double_spin_box.setMinimum(minimum)

    def set_minimum(self, minimum: float) -> None:
        self.double_spin_box.setMinimum(minimum)

    def maximum(self) -> float:
        return self.double_spin_box.maximum()

    def setMaximum(self, maximum: float) -> None:
        self.double_spin_box.setMaximum(maximum)

    def set_maximum(self, maximum: float) -> None:
        self.double_spin_box.setMaximum(maximum)

    def setReadOnly(self, read_only: bool) -> None:
        self.double_spin_box.setReadOnly(read_only)

    def set_read_only(self, read_only: bool) -> None:
        self.double_spin_box.setReadOnly(read_only)

    def setEnabled(self, enabled: bool) -> None:
        self.double_spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.double_spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def decimals(self) -> int:
        return self.double_spin_box.decimals()

    def setDecimals(self, decimals: int) -> None:
        self.double_spin_box.setDecimals(decimals)

    def set_decimals(self, decimals: int) -> None:
        self.double_spin_box.setDecimals(decimals)
#----------------------------------------------------------------------
