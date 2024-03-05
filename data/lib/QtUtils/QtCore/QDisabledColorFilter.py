#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel
#----------------------------------------------------------------------

    # Class
class QDisabledColorFilter(QObject):
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Paint and isinstance(watched, QLabel):
            painter = QPainter(watched)

            pixmap = watched.pixmap()
            watched.style().drawItemPixmap(painter, watched.rect(), watched.alignment(), pixmap)

            return True

        return False
#----------------------------------------------------------------------
