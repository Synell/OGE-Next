#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSortFilterProxyModel
#----------------------------------------------------------------------

    # Class
class QBetterSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent: QWidget = None, *args, **kwargs) -> None:
        super(QBetterSortFilterProxyModel, self).__init__(parent, *args, **kwargs)

    def lessThan(self, left: str, right: str) -> bool:
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        try:
            return self._convert_value(left_data) < self._convert_value(right_data)

        except Exception:
            return left_data < right_data

    def _convert_value(self, val: str) -> int | float | str | None:
        if val.lower() == 'true': return True
        if val.lower() == 'false': return False

        if val.startswith('0x'):
            try: return int(val, 16)
            except ValueError: pass

        if val.startswith('0b'):
            try: return int(val, 2)
            except ValueError: pass

        if val.startswith('0o'):
            try: return int(val, 8)
            except ValueError: pass

        if (val.count('.') == 1) and val.replace('.', '').isdigit():
            try: return float(val)
            except ValueError: pass

        constructors = [int, str]
        for c in constructors:
            try: return c(val)
            except ValueError: pass

        return val
#----------------------------------------------------------------------
