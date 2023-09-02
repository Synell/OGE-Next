#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, QSize, QPoint, QPointF, QRectF, QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup, Slot, Property
from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from . import QBaseApplication
from .QssSelector import QssSelector
#----------------------------------------------------------------------

    # Class
class QToggleButton(QCheckBox):
    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    _checked_color = '#0466C7'
    _checked_disabled_color = '#0466C7'

    _checked_color_handle = '#FBFEFB'
    _checked_disabled_color_handle = '#FBFEFB'

    _normal_color = '#44999999'
    _normal_disabled_color = '#44999999'

    _normal_color_handle = '#5D5D5D'
    _normal_disabled_color_handle = '#5D5D5D'

    @staticmethod
    def init(app: QBaseApplication) -> None:
        QToggleButton._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox')
        )['color']
        QToggleButton._normal_disabled_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['disabled'])
        )['color']

        QToggleButton._normal_color_handle = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', items = ['handle'])
        )['color']
        QToggleButton._normal_disabled_color_handle = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['disabled'], items = ['handle'])
        )['color']

        QToggleButton._checked_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'])
        )['color']
        QToggleButton._checked_disabled_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked', 'disabled'])
        )['color']

        QToggleButton._checked_color_handle = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'], items = ['handle'])
        )['color']
        QToggleButton._checked_disabled_color_handle = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked', 'disabled'], items = ['handle'])
        )['color']

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty('QToggleButton', True)

        self.setFixedWidth(58)
        self.setFixedHeight(45)

        self._bar_brush = QBrush(QColor(self._normal_color))
        self._bar_disabled_brush = QBrush(QColor(self._normal_disabled_color))

        self._bar_checked_brush = QBrush(QColor(self._checked_color))
        self._bar_checked_disabled_brush = QBrush(QColor(self._checked_disabled_color))

        self._handle_brush = QBrush(QColor(self._normal_color_handle))
        self._handle_disabled_brush = QBrush(QColor(self._normal_disabled_color_handle))

        self._handle_checked_brush = QBrush(QColor(self._checked_color_handle))
        self._handle_checked_disabled_brush = QBrush(QColor(self._checked_disabled_color_handle))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.animation = QPropertyAnimation(self, b'handle_position', self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)


        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        cont_rect = self.contentsRect()
        handle_radius = round(0.12 * cont_rect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        bar_rect = QRectF(
            0, 0,
            cont_rect.width() - handle_radius, 0.40 * cont_rect.height()
        )
        bar_rect.moveCenter(QPointF(cont_rect.center()))
        rounding = bar_rect.height() / 2

        trail_length = cont_rect.width() - 4.5 * handle_radius

        x_pos = cont_rect.x() + handle_radius * 2 + trail_length * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush if self.isEnabled() else self._bar_checked_disabled_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setBrush(self._handle_checked_brush if self.isEnabled() else self._handle_checked_disabled_brush)

        else:
            p.setBrush(self._bar_brush if self.isEnabled() else self._bar_disabled_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush if self.isEnabled() else self._handle_disabled_brush)

        p.drawEllipse(
            QPointF(x_pos, bar_rect.center().y()),
            handle_radius,
            handle_radius
        )

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()
#----------------------------------------------------------------------
