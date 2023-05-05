#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Grade
#----------------------------------------------------------------------

    # Class
class GradeWidget(OGEWidget):
    def __init__(self, grade: Grade) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'GradeWidget')

        label = QLabel(f'{grade.value}/{grade.total}')
        label.setStyleSheet(f'color: {self.perc2color(grade.value / grade.total)}')
        label.setProperty('class', 'grade')
        self.grid_layout.addWidget(label, 0, 0)

        label = QLabel(f'({grade.coefficient})')
        label.setProperty('class', 'coefficient')
        self.grid_layout.addWidget(label, 0, 1)

        self.grid_layout.setColumnStretch(2, 1)
#----------------------------------------------------------------------
