#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QRect, Signal, QPoint
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QGraphicsView
from .QBetterGraphicsItemWidget import QBetterGraphicsItemWidget
from .QBetterGraphicsScene import QBetterGraphicsScene
from .QNodeGraphicsItemWidget import QNodeGraphicsItemWidget
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .QNodeGraphicsItemLink import QNodeGraphicsItemLink
from .QNodeGraphicsBlockWidget import QNodeGraphicsBlockWidget
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
            item.lmb_pressed.connect(self.lmb_pressed)
            item.lmb_released.connect(self.lmb_released)

        return ret


    def add_link(self, start: QPoint, start_direction: QNodeGraphicsItemWidgetField.Connector.Type, end: QPoint, end_direction: QNodeGraphicsItemWidgetField.Connector.Type, pen: QPen) -> QNodeGraphicsItemLink:
        link = QNodeGraphicsItemLink(start, start_direction, end, end_direction)
        link.setPen(pen)
        self.add_item(link, self.connection_layer)

        return link
#----------------------------------------------------------------------
