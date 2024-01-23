#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QLogsList import QLogsList
from .QLangDataManager import QLangData
from .QWhatsNewWidget import QWhatsNewWidget
from . import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QWhatsNewDialog(QDialog):
    _lang: QLangData = QLangData.NoTranslation()


    def init(app: QBaseApplication) -> None:
        QWhatsNewDialog._lang = app.get_lang_data('QMainWindow.QWhatsNewDialog')


    def __init__(self, parent = None, markdown_path: str = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(self._lang.get('title'))

        self._root = QGridFrame(self)
        self._root.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._root.grid_layout.setSpacing(20)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        self._root.grid_layout.addWidget(frame, 0, 0)

        self._whats_new_widget: QWhatsNewWidget = QWhatsNewWidget(markdown_path)
        frame.grid_layout.addWidget(self._whats_new_widget, 0, 0)

        frame = QGridFrame()
        frame.grid_layout.setContentsMargins(20, 20, 20, 20)
        frame.grid_layout.setSpacing(0)
        frame.setProperty('border-top', True)
        self._root.grid_layout.addWidget(frame, 1, 0)
        self._root.grid_layout.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        right_buttons = QGridFrame()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(self._lang.get('QPushButton.ok'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        frame.grid_layout.addWidget(right_buttons, 0, 0)
        frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self._root.grid_layout)


    def exec(self) -> None:
        self.setMinimumSize(int(self.parent().window().size().width() * (205 / 256)), int(self.parent().window().size().height() * (13 / 15)))
        if super().exec(): pass
#----------------------------------------------------------------------
