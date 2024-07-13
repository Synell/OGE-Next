#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QColorPicker import QColorPicker
from ..QtGui import QUtilsColor
from ..QtCore import QLangData
#----------------------------------------------------------------------

    # Class
class QColorDialog(QDialog):
    def __init__(self, parent = None , lang: QLangData = {}, color: QUtilsColor = QUtilsColor('#FFFFFF')):
        super().__init__(parent)

        self.setWindowTitle(lang['title'])

        self.root = QGridFrame(self)
        self.root.layout_.setContentsMargins(0, 0, 0, 0)
        self.root.layout_.setSpacing(0)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        self.root.layout_.addWidget(frame, 0, 0)

        self.color_picker = QColorPicker(None, QUtilsColor.from_rgba(color.rgba))
        frame.layout_.addWidget(self.color_picker, 0, 0)
        frame.layout_.setAlignment(self.color_picker, Qt.AlignmentFlag.AlignCenter)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        frame.setProperty('border-top', True)
        self.root.layout_.addWidget(frame, 1, 0)

        right_buttons = QGridFrame()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang.get('QPushButton.cancel'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(button, 0, 0)

        button = QPushButton(lang.get('QPushButton.select'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.layout_.addWidget(button, 0, 1)

        frame.layout_.addWidget(right_buttons, 0, 0)
        frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.root.layout_)

    def exec(self) -> QUtilsColor | None:
        if super().exec(): return self.color_picker.color
#----------------------------------------------------------------------
