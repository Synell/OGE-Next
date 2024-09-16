#----------------------------------------------------------------------

    # Librairies
from data.lib.utils.AbstractTypeFactory import AbstractTypeFactory
from contextlib import suppress

from .QTerminalAction import QTerminalAction
from .QTerminalUnknownAction import QTerminalUnknownAction
#----------------------------------------------------------------------

    # Class
class QTerminalActionFabric(AbstractTypeFactory):
    @classmethod
    def register(cls_, key: str, cls: type[QTerminalAction]) -> None:
        super().register(key, cls)


    @classmethod
    def _try_parse(cls_, string: str) -> str | int | float | None:
        exc = suppress(Exception)

        if string in ('None', 'none', 'null', ''): return None

        with exc: return int(string)
        with exc: return float(string)

        return string


    @classmethod
    def _split_arguments(cls_, string: str) -> tuple[str | int | float | None]:
        key, *args = string.split('|')
        return (key, *(cls_._try_parse(arg) for arg in args))


    @classmethod
    def create(cls_, data: str) -> QTerminalAction:
        key, *args = cls_._split_arguments(data)

        cls = cls_.get(key)
        if cls is None:
            return QTerminalUnknownAction(key, *args)

        return cls(*args)


    @classmethod
    def get(cls, key: str) -> type[QTerminalAction]:
        return super().get(key)
#----------------------------------------------------------------------
