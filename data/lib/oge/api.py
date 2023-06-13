#----------------------------------------------------------------------

    # Libraries
from bs4.element import Tag, ResultSet
from requests import session, Session
import re, traceback, os
from bs4 import BeautifulSoup as BS
from .Grade import Grade
from .GradeGroup import GradeGroup
from .Subject import Subject
from .Pole import Pole
from .UE import UE
from .Semester import Semester
from .InfoType import InfoType
from PySide6.QtCore import QObject, Signal
#----------------------------------------------------------------------

    # Class
class OGE(QObject):
    info_changed = Signal(InfoType, str)
    failed = Signal(Exception)

    _URL_WEBSITE = 'http://casiut21.u-bourgogne.fr/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge%2F'
    _URL_GRADES = 'https://iutdijon.u-bourgogne.fr/oge/stylesheets/etu/bilanEtu.xhtml'

    def __init__(self, username: str, password: str) -> None:
        super().__init__()

        self._username = username
        self._password = password
        self._semester_data: dict[int, Semester] = {}
        self._semester_count = 0


    @property
    def semester_count(self) -> int:
        return self._semester_count


    @property
    def loaded_semesters(self) -> list[int]:
        return list(self._semester_data.keys())


    def set_data_from_json(self, json: list[dict]) -> None:
        self._semester_data = {}

        self._semester_count = json['semester_count']

        for semester in json['semesters']:
            s = Semester.from_json(semester)
            self._semester_data[s.id] = s


    def get_data_as_json(self) -> dict:
        return {
            'semester_count': self._semester_count,
            'semesters': [self._semester_data[semester].to_json() for semester in self._semester_data if self._semester_data[semester].id != self._semester_count]
        }


    def get_semestre_data(self, semester: int, force: bool = False) -> Semester:
        html = None

        try:
            if (semester not in self._semester_data) or force:
                html, sc = self._get_html(semester)
                self._semester_count = max(sc, self._semester_count)

                self._semester_data[semester] = Semester(semester, self._parse_html(html))

            return self._semester_data[semester]

        except Exception as err:
            self.info_changed.emit(InfoType.Error, str(err))
            self.failed.emit(Exception('An error has occurred while trying to get or parse OGE data!\nYou can find more information in the api-error.log file.'))

            if html:
                if not os.path.exists('./log/'): os.mkdir('./log/')
                with open(f'./log/api-error.log', 'w', encoding='utf-8') as file:
                    file.write(f'OGE API crashed!\n\n-----=====<( Python Traceback )>=====-----\n\n{traceback.format_exc()}\n\n\n-----=====<( HTML Code )>=====-----\n\n{html.prettify()}')


    def _get_key(self, session: Session) -> str:
        self.info_changed.emit(InfoType.Info, 'Trying to get a key...')

        try:
            key_results = re.findall(r'name=\"execution\" value=\"(.*?)\"/>', session.get(self._URL_WEBSITE).text)

        except Exception as err:
            raise Exception(f'Unable to get a key!\n{err}')

        if(len(key_results) == 0):
            raise Exception('Couldn\'t find a key!')

        else:
            self.info_changed.emit(InfoType.Success, 'Key obtained successfully!')
            return key_results[0]


    def _get_view_state(self, session_: Session) -> str:
        self.info_changed.emit(InfoType.Info, 'Trying to get a viewState key...')

        try:
            r = session_.get(self._URL_GRADES)
            id = re.findall(r'<li class=\"ui-tabmenuitem(?:.*?)onclick=\"PrimeFaces\.ab\({s:&quot;(.*?)&quot;,f:(?:.*?)</li>', r.text)
            view_state = re.findall(r'id=\"javax\.faces\.ViewState\" value=\"(.*?)\" />', r.text)

        except Exception as e:
            raise Exception(f'Unable to get a viewState key!\n{e}')

        if(len(id) == 0 or len(view_state) == 0):
            raise Exception('Couldn\'t find a valid viewState key!')

        else:
            self.info_changed.emit(InfoType.Success, 'Key obtained successfully!')
            return id[0], view_state[0]


    def _get_html(self, semester: int) -> tuple[BS, int]:
        session_ = session()

        data = {
            'username': self._username,
            'password': self._password,
            'execution': self._get_key(session_),
            '_eventId': 'submit',
            'geolocation' : ''
        }

        self.info_changed.emit(InfoType.Info, 'Creating a new session...')

        request = session_.post(self._URL_WEBSITE, data, {'referer': self._URL_WEBSITE})

        if request.status_code == 200:
            self.info_changed.emit(InfoType.Success, 'Session successfully created!')

        else:
            raise Exception(f'A connection error has occurred! (Status Code {request.status_code})')

        self.info_changed.emit(InfoType.Info, 'Waiting for GET request...')

        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'mainBilanForm:j_id_15',
            'javax.faces.partial.execute': 'mainBilanForm:j_id_15',
            'javax.faces.partial.render': 'mainBilanForm',
            'mainBilanForm:j_id_15': 'mainBilanForm:j_id_15',
            'i': str(semester - 1),
            'mainBilanForm:j_id_15_menuid': str(semester - 1),
            'mainBilanForm_SUBMIT': '1',
            'javax.faces.ViewState': self._get_view_state(session_)[1]
        }

        self.info_changed.emit(InfoType.Info, 'Waiting for POST request...')

        code = session_.post(self._URL_GRADES, data, headers = {'referer': self._URL_GRADES})

        session_.close()

        code = BS(code.text, 'lxml')

        semestre_count = len(code.find_all('a', attrs={'class': 'ui-menuitem-link ui-corner-all'}))

        return code, semestre_count


    def _parse_title_coeff(self, div: Tag) -> tuple[str, float]:
        title = list(div.children)[0].text.strip().replace('\n', '')
        coeff = float(div.find('span').text.strip().replace('\n', '').replace('(', '').replace(')', ''))
        return title, coeff

    def _parse_html(self, code: BS) -> list[UE]:
        log = [] # for debug

        self.info_changed.emit(InfoType.Info, 'Parsing OGE data...')

        data = []

        for moy_ue in code.find_all('table'):
            thead = moy_ue.find('thead')
            ue_div = thead.find('div')

            ue, ue_coeff = self._parse_title_coeff(ue_div)
            # print(ue, ue_coeff)

            tbody = moy_ue.find('tbody')

            rows: list[Tag]|ResultSet = tbody.find_all('tr')
            if len(rows) == 0: raise Exception('Couldn\'t find children in source code!')

            resource_tag = rows.pop(0)

            if resource_tag.attrs.get('class', None) != ['cell_BUT_RESSOURCE']:
                raise Exception('Couldn\'t find valid children in source code!')

            name_resource, coeff_resource = self._parse_title_coeff(resource_tag.find('td').find('span'))
            # print('>', name_resource, coeff_resource)

            is_sae = False

            matieres_resource: list[Subject] = []

            name_sae = ''
            coeff_sae = 0.0
            matieres_sae: list[Subject] = []

            for row in rows:
                if row.attrs.get('class', None) == ['cell_BUT_SAE']:
                    is_sae = True
                    name_sae, coeff_sae = self._parse_title_coeff(row.find('td').find('span'))
                    # print('>', name_sae, coeff_sae)
                    continue

                matiere_tag: list[Tag]|ResultSet = row.find('td').find_all('div')

                if len(matiere_tag) == 0:
                    log.append(f'Couldn\'t find valid children (row.find(\'td\').find_all(\'div\')) in source code!\nChildren:\n{matiere_tag.__repr__()}')
                    continue

                matiere_children: list[Tag]|ResultSet = matiere_tag.pop(0).find_all('span')
                matiere = matiere_children[0].text.strip().replace('\n', '')
                if len(matiere_children) == 1: matiere_coeff = 0.0 # bc OGE sucks
                else: matiere_coeff = float(matiere_children[1].text.strip().replace('\n', '').replace('(', '').replace(')', ''))
                # print('>>', matiere, matiere_coeff)

                note_groups: list[GradeGroup] = []

                for note_tag in matiere_tag:
                    children = list(note_tag.children)
                    if len(children) < 2:
                        log.append(f'Couldn\'t find valid children (note_tag.children) in source code!\nChildren:\n{children.__repr__()}')
                        continue

                    name = children.pop(0).text.replace('\n', '').replace('[', '').strip()

                    while children[-1].text == '\n':
                        children.pop(-1)

                    coeff = float(children.pop(-1).text.replace('\n', '').replace('(', '').replace(')', '').strip())
                    # print('>>>', name, coeff)

                    notes: list[Grade] = []

                    while children:
                        child = children.pop(0)

                        if isinstance(child, Tag):
                            if child.name == 'span':
                                if len(children) < 2:
                                    log.append(f'Couldn\'t find valid children (while note_tag.children) in source code!\nChildren:\n{children.__repr__()}')
                                    continue

                                note = float(child.text.strip().replace('\n', ''))

                                child = children.pop(0)
                                total = float(child.text.replace('\n', '').replace('/', '').strip())

                                child = children.pop(0).find('span')
                                coef = float(child.text.replace('\n', '').replace('(', '').replace(')', '').strip())

                                # print('>>>>', f'{note}/{total}', coef)
                                notes.append(Grade(note, total, coef))

                    note_group = GradeGroup(name, coeff, notes)
                    note_groups.append(note_group)

                matiere = Subject(matiere, matiere_coeff, note_groups)

                if is_sae:
                    matieres_sae.append(matiere)

                else:
                    matieres_resource.append(matiere)

            ue = UE(
                ue,
                ue_coeff,
                [
                    Pole(name_resource, coeff_resource, matieres_resource),
                    Pole(name_sae, coeff_sae, matieres_sae)
                ]
            )
            data.append(ue)

        if log:
            if not os.path.exists('./log/'): os.mkdir('./log/')

            with open(f'./log/api-warnings.log', 'w', encoding='utf-8') as file:
                file.write(f'OGE API warnings!\n\n-----=====<( API Warnings ({len(log)}) )>=====-----\n\n' + ('\n' + ('-' * 50) + '\n').join(log))

        return data
#----------------------------------------------------------------------
