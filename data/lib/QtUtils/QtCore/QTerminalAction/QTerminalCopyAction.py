#----------------------------------------------------------------------

    # Librairies
from .QTerminalAction import QTerminalAction
from .QTerminalActionFabric import QTerminalActionFabric
import pyperclip
#----------------------------------------------------------------------

    # Class
class QTerminalCopyAction(QTerminalAction):
    action = 'copy'


    def __init__(self, string: str) -> None:
        super().__init__()
        self._string = str(string)


    def exec(self) -> None:
        pyperclip.copy(self._string)
#----------------------------------------------------------------------

    # Register
QTerminalActionFabric.register(QTerminalCopyAction.action, QTerminalCopyAction)
#----------------------------------------------------------------------
