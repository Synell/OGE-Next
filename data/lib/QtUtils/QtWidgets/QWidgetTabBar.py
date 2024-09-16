#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QSizePolicy, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QMouseEvent
from .QScrollableGridWidget import QScrollableGridWidget
from .QDragList import QDragList, QDragListItem
from .QIconWidget import QIconWidget
from ..QtCore import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QWidgetTabBarItem(QDragListItem):
    _close_icon = None
    _unsaved_icon = None
    _icon_size = QSize(16, 16)


    clicked = Signal()
    tab_close_requested = Signal()


    def init(app: QBaseApplication) -> None:
        QWidgetTabBarItem._close_icon = app.get_icon('widgettabbar/close.png', True, app.save_data.IconMode.Global)
        QWidgetTabBarItem._unsaved_icon = app.get_icon('widgettabbar/unsaved.png', True, app.save_data.IconMode.Global)


    def __init__(self, widget: QWidget, closable: bool = True, savable: bool = True) -> None:
        super().__init__()
        self._savable = savable

        self._widget = widget
        self.setProperty('QWidgetTabBarItem', True)
        self.setProperty('selected', False)
        self.layout_.addWidget(self._widget, 0, 0)

        self._close_button = QPushButton()
        self._close_button.setProperty('close', True)
        self._close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_button.setFixedSize(self._icon_size.width(), self._icon_size.height())
        self._close_button.setIcon(self._close_icon)
        self._close_button.setIconSize(QSize(self._icon_size.width(), self._icon_size.height()))
        self._close_button.clicked.connect(self._close_requested_on_widget)
        self.layout_.addWidget(self._close_button, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        if not closable: self._close_button.setVisible(False)

        self._unsaved_icon = QIconWidget(None, self._unsaved_icon, QSize(self._icon_size.width(), self._icon_size.height()), False)
        self._unsaved_icon.setProperty('unsaved', True)
        self._unsaved_icon.setFixedSize(self._icon_size.width(), self._icon_size.height())
        self.layout_.addWidget(self._unsaved_icon, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self._unsaved_icon.setVisible(False)

        self.layout_.setRowStretch(1, 1)
        self.layout_.setColumnStretch(1, 1)


    @property
    def selected(self) -> bool:
        return self.property('selected')

    @selected.setter
    def selected(self, value: bool) -> None:
        self.setProperty('selected', value)
        self.style().polish(self)
        self._close_button.style().polish(self._close_button)


    @property
    def saved(self) -> bool:
        return not self._unsaved_icon.isVisible() or not self._savable

    @saved.setter
    def saved(self, value: bool) -> None:
        if not self._savable: raise ValueError('This tab is not savable')
        self._unsaved_icon.setVisible(not value)


    @property
    def widget(self) -> QWidget:
        return self._widget

    @widget.setter
    def widget(self, value: QWidget) -> None:
        close_visible = self._close_button.isVisible()
        unsaved_visible = self._unsaved_icon.isVisible()

        self._widget.setParent(None)
        self._close_button.setParent(None)
        self._unsaved_icon.setParent(None)

        self._widget = value
        self.layout_.addWidget(self._widget, 0, 0)
        self.layout_.addWidget(self._close_button, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self._close_button.setVisible(close_visible)
        self._unsaved_icon.setVisible(unsaved_visible)

        self.style().polish(self)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        self.clicked.emit()

    def _close_requested_on_widget(self) -> None:
        self.tab_close_requested.emit()


class QWidgetTabBar(QScrollableGridWidget):
    clicked = Signal(int)
    close_requested = Signal(int)
    moved = Signal(int, int)

    tab_changed = Signal(QWidgetTabBarItem)
    tab_index_changed = Signal(int)


    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> None:
        super().__init__()

        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self._root = QDragList(None, orientation)
        self._root.moved.connect(self.moved.emit)
        self.layout_.addWidget(self._root)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self._root.layout().setContentsMargins(0, 0, 0, 0)
        self._root.layout().setSpacing(5)
        self.layout_.setRowStretch(1, 1)
        self.layout_.setColumnStretch(1, 1)


    @property
    def orientation(self) -> Qt.Orientation:
        return self._root.orientation

    @orientation.setter
    def orientation(self, value: Qt.Orientation) -> None:
        self._root.set_orientation(value)

    def set_orientation(self, value: Qt.Orientation) -> None:
        self._root.set_orientation(value)


    @property
    def current_tab(self) -> QWidgetTabBarItem | None:
        for tab in self.tabs:
            if tab.selected: return tab

        return None

    @property
    def current_index(self) -> int:
        for i, tab in enumerate(self.tabs):
            if tab.selected: return i

        return -1


    @property
    def tabs(self) -> tuple[QWidgetTabBarItem]:
        return tuple(self._root.items)


    def _convert_widget(self, widget: QWidget | QWidgetTabBarItem) -> QWidgetTabBarItem:
        if isinstance(widget, QWidgetTabBarItem): return widget
        else: return QWidgetTabBarItem(widget)


    def add_tab(self, widget: QWidget | QWidgetTabBarItem) -> QWidgetTabBarItem:
        w = self._convert_widget(widget)
        self._root.add_item(w)
        w.clicked.connect(lambda: self._item_clicked(w))
        w.tab_close_requested.connect(lambda: self._close_requested(w))
        return w


    def insert_tab(self, index: int, widget: QWidget | QWidgetTabBarItem) -> QWidgetTabBarItem:
        w = self._convert_widget(widget)
        self._root.insert_item(index, w)
        w.clicked.connect(lambda: self._item_clicked(w))
        w.tab_close_requested.connect(lambda: self._close_requested(w))
        return w


    def remove_tab(self, widget: QWidget | QWidgetTabBarItem) -> None:
        w = self._convert_widget(widget)
        self._root.remove_item(w)
        w.clicked.disconnect()
        w.tab_close_requested.disconnect()


    def pop_tab(self, index: int) -> QWidgetTabBarItem:
        w: QWidgetTabBarItem = self._root.pop(index)
        w.clicked.disconnect()
        w.tab_close_requested.disconnect()
        return w


    def clear(self) -> None:
        self._root.clear()


    def index_of(self, widget: QWidget | QWidgetTabBarItem) -> int:
        return self._root.index(self._convert_widget(widget))


    def select_tab(self, widget: QWidgetTabBarItem) -> None:
        index = self.index_of(widget)
        if index == -1: raise ValueError('Tab not found')
        self.select_index(index)


    def select_index(self, index: int) -> None:
        while tab := self.current_tab: tab.selected = False
        tab: QWidgetTabBarItem = list(self._root.items)[index]
        tab.selected = True
        tab.widget.setFocus()
        self._call_tab_changed()


    def count(self) -> int:
        return len(list(self._root.items))


    def widget(self, index: int) -> QWidgetTabBarItem:
        return list(self._root.items)[index]


    def _item_clicked(self, widget: QWidgetTabBarItem) -> None:
        self.select_tab(widget)
        self.clicked.emit(self.index_of(widget))

    def _close_requested(self, widget: QWidgetTabBarItem) -> None:
        self.select_tab(widget)
        self.close_requested.emit(self.index_of(widget))


    def _call_tab_changed(self) -> None:
        self.tab_changed.emit(self.current_tab)
        self.tab_index_changed.emit(self.current_index)
#----------------------------------------------------------------------
