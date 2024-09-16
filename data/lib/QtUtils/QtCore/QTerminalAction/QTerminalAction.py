#----------------------------------------------------------------------

    # Librairies
from data.lib.utils.AbstractTypeFactory import AbstractTypeFactory
#----------------------------------------------------------------------

    # Class
class QTerminalAction:
    action: str


    def __init__(self) -> None:
        pass


    def exec(self) -> None:
        raise NotImplementedError()
#----------------------------------------------------------------------
