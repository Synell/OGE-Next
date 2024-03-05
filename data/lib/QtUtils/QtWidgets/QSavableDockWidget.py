#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDockWidget, QMainWindow
from PySide6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QSavableDockWidget(QDockWidget):
    # def __init__(self, name: str, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)
    #     self._name = name

    # @property
    # def name(self) -> str:
    #     return self._name

    @property
    def area(self) -> Qt.DockWidgetArea:
        return self.parent().dockWidgetArea(self)

    @property
    def is_floating(self) -> bool:
        return self.isFloating()

    @property
    def tabified(self) -> list:
        return self.parent().tabifiedDockWidgets(self)

    def to_dict(self) -> dict:
        return {
            'area': self.area.value if not self.is_floating else [self.geometry().x(), self.geometry().y()],
            'isFloating': self.is_floating,
            'tabified': [dw.objectName() for dw in self.tabified],
            'size': [self.size().width(), self.size().height()],
            'visible': not self.isHidden()
            # 'orientation': self.orientation().value
        }

    def load_dict(self, main_window: QMainWindow, data: dict, orientation: Qt.Orientation = Qt.Orientation.Vertical) -> None:
        if data['isFloating']:
            main_window.addDockWidget(Qt.DockWidgetArea(1), self, orientation)
            self.setFloating(True)
            self.move(data['area'][0], data['area'][1])
            self.resize(data['size'][0], data['size'][1])

        else:
            main_window.addDockWidget(Qt.DockWidgetArea(data['area']), self, orientation)

        # self.resize(data['size'][0], data['size'][1])

        for w in data['tabified']:
            if type(w) == str: w = main_window.findChild(QDockWidget, w, Qt.FindChildOption.FindDirectChildrenOnly)
            if w: main_window.tabifyDockWidget(self, w)

        self.setVisible(data['visible'])

    @staticmethod
    def from_dict(main_window: QMainWindow, data: dict, orientation: Qt.Orientation = Qt.Orientation.Vertical) -> 'QSavableDockWidget':
        widget = QSavableDockWidget()
        widget.load_dict(main_window, data, orientation)
        return widget
#----------------------------------------------------------------------
