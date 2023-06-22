
#----------------------------------------------------------------------

    # Libraries
from .UE import UE
#----------------------------------------------------------------------

    # Class
class Semester:
    def __init__(self, id_: int, ues: list[UE]) -> None:
        self._id = id_
        self._ues = ues
        self._avg = None
        self._new_grade_count = None
        self._has_missing_data = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def ues(self) -> list[UE]:
        return self._ues.copy()

    def find_ue_by_id(self, id_: int) -> UE | None:
        for ue in self._ues:
            if ue.id == id_: return ue
        return None
    
    def find_ue_by_name(self, name: str) -> UE | None:
        for ue in self._ues:
            if ue.title == name: return ue
        return None

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        grade, coeff = 0, 0
        for ue in self._ues:
            if ue.average is None: continue

            grade += ue.average * ue.coefficient
            coeff += ue.coefficient

        if coeff == 0: return None

        self._avg = grade / coeff

        return self._avg

    @property
    def new_grade_count(self) -> int:
        if self._new_grade_count == None: self._new_grade_count = sum(ue.new_grade_count for ue in self._ues)
        return self._new_grade_count

    @property
    def new_grades_str(self) -> list[str]:
        lst = []

        for ue in self._ues:
            if ue.new_grade_count <= 0: continue
            
            for s in ue.new_grades_str:
                lst.append(s)

        return lst

    @new_grade_count.setter
    def new_grade_count(self, value: int) -> None:
        self._new_grade_count = value

    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = any(ue.has_missing_data for ue in self._ues)
        return self._has_missing_data

    def set_as_new(self) -> None:
        for ue in self._ues: ue.set_as_new()

    def __str__(self) -> str:
        return f'Semester {self._id}\n' + '\n'.join([f'\t{ue}' for ue in self._ues])

    def to_json(self) -> dict:
        return {
            'id': self._id,
            'ues': [ue.to_json() for ue in self._ues]
        }

    @staticmethod
    def from_json(json: dict) -> 'Semester':
        return Semester(
            json['id'],
            [UE.from_json(ue) for ue in json['ues']]
        )
#----------------------------------------------------------------------
