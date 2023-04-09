#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QComboBox, QLabel, QLayout
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QNamedComboBox(QGridWidget):
    normal_color = '#FFFFFF'
    hover_color = '#FFFFFF'
    focus_color = '#FFFFFF'

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedComboBox', True)
        self.setProperty('color', 'main')

        self.combo_box = QComboBox()
        self.combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_box.view().setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_layout.addWidget(self.combo_box, 0, 0)
        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.combo_box.base_focusInEvent = self.combo_box.focusInEvent
        self.combo_box.base_focusOutEvent = self.combo_box.focusOutEvent
        self.combo_box.focusInEvent = self.focusInEvent
        self.combo_box.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self.normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.combo_box.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self.focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.combo_box.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self.hover_color}')
        else: self.label.setStyleSheet(f'color: {self.normal_color}')
#----------------------------------------------------------------------
