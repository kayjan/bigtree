from __future__ import annotations

from typing import Any, Callable, Iterable, TypeVar

from bigtree.node import node
from bigtree.tree.export._html import TREE_HTML_TEMPLATE
from bigtree.utils import common, constants, exceptions

try:
    import rich
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    rich = MagicMock()


try:
    import json
    import uuid

    from IPython.display import HTML, display
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    uuid = MagicMock()
    HTML = MagicMock()
    display = MagicMock()


__all__ = [
    "print_rich",
    "print_tree",
    "yield_tree",
    "hprint_tree",
    "hyield_tree",
    "vprint_tree",
    "vyield_tree",
    "iprint_tree",
    "tree_to_html",
    "tree_to_newick",
]

T = TypeVar("T", bound=node.Node)


@exceptions.optional_dependencies_rich
def print_rich(
    pre_str: str,
    fill_str: str,
    node_str: str,
    _node: T,
    console: rich.Console,
    *,
    node_format: str | None = None,
    node_format_attr: str | Callable[[T], str] | None = None,
    edge_format: str | None = None,
    icon_prefix_attr: str | Callable[[T], str] | None = None,
    icon_suffix_attr: str | Callable[[T], str] | None = None,
    **kwargs: Any,
) -> None:
    """Add rich formatting and print tree to console

    Args:
        pre_str: edge of tree
        fill_str: the empty spaces
        node_str: node details
        _node: node to print
        console: rich console if exist, otherwise a console will be created
        node_format: node format, sets the node format of every node, e.g., bold magenta
        node_format_attr: If string type, it refers to ``Node`` attribute for node format. If callable type, it
            takes in the node itself and returns the format. This sets the format of custom nodes, and overrides default
            `node_format`
        edge_format: edge format, sets the edge format, e.g., bold magenta
        icon_prefix_attr: node icon infront of node name. Accepts emoji code (e.g., `:thumbs_up:`), unicode characters
            (e.g., `\U0001f600`), or anything rich supports. If string type, it refers to ``Node`` attribute for icon.
            If callable type, it takes in the node itself and returns the icon
        icon_suffix_attr: node icon behind node name. Accepts emoji code (e.g., `:thumbs_up:`), unicode characters
            (e.g., `\U0001f600`), or anything rich supports. If string type, it refers to ``Node`` attribute for icon.
            If callable type, it takes in the node itself and returns the icon
    """
    if icon_prefix_attr:
        node_str_prefix = common.get_attr(_node, icon_prefix_attr, "")
        node_str = f"{node_str_prefix} {node_str}" if node_str_prefix else node_str
    if icon_suffix_attr:
        node_str_suffix = common.get_attr(_node, icon_suffix_attr, "")
        node_str = f"{node_str} {node_str_suffix}" if node_str_suffix else node_str
    if node_format or node_format_attr:
        _node_format = common.get_attr(_node, node_format_attr, node_format)
        node_str = f"[{_node_format}]{node_str}[/]" if _node_format else node_str
    if edge_format:
        pre_str = f"[{edge_format}]{pre_str}[/]"
        fill_str = f"[{edge_format}]{fill_str}[/]"
    console.print(f"{pre_str}{fill_str}{node_str}", **kwargs)


def print_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    all_attrs: bool = False,
    attr_list: Iterable[str] | None = None,
    attr_format: str = "{k}={v}",
    attr_sep: str = ", ",
    attr_omit_null: bool = False,
    attr_bracket: tuple[str, str] = ("[", "]"),
    style: str | Iterable[str] | constants.BasePrintStyle = "const",
    **kwargs: Any,
) -> None:
    """Print tree to console, starting from `tree`. Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to choose which attributes to show or show all attributes, using `all_attrs` and `attr_list`
    - For showing attributes, able to customise the format of attributes and separator of attributes
    - Able to omit showing of attributes if it is null, using `attr_omit_null`
    - Able to customise open and close brackets if attributes are shown, using `attr_bracket`
    - Able to customise style, to choose from str, list[str], or inherit from constants.BasePrintStyle, using `style`
    - Able to support rich format, using `rich=True`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (list[str]): Choose own style for stem, branch, and final stem icons, they must have the same number of characters
    - (constants.BasePrintStyle): `ANSIPrintStyle`, `ASCIIPrintStyle`, `ConstPrintStyle`, `ConstBoldPrintStyle`,
        `RoundedPrintStyle`, `DoublePrintStyle` style or inherit from `constants.BasePrintStyle`

    For rich format, set `rich=True` and refer to ``print_rich`` for the list of arguments.

    Examples:
        **Printing tree**

        >>> from bigtree import Node, Tree
        >>> root = Node("a", alias="alias-a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", alias="alias-c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.show()
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        **Printing alias**

        >>> tree.show(alias="alias")
        alias-a
        ├── b
        │   ├── d
        │   └── e
        └── alias-c

        **Printing Sub-tree**

        >>> tree.show(node_name_or_path="b")
        b
        ├── d
        └── e

        >>> tree.show(max_depth=2)
        a
        ├── b
        └── c

        **Printing Attributes**

        >>> tree.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        └── c [age=60]

        >>> tree.show(attr_list=["name", "age"], attr_format="{k}:{v}", attr_sep="; ")
        a [name:a; age:90]
        ├── b [name:b; age:65]
        │   ├── d [name:d; age:40]
        │   └── e [name:e; age:35]
        └── c [name:c; age:60]

        >>> tree.show(attr_list=["age"], attr_bracket=["*(", ")"])
        a *(age=90)
        ├── b *(age=65)
        │   ├── d *(age=40)
        │   └── e *(age=35)
        └── c *(age=60)

        **Available Styles**

        >>> tree.show(style="ansi")
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        >>> tree.show(style="ascii")
        a
        |-- b
        |   |-- d
        |   +-- e
        +-- c

        >>> tree.show(style="const")
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> tree.show(style="const_bold")
        a
        ┣━━ b
        ┃   ┣━━ d
        ┃   ┗━━ e
        ┗━━ c

        >>> tree.show(style="rounded")
        a
        ├── b
        │   ├── d
        │   ╰── e
        ╰── c

        >>> tree.show(style="double")
        a
        ╠══ b
        ║   ╠══ d
        ║   ╚══ e
        ╚══ c

        **Custom Styles**

        >>> from bigtree import ANSIPrintStyle
        >>> tree.show(style=ANSIPrintStyle)
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        **Printing to a file**

        >>> import io
        >>> output = io.StringIO()
        >>> tree.show(file=output)
        >>> tree_string = output.getvalue()
        >>> print(tree_string)
        a
        ├── b
        │   ├── d
        │   └── e
        └── c
        <BLANKLINE>

        **Printing rich format**

        >>> from rich.console import Console
        >>> console = Console(record=True, color_system=None)  # optional, for doctest for docstring
        >>> tree.show(rich=True, node_format="bold magenta", edge_format="blue", console=console)
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

    Args:
        tree: tree to print
        alias: node attribute to use for node name in tree as alias to `node_name`
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        all_attrs: indicator to show all attributes, overrides `attr_list` and `attr_omit_null`
        attr_list: node attributes to print
        attr_format: if attributes are displayed, the format in which to display, uses k,v to correspond to
            attribute name and attribute value
        attr_sep: if attributes are displayed, the separator of attributes, defaults to comma
        attr_omit_null: indicator whether to omit showing of null attributes
        attr_bracket: open and close bracket for `all_attrs` or `attr_list`
        style: style of print
    """
    # Backwards-compatible, so signature does not change
    rich_display = kwargs.pop("rich", False)
    if rich_display:
        exceptions.optional_dependencies_rich(lambda: None)()
        from rich.console import Console

        kwargs["console"] = kwargs.get("console") or Console(force_terminal=True)
        if attr_bracket[0] == "[":
            # Handle specific case where [ will be mistaken as rich formatting
            attr_bracket = ("\\" + attr_bracket[0], attr_bracket[1])

        # Handle specific case where [ will be mistaken as rich formatting
        attr_bracket = (
            ("\\" + attr_bracket[0], attr_bracket[1])
            if attr_bracket[0] == "["
            else attr_bracket
        )

    for pre_str, fill_str, _node in yield_tree(
        tree=tree,
        node_name_or_path=node_name_or_path,
        max_depth=max_depth,
        style=style,
    ):
        # Get node_str (node name and attributes)
        attr_str = ""
        if all_attrs or attr_list:
            if len(attr_bracket) != 2:
                raise ValueError(
                    f"Expect open and close brackets in `attr_bracket`, received {attr_bracket}"
                )
            attr_bracket_open, attr_bracket_close = attr_bracket
            if all_attrs:
                attrs = _node.describe(exclude_attributes=["name"], exclude_prefix="_")
                attr_str_list = [attr_format.format(k=k, v=v) for k, v in attrs]
            else:
                if attr_omit_null:
                    attr_str_list = [
                        attr_format.replace("{k}", attr_name).replace(
                            "{v}", str(_node.get_attr(attr_name))
                        )
                        for attr_name in attr_list
                        if not common.isnull(_node.get_attr(attr_name))
                    ]
                else:
                    attr_str_list = [
                        attr_format.replace("{k}", attr_name).replace(
                            "{v}", str(_node.get_attr(attr_name))
                        )
                        for attr_name in attr_list
                        if hasattr(_node, attr_name)
                    ]
            attr_str = attr_sep.join(attr_str_list)
            if attr_str:
                attr_str = f" {attr_bracket_open}{attr_str}{attr_bracket_close}"
        name_str = _node.get_attr(alias) or _node.node_name
        node_str = f"{name_str}{attr_str}"
        if rich_display:
            print_rich(pre_str, fill_str, node_str, _node, **kwargs)
        else:
            print(f"{pre_str}{fill_str}{node_str}", **kwargs)


def yield_tree(
    tree: T,
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    style: str | Iterable[str] | constants.BasePrintStyle = "const",
) -> Iterable[tuple[str, str, T]]:
    """Generator method for customizing printing of tree, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to customise style, to choose from str, list[str], or inherit from constants.BasePrintStyle, using `style`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (list[str]): Choose own style for stem, branch, and final stem icons, they must have the same number of characters
    - (constants.BasePrintStyle): `ANSIPrintStyle`, `ASCIIPrintStyle`, `ConstPrintStyle`, `ConstBoldPrintStyle`,
        `RoundedPrintStyle`, `DoublePrintStyle` style or inherit from `constants.BasePrintStyle`

    Examples:
        **Yield tree**

        >>> from bigtree import Node, yield_tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> for branch, stem, node in yield_tree(root):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        **Yield Sub-tree**

        >>> for branch, stem, node in yield_tree(root, node_name_or_path="b"):
        ...     print(f"{branch}{stem}{node.node_name}")
        b
        ├── d
        └── e

        >>> for branch, stem, node in yield_tree(root, max_depth=2):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ├── b
        └── c

        **Available Styles**

        >>> for branch, stem, node in yield_tree(root, style="ansi"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        >>> for branch, stem, node in yield_tree(root, style="ascii"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        |-- b
        |   |-- d
        |   +-- e
        +-- c

        >>> for branch, stem, node in yield_tree(root, style="const"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> for branch, stem, node in yield_tree(root, style="const_bold"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ┣━━ b
        ┃   ┣━━ d
        ┃   ┗━━ e
        ┗━━ c

        >>> for branch, stem, node in yield_tree(root, style="rounded"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ├── b
        │   ├── d
        │   ╰── e
        ╰── c

        >>> for branch, stem, node in yield_tree(root, style="double"):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        ╠══ b
        ║   ╠══ d
        ║   ╚══ e
        ╚══ c

        **Custom Styles**

        >>> from bigtree import ANSIPrintStyle
        >>> for branch, stem, node in yield_tree(root, style=ANSIPrintStyle):
        ...     print(f"{branch}{stem}{node.node_name}")
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        **Printing Attributes**

        >>> for branch, stem, node in yield_tree(root, style="const"):
        ...     print(f"{branch}{stem}{node.node_name} [age={node.age}]")
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        └── c [age=60]

    Args:
        tree: tree to print
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        style: style of print

    Returns:
        Yields tree in format branch, stem, and node
    """
    from bigtree.tree.export._yield_tree import YieldTree

    yield_class = YieldTree(
        tree,
        node_name_or_path,
        max_depth,
        style,
    )
    yield from yield_class.yield_tree()


def hprint_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 0,
    style: str | Iterable[str] | constants.BaseHPrintStyle = "const",
    border_style: str | Iterable[str] | constants.BorderStyle | None = None,
    strip: bool = True,
    **kwargs: Any,
) -> None:
    """Print tree in horizontal orientation to console, starting from `tree`. Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select horizontal spacing between nodes, using `spacing`
    - Able to customise style, to choose from str, Iterable[str], or inherit from constants.BaseHPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must have the same number of characters
    - (constants.BaseHPrintStyle): `ANSIHPrintStyle`, `ASCIIHPrintStyle`, `ConstHPrintStyle`, `ConstBoldHPrintStyle`,
        `RoundedHPrintStyle`, `DoubleHPrintStyle` style or inherit from constants.BaseHPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BorderStyle): `ANSIBorderStyle`, `ASCIIBorderStyle`, `ConstBorderStyle`, `ConstBoldBorderStyle`,
        `RoundedBorderStyle`, `DoubleBorderStyle` style or inherit from constants.BorderStyle

    Examples:
        **Printing tree**

        >>> from bigtree import Node, hprint_tree
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> c = Node("c", parent=root)
        >>> d = Node("d", parent=b)
        >>> e = Node("e", parent=b)
        >>> hprint_tree(root)
                   ┌─ d
             ┌─ b ─┤
        ─ a ─┤     └─ e
             └─ c

        **Printing Sub-tree**

        >>> hprint_tree(root, node_name_or_path="b")
             ┌─ d
        ─ b ─┤
             └─ e

        >>> hprint_tree(root, max_depth=2)
             ┌─ b
        ─ a ─┤
             └─ c

        **Available Styles**

        >>> hprint_tree(root, style="ansi")
                   /- d
             /- b -+
        - a -+     \\- e
             \\- c

        >>> hprint_tree(root, style="ascii")
                   +- d
             +- b -+
        - a -+     +- e
             +- c

        >>> hprint_tree(root, style="const")
                   ┌─ d
             ┌─ b ─┤
        ─ a ─┤     └─ e
             └─ c

        >>> hprint_tree(root, style="const_bold")
                   ┏━ d
             ┏━ b ━┫
        ━ a ━┫     ┗━ e
             ┗━ c

        >>> hprint_tree(root, style="rounded")
                   ╭─ d
             ╭─ b ─┤
        ─ a ─┤     ╰─ e
             ╰─ c

        >>> hprint_tree(root, style="double")
                   ╔═ d
             ╔═ b ═╣
        ═ a ═╣     ╚═ e
             ╚═ c

        **Custom Styles**

        >>> from bigtree import ANSIHPrintStyle
        >>> hprint_tree(root, style=ANSIHPrintStyle)
                   /- d
             /- b -+
        - a -+     \\- e
             \\- c

        **Border**

        >>> hprint_tree(root, style="rounded", border_style="rounded")
                            ╭───────╮
                  ╭───────╮╭┤   d   │
                 ╭┤   b   ├┤╰───────╯
        ╭───────╮│╰───────╯│╭───────╮
        │   a   ├┤         ╰┤   e   │
        ╰───────╯│          ╰───────╯
                 │╭───────╮
                 ╰┤   c   │
                  ╰───────╯

        **Printing to a file**

        >>> import io
        >>> output = io.StringIO()
        >>> hprint_tree(root, file=output)
        >>> tree_string = output.getvalue()
        >>> print(tree_string)
                   ┌─ d
             ┌─ b ─┤
        ─ a ─┤     └─ e
             └─ c
        <BLANKLINE>

    Args:
        tree: tree to print
        alias: node attribute to use for node name in tree as alias to `node_name`
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        intermediate_node_name: indicator if intermediate nodes have node names
        spacing: horizontal spacing between node displays
        style: style of print
        border_style: style of border
        strip: whether to strip results
    """
    result = hyield_tree(
        tree,
        alias=alias,
        node_name_or_path=node_name_or_path,
        max_depth=max_depth,
        intermediate_node_name=intermediate_node_name,
        spacing=spacing,
        style=style,
        border_style=border_style,
        strip=strip,
    )
    print("\n".join(result), **kwargs)


def hyield_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 0,
    style: str | Iterable[str] | constants.BaseHPrintStyle = "const",
    border_style: str | Iterable[str] | constants.BorderStyle | None = None,
    strip: bool = True,
) -> list[str]:
    """Yield tree in horizontal orientation to console, starting from `tree`.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select horizontal spacing between nodes, using `spacing`
    - Able to customise style, to choose from str, Iterable[str], or inherit from constants.BaseHPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseHPrintStyle): `ANSIHPrintStyle`, `ASCIIHPrintStyle`, `ConstHPrintStyle`, `ConstBoldHPrintStyle`,
        `RoundedHPrintStyle`, `DoubleHPrintStyle` style or inherit from constants.BaseHPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BorderStyle): `ANSIBorderStyle`, `ASCIIBorderStyle`, `ConstBorderStyle`, `ConstBoldBorderStyle`,
        `RoundedBorderStyle`, `DoubleBorderStyle` style or inherit from constants.BorderStyle

    Examples:
        **Printing tree**

        >>> from bigtree import Node, hyield_tree
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> c = Node("c", parent=root)
        >>> d = Node("d", parent=b)
        >>> e = Node("e", parent=b)
        >>> result = hyield_tree(root)
        >>> print("\\n".join(result))
                   ┌─ d
             ┌─ b ─┤
        ─ a ─┤     └─ e
             └─ c

        **Printing Sub-tree**

        >>> result = hyield_tree(root, node_name_or_path="b")
        >>> print("\\n".join(result))
             ┌─ d
        ─ b ─┤
             └─ e

        >>> result = hyield_tree(root, max_depth=2)
        >>> print("\\n".join(result))
             ┌─ b
        ─ a ─┤
             └─ c

        **Available Styles**

        >>> result = hyield_tree(root, style="ansi")
        >>> print("\\n".join(result))
                   /- d
             /- b -+
        - a -+     \\- e
             \\- c

        >>> result = hyield_tree(root, style="ascii")
        >>> print("\\n".join(result))
                   +- d
             +- b -+
        - a -+     +- e
             +- c

        >>> result = hyield_tree(root, style="const")
        >>> print("\\n".join(result))
                   ┌─ d
             ┌─ b ─┤
        ─ a ─┤     └─ e
             └─ c

        >>> result = hyield_tree(root, style="const_bold")
        >>> print("\\n".join(result))
                   ┏━ d
             ┏━ b ━┫
        ━ a ━┫     ┗━ e
             ┗━ c

        >>> result = hyield_tree(root, style="rounded")
        >>> print("\\n".join(result))
                   ╭─ d
             ╭─ b ─┤
        ─ a ─┤     ╰─ e
             ╰─ c

        >>> result = hyield_tree(root, style="double")
        >>> print("\\n".join(result))
                   ╔═ d
             ╔═ b ═╣
        ═ a ═╣     ╚═ e
             ╚═ c

        **Custom Styles**

        >>> from bigtree import ANSIHPrintStyle
        >>> result = hyield_tree(root, style=ANSIHPrintStyle)
        >>> print("\\n".join(result))
                   /- d
             /- b -+
        - a -+     \\- e
             \\- c

        **Border**

        >>> result = hyield_tree(root, style="rounded", border_style="rounded")
        >>> print("\\n".join(result))
                            ╭───────╮
                  ╭───────╮╭┤   d   │
                 ╭┤   b   ├┤╰───────╯
        ╭───────╮│╰───────╯│╭───────╮
        │   a   ├┤         ╰┤   e   │
        ╰───────╯│          ╰───────╯
                 │╭───────╮
                 ╰┤   c   │
                  ╰───────╯

    Args:
        tree: tree to print
        alias: node attribute to use for node name in tree as alias to `node_name`
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        intermediate_node_name: indicator if intermediate nodes have node names
        spacing: horizontal spacing between node displays
        style: style of print
        border_style: style of border
        strip: whether to strip results

    Returns:
        Yield tree in horizontal format
    """
    from bigtree.tree.export._yield_tree import HYieldTree

    yield_class = HYieldTree(
        tree,
        alias,
        node_name_or_path,
        max_depth,
        intermediate_node_name,
        spacing,
        style,
        border_style,
    )
    return yield_class.yield_tree(strip)


def vprint_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 2,
    style: str | Iterable[str] | constants.BaseVPrintStyle = "const",
    border_style: str | Iterable[str] | constants.BorderStyle | None = "const",
    strip: bool = False,
    **kwargs: Any,
) -> None:
    """Print tree in vertical orientation to console, starting from `tree`. Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select horizontal spacing between nodes, using `spacing`
    - Able to customise style, to choose from str, Iterable[str], or inherit from constants.BaseVPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseVPrintStyle): `ANSIVPrintStyle`, `ASCIIVPrintStyle`, `ConstVPrintStyle`, `ConstBoldVPrintStyle`,
        `RoundedVPrintStyle`, `DoubleVPrintStyle` style or inherit from constants.BaseVPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BorderStyle): `ANSIBorderStyle`, `ASCIIBorderStyle`, `ConstBorderStyle`, `ConstBoldBorderStyle`,
        `RoundedBorderStyle`, `DoubleBorderStyle` style or inherit from constants.BorderStyle

    Examples:
        **Printing tree**

        >>> from bigtree import Node, vprint_tree
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> c = Node("c", parent=root)
        >>> d = Node("d", parent=b)
        >>> e = Node("e", parent=b)
        >>> vprint_tree(root, strip=True)
                ┌───┐
                │ a │
                └─┬─┘
             ┌────┴─────┐
           ┌─┴─┐      ┌─┴─┐
           │ b │      │ c │
           └─┬─┘      └───┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        **Printing Sub-tree**

        >>> vprint_tree(root, node_name_or_path="b", strip=True)
           ┌───┐
           │ b │
           └─┬─┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        >>> vprint_tree(root, max_depth=2, strip=True)
           ┌───┐
           │ a │
           └─┬─┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ b │  │ c │
        └───┘  └───┘

        **Available Styles**

        >>> vprint_tree(root, style="ansi", border_style="ansi", strip=True)
                `---`
                | a |
                `-+-`
             /----+-----\\
           `-+-`      `-+-`
           | b |      | c |
           `-+-`      `---`
          /--+---\\
        `-+-`  `-+-`
        | d |  | e |
        `---`  `---`

        >>> vprint_tree(root, style="ascii", border_style="ascii", strip=True)
                +---+
                | a |
                +-+-+
             +----+-----+
           +-+-+      +-+-+
           | b |      | c |
           +-+-+      +---+
          +--+---+
        +-+-+  +-+-+
        | d |  | e |
        +---+  +---+

        >>> vprint_tree(root, style="const", border_style="const", strip=True)
                ┌───┐
                │ a │
                └─┬─┘
             ┌────┴─────┐
           ┌─┴─┐      ┌─┴─┐
           │ b │      │ c │
           └─┬─┘      └───┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        >>> vprint_tree(root, style="const_bold", border_style="const_bold", strip=True)
                ┏━━━┓
                ┃ a ┃
                ┗━┳━┛
             ┏━━━━┻━━━━━┓
           ┏━┻━┓      ┏━┻━┓
           ┃ b ┃      ┃ c ┃
           ┗━┳━┛      ┗━━━┛
          ┏━━┻━━━┓
        ┏━┻━┓  ┏━┻━┓
        ┃ d ┃  ┃ e ┃
        ┗━━━┛  ┗━━━┛

        >>> vprint_tree(root, style="rounded", border_style="rounded", strip=True)
                ╭───╮
                │ a │
                ╰─┬─╯
             ╭────┴─────╮
           ╭─┴─╮      ╭─┴─╮
           │ b │      │ c │
           ╰─┬─╯      ╰───╯
          ╭──┴───╮
        ╭─┴─╮  ╭─┴─╮
        │ d │  │ e │
        ╰───╯  ╰───╯

        >>> vprint_tree(root, style="double", border_style="double", strip=True)
                ╔═══╗
                ║ a ║
                ╚═╦═╝
             ╔════╩═════╗
           ╔═╩═╗      ╔═╩═╗
           ║ b ║      ║ c ║
           ╚═╦═╝      ╚═══╝
          ╔══╩═══╗
        ╔═╩═╗  ╔═╩═╗
        ║ d ║  ║ e ║
        ╚═══╝  ╚═══╝

        **Custom Styles**

        >>> from bigtree import RoundedVPrintStyle, RoundedBorderStyle
        >>> vprint_tree(root, style=RoundedVPrintStyle, border_style=RoundedBorderStyle, strip=True)
                ╭───╮
                │ a │
                ╰─┬─╯
             ╭────┴─────╮
           ╭─┴─╮      ╭─┴─╮
           │ b │      │ c │
           ╰─┬─╯      ╰───╯
          ╭──┴───╮
        ╭─┴─╮  ╭─┴─╮
        │ d │  │ e │
        ╰───╯  ╰───╯

        **Printing to a file**

        >>> import io
        >>> output = io.StringIO()
        >>> vprint_tree(root, file=output, strip=True)
        >>> tree_string = output.getvalue()
        >>> print(tree_string)
                ┌───┐
                │ a │
                └─┬─┘
             ┌────┴─────┐
           ┌─┴─┐      ┌─┴─┐
           │ b │      │ c │
           └─┬─┘      └───┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘
        <BLANKLINE>

    Args:
        tree: tree to print
        alias: node attribute to use for node name in tree as alias to `node_name`
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        intermediate_node_name: indicator if intermediate nodes have node names
        spacing: horizontal spacing between node displays
        style: style of print
        border_style: style of border
        strip: whether to strip results
    """
    result = vyield_tree(
        tree,
        alias=alias,
        node_name_or_path=node_name_or_path,
        max_depth=max_depth,
        intermediate_node_name=intermediate_node_name,
        spacing=spacing,
        style=style,
        border_style=border_style,
        strip=strip,
    )
    print("\n".join(result), **kwargs)


def vyield_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str | None = None,
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 2,
    style: str | Iterable[str] | constants.BaseVPrintStyle = "const",
    border_style: str | Iterable[str] | constants.BorderStyle | None = "const",
    strip: bool = False,
) -> list[str]:
    """Yield tree in vertical orientation to console, starting from `tree`.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customise for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select horizontal spacing between nodes, using `spacing`
    - Able to customise style, to choose from str, Iterable[str], or inherit from constants.BaseVPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseVPrintStyle): `ANSIVPrintStyle`, `ASCIIVPrintStyle`, `ConstVPrintStyle`, `ConstBoldVPrintStyle`,
        `RoundedVPrintStyle`, `DoubleVPrintStyle` style or inherit from constants.BaseVPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double` style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BorderStyle): `ANSIBorderStyle`, `ASCIIBorderStyle`, `ConstBorderStyle`, `ConstBoldBorderStyle`,
        `RoundedBorderStyle`, `DoubleBorderStyle` style or inherit from constants.BorderStyle

    Examples:
        **Printing tree**

        >>> from bigtree import Node, vyield_tree
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> c = Node("c", parent=root)
        >>> d = Node("d", parent=b)
        >>> e = Node("e", parent=b)
        >>> result = vyield_tree(root, strip=True)
        >>> print("\\n".join(result))
                ┌───┐
                │ a │
                └─┬─┘
             ┌────┴─────┐
           ┌─┴─┐      ┌─┴─┐
           │ b │      │ c │
           └─┬─┘      └───┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        **Printing Sub-tree**

        >>> result = vyield_tree(root, node_name_or_path="b", strip=True)
        >>> print("\\n".join(result))
           ┌───┐
           │ b │
           └─┬─┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        >>> result = vyield_tree(root, max_depth=2, strip=True)
        >>> print("\\n".join(result))
           ┌───┐
           │ a │
           └─┬─┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ b │  │ c │
        └───┘  └───┘

        **Available Styles**

        >>> result = vyield_tree(root, style="ansi", border_style="ansi", strip=True)
        >>> print("\\n".join(result))
                `---`
                | a |
                `-+-`
             /----+-----\\
           `-+-`      `-+-`
           | b |      | c |
           `-+-`      `---`
          /--+---\\
        `-+-`  `-+-`
        | d |  | e |
        `---`  `---`

        >>> result = vyield_tree(root, style="ascii", border_style="ascii", strip=True)
        >>> print("\\n".join(result))
                +---+
                | a |
                +-+-+
             +----+-----+
           +-+-+      +-+-+
           | b |      | c |
           +-+-+      +---+
          +--+---+
        +-+-+  +-+-+
        | d |  | e |
        +---+  +---+

        >>> result = vyield_tree(root, style="const", border_style="const", strip=True)
        >>> print("\\n".join(result))
                ┌───┐
                │ a │
                └─┬─┘
             ┌────┴─────┐
           ┌─┴─┐      ┌─┴─┐
           │ b │      │ c │
           └─┬─┘      └───┘
          ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐
        │ d │  │ e │
        └───┘  └───┘

        >>> result = vyield_tree(root, style="const_bold", border_style="const_bold", strip=True)
        >>> print("\\n".join(result))
                ┏━━━┓
                ┃ a ┃
                ┗━┳━┛
             ┏━━━━┻━━━━━┓
           ┏━┻━┓      ┏━┻━┓
           ┃ b ┃      ┃ c ┃
           ┗━┳━┛      ┗━━━┛
          ┏━━┻━━━┓
        ┏━┻━┓  ┏━┻━┓
        ┃ d ┃  ┃ e ┃
        ┗━━━┛  ┗━━━┛

        >>> result = vyield_tree(root, style="rounded", border_style="rounded", strip=True)
        >>> print("\\n".join(result))
                ╭───╮
                │ a │
                ╰─┬─╯
             ╭────┴─────╮
           ╭─┴─╮      ╭─┴─╮
           │ b │      │ c │
           ╰─┬─╯      ╰───╯
          ╭──┴───╮
        ╭─┴─╮  ╭─┴─╮
        │ d │  │ e │
        ╰───╯  ╰───╯

        >>> result = vyield_tree(root, style="double", border_style="double", strip=True)
        >>> print("\\n".join(result))
                ╔═══╗
                ║ a ║
                ╚═╦═╝
             ╔════╩═════╗
           ╔═╩═╗      ╔═╩═╗
           ║ b ║      ║ c ║
           ╚═╦═╝      ╚═══╝
          ╔══╩═══╗
        ╔═╩═╗  ╔═╩═╗
        ║ d ║  ║ e ║
        ╚═══╝  ╚═══╝

        **Custom Styles**

        >>> from bigtree import RoundedVPrintStyle, RoundedBorderStyle
        >>> result = vyield_tree(root, style=RoundedVPrintStyle, border_style=RoundedBorderStyle, strip=True)
        >>> print("\\n".join(result))
                ╭───╮
                │ a │
                ╰─┬─╯
             ╭────┴─────╮
           ╭─┴─╮      ╭─┴─╮
           │ b │      │ c │
           ╰─┬─╯      ╰───╯
          ╭──┴───╮
        ╭─┴─╮  ╭─┴─╮
        │ d │  │ e │
        ╰───╯  ╰───╯

    Args:
        tree: tree to print
        alias: node attribute to use for node name in tree as alias to `node_name`
        node_name_or_path: node to print from, becomes the root node of printing
        max_depth: maximum depth of tree to print, based on `depth` attribute
        intermediate_node_name: indicator if intermediate nodes have node names
        spacing: horizontal spacing between node displays
        style: style of print
        border_style: style of border
        strip: whether to strip results

    Returns:
        Yield tree in vertical format
    """
    from bigtree.tree.export._yield_tree import VYieldTree

    yield_class = VYieldTree(
        tree,
        alias,
        node_name_or_path,
        max_depth,
        intermediate_node_name,
        spacing,
        style,
        border_style,
    )
    return yield_class.yield_tree(strip)


def iprint_tree(
    tree: T,
    **kwargs: Any,
) -> None:
    """Display tree interactively on jupyter notebook.

    Refer to ``tree_to_html`` for list of parameters.

    Customisations include

    - Node colour (generic or custom), width
    - Border colour (generic or custom), width, radius
    - Edge colour, width
    - Font colour, title size, size

    Examples:
        >>> from bigtree import Node
        >>> root = Node("a", species="human")
        >>> b = Node("b", age=65, species="human", parent=root)
        >>> c = Node("c", age=60, species="human", parent=root)
        >>> d = Node("d", age=40, species="human", parent=b)
        >>> e = Node("e", age=35, species="human", parent=b)
        >>> root.ishow(all_attrs=True)
        <IPython.core.display.HTML object>

    Args:
        tree: tree to display
        **kwargs: refer to ``tree_to_html`` for list of parameters
    """
    tree_html = tree_to_html(
        tree,
        **kwargs,
    )
    display(HTML(tree_html))


DEFAULT_NODE_COLOUR = "#f8f9fa"
DEFAULT_BORDER_COLOUR = "#dee2e6"
DEFAULT_FONT_COLOUR = "#333"
DEFAULT_BORDER_WIDTH = 1


def tree_to_html(
    tree: T,
    all_attrs: bool = False,
    attr_list: Iterable[str] | None = None,
    node_colour: str = "#f8f9fa",
    node_width: int = 160,
    border_colour: str = "#dee2e6",
    border_radius: int = 12,
    border_width: float | int | str = 1,
    edge_colour: str = "#ccc",
    edge_width: float | int = 1.5,
    font_colour: str = "#333",
    font_title_size: int = 13,
    font_size: int = 11,
    height: int = 500,
    width: int = 900,
) -> str:
    """Get html tree diagram.

    Args:
        tree: tree to display
        all_attrs: indicator to show all attributes, overrides `attr_list`
        attr_list: node attributes to print
        node_colour: fill colour of nodes, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for node_colour
        node_width: node width of nodes
        border_colour: colour of node borders, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for custom border_colour
        border_radius: node radius of nodes
        border_width: width of node borders, accepts int/float, otherwise if it is string it will
            be interpreted as the ``Node`` attribute for custom border_width
        edge_colour: colour of edges
        edge_width: width of edges
        font_colour: font colour, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for custom font_colour
        font_title_size: font size of title text in node
        font_size: font size of attribute text in node
        height: height of diagram
        width: width of diagram

    Returns:
        HTML string to display
    """
    from bigtree.tree.export import tree_to_nested_dict

    tree_id = f"tree_{uuid.uuid4().hex[:6]}"
    attr_list = list(attr_list) if attr_list else []

    additional_attr_list: list[str] = []

    def _get_colour_or_attr(colour_param: str, default_param: str) -> tuple[str, str]:
        colour_attr: str | None = None
        if not colour_param.startswith("#"):
            colour_attr = colour_param
            additional_attr_list.append(colour_param)
            colour_param = default_param
        return colour_param, colour_attr

    def _get_int_or_attr(
        int_param: int | float | str, default_param: int | float
    ) -> tuple[int | float, str]:
        param_attr: str | None = None
        if isinstance(int_param, str):
            param_attr = int_param
            additional_attr_list.append(int_param)
            int_param = default_param
        return int_param, param_attr

    node_colour, node_colour_attr = _get_colour_or_attr(
        node_colour, DEFAULT_NODE_COLOUR
    )
    border_colour, border_colour_attr = _get_colour_or_attr(
        border_colour, DEFAULT_BORDER_COLOUR
    )
    font_colour, font_colour_attr = _get_colour_or_attr(
        font_colour, DEFAULT_FONT_COLOUR
    )
    border_width, border_width_attr = _get_int_or_attr(
        border_width, DEFAULT_BORDER_WIDTH
    )
    attr_dict: dict[str, str] = dict(
        zip(attr_list + additional_attr_list, attr_list + additional_attr_list)
    )
    tree_information = tree_to_nested_dict(
        tree, attr_dict=attr_dict, all_attrs=all_attrs
    )
    tree_data = json.dumps(tree_information)
    return TREE_HTML_TEMPLATE.format(
        tree_id=tree_id,
        tree_data=tree_data,
        node_width=node_width,
        node_radius=border_radius,
        node_colour=node_colour,
        node_colour_attr=node_colour_attr,
        border_width=border_width,
        border_width_attr=border_width_attr,
        border_colour=border_colour,
        border_colour_attr=border_colour_attr,
        edge_width=edge_width,
        edge_colour=edge_colour,
        font_colour=font_colour,
        font_colour_attr=font_colour_attr,
        font_title_size=font_title_size,
        font_size=font_size,
        height=height,
        width=width,
        attr_to_ignore=f""", '{"', '".join(additional_attr_list)}'""",
    )


def tree_to_newick(
    tree: T,
    intermediate_node_name: bool = True,
    length_attr: str | None = None,
    length_sep: str | constants.NewickCharacter = constants.NewickCharacter.SEP,
    attr_list: Iterable[str] | None = None,
    attr_prefix: str = "&&NHX:",
    attr_sep: str | constants.NewickCharacter = constants.NewickCharacter.SEP,
) -> str:
    """Export tree to Newick notation. Useful for describing phylogenetic tree.

    In the Newick Notation (or New Hampshire Notation)

    - Tree is represented in round brackets i.e., `(child1,child2,child3)parent`
    - If there are nested trees, they will be in nested round brackets i.e., `((grandchild1)child1,(grandchild2,grandchild3)child2)parent`
    - If there is length attribute, they will be beside the name i.e., `(child1:0.5,child2:0.1)parent`
    - If there are other attributes, attributes are represented in square brackets i.e., `(child1:0.5[S:human],child2:0.1[S:human])parent[S:parent]`

    Customisations include

    - Omitting names of root and intermediate nodes, default all node names are shown
    - Changing length separator to another symbol, default is `:`
    - Adding an attribute prefix, default is `&&NHX:`
    - Changing the attribute separator to another symbol, default is `:`

    Examples:
        >>> from bigtree import Node, tree_to_newick
        >>> root = Node("a", species="human")
        >>> b = Node("b", age=65, species="human", parent=root)
        >>> c = Node("c", age=60, species="human", parent=root)
        >>> d = Node("d", age=40, species="human", parent=b)
        >>> e = Node("e", age=35, species="human", parent=b)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> tree_to_newick(root)
        '((d,e)b,c)a'

        >>> tree_to_newick(root, length_attr="age")
        '((d:40,e:35)b:65,c:60)a'

        >>> tree_to_newick(root, length_attr="age", attr_list=["species"])
        '((d:40[&&NHX:species=human],e:35[&&NHX:species=human])b:65[&&NHX:species=human],c:60[&&NHX:species=human])a[&&NHX:species=human]'

    Args:
        tree: tree to be exported
        intermediate_node_name: indicator if intermediate nodes have node names
        length_attr: node length attribute to extract to beside name
        length_sep: separator between node name and length, used if length_attr is non-empty
        attr_list: node attributes to extract into square bracket
        attr_prefix: prefix before all attributes, within square bracket, used if attr_list is non-empty
        attr_sep: separator between attributes, within square brackets, used if attr_list is non-empty

    Returns:
        Newick string representation of tree
    """
    if not tree:
        return ""
    if isinstance(length_sep, constants.NewickCharacter):
        length_sep = length_sep.value
    if isinstance(attr_sep, constants.NewickCharacter):
        attr_sep = attr_sep.value

    def _serialize(item: Any) -> Any:
        """Serialise item if it contains special Newick characters.

        Args:
            item: item to serialise

        Returns:
            Serialised item
        """
        if isinstance(item, str) and set(item).intersection(
            constants.NewickCharacter.values()
        ):
            item = f"""'{item.replace(constants.NewickCharacter.ATTR_QUOTE, '"')}'"""
        return item

    node_name_str = ""
    if intermediate_node_name or (not intermediate_node_name and tree.is_leaf):
        node_name_str = _serialize(tree.node_name)
    if length_attr and not tree.is_root:
        if not tree.get_attr(length_attr):
            raise ValueError(f"Length attribute does not exist for node {tree}")
        node_name_str += f"{length_sep}{tree.get_attr(length_attr)}"

    attr_str = ""
    if attr_list:
        attr_str = attr_sep.join(
            [
                f"{_serialize(k)}={_serialize(tree.get_attr(k))}"
                for k in attr_list
                if tree.get_attr(k)
            ]
        )
        if attr_str:
            attr_str = f"[{attr_prefix}{attr_str}]"

    if tree.is_leaf:
        return f"{node_name_str}{attr_str}"

    children_newick = ",".join(
        tree_to_newick(
            child,
            intermediate_node_name=intermediate_node_name,
            length_attr=length_attr,
            length_sep=length_sep,
            attr_list=attr_list,
            attr_prefix=attr_prefix,
            attr_sep=attr_sep,
        )
        for child in tree.children
    )
    return f"({children_newick}){node_name_str}{attr_str}"
