#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt, QSize, QPoint, QPointF, QRectF, QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup, Slot, Property
from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
#----------------------------------------------------------------------

    # Class
class QToggleButton(QCheckBox):
    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    checked_color = '#0466C7'
    checked_color_handle = '#FBFEFB'
    normal_color = '#44999999'
    normal_color_handle = '#5D5D5D'

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty('QToggleButton', True)

        self.setFixedWidth(58)
        self.setFixedHeight(45)

        self._bar_brush = QBrush(QColor(self.normal_color))
        self._bar_checked_brush = QBrush(QColor(self.checked_color))

        self._handle_brush = QBrush(QColor(self.normal_color_handle))
        self._handle_checked_brush = QBrush(QColor(self.checked_color_handle))

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

        contRect = self.contentsRect()
        handleRadius = round(0.12 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(QPointF(contRect.center()))
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 4.5 * handleRadius

        xPos = contRect.x() + handleRadius * 2 + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()
#----------------------------------------------------------------------
