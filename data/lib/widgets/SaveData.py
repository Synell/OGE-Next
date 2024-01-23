#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtCore import Qt

from .PlatformType import PlatformType
from datetime import datetime
from contextlib import suppress

from data.lib.qtUtils import QColorSet, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QNamedComboBox, QUtilsColor, QBaseApplication
from cryptography.fernet import Fernet
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()
    downloads_folder = './OGENext/'

    def __init__(self, app: QBaseApplication, save_path: str = './data/save.dat', main_color_set: QColorSet = None, neutral_color_set: QColorSet = None) -> None:
        self.platform = PlatformType.from_qplatform(app.platform)

        self.check_for_updates = 4
        self.last_check_for_updates = datetime.now()
        self.version = '0' * 8
        self.username = ''
        self.password = ''
        self.remember = True

        super().__init__(app, save_path, main_color_set = main_color_set, neutral_color_set = neutral_color_set)


    def _settings_menu_extra(self):
        return {
            self.get_lang_data('QSettingsDialog.QSidePanel.updates.title'): (self.settings_menu_updates(), f'{self.get_icon_dir()}/sidepanel/updates.png'),
        }, self.get_extra



    def settings_menu_updates(self):
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.updates')
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get('QLabel.checkForUpdates.title'), lang.get('QLabel.checkForUpdates.description'))
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang.get('QNamedComboBox.checkForUpdates.title'))
        widget.check_for_updates_combobox.combo_box.addItems([
            lang.get('QNamedComboBox.checkForUpdates.values.never'),
            lang.get('QNamedComboBox.checkForUpdates.values.daily'),
            lang.get('QNamedComboBox.checkForUpdates.values.weekly'),
            lang.get('QNamedComboBox.checkForUpdates.values.monthly'),
            lang.get('QNamedComboBox.checkForUpdates.values.atLaunch')
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(widget.check_for_updates_combobox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def get_extra(self, extra_tabs: dict = {}):
        pass



    def valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


    def without_duplicates(self, l: list) -> list:
        return list(dict.fromkeys(l))


    def _save_extra_data(self) -> dict:
        # encrypt password so it's not stored in plain text
        key = Fernet.generate_key()
        fernet = Fernet(key)

        return {
            'version': self.version,
            'checkForUpdates': self.check_for_updates,
            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),
            'username': self.username,
            'password': fernet.encrypt(self.password.encode('utf-8')).decode('utf-8'),
            'key': key.decode('utf-8'),
            'remember': self.remember
        }

    def _load_extra_data(self, extra_data: dict = ..., reload: list = [], reload_all: bool = False) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.version = extra_data['version']
        with exc: self.check_for_updates = extra_data['checkForUpdates']
        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)
        with exc: self.username = extra_data['username']
        with exc: self.password = Fernet(extra_data['key']).decrypt(extra_data['password']).decode('utf-8')
        with exc: self.remember = extra_data['remember']

        return res

    def export_extra_data(self) -> dict:
        dct = self._save_extra_data()

        del dct['username']
        del dct['key']
        del dct['password']
        del dct['remember']

        return dct
#----------------------------------------------------------------------
