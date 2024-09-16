#----------------------------------------------------------------------

    # Librairies
from .QTerminalAction import QTerminalAction
#----------------------------------------------------------------------

    # Class
class QTerminalUnknownAction(QTerminalAction):
    def __init__(self, action: str, *arguments: object) -> None:
        super().__init__()
        self._action = action
        self._arguments = arguments


    @property
    def action(self) -> str:
        return self._action


    @property
    def arguments(self) -> tuple[object]:
        return self._arguments


    def exec(self) -> None:
        raise ValueError(f'Unknown action: {self._action}')
#----------------------------------------------------------------------
