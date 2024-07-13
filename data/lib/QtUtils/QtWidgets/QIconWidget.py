#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFileSystemModel
from PySide6.QtGui import QPixmap, QIcon, QImage, QBitmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QSize, QFileInfo
import os
from .QGridFrame import QGridFrame
#----------------------------------------------------------------------

    # Class
class QIconWidget(QGridFrame):
    def __init__(self, parent = None, icon: str | bytes | QPixmap | QSvgWidget | QIcon | QLabel | None = None, icon_size: QSize = QSize(96, 96), check_file: bool = False, mask: QBitmap = None) -> None:
        super().__init__(parent)
        self._icon_size = QSize(96, 96)
        self._check_file = check_file
        self._mask = mask
        self.set(icon, icon_size)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self.setProperty('QIconWidget', True)
        self.update()

    def set(self, icon: str | bytes | QPixmap | QSvgWidget | QIcon | QLabel, size: QSize = 0) -> None:
        self.icon = icon
        self.icon_size = size
        self.update()

    @property
    def icon(self) -> str | bytes | QPixmap | QSvgWidget | QIcon | QLabel:
        return self._icon

    @icon.setter
    def icon(self, icon: str | bytes | QPixmap | QSvgWidget | QIcon | QLabel) -> None:
        self._icon = icon
        self.update()

    @property
    def icon_size(self) -> QSize:
        return self._icon_size

    @icon_size.setter
    def icon_size(self, size: QSize) -> None:
        self._icon_size = size
        self.update()

    @property
    def check_file(self) -> bool:
        return self._check_file

    @check_file.setter
    def check_file(self, check_file: bool) -> None:
        self._check_file = check_file
        self.update()

    @property
    def mask(self) -> QBitmap:
        return self._mask

    @mask.setter
    def mask(self, mask: QBitmap) -> None:
        self._mask = mask
        self.update()

    @staticmethod
    def file_icon(path: str) -> QIcon:
        file = QFileInfo(path)
        model = QFileSystemModel()
        model.setRootPath(file.path())
        qq = model.iconProvider()
        return qq.icon(file)

    def update(self) -> None:
        for i in reversed(range(self.layout_.count())):
            self.layout_.itemAt(i).widget().setParent(None)

        pixmap = QIconWidget.generate_icon(self.icon, self.icon_size, self.check_file, self.mask)

        self.layout_.addWidget(pixmap, 0, 0)

    @staticmethod
    def is_file_icon(icon: str | bytes | QPixmap | QSvgWidget | QIcon | QLabel) -> bool:
        if isinstance(icon, str):
            if os.path.isfile(icon):
                if QIconWidget._check_extension(icon, ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg']): return False
            else: return False
        elif isinstance(icon, (bytes, QPixmap, QSvgWidget, QIcon, QLabel)): return False
        return True

    @staticmethod
    def generate_icon(icon: str | QPixmap | QSvgWidget | QIcon | QLabel, icon_size: QSize = QSize(96, 96), check_file: bool = False, mask: QBitmap = None) -> QLabel | QSvgWidget:
        pixmap = None

        if icon:
            if type(icon) is QPixmap:
                pixmap = QLabel()
                pixmap.setPixmap(icon.scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            elif type(icon) is QSvgWidget:
                pixmap = icon

            elif type(icon) is QIcon:
                pixmap = QLabel()
                pixmap.setPixmap(icon.pixmap(icon_size).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            
            elif type(icon) is QLabel:
                pixmap = QLabel()
                if icon.pixmap().width() == icon_size.width() and icon.pixmap().height() == icon_size.height():
                    pixmap.setPixmap(icon.pixmap())
                else:
                    pixmap.setPixmap(icon.pixmap().scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            elif type(icon) is str:
                if os.path.isfile(icon):
                    if icon.endswith('.svg'): pixmap = QSvgWidget(icon)
                    elif QIconWidget._check_extension(icon, ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico']):
                        pmap = QPixmap(icon).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        pixmap = QLabel()
                        pixmap.setPixmap(pmap)

                    elif check_file:
                        pixmap = QLabel()
                        pixmap.setPixmap(QIconWidget.file_icon(icon).pixmap(icon_size).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

                    else:
                        pixmap = QSvgWidget()

                else:
                    pixmap = QSvgWidget()

            elif type(icon) is bytes:
                pixmap = QLabel()
                img = QImage()
                img.loadFromData(icon)
                pixmap.setPixmap(QPixmap.fromImage(img).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            elif type(icon) is QImage:
                pixmap = QLabel()
                pixmap.setPixmap(QPixmap.fromImage(icon).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        else:
            pixmap = QSvgWidget()

        if not pixmap: pixmap = QLabel()
        pixmap.setFixedSize(icon_size)
        if mask: pixmap.setMask(mask)

        return pixmap

    @staticmethod
    def _check_extension(path: str, ext: list[str]) -> bool:
        for i in ext:
            if path.endswith(i): return True
        return False
#----------------------------------------------------------------------
