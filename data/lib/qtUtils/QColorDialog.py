#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QUtilsColor import QUtilsColor
from .QColorPicker import QColorPicker
#----------------------------------------------------------------------

    # Class
class QColorDialog(QDialog):
    def __init__(self, parent = None , lang: dict = {}, color: QUtilsColor = QUtilsColor('#FFFFFF')):
        super().__init__(parent)

        self.setWindowTitle(lang['title'])

        self.root = QGridFrame(self)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.root.grid_layout.setSpacing(0)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        self.root.grid_layout.addWidget(frame, 0, 0)

        self.color_picker = QColorPicker(None, QUtilsColor.from_rgba(color.rgba))
        frame.grid_layout.addWidget(self.color_picker, 0, 0)
        frame.grid_layout.setAlignment(self.color_picker, Qt.AlignmentFlag.AlignCenter)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(frame, 1, 0)

        right_buttons = QGridFrame()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(lang['QPushButton']['select'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        frame.grid_layout.addWidget(right_buttons, 0, 0)
        frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.root.grid_layout)

    def exec(self) -> QUtilsColor|None:
        if super().exec(): return self.color_picker.color
#----------------------------------------------------------------------
