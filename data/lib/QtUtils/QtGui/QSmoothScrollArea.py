#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QScrollArea, QWidget, QApplication, QScroller, QScrollerProperties, QAbstractItemView
from PySide6.QtCore import QTimer, Qt, QDateTime, QPoint, QEasingCurve
from PySide6.QtGui import QWheelEvent
from enum import Enum
from math import cos, pi
#----------------------------------------------------------------------

    # Class
class QSmoothScrollArea(QScrollArea):
    class SmoothMode(Enum):
        NoSmooth = 0
        Constant = 1
        Linear = 2
        Quadratic = 3
        Cosine = 4

    def __init__(self, parent: QWidget = None) -> None: # TODO: Fix speed inconsistencies due to widget size
        super().__init__(parent)

        # QScroller.scroller(self.viewport()).grabGesture(self.viewport(), QScroller.ScrollerGestureType.TouchGesture)
        QScroller.grabGesture(self, QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        prop: QScrollerProperties = QScroller.scroller(self.viewport()).scrollerProperties()
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.AxisLockThreshold, 0.66)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.ScrollingCurve, QEasingCurve(QEasingCurve.Type.OutExpo))
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, 0.05)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, 0.635)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.OvershootDragResistanceFactor, 0.33)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.OvershootScrollDistanceFactor, 0.33)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.SnapPositionRatio, 0.93)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.DragStartDistance, 0.001)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.VerticalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
        prop.setScrollMetric(QScrollerProperties.ScrollMetric.HorizontalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
        QScroller.scroller(self.viewport()).setScrollerProperties(prop)


        self._last_wheel_event = None
        self._smooth_move_timer = QTimer(self)
        self._smooth_move_timer.timeout.connect(self._slot_smooth_move)

        self._fps = 1000
        self._duration = 70
        self._smooth_mode = QSmoothScrollArea.SmoothMode.Cosine
        self._acceleration = 2.5

        # self._small_step_modifier = Qt.KeyboardModifier.ShiftModifier
        # self._small_step_ratio = 1.0 / 5.0
        # self._big_step_modifier = Qt.KeyboardModifier.AltModifier
        # self._big_step_ratio = 5.0

        self._steps_total = 0
        self._steps_left_queue = []

    def smooth_mode(self) -> SmoothMode:
        return self._smooth_mode

    def set_smooth_mode(self, mode: SmoothMode) -> None:
        self._smooth_mode = mode

    def fps(self) -> int:
        return self._fps

    def set_fps(self, fps: int) -> None:
        self._fps = fps

    def duration(self) -> int:
        return self._duration

    def set_duration(self, ms: int) -> None:
        self._duration = ms

    def acceleration(self) -> float:
        return self._acceleration

    def set_acceleration(self, acceleration: float) -> None:
        self._acceleration = acceleration

    # def small_step_ratio(self) -> float:
    #     return self._small_step_ratio

    # def set_small_step_ratio(self, small_step_ratio: float) -> None:
    #     self._small_step_ratio = small_step_ratio

    # def big_step_ratio(self) -> float:
    #     return self._big_step_ratio

    # def set_big_step_ratio(self, big_step_ratio: float) -> None:
    #     self._big_step_ratio = big_step_ratio

    # def small_step_modifier(self) -> Qt.KeyboardModifier:
    #     return self._small_step_modifier

    # def set_small_step_modifier(self, small_step_modifier: Qt.KeyboardModifier) -> None:
    #     self._small_step_modifier = small_step_modifier

    # def big_step_modifier(self) -> Qt.KeyboardModifier:
    #     return self._big_step_modifier

    # def set_big_step_modifier(self, big_step_modifier: Qt.KeyboardModifier) -> None:
    #     self._big_step_modifier = big_step_modifier


    def _wheel_event_orientation(self, e: QWheelEvent) -> Qt.Orientation:
        return Qt.Orientation.Horizontal if abs(e.angleDelta().x()) > abs(e.angleDelta().y()) else Qt.Orientation.Vertical


    def wheelEvent(self, e: QWheelEvent) -> None:
        if (self._smooth_mode == QSmoothScrollArea.SmoothMode.NoSmooth):
            return super().wheelEvent(e)

        scroll_stamps = []
        now = QDateTime.currentDateTime().toMSecsSinceEpoch()
        scroll_stamps.append(now)
        while (now - scroll_stamps[0] > 500):
            scroll_stamps.pop(0)
        acceration_ratio = min(len(scroll_stamps) / 15.0, 1.0)

        # Duplicate wheel event to avoid a bug with the QScrollArea
        self._last_wheel_event = QWheelEvent(e.position(), e.globalPosition(), e.pixelDelta(), e.angleDelta(), e.buttons(), e.modifiers(), e.phase(), e.inverted())

        self._steps_total = self._fps * self._duration / 1000
        multiplier = 1.0
        # if (QApplication.keyboardModifiers() == self._small_step_modifier):
        #     multiplier *= self._small_step_ratio
        # if (QApplication.keyboardModifiers() == self._big_step_modifier):
        #     multiplier *= self._big_step_ratio
        delta = (e.angleDelta().x() if self._wheel_event_orientation(e) == Qt.Orientation.Horizontal else e.angleDelta().y()) * multiplier
        if (self.acceleration() > 0):
            delta += delta * self.acceleration() * acceration_ratio

        self._steps_left_queue.insert(0, [delta, self._steps_total])
        self._smooth_move_timer.start(int(1000 / self._fps))


    def _slot_smooth_move(self) -> None:
        total_delta = 0

        for i in range(len(self._steps_left_queue)):
            delta, steps_left = self._steps_left_queue[i]

            total_delta += self._sub_delta(delta, steps_left)
            if steps_left > 0: self._steps_left_queue[i][1] -= 1

        while (self._steps_left_queue[0][1] == 0 if self._steps_left_queue else False):
            self._steps_left_queue.pop(0)

        orientation = self._wheel_event_orientation(self._last_wheel_event)

        # if (self._big_step_modifier == Qt.KeyboardModifier.ALT) or (self._small_step_modifier == Qt.KeyboardModifier.ALT):
        #     orientation = Qt.Orientation.Vertical

        e = QWheelEvent(
            self._last_wheel_event.position(),
            self._last_wheel_event.globalPosition(),
            self._last_wheel_event.pixelDelta(),
            QPoint(0, round(total_delta)) if orientation == Qt.Orientation.Vertical else QPoint(round(total_delta), 0),
            self._last_wheel_event.buttons(),
            self._last_wheel_event.modifiers(),
            self._last_wheel_event.phase(),
            self._last_wheel_event.inverted()
        )
        if (self._wheel_event_orientation(e) == Qt.Orientation.Horizontal):
            QApplication.sendEvent(self.horizontalScrollBar(), e)
        else:
            QApplication.sendEvent(self.verticalScrollBar(), e)

        if (not self._steps_left_queue):
            self._smooth_move_timer.stop()


    def _sub_delta(self, delta: float, steps_left: int) -> float:
        assert (self._smooth_mode != QSmoothScrollArea.SmoothMode.NoSmooth)

        m = self._steps_total / 2.0
        x = abs(self._steps_total - steps_left - m)

        match (self._smooth_mode):
            case QSmoothScrollArea.SmoothMode.NoSmooth:
                return 0

            case QSmoothScrollArea.SmoothMode.Constant:
                return float(delta) / self._steps_total

            case QSmoothScrollArea.SmoothMode.Linear:
                return 2.0 * delta / self._steps_total * (m - x) / m

            case QSmoothScrollArea.SmoothMode.Quadratic:
                return 3.0 / 4.0 / m * (1.0 - x * x / m / m) * delta

            case QSmoothScrollArea.SmoothMode.Cosine:
                return (cos(x * pi / m) + 1.0) / (2.0 * m) * delta

        return 0.0
#----------------------------------------------------------------------
