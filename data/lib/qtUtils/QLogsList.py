#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Qt
from .QBetterListWidget import QBetterListWidget
from .QBaseApplication import QBaseApplication
from .QSaveData import QSaveData
from .QLangDataManager import QLangData
#----------------------------------------------------------------------

    # Class
class QLogsList(QBetterListWidget):
    _lang: QLangData = QLangData.NoTranslation()

    _info_icon = None
    _warning_icon = None
    _error_icon = None
    _success_icon = None


    def init(app: QBaseApplication) -> None:
        QLogsList._lang = app.get_lang_data('QMainWindow.QLogsList')

        QLogsList._info_icon = app.get_icon('logslist/info.png', True, QSaveData.IconMode.Global)
        QLogsList._warning_icon = app.get_icon('logslist/warning.png', True, QSaveData.IconMode.Global)
        QLogsList._error_icon = app.get_icon('logslist/error.png', True, QSaveData.IconMode.Global)
        QLogsList._success_icon = app.get_icon('logslist/success.png', True, QSaveData.IconMode.Global)


    def __init__(self) -> None:
        super().__init__([self._lang.get('messages')])


    def add_info(self, message: str) -> None:
        return super().add_item([message], self._info_icon, Qt.AlignmentFlag.AlignLeft)


    def add_warning(self, message: str) -> None:
        return super().add_item([message], self._warning_icon, Qt.AlignmentFlag.AlignLeft)


    def add_error(self, message: str) -> None:
        return super().add_item([message], self._error_icon, Qt.AlignmentFlag.AlignLeft)


    def add_success(self, message: str) -> None:
        return super().add_item([message], self._success_icon, Qt.AlignmentFlag.AlignLeft)
#----------------------------------------------------------------------
