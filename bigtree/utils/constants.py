from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple

from bigtree.utils import assertions


class ExportConstants:
    DOWN_RIGHT = "\u250c"
    DOWN_LEFT = "\u2510"
    VERTICAL_RIGHT = "\u251c"
    VERTICAL_LEFT = "\u2524"
    VERTICAL_HORIZONTAL = "\u253c"
    UP_RIGHT = "\u2514"
    UP_LEFT = "\u2518"
    VERTICAL = "\u2502"
    HORIZONTAL = "\u2500"
    HORIZONTAL_UP = "\u2534"
    HORIZONTAL_DOWN = "\u252c"

    DOWN_RIGHT_ROUNDED = "\u256d"
    DOWN_LEFT_ROUNDED = "\u256e"
    UP_RIGHT_ROUNDED = "\u2570"
    UP_LEFT_ROUNDED = "\u256f"

    DOWN_RIGHT_BOLD = "\u250f"
    DOWN_LEFT_BOLD = "\u2513"
    VERTICAL_RIGHT_BOLD = "\u2523"
    VERTICAL_LEFT_BOLD = "\u252b"
    VERTICAL_HORIZONTAL_BOLD = "\u254b"
    UP_RIGHT_BOLD = "\u2517"
    UP_LEFT_BOLD = "\u251b"
    VERTICAL_BOLD = "\u2503"
    HORIZONTAL_BOLD = "\u2501"
    HORIZONTAL_UP_BOLD = "\u253b"
    HORIZONTAL_DOWN_BOLD = "\u2533"

    DOWN_RIGHT_DOUBLE = "\u2554"
    DOWN_LEFT_DOUBLE = "\u2557"
    VERTICAL_RIGHT_DOUBLE = "\u2560"
    VERTICAL_LEFT_DOUBLE = "\u2563"
    VERTICAL_HORIZONTAL_DOUBLE = "\u256c"
    UP_RIGHT_DOUBLE = "\u255a"
    UP_LEFT_DOUBLE = "\u255d"
    VERTICAL_DOUBLE = "\u2551"
    HORIZONTAL_DOUBLE = "\u2550"
    HORIZONTAL_UP_DOUBLE = "\u2569"
    HORIZONTAL_DOWN_DOUBLE = "\u2566"

    BORDER_STYLES: Dict[str, Tuple[str, str, str, str, str, str]] = {
        "ansi": ("`", "`", "`", "`", "-", "|"),
        "ascii": ("+", "+", "+", "+", "-", "|"),
        "const": (DOWN_RIGHT, DOWN_LEFT, UP_RIGHT, UP_LEFT, HORIZONTAL, VERTICAL),
        "const_bold": (
            DOWN_RIGHT_BOLD,
            DOWN_LEFT_BOLD,
            UP_RIGHT_BOLD,
            UP_LEFT_BOLD,
            HORIZONTAL_BOLD,
            VERTICAL_BOLD,
        ),
        "rounded": (
            DOWN_RIGHT_ROUNDED,
            DOWN_LEFT_ROUNDED,
            UP_RIGHT_ROUNDED,
            UP_LEFT_ROUNDED,
            HORIZONTAL,
            VERTICAL,
        ),
        "double": (
            DOWN_RIGHT_DOUBLE,
            DOWN_LEFT_DOUBLE,
            UP_RIGHT_DOUBLE,
            UP_LEFT_DOUBLE,
            HORIZONTAL_DOUBLE,
            VERTICAL_DOUBLE,
        ),
    }

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

    VPRINT_STYLES: Dict[str, Tuple[str, str, str, str, str, str, str]] = {
        "ansi": ("/", "+", "+", "+", "\\", "-", "|"),
        "ascii": ("+", "+", "+", "+", "+", "-", "|"),
        "const": (
            DOWN_RIGHT,
            HORIZONTAL_DOWN,
            HORIZONTAL_UP,
            VERTICAL_HORIZONTAL,
            DOWN_LEFT,
            HORIZONTAL,
            VERTICAL,
        ),
        "const_bold": (
            DOWN_RIGHT_BOLD,
            HORIZONTAL_DOWN_BOLD,
            HORIZONTAL_UP_BOLD,
            VERTICAL_HORIZONTAL_BOLD,
            DOWN_LEFT_BOLD,
            HORIZONTAL_BOLD,
            VERTICAL_BOLD,
        ),
        "rounded": (
            DOWN_RIGHT_ROUNDED,
            HORIZONTAL_DOWN,
            HORIZONTAL_UP,
            VERTICAL_HORIZONTAL,
            DOWN_LEFT_ROUNDED,
            HORIZONTAL,
            VERTICAL,
        ),
        "double": (
            DOWN_RIGHT_DOUBLE,
            HORIZONTAL_DOWN_DOUBLE,
            HORIZONTAL_UP_DOUBLE,
            VERTICAL_HORIZONTAL_DOUBLE,
            DOWN_LEFT_DOUBLE,
            HORIZONTAL_DOUBLE,
            VERTICAL_DOUBLE,
        ),
    }


@dataclass
class BaseStyle:
    @classmethod
    def from_style(cls, style_name: str) -> "BaseStyle":
        raise NotImplementedError  # pragma: no cover


@dataclass
class BorderStyle(BaseStyle):
    """Base style for `print_tree` and `yield_tree` function."""

    TOP_LEFT: str
    TOP_RIGHT: str
    BOTTOM_LEFT: str
    BOTTOM_RIGHT: str
    HORIZONTAL: str
    VERTICAL: str

    @classmethod
    def from_style(cls, style_name: str) -> "BorderStyle":
        assertions.assert_style_in_dict(style_name, ExportConstants.BORDER_STYLES)
        return BorderStyle(*ExportConstants.BORDER_STYLES[style_name])

    def __post_init__(self) -> None:
        if (
            not len(self.TOP_LEFT)
            == len(self.TOP_RIGHT)
            == len(self.BOTTOM_LEFT)
            == len(self.BOTTOM_RIGHT)
            == len(self.HORIZONTAL)
            == len(self.VERTICAL)
            == 1
        ):
            raise ValueError("All style icons must have length 1")


@dataclass
class BasePrintStyle(BaseStyle):
    """Base style for `print_tree` and `yield_tree` function."""

    STEM: str
    BRANCH: str
    STEM_FINAL: str

    @classmethod
    def from_style(cls, style_name: str) -> "BasePrintStyle":
        assertions.assert_style_in_dict(style_name, ExportConstants.PRINT_STYLES)
        return BasePrintStyle(*ExportConstants.PRINT_STYLES[style_name])

    def __post_init__(self) -> None:
        if not len(self.STEM) == len(self.BRANCH) == len(self.STEM_FINAL):
            raise ValueError(
                "`stem`, `branch`, and `stem_final` are of different length"
            )


@dataclass
class BaseHPrintStyle(BaseStyle):
    """Base style for `hprint_tree` and `hyield_tree` function."""

    FIRST_CHILD: str
    SUBSEQUENT_CHILD: str
    SPLIT_BRANCH: str
    MIDDLE_CHILD: str
    LAST_CHILD: str
    STEM: str
    BRANCH: str

    @classmethod
    def from_style(cls, style_name: str) -> "BaseHPrintStyle":
        assertions.assert_style_in_dict(style_name, ExportConstants.HPRINT_STYLES)
        return BaseHPrintStyle(*ExportConstants.HPRINT_STYLES[style_name])

    def __post_init__(self) -> None:
        if (
            not len(self.FIRST_CHILD)
            == len(self.SUBSEQUENT_CHILD)
            == len(self.SPLIT_BRANCH)
            == len(self.MIDDLE_CHILD)
            == len(self.LAST_CHILD)
            == len(self.STEM)
            == len(self.BRANCH)
            == 1
        ):
            raise ValueError("All style icons must have length 1")


@dataclass
class BaseVPrintStyle(BaseStyle):
    """Base style for `hprint_tree` and `hyield_tree` function."""

    FIRST_CHILD: str
    SUBSEQUENT_CHILD: str
    SPLIT_BRANCH: str
    MIDDLE_CHILD: str
    LAST_CHILD: str
    STEM: str
    BRANCH: str

    @classmethod
    def from_style(cls, style_name: str) -> "BaseVPrintStyle":
        assertions.assert_style_in_dict(style_name, ExportConstants.VPRINT_STYLES)
        return BaseVPrintStyle(*ExportConstants.VPRINT_STYLES[style_name])

    def __post_init__(self) -> None:
        if (
            not len(self.FIRST_CHILD)
            == len(self.SUBSEQUENT_CHILD)
            == len(self.SPLIT_BRANCH)
            == len(self.MIDDLE_CHILD)
            == len(self.LAST_CHILD)
            == len(self.STEM)
            == len(self.BRANCH)
            == 1
        ):
            raise ValueError("All style icons must have length 1")


ANSIBorderStyle = BorderStyle.from_style("ansi")
ASCIIBorderStyle = BorderStyle.from_style("ascii")
ConstBorderStyle = BorderStyle.from_style("const")
ConstBoldBorderStyle = BorderStyle.from_style("const_bold")
RoundedBorderStyle = BorderStyle.from_style("rounded")
DoubleBorderStyle = BorderStyle.from_style("double")

ANSIPrintStyle = BasePrintStyle.from_style("ansi")
ASCIIPrintStyle = BasePrintStyle.from_style("ascii")
ConstPrintStyle = BasePrintStyle.from_style("const")
ConstBoldPrintStyle = BasePrintStyle.from_style("const_bold")
RoundedPrintStyle = BasePrintStyle.from_style("rounded")
DoublePrintStyle = BasePrintStyle.from_style("double")

ANSIHPrintStyle = BaseHPrintStyle.from_style("ansi")
ASCIIHPrintStyle = BaseHPrintStyle.from_style("ascii")
ConstHPrintStyle = BaseHPrintStyle.from_style("const")
ConstBoldHPrintStyle = BaseHPrintStyle.from_style("const_bold")
RoundedHPrintStyle = BaseHPrintStyle.from_style("rounded")
DoubleHPrintStyle = BaseHPrintStyle.from_style("double")

ANSIVPrintStyle = BaseVPrintStyle.from_style("ansi")
ASCIIVPrintStyle = BaseVPrintStyle.from_style("ascii")
ConstVPrintStyle = BaseVPrintStyle.from_style("const")
ConstBoldVPrintStyle = BaseVPrintStyle.from_style("const_bold")
RoundedVPrintStyle = BaseVPrintStyle.from_style("rounded")
DoubleVPrintStyle = BaseVPrintStyle.from_style("double")


class MermaidConstants:
    THEMES: List[str] = ["default", "neutral", "dark", "forest", "base"]
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
