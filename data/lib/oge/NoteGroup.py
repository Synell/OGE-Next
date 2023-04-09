
#----------------------------------------------------------------------

    # Libraries
from .Note import Note
#----------------------------------------------------------------------

    # Class
class NoteGroup:
    def __init__(self, title: str, coeff: float, notes: list[Note]) -> None:
        self._title = title
        self._coeff = coeff
        self._notes = notes

    @property
    def title(self) -> str:
        return self._title

    @property
    def coeff(self) -> float:
        return self._coeff

    @property
    def notes(self) -> list[Note]:
        return self._notes.copy()

    @property
    def moyenne(self) -> float|None:
        note, coeff = 0, 0
        for note_ in self._notes:
            note += note_.value_20 * note_.coeff
            coeff += note_.coeff

        if coeff == 0: return None

        return note / coeff

    def __str__(self) -> str:
        return f'{self.title} ({self.coeff})\n\t' + '\n'.join([f'\t{note}' for note in self.notes]).replace('\n', '\n\t')
#----------------------------------------------------------------------
