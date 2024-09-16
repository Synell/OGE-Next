#----------------------------------------------------------------------

    # Librairies
from .QTerminalAction import QTerminalAction
from .QTerminalActionFabric import QTerminalActionFabric
import webbrowser
#----------------------------------------------------------------------

    # Class
class QTerminalHrefAction(QTerminalAction):
    action = 'href'


    def __init__(self, url: str) -> None:
        super().__init__()
        self._url = str(url)


    def exec(self) -> None:
        webbrowser.open(self._url)
#----------------------------------------------------------------------

    # Register
QTerminalActionFabric.register(QTerminalHrefAction.action, QTerminalHrefAction)
#----------------------------------------------------------------------
