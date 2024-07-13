#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QSizePolicy, QFrame
from PySide6.QtCore import Qt
import re, webbrowser
from .QGridFrame import QGridFrame
from .QScrollableGridFrame import QScrollableGridFrame
from .QLinkLabel import QLinkLabel
from ..QtCore import QBaseApplication
from ..QtCore.QLangData import QLangData
#----------------------------------------------------------------------

    # Class
class QWhatsNewWidget(QGridFrame):
    class Block(QGridFrame):
        _translations: dict[str, str] = {
            'fix': 'fixed',
            'fixes': 'fixed',
            'bug fix': 'fixed',
            'bug fixes': 'fixed',
            'bugfix': 'fixed',
            'bugfixes': 'fixed',
            'hotfix': 'fixed',
            'hotfixes': 'fixed',
            'bug': 'fixed',
            'bugs': 'fixed',
            'crash fix': 'fixed',
            'crash fixes': 'fixed',
            'crashfix': 'fixed',
            'crashfixes': 'fixed',
            'crash': 'fixed',
            'crashes': 'fixed',
            'add': 'added',
            'adds': 'added',
            'change': 'changed',
            'changes': 'changed',
            'technical change': 'technical',
            'technical changes': 'technical',
            'update': 'updated',
            'updates': 'updated',
            'remove': 'removed',
            'removes': 'removed',
            'improve': 'improved',
            'improves': 'improved',
            'improvement': 'improved',
            'improvements': 'improved',
        }

        def __init__(self, title: str, content: str, is_title: bool) -> None:
            super().__init__()

            self.setProperty('type', 'title' if is_title else 'content')

            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(20)

            translated_title = QWhatsNewWidget.Block._translations.get(title.lower(), title)

            title_label = QLabel(translated_title if is_title else translated_title.upper())
            title_label.setProperty('color-block' if is_title else 'sub-color-block', True)
            if not is_title: title_label.setProperty('type', translated_title.lower().replace(' ', '-'))

            self.layout_.addWidget(title_label, 0, 0)
            title_label.setFixedWidth(100)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if is_title: content_label = QLabel(content)
            else:
                content_label = QLinkLabel(content)
                content_label.clicked.connect(lambda link: webbrowser.open(link))

            content_label.setWordWrap(True)
            content_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.layout_.addWidget(content_label, 0, 1)


    class SubSection(QGridFrame):
        def __init__(self, content: str) -> None:
            super().__init__()

            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(10)

            title_pattern = r'^##\s(.*)$'
            section_pattern = r'^-\s(.*)$'
            titles: list[str] = re.findall(title_pattern, content, flags=re.MULTILINE)
            sections: list[str] = re.split(r'^##\s.*$', content, flags=re.MULTILINE)[1:]

            for title, section in zip(titles, sections):
                title = re.sub(title_pattern, r'\1', title).strip()
                section_texts: list[str] = [s.strip() for s in re.findall(section_pattern, section, flags = re.MULTILINE)]

                for text in section_texts:
                    text = self._format_text(text)

                    block = QWhatsNewWidget.Block(title, text, False)
                    self.layout_.addWidget(block, self.layout_.rowCount(), 0)


        def _issues_and_features_link(self, text: str) -> str:
            issues_pattern = r'(?:(?:[Ff]eature)|(?:[Ii]ssue)) #\d+'
            issues = re.findall(issues_pattern, text)

            for issue in issues:
                issue_number = re.findall(r'\d+', issue)[0]
                text = text.replace(issue, f'<a href="{QWhatsNewWidget._git_link}/issues/{issue_number}">{issue}</a>')

            return text


        def _pull_requests_link(self, text: str) -> str:
            pull_pattern = r'(?:(?:[Pp]ull [Rr]equest)|(?:[Pp]R)) #\d+'
            pulls = re.findall(pull_pattern, text)

            for pull in pulls:
                pull_number = re.findall(r'\d+', pull)[0]
                text = text.replace(pull, f'<a href="{QWhatsNewWidget._git_link}/pull/{pull_number}">{pull}</a>')

            return text


        def _commits_link(self, text: str) -> str:
            commit_pattern = r'(?:(?:[Cc]ommit)|(?:[Cc]ommits)) [0-9a-fA-F]+'
            commits = re.findall(commit_pattern, text)

            for commit in commits:
                commit_hash = re.findall(r'[0-9a-fA-F]+', commit)[0]
                text = text.replace(commit, f'<a href="{QWhatsNewWidget._git_link}/commit/{commit_hash}">{commit}</a>')

            return text


        def _branches_link(self, text: str) -> str:
            branch_pattern = r'(?:(?:[Bb]ranch)|(?:[Bb]ranches)) [0-9a-zA-Z]+'
            branches = re.findall(branch_pattern, text)

            for branch in branches:
                branch_name = re.findall(r'[0-9a-zA-Z]+', branch)[0]
                text = text.replace(branch, f'<a href="{QWhatsNewWidget._git_link}/tree/{branch_name}">{branch}</a>')

            return text


        def _tags_link(self, text: str) -> str:
            tag_pattern = r'(?:(?:[Tt]ag)|(?:[Tt]ags)) [0-9a-zA-Z]+'
            tags = re.findall(tag_pattern, text)

            for tag in tags:
                tag_name = re.findall(r'[0-9a-zA-Z]+', tag)[0]
                text = text.replace(tag, f'<a href="{QWhatsNewWidget._git_link}/tags/{tag_name}">{tag}</a>')

            return text


        def _bold_text(self, text: str) -> str:
            return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)


        def _italic_text(self, text: str) -> str:
            return re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)


        def _underline_text(self, text: str) -> str:
            return re.sub(r'__(.*?)__', r'<u>\1</u>', text)


        def _strikethrough_text(self, text: str) -> str:
            return re.sub(r'~~(.*?)~~', r'<s>\1</s>', text)


        def _format_text(self, text: str) -> str:
            text = self._issues_and_features_link(text)
            text = self._pull_requests_link(text)
            text = self._commits_link(text)
            text = self._branches_link(text)
            text = self._tags_link(text)

            text = self._bold_text(text)
            text = self._italic_text(text)
            text = self._underline_text(text)
            text = self._strikethrough_text(text)

            return text



    class Section(QGridFrame):
        def __init__(self, title: str, content: str) -> None:
            super().__init__()

            self.layout_.setContentsMargins(0, 0, 0, 0)
            self.layout_.setSpacing(20)

            pattern = r'# \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})'
            matches = re.match(pattern, title)
            version = matches.group(1)
            date = matches.group(2)

            block = QWhatsNewWidget.Block(version, date, True)
            self.layout_.addWidget(block, 0, 0)

            subsection = QWhatsNewWidget.SubSection(content)
            self.layout_.addWidget(subsection, 1, 0)



    _lang: QLangData = QLangData.NoTranslation()
    _git_link: str = ''


    def init(app: QBaseApplication) -> None:
        QWhatsNewWidget._lang = app.get_lang_data('QMainWindow.QWhatsNewWidget')
        QWhatsNewWidget._git_link = app.GITHUB_LINK


    def __init__(self, markdown_path: str) -> None:
        super().__init__()

        self.setProperty('QWhatsNewWidget', True)

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(16)

        self._label = QLabel(self._lang.get('title'))
        self._label.setProperty('h', 1)
        self.layout_.addWidget(self._label, 0, 0)

        with open(markdown_path, 'r', encoding='utf-8') as file:
            sections = self._parse_into_sections(file.read())

        scroll_frame = QScrollableGridFrame()
        scroll_frame.layout_.setContentsMargins(0, 0, 0, 0)
        scroll_frame.layout_.setSpacing(20)
        self.layout_.addWidget(scroll_frame, 1, 0)

        last_section = sections[-1]

        for section in sections:
            scroll_frame.layout_.addWidget(section, scroll_frame.layout_.rowCount(), 0)

            if section != last_section:
                line = QFrame()
                line.setProperty('separator', True)
                line.setProperty('soft', True)
                line.setFixedHeight(2)
                scroll_frame.layout_.addWidget(line, scroll_frame.layout_.rowCount(), 0)


    def _parse_into_sections(self, text: str) -> tuple[Section]:
        pattern = r'.*-{2,}.*\n?' # Matches any line that contains at least two dashes
        text = re.sub(pattern, '', text)

        pattern = r'^#\s\[.*\]\s-\s.*$' # Matches any line that starts with a title
        titles: list[str] = re.findall(pattern, text, flags = re.MULTILINE)
        sections: list[str] = re.split(pattern, text, flags = re.MULTILINE)[1:] # [1:] to ignore text before the very first title

        titles = [title.strip() for title in titles]

        for i in range(len(sections)):
            sections[i] = sections[i].strip()

            while sections[i].find('\n\n') != -1:
                sections[i] = sections[i].replace('\n\n', '\n')

        # sections = [section.strip() for section in sections if section.strip() != '']

        return [QWhatsNewWidget.Section(title, content) for title, content in zip(titles, sections)]
#----------------------------------------------------------------------
