#----------------------------------------------------------------------

    # Libraries
from datetime import datetime
#----------------------------------------------------------------------

    # Class
class QCrashReport:
    file: str = 'crash_report.txt'

    def __new__(cls, *args, **kwargs):
        return None

    def report(self, err: str = ''):
        with open(self.file, 'a') as f:
            f.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n=========================\n{err}\n\n\n')
#----------------------------------------------------------------------
