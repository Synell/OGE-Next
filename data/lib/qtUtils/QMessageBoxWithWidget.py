#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from PySide6.QtWidgets import QGridLayout, QWidget, QDialog, QPushButton, QStyle, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

from . import QBaseApplication
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QMessageBoxWithWidget(QDialog):
    class Icon(Enum):
        NoIcon = None
        Information = QStyle.StandardPixmap.SP_MessageBoxInformation
        Warning = QStyle.StandardPixmap.SP_MessageBoxWarning
        Critical = QStyle.StandardPixmap.SP_MessageBoxCritical
        About = QStyle.StandardPixmap.SP_MessageBoxQuestion

    def __init__(self, app: QBaseApplication = None, title: str = '', text: str = '', informative_text: str = '', icon: Icon|QIcon = Icon.NoIcon, widget: QWidget = None):
        super().__init__(parent = app.window)
        self._layout = QGridLayout(self)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.MSWindowsFixedSizeDialogHint)

        self._left = QWidget()
        self._left_layout = QGridLayout(self._left)

        self._right = QWidget()
        self._right_layout = QGridLayout(self._right)
        self._right_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._msg_box_widget = widget

        self._layout.addWidget(self._left, 0, 0)
        self._layout.addWidget(self._right, 0, 1)
        if self._msg_box_widget:
            self._layout.addWidget(self._msg_box_widget, 1, 0, 1, 2)

        if app:
            match icon:
                case QMessageBoxWithWidget.Icon.Warning: app.beep()
                case QMessageBoxWithWidget.Icon.Critical: app.beep()

        pixmap = QLabel()
        pixmap.setPixmap(self._generatePixmap(icon))
        self._left_layout.addWidget(pixmap)
        self._left_layout.setAlignment(pixmap, Qt.AlignmentFlag.AlignTop)
        self._left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(title)

        text = QLabel(text)
        informative_text = QLabel(informative_text)

        self._right_layout.addWidget(text, 0, 0)
        self._right_layout.setAlignment(text, Qt.AlignmentFlag.AlignLeft)
        self._right_layout.addWidget(informative_text, 1, 0)
        self._right_layout.setAlignment(informative_text, Qt.AlignmentFlag.AlignLeft)

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton('OK')
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 0)

        self._layout.addWidget(right_buttons, 2, 1)
        self._layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)


    def _generatePixmap(self, icon: Icon|QIcon = Icon.NoIcon):
        if type(icon) is QMessageBoxWithWidget.Icon:
            style = self.style()
            icon_size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize)
            icon = style.standardIcon(icon.value)
        elif type(icon) is not QIcon:
            return QPixmap()

        if not icon.isNull():
            return icon.pixmap(icon_size)
        return QPixmap()
#----------------------------------------------------------------------
