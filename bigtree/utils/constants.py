from typing import Dict, List, Tuple


class ExportConstants:
    AVAILABLE_STYLES: Dict[str, Tuple[str, str, str]] = {
        "ansi": ("|   ", "|-- ", "`-- "),
        "ascii": ("|   ", "|-- ", "+-- "),
        "const": ("\u2502   ", "\u251c\u2500\u2500 ", "\u2514\u2500\u2500 "),
        "const_bold": ("\u2503   ", "\u2523\u2501\u2501 ", "\u2517\u2501\u2501 "),
        "rounded": ("\u2502   ", "\u251c\u2500\u2500 ", "\u2570\u2500\u2500 "),
        "double": ("\u2551   ", "\u2560\u2550\u2550 ", "\u255a\u2550\u2550 "),
        "custom": ("", "", ""),
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
