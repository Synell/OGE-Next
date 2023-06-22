
#----------------------------------------------------------------------

    # Libraries
from .Subject import Subject
#----------------------------------------------------------------------

    # Class
class Pole:
    def __init__(self, title: str, coefficient: float, subjects: list[Subject]) -> None:
        self._title = title
        self._coefficient = coefficient
        self._subjects = subjects
        self._avg = None
        self._has_missing_data = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def subjects(self) -> list[Subject]:
        return self._subjects.copy()

    def find_subject_by_name(self, name: str) -> Subject | None:
        for subject in self._subjects:
            if subject.title == name: return subject
        return None

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        note, coeff = 0, 0
        for matiere in self._subjects:
            if matiere.average is None: continue

            note += matiere.average * matiere.coefficient
            coeff += matiere.coefficient

        if coeff == 0: return None

        self._avg = note / coeff

        return self._avg

    @property
    def new_grade_count(self) -> int:
        return sum(subject.new_grade_count for subject in self._subjects)
    
    @property
    def new_grades_str(self) -> str:
        lst = []

        for subject in self._subjects:
            if subject.new_grade_count <= 0: continue

            lst.append(f'• {self._title}\n\t' + subject.new_grades_str.replace('\n', '\n\t'))

        return '\n\n'.join(lst)

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(subject.has_missing_data for subject in self._subjects) or self._coefficient is None or self._coefficient == 0
        return self._has_missing_data

    def set_as_new(self) -> None:
        for subject in self._subjects: subject.set_as_new()

    def __str__(self) -> str:
        return f'{self._title} ({self._coefficient})\n\t' + '\n'.join([f'\t{matiere}' for matiere in self._subjects]).replace('\n', '\n\t')

    def to_json(self) -> dict:
        return {
            'title': self._title,
            'coefficient': self._coefficient,
            'subjects': [subject.to_json() for subject in self._subjects]
        }

    @staticmethod
    def from_json(json: dict) -> 'Pole':
        return Pole(
            json['title'],
            json['coefficient'],
            [Subject.from_json(subject) for subject in json['subjects']]
        )
#----------------------------------------------------------------------
