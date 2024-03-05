#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import Signal, QPropertyAnimation, Qt, QEasingCurve, QPoint, QParallelAnimationGroup, QAbstractAnimation

from enum import Enum
from math import fmod
#----------------------------------------------------------------------

    # Class
class QSlidingStackedWidget(QStackedWidget):
    class Direction(Enum):
        Left2Right = 'left2right',
        Right2Left = 'right2left',
        Top2Bottom = 'top2bottom',
        Bottom2Top = 'bottom2top'
        Automatic = 'automatic'

    animation_finished = Signal()

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setProperty('transparent', True)

        self._orientation = Qt.Orientation.Horizontal
        self._speed = 300
        self._animation_type = QEasingCurve.Type.OutQuart
        self._now = 0
        self._next = 0
        self._wrap = False
        self._p_now = QPoint(0, 0)
        self._active = False
        self._has_opacity_effect = True
        self._next_index: tuple[int, QSlidingStackedWidget.Direction] = None # In case the user moved too fast, we need to make sure that the animation starts

    @property
    def orientation(self) -> Qt.Orientation:
        return self._orientation

    def set_orientation(self, orientation: Qt.Orientation) -> None:
        self._orientation = orientation

    @property
    def speed(self) -> int:
        return self._speed

    def set_speed(self, speed: int) -> None:
        self._speed = speed

    @property
    def animation(self) -> QEasingCurve.Type:
        return self._animation_type

    def set_animation(self, animation: QEasingCurve.Type) -> None:
        self._animation_type = animation

    @property
    def wrap(self) -> bool:
        return self._wrap

    def set_wrap(self, wrap: bool) -> None:
        self._wrap = wrap

    @property
    def has_opacity_effect(self) -> bool:
        return self._has_opacity_effect

    def set_has_opacity_effect(self, has_opacity_effect: bool) -> None:
        self._has_opacity_effect = has_opacity_effect

    @property
    def active(self) -> bool:
        return self._active

    @property
    def current_index(self) -> int:
        return self._next_index[0] if (self._next_index is not None) else self._next

    def slide_loop_next(self, direction: Direction = Direction.Automatic) -> None:
        result = self.slide_in_next()
        if (not result): self.slide_in_index(0, direction)

    def slide_loop_previous(self, direction: Direction = Direction.Automatic) -> None:
        result = self.slide_in_previous()
        if (not result): self.slide_in_index(self.count() - 1, direction)

    def slide_in_next(self) -> bool:
        now = self.currentIndex()
        if (self._wrap or (now < self.count() - 1)): self.slide_in_index(now + 1)
        else: return False
        return True

    def slide_in_previous(self) -> bool:
        now = self.currentIndex()
        if (self._wrap or (now > 0)): self.slide_in_index(now - 1)
        else: return False
        return True

    def slide_in_index(self, index: int, direction: Direction = Direction.Automatic) -> None:
        if (index > self.count() - 1):
            if direction == QSlidingStackedWidget.Direction.Automatic: direction = QSlidingStackedWidget.Direction.Top2Bottom if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Right2Left
            index = int(fmod((index), self.count()))

        elif (index < 0):
            if direction == QSlidingStackedWidget.Direction.Automatic: direction = QSlidingStackedWidget.Direction.Bottom2Top if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Left2Right
            index = fmod((index + self.count()), self.count())

        if self._active:
            self._next_index = (index, direction)
            return

        self._slide_in_widget(self.widget(index), direction)

    def _slide_in_widget(self, newwidget: QWidget, direction: Direction) -> None:
        if (self._active): return
        else: self._active = True

        direction_hint = None
        now = self.currentIndex()
        next = self.indexOf(newwidget)

        if (now == next):
            self._active = False
            return

        elif (now < next):
            direction_hint = QSlidingStackedWidget.Direction.Top2Bottom if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Right2Left

        else:
            direction_hint = QSlidingStackedWidget.Direction.Bottom2Top if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Left2Right

        if (direction == QSlidingStackedWidget.Direction.Automatic):
            direction = direction_hint

        offset_x = self.frameRect().width()
        offset_y = self.frameRect().height()


        self.widget(next).setGeometry(0, 0, offset_x, offset_y)
        if (direction == QSlidingStackedWidget.Direction.Bottom2Top):
            offset_x = 0
            offset_y = -offset_y

        elif (direction == QSlidingStackedWidget.Direction.Top2Bottom):
                offset_x = 0

        elif (direction == QSlidingStackedWidget.Direction.Right2Left):
            offset_x = -offset_x
            offset_y = 0

        elif (direction == QSlidingStackedWidget.Direction.Left2Right):
            offset_y = 0

        p_next = self.widget(next).pos()
        p_now = self.widget(now).pos()
        self._p_now = p_now
        self.widget(next).move(p_next.x() - offset_x,p_next.y() - offset_y)

        self.widget(next).show()
        self.widget(next).raise_()

        anim_now = QPropertyAnimation(self.widget(now), b'pos')
        anim_now.setDuration(self._speed)
        anim_now.setEasingCurve(self._animation_type)
        anim_now.setStartValue(QPoint(p_now.x(), p_now.y()))
        anim_now.setEndValue(QPoint(offset_x + p_now.x(), offset_y + p_now.y()))

        anim_now_op_eff = QGraphicsOpacityEffect()
        self.widget(now).setGraphicsEffect(anim_now_op_eff)
        anim_now_op = QPropertyAnimation(anim_now_op_eff, b'opacity')
        anim_now_op.setDuration(self._speed // 2)
        anim_now_op.setStartValue(1)
        anim_now_op.setEndValue(0 if (self._has_opacity_effect) else 1)

        def finished(effect: QGraphicsOpacityEffect):
            if (effect != None):
                effect.deleteLater()

        anim_now_op.finished.connect(lambda: finished(anim_now_op_eff))

        anim_next_op_eff = QGraphicsOpacityEffect()
        anim_next_op_eff.setOpacity(0)
        self.widget(next).setGraphicsEffect(anim_next_op_eff)
        anim_next_op = QPropertyAnimation(anim_next_op_eff, b'opacity')
        anim_next_op.setDuration(self._speed // 2)
        anim_next_op.setStartValue(0 if (self._has_opacity_effect) else 1)
        anim_next_op.setEndValue(1)
        anim_next_op.finished.connect(lambda: finished(anim_next_op_eff))

        anim_next = QPropertyAnimation(self.widget(next), b'pos')
        anim_next.setDuration(self._speed)
        anim_next.setEasingCurve(self._animation_type)
        anim_next.setStartValue(QPoint(-offset_x + p_next.x(), offset_y + p_next.y()))
        anim_next.setEndValue(QPoint(p_next.x(), p_next.y()))

        self._anim_group = QParallelAnimationGroup()
        self._anim_group.addAnimation(anim_now)
        self._anim_group.addAnimation(anim_next)
        self._anim_group.addAnimation(anim_now_op)
        self._anim_group.addAnimation(anim_next_op)

        self._anim_group.finished.connect(self._animation_done_slot)
        self._next = next
        self._now = now
        self._active = True
        self._anim_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _animation_done_slot(self) -> None:
        super().setCurrentIndex(self._next)
        self.widget(self._now).hide()
        self.widget(self._now).move(self._p_now)
        self._active = False
        self.animation_finished.emit()
        
        if self._next_index is not None:
            self.slide_in_index(self._next_index[0], self._next_index[1])
            self._next_index = None

    def setCurrentIndex(self, index: int) -> None:
        self._next = index
        self._next_index = None
        self._animation_done_slot()
        self._now = index

    def set_current_index(self, index: int) -> None:
        self.setCurrentIndex(index)
#----------------------------------------------------------------------
