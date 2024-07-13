#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from .QGridFrame import QGridFrame
from .QWhatsNewWidget import QWhatsNewWidget
from ..QtCore import QBaseApplication
from ..QtCore.QLangData import QLangData
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
        self._root.layout_.setContentsMargins(0, 0, 0, 0)
        self._root.layout_.setSpacing(20)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 0)
        frame.layout_.setSpacing(0)
        self._root.layout_.addWidget(frame, 0, 0)

        self._whats_new_widget: QWhatsNewWidget = QWhatsNewWidget(markdown_path)
        frame.layout_.addWidget(self._whats_new_widget, 0, 0)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        frame.setProperty('border-top', True)
        self._root.layout_.addWidget(frame, 1, 0)
        self._root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        right_buttons = QGridFrame()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(self._lang.get('QPushButton.ok'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(button, 0, 0)

        frame.layout_.addWidget(right_buttons, 0, 0)
        frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self._root.layout_)


    def exec(self) -> None:
        self.setMinimumSize(int(self.parent().window().size().width() * (205 / 256)), int(self.parent().window().size().height() * (13 / 15)))
        if super().exec(): pass
#----------------------------------------------------------------------
