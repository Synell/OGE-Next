#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Qt, QEvent, Signal
from enum import Enum
from .QGridWidget import QGridWidget
from ..QtCore import QBaseApplication
from .QHexSpinBox import QHexSpinBox
from ..QtGui import QssSelector
#----------------------------------------------------------------------

    # Class
class QNamedHexSpinBox(QGridWidget):
    class Mode(Enum):
        Hex = 0
        Text = 1

        def next(self) -> 'QNamedHexSpinBox.Mode':
            return QNamedHexSpinBox.Mode((self.value + 1) % len(QNamedHexSpinBox.Mode))

    value_changed = Signal(object)

    _mode_icons: list = [None, None]

    _normal_color = '#FFFFFF'
    _hover_color = '#FFFFFF'
    _focus_color = '#FFFFFF'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QNamedHexSpinBox._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedHexSpinBox._hover_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedHexSpinBox._focus_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedHexSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedHexSpinBox._mode_icons[0] = app.get_icon('hexspinbox/hex.png', True, app.save_data.IconMode.Global)
        QNamedHexSpinBox._mode_icons[1] = app.get_icon('hexspinbox/text.png', True, app.save_data.IconMode.Global)

    def __init__(self, parent = None, name: str = '', allow_mode_change: bool = False) -> None:
        super().__init__(parent)
        self._mode = QNamedHexSpinBox.Mode.Hex
        self._allow_mode_change = allow_mode_change

        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QNamedHexSpinBox', True)
        self.setProperty('color', 'main')

        self.hex_spinbox = QHexSpinBox()
        self.hex_spinbox.value_changed.connect(self._value_changed)
        self.grid_layout.addWidget(self.hex_spinbox, 0, 0)

        self.text_lineedit = QLineEdit()
        self.text_lineedit.textChanged.connect(self._text_changed)
        self.grid_layout.addWidget(self.text_lineedit, 0, 0)
        self.text_lineedit.setVisible(False)

        self.mode_button = QPushButton()
        self.mode_button.setIcon(self._mode_icons[0])
        self.mode_button.clicked.connect(lambda: self.set_mode(QNamedHexSpinBox.Mode.next(self.mode())))
        self.mode_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_layout.addWidget(self.mode_button, 0, 0, Qt.AlignmentFlag.AlignRight)
        self.mode_button.setVisible(allow_mode_change)

        self.label = QLabel(name)
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('inputhover', False)
        self.label.setProperty('inputfocus', False)

        self.hex_spinbox.base_focusInEvent = self.hex_spinbox.focusInEvent
        self.hex_spinbox.base_focusOutEvent = self.hex_spinbox.focusOutEvent
        self.hex_spinbox.focusInEvent = self.focusInEvent
        self.hex_spinbox.focusOutEvent = self.focusOutEvent

        self.text_lineedit.base_focusInEvent = self.text_lineedit.focusInEvent
        self.text_lineedit.base_focusOutEvent = self.text_lineedit.focusOutEvent
        self.text_lineedit.focusInEvent = self.focusInEvent
        self.text_lineedit.focusOutEvent = self.focusOutEvent

        self.leaveEvent()

    def enterEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', True)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._hover_color}')

    def leaveEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputhover', False)
        if not self.label.property('inputfocus'): self.label.setStyleSheet(f'color: {self._normal_color}')

    def focusInEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', True)
        self.hex_spinbox.base_focusInEvent(event) if self.mode() == QNamedHexSpinBox.Mode.Hex else self.text_lineedit.base_focusInEvent(event)
        self.label.setStyleSheet(f'color: {self._focus_color}')

    def focusOutEvent(self, event: QEvent = None) -> None:
        self.label.setProperty('inputfocus', False)
        self.hex_spinbox.base_focusOutEvent(event)
        self.text_lineedit.base_focusOutEvent(event)
        if self.label.property('inputhover'): self.label.setStyleSheet(f'color: {self._hover_color}')
        else: self.label.setStyleSheet(f'color: {self._normal_color}')

    def value(self) -> int:
        return self.hex_spinbox.value()
    
    def set_value(self, value: int) -> None:
        self.hex_spinbox.set_value(value)
        if self.allow_mode_change(): self.text_lineedit.setText(self._hex2str(f'{value:X}'))

    def set_minimum(self, minimum: int) -> None:
        self.hex_spinbox.set_minimum(minimum)

    def set_maximum(self, maximum: int) -> None:
        self.hex_spinbox.set_maximum(maximum)

    def set_range(self, minimum: int, maximum: int) -> None:
        self.hex_spinbox.set_range(minimum, maximum)

    def isEnabled(self) -> bool:
        return self.hex_spinbox.isEnabled()

    def setEnabled(self, enabled: bool) -> None:
        self.hex_spinbox.setEnabled(enabled)
        if self.allow_mode_change(): self.text_lineedit.setEnabled(enabled)
        self.label.setEnabled(enabled)
    
    def allow_mode_change(self) -> bool:
        return self._allow_mode_change

    def set_allow_mode_change(self, allow: bool) -> None:
        self._allow_mode_change = allow
        self.mode_button.setVisible(allow)

    def mode(self) -> Mode:
        return self._mode

    def set_mode(self, mode: Mode) -> None:
        if not self.allow_mode_change(): return

        self._mode = mode

        self.mode_button.setIcon(self._mode_icons[mode.value])
        self.hex_spinbox.setVisible(mode == QNamedHexSpinBox.Mode.Hex)
        self.text_lineedit.setVisible(mode == QNamedHexSpinBox.Mode.Text)

    def _value_changed(self, value: int) -> None:
        if self.allow_mode_change(): self.text_lineedit.setText(self._hex2str(f'{value:X}'))
        self.value_changed.emit(value)

    def _text_changed(self, text: str) -> None:
        self.hex_spinbox.set_value(int(self._str2hex(text), 16))
        self.value_changed.emit(self.value())

    def _str2hex(self, s: str) -> str:
        return ''.join([f'{ord(c):02X}' for c in s])

    def _hex2str(self, s: str) -> str:
        return ''.join([chr(int(s[i:i + 2], 16)) for i in range(0, len(s), 2)]) # Doesn't work with 3+ bytes characters but no need for now
#----------------------------------------------------------------------
