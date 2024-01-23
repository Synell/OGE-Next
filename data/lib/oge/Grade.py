
#----------------------------------------------------------------------

    # Libraries
from datetime import date as Date
#----------------------------------------------------------------------

    # Class
class Grade:
    def __init__(self, value: float, value_total: float, coefficient: float) -> None:
        self._value = value
        self._value_total = value_total
        self._coefficient = coefficient
        self._name = None
        self._date = None
        self._rank = None
        self._rank_total = None
        self._is_new = False
        self._has_missing_data = None
        self._is_only_missing_coefficient = None

    @property
    def value(self) -> float:
        return self._value

    @property
    def value_total(self) -> float:
        return self._value_total

    @property
    def value_20(self) -> float:
        return (self._value * (20 / self._value_total)) if self._value is not None and self._value_total is not None else None

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def date(self) -> Date:
        return self._date

    @date.setter
    def date(self, value: Date) -> None:
        self._date = value

    @property
    def rank(self) -> int:
        return self._rank

    @rank.setter
    def rank(self, value: int) -> None:
        self._rank = value

    @property
    def rank_total(self) -> int:
        return self._rank_total

    @rank_total.setter
    def rank_total(self, value: int) -> None:
        self._rank_total = value

    @property
    def is_new(self) -> bool:
        return self._is_new

    @is_new.setter
    def is_new(self, value: bool) -> None:
        self._is_new = value

    @property
    def _has_missing_grade_data(self) -> bool:
        return self._value is None or self._value_total is None

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self._has_missing_grade_data or (not self._coefficient)
        return self._has_missing_data

    @property
    def is_only_missing_coefficient(self) -> bool:
        if self._is_only_missing_coefficient is None: self._is_only_missing_coefficient = (not self._has_missing_grade_data) and (not self._coefficient)
        return self._is_only_missing_coefficient

    def has_missing_rank_data(self, only_for_new_grades: bool = False) -> bool:
        return ((self._rank is None or self._rank_total is None) and (not only_for_new_grades)) or (only_for_new_grades and self._is_new)

    def __str__(self) -> str:
        return f'{self._value}/{self._value_total} ({self._coefficient})'

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Grade):
            return self._value == __value.value and self._value_total == __value.value_total and self._coefficient == __value.coefficient
        else:
            return False

    def to_json(self) -> dict:
        return {
            'value': self._value,
            'value-total': self._value_total,
            'coefficient': self._coefficient,
            'name': self._name if self._name else None,
            'date': self._date.isoformat() if self._date is not None else None,
            'rank': self._rank,
            'rank-total': self._rank_total
        }

    @staticmethod
    def from_json(json: dict) -> 'Grade':
        value = json.get('value')
        value_total = json.get('value-total')
        coefficient = json.get('coefficient')
        date = json.get('date')

        g = Grade(
            float(value) if value is not None else None,
            float(value_total) if value_total is not None else json.get('total'), # Retrocompatibility
            float(coefficient) if coefficient is not None else None
        )

        g.name = json.get('name')
        g.date = Date.fromisoformat(date) if date is not None else None
        g.rank = json.get('rank')
        g.rank_total = json.get('rank-total')

        return g
#----------------------------------------------------------------------
