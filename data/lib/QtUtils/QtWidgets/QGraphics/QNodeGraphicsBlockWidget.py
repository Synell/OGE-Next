#----------------------------------------------------------------------

    # Libraries
from typing import Sequence
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .. import QGridFrame, QBetterGraphicsItemWidget
from ...QtGui import QUtilsColor
from . import QNodeGraphicsItemWidgetBlock
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsBlockWidget(QBetterGraphicsItemWidget):
    lmb_pressed = Signal(QNodeGraphicsItemWidgetField.Connector)
    lmb_released = Signal(QNodeGraphicsItemWidgetField.Connector)

    in_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    in_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)

    out_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    out_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)


    def __init__(self, name: str, color: QUtilsColor, widget_block: QNodeGraphicsItemWidgetBlock) -> None:
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

        self._widget_block = widget_block

        widget_block.root = self
        widget.layout_.addWidget(widget_block, widget.layout_.rowCount(), 0)

        widget_block.lmb_pressed.connect(self.lmb_pressed)
        widget_block.lmb_released.connect(self.lmb_released)

        widget_block.in_connector_linked.connect(self.in_connector_linked)
        widget_block.in_connector_unlinked.connect(self.in_connector_unlinked)

        widget_block.out_connector_linked.connect(self.out_connector_linked)
        widget_block.out_connector_unlinked.connect(self.out_connector_unlinked)


    @property
    def widget_block(self) -> QNodeGraphicsItemWidgetBlock:
        return self._widget_block


    @property
    def in_connections(self) -> Sequence[QNodeGraphicsItemWidgetField.Connection]:
        return self._widget_block.in_connections

    @property
    def out_connections(self) -> Sequence[QNodeGraphicsItemWidgetField.Connection]:
        return self._widget_block.out_connections
#----------------------------------------------------------------------
