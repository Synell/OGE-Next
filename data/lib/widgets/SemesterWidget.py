#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton
from data.lib.qtUtils import QScrollableGridFrame
from data.lib.oge import UE
from .UEWidget import UEWidget
#----------------------------------------------------------------------

    # Class
class SemesterWidget(QScrollableGridFrame):
    refreshed = Signal(int)

    def __init__(self, lang: dict, semester: int) -> None:
        super().__init__()
        self.set_smooth_mode(QScrollableGridFrame.SmoothMode.Cosine)

        self._lang = lang
        self._semester = semester

        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        self.setProperty('class', 'SemesterWidget')

        self._data = []

    def set_data(self, data: list[UE], force: bool = False) -> None:
        if self._data and not force: return

        self._data = data
        self.build()

    def build(self) -> None:
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        button = QPushButton(self._lang['QPushButton']['refresh'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.setProperty('transparent', True)
        button.clicked.connect(lambda: self.refreshed.emit(self._semester))
        self.scroll_layout.addWidget(button, 0, 0)

        for index, ue in enumerate(self._data):
            ue_widget = UEWidget(ue)
            self.scroll_layout.addWidget(ue_widget, index + 1, 0)
#----------------------------------------------------------------------
