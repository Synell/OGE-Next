#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from enum import Enum
from typing import Iterable
#----------------------------------------------------------------------

    # Class
class QProgressIndicatorItem(QLabel):
    class State(Enum):
        Normal = 0
        Current = 1
        Done = 2


    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setProperty('QProgressIndicatorItem', True)
        self.setProperty('state', QProgressIndicatorItem.State.Normal.value)


    @property
    def state(self) -> State:
        return QProgressIndicatorItem.State(self.property('state'))

    @state.setter
    def state(self, value: State) -> None:
        self.setProperty('state', value.value)



class QProgressIndicator(QFrame):
    class Direction(Enum):
        Left2Right = 'left2right',
        Right2Left = 'right2left',
        Top2Bottom = 'top2bottom',
        Bottom2Top = 'bottom2top'


    def __init__(self, parent = None, direction: Direction = Direction.Bottom2Top, compact: bool = True, content_margins: tuple = (16, 16, 16, 16)) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._direction = direction

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(*content_margins)

        self.setProperty('QProgressIndicator', True)
        # self.setStyleSheet('background-color: #262626;')

        self._current_index = 0
        self._compact = compact
        self._items: list[QProgressIndicatorItem] = []

        self._active_bar = QFrame()
        self._bar = QFrame()


    def add_item(self, title: QProgressIndicatorItem) -> None:
        self._items.append(title)
        self._rebuild()


    def add_items(self, titles: Iterable[QProgressIndicatorItem]) -> None:
        self._items.extend(titles)
        self._rebuild()


    def remove_item_at(self, index: int) -> None:
        self._items.pop(index)
        self._rebuild()


    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction) -> None:
        self._direction = value
        self._rebuild()

    def set_direction(self, value: Direction) -> None:
        self.direction = value


    @property
    def current_index(self) -> int:
        return self._current_index

    @current_index.setter
    def current_index(self, value: int) -> None:
        if value < 0 or value >= len(self._items):
            raise ValueError('Index out of range')

        self._current_index = value
        self._rebuild()

    def set_current_index(self, value: int) -> None:
        self.current_index = value


    @property
    def compact(self) -> bool:
        return self._compact

    @compact.setter
    def compact(self, value: bool) -> None:
        self._compact = value
        self._rebuild()

    def set_compact(self, value: bool) -> None:
        self.compact = value


    @property
    def count(self) -> int:
        return len(self._items)


    def _rebuild(self) -> None:
        match self._direction:
            case QProgressIndicator.Direction.Left2Right:
                self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

            case QProgressIndicator.Direction.Right2Left:
                self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

            case QProgressIndicator.Direction.Top2Bottom:
                self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

            case QProgressIndicator.Direction.Bottom2Top:
                self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self._active_bar.setParent(None)
        self._active_bar.deleteLater()

        self._bar.setParent(None)
        self._bar.deleteLater()

        self._active_bar = QFrame()
        self._active_bar.setProperty('QProgressIndicatorBar', True)
        self._active_bar.setProperty('active', True)
        # self._active_bar.setStyleSheet('background-color: green;')

        self._bar = QFrame()
        self._bar.setProperty('QProgressIndicatorBar', True)
        self._bar.setProperty('active', False)
        # self._bar.setStyleSheet('background-color: red;')

        if self._direction in (QProgressIndicator.Direction.Left2Right, QProgressIndicator.Direction.Right2Left):
            self._active_bar.setFixedHeight(2)
            self._layout.addWidget(self._active_bar, 0, 0, 1, max(self._current_index + 1, 1), Qt.AlignmentFlag.AlignVCenter)

            self._bar.setFixedHeight(2)
            self._layout.addWidget(self._bar, 0, self._current_index, 1, max(len(self._items) - self._current_index, 1), Qt.AlignmentFlag.AlignVCenter)

        else:
            self._active_bar.setFixedWidth(2)
            self._layout.addWidget(self._active_bar, 0, 0, max(self._current_index + 1, 1), 1, Qt.AlignmentFlag.AlignHCenter)

            self._bar.setFixedWidth(2)
            self._layout.addWidget(self._bar, self._current_index, 0, max(len(self._items) - self._current_index, 1), 1, Qt.AlignmentFlag.AlignHCenter)


        for i, item in enumerate(self._items):
            item.state = QProgressIndicatorItem.State(2 if i < self._current_index else int(i == self._current_index))
            item.setText(' ' if self._compact else f'{i + 1}')
            item.setFixedWidth(16 if self._compact else 32)
            item.setFixedHeight(16 if self._compact else 32)
            item.setProperty('compact', self._compact)
            
            if self._direction in (QProgressIndicator.Direction.Left2Right, QProgressIndicator.Direction.Right2Left):
                self._layout.addWidget(item, 0, i)

            else:
                self._layout.addWidget(item, i, 0)
#----------------------------------------------------------------------
