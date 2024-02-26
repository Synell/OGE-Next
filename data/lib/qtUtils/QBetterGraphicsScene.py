#----------------------------------------------------------------------

    # Libraries
from typing import Sequence
from math import inf
from PySide6.QtCore import QPoint, Qt, QRect, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QPixmap, QImage, QPainterPath, QPolygon, QPolygonF
from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsPathItem, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsSimpleTextItem, QGraphicsItemGroup, QStyleOptionGraphicsItem, QGraphicsProxyWidget, QWidget, QGraphicsView
from .QBetterGraphicsLayer import QBetterGraphicsLayer
from .QBetterGraphicsItemWidget import QBetterGraphicsItemWidget
#----------------------------------------------------------------------

    # Class
class QBetterGraphicsScene(QGraphicsScene):
    def __init__(self, parent: QGraphicsView, size: QRect) -> None:
        super().__init__(size.x(), size.y(), size.width(), size.height())

        self._parent = parent
        self._layers: dict[int, QBetterGraphicsLayer] = {
            0: QBetterGraphicsLayer(0)
        }


    @property
    def parent(self) -> QGraphicsView:
        return self._parent


    @property
    def layers(self) -> dict[int, QBetterGraphicsLayer]:
        return self._layers.copy()


    @property
    def top_layer(self) -> QBetterGraphicsLayer:
        return self._layers[max(k for k in self._layers.keys() if k != inf)]


    @property
    def bottom_layer(self) -> QBetterGraphicsLayer:
        return self._layers[min(self._layers.keys())]


    def get_layer(self, id: int) -> QBetterGraphicsLayer:
        return self._layers[id]


    def items_at(self, pos: QPoint) -> list[QGraphicsItem | QBetterGraphicsItemWidget]:
        items = self.items(pos, Qt.ItemSelectionMode.ContainsItemBoundingRect, Qt.SortOrder.AscendingOrder)
        return [item for item in items if item.isVisible()]


    def items_in(self, rect: QRect) -> list[QGraphicsItem | QBetterGraphicsItemWidget]:
        items = self.items(rect, Qt.ItemSelectionMode.IntersectsItemShape, Qt.SortOrder.AscendingOrder)
        return [item for item in items if item.isVisible()]


    def add_item(self, item: QGraphicsItem | QBetterGraphicsItemWidget, layer: int = 0) -> QGraphicsItem | QGraphicsProxyWidget:
        if layer not in self._layers: raise ValueError(f'Layer with id {layer} does not exist')

        if isinstance(item, QWidget) and not isinstance(item, QBetterGraphicsItemWidget): raise ValueError('Use a QBetterGraphicsItemWidget instead of a QWidget')

        if isinstance(item, QBetterGraphicsItemWidget):
            proxy = self.addWidget(item)
            self._layers[layer].add_item(proxy)
            return proxy

        self._layers[layer].add_item(item)

        return item

    def addItem(self, item: QGraphicsItem | QBetterGraphicsItemWidget) -> QGraphicsItem | QGraphicsProxyWidget:
        return self.add_item(item)


    def add_ellipse(self, x: int, y: int, width: int, height: int, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsEllipseItem:
        item = super().addEllipse(x, y, width, height, pen, brush)
        self.add_item(item, layer)
        return item

    def addEllipse(self, x: int, y: int, width: int, height: int, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsEllipseItem:
        return self.add_ellipse(x, y, width, height, pen, brush, layer)


    def add_rect(self, x: int, y: int, width: int, height: int, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsRectItem:
        item = super().addRect(x, y, width, height, pen, brush)
        self.add_item(item, layer)
        return item

    def addRect(self, x: int, y: int, width: int, height: int, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsRectItem:
        return self.add_rect(x, y, width, height, pen, brush, layer)


    def add_text(self, text: str, font: QFont | str | Sequence[str], layer: int = 0) -> QGraphicsTextItem:
        item = super().addText(text)
        if isinstance(font, (str, Sequence)): item.setFont(QFont(*font))
        else: item.setFont(font)
        self.add_item(item, layer)
        return item

    def addText(self, text: str, font: QFont | str | Sequence[str], layer: int = 0) -> QGraphicsTextItem:
        return self.add_text(text, font, layer)


    def add_pixmap(self, pixmap: QPixmap | QImage | str, layer: int = 0) -> QGraphicsPixmapItem:
        item = super().addPixmap(pixmap)
        self.add_item(item, layer)
        return item

    def addPixmap(self, pixmap: QPixmap | QImage | str, layer: int = 0) -> QGraphicsPixmapItem:
        return self.add_pixmap(pixmap, layer)


    def add_path(self, path: QPainterPath, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsPathItem:
        item = super().addPath(path, pen, brush)
        self.add_item(item, layer)
        return item

    def addPath(self, path: QPainterPath, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsPathItem:
        return self.add_path(path, pen, brush, layer)


    def add_line(self, x1: int, y1: int, x2: int, y2: int, pen: QPen, layer: int = 0) -> QGraphicsLineItem:
        item = super().addLine(x1, y1, x2, y2, pen)
        self.add_item(item, layer)
        return item

    def addLine(self, x1: int, y1: int, x2: int, y2: int, pen: QPen, layer: int = 0) -> QGraphicsLineItem:
        return self.add_line(x1, y1, x2, y2, pen, layer)


    def add_polygon(self, polygon: QPolygon | QPolygonF, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsPolygonItem:
        item = super().addPolygon(polygon, pen, brush)
        self.add_item(item, layer)
        return item

    def addPolygon(self, polygon: QPolygon | QPolygonF, pen: QPen, brush: QBrush, layer: int = 0) -> QGraphicsPolygonItem:
        return self.add_polygon(polygon, pen, brush, layer)


    def add_simple_text(self, text: str, font: QFont | str | Sequence[str], layer: int = 0) -> QGraphicsSimpleTextItem:
        item = super().addSimpleText(text)
        if isinstance(font, (str, Sequence)): item.setFont(QFont(*font))
        else: item.setFont(font)
        self.add_item(item, layer)
        return item

    def addSimpleText(self, text: str, font: QFont | str | Sequence[str], layer: int = 0) -> QGraphicsSimpleTextItem:
        return self.add_simple_text(text, font, layer)


    def add_group(self, items: list[QGraphicsItem], layer: int = 0) -> QGraphicsItemGroup:
        item = super().createItemGroup(items)
        self.add_item(item, layer)
        return item

    def addGroup(self, items: list[QGraphicsItem], layer: int = 0) -> QGraphicsItemGroup:
        return self.add_group(items, layer)


    def remove_item(self, item: QGraphicsItem | QBetterGraphicsItemWidget, layer: int = 0) -> None:
        if layer not in self._layers: raise ValueError(f'Layer with id {layer} does not exist')

        self._layers[layer].remove_item(item)
        if item.scene() == self: super().removeItem(item)

    def removeItem(self, item: QGraphicsItem | QBetterGraphicsItemWidget, layer: int = 0) -> None:
        self.remove_item(item, layer)


    def clear_items(self, layer: int = 0) -> None:
        if layer not in self._layers: raise ValueError(f'Layer with id {layer} does not exist')
        for item in self._layers[layer].items:
            self.remove_item(item, layer)


    def clear(self) -> None:
        self.remove_all_items()
        for layer in list(self._layers.keys()):
            self.remove_layer(layer)


    def remove_all_items(self) -> None:
        for layer in self._layers.values():
            for item in layer.items:
                self.remove_item(item, layer.id)


    def add_layer(self, id: int) -> None:
        if id in self._layers: raise ValueError(f'Layer with id {id} already exists')
        self._layers[id] = QBetterGraphicsLayer(id)


    def remove_layer(self, id: int) -> None:
        if id not in self._layers: raise ValueError(f'Layer with id {id} does not exist')
        del self._layers[id]


    def drawBackground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        pass


    def drawForeground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        layers = sorted(self._layers.values(), key = lambda layer: layer.id)
        layers = [layer for layer in layers if layer.is_visible]

        for layer in layers:
            for item in layer.items:
                if rect.intersected(item.boundingRect()):
                    item.paint(painter, QStyleOptionGraphicsItem(), None)

        self.update(rect)
#----------------------------------------------------------------------
