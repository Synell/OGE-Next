#----------------------------------------------------------------------

    # Libraries
from .QssSelector import QssSelector
#----------------------------------------------------------------------

    # Class
class QssParser:    
    def __init__(self, stylesheet: str) -> None:
        '''Class for parsing QSS stylesheets.

        Args:
            stylesheet (str): QSS stylesheet to parse (e.g. `stylesheet = open('stylesheet.qss', 'r').read()`)
        '''
        self._styles = self._parse(stylesheet)


    def search(self, *selectors: QssSelector) -> dict:
        '''
        Search for a selector in the stylesheet.

        Args:
            selectors (QssSelector): Selectors to search for.

        Returns:
            dict: Dictionary of styles
        '''
        styles = self._styles

        for selector in selectors:
            found = False

            for key, value in styles.items():
                if selector.widget == key:
                    for v in value:
                        if v['properties']['attribute'] == selector.attributes:
                            if sorted(v['properties']['class']) == sorted(selector.classes):
                                if sorted(v['properties']['id']) == sorted(selector.ids):
                                    if sorted(v['properties']['state']) == sorted(selector.states):
                                        if sorted(v['properties']['item']) == sorted(selector.items):
                                            styles = v
                                            found = True
                                            if selector != selectors[-1]:
                                                styles = styles['children']
                                            break

                if found:
                    break

            if not found:
                return {}

        return styles['values']


    def _clear_comments(self, stylesheet: str) -> str:
        while '/*' in stylesheet:
            start = stylesheet.find('/*')
            end = stylesheet.find('*/')
            stylesheet = stylesheet.replace(stylesheet[start : end + 2], '', 1)
        
        while '//' in stylesheet:
            start = stylesheet.find('//')
            end = stylesheet.find('\n')
            stylesheet = stylesheet.replace(stylesheet[start : end], '', 1)

        return stylesheet


    def _split_selector(self, selector: str) -> tuple[str, dict[str, list | dict[str, str | int | bool]]]:
        split = {'class': [], 'id': [], 'attribute': {}, 'state': [], 'item': []}
        start = 0
        first = ''
        last = len(selector) - 1

        def append(s: str) -> None:
            if s.startswith('['):
                v = s.split('=')
                val = v[1].replace('\'', '').replace('\"', '')

                match val:
                    case 'true':
                        val = True
                    case 'false':
                        val = False
                    case int(val):
                        val = int(val)
                    case float(val):
                        val = float(val)
                    case _:
                        pass

                split['attribute'][v[0][1:]] = val

            elif s.startswith('#'):
                split['id'].append(s[1:])

            elif s.startswith('.'):
                split['class'].append(s[1:])

            elif s.startswith('::'):
                split['item'].append(s[2:])

            elif s.startswith(':'):
                split['state'].append(s[1:])

        i = 0
        for i in range(last + 1):
            if selector[i] in ['[', '#', '.', ':']:
                if i != last:
                    if selector[i + 1] == selector[i]:
                        continue

                    elif selector[i - 1] == selector[i]:
                        i -= 1

                append(selector[start:i].replace(']', ''))

                if not first:
                    first = selector[start:i]

                start = i

        if not first:
            first = selector[start:]
        else:
            append(selector[start:].replace(']', ''))

        return (first, split)


    def _parse(self, stylesheet: str) -> dict:
        def check_lst(lst: list, item: dict) -> int | None:
            for j in range(len(lst)):
                if lst[j]['properties'] == item:
                    return j

            return None

        stylesheet = self._clear_comments(stylesheet)
        stylesheet = stylesheet.replace('\n', '')
        while '  ' in stylesheet:
            stylesheet = stylesheet.replace('  ', ' ')

        styles = {}

        for style in stylesheet.split('}'):
            if style:
                style = style.split('{')

                selector = style[0].strip().replace('\t', '')
                style = style[1].strip().replace('\t', '')

                for select in selector.split(','):
                    select = select.strip()

                    path = styles
                    index = None
                    lst = select.split(' ')
                    for el in lst:
                        s = self._split_selector(el.strip())

                        if s[0] not in path: path[s[0]] = []
                        i = check_lst(path[s[0]], s[1])

                        if i is None:
                            path[s[0]].append({'properties': s[1], 'values': {}, 'children': {}})
                            i = len(path[s[0]]) - 1

                        path = path[s[0]]
                        if el != lst[-1]: path = path[i]['children']
                        index = i

                    if index is None:
                        index = len(path)
                        path.append({'properties': {'class': [], 'id': [], 'attribute': {}, 'state': [], 'item': []}, 'values': {}, 'children': {}})
                    path = path[index]['values']

                    for prop in style.split(';'):
                        prop = prop.strip()

                        if prop:
                            prop = prop.split(':')
                            path[prop[0].strip()] = prop[1].strip()

        return styles
#----------------------------------------------------------------------
