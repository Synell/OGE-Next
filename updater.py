#----------------------------------------------------------------------

    # Initial Setup
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__ if sys.argv[0].endswith('.py') else sys.executable)))
#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from PySide6.QtSvgWidgets import *
from datetime import datetime, timedelta
import base64, math, subprocess, platform
from urllib.request import urlopen, Request
from time import sleep
from data.lib.qtUtils import *
from data.lib.widgets import SaveData
from data.lib.widgets.updater import *
from data.lib.widgets.updater import data as updater_data
from data.lib.globalinfo import *
#----------------------------------------------------------------------

    # Class
class QUpdater(QBaseApplication):
    UPDATE_LINK = ''

    def __init__(self, platform: QPlatform) -> None:
        super().__init__(platform = platform, app_type = QAppType.Updater, single_instance = True)

        self.setOrganizationName('Synel')
        # self.setApplicationDisplayName(Info.application_name)
        self.setApplicationName(Info.application_name)
        self.setApplicationVersion(Info.version)

        self.save_data = self.save_data = SaveData(
            app = self,
            save_path = Info.save_path,
            main_color_set = Info.main_color_set,
            neutral_color_set = Info.neutral_color_set
        )

        self.save_data.set_stylesheet(self)

        self.setWindowIcon(QIcon(Info.icon_path))

        self.window.setFixedSize(int(self.primaryScreen().size().width() * (7 / 30)), int(self.primaryScreen().size().height() * (16 / 27)))

        self.create_widgets()
        self.load_colors()
        self.update_title()

        self.run()



    def update_title(self):
        self.window.setWindowTitle(self.get_lang_data('QUpdater.title') + f' | Version: {Info.version} • Build: {Info.build}')

    def load_colors(self):
        qss = super().load_colors()

        SaveData.COLOR_LINK = self.COLOR_LINK

    def settings_menu(self):
        self.save_data.settings_menu(self)
        self.load_colors()



    def not_implemented(self, text = ''):
        lang = self.get_lang_data('QMessageBox.critical.notImplemented')

        if text:
            w = QDropDownWidget(text = self.get_lang_data('QMessageBox.critical.notImplemented.details'), widget = QLabel(text))
        else: w = None

        QMessageBoxWithWidget(
            app = self,
            title = lang.get_data('title'),
            text = lang.get_data('text'),
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def create_widgets(self):
        self.root = QGridWidget()
        self.root.grid_layout.setSpacing(0)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.window.setCentralWidget(self.root)


        top_frame = QGridFrame()
        top_frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(top_frame, 0, 0)
        self.root.grid_layout.setAlignment(top_frame, Qt.AlignmentFlag.AlignTop)
        top_frame.grid_layout.setSpacing(5)
        top_frame.grid_layout.setContentsMargins(15, 10, 15, 10)

        self.progress_percent = QLabel(self.get_lang_data('QUpdater.QLabel.downloading').replace('%s', self.get_lang_data('QUpdater.QLabel.waiting')))
        self.progress_percent.setProperty('h', 2)
        top_frame.grid_layout.addWidget(self.progress_percent, 0, 0, 1, 2)

        self.progress_eta = QLabel(self.get_lang_data('QUpdater.QLabel.calculatingRemainingTime'))
        self.progress_eta.setProperty('subtitle', True)
        self.progress_eta.setProperty('bold', True)
        top_frame.grid_layout.addWidget(self.progress_eta, 1, 0)
        top_frame.grid_layout.setAlignment(self.progress_eta, Qt.AlignmentFlag.AlignLeft)

        self.progress_speed = QLabel(self.convert(0))
        self.progress_speed.setProperty('subtitle', True)
        self.progress_speed.setProperty('bold', True)
        top_frame.grid_layout.addWidget(self.progress_speed, 1, 1)
        top_frame.grid_layout.setAlignment(self.progress_speed, Qt.AlignmentFlag.AlignRight)


        self.progress = QAnimatedProgressBar()
        self.progress.setProperty('color', 'main')
        self.progress.setProperty('small', True)
        self.progress.setProperty('light', True)
        self.progress.setProperty('not-rounded', True)
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        self.progress.setValue(0)
        self.progress.setRange(0, 100)
        self.root.grid_layout.addWidget(self.progress, 1, 0)
        self.root.grid_layout.setAlignment(self.progress, Qt.AlignmentFlag.AlignTop)


        ratio = 1192 / self.window.width() # 1192x674
        self.screenshots = QSlidingStackedWidget()
        self.screenshots.set_speed(650)
        self.screenshots.set_animation(QEasingCurve.Type.OutCubic)
        self.screenshots.set_has_opacity_effect(False)
        self.screenshots.setFixedHeight(math.ceil(674 / ratio))
        self.screenshots.layout().setContentsMargins(0, 0, 0, 0)
        self.screenshots.layout().setSpacing(0)
        self.root.grid_layout.addWidget(self.screenshots, 2, 0)
        self.root.grid_layout.setAlignment(self.screenshots, Qt.AlignmentFlag.AlignTop)

        for image in updater_data.images:
            self.screenshots.addWidget(QIconWidget(None, base64.b64decode(image), QSize(self.window.width() + 1, math.ceil(674 / ratio)), False))

        bottom_frame = QGridFrame()
        bottom_frame.setFixedHeight(int(self.window.height() / 2.125))
        # bottom_frame.setProperty('border-top', True)
        self.root.grid_layout.addWidget(bottom_frame, 3, 0)
        bottom_frame.grid_layout.setSpacing(5)
        bottom_frame.grid_layout.setContentsMargins(0, 0, 0, 0)


        bottom_frame.top = QGridFrame()
        bottom_frame.top.grid_layout.setSpacing(0)
        bottom_frame.top.grid_layout.setContentsMargins(0, 10, 0, 10)
        bottom_frame.grid_layout.addWidget(bottom_frame.top, 0, 0)

        self.texts = QSlidingStackedWidget()
        self.texts.set_speed(650)
        self.texts.set_animation(QEasingCurve.Type.OutCubic)
        self.texts.layout().setContentsMargins(0, 0, 0, 0)
        self.texts.layout().setSpacing(0)
        bottom_frame.top.grid_layout.addWidget(self.texts, 0, 0)

        for text in self.get_lang_data('QUpdater.QSlidingStackedWidget.texts'):
            w = QGridFrame()
            w.grid_layout.setSpacing(0)
            w.grid_layout.setContentsMargins(50, 0, 50, 0)

            l = QLabel(text)
            l.setWordWrap(True)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            w.grid_layout.addWidget(l, 0, 0)

            self.texts.addWidget(w)


        bottom_frame.bottom = QGridFrame()
        bottom_frame.bottom.grid_layout.setSpacing(5)
        bottom_frame.bottom.grid_layout.setContentsMargins(10, 10, 10, 10)
        bottom_frame.bottom.setProperty('border-top', True)
        bottom_frame.grid_layout.addWidget(bottom_frame.bottom, 0, 0)
        bottom_frame.grid_layout.setAlignment(bottom_frame.bottom, Qt.AlignmentFlag.AlignBottom)

        self.close_button = QPushButton('Close')
        self.close_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        self.close_button.setDisabled(True)
        self.close_button.setProperty('color', 'white')
        self.close_button.setProperty('transparent', True)
        bottom_frame.bottom.grid_layout.addWidget(self.close_button, 0, 0)
        bottom_frame.bottom.grid_layout.setAlignment(self.close_button, Qt.AlignmentFlag.AlignLeft)

        self.open_button = QPushButton('Open App')
        self.open_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        self.open_button.setDisabled(True)
        self.open_button.setProperty('color', 'main')
        bottom_frame.bottom.grid_layout.addWidget(self.open_button, 0, 1)
        bottom_frame.bottom.grid_layout.setAlignment(self.open_button, Qt.AlignmentFlag.AlignRight)


    def run(self):
        self.slide_worker = SlideWorker()
        self.slide_worker.signals.slide_changed.connect(self.slide)
        self.slide_worker.start()

        self.update_worker = UpdateWorker(self.UPDATE_LINK, '', self.save_data.downloads_folder)
        self.update_worker.signals.download_progress_changed.connect(self.download_progress_changed)
        self.update_worker.signals.download_speed_changed.connect(self.download_speed_changed)
        self.update_worker.signals.download_eta_changed.connect(self.download_eta_changed)
        self.update_worker.signals.download_done.connect(self.download_done)
        self.update_worker.signals.install_progress_changed.connect(self.install_progress_changed)
        self.update_worker.signals.install_speed_changed.connect(self.install_speed_changed)
        self.update_worker.signals.install_eta_changed.connect(self.install_eta_changed)
        self.update_worker.signals.install_done.connect(self.install_done)
        self.update_worker.signals.install_failed.connect(self.install_failed)
        self.update_worker.start()

    def slide(self):
        self.screenshots.slide_loop_next(QSlidingStackedWidget.Direction.Right2Left)
        self.texts.slide_loop_next(QSlidingStackedWidget.Direction.Right2Left)

    def download_speed_changed(self, speed: float):
        self.progress_speed.setText(self.get_lang_data('QUpdater.QLabel.bytes').replace('%s', self.convert(speed)))

    def download_eta_changed(self, eta: float):
        self.progress_eta.setText(self.get_lang_data('QUpdater.QLabel.eta').replace('%s', self.convert_time(eta)))

    def download_progress_changed(self, progress: float):
        if self.progress._anim.state() != QPropertyAnimation.State.Running: self.progress.setValue(int(progress * 50))
        self.progress_percent.setText(self.get_lang_data('QUpdater.QLabel.downloading').replace('%s', f'{int(progress * 100)} %'))

    def download_done(self):
        self.progress.setValue(50)
        self.progress_percent.setText(self.get_lang_data('QUpdater.QLabel.downloading').replace('%s', self.get_lang_data('QUpdater.QLabel.done')))
        self.progress_eta.setText(self.get_lang_data('QUpdater.QLabel.done'))

    def install_speed_changed(self, speed: float):
        self.progress_speed.setText(self.get_lang_data('QUpdater.QLabel.items').replace('%s', f'{speed}'))

    def install_eta_changed(self, eta: float):
        self.progress_eta.setText(self.get_lang_data('QUpdater.QLabel.eta').replace('%s', self.convert_time(eta)))

    def install_progress_changed(self, progress: float):
        if self.progress._anim.state() != QPropertyAnimation.State.Running: self.progress.setValue(int(50 + progress * 50))
        self.progress_percent.setText(self.get_lang_data('QUpdater.QLabel.installing').replace('%s', f'{int(progress * 100)} %'))

    def install_done(self):
        self.progress.setValue(100)
        self.progress_percent.setText(self.get_lang_data('QUpdater.QLabel.done'))
        self.progress_eta.setText('')
        self.progress_speed.setText('')

        self.close_button.setDisabled(False)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.exit)

        self.open_button.setDisabled(False)
        self.open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_button.clicked.connect(self.open_app)

        self.save_data.last_check_for_updates = datetime.now()
        self.save_data.save()

    def install_failed(self, error: str, exit_code: int):
        QMessageBoxWithWidget(
            app = self,
            title = self.get_lang_data('QUpdater.QMessageBox.critical.' + ('downloadFailed' if exit_code < 2 else 'installFailed.title')),
            text = self.get_lang_data('QUpdater.QMessageBox.critical.' + ('downloadFailed' if exit_code < 2 else 'installFailed.text')),
            informative_text = str(sys.argv[2]),
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = QDropDownWidget(text = self.get_lang_data('QMessageBox.critical.notImplemented.details'), widget = QLabel(error))
        ).exec()

    def convert(self, bytes: float) -> str:
        step_unit = 1024
        units = ['B', 'KB', 'MB', 'GB', 'TB']

        for x in units[:-1]:
            if bytes < step_unit:
                return f'{bytes:.2f} {x}'
            bytes /= step_unit
        return f'{bytes:.2f} {units[-1]}'

    def convert_time(self, time: timedelta) -> str:
        secs = round(time.total_seconds())
        days = secs // 86400
        hours = (secs % 86400) // 3600
        minutes = (secs % 3600) // 60
        seconds = secs % 60

        if days == -1:
            return self.get_lang_data('QUpdater.QLabel.undefined')
        elif days > 0:
            return (self.get_lang_data('QUpdater.QLabel.days') if days > 1 else self.get_lang_data('QUpdater.QLabel.day')).replace('%s', str(days))
        elif hours > 0:
            return (self.get_lang_data('QUpdater.QLabel.hours') if hours > 1 else self.get_lang_data('QUpdater.QLabel.hour')).replace('%s', str(hours))
        elif minutes > 0:
            return (self.get_lang_data('QUpdater.QLabel.minutes') if minutes > 1 else self.get_lang_data('QUpdater.QLabel.minute')).replace('%s', str(minutes))
        else:
            return (self.get_lang_data('QUpdater.QLabel.seconds') if seconds > 1 else self.get_lang_data('QUpdater.QLabel.second')).replace('%s', str(seconds))

    def open_app(self):
        if len(sys.argv) > 2:
            try: subprocess.Popen(rf'{sys.argv[2]}', creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, cwd = os.getcwd())
            except Exception as e:
                QMessageBoxWithWidget(
                    app = self,
                    title = self.get_lang_data('QUpdater.QMessageBox.critical.openAppFailed.title'),
                    text = self.get_lang_data('QUpdater.QMessageBox.critical.openAppFailed.text'),
                    informative_text = str(sys.argv[2]),
                    icon = QMessageBoxWithWidget.Icon.Critical,
                    widget = QDropDownWidget(text = self.get_lang_data('QMessageBox.critical.notImplemented.details'), widget = QLabel(str(e)))
                ).exec()

            self.exit()

        else:
            QMessageBoxWithWidget(
                app = self,
                title = self.get_lang_data('QUpdater.QMessageBox.critical.appNotFound.title'),
                text = self.get_lang_data('QUpdater.QMessageBox.critical.appNotFound.text'),
                icon = QMessageBoxWithWidget.Icon.Critical
            ).exec()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    if len(sys.argv) > 1: QUpdater.UPDATE_LINK = sys.argv[1]
    else: sys.exit()

    platf = None
    match platform.system():
        case 'Windows': platf = QPlatform.Windows
        case 'Linux': platf = QPlatform.Linux
        case 'Darwin': platf = QPlatform.MacOS
        case 'Java': platf = QPlatform.Java
        case _: platf = QPlatform.Unknown

    if platf == QPlatform.Unknown: raise Exception('Unknown platform')

    app = QUpdater(platf)
    app.window.showNormal()
    sys.exit(app.exec())
#----------------------------------------------------------------------
