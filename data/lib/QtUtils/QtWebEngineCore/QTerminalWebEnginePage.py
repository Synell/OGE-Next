#----------------------------------------------------------------------

    # Librairies
from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineNewWindowRequest, QWebEngineSettings
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal

from ..QtCore import QTerminalElementModifier
#----------------------------------------------------------------------

    # Class
class QTerminalWebEnginePage(QWebEnginePage):
    action_triggered = Signal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._first_load = True

        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)


    def acceptNavigationRequest(self, url: QUrl | str, type: QWebEnginePage.NavigationType, is_main_frame: bool) -> bool:
        if self._first_load: return super().acceptNavigationRequest(url, type, is_main_frame)
        return False


    def acceptAsNewWindow(self, request: QWebEngineNewWindowRequest) -> None:
        pass


    def javaScriptConsoleMessage(self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, message: str, line_number: int, source_id: str) -> None:
        if message.startswith('buttonClicked:'):
            action = ':'.join(message.split(':')[1:])
            self.action_triggered.emit(action)
            return

        return super().javaScriptConsoleMessage(level, message, line_number, source_id)


    def modify_html(self, modifier: QTerminalElementModifier) -> None:
        self.runJavaScript((
            f'modifyHTML({modifier.selector.__repr__()}, {modifier.index}, {modifier.html.__repr__()}, {modifier.behaviour.value.__repr__()});'
        ).replace('\n', ''))
#----------------------------------------------------------------------
