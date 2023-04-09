
#----------------------------------------------------------------------

    # Class
class Note:
    def __init__(self, value: float, total: float, coeff: float) -> None:
        self._value = value
        self._total = total
        self._coeff = coeff

    @property
    def value(self) -> str:
        return self._value

    @property
    def total(self) -> str:
        return self._total

    @property
    def value_20(self) -> str:
        return self._value * (20 / self._total)

    @property
    def coeff(self) -> float:
        return self._coeff

    def __str__(self) -> str:
        return f'{self.value}/{self.total} ({self.coeff})'
#----------------------------------------------------------------------
