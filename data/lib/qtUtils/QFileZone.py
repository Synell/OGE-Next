#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .QFiles import QFiles
from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
from .QLinkLabel import QLinkLabel
#----------------------------------------------------------------------

    # Class
class QFileZone(QGridFrame):
    drag_and_drop_used = Signal()
    dialog_used = Signal()
    item_added = Signal(str)
    items_added = Signal(list)

    def __init__(self, parent = None, lang: dict = {}, icon: str = None, icon_size: int = 96, type: QFiles.Dialog = QFiles.Dialog.OpenFileName, dir: str = '', filter: str = '') -> None:
        super().__init__(parent)
        self._icon = icon
        self._lang = lang
        self._type = type
        self._dir = dir
        self.set_filter(filter)
        self._icon_size = icon_size

        match type:
            case QFiles.Dialog.OpenFileUrl: type = QFiles.Dialog.OpenFileName
            case QFiles.Dialog.OpenFileUrls: type = QFiles.Dialog.OpenFileNames
            case QFiles.Dialog.ExistingDirectoryUrl: type = QFiles.Dialog.ExistingDirectory
            case QFiles.Dialog.SaveFileName: type = QFiles.Dialog.OpenFileName
            case QFiles.Dialog.SaveFileUrl: type = QFiles.Dialog.OpenFileName
        self._type = type

        self.setProperty('QFileZone', True)

        icon_widget = QIconWidget(self, self._icon, icon_size)
        self.grid_layout.addWidget(icon_widget, 0, 0)

        widget = QGridFrame()
        widget.setProperty('transparent', True)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)

        label = QLabel(lang['QLabel']['dragAndDrop' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')])
        label.setProperty('class', 'h2')
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        label = QLinkLabel(lang['QLinkLabel']['select' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')])
        label.setProperty('class', 'bold')
        label.clicked.connect(self._clicked)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(widget, 1, 0)
        self.grid_layout.setAlignment(widget, Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(90, 60, 90, 60)

        self.setAcceptDrops(True)


    @property
    def filter(self):
        return self._filter

    def set_filter(self, filter: str) -> None:
        self._filter = filter

        self.__extension_list__ = []
        for ext in self._filter.split(';;'):
            ext = ext.split('(')[-1].replace('.', '').replace('*', '').replace(')', '').replace(' ', '').replace('.', '').split(',')
            for i in ext:
                if i: self.__extension_list__.append(i)


    def _clicked(self, action: str) -> None:
        path = None

        match action:
            case 'file':
                path = QFileDialog.getOpenFileName(self, dir = self._dir, filter = self._filter, caption = self._lang['QFileDialog']['file'])[0]
            case 'files':
                path = QFileDialog.getOpenFileNames(self, dir = self._dir, filter = self._filter, caption = self._lang['QFileDialog']['files'])[0]
            case 'directory':
                path = QFileDialog.getExistingDirectory(self, dir = self._dir, caption = self._lang['QFileDialog']['directory'])[0]

        if not path: return

        self.dialog_used.emit()

        if type(path) is not list:
            path = [path]

        for p in path:
            self.item_added.emit(p)

        self.items_added.emit(path)


    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if not event.mimeData().hasUrls(): return event.ignore()

        for e in event.mimeData().urls():
            if not e.isLocalFile():
                return event.ignore()
    
            if not e.toLocalFile().split('.')[-1] in self.__extension_list__:
                return event.ignore()

        event.accept()


    def dropEvent(self, event: QDropEvent) -> None:
        self.drag_and_drop_used.emit()
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.item_added.emit(f)
        self.items_added.emit(files)
#----------------------------------------------------------------------
