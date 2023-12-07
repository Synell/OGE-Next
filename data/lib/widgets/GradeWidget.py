#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from .OGEWidget import OGEWidget
from data.lib.oge import Grade
from data.lib.qtUtils import QIconWidget
#----------------------------------------------------------------------

    # Class
class GradeWidget(OGEWidget):
    _OGE_NEW_ICON: QPixmap = None

    def __init__(self, grade: Grade) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'GradeWidget')

        if grade.is_new:
            iw = QIconWidget(self, self._OGE_NEW_ICON, QSize(16, 16), False)
            self.grid_layout.addWidget(iw, 0, self.grid_layout.count(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        label = QLabel(f'{grade.value if grade.value is None else "?"}/{grade.total}')
        label.setStyleSheet(f'color: {GradeWidget.perc2color(grade.value / grade.total) if not grade.has_missing_data else "#00DEFF"}')
        label.setProperty('class', 'grade')
        self.grid_layout.addWidget(label, 0, self.grid_layout.count())

        label = QLabel(f'({grade.coefficient})')
        label.setProperty('class', 'coefficient')
        self.grid_layout.addWidget(label, 0, self.grid_layout.count())

        self.grid_layout.setColumnStretch(2, 1)
#----------------------------------------------------------------------
