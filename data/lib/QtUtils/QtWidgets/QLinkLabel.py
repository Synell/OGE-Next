#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
#----------------------------------------------------------------------

    # Class
class QLinkLabel(QLabel):
    _start_text = '<a'
    _end_text = '</a>'
    link_color = '#4B9CF5'

    clicked = Signal(str)


    def __init__(self, text: str = '', parent = None) -> None:
        super().__init__(parent)
        self.set_text(text)
        self.setProperty('QLinkLabel', True)
        self.setOpenExternalLinks(False)
        self.linkActivated.connect(self._link_activated)


    def text(self) -> str:
        return self._text

    def text_only(self) -> str:
        return self._text_only


    def set_text(self, text: str) -> None:
        self._text = text
        self.update()

    def setText(self, text: str) -> None:
        self.set_text(text)


    def update(self) -> None:
        new_text = ''
        start = self._text.find(self._start_text)
        end = self._text.find(self._end_text)
        text = self._text

        self._text_only = ''

        while start != -1 and end != -1 and start < end:
            new_text += text[:start]
            self._text_only += text[:start]

            link_text = text[start + len(self._start_text) + 1 : end]
            base_link_text = link_text

            ending = link_text.find('>')
            if ending == -1: raise ValueError(f'Invalid link: {link_text}')
            link_text = f'{self._start_text} {link_text[:ending]} style=\"color: {self.link_color}; text-decoration: none;\"{link_text[ending:]}{self._end_text}'

            new_text += link_text
            text = text[end + len(self._end_text):]
            self._text_only += base_link_text[ending + 1:]

            start = text.find(self._start_text)
            end = text.find(self._end_text)

        new_text += text
        self._text_only += text

        super().setText(new_text)


    def _link_activated(self, link: str) -> None:
        self.clicked.emit(link)
#----------------------------------------------------------------------
