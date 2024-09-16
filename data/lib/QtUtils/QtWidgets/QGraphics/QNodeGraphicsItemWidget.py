#----------------------------------------------------------------------

    # Libraries
from typing import Sequence
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .. import QGridFrame, QBetterGraphicsItemWidget
from ...QtGui import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsItemWidget(QBetterGraphicsItemWidget):
    lmb_pressed = Signal(QNodeGraphicsItemWidgetField.Connector)
    lmb_released = Signal(QNodeGraphicsItemWidgetField.Connector)

    in_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    in_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)

    out_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    out_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)


    def __init__(self, name: str, color: QUtilsColor, fields: Sequence[QNodeGraphicsItemWidgetField] = []) -> None:
        self._name = name
        self._color = color

        widget = QGridFrame()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.layout_.setContentsMargins(0, 0, 0, 2)
        widget.layout_.setHorizontalSpacing(0)
        widget.layout_.setVerticalSpacing(4)
        super().__init__(widget)

        self.setProperty('QNodeGraphicsItemWidget', True)

        if name:
            title_container = QGridFrame()
            title_container.setProperty('QNodeGraphicsItemWidgetTitle', True)
            title_container.layout_.setContentsMargins(0, 2, 0, 2)
            title_container.layout_.setHorizontalSpacing(0)
            title_container.layout_.setVerticalSpacing(0)
            title_container.setStyleSheet(f'background-color: {color.hex};')
            widget.layout_.addWidget(title_container, 0, 0)

            title = QLabel(name)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_container.layout_.addWidget(title, 0, 0)

        self._fields = fields
        for field in fields:
            field.root = self
            widget.layout_.addWidget(field, widget.layout_.rowCount(), 0)

            field.lmb_pressed.connect(self.lmb_pressed.emit)
            field.lmb_released.connect(self.lmb_released.emit)

            field.in_connector_linked.connect(self.in_connector_linked.emit)
            field.in_connector_unlinked.connect(self.in_connector_unlinked.emit)

            field.out_connector_linked.connect(self.out_connector_linked.emit)
            field.out_connector_unlinked.connect(self.out_connector_unlinked.emit)


    @property
    def fields(self) -> tuple[QNodeGraphicsItemWidgetField]:
        return tuple(self._fields)


    @property
    def in_connectors(self) -> tuple[QNodeGraphicsItemWidgetField.Connector]:
        return tuple(field.in_connector for field in self._fields if field.in_connector.input_connection_count > 0)

    @property
    def in_connections(self) -> tuple[QNodeGraphicsItemWidgetField.Connection]:
        return tuple(connection for field in self._fields for connection in field.in_connector.input_connections)

    @property
    def in_widgets(self) -> tuple[QBetterGraphicsItemWidget]:
        return tuple(connection.in_connector.root_widget for connection in self.in_connections)


    @property
    def out_connectors(self) -> tuple[QNodeGraphicsItemWidgetField.Connector]:
        return tuple(field.out_connector for field in self._fields if field.out_connector.output_connection_count > 0)

    @property
    def out_connections(self) -> tuple[QNodeGraphicsItemWidgetField.Connection]:
        return tuple(connection for field in self._fields for connection in field.out_connector.output_connections)

    @property
    def out_widgets(self) -> tuple[QBetterGraphicsItemWidget]:
        return tuple(connection.out_connector.root_widget for connection in self.out_connections)
#----------------------------------------------------------------------
