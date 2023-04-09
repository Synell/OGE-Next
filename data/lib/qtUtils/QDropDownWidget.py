#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Qt, Signal
#----------------------------------------------------------------------

    # Class
class QDropDownWidget(QWidget):
    clicked = Signal()

    def __init__(self, text: str = '', widget: QWidget = None):
        super().__init__()
        self._layout = QGridLayout(self)
        self._layout.setSpacing(1)

        self._layout.setColumnStretch(1, 1)
        self._layout.setRowStretch(2, 1)

        self._show_hide_button = QPushButton(text)
        self._show_hide_button.setCheckable(True)
        self._show_hide_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._show_hide_button.setProperty('QDropDownWidget', True)
        self._show_hide_button.clicked.connect(self._show_hide_button_clicked)

        self.show_hide_widget = widget

        self._layout.addWidget(self._show_hide_button, 0, 0)
        self._layout.setAlignment(self._show_hide_button, Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self.show_hide_widget , 1, 0)

        self.show_hide_widget.hide()

    def _show_hide_button_clicked(self, event = None):
        if self._show_hide_button.isChecked(): self.show_hide_widget.show()
        else: self.show_hide_widget.hide()
        self.clicked.emit()
#----------------------------------------------------------------------
