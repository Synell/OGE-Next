#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Note
#----------------------------------------------------------------------

    # Class
class NoteWidget(OGEWidget):
    def __init__(self, note: Note) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'NoteWidget')

        label = QLabel(f'{note.value}/{note.total}')
        label.setStyleSheet(f'color: {self.perc2color(note.value / note.total)}')
        label.setProperty('class', 'note')
        self.grid_layout.addWidget(label, 0, 0)

        label = QLabel(f'({note.coeff})')
        label.setProperty('class', 'coeff')
        self.grid_layout.addWidget(label, 0, 1)

        self.grid_layout.setColumnStretch(2, 1)
#----------------------------------------------------------------------
