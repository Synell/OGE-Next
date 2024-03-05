#----------------------------------------------------------------------

    # Libraries
from math import inf
from PySide6.QtWidgets import QGraphicsView, QGraphicsItem, QGraphicsProxyWidget
from PySide6.QtCore import QPoint, QPointF, Qt, Signal, QRect
from PySide6.QtGui import QMouseEvent, QPainter, QWheelEvent, QPen, QBrush, QInputEvent
from .QBetterGraphicsScene import QBetterGraphicsScene
from ..QtGui import QUtilsColor, QssSelector
from ..QtCore import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QBetterGraphicsView(QGraphicsView):
    class SelectedItem:
        def __init__(self, item: QGraphicsItem | QGraphicsProxyWidget, offset: QPointF) -> None:
            self._item: QGraphicsItem | QGraphicsProxyWidget = item
            self._offset: QPointF = offset

        @property
        def item(self) -> QGraphicsItem | QGraphicsProxyWidget:
            return self._item

        @property
        def offset(self) -> QPointF:
            return self._offset

        @offset.setter
        def offset(self, value: QPointF) -> None:
            self._offset = value



    _SCALE_FACTOR = 1.0015
    _SELECTION_BOX_LAYER = inf


    _selection_color: QUtilsColor = QUtilsColor.from_ahex('#550094FF')


    mouse_pressed = Signal(int, int, Qt.MouseButton)
    mouse_position_changed = Signal(int, int, Qt.MouseButton)
    mouse_released = Signal(int, int, Qt.MouseButton)
    scale_changed = Signal(float)


    @staticmethod
    def init(app: QBaseApplication) -> None:
        QBetterGraphicsView._selection_color = QUtilsColor.from_ahex(
            app.qss.search(
                QssSelector(widget = 'QWidget', attributes = {'QBetterGraphicsView': True, 'selection': True})
            )['color']
        )


    def __init__(self, size: QRect, scene_cls: type[QBetterGraphicsScene] = QBetterGraphicsScene) -> None:
        if not issubclass(scene_cls, QBetterGraphicsScene): raise TypeError('scene_cls must be a subclass of QBetterGraphicsScene')
        self._scene = scene_cls(self, size)
        self._selected_items: list[QBetterGraphicsView.SelectedItem] = []

        super().__init__(self._scene)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

        self._current_scale = 1.0

        self._drag_mouse_origin = QPoint()
        self._move_mouse_origin = QPoint()
        self._move_mouse_origin_scene = QPointF()

        self._selection_box_origin = None
        self._selection_box_item = None
        self._scene.add_layer(self._SELECTION_BOX_LAYER)


    @property
    def scene(self) -> QBetterGraphicsScene:
        return self._scene


    @property
    def current_scale(self) -> float:
        return self._current_scale


    def items_at(self, pos: QPointF) -> list[QGraphicsItem]:
        return [item for item in self._scene.items_at(pos)]


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.MiddleButton:
            self._drag_mouse_origin = event.pos()
            self.viewport().setCursor(Qt.CursorShape.SizeAllCursor)

        else:
            super().mousePressEvent(event)

        pos = self.mapToScene(event.pos())
        self.mouse_pressed.emit(pos.x(), pos.y(), event.buttons())

        if event.buttons() & Qt.MouseButton.LeftButton:
            items = self.items_at(pos)
            widgets = [item.widget().focusWidget() for item in items if isinstance(item, QGraphicsProxyWidget)]
            focus = any(not (w.property('fake-focus')) for w in widgets if w)
            old_items = [item.item for item in self._selected_items]

            if items and not focus:
                if any(item in old_items for item in items):
                    for item in self._selected_items:
                        item.offset = item.item.pos() - pos
                    return

                self._set_selected(False)
                self._selected_items = [QBetterGraphicsView.SelectedItem(items[-1], items[-1].pos() - pos)]
                self._set_selected(True)
                return

            self._set_selected(False)
            self._selected_items.clear()

            if not items:
                self._selection_box_origin = pos

                pen = QPen(self._selection_color.QColor)
                pen.setWidth(2)
                pen.setCosmetic(True)
                pen.setDashPattern([2.0, 4.0])

                brush = QBrush(self._selection_color.QColorAlpha)

                self._selection_box_item = self._scene.addRect(pos.x(), pos.y(), 0, 0, pen, brush, self._SELECTION_BOX_LAYER)


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.pos())
        self.mouse_position_changed.emit(pos.x(), pos.y(), event.buttons())

        self._move_mouse_origin = event.pos()
        self._move_mouse_origin_scene = pos

        if event.buttons() & Qt.MouseButton.MiddleButton:
            if self._drag_mouse_origin:
                old_drag_pos = self.mapToScene(self._drag_mouse_origin)
                delta = pos - old_drag_pos
                self.translate(delta.x(), delta.y())
                self._drag_mouse_origin = event.pos()
                self._move_mouse_origin_scene = pos

        else:
            super().mouseMoveEvent(event)


        if event.buttons() & Qt.MouseButton.LeftButton:
            if self._selection_box_item:
                if self.viewport().cursor().shape() != Qt.CursorShape.CrossCursor:
                    self.viewport().setCursor(Qt.CursorShape.CrossCursor)

                x = min(self._selection_box_origin.x(), pos.x())
                y = min(self._selection_box_origin.y(), pos.y())
                width = abs(self._selection_box_origin.x() - pos.x())
                height = abs(self._selection_box_origin.y() - pos.y())

                self._selection_box_item.setRect(x, y, width, height)

                items = self._scene.items_in(self._selection_box_item.rect())
                self._set_selected(False)
                self._selected_items = [QBetterGraphicsView.SelectedItem(item, item.pos() - pos) for item in items]
                self._set_selected(True)

            else:
                for item in self._selected_items:
                    item.item.setPos(pos + item.offset)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

        else:
            super().mouseReleaseEvent(event)

        pos = self.mapToScene(event.pos())
        self.mouse_released.emit(pos.x(), pos.y(), event.button())

        if event.button() == Qt.MouseButton.LeftButton:
            if self._selection_box_item:
                self._selection_box_origin = None
                self._selection_box_item = None

                self._scene.clear_items(self._SELECTION_BOX_LAYER)

                self.viewport().setCursor(Qt.CursorShape.ArrowCursor)


    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & (Qt.KeyboardModifier.ShiftModifier):
            self._move_mouse_origin = event.position().toPoint()
            self._move_mouse_origin_scene = self.mapToScene(self._move_mouse_origin)
            self.mouse_position_changed.emit(event.scenePosition().x(), event.scenePosition().y(), event.buttons())

            delta = event.angleDelta()
            self.translate(delta.x(), delta.y())
            return

        self._zoom_event(event)


    def _zoom_event(self, event: QWheelEvent) -> None:
        factor = pow(self._SCALE_FACTOR, event.angleDelta().y())
        self._current_scale *= factor

        self.scale(factor, factor)
        self.centerOn(self._move_mouse_origin_scene)

        delta_viewport_pos = self._move_mouse_origin.toPointF() - QPointF(self.viewport().width() / 2.0, self.viewport().height() / 2.0)
        viewport_center = self.mapFromScene(self._move_mouse_origin_scene) - delta_viewport_pos.toPoint()
        self.centerOn(self.mapToScene(viewport_center))

        self.scale_changed.emit(factor)


    def keyPressEvent(self, event: QInputEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            for item in self._selected_items:
                self._scene.remove_item(item.item)

            self._selected_items.clear()

        else:
            super().keyPressEvent(event)


    def _set_selected(self, selected: bool) -> None:
        for item in self._selected_items:
            if isinstance(item.item, QGraphicsProxyWidget):
                item.item.widget().selected = selected
#----------------------------------------------------------------------
