#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QTimer, Slot
from typing import Callable
#----------------------------------------------------------------------

    # Class
class DelayedSignal:
    def __init__(self, timeout_ms: int, func: Callable) -> None:
        self._timeout = timeout_ms
        self._func = func
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(timeout_ms)
        self._timer.timeout.connect(func)

    @property
    def timeout(self) -> int:
        return self._timeout
    
    @property
    def func(self) -> Callable:
        return self._func

    @Slot()
    def __call__(self):
        self._timer.stop()
        self._timer.start()
#----------------------------------------------------------------------
