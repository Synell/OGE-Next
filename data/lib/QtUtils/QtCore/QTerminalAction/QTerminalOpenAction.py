#----------------------------------------------------------------------

    # Librairies
from .QTerminalAction import QTerminalAction
from .QTerminalActionFabric import QTerminalActionFabric
import os, platform
#----------------------------------------------------------------------

    # Class
class QTerminalOpenAction(QTerminalAction):
    action = 'open'


    def __init__(self, file: str) -> None:
        super().__init__()
        self._file = str(file)


    def exec(self) -> None:
        match platform.system():
            case 'Windows': # Windows
                os.startfile(self._file)

            case 'Linux': # Linux
                os.system(f'xdg-open "{self._file}"')

            case 'Darwin': # MacOS
                os.system(f'open "{self._file}"')

            case _:
                raise Exception('Unknown platform')
#----------------------------------------------------------------------

    # Register
QTerminalActionFabric.register(QTerminalOpenAction.action, QTerminalOpenAction)
#----------------------------------------------------------------------
