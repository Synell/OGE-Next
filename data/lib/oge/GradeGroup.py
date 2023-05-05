
#----------------------------------------------------------------------

    # Libraries
from .Grade import Grade
#----------------------------------------------------------------------

    # Class
class GradeGroup:
    def __init__(self, title: str, coefficient: float, grades: list[Grade]) -> None:
        self._title = title
        self._coefficient = coefficient
        self._grades = grades
        self._avg = None
        self._has_missing_data = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def grades(self) -> list[Grade]:
        return self._grades.copy()

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        grade, coefficient = 0, 0
        for note_ in self._grades:
            grade += note_.value_20 * note_.coefficient
            coefficient += note_.coefficient

        if coefficient == 0: return None

        self._avg = grade / coefficient

        return self._avg

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(note.has_missing_data for note in self._grades) or self.coefficient is None or self.coefficient == 0
        return self._has_missing_data

    def __str__(self) -> str:
        return f'{self.title} ({self.coefficient})\n\t' + '\n'.join([f'\t{note}' for note in self.grades]).replace('\n', '\n\t')

    def to_json(self) -> dict:
        return {
            'title': self.title,
            'coefficient': self.coefficient,
            'notes': [note.to_json() for note in self.grades]
        }

    @staticmethod
    def from_json(json: dict) -> 'GradeGroup':
        return GradeGroup(
            json['title'],
            json['coefficient'],
            [Grade.from_json(note) for note in json['notes']]
        )
#----------------------------------------------------------------------
