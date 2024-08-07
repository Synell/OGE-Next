#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from data.lib.QtUtils import QFlowWidget
from .OGEWidget import OGEWidget
from data.lib.oge import GradeGroup
from .GradeWidget import GradeWidget
from .IconLabel import IconLabel
from data.lib.QtUtils import QGridFrame, QBetterToolTip
#----------------------------------------------------------------------

    # Class
class GradeGroupWidget(OGEWidget):
    class _Header(QGridFrame):
        def __init__(self, grade_group: GradeGroup) -> None:
            super().__init__()
            self.setProperty('class', 'oge-header')
            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(0)

            better_icon_label = QBetterToolTip(IconLabel)
            better_label = QBetterToolTip(QLabel)

            title_label = better_label(f'{grade_group.title} ({grade_group.coefficient if grade_group.coefficient else "?"})')
            title_label.setProperty('class', 'title')
            self.layout_.addWidget(title_label, 0, 0)

            avg = grade_group.average

            label = better_icon_label(f'{avg:.2f}/20' if avg is not None else '?/20')

            if avg is None or grade_group.is_only_missing_coefficient or grade_group.has_missing_grade_data:
                label.setIcon(GradeGroupWidget._OGE_WEIRD_ICON)
                label.setToolTip(GradeGroupWidget._OGE_WEIRD_TOOLTIP)
                label.setCursor(Qt.CursorShape.WhatsThisCursor)
                label.setProperty('oge-weird', True)
                title_label.setToolTip(GradeGroupWidget._OGE_WEIRD_TOOLTIP)
                title_label.setCursor(Qt.CursorShape.WhatsThisCursor)
                title_label.set_tooltip_property('oge-weird', True)

            else:
                label.setStyleSheet(f'color: {GradeGroupWidget.perc2color(avg / 20)}')

            label.setProperty('class', 'average')
            label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            self.layout_.addWidget(label, 0, 1)


    def __init__(self, grade_group: GradeGroup) -> None:
        super().__init__()

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.setProperty('class', 'GradeGroupWidget')

        self._header = self._Header(grade_group)
        self.layout_.addWidget(self._header, 0, 0)

        self._content_frame = QGridFrame()
        self._content_frame.setProperty('class', 'oge-content')
        self._content_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._content_frame.layout_.setSpacing(0)
        self.layout_.addWidget(self._content_frame, 1, 0)

        flow_widget = QFlowWidget(None, Qt.Orientation.Horizontal, 10)
        flow_widget.setProperty('class', 'oge-subcontent')
        self._content_frame.layout_.addWidget(flow_widget, 0, 0)

        for grade in grade_group.grades:
            frame = GradeWidget(grade)
            flow_widget.layout_.addWidget(frame)
#----------------------------------------------------------------------
