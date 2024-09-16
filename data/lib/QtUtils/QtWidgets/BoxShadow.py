#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QGraphicsEffect, QVBoxLayout, QGraphicsBlurEffect, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPainter, QTransform, QImage, QPixmap
from PySide6.QtCore import Qt, QRect, QRectF, QSize

from ..QtGui import QUtilsColor
#----------------------------------------------------------------------

    # Class (Credits to Leonid Gvozdev, Updated by Synel)
class BoxShadow(QGraphicsEffect):
    def __init__(
        self,
        shadow_list: list[dict] = None,
        border: int = 0,
        smooth: bool = False
    ) -> None:
        QGraphicsEffect.__init__(self)
        self._shadow_list = []

        self._max_x_offset = 0
        self._max_y_offset = 0
        self._border = 0
        self._smooth = smooth
        self.set_shadow_list(shadow_list)
        self.set_border(border)


    def set_shadow_list(self, shadow_list: list[dict] = None) -> None:
        if shadow_list is None:
            shadow_list = []
        self._shadow_list = shadow_list

        self._set_max_offset()


    def set_border(self, border: int) -> None:
        if border > 0:
            self._border = border
        else:
            self._border = 0


    def necessary_indentation(self) -> tuple[int, int]:
        return self._max_x_offset, self._max_y_offset


    def boundingRectFor(self, rect: QRect) -> QRect:
        return rect.adjusted(
            -self._max_x_offset, -self._max_y_offset,
            self._max_x_offset, self._max_y_offset
        )


    def _set_max_offset(self) -> None:
        for shadow in self._shadow_list:
            if 'outside' in shadow.keys():
                if self._max_x_offset < abs(shadow['offset'][0]) \
                        + shadow['blur'] * 2:
                    self._max_x_offset = abs(shadow['offset'][0]) \
                        + shadow['blur'] * 2
                if self._max_y_offset < abs(shadow['offset'][1]) \
                        + shadow['blur'] * 2:
                    self._max_y_offset = abs(shadow['offset'][1]) \
                        + shadow['blur'] * 2


    @staticmethod
    def _blur_pixmap(src: QPixmap, blur_radius: int) -> QPixmap:
        w, h = src.width(), src.height()

        effect = QGraphicsBlurEffect(blurRadius=blur_radius)

        scene = QGraphicsScene()
        item = QGraphicsPixmapItem()
        item.setPixmap(QPixmap(src))
        item.setGraphicsEffect(effect)
        scene.addItem(item)

        res = QImage(
            QSize(w, h),
            QImage.Format.Format_ARGB32
        )
        res.fill(Qt.GlobalColor.transparent)

        ptr = QPainter(res)
        ptr.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        scene.render(ptr, QRectF(), QRectF(0, 0, w, h))
        ptr.end()

        return QPixmap(res)


    @staticmethod
    def _colored_pixmap(color: QUtilsColor, pixmap: QPixmap) -> QPixmap:
        new_pixmap = QPixmap(pixmap)
        new_pixmap.fill(color.QColorAlpha)
        painter = QPainter(new_pixmap)
        painter.setTransform(QTransform())

        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return new_pixmap


    @staticmethod
    def _cut_shadow(
        pixmap: QPixmap,
        source: QPixmap,
        offset_x: int,
        offset_y: int
    ) -> QPixmap:
        painter = QPainter(pixmap)
        painter.setTransform(QTransform())

        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
        painter.drawPixmap(offset_x, offset_y, source)
        painter.end()

        return pixmap


    def _outside_shadow(self) -> QPixmap:
        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(QUtilsColor('#00000000').QColorAlpha, Qt.MaskMode.MaskInColor)

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if 'outside' in _shadow.keys():
                shadow = QPixmap(mask.size())
                shadow.fill(Qt.GlobalColor.transparent)
                shadow_painter = QPainter(shadow)

                shadow_painter.setRenderHints(
                    QPainter.RenderHint.Antialiasing |
                    QPainter.RenderHint.SmoothPixmapTransform
                )
                shadow_painter.setTransform(QTransform())
                shadow_painter.setPen(_shadow['color'].QColorAlpha)
                shadow_painter.drawPixmap(
                    _shadow['offset'][0],
                    _shadow['offset'][1],
                    mask
                )
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        outside_shadow = QPixmap(mask.size())
        outside_shadow.fill(Qt.GlobalColor.transparent)

        outside_shadow_painter = QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QTransform())
        outside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        for i, pixmap in enumerate(_pixmap_shadow_list):
            outside_shadow_painter.drawPixmap(
                0, 0,
                BoxShadow._blur_pixmap(pixmap, self._shadow_list[i]['blur'])
            )

        outside_shadow_painter.end()

        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(QUtilsColor('#00000000').QColorAlpha, Qt.MaskMode.MaskOutColor)

        outside_shadow.setMask(mask)

        return outside_shadow


    def _inside_shadow(self) -> QPixmap:
        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(QUtilsColor('#00000000').QColorAlpha, Qt.MaskMode.MaskInColor)

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if 'inside' in _shadow.keys():
                shadow = QPixmap(mask.size())
                shadow.fill(Qt.GlobalColor.transparent)
                shadow_painter = QPainter(shadow)
                shadow_painter.setRenderHints(
                    QPainter.RenderHint.Antialiasing |
                    QPainter.RenderHint.SmoothPixmapTransform
                )

                removed_color = QUtilsColor('#000000')
                color: QUtilsColor = _shadow['color']
                if removed_color == color:
                    removed_color = QUtilsColor('#FFFFFF')

                shadow_painter.setTransform(QTransform())
                shadow_painter.setPen(color.QColorAlpha)
                shadow_painter.drawPixmap(0, 0, mask)
                shadow_painter.setPen(removed_color.QColorAlpha)
                shadow_painter.drawPixmap(
                    _shadow['offset'][0],
                    _shadow['offset'][1],
                    mask
                )

                shadow_mask = shadow.createMaskFromColor(
                    color.QColorAlpha,
                    Qt.MaskMode.MaskOutColor
                )
                shadow.fill(Qt.GlobalColor.transparent)
                shadow_painter.setPen(color.QColorAlpha)
                shadow_painter.drawPixmap(0, 0, shadow_mask)

                shadow_painter.end()

                shadow.scaled(mask.size())

                _pixmap_shadow_list.append(shadow)

        inside_shadow = QPixmap(mask.size())
        inside_shadow.fill(Qt.GlobalColor.transparent)

        inside_shadow_painter = QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QTransform())
        inside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        for i, pixmap in enumerate(_pixmap_shadow_list):
            inside_shadow_painter.drawPixmap(
                0, 0,
                BoxShadow._blur_pixmap(pixmap, self._shadow_list[i]['blur'])
            )

        inside_shadow_painter.end()

        inside_shadow.setMask(mask)

        return inside_shadow


    def _smooth_outside_shadow(self) -> QPixmap:
        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        if isinstance(source, tuple):
            source = source[0]

        w, h = source.width(), source.height()

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if 'outside' in _shadow.keys():
                shadow = QPixmap(source.size())
                shadow.fill(Qt.GlobalColor.transparent)

                shadow_painter = QPainter(shadow)
                shadow_painter.setRenderHints(
                    QPainter.RenderHint.Antialiasing |
                    QPainter.RenderHint.SmoothPixmapTransform)
                shadow_painter.setTransform(QTransform())

                shadow_painter.drawPixmap(
                    _shadow['offset'][0],
                    _shadow['offset'][1],
                    w, h,
                    BoxShadow._colored_pixmap(_shadow['color'], source)
                )
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        outside_shadow = QPixmap(source.size())
        outside_shadow.fill(Qt.GlobalColor.transparent)

        outside_shadow_painter = QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QTransform())
        outside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        for i, pixmap in enumerate(_pixmap_shadow_list):
            outside_shadow_painter.drawPixmap(
                0, 0, w, h,
                BoxShadow._blur_pixmap(pixmap, self._shadow_list[i]['blur'])
            )

        outside_shadow_painter.end()

        outside_shadow_painter = QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QTransform())
        outside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        outside_shadow_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
        outside_shadow_painter.drawPixmap(0, 0, w, h, source)

        outside_shadow_painter.end()

        return outside_shadow


    def _smooth_inside_shadow(self) -> QPixmap:
        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        w, h = source.width(), source.height()

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if 'inside' in _shadow.keys():
                shadow = QPixmap(source.size())
                shadow.fill(Qt.GlobalColor.transparent)
                shadow_painter = QPainter(shadow)
                shadow_painter.setRenderHints(
                    QPainter.RenderHint.Antialiasing |
                    QPainter.RenderHint.SmoothPixmapTransform
                )
                shadow_painter.setTransform(QTransform())
                new_source = BoxShadow._colored_pixmap(_shadow['color'], source)
                shadow_painter.drawPixmap(
                    0, 0, w, h,
                    BoxShadow._cut_shadow(
                        new_source, source,
                        _shadow['offset'][0] / 2,
                        _shadow['offset'][1] / 2
                    )
                )
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        inside_shadow = QPixmap(source.size())
        inside_shadow.fill(Qt.GlobalColor.transparent)

        inside_shadow_painter = QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QTransform())
        inside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        for i, pixmap in enumerate(_pixmap_shadow_list):
            inside_shadow_painter.drawPixmap(
                0, 0, w, h,
                BoxShadow._blur_pixmap(pixmap, self._shadow_list[i]['blur'])
            )

        inside_shadow_painter.end()

        inside_shadow_painter = QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QTransform())
        inside_shadow_painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        inside_shadow_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        inside_shadow_painter.drawPixmap(0, 0, w, h, source)

        inside_shadow_painter.end()

        return inside_shadow


    def draw(self, painter: QPainter) -> None:
        if not painter.isActive(): return

        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        restore_transform = painter.worldTransform()

        source_rect = self.boundingRectFor(
            self.sourceBoundingRect(Qt.CoordinateSystem.DeviceCoordinates)
        ).toRect()
        x, y, w, h = source_rect.getRect()

        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        painter.setTransform(QTransform())

        if self._smooth:
            outside_shadow = self._smooth_outside_shadow()
            inside_shadow = self._smooth_inside_shadow()

        else:
            outside_shadow = self._outside_shadow()
            inside_shadow = self._inside_shadow()

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawPixmap(x, y, w, h, outside_shadow)
        painter.drawPixmap(x, y, source)
        painter.drawPixmap(
            x + self._border, y + self._border,
            w - self._border * 2, h - self._border * 2,
            inside_shadow
        )
        painter.setWorldTransform(restore_transform)

        painter.end()


class BoxShadowWrapper(QWidget):
    def __init__(self, widget: QWidget, shadow_list: list[dict] = None,
        border: int = 0, disable_margins: bool = False,
        margins: tuple[float, float, float, float] |
        tuple[float, float] = None,
        smooth: bool = False
    ) -> None:
        QWidget.__init__(self)

        self._widget = widget
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addWidget(self._widget)

        self._box_shadow = BoxShadow(shadow_list, border, smooth)
        self._widget.setGraphicsEffect(self._box_shadow)

        self._disable_margins = True if (
            disable_margins is True or
            margins is not None
        ) else False

        if not self._disable_margins:
            X, Y = self._box_shadow.necessary_indentation()
            self._layout.setContentsMargins(X, Y, X, Y)

        elif margins is not None:
            if len(margins) == 2:
                self._layout.setContentsMargins(margins[0], margins[1], margins[0], margins[1])

            elif len(margins) == 4:
                self._layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])


    def set_shadow_list(self, shadow_list: list[dict] = None) -> None:
        self._box_shadow.set_shadow_list(shadow_list)

        if not self._disable_margins:
            X, Y = self._box_shadow.necessary_indentation()
            self._layout.setContentsMargins(X, Y, X, Y)


    def set_border(self, border: int) -> None:
        self._box_shadow.set_border(border)
#----------------------------------------------------------------------
