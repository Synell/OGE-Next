#----------------------------------------------------------------------

    # Libraries
from typing import Sequence, Callable
from math import inf
from enum import Flag, StrEnum
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QMouseEvent
from .QGridFrame import QGridFrame
from .QNodeGraphicsItemLink import QNodeGraphicsItemLink
from . import QNodeGraphicsItemWidget
from .QBetterGraphicsItemWidget import QBetterGraphicsItemWidget
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsItemWidgetField(QGridFrame):
    class Color(StrEnum):
        Red = 'red'
        Green = 'green'
        Blue = 'blue'
        Yellow = 'yellow'
        Magenta = 'magenta'
        Cyan = 'cyan'



    class Connector(QGridFrame):
        class Type(Flag):
            Normal = 0
            Input = 1 << 0
            Output = 1 << 1


        lmb_pressed = Signal()
        lmb_released = Signal()

        _max_input_connections = 1
        _max_output_connections = inf


        def __init__(self, parent: 'QNodeGraphicsItemWidgetField', connection: 'QNodeGraphicsItemWidgetField.Connector.Type', color: 'QNodeGraphicsItemWidgetField.Color', types: Sequence[type]) -> None:
            super().__init__()

            self._parent = parent
            self._connection = connection
            self._types = tuple(types)
            self._connected_on_input: list[QNodeGraphicsItemWidgetField.Connection] = []
            self._connected_on_output: list[QNodeGraphicsItemWidgetField.Connection] = []

            self.setContentsMargins(0, 0, 0, 0)
            self.grid_layout.setContentsMargins(0, 0, 0, 0)
            self.grid_layout.setSpacing(0)
            self.setFixedSize(16, 16)
            self.setProperty('connector-color', color.value)

            self.setFocusPolicy(
                (Qt.FocusPolicy.StrongFocus | Qt.FocusPolicy.ClickFocus)
                    if connection != QNodeGraphicsItemWidgetField.Connector.Type.Normal
                    else Qt.FocusPolicy.NoFocus
                )

            if connection == QNodeGraphicsItemWidgetField.Connector.Type.Input:
                self.setProperty('input', True)

            if connection == QNodeGraphicsItemWidgetField.Connector.Type.Output:
                self.setProperty('output', True)

            self._connect_point = QLabel()
            self._connect_point.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._connect_point.setProperty('connector', True)
            self._connect_point.setFixedSize(8, 8)
            self.grid_layout.addWidget(self._connect_point, 0, 0, Qt.AlignmentFlag.AlignCenter)


        @property
        def parent(self) -> 'QNodeGraphicsItemWidgetField':
            return self._parent


        @property
        def connection_type(self) -> 'QNodeGraphicsItemWidgetField.Connector.Type':
            return self._connection


        @property
        def global_position(self) -> QPoint:
            half_size = QPoint(self._connect_point.size().width() // 2, self._connect_point.size().height() // 2)
            return self.mapToGlobal(self._connect_point.pos() + half_size)


        @property
        def types(self) -> Sequence[type]:
            return tuple(self._types)


        def mousePressEvent(self, event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.LeftButton and self._connection != QNodeGraphicsItemWidgetField.Connector.Type.Normal:
                self.lmb_pressed.emit()

        def mouseReleaseEvent(self, event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.LeftButton and self._connection != QNodeGraphicsItemWidgetField.Connector.Type.Normal:
                self.lmb_released.emit()


        def can_connect(self, other: 'QNodeGraphicsItemWidgetField.Connector') -> bool:
            if other.connection_type & QNodeGraphicsItemWidgetField.Connector.Type.Input and self.connection_type & QNodeGraphicsItemWidgetField.Connector.Type.Output:
                if self.is_max_output_connections_reached(): return False
                return any(issubclass(in_type, other._types) for in_type in self._types)

            if other.connection_type & QNodeGraphicsItemWidgetField.Connector.Type.Output and self.connection_type & QNodeGraphicsItemWidgetField.Connector.Type.Input:
                if self.is_max_input_connections_reached(): return False
                return any(issubclass(out_type, self._types) for out_type in other._types)

            return False


        def do_connect_on_input(self, conn: 'QNodeGraphicsItemWidgetField.Connection') -> None:
            if not self.can_connect(conn.out_connector): raise ValueError('Cannot connect')
            if conn in self._connected_on_input: raise ValueError('Input connection already exists')
            self._connected_on_input.append(conn)
            self.parent.in_connector_linked.emit(conn)

        def do_connect_on_output(self, conn: 'QNodeGraphicsItemWidgetField.Connection') -> None:
            if not self.can_connect(conn.in_connector): raise ValueError('Cannot connect')
            if conn in self._connected_on_output: raise ValueError('Output connection already exists')
            self._connected_on_output.append(conn)
            self.parent.out_connector_linked.emit(conn)


        @property
        def input_connection_count(self) -> int:
            return len(self._connected_on_input)

        @property
        def input_connections(self) -> tuple['QNodeGraphicsItemWidgetField.Connection']:
            return tuple(self._connected_on_input)

        def is_max_input_connections_reached(self) -> bool:
            return len(self._connected_on_input) >= self._max_input_connections

        def is_connected_on_input(self, obj: 'QNodeGraphicsItemWidgetField.Connection') -> bool:
            return obj in self._connected_on_input


        @property
        def output_connection_count(self) -> int:
            return len(self._connected_on_output)

        @property
        def output_connections(self) -> tuple['QNodeGraphicsItemWidgetField.Connection']:
            return tuple(self._connected_on_output)

        def is_max_output_connections_reached(self) -> bool:
            return len(self._connected_on_output) >= self._max_output_connections

        def is_connected_on_output(self, obj: 'QNodeGraphicsItemWidgetField.Connection') -> bool:
            return obj in self._connected_on_output


        def remove_connection_on_input(self, conn: 'QNodeGraphicsItemWidgetField.Connection') -> None:
            if conn not in self._connected_on_input: raise ValueError('Input connection was not found')
            self._connected_on_input.remove(conn)
            self.parent.in_connector_unlinked.emit(conn)

        def remove_connection_on_output(self, conn: 'QNodeGraphicsItemWidgetField.Connection') -> None:
            if conn not in self._connected_on_output: raise ValueError('Output connection was not found')
            self._connected_on_output.remove(conn)
            self.parent.out_connector_unlinked.emit(conn)


        @property
        def root_widget(self) -> QBetterGraphicsItemWidget | None:
            parent = self.parent
            i = 0
            while not isinstance(parent, (QBetterGraphicsItemWidget)) and (i := i + 1) < 100 and parent is not None:
                parent = parent.parent()
            return parent


    class Connection:
        def __init__(self, in_connector: 'QNodeGraphicsItemWidgetField.Connector', out_connector: 'QNodeGraphicsItemWidgetField.Connector', graphics_item: QNodeGraphicsItemLink) -> None:
            self._in_connector = in_connector
            self._out_connector = out_connector
            self._graphics_item = graphics_item

            if self._in_connector.is_max_input_connections_reached(): raise ValueError('Input connection limit reached')
            if self._out_connector.is_max_output_connections_reached(): raise ValueError('Output connection limit reached')

            in_connector.do_connect_on_input(self)
            out_connector.do_connect_on_output(self)


        @property
        def in_connector(self) -> 'QNodeGraphicsItemWidgetField.Connector':
            return self._in_connector

        @property
        def out_connector(self) -> 'QNodeGraphicsItemWidgetField.Connector':
            return self._out_connector

        @property
        def graphics_item(self) -> QNodeGraphicsItemLink:
            return self._graphics_item


        def remove_connection(self) -> None:
            self._in_connector.remove_connection_on_input(self)
            self._out_connector.remove_connection_on_output(self)


        def set_new_positions(self, in_connector: QPoint, out_connector: QPoint) -> None:
            self._graphics_item.set_all(
                in_connector,
                QNodeGraphicsItemLink.Direction.Left,
                out_connector,
                QNodeGraphicsItemLink.Direction.Right
            )



    lmb_pressed = Signal(Connector)
    lmb_released = Signal(Connector)

    in_connector_linked = Signal(Connection)
    in_connector_unlinked = Signal(Connection)

    out_connector_linked = Signal(Connection)
    out_connector_unlinked = Signal(Connection)

    data_received = Signal(object)


    def __init__(self, widget: 'QNodeGraphicsField', in_types: Sequence[type] = [], out_types: Sequence[type] = [], in_color: Color = Color.Red, out_color: Color = Color.Blue) -> None:
        super().__init__()

        self._field_type = (
            QNodeGraphicsItemWidgetField.Connector.Type.Normal | (
                QNodeGraphicsItemWidgetField.Connector.Type.Input if in_types else QNodeGraphicsItemWidgetField.Connector.Type(0)
            ) | (
                QNodeGraphicsItemWidgetField.Connector.Type.Output if out_types else QNodeGraphicsItemWidgetField.Connector.Type(0)
            )
        )

        self.setProperty('QNodeGraphicsItemWidgetField', True)
        self._root = None

        self._build(widget, in_color, out_color, in_types, out_types)


    @property
    def in_connector(self) -> Connector:
        return self._in_connector

    @property
    def out_connector(self) -> Connector:
        return self._out_connector


    @property
    def root(self) -> 'QNodeGraphicsItemWidget':
        return self._root
    
    @root.setter
    def root(self, root: 'QNodeGraphicsItemWidget') -> None:
        self._root = root


    def _build(self, widget: 'QNodeGraphicsField', in_color: Color = Color.Red, out_color: Color = Color.Blue, in_types: Sequence[type] = [], out_types: Sequence[type] = []) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(8)
        self.grid_layout.setVerticalSpacing(0)

        self._in_connector = QNodeGraphicsItemWidgetField.Connector(self, self._field_type & QNodeGraphicsItemWidgetField.Connector.Type.Input, in_color, in_types)
        self._in_connector.lmb_pressed.connect(lambda: self.lmb_pressed.emit(self._in_connector))
        self._in_connector.lmb_released.connect(lambda: self.lmb_released.emit(self._in_connector))
        self.grid_layout.addWidget(self._in_connector, 0, 0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.grid_layout.addWidget(widget, 0, 1, Qt.AlignmentFlag.AlignVCenter)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self._out_connector = QNodeGraphicsItemWidgetField.Connector(self, self._field_type & QNodeGraphicsItemWidgetField.Connector.Type.Output, out_color, out_types)
        self._out_connector.lmb_pressed.connect(lambda: self.lmb_pressed.emit(self._out_connector))
        self._out_connector.lmb_released.connect(lambda: self.lmb_released.emit(self._out_connector))
        self.grid_layout.addWidget(self._out_connector, 0, 2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)



class QNodeGraphicsField(QGridFrame):
    data_sent = Signal(object)

    in_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    in_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)

    out_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    out_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def __init_subclass__(cls) -> None:
        methods: tuple[Callable] = (
            (QNodeGraphicsField.on_data_received, cls.on_data_received),
        )
        for base_method, overriden_method in methods:
            if overriden_method is base_method:
                raise NotImplementedError(f'Class {cls.__name__} must implement method {base_method.__name__}')


    def on_data_received(self, data: object) -> None:
        pass

    def send_data(self, data: object) -> None:
        return self.data_sent.emit(data)
#----------------------------------------------------------------------
