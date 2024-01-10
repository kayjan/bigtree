from enum import Enum, auto
from typing import Dict, List, Tuple


class ExportConstants:
    DOWN_RIGHT = "\u250c"
    VERTICAL_RIGHT = "\u251c"
    VERTICAL_LEFT = "\u2524"
    VERTICAL_HORIZONTAL = "\u253c"
    UP_RIGHT = "\u2514"
    VERTICAL = "\u2502"
    HORIZONTAL = "\u2500"

    DOWN_RIGHT_ROUNDED = "\u256D"
    UP_RIGHT_ROUNDED = "\u2570"

    DOWN_RIGHT_BOLD = "\u250F"
    VERTICAL_RIGHT_BOLD = "\u2523"
    VERTICAL_LEFT_BOLD = "\u252B"
    VERTICAL_HORIZONTAL_BOLD = "\u254B"
    UP_RIGHT_BOLD = "\u2517"
    VERTICAL_BOLD = "\u2503"
    HORIZONTAL_BOLD = "\u2501"

    DOWN_RIGHT_DOUBLE = "\u2554"
    VERTICAL_RIGHT_DOUBLE = "\u2560"
    VERTICAL_LEFT_DOUBLE = "\u2563"
    VERTICAL_HORIZONTAL_DOUBLE = "\u256C"
    UP_RIGHT_DOUBLE = "\u255a"
    VERTICAL_DOUBLE = "\u2551"
    HORIZONTAL_DOUBLE = "\u2550"

    PRINT_STYLES: Dict[str, Tuple[str, str, str]] = {
        "ansi": ("|   ", "|-- ", "`-- "),
        "ascii": ("|   ", "|-- ", "+-- "),
        "const": (
            f"{VERTICAL}   ",
            f"{VERTICAL_RIGHT}{HORIZONTAL}{HORIZONTAL} ",
            f"{UP_RIGHT}{HORIZONTAL}{HORIZONTAL} ",
        ),
        "const_bold": (
            f"{VERTICAL_BOLD}   ",
            f"{VERTICAL_RIGHT_BOLD}{HORIZONTAL_BOLD}{HORIZONTAL_BOLD} ",
            f"{UP_RIGHT_BOLD}{HORIZONTAL_BOLD}{HORIZONTAL_BOLD} ",
        ),
        "rounded": (
            f"{VERTICAL}   ",
            f"{VERTICAL_RIGHT}{HORIZONTAL}{HORIZONTAL} ",
            f"{UP_RIGHT_ROUNDED}{HORIZONTAL}{HORIZONTAL} ",
        ),
        "double": (
            f"{VERTICAL_DOUBLE}   ",
            f"{VERTICAL_RIGHT_DOUBLE}{HORIZONTAL_DOUBLE}{HORIZONTAL_DOUBLE} ",
            f"{UP_RIGHT_DOUBLE}{HORIZONTAL_DOUBLE}{HORIZONTAL_DOUBLE} ",
        ),
    }

    HPRINT_STYLES: Dict[str, Tuple[str, str, str, str, str, str, str]] = {
        "ansi": ("/", "+", "+", "+", "\\", "|", "-"),
        "ascii": ("+", "+", "+", "+", "+", "|", "-"),
        "const": (
            DOWN_RIGHT,
            VERTICAL_RIGHT,
            VERTICAL_LEFT,
            VERTICAL_HORIZONTAL,
            UP_RIGHT,
            VERTICAL,
            HORIZONTAL,
        ),
        "const_bold": (
            DOWN_RIGHT_BOLD,
            VERTICAL_RIGHT_BOLD,
            VERTICAL_LEFT_BOLD,
            VERTICAL_HORIZONTAL_BOLD,
            UP_RIGHT_BOLD,
            VERTICAL_BOLD,
            HORIZONTAL_BOLD,
        ),
        "rounded": (
            DOWN_RIGHT_ROUNDED,
            VERTICAL_RIGHT,
            VERTICAL_LEFT,
            VERTICAL_HORIZONTAL,
            UP_RIGHT_ROUNDED,
            VERTICAL,
            HORIZONTAL,
        ),
        "double": (
            DOWN_RIGHT_DOUBLE,
            VERTICAL_RIGHT_DOUBLE,
            VERTICAL_LEFT_DOUBLE,
            VERTICAL_HORIZONTAL_DOUBLE,
            UP_RIGHT_DOUBLE,
            VERTICAL_DOUBLE,
            HORIZONTAL_DOUBLE,
        ),
    }


class MermaidConstants:
    RANK_DIR: List[str] = ["TB", "BT", "LR", "RL"]
    LINE_SHAPES: List[str] = [
        "basis",
        "bumpX",
        "bumpY",
        "cardinal",
        "catmullRom",
        "linear",
        "monotoneX",
        "monotoneY",
        "natural",
        "step",
        "stepAfter",
        "stepBefore",
    ]
    NODE_SHAPES: Dict[str, str] = {
        "rounded_edge": """("{label}")""",
        "stadium": """(["{label}"])""",
        "subroutine": """[["{label}"]]""",
        "cylindrical": """[("{label}")]""",
        "circle": """(("{label}"))""",
        "asymmetric": """>"{label}"]""",
        "rhombus": """{{"{label}"}}""",
        "hexagon": """{{{{"{label}"}}}}""",
        "parallelogram": """[/"{label}"/]""",
        "parallelogram_alt": """[\\"{label}"\\]""",
        "trapezoid": """[/"{label}"\\]""",
        "trapezoid_alt": """[\\"{label}"/]""",
        "double_circle": """((("{label}")))""",
    }
    EDGE_ARROWS: Dict[str, str] = {
        "normal": "-->",
        "bold": "==>",
        "dotted": "-.->",
        "open": "---",
        "bold_open": "===",
        "dotted_open": "-.-",
        "invisible": "~~~",
        "circle": "--o",
        "cross": "--x",
        "double_normal": "<-->",
        "double_circle": "o--o",
        "double_cross": "x--x",
    }


class NewickState(Enum):
    PARSE_STRING = auto()
    PARSE_ATTRIBUTE_NAME = auto()
    PARSE_ATTRIBUTE_VALUE = auto()


class NewickCharacter(str, Enum):
    OPEN_BRACKET = "("
    CLOSE_BRACKET = ")"
    ATTR_START = "["
    ATTR_END = "]"
    ATTR_KEY_VALUE = "="
    ATTR_QUOTE = "'"
    SEP = ":"
    NODE_SEP = ","

    @classmethod
    def values(cls) -> List[str]:
        return [c.value for c in cls]
