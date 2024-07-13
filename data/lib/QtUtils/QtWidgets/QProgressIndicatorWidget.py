#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from .QProgressIndicator import QProgressIndicator, QProgressIndicatorItem
from .QSlidingStackedWidget import QSlidingStackedWidget
from .QGridWidget import QGridWidget
from ..QtCore.QDirection import QDirection
#----------------------------------------------------------------------

    # Class
class QProgressIndicatorWidget(QWidget):
    def __init__(
        self,
        parent = None,
        progress_direction: QDirection = QDirection.Left2Right,
        compact: bool = True,
        progress_content_margins: tuple = (16, 16, 16, 16),
        direction: QSlidingStackedWidget.Direction = QSlidingStackedWidget.Direction.Bottom2Top,
        content_margins: tuple = (16, 16, 16, 16)
    ) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._direction = direction

        self._progress_indicator = QProgressIndicator(self, progress_direction, compact, progress_content_margins)
        match progress_direction:
            case QDirection.Left2Right:
                self._progress_indicator.setProperty('border-bottom', True)

            case QDirection.Right2Left:
                self._progress_indicator.setProperty('border-bottom', True)

            case QDirection.Top2Bottom:
                self._progress_indicator.setProperty('border-right', True)

            case QDirection.Bottom2Top:
                self._progress_indicator.setProperty('border-right', True)

        w = QGridWidget()
        w.layout_.setSpacing(0)
        w.layout_.setContentsMargins(*content_margins)

        self._widget = QSlidingStackedWidget()
        self._widget.set_orientation(Qt.Orientation.Vertical)
        w.layout_.addWidget(self._widget, 0, 0)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._progress_indicator, 0, 0)
        self._layout.addWidget(w, 0, 1)

    def add_widget(self, widget: QWidget) -> None:
        self._widget.addWidget(widget)
        self._progress_indicator.add_item(QProgressIndicatorItem())

    def remove_widget(self, index: int) -> None:
        self._widget.removeWidget(self._widget.widget(index))
        self._progress_indicator.remove_item_at(index)

        if self._widget.current_index == index and self._widget.count() > 0:
            self.set_current_index(0)

    def current_index(self) -> int:
        return self._progress_indicator.current_index

    def set_current_index(self, index: int) -> None:
        self._widget.slide_in_index(index, self._direction)
        self._progress_indicator.set_current_index(index)

    def count(self) -> int:
        return self._progress_indicator.count
#----------------------------------------------------------------------
