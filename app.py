#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from PySide6.QtSvgWidgets import *
from math import *
import os, sys
from datetime import datetime, timedelta
from data.lib import *
#----------------------------------------------------------------------

    # Class
class Application(QBaseApplication):
    BUILD = '07e77fc5'
    VERSION = 'Experimental'

    SERVER_NAME = 'OgeNext'

    MESSAGE_DURATION = 5000

    ALERT_RAISE_DURATION = 350
    ALERT_PAUSE_DURATION = 2300
    ALERT_FADE_DURATION = 350

    UPDATE_LINK = 'https://github.com/Synell/OGE-Next'

    def __init__(self, platform: QPlatform) -> None:
        super().__init__(platform = platform, single_instance = True)

        self.update_request = None

        self.setOrganizationName('Synel')
        # self.setApplicationDisplayName('OGE Next')
        self.setApplicationName('OGE Next')
        self.setApplicationVersion(self.VERSION)

        self.another_instance_opened.connect(self.on_another_instance)

        self.save_data = SaveData(save_path = os.path.abspath('./data/save.dat').replace('\\', '/'))
        self.must_exit_after_download = False

        self.oge_worker = None
        self.must_init_panels = True

        self.save_data.set_stylesheet(self)
        self.window.setProperty('color', 'yellow')

        self.setWindowIcon(QIcon('./data/icons/OGENext.svg'))

        SemesterWidget._ICON = f'{self.save_data.get_icon_dir()}/sidepanel/semester_%s.png'
        OGEWorker._CACHE_FILE = './data/oge_cache/%s.json'
        OGEWidget._OGE_WEIRD_TOOLTIP = self.save_data.language_data['QMainWindow']['mainPage']['QSidePanel']['dataPanel']['QToolTip']['ogeWeird']
        OGEWidget._OGE_WEIRD_ICON = QIcon(f'{self.save_data.get_icon_dir()}/oge/about.png').pixmap(16, 16)

        oge_new_icon = QIcon(f'{self.save_data.get_icon_dir()}/oge/new.png')
        SemesterWidget._OGE_NEW_ICON = oge_new_icon.pixmap(32, 32)
        GradeWidget._OGE_NEW_ICON = oge_new_icon.pixmap(16, 16)

        self.load_colors()
        self.create_widgets()
        self.update_title()

        self.create_about_menu()

        if self.save_data.check_for_updates == 4: self.check_updates()
        elif self.save_data.check_for_updates > 0 and self.save_data.check_for_updates < 4:
            deltatime = datetime.now() - self.save_data.last_check_for_updates

            match self.save_data.check_for_updates:
                case 1:
                    if deltatime > timedelta(days = 1): self.check_updates()
                case 2:
                    if deltatime > timedelta(weeks = 1): self.check_updates()
                case 3:
                    if deltatime > timedelta(weeks = 4): self.check_updates()

        self.window.setMinimumSize(int(self.primaryScreen().size().width() * (8 / 15)), int(self.primaryScreen().size().height() * (14 / 27))) # 128x71 -> 1022x568

        self.window.closeEvent = self.close_event



    def on_another_instance(self) -> None:
        self.window.showMinimized()
        self.window.setWindowState(self.window.windowState() and (not Qt.WindowState.WindowMinimized or Qt.WindowState.WindowActive))



    def update_title(self) -> None:
        self.window.setWindowTitle(self.save_data.language_data['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD}')

    def load_colors(self) -> None:
        qss = super().load_colors()

        SaveData.COLOR_LINK = self.COLOR_LINK



    def settings_menu(self) -> None:
        if self.save_data.settings_menu(self):
            self.load_colors()



    def not_implemented(self, text = '') -> None:
        if text:
            w = QDropDownWidget(text = lang['details'], widget = QLabel(text))
        else: w = None

        lang = self.save_data.language_data['QMessageBox']['critical']['notImplemented']

        QMessageBoxWithWidget(
            app = self,
            title = lang['title'],
            text = lang['text'],
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def create_widgets(self) -> None:
        self.root = QSlidingStackedWidget()

        self.window.setCentralWidget(self.root)

        self.create_status_bar()
        self.create_main_page()



    def change_status_message(self, info_type: InfoType, message: str) -> None:
        self.status_bar.status.icon.setPixmap(self.save_data.get_icon(f'statusbar/{info_type.value}.png').pixmap(16, 16))
        self.status_bar.status.label.setText(message)

    def create_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.window.setStatusBar(self.status_bar)

        self.status_bar.status = QGridWidget()
        self.status_bar.status.setContentsMargins(0, 0, 0, 0)
        self.status_bar.status.grid_layout.setContentsMargins(10, 5, 0, 5)
        self.status_bar.status.grid_layout.setSpacing(10)
        self.status_bar.addPermanentWidget(self.status_bar.status, 40)

        self.status_bar.status.icon = QLabel()
        self.status_bar.status.icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_bar.status.grid_layout.addWidget(self.status_bar.status.icon, 0, 0)

        self.status_bar.status.label = QLabel()
        self.status_bar.status.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_bar.status.grid_layout.addWidget(self.status_bar.status.label, 0, 1)

        self.status_bar.status.grid_layout.setColumnStretch(2, 1)

        self.change_status_message(InfoType.Info, 'Not connected')


        progress_widget = QGridWidget()
        progress_widget.setContentsMargins(0, 0, 0, 0)
        progress_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        progress_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(progress_widget, 20)

        # self.status_bar.progress = QAnimatedProgressBar()
        # self.status_bar.progress.setProperty('color', 'main')
        # self.status_bar.progress.setProperty('small', True)
        # self.status_bar.progress.setFixedHeight(6)
        # self.status_bar.progress.setTextVisible(False)
        # self.status_bar.progress.setRange(0, 100)
        # self.status_bar.progress.setValue(0)
        # progress_widget.grid_layout.addWidget(self.status_bar.progress, 0, 0)
        # self.status_bar.progress.setVisible(False)


        empty_widget = QGridWidget()
        empty_widget.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(empty_widget, 30)


        update_widget = QGridWidget()
        update_widget.setContentsMargins(0, 0, 0, 0)
        update_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        update_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(update_widget, 10)

        self.update_button = QPushButton(self.save_data.language_data['QStatusBar']['QPushButton']['update'])
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(self.update_click)
        self.update_button.setProperty('color', 'main')
        self.update_button.setProperty('transparent', True)
        update_widget.grid_layout.addWidget(self.update_button, 0, 0)
        self.update_button.setVisible(False)


    def create_main_page(self) -> None:
        self.main_page = QGridWidget()
        self.root.addWidget(self.main_page)

        self.main_page.left = QGridWidget()
        self.main_page.left.grid_layout.setSpacing(0)
        self.main_page.left.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_page.grid_layout.addWidget(self.main_page.left, 0, 0)
        self.main_page.grid_layout.setSpacing(0)
        self.main_page.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_page.grid_layout.setAlignment(self.main_page.left, Qt.AlignmentFlag.AlignLeft)

        self.main_page.right = QSlidingStackedWidget()
        self.main_page.right.set_orientation(Qt.Orientation.Horizontal)
        self.main_page.grid_layout.addWidget(self.main_page.right, 0, 1)

        self.create_empty_panel()

        self.main_page.right.semesters = QSlidingStackedWidget()
        self.main_page.right.semesters.set_orientation(Qt.Orientation.Vertical)
        self.main_page.right.addWidget(self.main_page.right.semesters)

        self.data_panels: list[SemesterWidget] = []
        self.main_page.right.slide_in_index(0)

        left_top = QFrame()
        left_top.grid_layout = QGridLayout()
        left_top.setLayout(left_top.grid_layout)
        left_top.setProperty('border-top', True)
        left_top.setProperty('border-left', True)
        left_top.setProperty('border-right', True)
        left_top.setProperty('background', 'light')
        self.main_page.left.grid_layout.addWidget(left_top, 0, 0)

        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(self.save_data.get_icon('/pushbutton/note.png'))
        button.clicked.connect(self.about_menu_clicked)
        left_top.grid_layout.addWidget(button, 0, 0)
        left_top.grid_layout.setAlignment(button, Qt.AlignmentFlag.AlignLeft)

        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(self.save_data.get_icon('/pushbutton/settings.png'))
        button.clicked.connect(self.settings_menu)
        left_top.grid_layout.addWidget(button, 0, 1)
        left_top.grid_layout.setAlignment(button, Qt.AlignmentFlag.AlignRight)

        self.main_page.side_panel = QSidePanel(width = 240)
        self.main_page.side_panel.setProperty('border-right', True)
        self.main_page.left.grid_layout.addWidget(self.main_page.side_panel, 1, 0)

    def create_empty_panel(self) -> None:
        lang = self.save_data.language_data['QMainWindow']['mainPage']['QSidePanel']['emptyPanel']

        self.main_page.empty_panel = QGridWidget()

        grid = QGridWidget()
        grid.grid_layout.setSpacing(20)
        grid.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_page.empty_panel.grid_layout.addWidget(grid, 0, 0)
        self.main_page.empty_panel.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_page.empty_panel.auth = QLoginWidget(None, lang['QLoginWidget'], self.save_data.username, self.save_data.password, True, self.save_data.remember)
        self.main_page.empty_panel.auth.enter_key_pressed.connect(self.login)
        grid.grid_layout.addWidget(self.main_page.empty_panel.auth, 0, 0)

        self.main_page.empty_panel.login_button = QPushButton(lang['QPushButton']['login'])
        self.main_page.empty_panel.login_button.setProperty('color', 'main')
        self.main_page.empty_panel.login_button.setProperty('transparent', True)
        self.main_page.empty_panel.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_page.empty_panel.login_button.clicked.connect(self.login)
        grid.grid_layout.addWidget(self.main_page.empty_panel.login_button, 1, 0)

        grid.setMaximumHeight(350)

        self.main_page.right.addWidget(self.main_page.empty_panel)



    def login(self) -> None:
        if not self.main_page.empty_panel.auth.username:
            self.show_alert(self.save_data.language_data['QMainWindow']['showMessage']['emptyUsername'])
            return

        if not self.main_page.empty_panel.auth.password:
            self.show_alert(self.save_data.language_data['QMainWindow']['showMessage']['emptyPassword'])
            return

        self.main_page.empty_panel.auth.set_disabled(True)
        self.main_page.empty_panel.login_button.setDisabled(True)

        self.oge_worker = OGEWorker(self, self.main_page.empty_panel.auth.username, self.main_page.empty_panel.auth.password)
        self.oge_worker.signals.finished.connect(self.login_success)
        self.oge_worker.signals.info_changed.connect(self.change_status_message)
        self.oge_worker.signals.failed.connect(self.login_failed)
        self.oge_worker.start()

        # self.status_bar.progress.setValue(10)
        # self.status_bar.progress.setVisible(True)
        self.show_alert(self.save_data.language_data['QMainWindow']['showMessage']['ogeLoading'], pause_duration = 4300)

    def login_success(self, semester: Semester) -> None:
        self.oge_worker.exit()
        self.change_status_message(InfoType.Info, self.save_data.language_data['QMainWindow']['showMessage']['createPanels'])

        # self.status_bar.progress.setValue(70)

        self.save_data.remember = self.main_page.empty_panel.auth.remember

        if self.main_page.empty_panel.auth.remember:
            self.save_data.username = self.main_page.empty_panel.auth.username
            self.save_data.password = self.main_page.empty_panel.auth.password

        else:
            self.save_data.username = ''
            self.save_data.password = ''

        self.save_data.remember = self.main_page.empty_panel.auth.remember

        self.save_data.save()

        if self.must_init_panels:
            self.must_init_panels = False

            c = self.oge_worker.semester_count
            send_param = lambda i: lambda: self.change_semester(i + 1)

            for i in range(c):
                item = QSidePanelItem(
                    self.save_data.language_data['QMainWindow']['QSideBar']['semester'].replace('%s', str(i + 1)),
                    f'{self.save_data.get_icon_dir()}/sidepanel/semester_unknown.png',
                    send_param(i)
                )

                widget = SemesterWidget(self.save_data.language_data['QMainWindow']['mainPage']['QSidePanel']['dataPanel'], i + 1, item)
                widget.refreshed.connect(lambda j: self.change_semester(j, True))
                self.main_page.right.semesters.addWidget(widget)
                self.data_panels.append(widget)

                self.main_page.side_panel.add_item(item)

            self.main_page.right.slide_in_index(1)

        # self.status_bar.progress.setValue(100)

        self.data_panels[semester.id - 1].set_data(semester, self.oge_worker.force)
        self.oge_worker.force = False
        self.main_page.side_panel.set_current_index(semester.id - 1)

        self.main_page.right.semesters.slide_in_index(semester.id - 1, QSlidingStackedWidget.Direction.Bottom2Top)

        self.change_status_message(InfoType.Success, self.save_data.language_data['QMainWindow']['showMessage']['loginSuccess'])

        semesters_to_load = [i + 1 for i, s in enumerate(self.data_panels) if (not s.loaded) and (i + 1 in self.oge_worker.loaded_semesters)]

        for i in semesters_to_load:
            self.data_panels[i - 1].set_data(self.oge_worker.get_loaded_semester(i), True)

        self.set_panel_disabled(False)

        # self.status_bar.progress.setVisible(False)
        # self.status_bar.progress.setValue(0)

    def login_failed(self, error: Exception) -> None:
        self.oge_worker.exit()
        self.main_page.empty_panel.auth.set_disabled(False)
        self.main_page.empty_panel.login_button.setDisabled(False)
        self.show_alert(str(error))
        self.change_status_message(InfoType.Error, self.save_data.language_data['QMainWindow']['showMessage']['loginFailed'])
        self.set_panel_disabled(False)

        # self.status_bar.progress.setVisible(False)
        # self.status_bar.progress.setValue(0)



    def change_semester(self, semester: int, force: bool = False) -> None:
        self.oge_worker.semester = semester
        self.oge_worker.force = force
        self.set_panel_disabled(True)
        self.oge_worker.start()

        # self.status_bar.progress.setVisible(True)
        # self.status_bar.progress.setValue(10)



    def set_panel_disabled(self, disabled: bool) -> None:
        self.main_page.side_panel.setDisabled(disabled)
        for panel in self.data_panels:
            panel.setDisabled(disabled)



    def check_updates(self) -> None:
        self.update_request = RequestWorker([self.UPDATE_LINK])
        self.update_request.signals.received.connect(self.check_updates_release)
        self.update_request.signals.failed.connect(self.check_updates_failed)
        self.update_request.start()

    def check_updates_release(self, rel: dict, app: str) -> None:
        self.update_request.exit()
        self.must_update_link = RequestWorker.get_release(rel, None).link
        if rel['tag_name'] > self.BUILD: self.set_update(True)
        else: self.save_data.last_check_for_updates = datetime.now()

    def check_updates_failed(self, error: str) -> None:
        self.update_request.exit()
        print('Failed to check for updates:', error)

    def set_update(self, update: bool) -> None:
        self.update_button.setVisible(update)

    def update_click(self) -> None:
        self.save_data.save()
        self.must_update = self.must_update_link
        self.exit()



    def create_about_menu(self) -> None:
        self.about_menu = QMenu(self.window)
        self.about_menu.setCursor(Qt.CursorShape.PointingHandCursor)

        act = self.about_menu.addAction(self.save_data.get_icon('menubar/qt.png', mode = QSaveData.IconMode.Global), self.save_data.language_data['QMenu']['about']['PySide'])
        act.triggered.connect(self.aboutQt)

        act = self.about_menu.addAction(QIcon('./data/icons/OGENext.svg'), self.save_data.language_data['QMenu']['about']['OGENext'])
        act.triggered.connect(self.about_clicked)

        self.about_menu.addSeparator()

        act = self.about_menu.addAction(self.save_data.get_icon('menubar/bug.png', mode = QSaveData.IconMode.Local), self.save_data.language_data['QMenu']['reportBug'])
        act.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/Synell/OGE-Next/issues')))

        self.about_menu.addSeparator()

        def create_donate_menu():
            donate_menu = QMenu(self.save_data.language_data['QMenu']['donate']['title'], self.window)
            donate_menu.setIcon(self.save_data.get_icon('menubar/donate.png'))

            buymeacoffee_action = QAction(self.save_data.get_icon('menubar/buyMeACoffee.png'), 'Buy Me a Coffee', self.window)
            buymeacoffee_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.buymeacoffee.com/Synell')))

            patreon_action = QAction(self.save_data.get_icon('menubar/patreon.png'), 'Patreon', self.window)
            patreon_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.patreon.com/synel')))

            donate_menu.addAction(buymeacoffee_action)
            donate_menu.addAction(patreon_action)

            return donate_menu

        self.about_menu.addMenu(create_donate_menu())

    def about_menu_clicked(self) -> None:
        self.about_menu.popup(QCursor.pos())

    def about_clicked(self) -> None:
        lang = self.save_data.language_data['QAbout']['OGENext']
        supports = '\n'.join(f'&nbsp;&nbsp;&nbsp;• <a href=\"{link}\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">{name}</a>' for name, link in [
            ('GitHub', 'https://github.com')
        ])
        QAboutBox(
            app = self,
            title = lang['title'],
            logo = './data/icons/OGENext.svg',
            texts = [
                lang['texts'][0],
                lang['texts'][1].replace('%s', f'<a href=\"https://github.com/Synell\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Synel</a>'),
                lang['texts'][2].replace('%s', f'<a href=\"https://github.com/Zenitude71\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Zenitude</a>', 1).replace('%s', f'<a href=\"https://github.com/Synell\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Synel</a>', 1),
                lang['texts'][3].replace('%s', f'<a href=\"https://github.com/Nikolasitude\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Nikolasitude</a>'),
                lang['texts'][4].replace('%s', f'<a href=\"https://github.com/Synell/OGE-Next\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">OGE Next Github</a>')
            ]
        ).exec()



    def close_event(self, event: QCloseEvent) -> None:
        self.exit()

    def exit(self) -> None:
        if self.update_request:
            self.update_request.exit()

            if self.update_request.isRunning():
                self.update_request.terminate()

        if self.oge_worker:
            self.oge_worker.exit()

            if self.oge_worker.isRunning():
                self.oge_worker.terminate()

            self.oge_worker.save_data()

        super().exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    app = Application(QPlatform.Windows)
    app.window.showNormal()
    sys.exit(app.exec())
#----------------------------------------------------------------------
