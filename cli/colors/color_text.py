from enum import Enum

class TerminalColor(Enum):
    RED = "\033[1;31;40m"
    GREEN ="\033[1;32m"
    WHITE ="\033[1;37;40m"

def color_text(text,color=TerminalColor.WHITE):
    """
        Colors the specified text
        params:
            text - text to be colored
            color - TerminalColor
        returns: colored Text
    """
    return f"{color.value}{text}{TerminalColor.WHITE.value}"
