#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Pole
from .MatiereWidget import MatiereWidget
#----------------------------------------------------------------------

    # Class
class PoleWidget(OGEWidget):
    def __init__(self, pole: Pole) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'PoleWidget')

        label = QLabel(f'{pole.title} ({pole.coefficient})')
        label.setProperty('class', 'title')
        self.grid_layout.addWidget(label, 0, 0)

        avg = pole.average

        label = QLabel(f'{avg:.2f}/20')
        label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')
        label.setProperty('class', 'moyenne')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        for index, matiere in enumerate(pole.matieres):
            frame = MatiereWidget(matiere)
            self.grid_layout.addWidget(frame, index + 1, 0, 1, 2)
#----------------------------------------------------------------------
