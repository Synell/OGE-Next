#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QProgressBar, QWidget
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
#----------------------------------------------------------------------

    # Class
class QAnimatedProgressBar(QProgressBar):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._value = 0
        self._duration = 300
        self._easing_curve = QEasingCurve.Type.InOutCirc
        self._anim = QPropertyAnimation(self, b'value')

    def setValue(self, val: int, animate: bool = True) -> None:
        self._value = val

        if (animate):
            self._anim.stop()
            self._anim.setDuration(self._duration)
            self._anim.setEasingCurve(self._easing_curve)
            self._anim.setStartValue(super().value())
            self._anim.setEndValue(val)
            self._anim.start()

        else:
            super().setValue(val)

    def value(self) -> int:
        return self._value

    def easing_curve(self) -> QEasingCurve.Type:
        return self._easing_curve

    def set_easing_curve(self, easing_curve: QEasingCurve.Type) -> None:
        self._easing_curve = easing_curve

    def duration(self) -> int:
        return self._duration

    def set_duration(self, duration: int) -> None:
        self._duration = duration
#----------------------------------------------------------------------
