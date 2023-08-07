#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGridLayout

from .QGridWidget import QGridWidget
from .QSubMainWindow import QSubMainWindow
from .QBaseApplication import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QSubGridMainWindow(QSubMainWindow):
    def __init__(self, app: QBaseApplication, *args, **kwargs) -> None:
        super().__init__(app, *args, **kwargs)

        self._root = QGridWidget()
        self.setCentralWidget(self._root)

    @property
    def root(self) -> QGridWidget:
        return self._root

    @property
    def grid_layout(self) -> QGridLayout:
        return self._root.grid_layout
#----------------------------------------------------------------------
