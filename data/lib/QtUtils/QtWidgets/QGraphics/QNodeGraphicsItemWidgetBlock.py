#----------------------------------------------------------------------

    # Libraries
from typing import Sequence
from PySide6.QtWidgets import QSizePolicy, QWidget
from PySide6.QtCore import Qt, Signal
from .QNodeGraphicsItemWidgetField import QNodeGraphicsItemWidgetField
from .. import QGridFrame
from . import QNodeGraphicsBlockWidget
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsItemWidgetBlock(QGridFrame):
    data_sent = Signal(object)
    data_received = Signal(object)

    lmb_pressed = Signal(QNodeGraphicsItemWidgetField.Connector)
    lmb_released = Signal(QNodeGraphicsItemWidgetField.Connector)

    in_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    in_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)

    out_connector_linked = Signal(QNodeGraphicsItemWidgetField.Connection)
    out_connector_unlinked = Signal(QNodeGraphicsItemWidgetField.Connection)

    def __init__(self, middle_widget: QWidget, in_types: Sequence[Sequence[type]] = [], in_colors: Sequence[QNodeGraphicsItemWidgetField.Color] = [], out_types: Sequence[Sequence[type]] = [], out_colors: Sequence[QNodeGraphicsItemWidgetField.Color] = []) -> None:
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setHorizontalSpacing(8)
        self.layout_.setVerticalSpacing(0)

        self._left_widget = QGridFrame()
        self._left_widget.setContentsMargins(0, 0, 0, 0)
        self._left_widget.layout_.setContentsMargins(0, 0, 0, 0)
        self._left_widget.layout_.setSpacing(0)
        self.layout_.addWidget(self._left_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._left_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._left_widget.setFixedWidth(32)
        self._left_widget.setProperty('QNodeGraphicsItemWidgetField', True)

        send_param_lm_pressed = lambda connector: lambda: self.lmb_pressed.emit(connector)
        send_param_lm_released = lambda connector: lambda: self.lmb_released.emit(connector)

        self._in_connectors: list[QNodeGraphicsItemWidgetField.Connector] = []

        for i, in_type in enumerate(in_types):
            connector = QNodeGraphicsItemWidgetField.Connector(self, QNodeGraphicsItemWidgetField.Connector.Type.Input, in_colors[i], in_type)
            connector.lmb_pressed.connect(send_param_lm_pressed(connector))
            connector.lmb_released.connect(send_param_lm_released(connector))
            self._left_widget.layout_.addWidget(connector, i, 0, Qt.AlignmentFlag.AlignLeft)
            self._in_connectors.append(connector)

        self._middle_widget = middle_widget
        self._middle_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_.addWidget(self._middle_widget, 0, 1, Qt.AlignmentFlag.AlignVCenter)

        self._right_widget = QGridFrame()
        self._right_widget.setContentsMargins(0, 0, 0, 0)
        self._right_widget.layout_.setContentsMargins(0, 0, 0, 0)
        self._right_widget.layout_.setSpacing(0)
        self.layout_.addWidget(self._right_widget, 0, 2, Qt.AlignmentFlag.AlignRight)
        self._right_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._right_widget.setFixedWidth(32)
        self._right_widget.setProperty('QNodeGraphicsItemWidgetField', True)

        self._out_connectors: list[QNodeGraphicsItemWidgetField.Connector] = []

        for i, out_type in enumerate(out_types):
            connector = QNodeGraphicsItemWidgetField.Connector(self, QNodeGraphicsItemWidgetField.Connector.Type.Output, out_colors[i], out_type)
            connector.lmb_pressed.connect(send_param_lm_pressed(connector))
            connector.lmb_released.connect(send_param_lm_released(connector))
            self._right_widget.layout_.addWidget(connector, i, 0, Qt.AlignmentFlag.AlignRight)
            self._out_connectors.append(connector)

        self._root = None


    @property
    def root(self) -> QNodeGraphicsBlockWidget:
        return self._root

    @root.setter
    def root(self, root: QNodeGraphicsBlockWidget) -> None:
        self._root = root


    @property
    def in_connectors(self) -> tuple[QNodeGraphicsItemWidgetField.Connector]:
        return tuple(self._in_connectors)

    @property
    def out_connectors(self) -> tuple[QNodeGraphicsItemWidgetField.Connector]:
        return tuple(self._out_connectors)

    @property
    def in_connections(self) -> Sequence[QNodeGraphicsItemWidgetField.Connection]:
        return [conn for connector in self._in_connectors for conn in connector.input_connections]
    
    @property
    def out_connections(self) -> Sequence[QNodeGraphicsItemWidgetField.Connection]:
        return [conn for connector in self._out_connectors for conn in connector.output_connections]
#----------------------------------------------------------------------
