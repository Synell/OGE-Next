
#----------------------------------------------------------------------

    # Libraries
from .Matiere import Matiere
#----------------------------------------------------------------------

    # Class
class Pole:
    def __init__(self, title: str, coeff: float, matieres: list[Matiere]) -> None:
        self._title = title
        self._coeff = coeff
        self._matieres = matieres
        self._avg = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coeff(self) -> float:
        return self._coeff

    @property
    def matieres(self) -> list[Matiere]:
        return self._matieres.copy()

    @property
    def moyenne(self) -> float|None:
        if self._avg is not None: return self._avg

        note, coeff = 0, 0
        for matiere in self._matieres:
            if matiere.moyenne is None: continue

            note += matiere.moyenne * matiere.coeff
            coeff += matiere.coeff

        if coeff == 0: return None

        self._avg = note / coeff

        return self._avg

    def __str__(self) -> str:
        return f'{self.title} ({self.coeff})\n\t' + '\n'.join([f'\t{matiere}' for matiere in self.matieres]).replace('\n', '\n\t')
#----------------------------------------------------------------------
