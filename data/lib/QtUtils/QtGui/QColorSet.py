#----------------------------------------------------------------------

    # Libraries
from .QUtilsColor import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QColorSet:
    def __init__(self, name: str, normal: QUtilsColor, hover: QUtilsColor, pressed: QUtilsColor, disabled: QUtilsColor) -> None:
        self._name = name
        self._normal = normal
        self._hover = hover
        self._pressed = pressed
        self._disabled = disabled

    @property
    def name(self) -> str: return self._name

    @property
    def normal(self) -> QUtilsColor: return self._normal

    @property
    def hover(self) -> QUtilsColor: return self._hover

    @property
    def pressed(self) -> QUtilsColor: return self._pressed

    @property
    def disabled(self) -> QUtilsColor: return self._disabled

    @property
    def items(self) -> tuple[tuple[str, QUtilsColor]]:
        return (
            ('color-normal', self._normal),
            ('color-hover', self._hover),
            ('color-pressed', self._pressed),
            ('color-disabled', self._disabled)
        )
#----------------------------------------------------------------------
