
#----------------------------------------------------------------------

    # Libraries
from .Pole import Pole
#----------------------------------------------------------------------

    # Class
class UE:
    def __init__(self, title: str, coeff: float, poles: list[Pole]) -> None:
        self._title = title
        self._coeff = coeff
        self._poles = poles

    @property
    def title(self) -> str:
        return self._title

    @property
    def coeff(self) -> float:
        return self._coeff

    @property
    def poles(self) -> list[Pole]:
        return self._poles.copy()

    @property
    def moyenne(self) -> float|None:
        note, coeff = 0, 0
        for pole in self._poles:
            if pole.moyenne is None: continue

            note += pole.moyenne * pole.coeff
            coeff += pole.coeff

        if coeff == 0: return None

        return note / coeff

    def __str__(self) -> str:
        return f'{self.title} ({self.coeff})\n' + '\n'.join([f'\t{pole}' for pole in self.poles])
#----------------------------------------------------------------------
