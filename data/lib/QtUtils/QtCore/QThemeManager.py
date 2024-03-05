#----------------------------------------------------------------------

    # Libraries
import json, os
from PySide6.QtCore import QObject, Signal

from ..QtGui.QColorSet import QColorSet
#----------------------------------------------------------------------

    # Class
class QThemeManager(QObject):
    warning_received = Signal(str)


    def __init__(self, main_color_set: QColorSet, neutral_color_set: QColorSet) -> None:
        super().__init__()

        self._data_global = ''
        self._data_local = ''
        self._main_color_set: QColorSet = main_color_set
        self._neutral_color_set: QColorSet = neutral_color_set


    @property
    def main_color_set(self) -> QColorSet:
        return self._main_color_set


    @property
    def neutral_color_set(self) -> QColorSet:
        return self._neutral_color_set


    def load(self, themes_folder: str, theme: str, theme_variant: str) -> None:
        try:
            self._load_global(themes_folder, theme, theme_variant)
            self._load_local(themes_folder, theme, theme_variant)

        except Exception as e:
            self.warning_received.emit(f'Failed to load theme data from {themes_folder}/{theme}/{theme_variant}: {e}')
            self._data_global = ''
            self._data_local = ''


    def _load_global(self, themes_folder: str, theme: str, theme_variant: str) -> None:
        self._data_global = ''

        with open(f'{themes_folder}/{theme}.json', 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)['qss']
            path = data[theme_variant]['location']

        if os.path.exists(f'data/lib/QtUtils/themes/{theme}/{theme_variant}/{path}/main.json'):
            with open(f'data/lib/QtUtils/themes/{theme}/{theme_variant}/{path}/main.json', 'r', encoding = 'utf-8') as infile:
                files = json.load(infile)['files']

            for file in files:
                with open(f'data/lib/QtUtils/themes/{theme}/{theme_variant}/{path}/{file}.qss', 'r', encoding = 'utf-8') as infile:
                    self._data_global += infile.read()

            self._data_global = self._data_global.replace(
                '{path}',
                f'data/lib/QtUtils/themes/{theme}/{theme_variant}/{path}/icons/'.replace('//', '/')
            )

            self._data_global = self._data_global.replace('{main-color-name}', self._main_color_set.name)
            for key, value in self._main_color_set.items:
                self._data_global = self._data_global.replace(f'{{main-{key}}}', value.hex[1:])

            self._data_global = self._data_global.replace('{neutral-color-name}', self._neutral_color_set.name)
            for key, value in self._neutral_color_set.items:
                self._data_global = self._data_global.replace(f'{{neutral-{key}}}', value.hex[1:])


    def _load_local(self, themes_folder: str, theme: str, theme_variant: str) -> None:
        self._data_local = ''

        with open(f'{themes_folder}/{theme}.json', 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)['qss']
            path = data[theme_variant]['location']

        with open(f'{themes_folder}/{theme}/{theme_variant}/{path}/main.json', 'r', encoding = 'utf-8') as infile:
            files = json.load(infile)['files']

        for file in files:
            with open(f'{themes_folder}/{theme}/{theme_variant}/{path}/{file}.qss', 'r', encoding = 'utf-8') as infile:
                self._data_local += infile.read()

        self._data_local = self._data_local.replace('{path}', f'{themes_folder}/{theme}/{theme_variant}/icons/'.replace('//', '/'))

        self._data_local = self._data_local.replace('{main-color-name}', self._main_color_set.name)
        for key, value in self._main_color_set.items:
            self._data_local = self._data_local.replace(f'{{main-{key}}}', value.hex[1:])

        self._data_local = self._data_local.replace('{neutral-color-name}', self._neutral_color_set.name)
        for key, value in self._neutral_color_set.items:
            self._data_local = self._data_local.replace(f'{{neutral-{key}}}', value.hex[1:])


    def get_global(self) -> str:
        return self._data_global


    def get_local(self) -> str:
        return self._data_local
#----------------------------------------------------------------------
