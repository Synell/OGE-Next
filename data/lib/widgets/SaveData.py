#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

from .PlatformType import PlatformType
from datetime import datetime
from contextlib import suppress
import os

from data.lib.qtUtils import QFiles, QNamedLineEdit, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QDragList
from cryptography.fernet import Fernet
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, save_path: str = './data/save.dat') -> None:
        self.platform = PlatformType.Windows

        self.check_for_updates = 4
        self.last_check_for_updates = datetime.now()
        self.username = ''
        self.password = ''
        self.remember = True

        super().__init__(save_path)


    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']: (self.settings_menu_updates(), f'{self.getIconsDir()}/sidepanel/updates.png'),
        }, self.get_extra



    def settings_menu_updates(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['updates']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['checkForUpdates']['title'], lang['QLabel']['checkForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        widget.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
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


    def save_extra_data(self) -> dict:
        # encrypt password so it's not stored in plain text
        key = Fernet.generate_key()
        fernet = Fernet(key)

        return {
            'checkForUpdates': self.check_for_updates,
            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),
            'username': self.username,
            'password': fernet.encrypt(self.password.encode('utf-8')).decode('utf-8'),
            'key': key.decode('utf-8'),
            'remember': self.remember
        }

    def load_extra_data(self, extra_data: dict = ...) -> None:
        exc = suppress(Exception)

        with exc: self.check_for_updates = extra_data['checkForUpdates']
        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)
        with exc: self.username = extra_data['username']
        with exc: self.password = Fernet(extra_data['key']).decrypt(extra_data['password']).decode('utf-8')
        with exc: self.remember = extra_data['remember']

        self.save()

    def export_extra_data(self) -> dict:
        dct = self.save_extra_data()

        del dct['username']
        del dct['key']
        del dct['password']
        del dct['remember']

        return dct
#----------------------------------------------------------------------
