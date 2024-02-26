#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QSharedMemory # Doesn't work with PySide6 for some reason
#----------------------------------------------------------------------

    # Class
class QMemoryCondition:
    def __init__(self, key: str = 'memory_condition_key') -> None:
        self._shm = QSharedMemory(key)

        if not self._shm.attach():
            if not self._shm.create(1):
                raise RuntimeError('error creating shared memory: %s' % self._shm.errorString())

        self._condition = False

    def __enter__(self) -> bool:
        self._shm.lock()

        if self._shm.data()[0] == b'\x00':
            self._condition = True
            self._shm.data()[0] = b'\x01'

        self._shm.unlock()

        return self._condition

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._condition:
            self._shm.lock()
            self._shm.data()[0] = b'\x00'
            self._shm.unlock()
#----------------------------------------------------------------------
