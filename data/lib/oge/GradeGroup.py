
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
        for grade_ in self._grades:
            grade += grade_.value_20 * grade_.coefficient
            coefficient += grade_.coefficient

        if coefficient == 0: return None

        self._avg = grade / coefficient

        return self._avg

    @property
    def new_grade_count(self) -> int:
        return sum(grade.is_new for grade in self._grades)
    
    @property
    def new_grades_str(self) -> list[str]:
        return [f'{self._title} > {grade}' for grade in self._grades if grade.is_new]

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(grade.has_missing_data for grade in self._grades) or self._coefficient is None or self._coefficient == 0
        return self._has_missing_data

    def set_as_new(self) -> None:
        for grade in self._grades: grade.is_new = True

    def __str__(self) -> str:
        return f'{self._title} ({self._coefficient})\n\t' + '\n'.join([f'\t{grade}' for grade in self._grades]).replace('\n', '\n\t')

    def to_json(self) -> dict:
        return {
            'title': self._title,
            'coefficient': self._coefficient,
            'grades': [grade.to_json() for grade in self._grades]
        }

    @staticmethod
    def from_json(json: dict) -> 'GradeGroup':
        return GradeGroup(
            json['title'],
            json['coefficient'],
            [Grade.from_json(grade) for grade in json['grades']]
        )
#----------------------------------------------------------------------
