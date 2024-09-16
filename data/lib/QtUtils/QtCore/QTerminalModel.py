#----------------------------------------------------------------------

    # Librairies
import regex, os

from .QLangData import QLangData
from .QEnumColor import QEnumColor
from .QTerminalAction import QTerminalAction, QTerminalActionFabric
from .QTerminalElementModifier import QTerminalElementModifier
from . import QBaseApplication
from ..QtGui.QssParser import QssSelector
#----------------------------------------------------------------------

    # Class
class QTerminalModel:
    _lang: QLangData = QLangData.NoTranslation()

    _unique_style: str = ''
    _model: str = ''

    _app: QBaseApplication = None


    def init(app: QBaseApplication) -> None:
        QTerminalModel._lang = app.get_lang_data('QTerminalModel')
        QTerminalModel._app = app

        folder = app.save_data.get_template_dir(app.save_data.StyleSheetMode.Global)

        if not os.path.exists(path := (os.path.join(folder, 'QTerminalModel/unique_style.css'))): return
        with open(path, 'r', encoding = 'utf-8') as f:
            QTerminalModel._unique_style = f.read()

        if not os.path.exists(path := (os.path.join(folder, 'QTerminalModel/model.html'))): return
        with open(path, 'r', encoding = 'utf-8') as f:
            QTerminalModel._model = f.read()


    def __init__(self, *enum_colors: type[QEnumColor], name: str = 'Terminal') -> None:
        self._html = ''
        self._last_added = ''

        fg_color = QTerminalModel._app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QWebEngineView')
        )['color']
        bg_color = QTerminalModel._app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QWebEngineView')
        )['background-color']
        a_color = QTerminalModel._app.save_data.COLOR_LINK.hexa

        root_vars = [
            f'--fg: {fg_color};',
            f'--bg: {bg_color};',
        ]
        unique_styles = []

        for enum_color in enum_colors:
            for color in enum_color:
                root_vars.append(f'--{color.name.lower()}-bg: {color.value.hexa};')
                unique_styles.append(QTerminalModel._unique_style.replace('%name', color.name.lower()))

        self._parsed_model = (
            QTerminalModel._model
                .replace('%title', name)
                .replace('%vars', '\n'.join(root_vars))
                .replace('%a-color', a_color)
                .replace('%unique-styles', '\n'.join(unique_styles))
        )


    def _str_to_html(self, html: str, accept_empty: bool = True) -> str:
        if html.strip() == '' and not accept_empty:
            return ''

        return (html
            # .replace('<', '&lt;')
            # .replace('>', '&gt;')
            # .replace('&', '&amp;')
            .replace(' ', '&nbsp;')
            .replace('\r', '')
            .replace('\n', '<br>')
            .replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        )


    def _split_string_around_tags(self, input: str) -> list[str]:
        tag_pattern = regex.compile(r'<[^>]+>')

        split_result = tag_pattern.split(input)

        return split_result


    def _extract_attributes(self, input: str) -> list[tuple[str, tuple[str, ...]]]:
        tag_pattern = regex.compile(r'<(\w+)([^>]*)>')
        attr_pattern = regex.compile(r'(\w+)=["\']?([^"\']+)["\']?')

        results = []

        for tag_match in tag_pattern.finditer(input):
            tag_name = tag_match.group(1)
            attributes_string = tag_match.group(2)

            attributes = tuple(attr_pattern.findall(attributes_string))

            results.append((tag_name, attributes))

        return results


    def _build_element(self, text: str) -> str:
        split = self._split_string_around_tags(text)
        attributes = self._extract_attributes(text)

        for i in range(len(split)):
            split[i] = self._str_to_html(split[i], i >= 0)

            if i % 2 == 0: # Outside a tag
                pass

            else: # Inside a tag
                tag_name, tag_info = attributes[i // 2]

                attr_convert = {}
                attr_disable = {}
                extra_classes = []

                match tag_name:
                    case 'button':
                        tag_name = 'a'
                        extra_classes.append('button')
                        attr_convert = {
                            'click': 'onclick="sendButtonClicked(\'%s\')" href="javascript:void(0)"',
                        }

                    case 'a':
                        attr_convert = {
                            'href': 'onclick="sendButtonClicked(\'href|%s\')" href="javascript:void(0)"',
                        }

                assembled_attributes = []
                if extra_classes:
                    if 'class' in [t[0] for t in tag_info]:
                        tag_info = list(tag_info)
                        index = [t[0] for t in tag_info].index('class')
                        tag_info[index] = ('class', ' '.join(extra_classes) + ' ' + tag_info[index][1])

                    else:
                        tag_info = list(tag_info)
                        tag_info.append(('class', ' '.join(extra_classes)))
                        tag_info = tuple(tag_info)

                for attr_name, attr_value in tag_info:
                    if attr_name in attr_convert:
                        assembled_attributes.append(attr_convert[attr_name].replace('%s', attr_value))
                        continue

                    if attr_name in attr_disable:
                        continue

                    assembled_attributes.append(f'{attr_name}="{attr_value}"')

                assembled_attributes = ' '.join(assembled_attributes)

                split[i] = f'<{tag_name} {assembled_attributes}>{split[i]}</{tag_name}>'

        return ''.join(split)


    def log_empty(self, *args, **kwargs) -> QTerminalElementModifier:
        div = f'<div class="columns"></div>'
        self._html += self._last_added + div
        self._last_added = ''

        return QTerminalElementModifier(
            '.vertical-space',
            0,
            div,
            QTerminalElementModifier.Behaviour.AddInner
        )


    def _log_continuous(self, text: str) -> None:
        add = self._build_element(text)

        last_span = self._last_added.rfind('</span>')
        if last_span != -1:
            self._last_added = self._last_added[:last_span] + '<br>' + add + self._last_added[last_span:]
        else: self._last_added += add

        return QTerminalElementModifier(
            '.columns',
            -1,
            self._last_added,
            QTerminalElementModifier.Behaviour.ReplaceOuter
        )


    def log(self, text: str, *log_types: QEnumColor, continuous: bool = False) -> QTerminalElementModifier:
        if continuous: return self._log_continuous(text)

        if (not log_types) or (not text.strip()):
            return self.log_empty()

        div = f'<div class="columns">%s</div>'

        parts = (
            f'<div class="column">' + ''.join((
                f'<span class="special-text{" first" if i == 0 else ""} {log_type.name.lower()}">'
                    f'{self._lang.get(log_type.name.lower())}'
                f'</span>'
            ) for i, log_type in enumerate(log_types)) + '</div>',
            f'<span>{self._build_element(text)}</span>'
        )

        self._html += self._last_added
        self._last_added = div.replace('%s', '\n'.join(parts))

        return QTerminalElementModifier(
            '.vertical-space',
            -1,
            self._last_added,
            QTerminalElementModifier.Behaviour.AddInner
        )


    def render(self) -> str:
        return self._parsed_model.replace('%s', self._html + self._last_added)


    def clear(self) -> None:
        self._html = ''
        self._last_added = ''


    def convert_to_action(self, action: str) -> QTerminalAction:
        return QTerminalActionFabric.create(action)
#----------------------------------------------------------------------
