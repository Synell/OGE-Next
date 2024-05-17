#----------------------------------------------------------------------

    # Libraries
from .UE import UE
#----------------------------------------------------------------------

    # Class
class UEAvg:
    def __init__(self, ues: tuple[UE]) -> None:
        self._ues = ues
        self._avg = None
        self._has_missing_data = None


    @property
    def ues(self) -> tuple[UE]:
        return self._ues


    @property
    def title(self) -> str:
        return self._ues[-1].title


    @property
    def coefficient(self) -> float:
        return sum([ue.coefficient for ue in self._ues if ue.coefficient is not None]) / max(sum([1 for ue in self._ues if ue.coefficient is not None]), 1)


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
    def has_missing_data(self) -> bool:
        if self._has_missing_data is not None: return self._has_missing_data

        self._has_missing_data = any([ue.has_missing_data for ue in self._ues])

        return self._has_missing_data


    @property
    def is_only_missing_coefficient(self) -> bool:
        return any([ue.is_only_missing_coefficient for ue in self._ues])
#----------------------------------------------------------------------
