#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QMainWindow
from .QBaseApplication import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QSubMainWindow(QMainWindow):
    def __init__(self, app: QBaseApplication, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._app = app

        self.setProperty('color', self._app.window.property('color'))
#----------------------------------------------------------------------
