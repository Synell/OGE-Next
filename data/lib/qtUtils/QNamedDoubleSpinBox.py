#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDoubleSpinBox, QLabel
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QNamedDoubleSpinBox(QGridWidget):
    normal_color = '#FFFFFF'
    hover_color = '#FFFFFF'
    focus_color = '#FFFFFF'

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

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.double_spin_box.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self.focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.double_spin_box.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self.hover_color}')
        else: self.label.setStyleSheet(f'color: {self.normal_color}')

    def value(self) -> float:
        return self.double_spin_box.value()

    def setValue(self, value: float) -> None:
        self.double_spin_box.setValue(value)

    def range(self) -> tuple[float, float]:
        return (self.double_spin_box.minimum(), self.double_spin_box.maximum())

    def setRange(self, min_value: float, max_value: float) -> None:
        self.double_spin_box.setRange(min_value, max_value)

    def singleStep(self) -> float:
        return self.double_spin_box.singleStep()

    def setSingleStep(self, step: float) -> None:
        self.double_spin_box.setSingleStep(step)

    def suffix(self) -> str:
        return self.double_spin_box.suffix()

    def setSuffix(self, suffix: str) -> None:
        self.double_spin_box.setSuffix(suffix)

    def prefix(self) -> str:
        return self.double_spin_box.prefix()

    def setPrefix(self, prefix: str) -> None:
        self.double_spin_box.setPrefix(prefix)

    def minimum(self) -> float:
        return self.double_spin_box.minimum()

    def setMinimum(self, minimum: float) -> None:
        self.double_spin_box.setMinimum(minimum)

    def maximum(self) -> float:
        return self.double_spin_box.maximum()

    def setMaximum(self, maximum: float) -> None:
        self.double_spin_box.setMaximum(maximum)

    def setReadOnly(self, read_only: bool) -> None:
        self.double_spin_box.setReadOnly(read_only)

    def setEnabled(self, enabled: bool) -> None:
        self.double_spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def decimals(self) -> int:
        return self.double_spin_box.decimals()

    def setDecimals(self, decimals: int) -> None:
        self.double_spin_box.setDecimals(decimals)
#----------------------------------------------------------------------
