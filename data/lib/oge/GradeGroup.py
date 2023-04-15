
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

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def notes(self) -> list[Grade]:
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

    def __str__(self) -> str:
        return f'{self.title} ({self.coefficient})\n\t' + '\n'.join([f'\t{note}' for note in self.notes]).replace('\n', '\n\t')
#----------------------------------------------------------------------
