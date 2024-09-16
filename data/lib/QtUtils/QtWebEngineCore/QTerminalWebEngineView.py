#----------------------------------------------------------------------

    # Librairies
from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Signal
from typing import Callable
import pyperclip

from ..QtCore import QTerminalModel, QEnumColor
from .QTerminalWebEnginePage import QTerminalWebEnginePage
#----------------------------------------------------------------------

    # Class
class QTerminalWebEngineView(QWebEngineView):
    action_triggered = Signal(object)


    def __init__(self, parent: QWidget = None, model: QTerminalModel = None) -> None:
        super().__init__(parent)
        self._model = model

        self._page = QTerminalWebEnginePage(self)
        self._page.action_triggered.connect(self._convert_action)
        super().setPage(self._page)

        self.update_html()


    @property
    def model(self) -> QTerminalModel:
        return self._model


    @property
    def html(self) -> str:
        return self._model.render()


    def _log_raw(self, func: Callable, text: str, *log_types: QEnumColor, continuous: bool = False) -> None:
        self._page.modify_html(
            func(text, *log_types, continuous = continuous)
        )

    def log_empty(self) -> None:
        self._log_raw(self._model.log_empty, '')


    def log(self, text: str, *log_types: QEnumColor, continuous: bool = False) -> None:
        self._log_raw(self._model.log, text, *log_types, continuous = continuous)


    def _convert_action(self, action: str) -> None:
        self.action_triggered.emit(self._model.convert_to_action(action))


    def update_html(self) -> None:
        self._page.setHtml(self.html)


    def clear(self) -> None:
        self._model.clear()
        self.update_html()


    def setPage(self) -> None:
        raise SyntaxError('Cannot override QTerminalWebEngineView.setPage()')


    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)
        action = menu.addAction('Copy')
        action.triggered.connect(self._copy_selection)
        action.setDisabled(not self._page.hasSelection())

        menu.popup(event.globalPos())

    def _copy_selection(self) -> None:
        pyperclip.copy(self._page.selectedText())
#----------------------------------------------------------------------
