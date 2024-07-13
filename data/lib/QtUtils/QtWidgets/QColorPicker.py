#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QPoint, Qt, Signal, QSize, QRect
from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox
from .QGridFrame import QGridFrame
from ..QtGui import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QColorPicker(QGridFrame):
    color_changed = Signal(QUtilsColor)

    def __init__(self, parent = None, color: QUtilsColor = QUtilsColor(), has_alpha: bool = True) -> None:
        super().__init__(parent)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(10)
        self._color = color
        self._hue_color__ = QUtilsColor.from_hsl(color.hue_hsl, 100.0, 50.0)
        self._has_alpha = has_alpha
        self._interaction_disabled = False

        self.setProperty('QColorPicker', True)
        self._create_widgets()
        self.color = color

    def _create_widgets(self) -> None:
        self._create_color_view()
        self._create_color_slider()
        self._create_alpha_slider()
        self._create_color_input()

    def _create_color_view(self) -> None:
        self._color_view = QFrame()
        self._color_view.setMinimumSize(QSize(300, 300))
        self._color_view.setMaximumSize(QSize(5000, 5000))
        self._color_view.setStyleSheet('background-color: qlineargradient(x1:1, x2:0, stop:0 hsl(0%,100%,50%), stop:1 rgba(255, 255, 255, 255));')
        self._color_view.setFrameShape(QFrame.Shape.StyledPanel)
        self._color_view.setFrameShadow(QFrame.Shadow.Raised)
        self._color_view.setProperty('Rounded', True)

        self._black_overlay = QFrame()
        self._black_overlay.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));')
        self._black_overlay.setFrameShape(QFrame.Shape.StyledPanel)
        self._black_overlay.setFrameShadow(QFrame.Shadow.Raised)
        self._black_overlay.setProperty('Rounded', True)

        self._selector = QFrame(self._black_overlay)
        self._selector.setGeometry(QRect(-9, -9, 18, 18))
        self._selector.setMinimumSize(QSize(18, 18))
        self._selector.setMaximumSize(QSize(18, 18))
        self._selector.setStyleSheet('background-color:none; border: 3px solid #3F3844; border-radius: 9px;')
        self._selector.setFrameShape(QFrame.Shape.StyledPanel)
        self._selector.setFrameShadow(QFrame.Shadow.Raised)

        self._white_ring = QLabel(self._selector)
        self._white_ring.setGeometry(QRect(3, 3, 15, 15))
        self._white_ring.setMinimumSize(QSize(12, 12))
        self._white_ring.setMaximumSize(QSize(12, 12))
        self._white_ring.setBaseSize(QSize(12, 12))
        self._white_ring.setStyleSheet('background-color: none; border: 3px solid white; border-radius: 6px;')

        self.layout_.addWidget(self._color_view, 0, 0)
        self.layout_.addWidget(self._black_overlay, 0, 0)
        self.layout_.addWidget(self._color_view, 0, 0)

        self._black_overlay.mouseMoveEvent = self._move_sv_selector
        self._black_overlay.mousePressEvent = self._move_sv_selector

    def _create_color_slider(self) -> None:
        self._hue_frame = QFrame()
        self._hue_frame.setProperty('Rounded', True)
        self._hue_frame.setMinimumSize(QSize(30, 0))
        self._hue_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._hue_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_.addWidget(self._hue_frame, 0, 1)

        self._hue_bg = QFrame()
        self._hue_bg.setGeometry(QRect(0, 0, self._hue_frame.minimumWidth(), self._color_view.minimumHeight()))
        self._hue_bg.setFixedSize(QSize(self._hue_frame.minimumWidth(), self._color_view.minimumHeight()))
        self._hue_bg.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));')
        self._hue_bg.setProperty('Rounded', True)
        self._hue_bg.setProperty('Hue', True)
        self._hue_bg.setFrameShape(QFrame.Shape.StyledPanel)
        self._hue_bg.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_.addWidget(self._hue_bg, 0, 1)
        self.layout_.setAlignment(self._hue_bg, Qt.AlignmentFlag.AlignCenter)

        self._hue_selector = QFrame(self._hue_bg)
        self._hue_selector.setGeometry(QRect(-3, 0, 36, 9))
        self._hue_selector.setFixedSize(QSize(36, 9))
        self._hue_selector.setProperty('Rounded', True)
        self._hue_selector.setProperty('Hue', True)
        self._hue_selector.setStyleSheet('background-color: transparent; border: 3px solid #878787;')

        self._hue_bg.mouseMoveEvent = self._move_hue_selector
        self._hue_bg.mousePressEvent = self._move_hue_selector

    def _create_alpha_slider(self) -> None:
        self._alpha_frame = QFrame()
        self._alpha_frame.setProperty('Rounded', True)
        self._alpha_frame.setMinimumSize(QSize(30, 0))
        self._alpha_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._alpha_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_.addWidget(self._alpha_frame, 0, 2)

        self._alpha_bg = QFrame()
        self._alpha_bg.setGeometry(QRect(0, 0, self._alpha_frame.minimumWidth(), self._color_view.minimumHeight()))
        self._alpha_bg.setFixedSize(QSize(self._alpha_frame.minimumWidth(), self._color_view.minimumHeight()))
        self._alpha_bg.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));')
        self._alpha_bg.setProperty('Rounded', True)
        self._alpha_bg.setProperty('Hue', True)
        self._alpha_bg.setFrameShape(QFrame.Shape.StyledPanel)
        self._alpha_bg.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_.addWidget(self._alpha_bg, 0, 2)
        self.layout_.setAlignment(self._alpha_bg, Qt.AlignmentFlag.AlignCenter)

        self._alpha_selector = QFrame(self._alpha_bg)
        self._alpha_selector.setGeometry(QRect(-3, 0, 36, 9))
        self._alpha_selector.setFixedSize(QSize(36, 9))
        self._alpha_selector.setProperty('Rounded', True)
        self._alpha_selector.setProperty('Hue', True)
        self._alpha_selector.setStyleSheet('background-color: transparent; border: 3px solid #878787;')

        self._alpha_bg.mouseMoveEvent = self._move_alpha_selector
        self._alpha_bg.mousePressEvent = self._move_alpha_selector

    def _create_color_input(self) -> None:
        frame = QGridFrame()
        frame.setFixedWidth(int(self._color_view.minimumWidth() / 2.5))
        frame.setFixedHeight(self._color_view.minimumWidth())
        frame.layout_.setContentsMargins(0, 0, 0, 0)
        frame.layout_.setSpacing(0)
        frame.setProperty('Rounded', True)
        frame.setProperty('ColorInput', True)
        self.layout_.addWidget(frame, 0, 3)

        self._color_vis = QFrame()
        self._color_vis.setMinimumWidth(self._color_view.minimumWidth() // 6)
        self._color_vis.setFixedHeight(self._color_view.minimumHeight() // 6)
        frame.layout_.addWidget(self._color_vis, 0, 0)
        self._color_vis.setStyleSheet('background-color: #fff;')

        input_frame = QGridFrame()
        input_frame.layout_.setContentsMargins(10, 10, 10, 10)
        input_frame.layout_.setSpacing(20)
        input_frame.setProperty('Bottom', True)
        frame.layout_.addWidget(input_frame, 1, 0)
        input_frame.layout_.setRowStretch(3, 1)


        self._color_combobox = QComboBox()
        self._color_combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        self._color_combobox.view().setCursor(Qt.CursorShape.PointingHandCursor)
        self._color_combobox.addItems([
            'RGB',
            'HSV',
            'HSL',
            'CMYK',
            'Hex'
        ])
        input_frame.layout_.addWidget(self._color_combobox, 0, 0)


        input_frame_top = QGridFrame()
        input_frame_top.layout_.setContentsMargins(0, 0, 0, 0)
        input_frame_top.layout_.setSpacing(10)
        input_frame.layout_.addWidget(input_frame_top, 1, 0)
        input_frame.layout_.setAlignment(input_frame_top, Qt.AlignmentFlag.AlignTop)

        input_frame_bottom = QGridFrame()
        input_frame_bottom.layout_.setContentsMargins(0, 0, 0, 0)
        input_frame_bottom.layout_.setSpacing(5)
        input_frame.layout_.addWidget(input_frame_bottom, 2, 0)
        input_frame.layout_.setAlignment(input_frame_bottom, Qt.AlignmentFlag.AlignTop)

        label = QLabel('A')
        label.setFixedWidth(20)
        input_frame_bottom.layout_.addWidget(label, 0, 0)
        self._alpha_spinbox = QSpinBox()
        self._alpha_spinbox.setRange(0, 255)
        # self._alpha_spinbox.setValue(self._color.alpha)
        input_frame_bottom.layout_.addWidget(self._alpha_spinbox, 0, 1)


        self._rgb_frame = QGridFrame()
        self._rgb_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._rgb_frame.layout_.setSpacing(5)

        label = QLabel('R')
        label.setFixedWidth(20)
        self._rgb_frame.layout_.addWidget(label, 0, 0)
        self._rgb_red_spinbox = QSpinBox()
        self._rgb_red_spinbox.setRange(0, 255)
        # self._rgb_red_spinbox.setValue(self._color.red)
        self._rgb_frame.layout_.addWidget(self._rgb_red_spinbox, 0, 1)

        label = QLabel('G')
        label.setFixedWidth(20)
        self._rgb_frame.layout_.addWidget(label, 1, 0)
        self._rgb_green_spinbox = QSpinBox()
        self._rgb_green_spinbox.setRange(0, 255)
        # self._rgb_green_spinbox.setValue(self._color.green)
        self._rgb_frame.layout_.addWidget(self._rgb_green_spinbox, 1, 1)

        label = QLabel('B')
        label.setFixedWidth(20)
        self._rgb_frame.layout_.addWidget(label, 2, 0)
        self._rgb_blue_spinbox = QSpinBox()
        self._rgb_blue_spinbox.setRange(0, 255)
        # self._rgb_blue_spinbox.setValue(self._color.blue)
        self._rgb_frame.layout_.addWidget(self._rgb_blue_spinbox, 2, 1)

        self._rgb_frame.layout_.setRowStretch(3, 1)
        input_frame_top.layout_.addWidget(self._rgb_frame, 0, 0)


        self._hsv_frame = QGridFrame()
        self._hsv_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._hsv_frame.layout_.setSpacing(5)

        label = QLabel('H')
        label.setFixedWidth(20)
        self._hsv_frame.layout_.addWidget(label, 0, 0)
        self._hsv_hue_spinbox = QSpinBox()
        self._hsv_hue_spinbox.setRange(0, 360)
        # self._hsv_hue_spinbox.setValue(int(self._color.hue_hsv * 360))
        self._hsv_frame.layout_.addWidget(self._hsv_hue_spinbox, 0, 1)

        label = QLabel('S')
        label.setFixedWidth(20)
        self._hsv_frame.layout_.addWidget(label, 1, 0)
        self._hsv_saturation_spinbox = QDoubleSpinBox()
        self._hsv_saturation_spinbox.setRange(0.0, 100.0)
        # self._hsv_saturation_spinbox.setValue(self._color.saturation_hsv)
        self._hsv_frame.layout_.addWidget(self._hsv_saturation_spinbox, 1, 1)

        label = QLabel('V')
        label.setFixedWidth(20)
        self._hsv_frame.layout_.addWidget(label, 2, 0)
        self._hsv_value_spinbox = QDoubleSpinBox()
        self._hsv_value_spinbox.setRange(0.0, 100.0)
        # self._hsv_value_spinbox.setValue(self._color.value_hsv)
        self._hsv_frame.layout_.addWidget(self._hsv_value_spinbox, 2, 1)

        self._hsv_frame.layout_.setRowStretch(3, 1)
        input_frame_top.layout_.addWidget(self._hsv_frame, 0, 0)
        self._hsv_frame.setVisible(False)


        self._hsl_frame = QGridFrame()
        self._hsl_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._hsl_frame.layout_.setSpacing(5)

        label = QLabel('H')
        label.setFixedWidth(20)
        self._hsl_frame.layout_.addWidget(label, 0, 0)
        self._hsl_hue_spinbox = QSpinBox()
        self._hsl_hue_spinbox.setRange(0, 360)
        # self._hsl_hue_spinbox.setValue(int(self._color.hue_hsl))
        self._hsl_frame.layout_.addWidget(self._hsl_hue_spinbox, 0, 1)

        label = QLabel('S')
        label.setFixedWidth(20)
        self._hsl_frame.layout_.addWidget(label, 1, 0)
        self._hsl_saturation_spinbox = QDoubleSpinBox()
        self._hsl_saturation_spinbox.setRange(0.0, 100.0)
        # self._hsl_saturation_spinbox.setValue(self._color.saturation_hsl)
        self._hsl_frame.layout_.addWidget(self._hsl_saturation_spinbox, 1, 1)

        label = QLabel('L')
        label.setFixedWidth(20)
        self._hsl_frame.layout_.addWidget(label, 2, 0)
        self._hsl_lightness_spinbox = QDoubleSpinBox()
        self._hsl_lightness_spinbox.setRange(0.0, 100.0)
        # self._hsl_lightness_spinbox.setValue(self._color.lightness_hsl)
        self._hsl_frame.layout_.addWidget(self._hsl_lightness_spinbox, 2, 1)

        self._hsl_frame.layout_.setRowStretch(3, 1)
        input_frame_top.layout_.addWidget(self._hsl_frame, 0, 0)
        self._hsl_frame.setVisible(False)


        self._cmyk_frame = QGridFrame()
        self._cmyk_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._cmyk_frame.layout_.setSpacing(5)

        label = QLabel('C')
        label.setFixedWidth(20)
        self._cmyk_frame.layout_.addWidget(label, 0, 0)
        self._cmyk_cyan_spinbox = QDoubleSpinBox()
        self._cmyk_cyan_spinbox.setRange(0.0, 100.0)
        # self._cmyk_cyan_spinbox.setValue(self._color.cyan)
        self._cmyk_frame.layout_.addWidget(self._cmyk_cyan_spinbox, 0, 1)

        label = QLabel('M')
        label.setFixedWidth(20)
        self._cmyk_frame.layout_.addWidget(label, 1, 0)
        self._cmyk_magenta_spinbox = QDoubleSpinBox()
        self._cmyk_magenta_spinbox.setRange(0.0, 100.0)
        # self._cmyk_magenta_spinbox.setValue(self._color.magenta)
        self._cmyk_frame.layout_.addWidget(self._cmyk_magenta_spinbox, 1, 1)

        label = QLabel('Y')
        label.setFixedWidth(20)
        self._cmyk_frame.layout_.addWidget(label, 2, 0)
        self._cmyk_yellow_spinbox = QDoubleSpinBox()
        self._cmyk_yellow_spinbox.setRange(0.0, 100.0)
        # self._cmyk_yellow_spinbox.setValue(self._color.yellow)
        self._cmyk_frame.layout_.addWidget(self._cmyk_yellow_spinbox, 2, 1)

        label = QLabel('K')
        label.setFixedWidth(20)
        self._cmyk_frame.layout_.addWidget(label, 3, 0)
        self._cmyk_key_spinbox = QDoubleSpinBox()
        self._cmyk_key_spinbox.setRange(0.0, 100.0)
        # self._cmyk_key_spinbox.setValue(self._color.black)
        self._cmyk_frame.layout_.addWidget(self._cmyk_key_spinbox, 3, 1)

        self._cmyk_frame.layout_.setRowStretch(4, 1)
        input_frame_top.layout_.addWidget(self._cmyk_frame, 0, 0)
        self._cmyk_frame.setVisible(False)


        self._hex_frame = QGridFrame()
        self._hex_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._hex_frame.layout_.setSpacing(5)

        label = QLabel('#')
        label.setFixedWidth(20)
        self._hex_frame.layout_.addWidget(label, 0, 0)
        self._hex_line_edit = QLineEdit()
        # self._hex_line_edit.setText(self._color.hex.replace('#', ''))
        self._hex_frame.layout_.addWidget(self._hex_line_edit, 0, 1)

        self._hex_frame.layout_.setRowStretch(1, 1)
        input_frame_top.layout_.addWidget(self._hex_frame, 0, 0)
        self._hex_frame.setVisible(False)

        self._color_combobox.currentIndexChanged.connect(self._color_combobox_changed)

        self._rgb_red_spinbox.valueChanged.connect(lambda _: self._rgb_changed())
        self._rgb_green_spinbox.valueChanged.connect(lambda _: self._rgb_changed())
        self._rgb_blue_spinbox.valueChanged.connect(lambda _: self._rgb_changed())

        self._hsv_hue_spinbox.valueChanged.connect(lambda _: self._hsv_changed())
        self._hsv_saturation_spinbox.valueChanged.connect(lambda _: self._hsv_changed())
        self._hsv_value_spinbox.valueChanged.connect(lambda _: self._hsv_changed())

        self._hsl_hue_spinbox.valueChanged.connect(lambda _: self._hsl_changed())
        self._hsl_saturation_spinbox.valueChanged.connect(lambda _: self._hsl_changed())
        self._hsl_lightness_spinbox.valueChanged.connect(lambda _: self._hsl_changed())

        self._cmyk_cyan_spinbox.valueChanged.connect(lambda _: self._cmyk_changed())
        self._cmyk_magenta_spinbox.valueChanged.connect(lambda _: self._cmyk_changed())
        self._cmyk_yellow_spinbox.valueChanged.connect(lambda _: self._cmyk_changed())
        self._cmyk_key_spinbox.valueChanged.connect(lambda _: self._cmyk_changed())

        self._hex_line_edit.textChanged.connect(lambda _: self._hex_changed())

        self._alpha_spinbox.valueChanged.connect(lambda _: self._alpha_changed())


    def _color_combobox_changed(self, index: int):
        self._rgb_frame.setVisible(index == 0)
        self._hsv_frame.setVisible(index == 1)
        self._hsl_frame.setVisible(index == 2)
        self._cmyk_frame.setVisible(index == 3)
        self._hex_frame.setVisible(index == 4)


    def _move_sv_selector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > self._color_view.minimumWidth(): pos.setX(self._color_view.minimumWidth())
            if pos.y() > self._color_view.minimumHeight(): pos.setY(self._color_view.minimumHeight())
            self._selector.move(int(pos.x() - 9), int(pos.y() - 9))
            self._hsv_data_changed()

    def _move_hue_selector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - 3
            if pos < 0: pos = 0
            if pos > self._hue_bg.minimumHeight() - 9: pos = self._hue_bg.minimumHeight() - 9
            self._hue_selector.move(QPoint(-3, int(pos)))
            self._hsv_data_changed()

    def _move_alpha_selector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - 3
            if pos < 0: pos = 0
            if pos > self._alpha_bg.minimumHeight() - 9: pos = self._alpha_bg.minimumHeight() - 9
            self._alpha_selector.move(QPoint(-3, int(pos)))
            self._alpha_data_changed()


    def update(self):
        self._color_vis.setStyleSheet(f'background-color: qlineargradient(x1:1, x2:0, stop:0 {self._color.ahex}, stop:0.35 {self._color.ahex}, stop:1 {self._color.hex});')
        self._color_view.setStyleSheet(f'border-radius: 5px; background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({int(self._hue_color__.hue_hsl)}%,100%,50%), stop:1 #fff);')

    def _changed(self):
        self.color_changed.emit(self._color)
        self.update()

    def _hsv_data_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        h, s, v = 100 - (self._hue_selector.y() / (self._hue_bg.minimumHeight() - 9) * 100.0), (self._selector.x() + 9) / self._color_view.minimumWidth() * 100.0, ((self._color_view.minimumHeight() - 9) - self._selector.y()) / self._color_view.minimumHeight() * 100.0
        self._color.hsv = (h, s, v)
        self._hue_color__.hue_hsl = h
        self._changed()
        self._set_rgb()
        self._set_hsv()
        self._set_hsl()
        self._set_cmyk()
        self._set_hex()

        self._interaction_disabled = False

    def _set_hsv_data(self):
        h, s, v = self._color.hsv[0], self._color.hsv[1], self._color.hsv[2]
        self._hue_selector.move(QPoint(-3, int((100 - (h if h > 0 else 100)) / 100 * (self._hue_bg.minimumHeight() - 9))))
        self._selector.move(int((s / 100 * self._color_view.minimumWidth()) - 9), int(((100 - v) / 100 * self._color_view.minimumHeight()) - 9))
        self._hue_color__.hue_hsl = h


    def _alpha_data_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        a = 100 - (self._alpha_selector.y() / (self._alpha_bg.minimumHeight() - 9) * 100.0)
        self._color.alpha = round(a * 2.55)
        self._changed()
        self._set_alpha()

        self._interaction_disabled = False

    def _set_alpha_data(self):
        self._alpha_selector.move(QPoint(-3, int((self._alpha_bg.minimumHeight() - 9) - (self._alpha_bg.minimumHeight() - 9) * (self._color.alpha / 255.0))))

    def _rgb_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        r, g, b = self._rgb_red_spinbox.value(), self._rgb_green_spinbox.value(), self._rgb_blue_spinbox.value()
        self._color.rgb = (r, g, b)
        self._changed()
        self._set_hsv_data()
        self._set_hsv()
        self._set_hsl()
        self._set_cmyk()
        self._set_hex()

        self._interaction_disabled = False

    def _set_rgb(self):
        r, g, b = self._color.rgb
        self._rgb_red_spinbox.setValue(r)
        self._rgb_green_spinbox.setValue(g)
        self._rgb_blue_spinbox.setValue(b)

    def _hsv_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        h, s, v = self._hsv_hue_spinbox.value(), self._hsv_saturation_spinbox.value(), self._hsv_value_spinbox.value()
        self._color.hsv = (h, s, v)
        self._changed()
        self._set_hsv_data()
        self._set_rgb()
        self._set_hsl()
        self._set_cmyk()
        self._set_hex()

        self._interaction_disabled = False

    def _set_hsv(self):
        h, s, v = self._color.hsv
        self._hsv_hue_spinbox.setValue(int(h * 3.6))
        self._hsv_saturation_spinbox.setValue(s)
        self._hsv_value_spinbox.setValue(v)

    def _hsl_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        h, s, l = self._hsl_hue_spinbox.value(), self._hsl_saturation_spinbox.value(), self._hsl_lightness_spinbox.value()
        self._color.hsl = (h, s, l)
        self._changed()
        self._set_hsv_data()
        self._set_rgb()
        self._set_hsv()
        self._set_cmyk()
        self._set_hex()

        self._interaction_disabled = False

    def _set_hsl(self):
        h, s, l = self._color.hsl
        self._hsl_hue_spinbox.setValue(int(h))
        self._hsl_saturation_spinbox.setValue(s)
        self._hsl_lightness_spinbox.setValue(l)

    def _cmyk_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        c, m, y, k = self._cmyk_cyan_spinbox.value(), self._cmyk_magenta_spinbox.value(), self._cmyk_yellow_spinbox.value(), self._cmyk_black_spinbox.value()
        self._color.cmyk = (c, m, y, k)
        self._changed()
        self._set_hsv_data()
        self._set_rgb()
        self._set_hsv()
        self._set_hsl()
        self._set_hex()

        self._interaction_disabled = False

    def _set_cmyk(self):
        c, m, y, k = self._color.cmyk
        self._cmyk_cyan_spinbox.setValue(c)
        self._cmyk_magenta_spinbox.setValue(m)
        self._cmyk_yellow_spinbox.setValue(y)
        self._cmyk_key_spinbox.setValue(k)

    def _hex_changed(self):
        s = self._hex_line_edit.text()
        pos = self._hex_line_edit.cursorPosition()
        hex = ''
        for ss in s:
            if ss in '0123456789abcdefABCDEF':
                hex += ss
        if len(hex) < 6: hex = hex + '0' * (6 - len(hex)) #hex.zfill(6)
        if len(hex) > 6: hex = hex[:6]
        s = self._hex_line_edit.setText(hex)
        self._hex_line_edit.setCursorPosition(pos)

        if self._interaction_disabled: return
        self._interaction_disabled = True

        self._color.hex = f'#{hex}'
        self._changed()
        self._set_hsv_data()
        self._set_rgb()
        self._set_hsv()
        self._set_hsl()
        self._set_cmyk()

        self._interaction_disabled = False

    def _set_hex(self):
        hex = self._color.hex
        self._hex_line_edit.setText(hex.replace('#', ''))

    def _alpha_changed(self):
        if self._interaction_disabled: return
        self._interaction_disabled = True

        a = self._alpha_spinbox.value()
        self._color.alpha = a
        self._changed()
        self._set_alpha_data()

        self._interaction_disabled = False

    def _set_alpha(self):
        self._alpha_spinbox.setValue(self._color.alpha)

    @property
    def color(self):
        return QUtilsColor.from_rgba(self._color.rgba)

    @color.setter
    def color(self, color):
        self._interaction_disabled = True
        self._color = QUtilsColor.from_rgba(color.rgba)
        self._set_hsv_data()
        self._set_rgb()
        self._set_hsv()
        self._set_hsl()
        self._set_cmyk()
        self._set_hex()
        self._set_alpha()
        self._set_alpha_data()
        self._changed()
        self._interaction_disabled = False
#----------------------------------------------------------------------
