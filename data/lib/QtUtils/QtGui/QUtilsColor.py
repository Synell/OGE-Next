#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QColor
from multipledispatch import dispatch
import colorsys
#----------------------------------------------------------------------

    # Class
class QUtilsColor:
    @dispatch()
    def __init__(self) -> None:
        self._red = 0
        self._green = 0
        self._blue = 0
        self._alpha = 255

    @dispatch(int, int, int)
    def __init__(self, red: int, green: int, blue: int) -> None:
        self._red = self._byte_range(red)
        self._green = self._byte_range(green)
        self._blue = self._byte_range(blue)
        self._alpha = 255

    @dispatch(int, int, int, int)
    def __init__(self, red: int, green: int, blue: int, alpha: int) -> None:
        self._red = self._byte_range(red)
        self._green = self._byte_range(green)
        self._blue = self._byte_range(blue)
        self._alpha = self._byte_range(alpha)

    @dispatch(tuple)
    def __init__(self, rgb: tuple[int, int, int]) -> None:
        self._red = self._byte_range(rgb[0])
        self._green = self._byte_range(rgb[1])
        self._blue = self._byte_range(rgb[2])
        self._alpha = 255

    @dispatch(tuple)
    def __init__(self, rgba: tuple[int, int, int, int]) -> None:
        self._red = self._byte_range(rgba[0])
        self._green = self._byte_range(rgba[1])
        self._blue = self._byte_range(rgba[2])
        self._alpha = self._byte_range(rgba[3])

    @dispatch(QColor)
    def __init__(self, color: QColor) -> None:
        self._red = color.red()
        self._green = color.green()
        self._blue = color.blue()
        self._alpha = color.alpha()

    @dispatch(str)
    def __init__(self, color: str) -> None:
        color = color.replace('#', '')
        self._red = int(color[0:2], 16)
        self._green = int(color[2:4], 16)
        self._blue = int(color[4:6], 16)
        self._alpha = int(color[6:8], 16) if len(color) == 8 else 255

    def _byte_range(self, value: int) -> int:
        return int(max(0, min(value, 255)))


    @dispatch((int, float), (int, float), (int, float))
    @staticmethod
    def from_rgb(red: int, green: int, blue: int) -> 'QUtilsColor':
        return QUtilsColor(red, green, blue)

    @dispatch(tuple)
    @staticmethod
    def from_rgb(rgb: tuple[int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor(rgb[0], rgb[1], rgb[2])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_rgba(red: int, green: int, blue: int, alpha: int) -> 'QUtilsColor':
        return QUtilsColor(red, green, blue, alpha)

    @dispatch(tuple)
    @staticmethod
    def from_rgba(rgba: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor(rgba[0], rgba[1], rgba[2], rgba[3])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_argb(alpha: int, red: int, green: int, blue: int) -> 'QUtilsColor':
        return QUtilsColor(red, green, blue, alpha)

    @dispatch(tuple)
    @staticmethod
    def from_argb(argb: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor(argb[1], argb[2], argb[3], argb[0])


    @staticmethod
    def from_QColor(color: QColor) -> 'QUtilsColor':
        return QUtilsColor(color)


    @staticmethod
    def from_hex(color: str) -> 'QUtilsColor':
        return QUtilsColor(color)

    @staticmethod
    def from_hexa(color: str) -> 'QUtilsColor':
        return QUtilsColor(color)

    @staticmethod
    def from_ahex(color: str) -> 'QUtilsColor':
        c = QUtilsColor()
        color = color.replace('#', '')

        c._alpha = int(color[0:2], 16)
        c._red = int(color[2:4], 16)
        c._green = int(color[4:6], 16)
        c._blue = int(color[6:8], 16)

        return c


    @dispatch((int, float), (int, float), (int, float))
    @staticmethod
    def from_hsv(hue: int|float, saturation: int|float, value: int|float) -> 'QUtilsColor':
        r, g, b = colorsys.hsv_to_rgb(hue / 100.0, saturation / 100.0, value / 100.0)
        return QUtilsColor(int(r * 255), int(g * 255), int(b * 255))

    @dispatch(tuple)
    @staticmethod
    def from_hsv(hsv: tuple[int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hsv(hsv[0], hsv[1], hsv[2])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_hsva(hue: int|float, saturation: int|float, value: int|float, alpha: int|float) -> 'QUtilsColor':
        c = QUtilsColor.from_hsv(hue, saturation, value)
        c.alpha = alpha * 2.55
        return c

    @dispatch(tuple)
    @staticmethod
    def from_hsva(hsva: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hsva(hsva[0], hsva[1], hsva[2], hsva[3])


    @dispatch((int, float), (int, float), (int, float))
    @staticmethod
    def from_hls(hue: int|float, lightness: int|float, saturation: int|float) -> 'QUtilsColor':
        r, g, b = colorsys.hls_to_rgb(hue / 100.0, lightness / 100.0, saturation / 100.0)
        return QUtilsColor(int(r * 255), int(g * 255), int(b * 255))

    @dispatch(tuple)
    @staticmethod
    def from_hls(hls: tuple[int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hls(hls[0], hls[1], hls[2])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_hlsa(hue: int|float, lightness: int|float, saturation: int|float, alpha: int|float) -> 'QUtilsColor':
        c = QUtilsColor.from_hls(hue, lightness, saturation)
        c.alpha = alpha * 2.55
        return c

    @dispatch(tuple)
    @staticmethod
    def from_hlsa(hlsa: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hlsa(hlsa[0], hlsa[1], hlsa[2], hlsa[3])


    @dispatch((int, float), (int, float), (int, float))
    @staticmethod
    def from_hsl(hue: int|float, saturation: int|float, lightness: int|float) -> 'QUtilsColor':
        r, g, b = colorsys.hls_to_rgb(hue / 100.0, lightness / 100.0, saturation / 100.0)
        return QUtilsColor(int(r * 255), int(g * 255), int(b * 255))

    @dispatch(tuple)
    @staticmethod
    def from_hsl(hsl: tuple[int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hsl(hsl[0], hsl[1], hsl[2])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_hsla(hue: int|float, saturation: int|float, lightness: int|float, alpha: int|float) -> 'QUtilsColor':
        c = QUtilsColor.from_hsl(hue, saturation, lightness)
        c.alpha = alpha * 2.55
        return c

    @dispatch(tuple)
    @staticmethod
    def from_hsla(hsla: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_hsla(hsla[0], hsla[1], hsla[2], hsla[3])





    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_cmyk(cyan: int|float, magenta: int|float, yellow: int|float, black: int|float) -> 'QUtilsColor':
        r, g, b = int(2.55 * (100.0 - cyan) * (100.0 - black)), int(2.55 * (100.0 - magenta) * (100.0 - black)), int(2.55 * (100.0 - yellow) * (100.0 - black))
        return QUtilsColor(r, g, b)

    @dispatch(tuple)
    @staticmethod
    def from_cmyk(cmyk: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_cmyk(cmyk[0], cmyk[1], cmyk[2], cmyk[3])

    @dispatch((int, float), (int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_cmyka(cyan: int|float, magenta: int|float, yellow: int|float, black: int|float, alpha: int|float) -> 'QUtilsColor':
        c = QUtilsColor.from_cmyk(cyan, magenta, yellow, black)
        c.alpha = alpha * 2.55
        return c

    @dispatch(tuple)
    @staticmethod
    def from_cmyka(cmyka: tuple[int|float, int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_cmyka(cmyka[0], cmyka[1], cmyka[2], cmyka[3], cmyka[4])


    @dispatch((int, float), (int, float), (int, float))
    @staticmethod
    def from_yiq(y: int|float, i: int|float, q: int|float) -> 'QUtilsColor':
        r, g, b = colorsys.yiq_to_rgb(y / 100.0, i / 100.0, q / 100.0)
        return QUtilsColor(int(r * 255), int(g * 255), int(b * 255))

    @dispatch(tuple)
    @staticmethod
    def from_yiq(yiq: tuple[int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_yiq(yiq[0], yiq[1], yiq[2])

    @dispatch((int, float), (int, float), (int, float), (int, float))
    @staticmethod
    def from_yiqa(y: int|float, i: int|float, q: int|float, alpha: int|float) -> 'QUtilsColor':
        c = QUtilsColor.from_yiq(y, i, q)
        c.alpha = alpha * 2.55
        return c

    @dispatch(tuple)
    @staticmethod
    def from_yiqa(yiq: tuple[int|float, int|float, int|float, int|float]) -> 'QUtilsColor':
        return QUtilsColor.from_yiqa(yiq[0], yiq[1], yiq[2], yiq[3])


    @property
    def red(self) -> int:
        return self._red

    @red.setter
    def red(self, red: int) -> None:
        self._red = self._byte_range(red)

    @property
    def green(self) -> int:
        return self._green

    @green.setter
    def green(self, green: int) -> None:
        self._green = self._byte_range(green)

    @property
    def blue(self) -> int:
        return self._blue

    @blue.setter
    def blue(self, blue: int) -> None:
        self._blue = self._byte_range(blue)

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: int) -> None:
        self._alpha = self._byte_range(alpha)


    @property
    def hue_hsv(self) -> int|float:
        return self.hsv[0]

    @hue_hsv.setter
    def hue_hsv(self, hue: int|float) -> None:
        self.hsv = (hue, self.hsv[1], self.hsv[2])

    @property
    def saturation_hsv(self) -> int|float:
        return self.hsv[1]

    @saturation_hsv.setter
    def saturation(self, saturation: int|float) -> None:
        self.hsv = (self.hsv[0], saturation, self.hsv[2])

    @property
    def value_hsv(self) -> int|float:
        return self.hsv[2]

    @value_hsv.setter
    def value(self, value: int|float) -> None:
        self.hsv = (self.hsv[0], self.hsv[1], value)


    @property
    def hue_hls(self) -> int|float:
        return self.hls[0]

    @hue_hls.setter
    def hue_hls(self, hue: int|float) -> None:
        self.hls = (hue, self.hls[1], self.hls[2])

    @property
    def saturation_hls(self) -> int|float:
        return self.hls[1]

    @saturation_hls.setter
    def saturation(self, saturation: int|float) -> None:
        self.hls = (self.hls[0], saturation, self.hls[2])

    @property
    def lightness_hls(self) -> int|float:
        return self.hls[2]

    @lightness_hls.setter
    def lightness(self, lightness: int|float) -> None:
        self.hls = (self.hls[0], self.hls[1], lightness)


    @property
    def hue_hsl(self) -> int|float:
        return self.hsl[0]

    @hue_hsl.setter
    def hue_hsl(self, hue: int|float) -> None:
        self.hsl = (hue, self.hsl[1], self.hsl[2])

    @property
    def saturation_hsl(self) -> int|float:
        return self.hsl[1]

    @saturation_hsl.setter
    def saturation(self, saturation: int|float) -> None:
        self.hsl = (self.hsl[0], saturation, self.hsl[2])

    @property
    def lightness_hsl(self) -> int|float:
        return self.hsl[2]

    @lightness_hsl.setter
    def lightness(self, lightness: int|float) -> None:
        self.hsl = (self.hsl[0], self.hsl[1], lightness)


    @property
    def cyan(self) -> int|float:
        return self.cmyk[0]

    @cyan.setter
    def cyan(self, cyan: int|float) -> None:
        self.cmyk = (cyan, self.cmyk[1], self.cmyk[2], self.cmyk[3])

    @property
    def magenta(self) -> int|float:
        return self.cmyk[1]

    @magenta.setter
    def magenta(self, magenta: int|float) -> None:
        self.cmyk = (self.cmyk[0], magenta, self.cmyk[2], self.cmyk[3])

    @property
    def yellow(self) -> int|float:
        return self.cmyk[2]

    @yellow.setter
    def yellow(self, yellow: int|float) -> None:
        self.cmyk = (self.cmyk[0], self.cmyk[1], yellow, self.cmyk[3])

    @property
    def black(self) -> int|float:
        return self.cmyk[3]

    @black.setter
    def black(self, black: int|float) -> None:
        self.cmyk = (self.cmyk[0], self.cmyk[1], self.cmyk[2], black)

    @property
    def key(self) -> int|float:
        return self.cmyk[3]

    @key.setter
    def key(self, key: int|float) -> None:
        self.cmyk = (self.cmyk[0], self.cmyk[1], self.cmyk[2], key)


    @property
    def QColor(self) -> QColor:
        return QColor(self.red, self.green, self.blue, 255)

    @property
    def QColorAlpha(self) -> QColor:
        return QColor(self.red, self.green, self.blue, self.alpha)


    @property
    def hex(self) -> str:
        return f'#{self.red:02x}{self.green:02x}{self.blue:02x}'

    @hex.setter
    def hex(self, hex: str) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_hex(hex).rgb

    @property
    def hexa(self) -> str:
        return f'#{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}'

    @hexa.setter
    def hexa(self, hexa: str) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_hexa(hexa).rgba

    @property
    def ahex(self) -> str:
        return f'#{self.alpha:02x}{self.red:02x}{self.green:02x}{self.blue:02x}'

    @ahex.setter
    def ahex(self, ahex: str) -> None:
        self.alpha, self.red, self.green, self.blue = QUtilsColor.from_ahex(ahex).rgba


    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    @rgb.setter
    def rgb(self, rgb: tuple[int, int, int]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_rgb(rgb).rgb

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)

    @rgba.setter
    def rgba(self, rgba: tuple[int, int, int, int]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_rgba(rgba).rgba

    @property
    def argb(self) -> tuple[int, int, int, int]:
        return (self.alpha, self.red, self.green, self.blue)

    @argb.setter
    def argb(self, argb: tuple[int, int, int, int]) -> None:
        self.alpha, self.red, self.green, self.blue = QUtilsColor.from_argb(argb).argb


    @property
    def hsv(self) -> tuple[int|float, int|float, int|float]:
        h, s, v = colorsys.rgb_to_hsv(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        return (h * 100.0, s * 100.0, v * 100.0)

    @hsv.setter
    def hsv(self, hsv: tuple[int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_hsv(hsv).rgb

    @property
    def hsva(self) -> tuple[int|float, int|float, int|float, int|float]:
        h, s, v = self.hsv
        return (h, s, v, self.alpha / 2.55)

    @hsva.setter
    def hsva(self, hsva: tuple[int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_hsva(hsva).rgba


    @property
    def hls(self) -> tuple[int|float, int|float, int|float]:
        h, l, s = colorsys.rgb_to_hls(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        return (h * 100.0, l * 100.0, s * 100.0)

    @hls.setter
    def hls(self, hls: tuple[int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_hls(hls).rgb

    @property
    def hlsa(self) -> tuple[int|float, int|float, int|float, int|float]:
        h, l, s = self.hls
        return (h, l, s, self.alpha / 2.55)

    @hlsa.setter
    def hlsa(self, hlsa: tuple[int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_hlsa(hlsa).rgba


    @property
    def hsl(self) -> tuple[int|float, int|float, int|float]:
        h, l, s = colorsys.rgb_to_hls(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        return (h * 100.0, s * 100.0, l * 100.0)

    @hsl.setter
    def hsl(self, hsl: tuple[int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_hsl(hsl).rgb

    @property
    def hsla(self) -> tuple[int|float, int|float, int|float, int|float]:
        h, l, s = self.hsl
        return (h, s, l, self.alpha / 2.55)

    @hsla.setter
    def hsla(self, hsla: tuple[int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_hsla(hsla).rgba


    @property
    def yiq(self) -> tuple[int|float, int|float, int|float]:
        y, i, q = colorsys.rgb_to_yiq(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        return (y * 100.0, i * 100.0, q * 100.0)

    @yiq.setter
    def yiq(self, yiq: tuple[int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_yiq(yiq).rgb

    @property
    def yiqa(self) -> tuple[int|float, int|float, int|float, int|float]:
        y, i, q = self.yiq
        return (y, i, q, self.alpha / 2.55)

    @yiqa.setter
    def yiqa(self, yiqa: tuple[int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_yiqa(yiqa).rgba


    @property
    def cmyk(self) -> tuple[int|float, int|float, int|float, int|float]:
        k = 1.0 - max(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        k = k if k < 1.0 else 0.0
        c = (1.0 - self.red / 255.0 - k) / (1 - k)
        m = (1.0 - self.green / 255.0 - k) / (1 - k)
        y = (1.0 - self.blue / 255.0 - k) / (1 - k)
        return (c * 100.0, m * 100.0, y * 100.0, k * 100.0)

    @cmyk.setter
    def cmyk(self, cmyk: tuple[int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue = QUtilsColor.from_cmyk(cmyk).rgb

    @property
    def cmyka(self) -> tuple[int|float, int|float, int|float, int|float, int|float]:
        c, m, y, k = self.cmyk
        return (c, m, y, k, self.alpha / 2.55)

    @cmyka.setter
    def cmyka(self, cmyka: tuple[int|float, int|float, int|float, int|float, int|float]) -> None:
        self.red, self.green, self.blue, self.alpha = QUtilsColor.from_cmyka(cmyka).rgba
#----------------------------------------------------------------------
