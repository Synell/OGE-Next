#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget
from PySide6.QtCore import QPoint, Qt, QRect, QPointF
from PySide6.QtGui import QMouseEvent, QPen
from .QBetterGraphicsView import QBetterGraphicsView
from .QNodeGraphicsScene import QNodeGraphicsScene
from .QNodeGraphicsItemWidget import QNodeGraphicsItemWidget
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .QUtilsColor import QUtilsColor
from .QNodeGraphicsItemLink import QNodeGraphicsItemLink
from .QNodeGraphicsBlockWidget import QNodeGraphicsBlockWidget
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsView(QBetterGraphicsView):
    _connection_pen = QPen(QUtilsColor.from_hexa('#ffffff55').QColorAlpha, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)


    def __init__(self, size: QRect) -> None:
        super().__init__(size, QNodeGraphicsScene)
        self._scene: QNodeGraphicsScene

        self._scene.lmb_pressed.connect(self._on_node_lmb_pressed)

        self._current_connection: QNodeGraphicsItemLink = None
        self._current_connector: QNodeGraphicsItemWidgetField.Connector = None
        self._valid_connector: QNodeGraphicsItemWidgetField.Connector = None


    def _on_node_lmb_pressed(self, connector: QNodeGraphicsItemWidgetField.Connector) -> None:
        pos = self._fix_position(connector.global_position)

        conn = None
        if connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input:
            conn = connector.input_connections[0] if connector.input_connections else None

        if conn:
            self._current_connection = conn.graphics_item
            self._current_connector = conn.out_connector

            conn.remove_connection()

        else:
            self._current_connection = self._scene.add_link(
                pos,
                QNodeGraphicsItemLink.Direction.Left if connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else QNodeGraphicsItemLink.Direction.Right,
                pos,
                QNodeGraphicsItemLink.Direction.Right if connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else QNodeGraphicsItemLink.Direction.Left,
                self._connection_pen,
            )
            self._current_connector = connector


    def _mouse_move_event_connection(self, event: QMouseEvent, pos: QPointF) -> None:
        scene_items = [item for item in self._scene.items_at(pos) if isinstance(item, QGraphicsProxyWidget)]
        items: list[QNodeGraphicsItemWidget | QNodeGraphicsBlockWidget] = [
            item.widget() for item in scene_items
                if isinstance(item.widget(), (QNodeGraphicsItemWidget, QNodeGraphicsBlockWidget)) and item.widget() != self._current_connector.root_widget
        ]

        goal_type = QNodeGraphicsItemWidgetField.Connector.Type.Input if self._current_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Output else QNodeGraphicsItemWidgetField.Connector.Type.Output
        if isinstance(self._current_connector.parent, QNodeGraphicsBlockWidget):
            get_connector = lambda field_: field_.widget_block._left_widget if goal_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else field_.widget_block._right_widget
        get_connector = lambda field_: field_.in_connector if goal_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else field_.out_connector

        self._valid_connector = None
        for item in items:
            if isinstance(item, QNodeGraphicsItemWidget):
                for field in item.fields:
                    conn: QNodeGraphicsItemWidgetField.Connector = get_connector(field)

                    if conn.connection_type == goal_type:
                        half_size = QPoint(conn.size().width() // 2, conn.size().height() // 2)
                        rect = QRect(
                            self._fix_position(conn.global_position).toPoint() - half_size,
                            self._fix_position(conn.global_position).toPoint() + half_size
                        )

                        if rect.contains(pos.toPoint()) and self._current_connector.can_connect(conn) and conn.can_connect(self._current_connector):
                            self._valid_connector = conn
                            break

            elif isinstance(item, QNodeGraphicsBlockWidget):
                connectors = item.widget_block.in_connectors if goal_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else item.widget_block.out_connectors
                for conn in connectors:
                    half_size = QPoint(conn.size().width() // 2, conn.size().height() // 2)
                    rect = QRect(
                        self._fix_position(conn.global_position).toPoint() - half_size,
                        self._fix_position(conn.global_position).toPoint() + half_size
                    )

                    if rect.contains(pos.toPoint()) and self._current_connector.can_connect(conn) and conn.can_connect(self._current_connector):
                        self._valid_connector = conn
                        break

        if self._valid_connector:
            pos = self._fix_position(self._valid_connector.global_position)

        connector_pos = self._fix_position(self._current_connector.global_position)
        self._current_connection.set_all(
            connector_pos,
            QNodeGraphicsItemLink.Direction.Left if self._current_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else QNodeGraphicsItemLink.Direction.Right,
            pos,
            QNodeGraphicsItemLink.Direction.Right if self._current_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else QNodeGraphicsItemLink.Direction.Left
        )


    def _fix_position(self, pos: QPointF) -> QPointF:
        return self.mapToScene(self.mapFromGlobal(pos))


    def _update_connection_positions(self, conn: QNodeGraphicsItemWidgetField.Connection) -> None:
        conn.set_new_positions(
            self._fix_position(conn.in_connector.global_position),
            self._fix_position(conn.out_connector.global_position)
        )

    def _update_connections(self) -> None:
        if not self._selection_box_item:
            for item in self._selected_items:
                if not isinstance(item.item, QGraphicsProxyWidget): continue

                if isinstance(item.item.widget(), QNodeGraphicsItemWidget):
                    w: QNodeGraphicsItemWidget = item.item.widget()
                    for field in w.fields:
                        for conn in field.in_connector.input_connections: self._update_connection_positions(conn)
                        for conn in field.out_connector.output_connections: self._update_connection_positions(conn)

                elif isinstance(item.item.widget(), QNodeGraphicsBlockWidget):
                    w: QNodeGraphicsBlockWidget = item.item.widget()
                    for conn in w.widget_block.in_connectors:
                        for c in conn.input_connections: self._update_connection_positions(c)

                    for conn in w.widget_block.out_connectors:
                        for c in conn.output_connections: self._update_connection_positions(c)


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.pos())
        if self._current_connection: self._mouse_move_event_connection(event, pos)

        if event.buttons() & Qt.MouseButton.LeftButton:
            self._update_connections()

        return super().mouseMoveEvent(event)


    def _mouse_release_event_connection(self, event: QMouseEvent, pos: QPointF) -> None:
        if self._valid_connector:
            in_connector = self._current_connector if self._current_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else self._valid_connector
            out_connector = self._current_connector if self._current_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Output else self._valid_connector

            try:
                QNodeGraphicsItemWidgetField.Connection(
                    in_connector,
                    out_connector,
                    self._current_connection
                )

            except Exception:
                self._scene.remove_item(self._current_connection, self._scene.connection_layer)

        else:
            self._scene.remove_item(self._current_connection, self._scene.connection_layer)

        self._current_connection = None
        self._current_connector = None
        self._valid_connector = None


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.pos())
        if self._current_connection: self._mouse_release_event_connection(event, pos)

        if event.button() == Qt.MouseButton.LeftButton:
            self._update_connections()

        return super().mouseReleaseEvent(event)


    def connect_nodes(self, in_connector: QNodeGraphicsItemWidgetField.Connector, out_connector: QNodeGraphicsItemWidgetField.Connector) -> None:
        QNodeGraphicsItemWidgetField.Connection(
            in_connector,
            out_connector,
            self._scene.add_link(
                self._fix_position(in_connector.global_position),
                QNodeGraphicsItemLink.Direction.Left if in_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Input else QNodeGraphicsItemLink.Direction.Right,
                self._fix_position(out_connector.global_position),
                QNodeGraphicsItemLink.Direction.Right if out_connector.connection_type == QNodeGraphicsItemWidgetField.Connector.Type.Output else QNodeGraphicsItemLink.Direction.Left,
                self._connection_pen
            )
        )


    def set_scale(self, scale: float) -> None:
        self.scale(scale, scale)
#----------------------------------------------------------------------
