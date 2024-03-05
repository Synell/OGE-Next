#----------------------------------------------------------------------

    # Libraries
from ..QtUtils import QColorSet, QUtilsColor
import os
#----------------------------------------------------------------------

    # Class
class Info:
    def __new__(cls) -> None:
        return None

    build: str = '07e815bd'
    version: str = 'Experimental'

    application_name: str = 'Oge Next'

    save_path: str = os.path.abspath('./data/save.dat').replace('\\', '/')

    main_color_set: QColorSet = QColorSet(
        'yellow',
        QUtilsColor.from_hex('#D2A800'),
        QUtilsColor.from_hex('#BC9900'),
        QUtilsColor.from_hex('#E8BC07'),
        QUtilsColor.from_hex('#6E6123'),
    )
    neutral_color_set: QColorSet = QColorSet(
        'white',
        QUtilsColor.from_hex('#E3E3E3'),
        QUtilsColor.from_hex('#D7D7D7'),
        QUtilsColor.from_hex('#EFEFEF'),
        QUtilsColor.from_hex('#CACACA'),
    )

    icon_path: str = './data/icons/OGENext.svg'
#----------------------------------------------------------------------
