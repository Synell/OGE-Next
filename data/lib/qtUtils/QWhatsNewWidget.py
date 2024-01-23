#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from .QGridFrame import QGridFrame
from . import QBaseApplication
from .QLangDataManager import QLangData
from .QMarkDownWidget import QMarkDownWidget
#----------------------------------------------------------------------

    # Class
class QWhatsNewWidget(QGridFrame):
    _lang: QLangData = QLangData.NoTranslation()


    def init(app: QBaseApplication) -> None:
        QWhatsNewWidget._lang = app.get_lang_data('QMainWindow.QWhatsNewWidget')


    def __init__(self, markdown_path: str) -> None:
        super().__init__()

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)

        self._label = QLabel(self._lang.get('title'))
        self._label.setProperty('h', 1)
        self.grid_layout.addWidget(self._label, 0, 0)

        self._markdown = QMarkDownWidget.from_file(markdown_path)
        self.grid_layout.addWidget(self._markdown, 1, 0)
#----------------------------------------------------------------------
