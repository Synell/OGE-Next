#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QMenu

from data.lib.QtUtils import QScrollableGridFrame, QGridFrame, QSidePanelItem, QIconWidget, QDropDownWidget, QLangData, QBetterToolTip, QMoreButton
from data.lib.oge import UE, Semester
from .UEWidget import UEWidget
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class SemesterWidget(QScrollableGridFrame):
    refreshed = Signal(int, bool)
    _ICON: QPixmap = ''
    _OGE_NEW_ICON: QPixmap = ''
    _app = None

    def __init__(self, lang: QLangData, id_: int, item: QSidePanelItem) -> None:
        super().__init__()

        self._lang = lang
        self._id = id_
        self._item = item

        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        self.setProperty('class', 'SemesterWidget')

        self._data: Semester = None

    @property
    def loaded(self) -> bool:
        return self._data is not None

    def set_data(self, data: Semester, force: bool = False) -> None:
        if self._data and not force: return

        self._data = data
        self.build()

    def build(self) -> None:
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        widget = QGridFrame()
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)
        self.scroll_layout.addWidget(widget, 0, 0)

        button = QMoreButton(self._lang.get('QPushButton.refreshGrades'))
        button.more_clicked.connect(self.refresh_more_clicked)
        button.setProperty('color', 'main')
        button.setProperty('transparent', True)
        button.clicked.connect(lambda: self.refreshed.emit(self._id, False))
        widget.grid_layout.addWidget(button, widget.grid_layout.count(), 0)

        better_grid_frame = QBetterToolTip(QGridFrame)

        details_subwidget = better_grid_frame()
        details_subwidget.grid_layout.setContentsMargins(0, 0, 0, 0)
        details_subwidget.grid_layout.setSpacing(10)
        widget.grid_layout.addWidget(details_subwidget, widget.grid_layout.count(), 0)
        details_subwidget.grid_layout.setColumnStretch(2, 1)

        details_sw_icon_label = QLabel()
        details_subwidget.grid_layout.addWidget(details_sw_icon_label, 0, 0)

        details_sw_title_label = QLabel()
        details_sw_title_label.setProperty('title', True)
        details_subwidget.grid_layout.addWidget(details_sw_title_label, 0, 1)

        details_sw_desc_label = QLabel()
        details_sw_desc_label.setProperty('desc', True)
        details_sw_desc_label.setWordWrap(True)

        ue10: list[UE] = []
        ue8: list[UE] = []
        ue_other: list[UE] = []

        total_ue = 0

        for index, ue in enumerate(self._data.ues):
            ue_widget = UEWidget(ue)
            self.scroll_layout.addWidget(ue_widget, index + 1, 0)

            if ue.average:
                if ue.average >= 10:
                    ue10.append(ue)

                elif ue.average >= 8:
                    ue8.append(ue)

                else:
                    ue_other.append(ue)

                total_ue += 1

        ue10_count = len(ue10)
        ue8_count = len(ue8)

        title = ''
        icon = ''
        texts = []

        if total_ue == 0:
            icon = self._ICON.replace('%s', 'alert')
            title = self._lang.get('QLabel.errorSemester')
            texts.append(self._lang.get('QLabel.noUE'))

        elif ue10_count == total_ue:
            icon = self._ICON.replace('%s', 'perfect')
            title = self._lang.get('QLabel.perfectSemester')

        elif ue10_count > total_ue / 2 and ue8_count >= total_ue - ue10_count:
            icon = self._ICON.replace('%s', 'good')
            title = self._lang.get('QLabel.goodSemester')
            texts.append(self._lang.get('QLabel.between8And10').replace('%s', '\n'.join([f' • {ue.title} ({ue.average:.2f}/20)' for ue in ue8])))

        elif ue10_count + ue8_count != total_ue:
            icon = self._ICON.replace('%s', 'bad')
            title = self._lang.get('QLabel.badSemester')
            texts.append(self._lang.get('QLabel.allBelow8'))

        else:
            icon = self._ICON.replace('%s', 'alert')
            title = self._lang.get('QLabel.alertSemester')
            texts.append(self._lang.get('QLabel.between8And10').replace('%s', '\n'.join([f' • {ue.title}' for ue in ue8])))
            texts.append(self._lang.get('QLabel.below8').replace('%s', '\n'.join([f' • {ue.title} ({ue.average:.2f}/20)' for ue in ue_other])))

        details_sw_title_label.setText(title)
        if self._data.has_missing_data:
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

        if self._data.new_grade_count:
            new_grades_title_subwidget = QGridFrame()
            new_grades_title_subwidget.grid_layout.setContentsMargins(0, 0, 0, 0)
            new_grades_title_subwidget.grid_layout.setSpacing(10)
            new_grades_title_subwidget.grid_layout.setColumnStretch(2, 1)

            new_grades_sw_icon_label = QIconWidget(None, self._OGE_NEW_ICON, QSize(32, 32), False)
            new_grades_title_subwidget.grid_layout.addWidget(new_grades_sw_icon_label, 0, 0, Qt.AlignmentFlag.AlignLeft)

            new_grades_sw_title_label = QLabel(self._lang.get('QLabel.newGrade' + ('s' if self._data.new_grade_count > 1 else '')).replace('%s', str(self._data.new_grade_count)))
            new_grades_sw_title_label.setProperty('title', True)
            new_grades_title_subwidget.grid_layout.addWidget(new_grades_sw_title_label, 0, 1)

            new_grades_sw_desc_label = QLabel(self._data.new_grades_str)
            new_grades_sw_desc_label.setProperty('desc', True)

            new_grades_subwidget = QDropDownWidget(new_grades_title_subwidget, new_grades_sw_desc_label, True)
            widget.grid_layout.addWidget(new_grades_subwidget, widget.grid_layout.count(), 0)


    def update_sidebar_item(self) -> None:
        if not self._data: return

        self._item.text = self._app.get_lang_data('QMainWindow.QSideBar.semester').replace(
            '%s',
            (
                (f'{self._data.number}' if self._data.number is not None else f'{self._data.id}?') +
                ' ' +
                (f'({"-".join([str(y) for y in self._data.years])})' if self._data.years else '(?-?)')
            )
        )


    def refresh_more_clicked(self) -> None:
        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        action = menu.addAction(self._lang.get('QAction.refreshAll'))
        action.triggered.connect(lambda: self.refreshed.emit(self._id, True))

        # menu.exec_(self.mapToGlobal(self.sender().pos()))
        menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomRight()))
#----------------------------------------------------------------------
