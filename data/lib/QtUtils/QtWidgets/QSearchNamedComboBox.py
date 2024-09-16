#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QComboBox, QCompleter
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QValidator, QStandardItemModel, QStandardItem
from typing import Sequence

from .QGridWidget import QGridWidget
from .QNamedComboBox import QNamedComboBox
#----------------------------------------------------------------------

    # Class
class QSearchNamedComboBox(QNamedComboBox):
    class ItemValidator(QValidator):
        def __init__(self, items: Sequence[str]) -> None:
            super().__init__()
            self._items = list(items)


        def add_item(self, item: str) -> None:
            self._items.append(item)

        def add_items(self, items: Sequence[str]) -> None:
            self._items.extend(items)


        def remove_item(self, item: str) -> None:
            self._items.remove(item)

        def remove_items(self, items: Sequence[str]) -> None:
            for item in items: self._items.remove(item)


        def clear_items(self) -> None:
            self._items.clear()


        def validate(self, input: str, pos: int) -> tuple[QValidator.State, str, int]:
            return QValidator.State.Acceptable, input, pos



    class StrictItemValidator(ItemValidator):
        def validate(self, input: str, pos: int) -> tuple[QValidator.State, str, int]:
            if input in self._items: return QValidator.State.Acceptable, input, pos
            return QValidator.State.Intermediate, input, pos



    def __init__(self, parent = None, name: str = '', placeholder: str = '', items: Sequence[str] = [], validator_cls: type[ItemValidator] = ItemValidator) -> None:
        super().__init__(parent, name)
        self.setProperty('QSearchNamedComboBox', True)

        self.combo_box.setEditable(True)

        self._validator = validator_cls(items)

        self.combo_box.lineEdit().setValidator(self._validator)
        self.combo_box.lineEdit().setPlaceholderText(placeholder)

        self.combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self._item_model = QStandardItemModel(self)
        self._item_model.setColumnCount(1)

        for item in items:
            item = QStandardItem(item)
            item.setData(item)
            self._item_model.appendRow([item])

        proxy_model = QSortFilterProxyModel(self)
        proxy_model.setSourceModel(self._item_model)
        proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        proxy_model.setFilterKeyColumn(0)
        proxy_model.setFilterRole(Qt.ItemDataRole.UserRole)

        self.combo_box.setModel(proxy_model)
        self.combo_box.setModelColumn(0)

        self._object_completer = QCompleter(self)
        self._object_completer.popup().setProperty('completerPopup', True)
        self._object_completer.popup().setCursor(Qt.CursorShape.PointingHandCursor)
        self._object_completer.popup().setMinimumHeight(200)
        self._object_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._object_completer.setModel(proxy_model)
        self._object_completer.setCompletionColumn(0)
        self._object_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.combo_box.setCompleter(self._object_completer)


    def addItem(self, item: str) -> None:
        self._item_model.appendRow([QStandardItem(item)])


    def addItems(self, items: list[str]) -> None:
        for item in items: self.addItem(item)


    def removeItem(self, item: str) -> None:
        for index in range(self._item_model.rowCount()):
            if self._item_model.item(index).text() == item:
                self._item_model.removeRow(index)
                break


    def removeItems(self, items: list[str]) -> None:
        for item in items: self.removeItem(item)
#----------------------------------------------------------------------
