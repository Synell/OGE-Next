#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from PySide6.QtWidgets import QGraphicsPathItem, QWidget, QStyleOptionGraphicsItem
from PySide6.QtCore import QPoint, QPointF
from PySide6.QtGui import QPainterPath, QPainter
#----------------------------------------------------------------------

    # Class
class QNodeGraphicsItemLink(QGraphicsPathItem):
    class Direction(Enum):
        Top = 0
        Bottom = 1
        Right = 2
        Left = 3


    def __init__(self, start: QPoint | QPointF, start_direction: Direction, end: QPoint | QPointF, end_direction: Direction) -> None:
        super().__init__()
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsFocusable, False)

        self._start: QPoint | QPointF = start
        self._start_direction: QNodeGraphicsItemLink.Direction = start_direction
        self._end: QPoint | QPointF = end
        self._end_direction: QNodeGraphicsItemLink.Direction = end_direction

        self._path = QPainterPath()

        self._adjust_path()


    def _adjust_path(self) -> None:
        self._path.clear()
        self._path.moveTo(self._start)
        self.setPos(QPointF(0, 0))

        star_control_point = QPointF()
        end_control_point = QPointF()

        weight = (self._end - self._start).manhattanLength() / 2.0

        match self._start_direction:
            case QNodeGraphicsItemLink.Direction.Top:
                star_control_point = QPointF(self._start.x(), self._start.y() - weight)

            case QNodeGraphicsItemLink.Direction.Bottom:
                star_control_point = QPointF(self._start.x(), self._start.y() + weight)

            case QNodeGraphicsItemLink.Direction.Right:
                star_control_point = QPointF(self._start.x() + weight, self._start.y())

            case QNodeGraphicsItemLink.Direction.Left:
                star_control_point = QPointF(self._start.x() - weight, self._start.y())

            case _:
                raise ValueError('Invalid start direction')

        match self._end_direction:
            case QNodeGraphicsItemLink.Direction.Top:
                end_control_point = QPointF(self._end.x(), self._end.y() - weight)

            case QNodeGraphicsItemLink.Direction.Bottom:
                end_control_point = QPointF(self._end.x(), self._end.y() + weight)

            case QNodeGraphicsItemLink.Direction.Right:
                end_control_point = QPointF(self._end.x() + weight, self._end.y())

            case QNodeGraphicsItemLink.Direction.Left:
                end_control_point = QPointF(self._end.x() - weight, self._end.y())

            case _:
                raise ValueError('Invalid end direction')

        self._path.cubicTo(
            star_control_point,
            end_control_point,
            self._end
        )

        self.setPath(self._path)


    @property
    def start(self) -> QPoint | QPointF:
        return self._start

    @start.setter
    def start(self, start: QPoint | QPointF) -> None:
        self._start = start
        self._adjust_path()


    @property
    def start_direction(self) -> 'QNodeGraphicsItemLink.Direction':
        return self._start_direction

    @start_direction.setter
    def start_direction(self, start_direction: 'QNodeGraphicsItemLink.Direction') -> None:
        self._start_direction = start_direction
        self._adjust_path()


    @property
    def end(self) -> QPoint | QPointF:
        return self._end

    @end.setter
    def end(self, end: QPoint | QPointF) -> None:
        self._end = end
        self._adjust_path()


    @property
    def end_direction(self) -> 'QNodeGraphicsItemLink.Direction':
        return self._end_direction

    @end_direction.setter
    def end_direction(self, end_direction: 'QNodeGraphicsItemLink.Direction') -> None:
        self._end_direction = end_direction
        self._adjust_path()


    def set_positions(self, start: QPoint | QPointF, end: QPoint | QPointF) -> None:
        self._start = start
        self._end = end
        self._adjust_path()


    def set_directions(self, start_direction: 'QNodeGraphicsItemLink.Direction', end_direction: 'QNodeGraphicsItemLink.Direction') -> None:
        self._start_direction = start_direction
        self._end_direction = end_direction
        self._adjust_path()


    def set_all(self, start: QPoint | QPointF, start_direction: 'QNodeGraphicsItemLink.Direction', end: QPoint | QPointF, end_direction: 'QNodeGraphicsItemLink.Direction') -> None:
        self._start = start
        self._start_direction = start_direction
        self._end = end
        self._end_direction = end_direction
        self._adjust_path()


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        self.setPos(QPointF(0, 0))
        return super().paint(painter, option, widget)
#----------------------------------------------------------------------
