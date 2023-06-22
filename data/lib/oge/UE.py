
#----------------------------------------------------------------------

    # Libraries
from .Pole import Pole
#----------------------------------------------------------------------

    # Class
class UE:
    def __init__(self, title: str, coefficient: float, poles: list[Pole]) -> None:
        self._title = title
        self._coefficient = coefficient
        self._poles = poles
        self._avg = None
        self._has_missing_data = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def poles(self) -> list[Pole]:
        return self._poles.copy()

    def find_pole_by_name(self, name: str) -> Pole | None:
        for pole in self._poles:
            if pole.title == name: return pole
        return None

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        grade, coeff = 0, 0
        for pole in self._poles:
            if pole.average is None: continue

            grade += pole.average * pole.coefficient
            coeff += pole.coefficient

        if coeff == 0: return None

        self._avg = grade / coeff

        return self._avg

    @property
    def new_grade_count(self) -> int:
        return sum(pole.new_grade_count for pole in self._poles)
    
    @property
    def new_grades_str(self) -> str:
        lst = []

        for pole in self._poles:
            if pole.new_grade_count <= 0: continue

            lst.append(f'• {self._title}\n\t' + pole.new_grades_str.replace('\n', '\n\t'))

        return '\n\n'.join(lst)

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(pole.has_missing_data for pole in self._poles) or self._coefficient is None or self._coefficient == 0
        return self._has_missing_data

    def set_as_new(self) -> None:
        for pole in self._poles: pole.set_as_new()

    def __str__(self) -> str:
        return f'{self._title} ({self._coefficient})\n' + '\n'.join([f'\t{pole}' for pole in self._poles])

    def to_json(self) -> dict:
        return {
            'title': self._title,
            'coefficient': self._coefficient,
            'poles': [pole.to_json() for pole in self._poles]
        }

    @staticmethod
    def from_json(json: dict) -> 'UE':
        return UE(
            json['title'],
            json['coefficient'],
            [Pole.from_json(pole) for pole in json['poles']]
        )
#----------------------------------------------------------------------
