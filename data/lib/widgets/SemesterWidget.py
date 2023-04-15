#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QLabel
from data.lib.qtUtils import QScrollableGridFrame, QGridFrame, QSidePanelItem
from data.lib.oge import UE
from .UEWidget import UEWidget
#----------------------------------------------------------------------

    # Class
class SemesterWidget(QScrollableGridFrame):
    refreshed = Signal(int)
    ICON = ''

    def __init__(self, lang: dict, semester: int, item: QSidePanelItem) -> None:
        super().__init__()
        self.set_smooth_mode(QScrollableGridFrame.SmoothMode.Cosine)

        self._lang = lang
        self._semester = semester
        self._item = item

        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(50)
        self.setProperty('class', 'SemesterWidget')

        self._data = []

    def set_data(self, data: list[UE], force: bool = False) -> None:
        if self._data and not force: return

        self._data = data
        self.build()

    def build(self) -> None:
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        widget = QGridFrame()
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(20)
        self.scroll_layout.addWidget(widget, 0, 0)

        button = QPushButton(self._lang['QPushButton']['refresh'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.setProperty('transparent', True)
        button.clicked.connect(lambda: self.refreshed.emit(self._semester))
        widget.grid_layout.addWidget(button, 0, 0)

        subwidget = QGridFrame()
        subwidget.grid_layout.setContentsMargins(0, 0, 0, 0)
        subwidget.grid_layout.setSpacing(10)
        widget.grid_layout.addWidget(subwidget, 1, 0)
        subwidget.grid_layout.setColumnStretch(2, 1)

        icon_label = QLabel()
        subwidget.grid_layout.addWidget(icon_label, 0, 0)

        title_label = QLabel()
        title_label.setProperty('title', True)
        subwidget.grid_layout.addWidget(title_label, 0, 1)

        desc_label = QLabel()
        desc_label.setProperty('desc', True)
        desc_label.setWordWrap(True)

        ue10: list[UE] = []
        ue8: list[UE] = []
        ue_other: list[UE] = []

        for index, ue in enumerate(self._data):
            ue_widget = UEWidget(ue)
            self.scroll_layout.addWidget(ue_widget, index + 1, 0)

            if ue.average:
                if ue.average >= 10:
                    ue10.append(ue)

                elif ue.average >= 8:
                    ue8.append(ue)

                else:
                    ue_other.append(ue)

        total_ue = len(self._data)
        ue10_count = len(ue10)
        ue8_count = len(ue8)

        title = ''
        icon = ''
        texts = []

        if ue10_count == total_ue:
            icon = self.ICON.replace('%s', 'perfect')
            title = self._lang['QLabel']['perfectSemester']

        elif ue10_count > total_ue / 2 and ue8_count >= total_ue - ue10_count:
            icon = self.ICON.replace('%s', 'good')
            title = self._lang['QLabel']['goodSemester']
            texts.append(self._lang['QLabel']['between8And10'].replace('%s', '\n'.join([f' • {ue.title}' for ue in ue8])))

        elif ue10_count + ue8_count != total_ue:
            icon = self.ICON.replace('%s', 'bad')
            title = self._lang['QLabel']['badSemester']
            texts.append(self._lang['QLabel']['allBelow8'])

        else:
            icon = self.ICON.replace('%s', 'alert')
            title = self._lang['QLabel']['alertSemester']
            texts.append(self._lang['QLabel']['between8And10'].replace('%s', '\n'.join([f' • {ue.title}' for ue in ue8])))
            texts.append(self._lang['QLabel']['below8'].replace('%s', '\n'.join([f' • {ue.title}' for ue in ue_other])))

        title_label.setText(title)
        icon = QIcon(icon)
        icon_label.setPixmap(icon.pixmap(32, 32))
        self._item.icon = icon

        if texts:
            desc_label.setText('\n\n'.join(texts))
            widget.grid_layout.addWidget(desc_label, 2, 0)
#----------------------------------------------------------------------
