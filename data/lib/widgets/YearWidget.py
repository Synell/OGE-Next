#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QMenu
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap

from data.lib.QtUtils import QScrollableGridFrame, QGridFrame, QSidePanelItem, QIconWidget, QDropDownWidget, QLangData, QBetterToolTip, QMoreButton
from data.lib.oge import Semester, UEAvg
from .UEAvgWidget import UEAvgWidget
from .OGEWidget import OGEWidget
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class YearWidget(QScrollableGridFrame):
    refreshed = Signal(int, bool)

    _ICON: str = ''
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

        if all([bool(semester) for semester in self._data]):
            self._build_data()

        else:
            self._data = None
            self._build_not_enough_data()


    def _build_not_enough_data(self) -> None:
        widget = QGridFrame()
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)
        self.scroll_layout.addWidget(widget, 0, 0)

        details_sw_icon_label = QLabel()
        icon = QIcon(self._ICON.replace('%s', 'invalid'))
        details_sw_icon_label.setPixmap(icon.pixmap(32, 32))
        self.update_sidebar_item()
        self._item.icon = icon

        details_subwidget = QGridFrame()
        details_subwidget.grid_layout.setContentsMargins(0, 0, 0, 0)
        details_subwidget.grid_layout.setSpacing(10)
        widget.grid_layout.addWidget(details_subwidget, widget.grid_layout.count(), 0)
        details_subwidget.grid_layout.setColumnStretch(2, 1)

        details_subwidget.grid_layout.addWidget(details_sw_icon_label, 0, 0)

        details_sw_title_label = QLabel()
        details_sw_title_label.setText(self._lang.get('QLabel.cannotLoad'))
        details_sw_title_label.setProperty('title', True)
        details_subwidget.grid_layout.addWidget(details_sw_title_label, 0, 1)

        details_sw_desc_label = QLabel()
        details_sw_desc_label.setProperty('desc', True)
        details_sw_desc_label.setWordWrap(True)

        details_sw_desc_label.setText(self._lang.get('QLabel.invalidData'))
        widget.grid_layout.addWidget(details_sw_desc_label, widget.grid_layout.count(), 0)


    def _build_data(self) -> None:
        widget = QGridFrame()
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)
        self.scroll_layout.addWidget(widget, 0, 0)

        better_grid_frame = QBetterToolTip(QGridFrame)

        details_subwidget = better_grid_frame()
        details_subwidget.grid_layout.setContentsMargins(0, 0, 0, 0)
        details_subwidget.grid_layout.setSpacing(10)
        widget.grid_layout.addWidget(details_subwidget, widget.grid_layout.count(), 0)
        details_subwidget.grid_layout.setColumnStretch(4, 1)

        details_sw_icon_label = QLabel()
        details_subwidget.grid_layout.addWidget(details_sw_icon_label, 0, 0)

        details_sw_title_label = QLabel()
        details_sw_title_label.setProperty('title', True)
        details_subwidget.grid_layout.addWidget(details_sw_title_label, 0, 1)

        details_sw_sep_label = QLabel()
        details_sw_sep_label.setProperty('title', True)
        details_sw_sep_label.setText(' • ')
        details_subwidget.grid_layout.addWidget(details_sw_sep_label, 0, 2)

        details_sw_general_avg_label = QLabel()
        details_sw_general_avg_label.setProperty('title', True)

        semester_avg_list = [semester.average for semester in self._data if semester.average is not None]
        if semester_avg_list:
            general_avg = sum(semester_avg_list) / max(sum([1 for semester in self._data if semester.average is not None]), 1)

        else:
            general_avg = None

        missing_data = any([semester.has_missing_data for semester in self._data])

        details_sw_general_avg_label.setText(
            f'{self._lang.get("QLabel.generalAverage")}'.replace('%s', f'{general_avg:.2f}/20')
            if general_avg is not None
            else self._lang.get('QLabel.noGeneralAverage')
        )

        if missing_data:
            details_sw_general_avg_label.setStyleSheet(f'color: #00DEFF')

        else:
            details_sw_general_avg_label.setStyleSheet(f'color: {OGEWidget.perc2color(general_avg / 20)}')

        details_subwidget.grid_layout.addWidget(details_sw_general_avg_label, 0, 3)

        details_sw_desc_label = QLabel()
        details_sw_desc_label.setProperty('desc', True)
        details_sw_desc_label.setWordWrap(True)

        ue10: list[UEAvg] = []
        ue8: list[UEAvg] = []
        ue_other: list[UEAvg] = []
        all_ues: list[UEAvg] = []

        total_ue = 0

        list_ues = [[] for _ in max([semester.ues for semester in self._data], key = len)]
        for semester in self._data:
            for j, ue in enumerate(semester.ues):
                list_ues[j].append(ue)

        for index, ues in enumerate(list_ues):
            ue_avg = UEAvg(ues)
            avg = ue_avg.average
            all_ues.append(ue_avg)
            self.scroll_layout.addWidget(UEAvgWidget(ue_avg), index + 1, 0)

            if avg is None:
                continue

            if avg >= 10:
                ue10.append(ue_avg)

            elif avg >= 8:
                ue8.append(ue_avg)

            else:
                ue_other.append(ue_avg)

            total_ue += 1


        ue10_count = len(ue10)
        ue8_count = len(ue8)
        ue_other_count = len(ue_other)

        title = ''
        icon = ''
        texts = []

        if total_ue == 0:
            icon = self._ICON.replace('%s', 'invalid')
            title = self._lang.get('QLabel.errorYear')
            texts.append(self._lang.get('QLabel.noUE'))

        elif ue10_count == total_ue:
            icon = self._ICON.replace('%s', 'perfect')
            title = self._lang.get('QLabel.perfectYear')

        elif ue_other_count > 0:
            icon = self._ICON.replace('%s', 'alert')
            title = self._lang.get('QLabel.alertYear')
            texts.append(self._lang.get('QLabel.below8').replace('%s', '\n'.join([f' • {ue.title} ({ue.average:.2f}/20)' for ue in ue_other])))

        else:
            icon = self._ICON.replace('%s', 'bad')
            title = self._lang.get('QLabel.badYear')
            texts.append(self._lang.get('QLabel.between8And10').replace('%s', '\n'.join([f' • {ue.title} ({ue.average:.2f}/20)' for ue in ue8])))

        details_sw_title_label.setText(title)
        if any(ue.has_missing_data for ue in all_ues):
            details_subwidget.setToolTip(self._lang.get('QToolTip.ogeWeirdTop'))
            details_subwidget.setCursor(Qt.CursorShape.WhatsThisCursor)
            details_subwidget.set_tooltip_property('oge-weird', True)
            details_subwidget.setProperty('oge-details', True)

        icon = QIcon(icon)
        details_sw_icon_label.setPixmap(icon.pixmap(32, 32))
        self.update_sidebar_item()
        self._item.icon = icon

        if texts:
            details_sw_desc_label.setText('\n\n'.join(texts))
            widget.grid_layout.addWidget(details_sw_desc_label, widget.grid_layout.count(), 0)


    def update_sidebar_item(self) -> None:
        if not self._data: return

        self._item.text = YearWidget.generate_sidebar_item_name(self._app, self._number, self._data if self._data else tuple())


    @staticmethod
    def generate_sidebar_item_name(app, number: int, semesters: tuple[Semester] = tuple()) -> str:
        s = app.get_lang_data('QMainWindow.QSideBar.year').replace('%s', str(number))
        if semesters:
            start_year = min([semester.start_year for semester in semesters if semester.start_year] + [999999999999])
            end_year = max([semester.end_year for semester in semesters if semester.end_year] + [0])

            if start_year != 0 and end_year != 999999999999:
                s += f' ({start_year}-{end_year})'

        return s
#----------------------------------------------------------------------
