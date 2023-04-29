#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
from data.lib.oge import OGE, Semester, InfoType
import json, os
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    info_changed = Signal(InfoType, str)
    failed = Signal(Exception)
    finished = Signal(Semester)

class OGEWorker(QThread):
    CACHE_FILE = './data/oge_cache/%s.json'

    def __init__(self, parent: QObject = None, username: str = None, password: str = None) -> None:
        super(OGEWorker, self).__init__(parent)
        self.signals = __WorkerSignals__()

        self._username = username
        self._force = False
        self._oge = OGE(username, password)

        json_data: dict = self._load_data()

        if json_data:
            self._oge.set_data_from_json(json_data)

        self._semester = max(self._oge.semester_count, 1)

        self._oge.info_changed.connect(self.signals.info_changed.emit)
        self._oge.failed.connect(self.signals.failed.emit)

    def run(self) -> None:
        data = self._oge.get_semestre_data(self._semester, self._force)
        if data: self.signals.finished.emit(data)

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

    def _load_data(self) -> dict:
        try:
            with open(self.CACHE_FILE.replace('%s', self._username), 'r', encoding = 'utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self) -> None:
        if not self._oge.semester_count: return

        data = self._oge.get_data_as_json()

        file = self.CACHE_FILE.replace('%s', self._username)
        dir_ = os.path.dirname(file)

        if not os.path.exists(dir_):
            os.mkdir(dir_)

        with open(file, 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False)
#----------------------------------------------------------------------
