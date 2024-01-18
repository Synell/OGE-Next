#----------------------------------------------------------------------

    # Libraries
import json
from typing import Union
from PySide6.QtCore import QObject, Signal

from .QLangData import QLangData
from .QAppType import QAppType
#----------------------------------------------------------------------

    # Class
class QLangDataManager(QObject):
    warning_received = Signal(str)


    def __init__(self) -> None:
        super().__init__()

        self._data = QLangData.NoTranslation()


    def load(self, language_path: str, app_type: QAppType) -> None:
        try:
            with open(f'{language_path}.json', 'r', encoding = 'utf-8') as infile:
                filename = json.load(infile)['root'][app_type.value]

            with open(f'{language_path}/{filename}.json', 'r', encoding = 'utf-8') as infile:
                self._data = QLangData(json.load(infile), f'{language_path}/', f'{language_path}/{filename}.json')
                self._data.warning_received.connect(self.warning_received.emit)

        except Exception as e:
            self.warning_received.emit(f'Failed to load language data from {language_path}: {e}')
            self._data = QLangData.NoTranslation()


    def get(self, path: str) -> Union[str, QLangData, list[Union[str, QLangData]]]:
        return self._data.get(path)


    def __getitem__(self, path: str) -> Union[str, QLangData, list[Union[str, QLangData]]]:
        return self.get(path)


    def __getattr__(self, path: str) -> Union[str, QLangData, list[Union[str, QLangData]]]:
        return self.get(path)


    def __call__(self, path: str) -> Union[str, QLangData, list[Union[str, QLangData]]]:
        return self.get(path)
#----------------------------------------------------------------------
