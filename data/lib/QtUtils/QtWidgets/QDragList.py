#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStyleOption, QStyle
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter
from PySide6.QtCore import Qt, Signal
from typing import Generator

from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QDragListItem(QGridFrame):
    normal_cursor = Qt.CursorShape.ArrowCursor
    drag_cursor = Qt.CursorShape.ClosedHandCursor

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setCursor(self.normal_cursor)

        self.mouse_click_x = 0
        self.mouse_click_y = 0
        self.old_x = 0
        self.old_y = 0


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if (not (event.buttons() == Qt.MouseButton.LeftButton)): return
        if (self._is_minimum_distance_riched(event)): return
        if (self.cursor() != self.drag_cursor): self.setCursor(self.drag_cursor)
        self.raise_()

        if self.isVertical():
            y = event.globalPosition().y() - self.mouse_click_y + self.old_y
            bottom_border = self.parentWidget().geometry().height() - self.geometry().height()
            if (y < 0): y = 0
            elif (y > bottom_border): y = bottom_border
            self.move(int(self.old_x), int(y))

        else:
            x = event.globalPosition().x() - self.mouse_click_x + self.old_x
            bottom_border = self.parentWidget().geometry().width() - self.geometry().width()
            if (x < 0): x = 0
            elif (x > bottom_border): x = bottom_border
            self.move(int(x), int(self.old_y))


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if (event.buttons() == Qt.MouseButton.LeftButton): self.dragStartPosition = event.position()
        self.old_x = self.geometry().x()
        self.old_y = self.geometry().y()
        self.mouse_click_x = event.globalPosition().x()
        self.mouse_click_y = event.globalPosition().y()


    def _is_minimum_distance_riched(self, event: QMouseEvent) -> bool:
        return False
        # return (event.position() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance()


    def _move_in_layout(self, widget: QWidget, direction: str) -> bool:
        layout: QHBoxLayout | QVBoxLayout = widget.parentWidget().layout()

        index = layout.indexOf(widget)
        if (direction == 'MoveUp' and index == 0): return False
        if (direction == 'MoveDown' and index == layout.count() - 1): return False
        new_index = index - 1 if direction == 'MoveUp' else index + 1
        layout.removeWidget(widget)
        layout.insertWidget(new_index, widget)
        self.parentWidget().moved.emit(index, new_index)
        return True


    def paintEvent(self, _: QPaintEvent) -> None:
        style_option = QStyleOption()
        style_option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, style_option, painter, self)


    def mouseReleaseEvent(self, _: QMouseEvent) -> None:
        self.setCursor(self.normal_cursor)

        if self.isVertical():
            y = self.geometry().y()
            direct = ''
            offset = 0
            if(self.old_y > y):
                offset = self.old_y - y
                direct = 'MoveUp'
            elif(self.old_y < y):
                offset = y - self.old_y
                direct = 'MoveDown'
            count = offset // self.height()

        else:
            x = self.geometry().x()
            direct = ''
            offset = 0
            if(self.old_x > x):
                offset = self.old_x - x
                direct = 'MoveUp'
            elif(self.old_x < x):
                offset = x - self.old_x
                direct = 'MoveDown'
            count = offset // self.width()

        for _ in range(count): self._move_in_layout(self, direct)
        self.update()
        layout = self.parentWidget().layout()
        layout.update()
        self.saveGeometry()


    def isVertical(self) -> bool:
        return self.parentWidget().orientation == Qt.Orientation.Vertical



class QDragList(QWidget):
    moved = Signal(int, int)

    def __init__(self, parent = None, orientation: Qt.Orientation = Qt.Orientation.Vertical) -> None:
        super().__init__(parent)

        self._orientation = orientation

        if self._orientation == Qt.Orientation.Vertical: self._layout = QVBoxLayout()
        else: self._layout = QHBoxLayout()

        self.setLayout(self._layout)

        self.setProperty('QDragAndDropList', True)


    @property
    def orientation(self) -> Qt.Orientation:
        return self._orientation

    @orientation.setter
    def orientation(self, value: Qt.Orientation) -> None:
        self.set_orientation(value)

    def set_orientation(self, orientation: Qt.Orientation) -> None:
        self._orientation = orientation
        children = list(self.items)

        for child in children: self.remove_item(child)
        margins = self._layout.contentsMargins()
        spacing = self._layout.spacing()

        if self._orientation == Qt.Orientation.Vertical: self._layout = QVBoxLayout()
        else: self._layout = QHBoxLayout()

        self._layout.setContentsMargins(margins)
        self._layout.setSpacing(spacing)

        self.setLayout(self._layout)

        for child in children: self.add_item(child)


    def add_item(self, item: QDragListItem) -> None:
        self._layout.addWidget(item)


    def insert_item(self, index: int, item: QDragListItem) -> None:
        self._layout.insertWidget(index, item)


    def remove_item(self, item: QDragListItem) -> None:
        self._layout.removeWidget(item)
        item.setParent(None)


    def pop(self, index: int) -> QDragListItem:
        item = self._layout.itemAt(index).widget()
        self.remove_item(item)
        return item


    def clear(self) -> None:
        for child in list(self.items): self.remove_item(child)


    def index(self, item: QDragListItem) -> int:
        return self._layout.indexOf(item)


    @property
    def items(self) -> Generator[QDragListItem, None, None]:
        for i in range(self._layout.count()):
            if (not self._layout.itemAt(i)): continue

            w = self._layout.itemAt(i).widget()
            if (isinstance(w, QDragListItem)):
                yield w
#----------------------------------------------------------------------
