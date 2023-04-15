#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
from datetime import datetime
from collections import namedtuple
import requests
from .PlatformType import PlatformType
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
    received = Signal(dict, str)
    failed = Signal(str)

class RequestWorker(QThread):
    download_data = namedtuple('download_data', ['name', 'tag_name', 'link', 'prerelease', 'created_at', 'token'])
    platform = PlatformType.Windows
    token: str = None

    def __init__(self, followed_apps: list[str] = []):
        super(RequestWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.followed_apps = followed_apps
        self.time = datetime.now()

    def run(self):
        for app in self.followed_apps:
            try:
                response = requests.get(
                    f'{app.replace("https://github.com/", "https://api.github.com/repos/")}/releases',
                    headers = {'Authorization': f'token {self.token}'} if self.token else None
                )
                if response.status_code != 200: continue
                response = response.json()
                if type(response) is not list: return self.signals.failed.emit('Invalid response')

                name = f'{app.replace("https://github.com/", "").split("/")[-1].replace("-", " ")}'

                official_release = None
                for i in response:
                    if not i['prerelease']:
                        i['name'] = name
                        official_release = i
                        break

                pre_release = None
                for i in response:
                    if i['prerelease']:
                        i['name'] = name
                        pre_release = i
                        break

                if official_release and pre_release:
                    self.signals.received.emit(official_release, app)
                elif official_release:
                    self.signals.received.emit(official_release, app)
                elif pre_release:
                    self.signals.received.emit(pre_release, app)

            except Exception as e:
                self.signals.failed.emit(f'{e}')


    @staticmethod
    def get_release(data: dict, token: str = None) -> download_data:
        def in_platform(s: str) -> bool:
            for i in RequestWorker.platform.value:
                if i in s: return True
            return False

        def is_content_type(s: str) -> bool:
            types = []
            match RequestWorker.platform:
                case PlatformType.Windows:
                    types = [
                        'application/x-zip-compressed', # .zip
                        'application/zip' # .zip
                        #'application/octet-stream' # .7z
                    ]
                case PlatformType.Linux:
                    types = [
                        'application/x-gzip', # .tar.gz
                        'application/gzip' # .tar.gz
                    ]
                case PlatformType.MacOS:
                    types = [
                        'application/x-gzip', # .tar.gz
                        'application/gzip' # .tar.gz
                        #'application/octet-stream' # .7z
                    ]

            for i in types:
                if i == s: return True
            return False

        def better_file(files: list) -> str:
            for i in RequestWorker.platform.value:
                for j in files:
                    if i.lower() in j.lower(): return j

        files = [asset['browser_download_url'] for asset in data['assets'] if is_content_type(asset['content_type']) if in_platform(asset['name'].lower())]
        if files: return RequestWorker.download_data(data['name'], data['tag_name'], better_file(files), data['prerelease'], data['created_at'], token)
#----------------------------------------------------------------------
