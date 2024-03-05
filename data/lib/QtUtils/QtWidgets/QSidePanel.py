#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from typing import Callable, Iterator
from PySide6.QtWidgets import QPushButton, QSizePolicy, QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
from .QScrollableGridFrame import QScrollableGridFrame
#----------------------------------------------------------------------

    # Class
class QSidePanelItem:
    clicked = Signal()

    def __init__(self, text: str = '', icon: QIcon|str = None, connect: Callable = None) -> None:
        self._widget = QPushButton()
        # self._widget.setCheckable(True)
        self._widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self._widget.setProperty('QSidePanel', True)
        self.text = text
        self.icon = icon
        self.auto_select = True
        self.connect = connect

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._widget.setText(text)

    @property
    def icon(self) -> QIcon:
        return self._icon

    @icon.setter
    def icon(self, icon: QIcon|str) -> None:
        self._icon = icon if isinstance(icon, QIcon) else QIcon(icon)
        if icon is None: self._widget.setIcon(QIcon())
        else: self._widget.setIcon(self.icon)

    @property
    def auto_select(self) -> bool:
        return self._auto_select

    @auto_select.setter
    def auto_select(self, auto_select: bool) -> None:
        self._auto_select = auto_select

    @property
    def connect(self) -> Callable:
        return self._connect

    @connect.setter
    def connect(self, connect: Callable) -> None:
        self._connect = connect



class QSidePanelSeparator:
    class Shape(Enum):
        Plain = QFrame.Shadow.Plain
        Raised = QFrame.Shadow.Raised
        Sunken = QFrame.Shadow.Sunken

    def __init__(self, shape: Shape = Shape.Sunken) -> None:
        self.shape = shape
        self._widget = QFrame()
        self._widget.setFixedHeight(1)
        self._widget.setFrameShape(QFrame.Shape.HLine)

    @property
    def shape(self) -> Shape:
        return self.shape_

    @shape.setter
    def shape(self, shape: Shape) -> None:
        if type(shape) is QSidePanelSeparator.Shape:
            self.shape_ = shape
        else: raise ValueError(f'Argument must be a \'QSidePanelSeparator.Shape\'.')


class QSidePanel(QScrollableGridFrame):
    current_index_changed: Signal = Signal(int)
    current_item_changed: Signal = Signal(QSidePanelItem)

    def __init__(self, parent = None, width: int = 120, transparent: bool = False) -> None:
        super().__init__()
        self.set_transparent(transparent)
        self.setProperty('color', 'main')

        self._items = []

        self.setParent(parent)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._items = []
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.set_width(width)
        self.setProperty('QSidePanel', True)

        self._current_index = 0
        self.update()

    @property
    def transparent(self) -> bool:
        return self.property('transparent')

    def set_transparent(self, transparent: bool) -> None:
        self.setProperty('transparent', transparent)

    @property
    def width(self) -> int:
        return self.width()

    def set_width(self, width: int) -> None:
        self.setMinimumWidth(width)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

    @property
    def current_index(self) -> int:
        return self._current_index

    def set_current_index(self, index: int) -> None:
        if index >= self.count() or index < 0: raise IndexError(f'Index {index} out of range.')
        self._current_index = index
        self.update()

    @property
    def current_item(self) -> QSidePanelItem:
        return self._items[self._current_index]

    def set_current_item(self, item: QSidePanelItem) -> None:
        self.set_current_index(self.items.index(item))

    def update(self) -> None:
        if self._current_index >= self.count(): self._current_index = self.count() - 1
        if self._current_index < 0: self._current_index = 0

        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        send_param = lambda i: lambda: self._clicked(i)

        for index, item in enumerate(self._items):
            if type(item) is QSidePanelItem:
                try: item._widget.clicked.disconnect()
                except: pass
                item._widget.clicked.connect(send_param(index))
                # item._widget.setChecked(index == self._current_index)
                item._widget.setProperty('selected', True) if index == self._current_index else item._widget.setProperty('selected', False)
                item._widget.clearFocus()
                item._widget.update()
            self.scroll_layout.addWidget(item._widget, index, 0)

    def _clicked(self, index: int) -> None:
        self.current_index_changed.emit(index)
        self.current_item_changed.emit(self._items[index])
        if self._items[index].auto_select: self._current_index = index
        if self._items[index].connect is not None: self._items[index].connect()
        self.update()

    def add_item(self, item: QSidePanelItem) -> None:
        self._items.append(item)
        self.update()

    def add_items(self, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.add_item(item)

    def insert_item(self, index: int, item: QSidePanelItem) -> None:
        self._items.insert(index, item)
        self.update()

    def insert_items(self, index: int, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.insert_item(index, item)

    def remove_item(self, item: QSidePanelItem) -> None:
        self._items.remove(item)
        self.update()

    def remove_item_at(self, index: int) -> None:
        self._items.pop(index)
        self.update()

    def remove_items(self, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.remove_item(item)

    def pop_item(self, index: int) -> QSidePanelItem:
        item = self._items.pop(index)
        self.update()
        return item

    def clear(self) -> None:
        self._items = []
        self.update()

    def set_item_callback(self, index: int, callback: Callable) -> None:
        self._items[index].connect = callback
        self.update()

    @property
    def items(self) -> list[QSidePanelItem]:
        return [item for item in self._items]

    def item_at(self, index: int) -> QSidePanelItem:
        return self._items[index]

    def index_of(self, item: QSidePanelItem) -> int:
        return self._items.index(item)

    def count(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[QSidePanelItem]:
        return iter(self._items)

    def __getitem__(self, index: int) -> QSidePanelItem:
        return self._items[index]

    def __setitem__(self, index: int, item: QSidePanelItem) -> None:
        self._items[index] = item
        self.update()
#----------------------------------------------------------------------
