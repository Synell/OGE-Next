
#----------------------------------------------------------------------

    # Class
class Grade:
    def __init__(self, value: float, total: float, coefficient: float) -> None:
        self._value = value
        self._total = total
        self._coefficient = coefficient
        self._is_new = False
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
    def is_new(self) -> bool:
        return self._is_new
    
    @is_new.setter
    def is_new(self, value: bool) -> None:
        self._is_new = value

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self.value is None or self.total is None or self.coefficient is None or self.coefficient == 0
        return self._has_missing_data

    def __str__(self) -> str:
        return f'{self.value}/{self.total} ({self.coefficient})'

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Grade):
            return self.value == __value.value and self.total == __value.total and self.coefficient == __value.coefficient
        else:
            return False

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
