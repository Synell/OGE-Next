
#----------------------------------------------------------------------

    # Class
class Grade:
    def __init__(self, value: float, total: float, coefficient: float) -> None:
        self._value = value
        self._total = total
        self._coefficient = coefficient
        self._has_missing_data = None

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
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self.value is None or self.total is None or self.coefficient is None or self.coefficient == 0
        return self._has_missing_data

    def __str__(self) -> str:
        return f'{self.value}/{self.total} ({self.coefficient})'

    def to_json(self) -> dict:
        return {
            'value': self.value,
            'total': self.total,
            'coefficient': self.coefficient
        }

    @staticmethod
    def from_json(json: dict) -> 'Grade':
        return Grade(
            json['value'],
            json['total'],
            json['coefficient']
        )
#----------------------------------------------------------------------
