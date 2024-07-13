#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGridLayout, QDialog, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize

from ..QtCore import QBaseApplication
from .QGridWidget import QGridWidget
from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
#----------------------------------------------------------------------

    # Class
class QAboutBox(QDialog):
    def __init__(self, app: QBaseApplication = None, title: str = '', logo: str = '', texts: list[str] = []):
        super().__init__(parent = app.window)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)

        self._layout = QGridLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.left = QGridWidget()

        self.right = QGridWidget()
        self.right.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.right.layout_.setSpacing(20)
        self.right.layout_.setContentsMargins(20, 20, 20, 20)

        self.__down__ = QGridWidget()

        self._layout.addWidget(self.left, 0, 0)
        self._layout.addWidget(self.right, 0, 1)


        icon_widget = QIconWidget(None, logo, QSize(128, 128), False)

        self.left.layout_.addWidget(icon_widget)
        self.left.layout_.setAlignment(icon_widget, Qt.AlignmentFlag.AlignTop)
        self.left.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(title)


        text = QLabel(title)
        text.setProperty('h', 2)
        self.right.layout_.addWidget(text, 0, 0)
        self.right.layout_.setAlignment(text, Qt.AlignmentFlag.AlignTop)

        self.right.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)

        for textID in range(len(texts)):
            lines = texts[textID].split('\n')
            if len(lines) == 1: label = self.generate_label(texts[textID])
            else: label = self.generate_label_group(lines)
            self.right.layout_.addWidget(label, textID + 1, 0)
            self.right.layout_.setAlignment(label, Qt.AlignmentFlag.AlignTop)


        right_buttons = QGridWidget()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton('OK')
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('class', 'gray')
        right_buttons.layout_.addWidget(button, 0, 1)

        self.frame = QGridFrame()
        self.frame.layout_.addWidget(right_buttons, 0, 0)
        self.frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self.frame.layout_.setSpacing(0)
        self.frame.layout_.setContentsMargins(16, 16, 16, 16)
        self.frame.setProperty('border-top', True)
        self.frame.setProperty('border-bottom', True)
        self.frame.setProperty('border-left', True)
        self.frame.setProperty('border-right', True)

        self._layout.addWidget(self.frame, 1, 0, 1, 2)
        self._layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignBottom)

        self.right.setFixedWidth(int(self.right.sizeHint().width() * 1.5))

    def generate_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        return label

    def generate_label_group(self, texts: list[str]) -> QGridFrame:
        frame = QGridFrame()
        frame.layout_.setSpacing(0)
        frame.layout_.setContentsMargins(0, 0, 0, 0)

        for textID in range(len(texts)):
            label = self.generate_label(texts[textID])
            frame.layout_.addWidget(label, textID, 0)
            frame.layout_.setAlignment(label, Qt.AlignmentFlag.AlignTop)

        return frame
#----------------------------------------------------------------------
