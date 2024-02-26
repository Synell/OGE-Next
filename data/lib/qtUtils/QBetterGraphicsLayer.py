#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGraphicsItem, QWidget
#----------------------------------------------------------------------

    # Class
class QBetterGraphicsLayer:
    def __init__(self, id: int) -> None:
        self._id = id
        self._items: list[QGraphicsItem | QWidget] = []
        self._is_visible = True


    @property
    def id(self) -> int:
        return self._id


    @property
    def items(self) -> list[QGraphicsItem]:
        return self._items.copy()


    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        self._is_visible = value


    def add_item(self, item: QGraphicsItem | QWidget) -> None:
        self._items.append(item)

    def remove_item(self, item: QGraphicsItem | QWidget) -> None:
        self._items.remove(item)

    def clear(self) -> None:
        self._items.clear()


    def hide(self) -> None:
        self._is_visible = False

    def show(self) -> None:
        self._is_visible = True
#----------------------------------------------------------------------
