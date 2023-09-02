#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QSpinBox, QLabel
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
from . import QBaseApplication
from .QssSelector import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedSpinBox(QGridWidget):
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
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedSpinBox', True)
        self.setProperty('color', 'main')

        self.spin_box = QSpinBox()
        self.grid_layout.addWidget(self.spin_box, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.spin_box.base_focusInEvent = self.spin_box.focusInEvent
        self.spin_box.base_focusOutEvent = self.spin_box.focusOutEvent
        self.spin_box.focusInEvent = self.focusInEvent
        self.spin_box.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

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

    def range(self) -> tuple[int, int]:
        return (self.spin_box.minimum(), self.spin_box.maximum())

    def setRange(self, min_value: int, max_value: int) -> None:
        self.spin_box.setRange(min_value, max_value)

    def singleStep(self) -> int:
        return self.spin_box.singleStep()

    def setSingleStep(self, step: int) -> None:
        self.spin_box.setSingleStep(step)

    def suffix(self) -> str:
        return self.spin_box.suffix()

    def setSuffix(self, suffix: str) -> None:
        self.spin_box.setSuffix(suffix)

    def prefix(self) -> str:
        return self.spin_box.prefix()

    def setPrefix(self, prefix: str) -> None:
        self.spin_box.setPrefix(prefix)

    def minimum(self) -> int:
        return self.spin_box.minimum()

    def setMinimum(self, minimum: int) -> None:
        self.spin_box.setMinimum(minimum)

    def maximum(self) -> int:
        return self.spin_box.maximum()

    def setMaximum(self, maximum: int) -> None:
        self.spin_box.setMaximum(maximum)

    def setReadOnly(self, read_only: bool) -> None:
        self.spin_box.setReadOnly(read_only)

    def setEnabled(self, enabled: bool) -> None:
        self.spin_box.setEnabled(enabled)
        self.label.setEnabled(enabled)
#----------------------------------------------------------------------
