
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
    def matieres(self) -> list[Subject]:
        return self._subjects.copy()

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
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(subject.has_missing_data for subject in self._subjects) or self.coefficient is None or self.coefficient == 0
        return self._has_missing_data

    def __str__(self) -> str:
        return f'{self.title} ({self.coefficient})\n\t' + '\n'.join([f'\t{matiere}' for matiere in self.matieres]).replace('\n', '\n\t')

    def to_json(self) -> dict:
        return {
            'title': self.title,
            'coefficient': self.coefficient,
            'subjects': [subject.to_json() for subject in self.matieres]
        }

    @staticmethod
    def from_json(json: dict) -> 'Pole':
        return Pole(
            json['title'],
            json['coefficient'],
            [Subject.from_json(subject) for subject in json['subjects']]
        )
#----------------------------------------------------------------------
