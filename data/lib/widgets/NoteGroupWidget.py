#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt

from data.lib.qtUtils import QFlowWidget
from .OGEWidget import OGEWidget
from data.lib.oge import GradeGroup
from .NoteWidget import NoteWidget
#----------------------------------------------------------------------

    # Class
class NoteGroupWidget(OGEWidget):
    def __init__(self, note_group: GradeGroup) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'NoteGroupWidget')

        label = QLabel(f'{note_group.title} ({note_group.coefficient if note_group.coefficient else "?"})')
        label.setProperty('class', 'title')
        if note_group.coefficient == 0: label.setToolTip(self._OGE_WEIRD_TOOLTIP)
        self.grid_layout.addWidget(label, 0, 0)

        avg = note_group.average

        label = QLabel(f'{avg:.2f}/20')
        label.setStyleSheet(f'color: {self.perc2color(avg / 20)}')
        label.setProperty('class', 'moyenne')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, 0, 1)

        flow_widget = QFlowWidget(None, Qt.Orientation.Horizontal, 10)
        flow_widget.setProperty('class', 'note-group')
        self.grid_layout.addWidget(flow_widget, 1, 0, 1, 2)

        for note in note_group.notes:
            frame = NoteWidget(note)
            flow_widget.flow_layout.addWidget(frame)
#----------------------------------------------------------------------
