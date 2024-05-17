#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from .OGEWidget import OGEWidget
from data.lib.oge import Grade
from data.lib.QtUtils import QIconWidget, QBetterToolTip
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
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

        label = QLabel(self._tooltip_format(grade))
        label.setTextFormat(Qt.TextFormat.RichText)
        self.setToolTip(label)

        label = QLabel(f'{grade.value if grade.value is not None else "?"}/{grade.value_total}')
        label.setStyleSheet(f'color: {GradeWidget.perc2color(grade.value / grade.value_total) if not grade.has_missing_data else "#00DEFF"}')
        label.setProperty('class', 'grade')
        self.grid_layout.addWidget(label, 0, self.grid_layout.count())

        label = QLabel(f'({grade.coefficient if grade.coefficient is not None else "?"})')
        if grade.coefficient is None: label.setStyleSheet('color: #00DEFF')
        label.setProperty('class', 'coefficient')
        self.grid_layout.addWidget(label, 0, self.grid_layout.count())

        self.grid_layout.setColumnStretch(2, 1)


    def _tooltip_format(self, grade: Grade) -> str:
        name = grade.name if grade.name is not None else ''
        date = grade.date.strftime('%d/%m/%Y') if grade.date is not None else ''
        rank = f'{grade.rank if grade.rank is not None else "?"}/{grade.rank_total if grade.rank_total is not None else "?"}'
        rank_color = f'color: {GradeWidget.perc2color(1 - (grade.rank / grade.rank_total)) if not grade.has_missing_rank_data() else "#00DEFF"}'
        rank = f'<font style="{rank_color}">{rank}</font>'

        s = name
        if name and date: s += ' • '
        if date: s += date

        if s: s += '\n'
        s += rank

        return s.replace('\n', '<br>')
#----------------------------------------------------------------------
