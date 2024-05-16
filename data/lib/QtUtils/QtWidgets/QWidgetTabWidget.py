#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QTabWidget
from PySide6.QtCore import Qt, Signal
from .QGridWidget import QGridWidget
from .QWidgetTabBar import QWidgetTabBar, QWidgetTabBarItem
from .QSlidingStackedWidget import QSlidingStackedWidget
#----------------------------------------------------------------------

    # Class
class QWidgetTabWidget(QGridWidget):
    clicked = Signal(int)
    tab_close_requested = Signal(int)

    tab_changed = Signal(QWidgetTabBarItem, QWidget)
    tab_index_changed = Signal(int)

    moved = Signal(int, int)


    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> None:
        super().__init__()

        self._tab_bar = QWidgetTabBar(orientation)
        self.grid_layout.addWidget(self._tab_bar, 0, 0)
        self._tab_position = QTabWidget.TabPosition.North

        self._root = QSlidingStackedWidget()
        self._root.set_orientation(orientation)
        self.grid_layout.addWidget(self._root, 1, 0)

        self._tab_bar.moved.connect(self._moved)


    @property
    def tab_bar(self) -> QWidgetTabBar:
        return self._tab_bar


    @property
    def tab_position(self) -> QTabWidget.TabPosition:
        return self._tab_position

    @tab_position.setter
    def tab_position(self, value: QTabWidget.TabPosition) -> None:
        self._tab_position = value
        self._tab_bar.setParent(None)
        self._root.setParent(None)

        match value:
            case QTabWidget.TabPosition.North:
                self._tab_bar.orientation = Qt.Orientation.Horizontal
                self.grid_layout.addWidget(self._tab_bar, 0, 0)
                self._root.set_orientation(Qt.Orientation.Horizontal)
                self.grid_layout.addWidget(self._root, 1, 0)

            case QTabWidget.TabPosition.South:
                self._tab_bar.orientation = Qt.Orientation.Horizontal
                self.grid_layout.addWidget(self._tab_bar, 1, 0)
                self._root.set_orientation(Qt.Orientation.Horizontal)
                self.grid_layout.addWidget(self._root, 0, 0)

            case QTabWidget.TabPosition.West:
                self._tab_bar.orientation = Qt.Orientation.Vertical
                self.grid_layout.addWidget(self._tab_bar, 0, 0)
                self._root.set_orientation(Qt.Orientation.Vertical)
                self.grid_layout.addWidget(self._root, 0, 1)

            case QTabWidget.TabPosition.East:
                self._tab_bar.orientation = Qt.Orientation.Vertical
                self.grid_layout.addWidget(self._tab_bar, 0, 1)
                self._root.set_orientation(Qt.Orientation.Vertical)
                self.grid_layout.addWidget(self._root, 0, 0)

    def set_tab_position(self, value: QTabWidget.TabPosition) -> None:
        self.tab_position = value


    def add_tab(self, tab_widget: QWidget | QWidgetTabBarItem, widget: QWidget) -> None:
        w = self._tab_bar.add_tab(tab_widget)
        self._root.addWidget(widget)

        w.clicked.connect(lambda: self._clicked_on_tab(self._root.indexOf(widget)))
        w.tab_close_requested.connect(lambda: self._close_requested_on_tab(self._root.indexOf(widget)))

        self.set_current_index(self.count() - 1)


    def insert_tab(self, index: int, tab_widget: QWidget | QWidgetTabBarItem, widget: QWidget) -> None:
        w = self._tab_bar.insert_tab(index, tab_widget)
        self._root.insertWidget(index, widget)

        w.clicked.connect(lambda: self._clicked_on_tab(self._root.indexOf(widget)))
        w.tab_close_requested.connect(lambda: self._close_requested_on_tab(self._root.indexOf(widget)))

        self._tab_bar.select_index(index)
        self._root.set_current_index(index)


    def remove_tab(self, tab_widget: QWidgetTabBarItem, widget: QWidget) -> None:
        tab_index = self._tab_bar.index_of(tab_widget)
        widget_index = self._root.indexOf(widget)

        if tab_index != widget_index: raise ValueError('Tab and widget are not in sync')

        self._tab_bar.remove_tab(tab_widget)
        self._root.removeWidget(widget)

        new_index = min(tab_index, self.count() - 1)
        if new_index >= 0: self.force_set_current_index(new_index)


    def pop_tab(self, index: int) -> tuple[QWidgetTabBarItem, QWidget]:
        tab = self._tab_bar.pop_tab(index)
        widget = self._root.widget(index)
        self._root.removeWidget(widget)

        new_index = min(index, self.count() - 1)
        if new_index >= 0: self.force_set_current_index(new_index)

        return tab, widget


    def clear(self) -> None:
        self._tab_bar.clear()
        for i in reversed(range(self._root.count())): self._root.removeWidget(self._root.widget(i))


    def tab(self, index: int) -> QWidgetTabBarItem:
        return self._tab_bar.widget(index)


    def widget(self, index: int) -> QWidget:
        return self._root.widget(index)


    def index_of_tab(self, tab: QWidgetTabBarItem) -> int:
        return self._tab_bar.index_of(tab)


    def index_of_widget(self, widget: QWidget) -> int:
        return self._root.indexOf(widget)


    def set_current_index(self, index: int) -> None:
        self._tab_bar.select_index(index)
        self._root.slide_in_index(index)
        self._call_tab_changed()


    def force_set_current_index(self, index: int) -> None:
        self._tab_bar.select_index(index)
        self._root.set_current_index(index)
        self._call_tab_changed()


    def count(self) -> int:
        return self._root.count()


    def current_tab(self) -> QWidgetTabBarItem | None:
        return self._tab_bar.current_tab


    def current_widget(self) -> QWidget:
        return self._root.widget(self._root.current_index)


    def current_index(self) -> int:
        return self._root.current_index


    def set_current_tab(self, tab: QWidgetTabBarItem) -> None:
        self._tab_bar.select_tab(tab)
        self._root.slide_in_index(self._tab_bar.index_of(tab))
        self._call_tab_changed()


    def set_current_widget(self, widget: QWidget) -> None:
        index = self._root.indexOf(widget)
        self._tab_bar.select_index(index)
        self._root.slide_in_index(index)
        self._call_tab_changed()


    def _clicked_on_tab(self, index: int) -> None:
        self.clicked.emit(index)
        self._root.slide_in_index(index)
        self._call_tab_changed()


    def _close_requested_on_tab(self, index: int) -> None:
        self.tab_close_requested.emit(index)


    def _moved(self, previous: int, index: int) -> None:
        if index == previous: return

        widget = self._root.widget(previous)
        self._root.removeWidget(widget)
        self._root.insertWidget(index, widget)

        self._root.set_current_index(index)

        self.moved.emit(previous, index)


    def _call_tab_changed(self) -> None:
        self.tab_changed.emit(self.current_tab(), self.current_widget())
        self.tab_index_changed.emit(self.current_index())
#----------------------------------------------------------------------
