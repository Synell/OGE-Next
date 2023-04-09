
#----------------------------------------------------------------------

    # Libraries
from .NoteGroup import NoteGroup
#----------------------------------------------------------------------

    # Class
class Matiere:
    def __init__(self, title: str, coeff: float, note_groups: list[NoteGroup]) -> None:
        self._title = title
        self._coeff = coeff
        self._note_groups = note_groups

    @property
    def title(self) -> str:
        return self._title

    @property
    def coeff(self) -> float:
        return self._coeff

    @property
    def note_groups(self) -> list[NoteGroup]:
        return self._note_groups.copy()

    @property
    def moyenne(self) -> float|None:
        note, coeff = 0, 0
        for note_group in self._note_groups:
            if note_group.moyenne is None: continue

            note += note_group.moyenne * note_group.coeff
            coeff += note_group.coeff

        if coeff == 0: return None

        return note / coeff

    def __str__(self) -> str:
        return f'{self.title} ({self.coeff})\n\t' + '\n'.join([f'\t{note_group}' for note_group in self.note_groups]).replace('\n', '\n\t')
#----------------------------------------------------------------------
