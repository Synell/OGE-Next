#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import Qt, QEvent
from .QGridWidget import QGridWidget
from . import QBaseApplication
from .QssSelector import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedComboBox(QGridWidget):
    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedComboBox._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedComboBox._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedComboBox._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

    def __init__(self, parent = None, name: str = '') -> None:
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedComboBox', True)
        self.setProperty('color', 'main')
        self.setProperty('transparent', True)

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
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.combo_box.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.combo_box.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')
#----------------------------------------------------------------------
