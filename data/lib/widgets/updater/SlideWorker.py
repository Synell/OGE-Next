#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
from data.lib.qtUtils import QSlidingStackedWidget
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        slide_changed = Signal()

class SlideWorker(QThread):
    def __init__(self):
        super(SlideWorker, self).__init__()
        self.signals = __WorkerSignals__()

    def run(self):
        while True:
            self.sleep(10)
            self.signals.slide_changed.emit()
#----------------------------------------------------------------------
