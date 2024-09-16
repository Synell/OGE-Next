#----------------------------------------------------------------------

    # Librairies
from enum import StrEnum
#----------------------------------------------------------------------

    # Class
class QTerminalElementModifier:
    class Behaviour(StrEnum):
        AddInner = 'add-inner'
        AddOuter = 'add-outer'
        ReplaceInner = 'replace-inner'
        ReplaceOuter = 'replace-outer'


    def __init__(self, selector: str, index: int, html: str, behaviour: Behaviour = Behaviour.AddInner) -> None:
        self._selector = selector
        self._index = index
        self._html = html
        self._behaviour = behaviour


    @property
    def selector(self) -> str:
        return self._selector


    @property
    def index(self) -> int:
        return self._index


    @property
    def html(self) -> str:
        return self._html
    

    @property
    def behaviour(self) -> Behaviour:
        return self._behaviour
#----------------------------------------------------------------------
