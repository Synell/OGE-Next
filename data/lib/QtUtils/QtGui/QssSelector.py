#----------------------------------------------------------------------

    # Class
class QssSelector:
    def __init__(self, widget: str, attributes: dict = {}, classes: list = [], ids: list = [], states: list = [], items: list = []):
        '''
        Class for storing a parsed QSS selector.

        Args:
            widget (str): Widget name
            attributes (dict, optional): Attributes (e.g. `{'key1': 'value1', 'key2': 'value2'}` for `[key1='value1'][key2='value2']`). Defaults to `{}`.
            classes (list, optional): Classes (e.g. `['class1', 'class2']` for `.class1.class2`). Defaults to `[]`.
            ids (list, optional): IDs (e.g. `['id1', 'id2']` for `#id1#id2`). Defaults to `[]`.
            states (list, optional): States (e.g. `['state1', 'state2']` for `:state1:state2`). Defaults to `[]`.
            items (list, optional): Items (e.g. `['item1', 'item2']` for `::item1::item2`). Defaults to `[]`.
        '''
        self._widget = widget
        self._attributes = attributes
        self._classes = classes
        self._ids = ids
        self._states = states
        self._items = items

    @property
    def widget(self) -> str:
        '''
        Widget name
        '''
        return self._widget

    @property
    def attributes(self) -> dict:
        '''
        Attributes (e.g. `{'key1': 'value1', 'key2': 'value2'}` for `[key1='value1'][key2='value2']`)
        '''
        return self._attributes

    @property
    def classes(self) -> list:
        '''
        Classes (e.g. `['class1', 'class2']` for `.class1.class2`)
        '''
        return self._classes

    @property
    def ids(self) -> list[str]:
        '''
        IDs (e.g. `['id1', 'id2']` for `#id1#id2`)
        '''
        return self._ids

    @property
    def states(self) -> list:
        '''
        States (e.g. `['state1', 'state2']` for `:state1:state2`)
        '''
        return self._states

    @property
    def items(self) -> list:
        '''
        Items (e.g. `['item1', 'item2']` for `::item1::item2`)
        '''
        return self._items
#----------------------------------------------------------------------
