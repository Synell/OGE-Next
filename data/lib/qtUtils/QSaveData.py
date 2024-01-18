#----------------------------------------------------------------------

    # Libraries
from typing import Callable
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
import json, os
from enum import Enum
from contextlib import suppress
from typing import Union

from .QMessageBoxWithWidget import QMessageBoxWithWidget
from . import QBaseApplication
from .QSettingsDialog import QSettingsDialog
from .QUtilsColor import QUtilsColor
from .QAppType import QAppType
from .QLangDataManager import QLangDataManager, QLangData
from .QThemeManager import QThemeManager, QColorSet
#----------------------------------------------------------------------

    # Class
class QSaveData(QObject):
    warning_received = Signal(str)


    class StyleSheetMode(Enum):
        All = 'all'
        Global = 'global'
        Local = 'local'


    class IconMode(Enum):
        Global = 'global'
        Local = 'local'


    def __init__(self,
        app: QBaseApplication,
        save_path = './data/save.dat',
        lang_folder = './data/lang/',
        themes_folder = './data/themes/',
        default_language = 'english',
        default_theme = 'neutron',
        default_theme_variant = 'dark',
        main_color_set: QColorSet = QColorSet(
            'smth',
            QUtilsColor('#000000'),
            QUtilsColor('#000000'),
            QUtilsColor('#000000'),
            QUtilsColor('#000000')
        ),
        neutral_color_set: QColorSet = QColorSet(
            'smthelse',
            QUtilsColor('#000000'),
            QUtilsColor('#000000'),
            QUtilsColor('#000000'),
            QUtilsColor('#000000')
        )
    ) -> None:
        super().__init__()

        self._app_type: QAppType = app.app_type
        self._language: str = default_language
        self._theme: str = default_theme
        self._theme_variant: str = default_theme_variant
        self._path: str = save_path
        self._lang_folder: str = lang_folder
        self._themes_folder: str = themes_folder
        self._first_time: bool = False
        self._developer_mode: bool = False

        self._language_manager: QLangDataManager = QLangDataManager()
        self._language_manager.warning_received.connect(self.warning_received.emit)

        self._theme_manager: QThemeManager = QThemeManager(main_color_set, neutral_color_set)
        self._theme_manager.warning_received.connect(self.warning_received.emit)

        self._load(reload_all = True)


    @property
    def developer_mode(self) -> bool: return self._developer_mode


    def get_lang_data(self, path: str) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        return self._language_manager.get(path)

    def save(self) -> None:
        extra_data = self._save_extra_data()
        with open(self._path, 'w', encoding = 'utf-8') as outfile:
            json.dump(
                obj = {
                    'language': self._language,
                    'theme': self._theme,
                    'themeVariant': self._theme_variant,
                    'developerMode': self._developer_mode
                } | extra_data,
                fp = outfile,
                ensure_ascii = False
            )

    def _save_extra_data(self) -> dict: return {}

    def _load(self, safe_mode: bool = False, reload: list = [], reload_all: bool = False) -> bool:
        res = False

        if not os.path.exists(self._path):
            self._first_time = True
            self.save()

        try:
            with open(self._path, 'r', encoding = 'utf-8') as infile:
                data = json.load(infile)

            exc = suppress(Exception)

            try:
                if 'language' in reload or reload_all:
                    self._language = data['language']
                    self._load_language_data()
                    res |= True

            except Exception as e:
                print(e)

            with exc:
                if 'theme' in reload or reload_all:
                    self._theme = data['theme']
                    self._theme_variant = data['themeVariant']
                    self._load_theme_data()
                    res |= True

            with exc:
                if 'developerMode' in reload or reload_all:
                    self._developer_mode = data['developerMode']

            with exc: res |= self._load_extra_data(data, reload, reload_all)

        except Exception as e:
            self.save()
            if not safe_mode: return self._load()

        return res

    def _load_language_data(self) -> None:
        self._language_manager.load(f'{self._lang_folder}{self._language}', self._app_type)

    def _load_theme_data(self) -> None:
        self._theme_manager.load(self._themes_folder, self._theme, self._theme_variant)

    def _load_extra_data(self, extra_data: dict = {}, reload: list = [], reload_all: bool = False) -> bool: return False

    def set_stylesheet(self, app: QBaseApplication = None) -> None:
        if not app: return
        app.setStyleSheet(self.get_stylesheet(app, QSaveData.StyleSheetMode.All))
        app.window.setProperty('color', self._theme_manager.main_color_set.name)

    def get_stylesheet(self, app: QBaseApplication = None, mode: StyleSheetMode = StyleSheetMode.All) -> str:
        if not app: return ''

        match mode:
            case QSaveData.StyleSheetMode.All:
                return self.get_stylesheet(
                        app,
                        QSaveData.StyleSheetMode.Global
                    ) + '\n' + self.get_stylesheet(
                        app,
                        QSaveData.StyleSheetMode.Local
                    )

            case QSaveData.StyleSheetMode.Global:
                return self._theme_manager.get_global()

            case QSaveData.StyleSheetMode.Local:
                return self._theme_manager.get_local()

        return ''

    def get_icon_dir(self) -> str:
        return f'{self._themes_folder}/{self._theme}/{self._theme_variant}/icons/'

    def get_icon(self, path: str, asQIcon = True, mode: IconMode = IconMode.Local) -> QIcon | str:
        if mode == QSaveData.IconMode.Local:
            if asQIcon: return QIcon(f'{self._themes_folder}/{self._theme}/{self._theme_variant}/icons/{path}')
            return f'{self._themes_folder}/{self._theme}/{self._theme_variant}/icons/{path}'
        elif mode == QSaveData.IconMode.Global:
            if asQIcon: return QIcon(f'./data/lib/qtUtils/themes/{self._theme}/{self._theme_variant}/icons/{path}')
            return f'./data/lib/qtUtils/themes/{self._theme}/{self._theme_variant}/icons/{path}'

    def settings_menu(self, app: QBaseApplication = None) -> bool:
        dat = self._settings_menu_extra()

        dialog = QSettingsDialog(
            parent = app.window,
            settings_data = self._language_manager.get('QSettingsDialog'),
            lang_folder = self._lang_folder,
            themes_folder = self._themes_folder,
            current_lang = self._language,
            current_theme = self._theme,
            current_theme_variant = self._theme_variant,
            extra_tabs = dat[0],
            get_function = dat[1]
        )
        dialog.close_app.connect(lambda: self._close_app(app))
        dialog.restart_app.connect(lambda: self._restart_app(app))
        dialog.clear_data.connect(self.clear_data)
        dialog.import_data.connect(self.import_data)
        dialog.export_data.connect(self.export_data)

        response = dialog.exec()
        if response != None:
            reload_list = []

            if response[0] != self._language:
                self._language = response[0]
                reload_list.append('language')

            if response[1] != self._theme or response[2] != self._theme_variant:
                self._theme = response[1]
                self._theme_variant = response[2]
                reload_list.append('theme')


            self.save()
            res = self._load(False, (reload_list))
            if 'theme' in reload_list: self.set_stylesheet(app)
            if res:
                QMessageBoxWithWidget(app,
                    self._language_manager.get('QMessageBox.information.settingsReload.title'),
                    self._language_manager.get('QMessageBox.information.settingsReload.text'),
                    None,
                    QMessageBoxWithWidget.Icon.Information,
                    None
                ).exec()

            return True
        return False

    def _settings_menu_extra(self) -> tuple[dict, Callable | None]:
        return {}, None

    def _close_app(self, app: QBaseApplication) -> None:
        app.exit()

    def _restart_app(self, app: QBaseApplication) -> None:
        app.must_restart = True
        app.exit()

    def clear_data(self) -> None:
        os.remove(self._path)

    def export_data(self, filename: str) -> None:
        new_data = {'language': self._language, 'theme': self._theme, 'themeVariant': self._theme_variant, 'developerMode': self._developer_mode} | self._export_extra_data()

        with open(filename, 'w', encoding = 'utf-8') as outfile:
            json.dump(new_data, outfile)

    def _export_extra_data(self) -> dict: return {}

    def import_data(self, filename: str) -> None:
        with open(filename, 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)

        self._language = data['language']
        self._theme = data['theme']
        self._theme_variant = data['themeVariant']
        self._developer_mode = data['developerMode']
        self._load_extra_data(data)
        self.save()
#----------------------------------------------------------------------
