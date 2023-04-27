#----------------------------------------------------------------------

    # Libraries
from sys import argv
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QPauseAnimation, QRect, QEvent, QSequentialAnimationGroup, QPauseAnimation, QPropertyAnimation, Qt, QEasingCurve, Signal
from PySide6.QtNetwork import QLocalSocket, QLocalServer
from PySide6.QtGui import QIcon, QPixmap

from .QPlatform import QPlatform
from .QssParser import QssParser, QssSelector
from .QUtilsColor import QUtilsColor
from .QNamedLineEdit import QNamedLineEdit
from .QNamedTextEdit import QNamedTextEdit
from .QNamedComboBox import QNamedComboBox
from .QNamedSpinBox import QNamedSpinBox
from .QNamedDoubleSpinBox import QNamedDoubleSpinBox
from .QToggleButton import QToggleButton
from .QFileButton import QFileButton
from .QLinkLabel import QLinkLabel
#----------------------------------------------------------------------

    # Class
class QBaseApplication(QApplication):
    another_instance_opened = Signal()

    SERVER_NAME = 'myApp'

    COLOR_LINK = QUtilsColor.from_hex('#cccccc')

    def __init__(self, platform: QPlatform, single_instance: bool = False) -> None:
        super().__init__([argv[0]])
        self.window = QMainWindow()
        self.window.setWindowTitle('Base Qt Window')

        self.platform = platform

        self.must_update = None
        self.must_update_link = None

        self.must_restart = None

        self.save_data = None

        self._alerts = []
        self._has_alert_queue = True
        self._has_installed_event_filter = False

        if single_instance: self._start_listener()



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
        qss = QssParser(
            self.save_data.get_stylesheet(app = self, mode = self.save_data.StyleSheetMode.Local) + '\n' +
            self.save_data.get_stylesheet(app = self, mode = self.save_data.StyleSheetMode.Global)
        )

        self.COLOR_LINK = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QLabel', attributes = {'color': self.window.property('color')}, items = ['link'])
            )['color']
        )
        QLinkLabel.link_color = self.COLOR_LINK.hex

        QNamedLineEdit.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedLineEdit.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedLineEdit.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedLineEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedTextEdit.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedTextEdit.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedTextEdit.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedTextEdit': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedComboBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedComboBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedComboBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedComboBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedSpinBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedSpinBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedSpinBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QNamedDoubleSpinBox.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QNamedDoubleSpinBox.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']
        QNamedDoubleSpinBox.focus_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QNamedDoubleSpinBox': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'focus': True})
        )['color']

        QFileButton.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QFileButton': True}),
            QssSelector(widget = 'QLabel')
        )['color']
        QFileButton.hover_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QFileButton': True}),
            QssSelector(widget = 'QLabel', attributes = {'hover': True})
        )['color']

        QToggleButton.normal_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox')
        )['color']
        QToggleButton.normal_color_handle = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', items = ['handle'])
        )['color']
        QToggleButton.checked_color = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': self.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'])
        )['color']
        QToggleButton.checked_color_handle = qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QToggleButton': True}),
            QssSelector(widget = 'QCheckBox', states = ['checked'], items = ['handle'])
        )['color']

        return qss
#----------------------------------------------------------------------
