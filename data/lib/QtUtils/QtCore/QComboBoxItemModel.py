#----------------------------------------------------------------------

    # Libraries
from typing import Union
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QListView
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel, QPersistentModelIndex

from ..QtGui.QSpecialCharacter import QSpecialCharacter
#----------------------------------------------------------------------

    # Class
class QComboBoxItemModel(QAbstractItemModel):
    class ItemDelegate(QStyledItemDelegate):
        def __init__(self, combo_box_item_model: 'QComboBoxItemModel') -> None:
            super().__init__(None)
            self._combo_box_item_model = combo_box_item_model


        def displayText(self, value: Union[str, int], locale: str) -> str:
            # Override displayText to show custom text in the combobox
            items = self._combo_box_item_model.get_items()
            for item in items:
                if item[0] == value:
                    return item[1].replace('\n', QSpecialCharacter.LineSeparator)

            return str(value)



    def __init__(self) -> None:
        super().__init__(None)
        self._items: list[tuple[str]] = []
        self._delegate = QComboBoxItemModel.ItemDelegate(self)


    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = ...) -> int:
        return len(self._items)

    def row_count(self) -> int:
        return self.rowCount()


    def columnCount(self, parent = QModelIndex()) -> int:
        return 1

    def column_count(self) -> int:
        return self.columnCount()


    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._items[index.row()][0]

        return None


    def index(self, row, column, parent=QModelIndex()) -> QModelIndex:
        if row >= 0 and row < len(self._items) and column == 0:
            return self.createIndex(row, column)

        return QModelIndex()


    def parent(self, child: QModelIndex) -> QModelIndex:
        return QModelIndex()


    def set_items(self, items: list[tuple[str]]) -> None:
        for item in items:
            if len(item) != 2:
                raise ValueError('Each item must be a tuple of length 2')

        self._items = items
        self.reset()


    def get_items(self) -> list[tuple[str]]:
        return self._items


    def add_item(self, item: str, value: str) -> None:
        self._items.append((item, value))


    def remove_item(self, item: str, value: str) -> None:
        self._items.remove((item, value))
        self.reset()


    def clear(self) -> None:
        self._items.clear()
        self.reset()


    def sort(self, reverse: bool = False) -> None:
        self._items.sort(reverse = reverse)
        self.reset()


    def reverse(self) -> None:
        self._items.reverse()
        self.reset()


    def reset(self) -> None:
        self.beginResetModel()
        self.endResetModel()


    def get_delegate(self) -> QStyledItemDelegate:
        return self._delegate


    def bind(self, combo_box: QComboBox) -> None:
        combo_box.setModel(self)
        combo_box.setModelColumn(0)

        lv = QListView()
        lv.setCursor(Qt.CursorShape.PointingHandCursor)
        lv.setWordWrap(True)

        combo_box.setView(lv)  # This line is important to show custom data in the dropdown
        combo_box.setItemDelegate(self._delegate)
#----------------------------------------------------------------------
