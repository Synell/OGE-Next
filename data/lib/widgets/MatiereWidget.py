#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Subject
from .NoteGroupWidget import NoteGroupWidget
#----------------------------------------------------------------------

    # Class
class MatiereWidget(OGEWidget):
    def __init__(self, matiere: Subject) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'MatiereWidget')

        label = QLabel(f'{matiere.title} ({matiere.coefficient if matiere.coefficient else "?"})')
        label.setProperty('class', 'title')
        if matiere.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = matiere.average

        label = QLabel(f'{avg:.2f}/20' if avg is not None else '?/20')
        if avg is None: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        else: label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')
        label.setProperty('class', 'moyenne')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        for index, note_group in enumerate(matiere.grade_groups):
            frame = NoteGroupWidget(note_group)
            self.grid_layout.addWidget(frame, index + 1, 0, 1, 2)
#----------------------------------------------------------------------
