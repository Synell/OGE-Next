
#----------------------------------------------------------------------

    # Libraries
from .UE import UE
from .SemesterName import SemesterName
#----------------------------------------------------------------------

    # Class
class Semester:
    def __init__(self, id_: int, name: SemesterName | str | None, ues: list[UE]) -> None:
        self._id = id_
        self._semester_name = name if isinstance(name, SemesterName) else SemesterName.from_string(name)
        self._ues = ues
        self._avg = None
        self._new_grade_count = None
        self._has_missing_data = None
        self._has_missing_ue_data = None


    @property
    def id(self) -> int:
        return self._id


    @property
    def number(self) -> int:
        return self._semester_name.number if self._semester_name is not None else None


    @property
    def years(self) -> tuple[int, int]:
        return (self._semester_name.start_year, self._semester_name.end_year) if self._semester_name is not None else (None, None)


    @property
    def raw_name(self) -> str:
        return self._semester_name.raw_name if self._semester_name is not None else None

    @raw_name.setter
    def raw_name(self, value: str) -> None:
        self._semester_name = SemesterName.from_string(value)


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
    def average(self) -> float | None:
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
    def new_grades_str(self) -> str:
        return '\n\n\n'.join(ue.new_grades_str.replace('\n', '\n        ') for ue in self._ues if ue.new_grade_count > 0)

    @new_grade_count.setter
    def new_grade_count(self, value: int) -> None:
        self._new_grade_count = value


    @property
    def has_missing_ue_data(self) -> bool:
        if self._has_missing_ue_data is None: self._has_missing_ue_data = any(ue.has_missing_data for ue in self._ues)
        return self._has_missing_ue_data


    @property
    def has_missing_data(self) -> bool:
        if self._has_missing_data is None: self._has_missing_data = self.has_missing_ue_data
        return self._has_missing_data


    def set_as_new(self) -> None:
        for ue in self._ues: ue.set_as_new()


    def __str__(self) -> str:
        return f'Semester {self._id}\n' + '\n'.join([f'\t{ue}' for ue in self._ues])


    def to_json(self) -> dict:
        return {
            'id': self._id,
            'name': self._semester_name.to_json() if self._semester_name is not None else None,
            'ues': [ue.to_json() for ue in self._ues]
        }


    @staticmethod
    def from_json(json: dict) -> 'Semester':
        raw_name = json.get('rawName', None)
        semester_name = json.get('name', None)

        return Semester(
            json['id'],
            SemesterName.from_json(raw_name if raw_name is not None else semester_name),
            [UE.from_json(ue) for ue in json['ues']]
        )
#----------------------------------------------------------------------
