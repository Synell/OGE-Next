#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QEvent, Signal
from data.lib.qtUtils.QUtilsColor import QUtilsColor
from .QColorDialog import QColorDialog
#----------------------------------------------------------------------

    # Class
class QColorButton(QPushButton):
    color_changed = Signal(QUtilsColor)

    def __init__(self, parent = None, lang: dict = {}, color: QUtilsColor = QUtilsColor('#FFFFFF')) -> None:
        super().__init__(parent)

        self._color = QUtilsColor.from_rgba(color.rgba)
        self._lang = lang
        self.setProperty('QColorButton', True)
        self.setProperty('color', 'main')
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update()
        self.clicked.connect(self._clicked)

    def _clicked(self) -> None:
        result = QColorDialog(self.parent(), self._lang, self.color).exec()
        if result:
            self.color = result

    def update(self) -> None:
        self.setStyleSheet(f'background-color: {self.color.ahex};')
        return super().update()

    @property
    def color(self) -> QUtilsColor:
        return self._color

    @color.setter
    def color(self, color: QUtilsColor) -> None:
        self._color = color
        self.update()
        self.color_changed.emit(self.color)
#----------------------------------------------------------------------
