#----------------------------------------------------------------------

    # Librairies
from .QTerminalAction import QTerminalAction
from .QTerminalActionFabric import QTerminalActionFabric
from data.lib.utils import CombinedException

from pathlib import Path
import platform, subprocess, shutil
#----------------------------------------------------------------------

    # Class
class QTerminalOpenCodeAction(QTerminalAction):
    action = 'open-code'


    def __init__(self, file: str, line: int, string: str) -> None:
        super().__init__()
        self._file = Path(file).resolve()
        self._line = int(line)
        self._string = str(string)


    def _is_app_installed(self, app: str) -> str | None:
        return shutil.which(app)


    def exec(self) -> None:
        startupinfo = {}

        with open(self._file, 'r', encoding = 'utf-8') as infile:
            line = infile.readlines()[self._line - 1]
            char_index = line.index(self._string)

        commands: list[list[str]] = []
        if (command := self._is_app_installed('codium')): commands.append(f'"{command}" -r --goto "{self._file}:{self._line}:{char_index + 1}"')
        if (command := self._is_app_installed('code')): commands.append(f'"{command}" --goto "{self._file}:{self._line}:{char_index + 1}"')
        if (command := self._is_app_installed('subl')): commands.append(f'"{command}" "{self._file}"')
        if (command := self._is_app_installed('notepad++')): commands.append(f'"{command}" "{self._file}"')

        match platform.system():
            case 'Windows': # Windows
                startupinfo['startupinfo'] = subprocess.STARTUPINFO()
                startupinfo['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo['startupinfo'].wShowWindow = subprocess.SW_HIDE

                if (command := self._is_app_installed('notepad')): commands.append(f'"{command}" "{self._file}"')

            case 'Linux': # Linux
                if (command := self._is_app_installed('gedit')): commands.append(f'"{command}" "{self._file}"')
                if (command := self._is_app_installed('nano')): commands.append(f'"{command}" "{self._file}"')
                if (command := self._is_app_installed('vim')): commands.append(f'"{command}" "{self._file}"')

            case 'Darwin': # MacOS
                if (command := self._is_app_installed('gedit')): commands.append(f'"{command}" "{self._file}"')
                if (command := self._is_app_installed('nano')): commands.append(f'"{command}" "{self._file}"')
                if (command := self._is_app_installed('vim')): commands.append(f'"{command}" "{self._file}"')

            case _:
                raise Exception('Unknown platform')

        exceptions = []

        for command in commands:
            p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, **startupinfo)
            if p.wait() == 0: return
            exceptions.append(Exception(f'Error: {p.stderr.read()}'))

        if len(exceptions) > 0:
            raise CombinedException(exceptions)
#----------------------------------------------------------------------

    # Register
QTerminalActionFabric.register(QTerminalOpenCodeAction.action, QTerminalOpenCodeAction)
#----------------------------------------------------------------------
