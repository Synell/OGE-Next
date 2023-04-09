#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import QObject, Signal, QThread
import os, zipfile, shutil, traceback, sys
from urllib.request import urlopen, Request
from datetime import timedelta
from time import sleep
#----------------------------------------------------------------------

    # Class
class __WorkerSignals__(QObject):
        download_progress_changed = Signal(float)
        install_progress_changed = Signal(float)
        download_speed_changed = Signal(float)
        install_speed_changed = Signal(float)
        download_eta_changed = Signal(timedelta)
        install_eta_changed = Signal(timedelta)
        download_done = Signal()
        install_done = Signal()
        install_failed = Signal(str, int)

class UpdateWorker(QThread):
    def __init__(self, link: str, token: str, download_folder: str):
        super(UpdateWorker, self).__init__()
        self.signals = __WorkerSignals__()
        self.link = link
        self.token = token
        self.dest_path = f'{download_folder}/AppManager'
        self.out_path = './temp/' if sys.argv[0].endswith('.py') else './'
        if not os.path.exists(self.out_path): os.makedirs(self.out_path)
        self.timer = TimeWorker(timedelta(milliseconds = 500))
        self.timer.time_triggered.connect(self.time_triggered)
        self.speed = 0
        self.timed_chunk = 0
        self.timed_items = 0
        self.install = False
        self.done = False
        self.download_left = 0
        self.install_left = 0
        self.state = 0
        self.speeds = []
        self.len_speeds = 4

    def run(self):
        self.timer.start()

        try:
            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path)

            filename = self.link.split('/')[-1].replace(' ', '_')
            file_path = os.path.join(self.dest_path, filename)
            exclude_path = ['MACOSX', '__MACOSX']

            read_bytes = 0
            chunk_size = 1024

            self.state = 1

            with urlopen(Request(self.link, headers = {'Authorization': f'token {self.token}'}) if self.token else self.link) as r:
                total = int(r.info()['Content-Length'])
                with open(file_path, 'ab') as f:
                    self.signals.download_speed_changed.emit(0)
                    while True:
                        chunk = r.read(chunk_size)

                        if chunk is None:
                            continue

                        elif chunk == b'':
                            break

                        f.write(chunk)
                        read_bytes += chunk_size
                        self.timed_chunk += chunk_size

                        self.download_left = total - read_bytes
                        self.signals.download_progress_changed.emit(read_bytes / total)

            self.signals.download_done.emit()
            self.signals.download_speed_changed.emit(-1)
            self.state = 2

            self.zipfile = zipfile.ZipFile(file_path)

            items = self.zipfile.infolist()
            total_n = len(items)

            self.signals.install_speed_changed.emit(0)
            self.install = True
            self.speeds = []
            file = sys.executable.replace(os.path.dirname(sys.executable), '').replace('\\', '').replace('/', '')

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in exclude_path):
                    if item.orig_filename == file: self.zipfile.extract(item, f'{self.out_path}/#tmp#/')
                    else: self.zipfile.extract(item, self.out_path)

                self.install_left = total_n - n
                self.signals.install_progress_changed.emit(n / total_n)
                self.timed_items += 1

            self.zipfile.close()

            self.state = 3

            shutil.rmtree(self.dest_path)

            self.signals.install_speed_changed.emit(-1)
            self.signals.install_done.emit()

        except Exception as e:
            print(traceback.format_exc())
            self.signals.install_failed.emit(str(e), self.state)

        self.timer.exit(0)
        self.done = True


    def time_triggered(self, deltatime: timedelta):
        if self.done: return

        if not self.install:
            t = self.timed_chunk / deltatime.total_seconds()
            self.signals.download_speed_changed.emit(t)

            if len(self.speeds) >= self.len_speeds: self.speeds.pop(0)
            if t: self.speeds.append(self.download_left / t)
            self.signals.download_eta_changed.emit(timedelta(seconds = (sum(self.speeds) / len(self.speeds) if self.speeds else -1)))

        else:
            t = self.timed_items / deltatime.total_seconds()
            self.signals.install_speed_changed.emit(t)

            if len(self.speeds) >= self.len_speeds: self.speeds.pop(0)
            if t: self.speeds.append(self.install_left / t)
            self.signals.install_eta_changed.emit(timedelta(seconds = (sum(self.speeds) / len(self.speeds) if self.speeds else -1)))

        self.timed_chunk = 0



class TimeWorker(QThread):
    time_triggered = Signal(timedelta)

    def __init__(self, interval: timedelta):
        super(TimeWorker, self).__init__()
        self.interval = interval

    def run(self):
        while True:
            self.time_triggered.emit(self.interval)
            sleep(self.interval.total_seconds())
#----------------------------------------------------------------------
