#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTreeView, QAbstractItemView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, QItemSelectionModel, QModelIndex, QSize
#----------------------------------------------------------------------

    # Class
class _verification:
    def good_headers(headers = None):
        if type(headers) is not list: return False
        if len(headers) < 1: return False
        for i in headers:
            if type(i) is not str: return False
        return True



class QBetterListWidget(QTreeView):
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

    def get_items(self) -> tuple[tuple[str]]:
        l = []
        root = self.tree_view_model.invisibleRootItem()
        for i in range(root.rowCount()):
            subL = []
            for j in range(root.columnCount()):
                subL.append(root.child(i, j).text())
            l.append(tuple(subL))

        return tuple(l)

    def get_item(self, index: int = 0) -> tuple[str]:
        l = []
        root = self.tree_view_model.invisibleRootItem()
        for j in range(root.columnCount()):
            l.append(root.child(index, j).text())

        return tuple(l)

    def count(self) -> int:
        return len(self.get_items())

    def add_item(self, items: list[str], icon = None, alignmentFlag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft) -> None:
        if not _verification.good_headers(items):
            print('Items must be strings!')
            return

        for index in range(min(len(self._headers), len(items))):
            items[index] = QStandardItem(items[index])
            items[index].setTextAlignment(alignmentFlag)

        for index in range(len(self._headers) - len(items)):
            items.append(QStandardItem(''))

        if icon != None:
            items[0].setIcon(QIcon(icon))

        self.tree_view_model.appendRow(items)

    def remove_item(self, index: int = 0) -> None:
        self.tree_view_model.removeRow(index)
    
    def remove_items(self, startIndex: int = 0, endIndex: int = 1) -> None:
        self.tree_view_model.removeRows(startIndex, endIndex)

    def clear(self) -> None:
        self.tree_view_model.removeRows(0, self.tree_view_model.invisibleRootItem().rowCount())

    def select(self, index: int = 0) -> None:
        self.deselect_all()
        self.selectionModel().select(self.tree_view_model.index(index, 0, QModelIndex()), QItemSelectionModel.SelectionFlag.Select|QItemSelectionModel.SelectionFlag.Rows)

    def deselect_all(self) -> None:
        self.clearSelection()

    def is_selection(self) -> bool:
        return bool(len(self.selectedIndexes()))

    def get_selected_row(self) -> int:
        return self.selectedIndexes()[0].row()

    def get_selected_item(self) -> tuple[str]:
        return tuple(self.tree_view_model.data(self.selectedIndexes()[item]) for item in range(len(self._headers)))

    def get_selected_item_index(self) -> int:
        return self.selectedIndexes()[0].row()
#----------------------------------------------------------------------
