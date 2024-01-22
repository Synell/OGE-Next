#----------------------------------------------------------------------

    # Libraries
from bs4.element import Tag, ResultSet
from requests import session, Session
import re, traceback, os, warnings
from bs4 import BeautifulSoup as BS
from bs4 import XMLParsedAsHTMLWarning
from collections import namedtuple
from datetime import datetime
from .Grade import Grade
from .GradeGroup import GradeGroup
from .Subject import Subject
from .Pole import Pole
from .UE import UE
from .Semester import Semester
from .InfoType import InfoType
from .RankMode import RankMode
from PySide6.QtCore import QObject, Signal
#----------------------------------------------------------------------

    # Setup
warnings.filterwarnings('ignore', category = XMLParsedAsHTMLWarning)
#----------------------------------------------------------------------

    # Class
class OGE(QObject):
    info_changed = Signal(InfoType, str)
    failed = Signal(Exception)

    _URL_WEBSITE = 'http://casiut21.u-bourgogne.fr/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge%2F'
    _URL_GRADES = 'https://iutdijon.u-bourgogne.fr/oge/stylesheets/etu/bilanEtu.xhtml'
    _URL_DETAILS = 'https://iutdijon.u-bourgogne.fr/oge/stylesheets/etu/detailsEtu.xhtml'

    _details_info = namedtuple('DetailsInfo', ['date', 'name', 'value', 'value_total', 'coefficient', 'rank', 'rank_total'])

    def __init__(self, username: str, password: str) -> None:
        super().__init__()

        self._username = username
        self._password = password
        self._semester_data: dict[int, Semester] = {}
        self._semester_count = 0
        self._new_semester: Semester = None


    @property
    def semester_count(self) -> int:
        return self._semester_count


    @property
    def loaded_semesters(self) -> list[int]:
        return list(self._semester_data.keys())


    def set_data_from_json(self, json: dict) -> None:
        self._semester_data = {}

        self._semester_count = json['semester_count']

        for semester in json['semesters']:
            s = None

            try: s = Semester.from_json(semester)
            except: continue

            self._semester_data[s.id] = s

        if json.get('last_semester', None) is not None:
            s = Semester.from_json(json['last_semester'])

            if s.id == self._semester_count:
                self._new_semester = s


    def get_data_as_json(self) -> dict:
        return {
            'semester_count': self._semester_count,
            'semesters': [self._semester_data[semester].to_json() for semester in self._semester_data if self._semester_data[semester].id != self._semester_count],
            'last_semester': self._semester_data[self._semester_count].to_json() if self._semester_count in self._semester_data else None
        }


    def get_semester_data(self, semester: int, rank_mode: RankMode = RankMode.OnlyForNewGrades, force: bool = False) -> Semester:
        html = None
        session_ = session()

        try:
            if (semester not in self._semester_data) or force:
                html, sc = self._get_grades_html(semester, session_)
                self._semester_count = max(sc, self._semester_count)

                new_grades = False

                self._semester_data[semester] = Semester(semester, self._parse_bilan_html(html))
                if semester == self._semester_count: new_grades = self._set_new()

                if (rank_mode == RankMode.OnlyForNewGrades and new_grades) or rank_mode == RankMode.All:
                    self._set_missing_ranks(session_, semester, rank_mode == RankMode.OnlyForNewGrades)

            return self._semester_data[semester]

        except Exception as err:
            self.info_changed.emit(InfoType.Error, str(err))
            self.failed.emit(Exception('An error has occurred while trying to get or parse OGE data!\nYou can find more information in the api-error.log file.'))

            if html:
                if not os.path.exists('./log/'): os.mkdir('./log/')
                with open(f'./log/api-error.log', 'w', encoding='utf-8') as file:
                    file.write(f'OGE API crashed!\n\n-----=====<( Python Traceback )>=====-----\n\n{traceback.format_exc()}\n\n\n-----=====<( HTML Code )>=====-----\n\n{html.prettify()}')

        session_.close()


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


    def _get_view_state(self, session_: Session, url: str, info_title: str) -> str:
        self.info_changed.emit(InfoType.Info, f'{info_title} > Trying to get a viewState key...')

        try:
            r = session_.get(url)
            id = re.findall(r'<li class=\"ui-tabmenuitem(?:.*?)onclick=\"PrimeFaces\.ab\({s:&quot;(.*?)&quot;,f:(?:.*?)</li>', r.text)
            view_state = re.findall(r'id=\"javax\.faces\.ViewState\" value=\"(.*?)\" />', r.text)

        except Exception as e:
            raise Exception(f'Unable to get a viewState key!\n{e}')

        if(len(id) == 0 or len(view_state) == 0):
            raise Exception('Couldn\'t find a valid viewState key!')

        else:
            self.info_changed.emit(InfoType.Success, 'Key obtained successfully!')
            return id[0], view_state[0]


    def _get_grades_html(self, semester: int, session: Session) -> tuple[BS, int]:
        data = {
            'username': self._username,
            'password': self._password,
            'execution': self._get_key(session),
            '_eventId': 'submit',
            'geolocation' : ''
        }

        self.info_changed.emit(InfoType.Info, 'Creating a new session...')

        request = session.post(self._URL_WEBSITE, data, {'referer': self._URL_WEBSITE})

        if request.status_code == 200:
            self.info_changed.emit(InfoType.Success, 'Session successfully created!')

        else:
            raise Exception(f'A connection error has occurred! (Status Code {request.status_code})')

        # self.info_changed.emit(InfoType.Info, 'Grades > Waiting for GET request...')

        s = 'mainBilanForm:j_id_15'
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': s,
            'javax.faces.partial.execute': s,
            'javax.faces.partial.render': 'mainBilanForm',
            s: s,
            'i': str(semester - 1),
            f'{s}_menuid': str(semester - 1),
            'mainBilanForm_SUBMIT': '1',
            'javax.faces.ViewState': self._get_view_state(session, self._URL_GRADES, 'Grades')[1]
        }

        self.info_changed.emit(InfoType.Info, 'Grades > Waiting for POST request...')

        code = session.post(self._URL_GRADES, data, headers = {'referer': self._URL_GRADES})

        code = BS(code.text, 'lxml')

        semester_count = len(code.find_all('a', attrs={'class': 'ui-menuitem-link ui-corner-all'}))

        return code, semester_count


    def _parse_title_coeff(self, div: Tag) -> tuple[str, float]:
        title = list(div.children)[0].text.strip().replace('\n', '')
        coeff_s = div.find('span').text.strip().replace('\n', '').replace('(', '').replace(')', '')
        coeff = float(coeff_s) if coeff_s else 0.0
        return title, coeff

    def _parse_bilan_html(self, code: BS) -> list[UE]:
        log = [] # for debug

        self.info_changed.emit(InfoType.Info, 'Grades > Parsing OGE data...')

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
                else:
                    s = matiere_children[1].text.strip().replace('\n', '').replace('(', '').replace(')', '')
                    if s: matiere_coeff: matiere_coeff = float(s)
                    else: matiere_coeff = 0.0
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

                                try: note = float(child.text.strip().replace('\n', ''))
                                except: note = None # bc OGE sucks

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


    def _set_new(self) -> bool:
        ret = False

        for i in range(self._semester_count - 1):
            if i not in self._semester_data: continue
            self._semester_data[i].new_grade_count = 0

        if self._new_semester is None:
            # self._semester_data[self._semester_count].set_as_new()
            return False

        for ue in self._semester_data[self._semester_count].ues:
            # Get UE
            ue_progress = self._new_semester.find_ue_by_name(ue.title)
            if ue_progress is None:
                ue.set_as_new()
                ret = True
                continue

            for pole in ue.poles:
                # Get Pole
                pole_progress = ue_progress.find_pole_by_name(pole.title)
                if pole_progress is None:
                    pole.set_as_new()
                    ret = True
                    continue

                for subject in pole.subjects:
                    # Get Subject
                    subject_progress = pole_progress.find_subject_by_name(subject.title)
                    if subject_progress is None:
                        subject.set_as_new()
                        ret = True
                        continue

                    for grade_group in subject.grade_groups:
                        # Get Grade Group
                        grade_group_progress = subject_progress.find_grade_group_by_name(grade_group.title)
                        if grade_group_progress is None:
                            grade_group.set_as_new()
                            ret = True
                            continue

                        lst_new = grade_group.grades.copy()
                        lst_old = grade_group_progress.grades.copy()

                        while lst_new and lst_old:
                            grade_new = lst_new[0]
                            grade_old = lst_old[0]

                            if grade_new == grade_old:
                                lst_new.pop(0)
                                lst_old.pop(0)

                                grade_new.name = grade_old.name
                                grade_new.date = grade_old.date
                                grade_new.rank = grade_old.rank
                                grade_new.rank_total = grade_old.rank_total

                                continue

                            grade_new.is_new = True
                            ret = True
                            lst_new.pop(0)

                        for grade in lst_new:
                            grade.is_new = True
                            ret = True

        return ret


    def _load_details_semester(self, session: Session, view_state_key: str, semester: int) -> None:
        s = f'mainFormDetailNote:j_id_16'
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': s,
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'mainFormDetailNote',
            s: s,
            'mainFormDetailNote:j_id_16_menuid': semester - 1,
            'mainFormDetailNote:j_id_1b_scrollState': '0,0',
            'mainFormDetailNote_SUBMIT': '1',
            'javax.faces.ViewState': view_state_key
        }

        self.info_changed.emit(InfoType.Info, 'Ranks > Change Loaded Semester > Waiting for POST request...')
        session.post(self._URL_DETAILS, data, headers = {'referer': self._URL_DETAILS})


    def _load_details_subject(self, session: Session, view_state_key: str, ue_id: int, ue_title: str, pole_id: int, pole_title: str, subject_id: int, subject_title: str) -> tuple[BS, int] | None:
        s = f'mainFormDetailNote:j_id_1b:0_{ue_id}_{pole_id}_{subject_id}:elpLink'
        data = {
            'mainFormDetailNote:j_id_1b_scrollState': '0,0',
            'mainFormDetailNote_SUBMIT': '1',
            'javax.faces.ViewState': view_state_key,
            'javax.faces.behavior.event': 'click',
            'javax.faces.partial.event': 'click',
            'javax.faces.source': s,
            'javax.faces.partial.ajax': 'true',
            'javax.faces.partial.execute': s,
            'mainFormDetailNote': 'mainFormDetailNote'
        }

        self.info_changed.emit(InfoType.Info, f'Ranks > Change Loaded Subject ({ue_title} > {pole_title} > {subject_title}) > Waiting for POST request...')
        session.post(self._URL_DETAILS, data, headers = {'referer': self._URL_DETAILS})

        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': s,
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'mainFormDetailNote:mainPanel',
            s: s,
            'mainFormDetailNote:j_id_1b_scrollState': '0,0',
            'mainFormDetailNote_SUBMIT': '1',
            'javax.faces.ViewState': view_state_key,
        }

        self.info_changed.emit(InfoType.Info, f'Ranks > Get Loaded Subject ([{ue_id}] {ue_title} > [{pole_id}] {pole_title} > [{subject_id}] {subject_title}) > Waiting for POST request...')
        response = session.post(self._URL_DETAILS, data, headers = {'referer': self._URL_DETAILS})
        if response.status_code != 200: return None

        code = None
        offset = 0
        if response.status_code == 200:
            code = BS(response.text, 'lxml')

            if code.text.find('Pas de notes saisies sur cette matière') != -1:
                self.info_changed.emit(InfoType.Warning, f'Ranks > Wrong Subject Offset ([{ue_id}] {ue_title} > [{pole_id}] {pole_title} > [{subject_id}] {subject_title}) > Trying to find the right offset...')
                code, offset = self._load_details_subject(session, view_state_key, ue_id, ue_title, pole_id, pole_title, subject_id + 1, subject_title)
                offset += 1

        return (code, offset) if code else None


    def _parse_details_html(self, code: BS) -> dict[str, list[_details_info]]:
        self.info_changed.emit(InfoType.Info, 'Ranks > Parsing OGE data...')

        div = code.find('div', attrs = {'id': 'mainFormDetailNote:listeEvaluation_content'})
        if not div: return tuple()

        values = {}

        for table in div.find_all('table'):
            group_name = table.find('thead').find('td').text.strip().replace('\n', '')
            values[group_name] = []

            for row in table.find('tbody').find_all('tr'):
                children: list[Tag] = list(row.children)
                if len(children) != 5: continue

                date = children[0].text.replace(children[0].find('span').text, '').strip()
                date = datetime.strptime(date, '%d/%m/%Y').date()
                name = children[1].text.strip()

                value_str = children[2].text.strip()
                value, value_total = None, None
                if value_str:
                    try: value, value_total = map(float, value_str.split('/'))
                    except: pass

                coeff_str = children[3].text.replace('coef.', '').strip()
                coeff = None
                if coeff_str:
                    try: coeff = float(coeff_str)
                    except: pass

                rank_spans = children[4].find_all('span')
                rank, rank_total = None, None
                if len(rank_spans) == 2:
                    rank_str = rank_spans[1].text.strip()
                    try: rank, rank_total = map(int, rank_str.split('/'))
                    except: pass

                values[group_name].append(self._details_info(date, name, value, value_total, coeff, rank, rank_total))

            if len(values[group_name]) == 0: del values[group_name]

        return values

    def _set_missing_ranks(self, session: Session, semester: int, only_for_new_grades: bool) -> None:
        view_state_key = self._get_view_state(session, self._URL_DETAILS, 'Ranks')[1]

        if self._semester_count != semester: self._load_details_semester(session, view_state_key, semester)

        for ue_id, ue in enumerate(self._semester_data[semester].ues):
            for pole_id, pole in enumerate(ue.poles):
                subject_id_offset = 0

                for subject_id, subject in enumerate(pole.subjects):
                    if subject.has_missing_rank_data(only_for_new_grades):
                        # print(f'Loading {ue.title} > {pole.title} > {subject.title}...')
                        bs, offset = self._load_details_subject(
                            session,
                            view_state_key,
                            ue_id,
                            ue.title,
                            pole_id,
                            pole.title,
                            subject_id + subject_id_offset,
                            subject.title
                        )
                        subject_id_offset += offset
                        if bs is None: continue

                        values = self._parse_details_html(bs)
                        # print(values)
                        if 'Sensi programm multimédia' == subject.title: print(values, f'mainFormDetailNote:j_id_1b:0_{ue_id}_{pole_id}_{subject_id + subject_id_offset}:elpLink', bs)
                        if not values: continue

                        for grade_group in subject.grade_groups:
                            if grade_group.has_missing_rank_data(only_for_new_grades):
                                # print(f'Loading {ue.title} > {pole.title} > {subject.title} > {grade_group.title}...')

                                for group_name in values:
                                    if grade_group.title in group_name:
                                        # print(f'Loading {ue.title} > {pole.title} > {subject.title} > {grade_group.title} > {group_name}...')
                                        if len(values[group_name]) != len(grade_group.grades): continue

                                        grades = grade_group.grades.copy()

                                        while values[group_name] and grades:
                                            grade = values[group_name].pop(0)

                                            for i, g in enumerate(grades):
                                                if g.value == grade.value and g.value_total == grade.value_total and g.coefficient == grade.coefficient:
                                                    # print(f'Found {ue.title} > {pole.title} > {subject.title} > {grade_group.title} > {group_name} > {g.name}')
                                                    g.name = grade.name
                                                    g.date = grade.date
                                                    g.rank = grade.rank
                                                    g.rank_total = grade.rank_total
                                                    grades.pop(i)
                                                    break
#----------------------------------------------------------------------
