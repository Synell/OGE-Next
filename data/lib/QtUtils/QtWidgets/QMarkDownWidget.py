#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTextBrowser
import webbrowser, requests
#----------------------------------------------------------------------

    # Class
class QMarkDownWidget(QTextBrowser):
    def __init__(self, markdown: str = None) -> None:
        super().__init__()
        self.anchorClicked.connect(webbrowser.open)
        self.setReadOnly(True)
        if markdown: self.setMarkdown(markdown)

    def setMarkdown(self, markdown: str) -> None:
        super().setMarkdown(markdown)

    @staticmethod
    def from_file(path: str) -> 'QMarkDownWidget':
        with open(path, 'r', encoding = 'utf-8') as f:
            return QMarkDownWidget(f.read())

    @staticmethod
    def from_url(url: str) -> 'QMarkDownWidget':
        return QMarkDownWidget(requests.get(url).text)
#----------------------------------------------------------------------
