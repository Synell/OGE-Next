#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt

from data.lib.qtUtils import QFlowWidget
from .OGEWidget import OGEWidget
from data.lib.oge import GradeGroup
from .GradeWidget import GradeWidget
from .IconLabel import IconLabel
#----------------------------------------------------------------------

    # Class
class GradeGroupWidget(OGEWidget):
    def __init__(self, grade_group: GradeGroup) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'GradeGroupWidget')

        label = QLabel(f'{grade_group.title} ({grade_group.coefficient if grade_group.coefficient else "?"})')
        label.setProperty('class', 'title')
        if grade_group.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = grade_group.average

        label = IconLabel(f'{avg:.2f}/20' if avg is not None else '?/20')

        if avg is None or grade_group.has_missing_data:
            label.setIcon(self._OGE_WEIRD_ICON)
            label.setToolTip(self._OGE_WEIRD_TOOLTIP)
            label.setProperty('oge-weird', True)

        else:
            label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')

        label.setProperty('class', 'average')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        flow_widget = QFlowWidget(None, Qt.Orientation.Horizontal, 10)
        flow_widget.setProperty('class', 'grade-group')
        self.grid_layout.addWidget(flow_widget, 1, 0, 1, 2)

        for grade in grade_group.grades:
            frame = GradeWidget(grade)
            flow_widget.flow_layout.addWidget(frame)
#----------------------------------------------------------------------
