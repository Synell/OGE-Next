
#----------------------------------------------------------------------

    # Class
class Grade:
    def __init__(self, value: float, total: float, coefficient: float) -> None:
        self._value = value
        self._total = total
        self._coefficient = coefficient

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
