#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from .OGEWidget import OGEWidget
from data.lib.oge import UEAvg
from .IconLabel import IconLabel
from data.lib.QtUtils import QBetterToolTip
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class UEAvgWidget(OGEWidget):
    def __init__(self, ue_avg: UEAvg) -> None:
        super().__init__()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.setProperty('background', 'transparent')
        self.setProperty('class', 'UEAvgWidget')

        better_icon_label = QBetterToolTip(IconLabel)
        better_label = QBetterToolTip(QLabel)

        title_label = better_label(f'{ue_avg.title} ({ue_avg.coefficient if ue_avg.coefficient else "?"})')
        title_label.setProperty('class', 'title')
        self.layout_.addWidget(title_label, 0, 0)

        avg = ue_avg.average

        label = better_icon_label(f'{avg:.2f}/20' if avg is not None else '?/20')

        if avg is None or ue_avg.is_only_missing_coefficient or ue_avg.has_missing_data:
            label.setIcon(UEAvgWidget._OGE_WEIRD_ICON)
            label.setToolTip(UEAvgWidget._OGE_WEIRD_TOOLTIP)
            label.setProperty('oge-weird', True)
            label.setCursor(Qt.CursorShape.WhatsThisCursor)
            title_label.setToolTip(UEAvgWidget._OGE_WEIRD_TOOLTIP)
            title_label.set_tooltip_property('oge-weird', True)
            title_label.setCursor(Qt.CursorShape.WhatsThisCursor)

        else:
            label.setStyleSheet(f'color: {UEAvgWidget.perc2color(avg / 20)}')

        label.setProperty('class', 'average')
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.layout_.addWidget(label, 0, 1)
#----------------------------------------------------------------------
