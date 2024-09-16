#----------------------------------------------------------------------

    # Libraries
from .QFileExplorer import QFileExplorer
import json
#----------------------------------------------------------------------

    # Class
class QData:
    class QLang:
        def __init__(self, lang_folder: str, lang_path: str) -> None:
            with open(f'{lang_folder}/{lang_path}', encoding = 'utf-8') as infile:
                data = json.load(infile)
                info: dict = data['info']

                self._display_name = info.get('name', '???')
                self._version = info.get('version', 'v1.0')
                self._author = info.get('author', '???')
                self._description = info.get('description', '')

                self._filename = '.'.join(lang_path.split('.')[:-1])


        @property
        def display_name(self) -> str:
            return self._display_name

        @property
        def version(self) -> str:
            return self._version

        @property
        def author(self) -> str:
            return self._author

        @property
        def description(self) -> str:
            return self._description

        @property
        def filename(self) -> str:
            return self._filename


    class QTheme:
        def __init__(self, themes_folder: str, theme_path: str) -> None:
            with open(f'{themes_folder}/{theme_path}', encoding = 'utf-8') as infile:
                data = json.load(infile)
                info: dict = data['info']

                self._display_name = info.get('name', '???')
                self._version = info.get('version', 'v1.0')
                self._author = info.get('author', '???')
                self._desc = info.get('description', '')

                self._filename = '.'.join(theme_path.split('.')[:-1])
                self._variants = data['qss']


        @property
        def display_name(self) -> str:
            return self._display_name

        @property
        def version(self) -> str:
            return self._version

        @property
        def author(self) -> str:
            return self._author

        @property
        def description(self) -> str:
            return self._desc

        @property
        def filename(self) -> str:
            return self._filename

        @property
        def variants(self) -> list[str]:
            return self._variants



    def __init__(self, lang_folder: str, themes_folder: str) -> None:
        self._langs: tuple[QData.QLang] = []
        for file in QFileExplorer.get_files(lang_folder, ['json'], False, True):
            self._langs.append(self.QLang(lang_folder, file))
        self._langs = tuple(self._langs)

        self._themes: list[QData.QTheme] = []
        for file in QFileExplorer.get_files(themes_folder, ['json'], False, True):
            self._themes.append(self.QTheme(themes_folder, file))
        self._themes = tuple(self._themes)


    @property
    def langs(self) -> 'tuple[QData.QLang]':
        return self._langs

    @property
    def themes(self) -> 'tuple[QData.QTheme]':
        return self._themes
#----------------------------------------------------------------------
