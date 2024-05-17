#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QMenu

from data.lib.QtUtils import QScrollableGridFrame, QGridFrame, QSidePanelItem, QIconWidget, QDropDownWidget, QLangData, QBetterToolTip, QMoreButton
from data.lib.oge import Semester
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class YearWidget(QScrollableGridFrame):
    refreshed = Signal(int, bool)
    _app = None

    def __init__(self, lang: QLangData, id_: int, number: int, item: QSidePanelItem) -> None:
        super().__init__()

        self._lang = lang
        self._id = id_
        self._number = number
        self._item = item

        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        self.setProperty('class', 'YearWidget')

        self._data: tuple[Semester] = None
        self._built = False

    @property
    def loaded(self) -> bool:
        return self._data is not None


    def set_data(self, data: tuple[Semester], force: bool = False) -> None:
        if self._data and not force: return
        if not all([isinstance(semester, Semester) for semester in data]) and self._built: return

        self._data = data
        self.build()


    def build(self) -> None:
        self._built = True
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        widget = QGridFrame()
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)
        self.scroll_layout.addWidget(widget, 0, 0)

        if all([bool(semester) for semester in self._data]):
            self._build_data()

        else:
            self._data = None
            self._build_not_enough_data()


    def _build_not_enough_data(self) -> None:
        pass


    def _build_data(self) -> None:
        pass


    def update_sidebar_item(self) -> None:
        if not self._data: return

        self._item.text = YearWidget.generate_sidebar_item_name(self._app, self._number)


    @staticmethod
    def generate_sidebar_item_name(app, number: int) -> str:
        return app.get_lang_data('QMainWindow.QSideBar.year').replace('%s', str(number))
#----------------------------------------------------------------------
