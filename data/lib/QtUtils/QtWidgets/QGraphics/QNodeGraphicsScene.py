#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QRect, Signal, QPointF
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QGraphicsView

from .QNodeGraphicsItemWidget import QNodeGraphicsItemWidget
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .QNodeGraphicsItemLink import QNodeGraphicsItemLink
from .QNodeGraphicsBlockWidget import QNodeGraphicsBlockWidget
from .. import QBetterGraphicsItemWidget, QBetterGraphicsScene
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsScene(QBetterGraphicsScene):
    lmb_pressed = Signal(QNodeGraphicsItemWidgetField.Connector)
    lmb_released = Signal(QNodeGraphicsItemWidgetField.Connector)


    def __init__(self, parent: QGraphicsView, size: QRect) -> None:
        super().__init__(parent, size)
        self.add_layer(self.connection_layer)


    @property
    def connection_layer(self) -> int:
        return 10


    def add_item(self, item: QGraphicsItem | QBetterGraphicsItemWidget, layer: int = 0) -> QGraphicsItem | QGraphicsProxyWidget:
        ret = super().add_item(item, layer)

        if isinstance(item, (QNodeGraphicsItemWidget, QNodeGraphicsBlockWidget)):
            item.lmb_pressed.connect(self.lmb_pressed.emit)
            item.lmb_released.connect(self.lmb_released.emit)

        return ret


    def remove_item(self, item: QGraphicsItem | QBetterGraphicsItemWidget, layer: int = 0) -> None:
        widget = item.widget() if isinstance(item, QGraphicsProxyWidget) else None

        if isinstance(widget, (QNodeGraphicsItemWidget, QNodeGraphicsBlockWidget)):
            widget.lmb_pressed.disconnect(self.lmb_pressed.emit)
            widget.lmb_released.disconnect(self.lmb_released.emit)

            for conn in widget.in_connections:
                super().remove_item(conn.graphics_item, self.connection_layer)
                conn.remove_connection()

            for conn in widget.out_connections:
                super().remove_item(conn.graphics_item, self.connection_layer)
                conn.remove_connection()

        return super().remove_item(item, layer)


    def add_link(self, start: QPointF, start_direction: QNodeGraphicsItemWidgetField.Connector.Type, end: QPointF, end_direction: QNodeGraphicsItemWidgetField.Connector.Type, pen: QPen) -> QNodeGraphicsItemLink:
        link = QNodeGraphicsItemLink(start, start_direction, end, end_direction)
        link.setPen(pen)
        self.add_item(link, self.connection_layer)

        return link
#----------------------------------------------------------------------
