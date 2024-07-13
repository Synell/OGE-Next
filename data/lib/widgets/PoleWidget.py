#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import Pole
from .SubjectWidget import SubjectWidget
from .IconLabel import IconLabel
from data.lib.QtUtils import QGridFrame, QBetterToolTip
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class PoleWidget(OGEWidget):
    class _Header(QGridFrame):
        def __init__(self, pole: Pole) -> None:
            super().__init__()
            self.setProperty('class', 'oge-header')
            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(0)

            better_icon_label = QBetterToolTip(IconLabel)
            better_label = QBetterToolTip(QLabel)

            title_label = better_label(f'{pole.title} ({pole.coefficient if pole.coefficient else "?"})')
            title_label.setProperty('class', 'title')
            self.layout_.addWidget(title_label, 0, 0)

            avg = pole.average

            label = better_icon_label(f'{avg:.2f}/20' if avg is not None else '?/20')

            if avg is None or pole.is_only_missing_coefficient or pole.has_missing_subject_data:
                label.setIcon(PoleWidget._OGE_WEIRD_ICON)
                label.setToolTip(PoleWidget._OGE_WEIRD_TOOLTIP)
                label.setCursor(Qt.CursorShape.WhatsThisCursor)
                label.setProperty('oge-weird', True)
                title_label.setToolTip(PoleWidget._OGE_WEIRD_TOOLTIP)
                title_label.setCursor(Qt.CursorShape.WhatsThisCursor)
                title_label.set_tooltip_property('oge-weird', True)

            else:
                label.setStyleSheet(f'color: {PoleWidget.perc2color(avg / 20)}')

            label.setProperty('class', 'average')
            label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            self.layout_.addWidget(label, 0, 1)


    def __init__(self, pole: Pole) -> None:
        super().__init__()

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.setProperty('class', 'PoleWidget')

        self._header = self._Header(pole)
        self.layout_.addWidget(self._header, 0, 0)

        self._content_frame = QGridFrame()
        self._content_frame.setProperty('class', 'oge-content')
        self._content_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._content_frame.layout_.setSpacing(0)
        self.layout_.addWidget(self._content_frame, 1, 0)

        last_child = None

        for index, subject in enumerate(pole.subjects):
            frame = SubjectWidget(subject)
            if index == 0: frame.setProperty('first-child', True)
            self._content_frame.layout_.addWidget(frame, index, 0)
            last_child = frame

        if last_child: last_child.setProperty('last-child', True)
#----------------------------------------------------------------------
