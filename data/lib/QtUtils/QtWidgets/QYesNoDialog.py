#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

from .QDialogBase import QDialogBase
from ..QtCore.QLangData import QLangData
#----------------------------------------------------------------------

    # Class
class QYesNoDialog(QDialogBase):
    def __init__(self, parent: QWidget = None, widget_or_text: QWidget | str = '???', lang: QLangData = QLangData.NoTranslation()) -> None:
        super().__init__(
            parent = parent,
            lang = lang,
            buttons = [
                QDialogBase.Button('no', lang.get('QPushButton.no'), {'color': 'white', 'transparent': True}, self.reject),
                QDialogBase.Button('yes', lang.get('QPushButton.yes'), {'color': 'main'}, self.accept),
            ],
            button_alignment = Qt.AlignmentFlag.AlignCenter,
        )

        if isinstance(widget_or_text, QWidget):
            self._content.layout_.addWidget(widget_or_text, 0, 0)

        elif isinstance(widget_or_text, str):
            label = QLabel(widget_or_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self._content.layout_.addWidget(label, 0, 0)

        else:
            raise TypeError('widget_or_text must be QWidget or str')
#----------------------------------------------------------------------
