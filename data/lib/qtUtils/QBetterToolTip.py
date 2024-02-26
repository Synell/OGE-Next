#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent

from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Decorator
def QBetterToolTip(cls: QWidget):
    class Wrapper(cls):
        def __init__(self, *args, **kwargs) -> None:
            self._q_better_tooltip: QGridFrame | None = None
            self._q_better_tooltip_properties: dict[str, object] = {}
            super().__init__(*args, **kwargs)
            self._set_children_mouse_tracking(self, True)


        def _set_children_mouse_tracking(self, widget: QWidget, value: bool) -> None:
            widget.setMouseTracking(value)
            for child in widget.findChildren(QWidget):
                child.setMouseTracking(value)
                self._set_children_mouse_tracking(child, value)


        def setToolTip(self, widget: QWidget | str) -> None:
            if self._q_better_tooltip:
                self._q_better_tooltip.hide()
                self._q_better_tooltip.setParent(None)

            self._q_better_tooltip = QGridFrame()

            self._q_better_tooltip.setParent(self)
            self._q_better_tooltip.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self._q_better_tooltip.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
            self._q_better_tooltip.setAttribute(Qt.WidgetAttribute.WA_MouseTracking, False)
            self._q_better_tooltip.setMouseTracking(False)
            self._q_better_tooltip.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self._q_better_tooltip.setProperty('QBetterToolTip', True)
            for property, value in self._q_better_tooltip_properties.items():
                self._q_better_tooltip.setProperty(property, value)

            if isinstance(widget, str):
                label = QLabel(widget)
                label.setContentsMargins(0, 0, 0, 0)
                label.setMouseTracking(False)
                label.setWordWrap(True)
                self._q_better_tooltip.grid_layout.addWidget(label, 0, 0)

            elif isinstance(widget, QWidget):
                widget.setContentsMargins(0, 0, 0, 0)
                if widget.layout(): widget.layout().setContentsMargins(0, 0, 0, 0)
                self._set_children_mouse_tracking(widget, False)
                self._q_better_tooltip.grid_layout.addWidget(widget, 0, 0)

            else:
                raise TypeError('widget must be a QWidget or a str')

            self._q_better_tooltip.hide()


        def set_tooltip(self, widget: QWidget | str) -> None:
            self.setToolTip(widget)


        def set_tooltip_property(self, property: str, value: object) -> None:
            if self._q_better_tooltip:
                self._q_better_tooltip.setProperty(property, value)
                self._q_better_tooltip.style().unpolish(self._q_better_tooltip)
                self._q_better_tooltip.style().polish(self._q_better_tooltip)

            self._q_better_tooltip_properties[property] = value


        def enterEvent(self, event: QEvent) -> None:
            if self._q_better_tooltip and self.isEnabled():
                self._q_better_tooltip.show()

            super().enterEvent(event)


        def leaveEvent(self, event: QEvent) -> None:
            if self._q_better_tooltip:
                self._q_better_tooltip.hide()

            super().leaveEvent(event)


        def mouseMoveEvent(self, event: QMouseEvent) -> None:
            if self._q_better_tooltip:
                self._q_better_tooltip.move(event.globalPos().x() + 18, event.globalPos().y() + 22)
                self._q_better_tooltip.raise_()
                self._q_better_tooltip.resize(self._q_better_tooltip.sizeHint())

            super().mouseMoveEvent(event)


    return Wrapper
#----------------------------------------------------------------------
