#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent

from .OGEWidget import OGEWidget
from data.lib.oge import UE
from .PoleWidget import PoleWidget
from .IconLabel import IconLabel
from data.lib.qtUtils import QGridFrame
#----------------------------------------------------------------------

    # Class
class UEWidget(OGEWidget):
    class _Header(QGridFrame):
        clicked = Signal()

        def __init__(self, ue: UE) -> None:
            super().__init__()
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.grid_layout.setContentsMargins(0, 0, 0, 0)
            self.grid_layout.setSpacing(0)
            self.setProperty('background', 'transparent')

            title_label = QLabel(f'{ue.title} ({ue.coefficient if ue.coefficient else "?"})')
            title_label.setProperty('class', 'title')
            self.grid_layout.addWidget(title_label, 0, 0)

            avg = ue.average

            label = IconLabel(f'{avg:.2f}/20' if avg is not None else '?/20')

            if avg is None or ue.is_only_missing_coefficient or ue.has_missing_pole_data:
                label.setIcon(UEWidget._OGE_WEIRD_ICON)
                label.setToolTip(UEWidget._OGE_WEIRD_TOOLTIP)
                label.setProperty('oge-weird', True)
                title_label.setToolTip(UEWidget._OGE_WEIRD_TOOLTIP)

            else:
                label.setStyleSheet(f'color: {UEWidget.perc2color(avg / 20)}')

            label.setProperty('class', 'average')
            label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            self.grid_layout.addWidget(label, 0, 1)

        def mousePressEvent(self, event: QMouseEvent) -> None:
            self.clicked.emit()
            return super().mousePressEvent(event)


    def __init__(self, ue: UE) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setProperty('class', 'UEWidget')

        self._header = self._Header(ue)
        self._header.clicked.connect(lambda: self.set_poles_visible(not self.poles_visible))
        self.grid_layout.addWidget(self._header, 0, 0)

        self._content_frame = QGridFrame()
        self._content_frame.setProperty('class', 'oge-content')
        self._content_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._content_frame.grid_layout.setSpacing(0)
        self.grid_layout.addWidget(self._content_frame, 1, 0)

        last_child = None

        for index, pole in enumerate(ue.poles):
            frame = PoleWidget(pole)
            if index == 0: frame.setProperty('first-child', True)
            self._content_frame.grid_layout.addWidget(frame, index, 0)
            last_child = frame

        if last_child: last_child.setProperty('last-child', True)

    @property
    def poles_visible(self) -> bool:
        return self._content_frame.isVisible()

    def set_poles_visible(self, visible: bool) -> None:
        self._content_frame.setVisible(visible)
#----------------------------------------------------------------------
