
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

    @property
    def id(self) -> int:
        return self._id

    @property
    def ues(self) -> list[UE]:
        return self._ues.copy()

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

    def __str__(self) -> str:
        return f'Semester {self.id}\n' + '\n'.join([f'\t{ue}' for ue in self.ues])
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'ues': [ue.to_json() for ue in self.ues]
        }
    
    @staticmethod
    def from_json(json: dict) -> 'Semester':
        return Semester(
            json['id'],
            [UE.from_json(ue) for ue in json['ues']]
        )
#----------------------------------------------------------------------
