
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
        self._has_missing_data = None
        self._is_only_missing_coefficient = None
        self._has_missing_grade_group_data = None


    @property
    def title(self) -> str:
        return self._title


    @property
    def coefficient(self) -> float:
        return self._coefficient


    @property
    def grade_groups(self) -> list[GradeGroup]:
        return self._grade_groups.copy()


    def find_grade_group_by_name(self, name: str) -> GradeGroup | None:
        for grade_group in self._grade_groups:
            if grade_group.title == name: return grade_group
        return None


    @property
    def average(self) -> float | None:
        if self._avg is not None: return self._avg

        note, coeff = 0, 0
        for grade_group in self._grade_groups:
            if grade_group.average is None: continue

            note += grade_group.average * grade_group.coefficient
            coeff += grade_group.coefficient

        if coeff == 0: return None

        self._avg = note / coeff

        return self._avg


    @property
    def new_grade_count(self) -> int:
        return sum(grade_group.new_grade_count for grade_group in self._grade_groups)


    @property
    def new_grades_str(self) -> str:
        return f'• {self._title}\n' + '\n\n'.join(grade_group.new_grades_str.replace('\n', '\n        ') for grade_group in self._grade_groups if grade_group.new_grade_count > 0)


    @property
    def has_missing_grade_group_data(self) -> bool:
        if self._has_missing_grade_group_data is None: self._has_missing_grade_group_data = any(grade_group.has_missing_data for grade_group in self._grade_groups)
        return self._has_missing_grade_group_data


    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self.has_missing_grade_group_data or self._coefficient is None or (not self._coefficient)
        return self._has_missing_data


    @property
    def is_only_missing_coefficient(self) -> bool:
        if self._is_only_missing_coefficient is None: self._is_only_missing_coefficient = (not self.has_missing_grade_group_data) and (not self._coefficient)
        return self._is_only_missing_coefficient


    def has_missing_rank_data(self, only_for_new_grades: bool) -> bool:
        return any(grade_group.has_missing_rank_data(only_for_new_grades) for grade_group in self._grade_groups)


    def set_as_new(self) -> None:
        for grade_group in self._grade_groups: grade_group.set_as_new()


    def is_empty(self) -> bool:
        return len(self._grade_groups) == 0 or all(grade_group.is_empty() for grade_group in self._grade_groups)


    def __str__(self) -> str:
        return f'{self._title} ({self._coefficient})\n\t' + '\n'.join([f'\t{grade_group}' for grade_group in self._grade_groups]).replace('\n', '\n\t')


    def to_json(self) -> dict:
        return {
            'title': self._title,
            'coefficient': self._coefficient,
            'grade_groups': [grade_group.to_json() for grade_group in self._grade_groups]
        }


    @staticmethod
    def from_json(json: dict) -> 'Subject':
        return Subject(
            json['title'],
            json['coefficient'],
            [GradeGroup.from_json(grade_group) for grade_group in json['grade_groups']]
        )
#----------------------------------------------------------------------
