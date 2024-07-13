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
from math import *
import json, zipfile, shutil, traceback, subprocess, platform, logging
from urllib.request import urlopen, Request
from datetime import datetime, timedelta
from app import Application
from data.lib import *
#----------------------------------------------------------------------

    # Class
class ApplicationError(QApplication):
    def __init__(self, err: str = ''):
        super().__init__(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('OGE Next - Error')
        QMessageBoxWithWidget(
            app = self,
            title = 'OGE Next - Error',
            text = 'Oups, something went wrong...\nPlease check the log/error.log file to see what happened.',
            informative_text = f'Error:\n{err}',
            icon = QMessageBoxWithWidget.Icon.Critical
        ).exec()
        sys.exit()
#----------------------------------------------------------------------

    # Main Function

def config_logger() -> None:
    os.makedirs('data/logs', exist_ok = True)

    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('aiohttp').setLevel(logging.ERROR)

    logging.basicConfig(
        filename = 'data/logs/app.log',
        filemode = 'w',
        format = ('=' * 64) + '\n[%(levelname)s] %(name)s at %(asctime)s\n%(message)s\n',
        level = logging.WARNING
    )

    def excepthook(type: type, value: Exception, tb: traceback) -> None:
        logging.error('Uncaught exception', exc_info = (type, value, tb))
        sys.__excepthook__(type, value, tb)

    sys.excepthook = excepthook


def main() -> None:
    app = None
    config_logger()

    try:
        if os.path.exists('./#tmp#/'):
            try:
                for file in os.listdir('./#tmp#'):
                    shutil.copy(f'./#tmp#/{file}', f'./{file}')
                shutil.rmtree('./#tmp#')

            except: pass

        platf = None
        match platform.system():
            case 'Windows': platf = QPlatform.Windows
            case 'Linux': platf = QPlatform.Linux
            case 'Darwin': platf = QPlatform.MacOS
            case 'Java': platf = QPlatform.Java
            case _: platf = QPlatform.Unknown

        if platf not in [QPlatform.Windows, QPlatform.Linux, QPlatform.MacOS]: raise Exception('Unknown platform')

        if Application.instance_exists(Application.SERVER_NAME):
            print('App is already running, exiting...')
            sys.exit(0)

        app = Application(platf)
        app.window.showNormal()
        exit_code = app.exec()
        if exit_code == 0:
            if app.must_update and (not app.must_restart):
                ex = 'py main.py' if sys.argv[0].endswith('.py') else f'{sys.executable}'
                try: subprocess.Popen(rf'{"py updater.py" if sys.argv[0].endswith(".py") else "./Updater"} "{app.must_update}" "{ex}"', creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, cwd = os.getcwd(), shell = False)
                except Exception as e:
                    exit_code = 1

            elif app.must_restart:
                try: subprocess.Popen(rf'{"py main.py" if sys.argv[0].endswith(".py") else sys.argv[0]}', creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, cwd = os.getcwd(), shell = False)
                except Exception as e:
                    exit_code = 1

        sys.exit(exit_code)

    except Exception as err:
        logging.exception(err)

        if app := QApplication.instance():
            if app.thread().isRunning(): app.shutdown()

        app = ApplicationError(err)
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    main()
#----------------------------------------------------------------------
