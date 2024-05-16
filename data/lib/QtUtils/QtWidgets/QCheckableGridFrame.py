#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QCheckableGridFrame(QGridFrame):
    class Mode(Enum):
        CheckBox = 0
        RadioButton = 1


    clicked = Signal()
    check_changed = Signal(bool)


    def __init__(self, mode: Mode = Mode.CheckBox) -> None:
        super().__init__()
        self.setProperty("QCheckableGridFrame", True)
        self.setProperty('selected', False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._mode = mode
        self._checked = False


    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool) -> None:
        if self._checked == value: return

        self._checked = value
        self.check_changed.emit(value)

        self.setProperty('selected', value)
        self.style().polish(self)


    def toggle(self) -> None:
        self.checked = not self.checked
        self.check_changed.emit(self.checked)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        match self._mode:
            case QCheckableGridFrame.Mode.CheckBox:
                self.toggle()

            case QCheckableGridFrame.Mode.RadioButton:
                self.checked = True

        self.clicked.emit()
#----------------------------------------------------------------------
