
#----------------------------------------------------------------------

    # Class
class Grade:
    def __init__(self, value: float, total: float, coefficient: float) -> None:
        self._value = value
        self._total = total
        self._coefficient = coefficient
        self._is_new = False
        self._has_missing_data = None
        self._is_only_missing_coefficient = None

    @property
    def value(self) -> str:
        return self._value

    @property
    def total(self) -> str:
        return self._total

    @property
    def value_20(self) -> str:
        return (self._value * (20 / self._total)) if self._value is not None and self._total is not None else None

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
    def _has_missing_grade_data(self) -> bool:
        return self._value is None or self._total is None

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self._has_missing_grade_data or (not self._coefficient)
        return self._has_missing_data

    @property
    def is_only_missing_coefficient(self) -> bool:
        if self._is_only_missing_coefficient is None: self._is_only_missing_coefficient = (not self._has_missing_grade_data) and (not self._coefficient)
        return self._is_only_missing_coefficient

    def __str__(self) -> str:
        return f'{self._value}/{self._total} ({self._coefficient})'

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Grade):
            return self._value == __value.value and self._total == __value.total and self._coefficient == __value.coefficient
        else:
            return False

    def to_json(self) -> dict:
        return {
            'value': self._value,
            'total': self._total,
            'coefficient': self._coefficient
        }

    @staticmethod
    def from_json(json: dict) -> 'Grade':
        return Grade(
            json['value'],
            json['total'],
            json['coefficient']
        )
#----------------------------------------------------------------------
