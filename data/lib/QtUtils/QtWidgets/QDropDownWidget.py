#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QMouseEvent
from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
from ..QtCore import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QDropDownWidget(QGridFrame):
    class _ShowHideButton(QGridFrame):
        clicked = Signal()

        def __init__(self, header: QWidget, icon: QIconWidget) -> None:
            super().__init__()
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(0)
            self.layout_.addWidget(header, 0, 0)
            self.layout_.addWidget(icon, 0, 1)
            self.layout_.setColumnStretch(2, 1)

        def mousePressEvent(self, event: QMouseEvent) -> None:
            self.clicked.emit()
            return super().mousePressEvent(event)

    clicked = Signal()

    _close_icon = None
    _open_icon = None

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QDropDownWidget._close_icon = app.save_data.get_icon('/dropdownwidget/close.png', True, app.save_data.IconMode.Global)
        QDropDownWidget._open_icon = app.save_data.get_icon('/dropdownwidget/open.png', True, app.save_data.IconMode.Global)

    def __init__(self, header: str | QWidget = '', widget: QWidget = None, already_open: bool = False) -> None:
        super().__init__()
        self.layout_.setSpacing(1)
        self.setContentsMargins(0, 0, 0, 0)

        # self.layout_.setColumnStretch(1, 1)
        self.layout_.setRowStretch(2, 1)

        self._must_be_shown = already_open
        self._icon = QIconWidget(None, self._close_icon if not already_open else self._open_icon, QSize(32, 32), False)

        self._show_hide_button = QDropDownWidget._ShowHideButton(self._convert_header(header), self._icon)
        self._show_hide_button.clicked.connect(self._show_hide_button_clicked)

        self._show_hide_widget = widget

        self.layout_.addWidget(self._show_hide_button, 0, 0)
        self.layout_.setAlignment(self._show_hide_button, Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self._show_hide_widget , 1, 0)

        if not already_open: self._show_hide_widget.hide()

    def _convert_header(self, header: str | QWidget) -> QWidget:
        if isinstance(header, str):
            return QLabel(header)

        return header

    def _show_hide_button_clicked(self, event = None) -> None:
        self._must_be_shown = not self._must_be_shown
        self._icon.icon = self._open_icon if self._must_be_shown else self._close_icon

        if self._must_be_shown: self._show_hide_widget.show()
        else: self._show_hide_widget.hide()

        self.clicked.emit()
#----------------------------------------------------------------------
