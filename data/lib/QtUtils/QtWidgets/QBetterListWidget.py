#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTreeView, QAbstractItemView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, QItemSelectionModel, QModelIndex, QSize, Signal, QItemSelection
#----------------------------------------------------------------------

    # Class
class _verification:
    def good_headers(headers = None):
        if not isinstance(headers, list): return False
        if len(headers) < 1: return False
        for i in headers:
            if not isinstance(i, str): return False
        return True



class QBetterListWidget(QTreeView):
    clicked = Signal()
    row_selection_changed = Signal(int, int)
    item_selection_changed = Signal(tuple or None, tuple or None)

    def __new__(cls, headers = ['column'], minimum_section_size: int = 50, alignment_flag = Qt.AlignmentFlag.AlignCenter) -> 'QBetterListWidget':
        if not _verification.good_headers(headers):
            print('Headers must be a list of strings!')
            return
        return super().__new__(cls, headers, minimum_section_size, alignment_flag)

    def __init__(self, headers: list[str] = None, minimum_section_size: int = 50, alignment_flag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft) -> None:
        super().__init__()
        self._headers = headers
        self.tree_view_model = QStandardItemModel()
        self.tree_view_model.setHorizontalHeaderLabels(self._headers)
        self.setModel(self.tree_view_model)
        self.setUniformRowHeights(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setRootIsDecorated(False)
        self.header().setDefaultAlignment(alignment_flag)
        self.header().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(True)
        self.header().setCascadingSectionResizes(True)
        self.header().setMinimumSectionSize(minimum_section_size)
        self.setIconSize(QSize(16, 16))

    def set_headers(self, headers = ['column']) -> None:
        if not _verification.good_headers(headers): return
        self._headers = headers
        self.tree_view_model.setHorizontalHeaderLabels(self._headers)

    def add_header(self, header = 'column') -> None:
        if not _verification.good_headers([header]): return
        self._headers.append(header)

    def set_header_alignment(self, alignment_flag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft) -> None:
        self.header().setDefaultAlignment(alignment_flag)

    def set_minimum_section_size(self, minimum_section_size: int = 50):
        self.header().setMinimumSectionSize(minimum_section_size)

    def get_headers(self) -> list[str]:
        return self._headers

    def index(self, item: tuple[str]) -> int:
        for i in range(self.tree_view_model.invisibleRootItem().rowCount()):
            if self.get_item(i) == item: return i
        return -1

    def get_items(self, append_order: bool = False) -> tuple[tuple[str]]:
        l = []
        root = self.tree_view_model.invisibleRootItem()
        for i in range(root.rowCount()):
            sub_l = []
            for j in range(root.columnCount()):
                if append_order: sub_l.append(root.child(i, j).text())
                else:
                    item = self.model().itemData(self.model().index(i, j))
                    if not item: break
                    sub_l.append(item[0])
            l.append(tuple(sub_l))

        return tuple(l)

    def get_item(self, index: int = 0) -> tuple[str] | None:
        if index < 0 or index >= self.count(): return None

        l = []
        root = self.tree_view_model.invisibleRootItem()
        for j in range(root.columnCount()):
            item = self.model().itemData(self.model().index(index, j))
            if not item: return None
            l.append(item[0])

        return tuple(l)

    def count(self) -> int:
        return len(self.get_items(True))

    def add_item(self, items: list[str], icon = None, alignment_flag: Qt.AlignmentFlag | list[Qt.AlignmentFlag] = Qt.AlignmentFlag.AlignLeft) -> None:
        if not _verification.good_headers(items):
            print('Items must be strings!')
            return

        for index in range(min(len(self._headers), len(items))):
            items[index] = QStandardItem(items[index])
            if isinstance(alignment_flag, list): items[index].setTextAlignment(alignment_flag[index])
            else: items[index].setTextAlignment(alignment_flag)

        for index in range(len(self._headers) - len(items)):
            items.append(QStandardItem(''))

        if icon != None:
            items[0].setIcon(QIcon(icon))

        self.tree_view_model.appendRow(items)

    def remove_item(self, index: int = 0) -> None:
        item = self.model().index(index, 1)
        self.model().removeRow(item.row(), item.parent())
    
    def remove_items(self, start_index: int = 0, end_index: int = 1) -> None:
        self.model().removeRows(start_index, end_index - start_index)

    def replace_item(self, index: int, items: list[str], icon = None, alignment_flag: Qt.AlignmentFlag | list[Qt.AlignmentFlag] = Qt.AlignmentFlag.AlignLeft) -> None:
        if not _verification.good_headers(items):
            print('Items must be strings!')
            return

        for i in range(min(len(self._headers), len(items))):
            items[i] = QStandardItem(items[i])
            if isinstance(alignment_flag, list): items[i].setTextAlignment(alignment_flag[i])
            else: items[i].setTextAlignment(alignment_flag)

        for i in range(len(self._headers) - len(items)):
            items.append(QStandardItem(''))

        if icon != None:
            items[0].setIcon(QIcon(icon))

        self.remove_item(index)
        self.tree_view_model.insertRow(index, items)

    def clear(self) -> None:
        self.tree_view_model.removeRows(0, self.tree_view_model.invisibleRootItem().rowCount())

    def select(self, index: int = 0) -> None:
        self.deselect_all()
        self.selectionModel().select(self.tree_view_model.index(index, 0, QModelIndex()), QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

    def deselect_all(self) -> None:
        self.selectionModel().clearSelection()

        for item in self.selectedIndexes():
            if self.selectionModel().isSelected(item):
                self.selectionModel().select(item, QItemSelectionModel.SelectionFlag.Deselect)

    def is_selection(self) -> bool:
        return bool(len(self.selectedIndexes()))

    def get_selected_row(self) -> int:
        return self.selectedIndexes()[0].row() if self.is_selection() else -1

    def get_selected_item(self) -> tuple[str]:
        return tuple(self.tree_view_model.data(self.selectedIndexes()[item]) for item in range(len(self._headers)))

    def get_selected_item_index(self) -> int:
        return self.selectedIndexes()[0].row()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        super().selectionChanged(selected, deselected)
        selection = self.get_selected_row()
        deselection = deselected.indexes()[0].row() if len(deselected.indexes()) > 0 else -1
        self.row_selection_changed.emit(selection, deselection)
        self.item_selection_changed.emit(self.get_item(selection) if selection != -1 else None, self.get_item(deselection) if deselection != -1 else None)
#----------------------------------------------------------------------
