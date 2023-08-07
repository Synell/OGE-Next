#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGridLayout

from .QScrollableGridWidget import QScrollableGridWidget
from .QSubMainWindow import QSubMainWindow
from .QBaseApplication import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QSubScrollableGridMainWindow(QSubMainWindow):
    def __init__(self, app: QBaseApplication, *args, **kwargs) -> None:
        super().__init__(app, *args, **kwargs)

        self._root = QScrollableGridWidget()
        self.setCentralWidget(self._root)

    @property
    def root(self) -> QScrollableGridWidget:
        return self._root

    @property
    def scroll_layout(self) -> QGridLayout:
        return self._root.scroll_layout
#----------------------------------------------------------------------
