#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QSizePolicy, QLayout, QLayoutItem
from PySide6.QtCore import Qt, QRect, QSize, QPoint
#----------------------------------------------------------------------

    # Class
class QFlowLayout(QLayout):
    def __init__(self, parent = None, orientation: Qt.Orientation = Qt.Orientation.Horizontal, spacing: int = -1) -> None:
        super().__init__(parent)
        self.orientation = orientation

        self.setContentsMargins(0, 0, 0, 0)

        self.setSpacing(spacing)

        self._item_list: list = []


    def __del__(self) -> None:
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)


    def addItem(self, item: QLayoutItem) -> None:
        self._item_list.append(item)

    # def addWidget(self, widget):
    #     self.addItem(QWidgetItem(widget))


    def count(self) -> int:
        return len(self._item_list)


    def itemAt(self, index: int) -> QLayoutItem:
        if index >= 0 and index < len(self._item_list):
            return self._item_list[index]

        return None


    def takeAt(self, index: int) -> QLayoutItem:
        if index >= 0 and index < len(self._item_list):
            return self._item_list.pop(index)

        return None


    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(0)


    def hasHeightForWidth(self) -> bool:
        return self.orientation == Qt.Orientation.Horizontal


    def heightForWidth(self, width: int) -> int:
        return self._do_layout(QRect(0, 0, width, 0), True)


    def hasWidthForHeight(self) -> bool:
        return self.orientation == Qt.Orientation.Vertical


    def widthForHeight(self, height: int) -> int:
        return self._do_layout(QRect(0, 0, 0, height), True)


    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self._do_layout(rect, False)


    def sizeHint(self) -> QSize:
        return self.minimumSize()


    def minimumSize(self) -> QSize:
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size


    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        x = rect.x()
        y = rect.y()
        line_height = column_width = height_for_width = 0

        for item in self._item_list:
            wid = item.widget()
            space_x = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
            space_y = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)

            if self.orientation == Qt.Orientation.Horizontal:
                next_x = x + item.sizeHint().width() + space_x
                if next_x - space_x > rect.right() and line_height > 0:
                    x = rect.x()
                    y = y + line_height + space_y
                    next_x = x + item.sizeHint().width() + space_x
                    line_height = 0

                if not test_only:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                x = next_x
                line_height = max(line_height, item.sizeHint().height())

            else:
                next_y = y + item.sizeHint().height() + space_y
                if next_y - space_y > rect.bottom() and column_width > 0:
                    x = x + column_width + space_x
                    y = rect.y()
                    next_y = y + item.sizeHint().height() + space_y
                    column_width = 0

                height_for_width += item.sizeHint().height() + space_y
                if not test_only:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                y = next_y
                column_width = max(column_width, item.sizeHint().width())

        if self.orientation == Qt.Orientation.Horizontal:
            return y + line_height - rect.y()

        else:
            return height_for_width - rect.y()
#----------------------------------------------------------------------
