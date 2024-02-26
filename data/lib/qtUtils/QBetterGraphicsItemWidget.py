#----------------------------------------------------------------------

    # Libraries
from typing import Any
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QBetterGraphicsItemWidget(QGridFrame):
    def __init__(self, widget: QWidget) -> None:
        super().__init__()

        self._widget = widget

        super().setProperty('fake-focus', True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus | Qt.FocusPolicy.ClickFocus | Qt.FocusPolicy.TabFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self._patch_children(widget)

        self._root = QGridFrame()
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._root.grid_layout.setSpacing(0)
        self._root.setProperty('QBetterGraphicsItemWidget', True)
        self._root.setProperty('fake-focus', True)
        self.grid_layout.addWidget(self._root, 0, 0)

        self._root.grid_layout.addWidget(self._widget, 0, 0)


    @property
    def root_widget(self) -> QWidget:
        return self._root


    def _patch_children(self, widget: QWidget) -> None:
        if widget.focusPolicy() == Qt.FocusPolicy.NoFocus:
            widget.setProperty('fake-focus', True)
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus | Qt.FocusPolicy.ClickFocus | Qt.FocusPolicy.TabFocus)

        for child in widget.findChildren(QWidget):
            if isinstance(child, QWidget): self._patch_children(child)


    def set_property(self, name: str, value: Any) -> None:
        self._root.setProperty(name, value)
        self._root.style().unpolish(self._root)
        self._root.style().polish(self._root)

    def setProperty(self, name: str, value: Any) -> bool:
        self.set_property(name, str(value))


    def add_widget(self, widget: QWidget, row: int, column: int) -> None:
        self._root.grid_layout.addWidget(widget, row, column)

    def addWidget(self, widget: QWidget, row: int, column: int) -> None:
        self.add_widget(widget, row, column)


    @property
    def selected(self) -> bool:
        return self._root.property('selected')

    @selected.setter
    def selected(self, value: bool) -> None:
        if value:
            self._root.setProperty('selected', True)

        else:
            self._root.setProperty('selected', False)

        self._root.style().unpolish(self._root)
        self._root.style().polish(self._root)


    def setSelected(self, value: bool) -> None:
        self.selected = value
#----------------------------------------------------------------------
