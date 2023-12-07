#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLineEdit, QWidget
from PySide6.QtCore import Signal
from .QHexValidator import QHexValidator
#----------------------------------------------------------------------

    # Class
class QHexSpinBox(QLineEdit):
    value_changed = Signal(object)

    def __init__(self, parent: QWidget = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self._validator = QHexValidator(self)
        self.setValidator(self._validator)
        self.textChanged.connect(lambda h: self.value_changed.emit(int(h, 16)) if h else None)

    def set_minimum(self, minimum: int) -> None:
        self._validator.set_bottom(minimum)

    def set_maximum(self, maximum: int) -> None:
        self._validator.set_top(maximum)

    def set_range(self, minimum: int, maximum: int) -> None:
        self._validator.set_range(minimum, maximum)

    def value(self) -> int:
        return int(self.text(), 16)

    def set_value(self, value: int) -> None:
        self.setText(f'{value:X}')
#----------------------------------------------------------------------
