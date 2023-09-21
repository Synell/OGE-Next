#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject
from PySide6.QtGui import QValidator
#----------------------------------------------------------------------

    # Class
class QHexValidator(QValidator):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self._bottom = 0
        self._top = 0xFFFFFFFF

    def bottom(self) -> int:
        return self._bottom

    def set_bottom(self, bottom: int) -> None:
        self._bottom = bottom
        if self._top < bottom: self._bottom, self._top = self._top, self._bottom

    def top(self) -> int:
        return self._top

    def set_top(self, top: int) -> None:
        self._top = top
        if self._bottom > top: self._bottom, self._top = self._top, self._bottom

    def set_range(self, bottom: int, top: int) -> None:
        self._bottom = bottom
        self._top = top
        if self._bottom > self._top: self._bottom, self._top = self._top, self._bottom

    def validate(self, input: str, pos: int) -> tuple:
        if input == '': return (QValidator.State.Acceptable, input, pos)

        try:
            i = int(input, 16)
            assert i >= self.bottom() and i <= self.top()

        except ValueError: return (QValidator.State.Invalid, input, pos)
        except AssertionError: return (QValidator.State.Invalid, input, pos)

        return (QValidator.State.Acceptable, f'{i:X}', pos)
#----------------------------------------------------------------------
