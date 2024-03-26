
#----------------------------------------------------------------------

    # Libraries
from .UE import UE
import re
#----------------------------------------------------------------------

    # Class
class Semester:
    def __init__(self, id_: int, raw_name: str, ues: list[UE]) -> None:
        self._id = id_
        self.raw_name = raw_name
        self._ues = ues
        self._avg = None
        self._new_grade_count = None
        self._has_missing_data = None
        self._has_missing_ue_data = None


    @property
    def id(self) -> int:
        return self._id


    @property
    def raw_name(self) -> str:
        return self._raw_name

    @raw_name.setter
    def raw_name(self, value: str) -> None:
        self._raw_name = value

        try:
            pattern = re.compile(r'(\d{4})\/(\d{4})-(?:.*)[A-Za-z] (\d+)')
            year1, year2, sm_n = pattern.findall(value)[0]
            year1, year2, sm_n = int(year1), int(year2), int(sm_n)

            self._number = sm_n
            self._years = (year1, year2)

        except:
            self._number = None
            self._years = (None, None)


    @property
    def number(self) -> int:
        return self._number


    @property
    def years(self) -> tuple[int, int]:
        return self._years


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
            'rawName': self._raw_name,
            'ues': [ue.to_json() for ue in self._ues]
        }


    @staticmethod
    def from_json(json: dict) -> 'Semester':
        return Semester(
            json['id'],
            json.get('rawName', f'Semester {json["id"]} (?)'),
            [UE.from_json(ue) for ue in json['ues']]
        )
#----------------------------------------------------------------------
