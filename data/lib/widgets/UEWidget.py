#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import UE
from .PoleWidget import PoleWidget
#----------------------------------------------------------------------

    # Class
class UEWidget(OGEWidget):
    def __init__(self, ue: UE) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'UEWidget')

        label = QLabel(f'{ue.title} ({ue.coefficient if ue.coefficient else "?"})')
        label.setProperty('class', 'title')
        if ue.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = ue.average

        label = QLabel(f'{avg:.2f}/20')
        label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')
        label.setProperty('class', 'moyenne')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        for index, pole in enumerate(ue.poles):
            frame = PoleWidget(pole)
            self.grid_layout.addWidget(frame, index + 1, 0, 1, 2)
#----------------------------------------------------------------------
