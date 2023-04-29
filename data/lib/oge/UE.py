
#----------------------------------------------------------------------

    # Libraries
from .Pole import Pole
#----------------------------------------------------------------------

    # Class
class UE:
    def __init__(self, title: str, coefficient: float, poles: list[Pole]) -> None:
        self._title = title
        self._coefficient = coefficient
        self._poles = poles
        self._avg = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def poles(self) -> list[Pole]:
        return self._poles.copy()

    @property
    def average(self) -> float|None:
        if self._avg is not None: return self._avg

        grade, coeff = 0, 0
        for pole in self._poles:
            if pole.average is None: continue

            grade += pole.average * pole.coefficient
            coeff += pole.coefficient

        if coeff == 0: return None

        self._avg = grade / coeff

        return self._avg

    def __str__(self) -> str:
        return f'{self.title} ({self.coefficient})\n' + '\n'.join([f'\t{pole}' for pole in self.poles])
    
    def to_json(self) -> dict:
        return {
            'title': self.title,
            'coefficient': self.coefficient,
            'poles': [pole.to_json() for pole in self.poles]
        }
    
    @staticmethod
    def from_json(json: dict) -> 'UE':
        return UE(
            json['title'],
            json['coefficient'],
            [Pole.from_json(pole) for pole in json['poles']]
        )
#----------------------------------------------------------------------
