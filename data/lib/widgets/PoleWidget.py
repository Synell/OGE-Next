#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Pole
from .SubjectWidget import SubjectWidget
from .IconLabel import IconLabel
#----------------------------------------------------------------------

    # Class
class PoleWidget(OGEWidget):
    def __init__(self, pole: Pole) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'PoleWidget')

        label = QLabel(f'{pole.title} ({pole.coefficient if pole.coefficient else "?"})')
        label.setProperty('class', 'title')
        if pole.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = pole.average

        label = IconLabel(f'{avg:.2f}/20' if avg is not None else '?/20')

        if avg is None or pole.has_missing_data:
            label.setIcon(self._OGE_WEIRD_ICON)
            label.setToolTip(self._OGE_WEIRD_TOOLTIP)
            label.setProperty('oge-weird', True)

        else:
            label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')

        label.setProperty('class', 'average')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        for index, subject in enumerate(pole.matieres):
            frame = SubjectWidget(subject)
            self.grid_layout.addWidget(frame, index + 1, 0, 1, 2)
#----------------------------------------------------------------------
