from __future__ import annotations

import collections
from typing import Any, Iterable, List, Optional, Tuple, TypeVar, Union

from bigtree.node import node
from bigtree.utils import assertions, constants, iterators

__all__ = [
    "print_tree",
    "yield_tree",
    "hprint_tree",
    "hyield_tree",
    "vprint_tree",
    "vyield_tree",
    "tree_to_newick",
]

T = TypeVar("T", bound=node.Node)


def print_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str = "",
    max_depth: int = 0,
    all_attrs: bool = False,
    attr_list: Iterable[str] = [],
    attr_omit_null: bool = False,
    attr_bracket: List[str] = ["[", "]"],
    style: Union[str, Iterable[str], constants.BasePrintStyle] = "const",
    **kwargs: Any,
) -> None:
    """Print tree to console, starting from `tree`.
    Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to choose which attributes to show or show all attributes, using `attr_name_filter` and `all_attrs`
    - Able to omit showing of attributes if it is null, using `attr_omit_null`
    - Able to customize open and close brackets if attributes are shown, using `attr_bracket`
    - Able to customize style, to choose from str, List[str], or inherit from constants.BasePrintStyle, using `style`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (List[str]): Choose own style for stem, branch, and final stem icons, they must have the same number of characters
    - (constants.BasePrintStyle): `ANSIPrintStyle`, `ASCIIPrintStyle`, `ConstPrintStyle`, `ConstBoldPrintStyle`, `RoundedPrintStyle`,
        `DoublePrintStyle` style or inherit from `constants.BasePrintStyle`

    Examples:
        **Printing tree**

        >>> from bigtree import Node, print_tree
        >>> root = Node("a", alias="alias-a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", alias="alias-c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> print_tree(root)
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        **Printing alias**

        >>> print_tree(root, alias="alias")
        alias-a
        ├── b
        │   ├── d
        │   └── e
        └── alias-c

        **Printing Sub-tree**

        >>> print_tree(root, node_name_or_path="b")
        b
        ├── d
        └── e

        >>> print_tree(root, max_depth=2)
        a
        ├── b
        └── c

        **Printing Attributes**

        >>> print_tree(root, attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        └── c [age=60]

        >>> print_tree(root, attr_list=["age"], attr_bracket=["*(", ")"])
        a *(age=90)
        ├── b *(age=65)
        │   ├── d *(age=40)
        │   └── e *(age=35)
        └── c *(age=60)

        **Available Styles**

        >>> print_tree(root, style="ansi")
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        >>> print_tree(root, style="ascii")
        a
        |-- b
        |   |-- d
        |   +-- e
        +-- c

        >>> print_tree(root, style="const")
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> print_tree(root, style="const_bold")
        a
        ┣━━ b
        ┃   ┣━━ d
        ┃   ┗━━ e
        ┗━━ c

        >>> print_tree(root, style="rounded")
        a
        ├── b
        │   ├── d
        │   ╰── e
        ╰── c

        >>> print_tree(root, style="double")
        a
        ╠══ b
        ║   ╠══ d
        ║   ╚══ e
        ╚══ c

        **Custom Styles**

        >>> from bigtree import ANSIPrintStyle
        >>> print_tree(root, style=ANSIPrintStyle)
        a
        |-- b
        |   |-- d
        |   `-- e
        `-- c

        **Printing to a file**

        >>> import io
        >>> output = io.StringIO()
        >>> print_tree(root, file=output)
        >>> tree_string = output.getvalue()
        >>> print(tree_string)
        a
        ├── b
        │   ├── d
        │   └── e
        └── c
        <BLANKLINE>

    Args:
        tree (Node): tree to print
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        all_attrs (bool): indicator to show all attributes, defaults to False, overrides `attr_list` and `attr_omit_null`
        attr_list (Iterable[str]): list of node attributes to print, optional
        attr_omit_null (bool): indicator whether to omit showing of null attributes, defaults to False
        attr_bracket (List[str]): open and close bracket for `all_attrs` or `attr_list`
        style (Union[str, Iterable[str], constants.BasePrintStyle]): style of print, defaults to const
    """
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
                attr_str_list = [f"{k}={v}" for k, v in attrs]
            else:
                if attr_omit_null:
                    attr_str_list = [
                        f"{attr_name}={_node.get_attr(attr_name)}"
                        for attr_name in attr_list
                        if not assertions.isnull(_node.get_attr(attr_name))
                    ]
                else:
                    attr_str_list = [
                        f"{attr_name}={_node.get_attr(attr_name)}"
                        for attr_name in attr_list
                        if hasattr(_node, attr_name)
                    ]
            attr_str = ", ".join(attr_str_list)
            if attr_str:
                attr_str = f" {attr_bracket_open}{attr_str}{attr_bracket_close}"
        name_str = _node.get_attr(alias) or _node.node_name
        node_str = f"{name_str}{attr_str}"
        print(f"{pre_str}{fill_str}{node_str}", **kwargs)


def yield_tree(
    tree: T,
    node_name_or_path: str = "",
    max_depth: int = 0,
    style: Union[str, Iterable[str], constants.BasePrintStyle] = "const",
) -> Iterable[Tuple[str, str, T]]:
    """Generator method for customizing printing of tree, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to customize style, to choose from str, List[str], or inherit from constants.BasePrintStyle, using `style`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (List[str]): Choose own style for stem, branch, and final stem icons, they must have the same number of characters
    - (constants.BasePrintStyle): `ANSIPrintStyle`, `ASCIIPrintStyle`, `ConstPrintStyle`, `ConstBoldPrintStyle`, `RoundedPrintStyle`,
        `DoublePrintStyle` style or inherit from `constants.BasePrintStyle`

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
        tree (Node): tree to print
        node_name_or_path (str): node to print from, becomes the root node of printing, optional
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        style (Union[str, Iterable[str], constants.BasePrintStyle]): style of print, defaults to const
    """
    from bigtree.tree.helper import get_subtree

    tree = get_subtree(tree, node_name_or_path, max_depth)

    # Set style
    if isinstance(style, str):
        style_class = constants.BasePrintStyle.from_style(style)
    elif isinstance(style, constants.BasePrintStyle):
        style_class = style
    else:
        if len(list(style)) != 3:
            raise ValueError(
                "Please specify the style of stem, branch, and final stem in `style`"
            )
        style_class = constants.BasePrintStyle(*style)

    gap_str = " " * len(style_class.STEM)
    unclosed_depth = set()
    initial_depth = tree.depth
    for _node in iterators.preorder_iter(tree, max_depth=max_depth):
        pre_str = ""
        fill_str = ""
        if not _node.is_root:
            node_depth = _node.depth - initial_depth

            # Get fill_str (style_branch or style_stem_final)
            if _node.right_sibling:
                unclosed_depth.add(node_depth)
                fill_str = style_class.BRANCH
            else:
                if node_depth in unclosed_depth:
                    unclosed_depth.remove(node_depth)
                fill_str = style_class.STEM_FINAL

            # Get pre_str (style_stem, style_branch, style_stem_final, or gap)
            pre_str = ""
            for _depth in range(1, node_depth):
                if _depth in unclosed_depth:
                    pre_str += style_class.STEM
                else:
                    pre_str += gap_str

        yield pre_str, fill_str, _node


def hprint_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str = "",
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    style: Union[str, Iterable[str], constants.BaseHPrintStyle] = "const",
    border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = None,
    strip: bool = True,
    **kwargs: Any,
) -> None:
    """Print tree in horizontal orientation to console, starting from `tree`.
    Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to customize style, to choose from str, List[str], or inherit from constants.BaseHPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (Iterable[str]): Choose own style icons, they must have the same number of characters
    - (constants.BaseHPrintStyle): `ANSIHPrintStyle`, `ASCIIHPrintStyle`, `ConstHPrintStyle`, `ConstBoldHPrintStyle`,
        `RoundedHPrintStyle`, `DoubleHPrintStyle` style or inherit from constants.BaseHPrintStyle

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

    Args:
        tree (Node): tree to print
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        style (Union[str, Iterable[str], constants.BaseHPrintStyle]): style of print, defaults to const
        border_style (Union[str, Iterable[str], constants.BorderStyle]): style of border, defaults to None
        strip (bool): whether to strip results, defaults to True
    """
    result = hyield_tree(
        tree,
        alias=alias,
        node_name_or_path=node_name_or_path,
        intermediate_node_name=intermediate_node_name,
        max_depth=max_depth,
        style=style,
        border_style=border_style,
        strip=strip,
    )
    print("\n".join(result), **kwargs)


def hyield_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str = "",
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    style: Union[str, Iterable[str], constants.BaseHPrintStyle] = "const",
    border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = None,
    strip: bool = True,
) -> List[str]:
    """Yield tree in horizontal orientation to console, starting from `tree`.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to customize style, to choose from str, List[str], or inherit from constants.BaseHPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseHPrintStyle): `ANSIHPrintStyle`, `ASCIIHPrintStyle`, `ConstHPrintStyle`, `ConstBoldHPrintStyle`,
        `RoundedHPrintStyle`, `DoubleHPrintStyle` style or inherit from constants.BaseHPrintStyle

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
        tree (Node): tree to print
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        style (Union[str, Iterable[str], constants.BaseHPrintStyle]): style of print, defaults to const
        border_style (Union[str, Iterable[str], constants.BorderStyle]): style of border, defaults to None
        strip (bool): whether to strip results, defaults to True

    Returns:
        (List[str])
    """
    from bigtree.tree.export._stdout import (
        calculate_stem_pos,
        format_node,
        horizontal_join,
        vertical_join,
    )
    from bigtree.tree.helper import get_subtree

    tree = get_subtree(tree, node_name_or_path, max_depth)

    # Set style
    if isinstance(style, str):
        style_class = constants.BaseHPrintStyle.from_style(style)
    elif isinstance(style, constants.BaseHPrintStyle):
        style_class = style
    else:
        if len(list(style)) != 7:
            raise ValueError("Please specify the style of 7 icons in `style`")
        style_class = constants.BaseHPrintStyle(*style)

    if border_style is None:
        border_style_class = None
    elif isinstance(border_style, str):
        border_style_class = constants.BorderStyle.from_style(border_style)
    elif isinstance(border_style, constants.BorderStyle):
        border_style_class = border_style
    else:
        if len(list(border_style)) != 6:
            raise ValueError("Please specify the style of 6 icons in `border_style`")
        border_style_class = constants.BorderStyle(*border_style)

    # Calculate padding
    space = " "
    padding_depths = collections.defaultdict(int)
    if intermediate_node_name:
        for _idx, _children in enumerate(iterators.levelordergroup_iter(tree)):
            padding_depths[_idx + 1] = max(
                [
                    len(
                        format_node(
                            _node,
                            alias,
                            intermediate_node_name,
                            style_class,
                            border_style_class,
                            add_buffer=False,
                        )[0]
                    )
                    for _node in _children
                ]
            )

    def _hprint_branch(
        _node: Union[T, node.Node], _cur_depth: int
    ) -> Tuple[List[str], int]:
        """Get string for tree horizontally.
        Recursively iterate the nodes in post-order traversal manner.

        Args:
            _node (Node): node to get string
            _cur_depth (int): current depth of node

        Returns:
            (Tuple[List[str], int]): Intermediate/final result for node, index of branch
        """
        if not _node:
            # For binary node
            _node = node.Node(" ")
        node_display_lines = format_node(
            _node,
            alias,
            intermediate_node_name,
            style_class,
            border_style_class,
            padding_depths[_cur_depth],
        )
        node_mid = calculate_stem_pos(len(node_display_lines))

        children = list(_node.children) if any(list(_node.children)) else []
        if not len(children):
            return node_display_lines, node_mid

        result_children, result_idx = [], []
        cumulative_height = 0
        for idx, child in enumerate(children):
            result_child, result_branch_idx = _hprint_branch(child, _cur_depth + 1)
            result_idx.append(cumulative_height + result_branch_idx)
            cumulative_height += len(result_child)
            result_children.append(result_child)

        # Join children column
        children_display_lines = vertical_join(result_children)

        # Calculate index of first branch, last branch, total length, and midpoint
        first, last, total = (
            result_idx[0],
            result_idx[-1],
            len(children_display_lines),
        )
        mid = (first + last) // 2

        if len(children) == 1:
            # Special case for one child (need only one branch)
            result_prefix = (
                space * first + style_class.BRANCH + space * (total - first - 1)
            )
        elif len(children) == 2 and (last - first == 1):
            # Special case for two children (need split_branch)
            # Create gap if two children occupy two rows
            children_display_lines.insert(last, "")
            last = first + 2
            mid = (last - first) // 2
            result_prefix = (
                space * first
                + style_class.FIRST_CHILD
                + style_class.SPLIT_BRANCH
                + style_class.LAST_CHILD
            )
        else:
            result_prefix = space * first + style_class.FIRST_CHILD
            for idx, (bef, aft) in enumerate(zip(result_idx, result_idx[1:])):
                result_prefix += style_class.STEM * (aft - bef - 1)
                result_prefix += style_class.SUBSEQUENT_CHILD
            result_prefix = result_prefix[:-1] + style_class.LAST_CHILD
            result_prefix += space * (total - result_idx[-1] - 1)
            if mid in result_idx:
                stem = style_class.MIDDLE_CHILD if mid else style_class.FIRST_CHILD
                result_prefix = (
                    result_prefix[:mid] + stem + result_prefix[mid + 1 :]  # noqa
                )
            else:
                result_prefix = (
                    result_prefix[:mid]
                    + style_class.SPLIT_BRANCH
                    + result_prefix[mid + 1 :]  # noqa
                )
        parent_buffer = max(0, mid - node_mid)
        child_buffer = max(0, node_mid - mid)
        mid += child_buffer
        node_display_lines = [
            len(node_display_lines[0]) * space
        ] * parent_buffer + node_display_lines
        result_prefix = " " * child_buffer + result_prefix
        children_display_lines = [
            len(children_display_lines[0]) * space
        ] * child_buffer + children_display_lines
        result = horizontal_join(
            [node_display_lines, list(result_prefix), children_display_lines]
        )
        return result, mid

    result_tree, _ = _hprint_branch(tree, 1)
    if strip:
        return [result.rstrip() for result in result_tree]
    return result_tree


def vprint_tree(
    tree: T,
    alias: str = "node_name",
    node_name_or_path: str = "",
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 2,
    style: Union[str, Iterable[str], constants.BaseVPrintStyle] = "const",
    border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = "const",
    strip: bool = False,
    **kwargs: Any,
) -> None:
    """Print tree in vertical orientation to console, starting from `tree`.
    Accepts kwargs for print() function.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select spacing between nodes, using `spacing`
    - Able to customize style, to choose from str, Iterable[str], or inherit from constants.BaseVPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseVPrintStyle): `ANSIVPrintStyle`, `ASCIIVPrintStyle`, `ConstVPrintStyle`, `ConstBoldVPrintStyle`,
        `RoundedVPrintStyle`, `DoubleVPrintStyle` style or inherit from constants.BaseVPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
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

    Args:
        tree (Node): tree to print
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        spacing (int): spacing between node displays
        style (Union[str, Iterable[str], constants.BaseVPrintStyle]): style of print, defaults to const
        border_style (Union[str, Iterable[str], constants.BorderStyle]): style of border, defaults to const
        strip (bool): whether to strip results, defaults to False

    Returns:
        (List[str])
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
    node_name_or_path: str = "",
    max_depth: int = 0,
    intermediate_node_name: bool = True,
    spacing: int = 2,
    style: Union[str, Iterable[str], constants.BaseVPrintStyle] = "const",
    border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = "const",
    strip: bool = False,
) -> List[str]:
    """Yield tree in vertical orientation to console, starting from `tree`.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to hide names of intermediate nodes, using `intermediate_node_name`
    - Able to select spacing between nodes, using `spacing`
    - Able to customize style, to choose from str, Iterable[str], or inherit from constants.BaseVPrintStyle, using `style`
    - Able to toggle border, with border style to choose from str, Iterable[str], or inherit from constants.BorderStyle,
        using `border_style`
    - Able to have constant width output string or to strip the trailing spaces, using `strip`

    For style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
    - (Iterable[str]): Choose own style icons, they must be 1 character long
    - (constants.BaseVPrintStyle): `ANSIVPrintStyle`, `ASCIIVPrintStyle`, `ConstVPrintStyle`, `ConstBoldVPrintStyle`,
        `RoundedVPrintStyle`, `DoubleVPrintStyle` style or inherit from constants.BaseVPrintStyle

    For border_style,

    - (str): `ansi`, `ascii`, `const` (default), `const_bold`, `rounded`, `double`  style
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
        tree (Node): tree to print
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        spacing (int): spacing between node displays
        style (Union[str, Iterable[str], constants.BaseHPrintStyle]): style of print, defaults to const
        border_style (Union[str, Iterable[str], constants.BorderStyle]): style of border, defaults to const
        strip (bool): whether to strip results, defaults to False

    Returns:
        (List[str])
    """
    from bigtree.tree.export._stdout import (
        calculate_stem_pos,
        format_node,
        horizontal_join,
    )
    from bigtree.tree.helper import get_subtree

    tree = get_subtree(tree, node_name_or_path, max_depth)

    # Set style
    if isinstance(style, str):
        style_class = constants.BaseVPrintStyle.from_style(style)
    elif isinstance(style, constants.BaseVPrintStyle):
        style_class = style
    else:
        if len(list(style)) != 7:
            raise ValueError("Please specify the style of 7 icons in `style`")
        style_class = constants.BaseVPrintStyle(*style)

    if border_style is None:
        border_style_class = None
    elif isinstance(border_style, str):
        border_style_class = constants.BorderStyle.from_style(border_style)
    elif isinstance(border_style, constants.BorderStyle):
        border_style_class = border_style
    else:
        if len(list(border_style)) != 6:
            raise ValueError("Please specify the style of 6 icons in `border_style`")
        border_style_class = constants.BorderStyle(*border_style)

    space = " "

    def _vprint_branch(_node: Union[T, node.Node]) -> Tuple[List[str], int]:
        """Get string for tree vertically.
        Recursively iterate the nodes in post-order traversal manner.

        Args:
            _node (Node): node to get string

        Returns:
            (Tuple[List[str], int]): Intermediate/final result for node, index of branch
        """
        if not _node:
            # For binary node
            _node = node.Node(" ", parent=node.Node(" "))
        node_display_lines = format_node(
            _node, alias, intermediate_node_name, style_class, border_style_class
        )
        node_width = len(node_display_lines[0])
        node_mid = calculate_stem_pos(node_width)

        children = list(_node.children) if any(list(_node.children)) else []
        if not len(children):
            return node_display_lines, node_mid

        result_children, result_idx = [], []
        cumulative_width = 0
        for idx, child in enumerate(children):
            result_child, result_branch_idx = _vprint_branch(child)
            result_idx.append(cumulative_width + result_branch_idx)
            cumulative_width += len(result_child[0]) + spacing
            result_children.append(result_child)

        # Join children row
        children_display_lines = horizontal_join(result_children, spacing)

        # Calculate index of first branch, last branch, total length, and midpoint
        first, last, total = (
            result_idx[0],
            result_idx[-1],
            len(children_display_lines[0]),
        )
        mid = (first + last) // 2

        if len(children) == 1:
            # Special case for one child (need only one branch)
            result_prefix = (
                space * first + style_class.BRANCH + space * (total - first - 1)
            )
        else:
            result_prefix = space * first + style_class.FIRST_CHILD
            for idx, (bef, aft) in enumerate(zip(result_idx, result_idx[1:])):
                result_prefix += style_class.STEM * (aft - bef - 1)
                result_prefix += style_class.SUBSEQUENT_CHILD
            result_prefix = result_prefix[:-1] + style_class.LAST_CHILD
            result_prefix += space * (total - result_idx[-1] - 1)
            if mid in result_idx:
                result_prefix = (
                    result_prefix[:mid]
                    + style_class.MIDDLE_CHILD
                    + result_prefix[mid + 1 :]  # noqa
                )
            else:
                result_prefix = (
                    result_prefix[:mid]
                    + style_class.SPLIT_BRANCH
                    + result_prefix[mid + 1 :]  # noqa
                )
        result = []
        for result_line in node_display_lines:
            result_line_buffer = max(0, mid - node_mid) * space + result_line
            result_line_buffer += max(0, total - len(result_line_buffer)) * space
            result.append(result_line_buffer)
        for result_line in [result_prefix] + children_display_lines:
            result_line_buffer = max(0, node_mid - mid) * space + result_line
            result_line_buffer += max(0, node_width - len(result_line_buffer)) * space
            result.append(result_line_buffer)
        return result, mid

    result_tree, _ = _vprint_branch(tree)
    if strip:
        return [result.rstrip() for result in result_tree]
    return result_tree


def tree_to_newick(
    tree: T,
    intermediate_node_name: bool = True,
    length_attr: str = "",
    length_sep: Union[str, constants.NewickCharacter] = constants.NewickCharacter.SEP,
    attr_list: Iterable[str] = [],
    attr_prefix: str = "&&NHX:",
    attr_sep: Union[str, constants.NewickCharacter] = constants.NewickCharacter.SEP,
) -> str:
    """Export tree to Newick notation. Useful for describing phylogenetic tree.

    In the Newick Notation (or New Hampshire Notation),
      - Tree is represented in round brackets i.e., `(child1,child2,child3)parent`.
      - If there are nested trees, they will be in nested round brackets i.e., `((grandchild1)child1,(grandchild2,grandchild3)child2)parent`.
      - If there is length attribute, they will be beside the name i.e., `(child1:0.5,child2:0.1)parent`.
      - If there are other attributes, attributes are represented in square brackets i.e., `(child1:0.5[S:human],child2:0.1[S:human])parent[S:parent]`.

    Customizations include:
      - Omitting names of root and intermediate nodes, default all node names are shown.
      - Changing length separator to another symbol, default is `:`.
      - Adding an attribute prefix, default is `&&NHX:`.
      - Changing the attribute separator to another symbol, default is `:`.

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
        tree (Node): tree to be exported
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        length_attr (str): node length attribute to extract to beside name, optional
        length_sep (str): separator between node name and length, used if length_attr is non-empty, defaults to ":"
        attr_list (Iterable[str]): list of node attributes to extract into square bracket, optional
        attr_prefix (str): prefix before all attributes, within square bracket, used if attr_list is non-empty, defaults to "&&NHX:"
        attr_sep (str): separator between attributes, within square brackets, used if attr_list is non-empty, defaults to ":"

    Returns:
        (str)
    """
    if not tree:
        return ""
    if isinstance(length_sep, constants.NewickCharacter):
        length_sep = length_sep.value
    if isinstance(attr_sep, constants.NewickCharacter):
        attr_sep = attr_sep.value

    def _serialize(item: Any) -> Any:
        """Serialize item if it contains special Newick characters.

        Args:
            item (Any): item to serialize

        Returns:
            (Any)
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
