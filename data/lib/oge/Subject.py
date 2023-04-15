
#----------------------------------------------------------------------

    # Libraries
from .GradeGroup import GradeGroup
#----------------------------------------------------------------------

    # Class
class Subject:
    def __init__(self, title: str, coefficient: float, grade_groups: list[GradeGroup]) -> None:
        self._title = title
        self._coefficient = coefficient
        self._grade_groups = grade_groups
        self._avg = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def grade_groups(self) -> list[GradeGroup]:
        return self._grade_groups.copy()

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        note, coeff = 0, 0
        for note_group in self._grade_groups:
            if note_group.average is None: continue

            note += note_group.average * note_group.coefficient
            coeff += note_group.coefficient

        if coeff == 0: return None

        self._avg = note / coeff

        return self._avg

    def __str__(self) -> str:
        return f'{self.title} ({self.coefficient})\n\t' + '\n'.join([f'\t{note_group}' for note_group in self.grade_groups]).replace('\n', '\n\t')
#----------------------------------------------------------------------
