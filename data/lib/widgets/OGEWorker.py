#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
from data.lib.oge import OGE, InfoType
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    info_changed = Signal(InfoType, str)
    failed = Signal(Exception)
    finished = Signal(list, int)

class OGEWorker(QThread):
    def __init__(self, parent: QObject = None, username: str = None, password: str = None) -> None:
        super(OGEWorker, self).__init__(parent)
        self.signals = __WorkerSignals__()
        self._semester = 1
        self._force = False
        self._oge = OGE(username, password)
        self._oge.info_changed.connect(self.signals.info_changed.emit)
        self._oge.failed.connect(self.signals.failed.emit)

    def run(self) -> None:
        data = self._oge.get_semestre_data(self._semester, self._force)
        if data: self.signals.finished.emit(data, self._semester)

    @property
    def semester(self) -> int:
        return self._semester

    @semester.setter
    def semester(self, value: int) -> None:
        self._semester = value

    @property
    def semester_count(self) -> int:
        return self._oge.semester_count

    @property
    def force(self) -> bool:
        return self._force
    
    @force.setter
    def force(self, value: bool) -> None:
        self._force = value
#----------------------------------------------------------------------
