#----------------------------------------------------------------------

    # Libraries
from enum import IntEnum
#----------------------------------------------------------------------

    # Class
class WidgetKey:
    class Type(IntEnum):
        Semester = 0
        Year = 1


    def __init__(self, widget_type: Type, id: int) -> None:
        self._widget_type = widget_type
        self._id = id


    @property
    def widget_type(self) -> Type:
        return self._widget_type


    @property
    def id(self) -> int:
        return self._id


    def __eq__(self, other: 'WidgetKey') -> bool:
        return self.widget_type == other.widget_type and self.id == other.id


    def __hash__(self) -> int:
        return hash((self.widget_type, self.id))


    def __repr__(self) -> str:
        return f'WidgetKey({self.widget_type}, {self.id})'
#----------------------------------------------------------------------
