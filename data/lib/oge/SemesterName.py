
#----------------------------------------------------------------------

    # Libraries
import re
#----------------------------------------------------------------------

    # Class
class SemesterName:
    def __init__(self, number: int, start_year: int, end_year: int) -> None:
        self._number = number
        self._start_year = start_year
        self._end_year = end_year


    @staticmethod
    def from_string(string: str | None) -> 'SemesterName':
        if string is None: return None

        s = SemesterName(None, None, None)

        try:
            pattern = re.compile(r'(\d{4})\/(\d{4})-(?:.*)[A-Za-z] (\d+)')
            year1, year2, sm_n = pattern.findall(string)[0]
            year1, year2, sm_n = int(year1), int(year2), int(sm_n)

            s._number = sm_n
            s._start_year, s._end_year = (year1, year2)

        except:
            return None

        return s


    @property
    def number(self) -> int:
        return self._number


    @property
    def start_year(self) -> int:
        return self._start_year


    @property
    def end_year(self) -> int:
        return self._end_year


    @property
    def years(self) -> tuple[int, int]:
        return (self._start_year, self._end_year)


    @property
    def raw_name(self) -> str:
        return f'{self._start_year}/{self._end_year} - Semester {self._number}'


    def to_json(self) -> dict:
        return {
            'number': self._number,
            'startYear': self._start_year,
            'endYear': self._end_year
        }


    @staticmethod
    def from_json(d: dict | str) -> 'SemesterName | None':
        if d is None: return None
        if isinstance(d, str): return SemesterName.from_string(d)
        return SemesterName(d['number'], d['startYear'], d['endYear'])


    def __repr__(self) -> str:
        return f'SemesterName({self.raw_name})'
#----------------------------------------------------------------------
