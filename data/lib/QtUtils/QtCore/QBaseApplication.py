#----------------------------------------------------------------------

    # Libraries
from sys import argv
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QPauseAnimation, QRect, QEvent, QSequentialAnimationGroup, QPauseAnimation, QPropertyAnimation, Qt, QEasingCurve, Signal
from PySide6.QtNetwork import QLocalSocket, QLocalServer
from PySide6.QtGui import QIcon, QPixmap
from typing import Union

from .QSaveData import QSaveData
from ..QtCore import QLangData, QPlatform, QAppType
from ..QtGui import QUtilsColor, QssParser, QssSelector

from ..QtWidgets.QNamedLineEdit import QNamedLineEdit
from ..QtWidgets.QNamedTextEdit import QNamedTextEdit
from ..QtWidgets.QNamedTextBrowser import QNamedTextBrowser
from ..QtWidgets.QNamedComboBox import QNamedComboBox
from ..QtWidgets.QNamedSpinBox import QNamedSpinBox
from ..QtWidgets.QNamedDoubleSpinBox import QNamedDoubleSpinBox
from ..QtWidgets.QNamedHexSpinBox import QNamedHexSpinBox
from ..QtWidgets.QToggleButton import QToggleButton
from ..QtWidgets.QFileButton import QFileButton
from ..QtWidgets.QLinkLabel import QLinkLabel
from ..QtWidgets.QDropDownWidget import QDropDownWidget
from ..QtWidgets.QLogsList import QLogsList
from ..QtWidgets.QLogsDialog import QLogsDialog
from ..QtWidgets.QWhatsNewWidget import QWhatsNewWidget
from ..QtWidgets.QWhatsNewDialog import QWhatsNewDialog
from ..QtWidgets.QBetterGraphicsView import QBetterGraphicsView
from ..QtWidgets.QWidgetTabBar import QWidgetTabBarItem
from ..QtWidgets.QNamedDateTimeEdit import QNamedDateTimeEdit
from ..QtWidgets.QNamedDateEdit import QNamedDateEdit
from ..QtWidgets.QNamedTimeEdit import QNamedTimeEdit
#----------------------------------------------------------------------

    # Class
class QBaseApplication(QApplication):
    another_instance_opened = Signal()

    SERVER_NAME = 'myApp'
    GITHUB_LINK = ''

    COLOR_LINK = QUtilsColor.from_hex('#cccccc')

    def __init__(self, platform: QPlatform, app_type: QAppType, single_instance: bool = False) -> None:
        super().__init__([argv[0]])
        self.window = QMainWindow()
        self.window.setWindowTitle('Base Qt Window')

        self.platform = platform
        self.app_type = app_type

        self._must_update = None
        self._must_update_link = None

        self._must_restart = None

        self._save_data: QSaveData = None

        self._alerts = []
        self._has_alert_queue = True
        self._has_installed_event_filter = False

        if single_instance: self._start_listener()


    @property
    def must_update(self) -> bool:
        return self._must_update


    @property
    def must_restart(self) -> bool:
        return self._must_restart


    @property
    def save_data(self) -> QSaveData:
        return self._save_data


    @staticmethod
    def instance_exists(server_name: str) -> bool:
        socket = QLocalSocket()
        socket.connectToServer(server_name)
        return socket.state() == QLocalSocket.LocalSocketState.ConnectedState

    def is_unique(self) -> bool:
        return not QBaseApplication.instance_exists(self.SERVER_NAME)

    def _start_listener(self) -> None:
        self._listener = QLocalServer(self)
        self._listener.setSocketOptions(self._listener.SocketOption.WorldAccessOption)
        self._listener.newConnection.connect(lambda: self.another_instance_opened.emit())
        self._listener.listen(self.SERVER_NAME)
        print(f'Waiting for connections on "{self._listener.serverName()}"')


    def has_alert_queue(self) -> bool:
        return self._has_alert_queue

    def set_alert_queue(self, has_alert_queue: bool) -> None:
        self._has_alert_queue = has_alert_queue

    def show_alert(self, message: str, icon: QIcon|QPixmap = None, raise_duration: int = 350, pause_duration: int = 1300, fade_duration: int = 350, color: str = 'main') -> None:
        if not self._has_installed_event_filter:
            self.window.centralWidget().installEventFilter(self)
            self._has_installed_event_filter = True

        alert = QLabel(message, self.window.centralWidget(), alignment = Qt.AlignmentFlag.AlignCenter)
        alert.setWordWrap(True)
        if icon: alert.setPixmap(icon.pixmap(16, 16) if isinstance(icon, QIcon) else icon)
        alert.setProperty('QAlert', True)
        alert.setProperty('color', color)
        alert.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        alert.animation = QSequentialAnimationGroup(alert)
        alert.animation.addAnimation(QPropertyAnimation(alert, b'geometry', duration = raise_duration, easingCurve = QEasingCurve.Type.OutCubic))
        alert.animation.addAnimation(QPauseAnimation(pause_duration))
        alert.animation.addAnimation(QPropertyAnimation(alert, b'geometry', duration = fade_duration, easingCurve = QEasingCurve.Type.InCubic))
        self._alerts.append(alert)

        def delete_later() -> None:
            self._alerts.remove(alert)
            alert.deleteLater()
            if self._has_alert_queue and self._alerts:
                self._start_alert(self._alerts[0])
        alert.animation.finished.connect(delete_later)

        self._update_alert_animations()

        alert.setVisible(False)

        if self._has_alert_queue:
            if alert == self._alerts[0]: self._start_alert(alert)
        else: self._start_alert(alert)

        alert.setGeometry(alert.animation.animationAt(0).startValue())


    def _start_alert(self, alert: QLabel) -> None:
        alert.setVisible(True)
        alert.setGeometry(alert.animation.animationAt(0).startValue())
        alert.show()
        alert.raise_()
        alert.animation.start()

    def _update_alert_animations(self) -> None:
        width = self.window.centralWidget().width() - 20
        y = self.window.centralWidget().height() - 10
        margin = self.window.fontMetrics().height()
        for alert in self._alerts:
            height = alert.heightForWidth(width) + margin
            startRect = QRect(10, y, width, height)
            endRect = startRect.translated(0, -height)
            alert.animation.animationAt(0).setStartValue(startRect)
            alert.animation.animationAt(0).setEndValue(endRect)
            alert.animation.animationAt(2).setStartValue(endRect)
            alert.animation.animationAt(2).setEndValue(startRect)

    def eventFilter(self, obj: QLabel, event: QEvent) -> bool:
        try:
            if obj == self.window.centralWidget() and event.type() == event.Type.Resize and self._alerts:
                self._update_alert_animations()
                for alert in self._alerts:
                    anim = alert.animation
                    if isinstance(anim.currentAnimation(), QPauseAnimation):
                        alert.setGeometry(anim.animationAt(0).endValue())

        except: pass

        return super().eventFilter(obj, event)

    def load_colors(self) -> QssParser:
        self._qss = QssParser(self._save_data.get_stylesheet(app = self, mode = self._save_data.StyleSheetMode.All))

        self.COLOR_LINK = QUtilsColor(
            self._qss.search(
                QssSelector(widget = 'QLabel', attributes = {'color': self.window.property('color')}, items = ['link'])
            )['color']
        )
        QLinkLabel.link_color = self.COLOR_LINK.hex

        QNamedLineEdit.init(self)
        QNamedTextEdit.init(self)
        QNamedTextBrowser.init(self)
        QNamedComboBox.init(self)
        QNamedSpinBox.init(self)
        QNamedDoubleSpinBox.init(self)
        QNamedHexSpinBox.init(self)
        QFileButton.init(self)
        QToggleButton.init(self)
        QDropDownWidget.init(self)
        QLogsList.init(self)
        QLogsDialog.init(self)
        QWhatsNewWidget.init(self)
        QWhatsNewDialog.init(self)
        QBetterGraphicsView.init(self)
        QWidgetTabBarItem.init(self)
        QNamedDateTimeEdit.init(self)
        QNamedDateEdit.init(self)
        QNamedTimeEdit.init(self)

        return self._qss

    @property
    def qss(self) -> QssParser:
        return self._qss

    @property
    def language(self) -> str:
        return self._save_data.current_language

    @property
    def theme(self) -> str:
        return self._save_data.theme

    @property
    def theme_variant(self) -> str:
        return self._save_data.theme_variant

    def get_lang_data(self, path: str) -> Union[str, QLangData, list[Union[str, QLangData]]]:
        return self._save_data.get_lang_data(path)

    def get_icon_dir(self) -> str:
        return self._save_data.get_icon_dir()
    
    def get_icon(self, name: str, asQIcon = True, mode: QSaveData.IconMode = QSaveData.IconMode.Local) -> QIcon | str:
        return self._save_data.get_icon(name, asQIcon, mode)
#----------------------------------------------------------------------
