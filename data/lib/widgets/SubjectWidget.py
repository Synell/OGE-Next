#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from .OGEWidget import OGEWidget
from data.lib.oge import Subject
from .GradeGroupWidget import GradeGroupWidget
from .IconLabel import IconLabel
#----------------------------------------------------------------------

    # Class
class SubjectWidget(OGEWidget):
    def __init__(self, subject: Subject) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'SubjectWidget')

        label = QLabel(f'{subject.title} ({subject.coefficient if subject.coefficient else "?"})')
        label.setProperty('class', 'title')
        if subject.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = subject.average

        label = IconLabel(f'{avg:.2f}/20' if avg is not None else '?/20')

        if avg is None or subject.has_missing_data:
            label.setIcon(self._OGE_WEIRD_ICON)
            label.setToolTip(self._OGE_WEIRD_TOOLTIP)
            label.setProperty('oge-weird', True)

        else:
            label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')

        label.setProperty('class', 'average')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        for index, grade_group in enumerate(subject.grade_groups):
            frame = GradeGroupWidget(grade_group)
            self.grid_layout.addWidget(frame, index + 1, 0, 1, 2)
#----------------------------------------------------------------------
