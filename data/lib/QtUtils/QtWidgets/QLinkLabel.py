#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
#----------------------------------------------------------------------

    # Class
class QLinkLabel(QLabel):
    start_text = '<a'
    end_text = '</a>'
    link_color = '#4B9CF5'

    clicked = Signal(str)

    def __init__(self, text: str = '', parent = None) -> None:
        super().__init__(parent)
        self.setText(text)
        self.setProperty('QLinkLabel', True)
        self.setOpenExternalLinks(False)
        self.linkActivated.connect(self.__linkActivated__)

    def setText(self, text: str = '') -> None:
        self.__text__ = text
        self.update()

    def update(self) -> None:
        new_text = ''
        start = self.__text__.find(self.start_text)
        end = self.__text__.find(self.end_text)
        text = self.__text__

        while start != -1 and end != -1 and start < end:
            new_text += text[:start]

            link_text = text[start + len(self.start_text) + 1 : end]
            base_link_text = link_text

            ending = link_text.find('>')
            if ending == -1: raise ValueError(f'Invalid link: {base_link_text}')
            link_text = f'{self.start_text} {link_text[:ending]} style=\"color: {self.link_color}; text-decoration: none;\"{link_text[ending:]}{self.end_text}'

            new_text += link_text
            text = text[end + len(self.end_text):]

            start = text.find(self.start_text)
            end = text.find(self.end_text)

        new_text += text

        super().setText(new_text)

    def __linkActivated__(self, link: str) -> None:
        self.clicked.emit(link)
#----------------------------------------------------------------------
