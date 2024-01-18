#----------------------------------------------------------------------

    # Libraries
from enum import StrEnum
#----------------------------------------------------------------------

    # Enum
class QSpecialCharacter(StrEnum):
    Null = chr(0x0000)
    Tabulation = chr(0x0009)
    LineFeed = chr(0x000a)
    FormFeed = chr(0x000c)
    CarriageReturn = chr(0x000d)
    Space = chr(0x0020)
    Nbsp = chr(0x00a0)
    SoftHyphen = chr(0x00ad)
    ReplacementCharacter = chr(0xfffd)
    ObjectReplacementCharacter = chr(0xfffc)
    ByteOrderMark = chr(0xfeff)
    ByteOrderSwapped = chr(0xfffe)
    ParagraphSeparator = chr(0x2029)
    LineSeparator = chr(0x2028)
    LastValidCodePoint = chr(0x10ffff)
#----------------------------------------------------------------------
