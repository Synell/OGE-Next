#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
from .QLinkLabel import QLinkLabel
from ..QtCore import QLangData
from ..QtCore.QFiles import QFiles
#----------------------------------------------------------------------

    # Class
class QFileZone(QGridFrame):
    drag_and_drop_used = Signal()
    dialog_used = Signal()
    item_added = Signal(str)
    items_added = Signal(list)

    def __init__(self, parent = None, lang: QLangData = {}, icon: str = None, icon_size: int = 96, type: QFiles.Dialog = QFiles.Dialog.OpenFileName, dir: str = '', filter: str = '') -> None:
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
            case QFiles.Dialog.SaveFileUrl: type = QFiles.Dialog.SaveFileName
        self._type = type

        self.setProperty('QFileZone', True)

        icon_widget = QIconWidget(self, self._icon, icon_size)
        self.layout_.addWidget(icon_widget, 0, 0)

        widget = QGridFrame()
        widget.setProperty('transparent', True)
        widget.layout_.setContentsMargins(0, 0, 0, 0)
        widget.layout_.setSpacing(5)

        label = QLabel(lang.get('QLabel.dragAndDrop' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')))
        label.setProperty('class', 'h2')
        widget.layout_.addWidget(label, 0, 0)
        widget.layout_.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        label = QLinkLabel(lang.get('QLinkLabel.select' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')))
        label.setProperty('class', 'bold')
        label.clicked.connect(self._clicked)
        widget.layout_.addWidget(label, 1, 0)
        widget.layout_.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        self.layout_.addWidget(widget, 1, 0)
        self.layout_.setAlignment(widget, Qt.AlignmentFlag.AlignCenter)

        self.layout_.setSpacing(10)
        self.layout_.setContentsMargins(90, 60, 90, 60)

        self.setAcceptDrops(True)


    @property
    def filter(self):
        return self._filter

    def set_filter(self, filter: str) -> None:
        self._filter = filter

        self._extension_list = []
        for ext in self._filter.split(';;'):
            ext = ext.split('(')[-1].replace('.', '').replace('*', '').replace(')', '').replace(' ', '').replace('.', '').split(',')
            for i in ext:
                if i: self._extension_list.append(i.lower())


    def _clicked(self, action: str) -> None:
        path = None

        match action:
            case 'file':
                path = QFileDialog.getOpenFileName(self, dir = self._dir, filter = self._filter, caption = self._lang.get('QFileDialog.file'))[0]

            case 'files':
                path = QFileDialog.getOpenFileNames(self, dir = self._dir, filter = self._filter, caption = self._lang.get('QFileDialog.files'))[0]

            case 'directory':
                path = QFileDialog.getExistingDirectory(self, dir = self._dir, caption = self._lang.get('QFileDialog.directory'))[0]

        if not path: return

        self.dialog_used.emit()

        if type(path) is not list:
            path = [path]

        for p in path:
            self.item_added.emit(p)

        self.items_added.emit(path)


    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if not event.mimeData().hasUrls(): return event.ignore()

        if self._type == QFiles.Dialog.OpenFileNames:
            if len(event.mimeData().urls()) > 1: return event.ignore()

        for e in event.mimeData().urls():
            if not e.isLocalFile():
                return event.ignore()
    
            if not e.toLocalFile().split('.')[-1].lower() in self._extension_list:
                return event.ignore()

        event.accept()


    def dropEvent(self, event: QDropEvent) -> None:
        self.drag_and_drop_used.emit()

        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files: self.item_added.emit(f)

        self.items_added.emit(files)
#----------------------------------------------------------------------
