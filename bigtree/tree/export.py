from __future__ import annotations

import collections
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, TypeVar, Union
from urllib.request import urlopen

from bigtree.node.node import Node
from bigtree.tree.search import find_path
from bigtree.utils.assertions import assert_key_in_dict, assert_str_in_list
from bigtree.utils.constants import ExportConstants, MermaidConstants
from bigtree.utils.exceptions import (
    optional_dependencies_image,
    optional_dependencies_pandas,
)
from bigtree.utils.iterators import preorder_iter

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

try:
    import pydot
except ImportError:  # pragma: no cover
    pydot = None

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = ImageDraw = ImageFont = None


__all__ = [
    "print_tree",
    "yield_tree",
    "tree_to_dict",
    "tree_to_nested_dict",
    "tree_to_dataframe",
    "tree_to_dot",
    "tree_to_pillow",
    "tree_to_mermaid",
]

T = TypeVar("T", bound=Node)


def print_tree(
    tree: T,
    node_name_or_path: str = "",
    max_depth: int = 0,
    all_attrs: bool = False,
    attr_list: Iterable[str] = [],
    attr_omit_null: bool = False,
    attr_bracket: List[str] = ["[", "]"],
    style: str = "const",
    custom_style: Iterable[str] = [],
) -> None:
    """Print tree to console, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to choose which attributes to show or show all attributes, using `attr_name_filter` and `all_attrs`
    - Able to omit showing of attributes if it is null, using `attr_omit_null`
    - Able to customize open and close brackets if attributes are shown, using `attr_bracket`
    - Able to customize style, to choose from `ansi`, `ascii`, `const`, `rounded`, `double`, and `custom` style
        - Default style is `const` style
        - If style is set to custom, user can choose their own style for stem, branch and final stem icons
        - Stem, branch, and final stem symbol should have the same number of characters

    **Printing tree**

    >>> from bigtree import Node, print_tree
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    └── c

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

    Args:
        tree (Node): tree to print
        node_name_or_path (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        all_attrs (bool): indicator to show all attributes, defaults to False, overrides `attr_list` and `attr_omit_null`
        attr_list (Iterable[str]): list of node attributes to print, optional
        attr_omit_null (bool): indicator whether to omit showing of null attributes, defaults to False
        attr_bracket (List[str]): open and close bracket for `all_attrs` or `attr_list`
        style (str): style of print, defaults to abstract style
        custom_style (Iterable[str]): style of stem, branch and final stem, used when `style` is set to 'custom'
    """
    for pre_str, fill_str, _node in yield_tree(
        tree=tree,
        node_name_or_path=node_name_or_path,
        max_depth=max_depth,
        style=style,
        custom_style=custom_style,
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
                        if _node.get_attr(attr_name)
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
        node_str = f"{_node.node_name}{attr_str}"
        print(f"{pre_str}{fill_str}{node_str}")


def yield_tree(
    tree: T,
    node_name_or_path: str = "",
    max_depth: int = 0,
    style: str = "const",
    custom_style: Iterable[str] = [],
) -> Iterable[Tuple[str, str, T]]:
    """Generator method for customizing printing of tree, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name_or_path`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to customize style, to choose from `ansi`, `ascii`, `const`, `rounded`, `double`, and `custom` style
        - Default style is `const` style
        - If style is set to custom, user can choose their own style for stem, branch and final stem icons
        - Stem, branch, and final stem symbol should have the same number of characters

    **Printing tree**

    >>> from bigtree import Node, print_tree
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

    **Printing Sub-tree**

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
        style (str): style of print, defaults to abstract style
        custom_style (Iterable[str]): style of stem, branch and final stem, used when `style` is set to 'custom'
    """
    available_styles = ExportConstants.AVAILABLE_STYLES
    if style not in available_styles.keys():
        raise ValueError(
            f"Choose one of {available_styles.keys()} style, use `custom` to define own style"
        )

    tree = tree.copy()
    if node_name_or_path:
        tree = find_path(tree, node_name_or_path)
        if not tree:
            raise ValueError(f"Node name or path {node_name_or_path} not found")
    if not tree.is_root:
        tree.parent = None

    # Set style
    if style == "custom":
        if len(list(custom_style)) != 3:
            raise ValueError(
                "Custom style selected, please specify the style of stem, branch, and final stem in `custom_style`"
            )
        style_stem, style_branch, style_stem_final = custom_style
    else:
        style_stem, style_branch, style_stem_final = available_styles[style]

    if not len(style_stem) == len(style_branch) == len(style_stem_final):
        raise ValueError(
            "`style_stem`, `style_branch`, and `style_stem_final` are of different length"
        )

    gap_str = " " * len(style_stem)
    unclosed_depth = set()
    initial_depth = tree.depth
    for _node in preorder_iter(tree, max_depth=max_depth):
        pre_str = ""
        fill_str = ""
        if not _node.is_root:
            node_depth = _node.depth - initial_depth

            # Get fill_str (style_branch or style_stem_final)
            if _node.right_sibling:
                unclosed_depth.add(node_depth)
                fill_str = style_branch
            else:
                if node_depth in unclosed_depth:
                    unclosed_depth.remove(node_depth)
                fill_str = style_stem_final

            # Get pre_str (style_stem, style_branch, style_stem_final, or gap)
            pre_str = ""
            for _depth in range(1, node_depth):
                if _depth in unclosed_depth:
                    pre_str += style_stem
                else:
                    pre_str += gap_str

        yield pre_str, fill_str, _node


def tree_to_dict(
    tree: T,
    name_key: str = "name",
    parent_key: str = "",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> Dict[str, Any]:
    """Export tree to dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node path, and node attributes as a nested dictionary.

    >>> from bigtree import Node, tree_to_dict
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> tree_to_dict(root, name_key="name", parent_key="parent", attr_dict={"age": "person age"})
    {'/a': {'name': 'a', 'parent': None, 'person age': 90}, '/a/b': {'name': 'b', 'parent': 'a', 'person age': 65}, '/a/b/d': {'name': 'd', 'parent': 'b', 'person age': 40}, '/a/b/e': {'name': 'e', 'parent': 'b', 'person age': 35}, '/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

    For a subset of a tree

    >>> tree_to_dict(c, name_key="name", parent_key="parent", attr_dict={"age": "person age"})
    {'/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

    Args:
        tree (Node): tree to be exported
        name_key (str): dictionary key for `node.node_name`, defaults to 'name'
        parent_key (str): dictionary key for `node.parent.node_name`, optional
        attr_dict (Dict[str, str]): dictionary mapping node attributes to dictionary key,
            key: node attributes, value: corresponding dictionary key, optional
        all_attrs (bool): indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`, defaults to False
        max_depth (int): maximum depth to export tree, optional
        skip_depth (int): number of initial depths to skip, optional
        leaf_only (bool): indicator to retrieve only information from leaf nodes

    Returns:
        (Dict[str, Any])
    """
    tree = tree.copy()
    data_dict = {}

    def recursive_append(node: T) -> None:
        if node:
            if (
                (not max_depth or node.depth <= max_depth)
                and (not skip_depth or node.depth > skip_depth)
                and (not leaf_only or node.is_leaf)
            ):
                data_child: Dict[str, Any] = {}
                if name_key:
                    data_child[name_key] = node.node_name
                if parent_key:
                    parent_name = None
                    if node.parent:
                        parent_name = node.parent.node_name
                    data_child[parent_key] = parent_name
                if all_attrs:
                    data_child.update(
                        dict(
                            node.describe(
                                exclude_attributes=["name"], exclude_prefix="_"
                            )
                        )
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = node.get_attr(k)
                data_dict[node.path_name] = data_child
            for _node in node.children:
                recursive_append(_node)

    recursive_append(tree)
    return data_dict


def tree_to_nested_dict(
    tree: T,
    name_key: str = "name",
    child_key: str = "children",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
) -> Dict[str, Any]:
    """Export tree to nested dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node attribute names, and children as a nested recursive dictionary.

    >>> from bigtree import Node, tree_to_nested_dict
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> tree_to_nested_dict(root, all_attrs=True)
    {'name': 'a', 'age': 90, 'children': [{'name': 'b', 'age': 65, 'children': [{'name': 'd', 'age': 40}, {'name': 'e', 'age': 35}]}, {'name': 'c', 'age': 60}]}

    Args:
        tree (Node): tree to be exported
        name_key (str): dictionary key for `node.node_name`, defaults to 'name'
        child_key (str): dictionary key for list of children, optional
        attr_dict (Dict[str, str]): dictionary mapping node attributes to dictionary key,
            key: node attributes, value: corresponding dictionary key, optional
        all_attrs (bool): indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`, defaults to False
        max_depth (int): maximum depth to export tree, optional

    Returns:
        (Dict[str, Any])
    """
    tree = tree.copy()
    data_dict: Dict[str, List[Dict[str, Any]]] = {}

    def recursive_append(node: T, parent_dict: Dict[str, Any]) -> None:
        if node:
            if not max_depth or node.depth <= max_depth:
                data_child = {name_key: node.node_name}
                if all_attrs:
                    data_child.update(
                        dict(
                            node.describe(
                                exclude_attributes=["name"], exclude_prefix="_"
                            )
                        )
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = node.get_attr(k)
                if child_key in parent_dict:
                    parent_dict[child_key].append(data_child)
                else:
                    parent_dict[child_key] = [data_child]

                for _node in node.children:
                    recursive_append(_node, data_child)

    recursive_append(tree, data_dict)
    return data_dict[child_key][0]


@optional_dependencies_pandas
def tree_to_dataframe(
    tree: T,
    path_col: str = "path",
    name_col: str = "name",
    parent_col: str = "",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> pd.DataFrame:
    """Export tree to pandas DataFrame.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    >>> from bigtree import Node, tree_to_dataframe
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> tree_to_dataframe(root, name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
         path name parent  person age
    0      /a    a   None          90
    1    /a/b    b      a          65
    2  /a/b/d    d      b          40
    3  /a/b/e    e      b          35
    4    /a/c    c      a          60


    For a subset of a tree.

    >>> tree_to_dataframe(b, name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
         path name parent  person age
    0    /a/b    b      a          65
    1  /a/b/d    d      b          40
    2  /a/b/e    e      b          35

    Args:
        tree (Node): tree to be exported
        path_col (str): column name for `node.path_name`, defaults to 'path'
        name_col (str): column name for `node.node_name`, defaults to 'name'
        parent_col (str): column name for `node.parent.node_name`, optional
        attr_dict (Dict[str, str]): dictionary mapping node attributes to column name,
            key: node attributes, value: corresponding column in dataframe, optional
        all_attrs (bool): indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`, defaults to False
        max_depth (int): maximum depth to export tree, optional
        skip_depth (int): number of initial depths to skip, optional
        leaf_only (bool): indicator to retrieve only information from leaf nodes

    Returns:
        (pd.DataFrame)
    """
    tree = tree.copy()
    data_list = []

    def recursive_append(node: T) -> None:
        if node:
            if (
                (not max_depth or node.depth <= max_depth)
                and (not skip_depth or node.depth > skip_depth)
                and (not leaf_only or node.is_leaf)
            ):
                data_child: Dict[str, Any] = {}
                if path_col:
                    data_child[path_col] = node.path_name
                if name_col:
                    data_child[name_col] = node.node_name
                if parent_col:
                    parent_name = None
                    if node.parent:
                        parent_name = node.parent.node_name
                    data_child[parent_col] = parent_name

                if all_attrs:
                    data_child.update(
                        node.describe(exclude_attributes=["name"], exclude_prefix="_")
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = node.get_attr(k)
                data_list.append(data_child)
            for _node in node.children:
                recursive_append(_node)

    recursive_append(tree)
    return pd.DataFrame(data_list)


@optional_dependencies_image("pydot")
def tree_to_dot(
    tree: Union[T, List[T]],
    directed: bool = True,
    rankdir: str = "TB",
    bg_colour: str = "",
    node_colour: str = "",
    node_shape: str = "",
    edge_colour: str = "",
    node_attr: Callable[[T], Dict[str, Any]] | str = "",
    edge_attr: Callable[[T], Dict[str, Any]] | str = "",
) -> pydot.Dot:
    r"""Export tree or list of trees to image.
    Possible node attributes include style, fillcolor, shape.

    >>> from bigtree import Node, tree_to_dot
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> graph = tree_to_dot(root)

    Display image directly without saving (requires IPython)

    >>> from IPython.display import Image, display
    >>> plt = Image(graph.create_png())
    >>> display(plt)

    Export to image, dot file, etc.

    >>> graph.write_png("tree.png")
    >>> graph.write_dot("tree.dot")

    Export to string

    >>> graph.to_string()
    'strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\nc0 [label=c];\na0 -> c0;\n}\n'

    Defining node and edge attributes (using node attribute)

    >>> class CustomNode(Node):
    ...     def __init__(self, name, node_shape="", edge_label="", **kwargs):
    ...         super().__init__(name, **kwargs)
    ...         self.node_shape = node_shape
    ...         self.edge_label = edge_label
    ...
    ...     @property
    ...     def edge_attr(self):
    ...         if self.edge_label:
    ...             return {"label": self.edge_label}
    ...         return {}
    ...
    ...     @property
    ...     def node_attr(self):
    ...         if self.node_shape:
    ...             return {"shape": self.node_shape}
    ...         return {}
    >>>
    >>>
    >>> root = CustomNode("a", node_shape="circle")
    >>> b = CustomNode("b", edge_label="child", parent=root)
    >>> c = CustomNode("c", edge_label="child", parent=root)
    >>> d = CustomNode("d", node_shape="square", edge_label="child", parent=b)
    >>> e = CustomNode("e", node_shape="square", edge_label="child", parent=b)
    >>> graph = tree_to_dot(root, node_colour="gold", node_shape="diamond", node_attr="node_attr", edge_attr="edge_attr")
    >>> graph.write_png("assets/custom_tree.png")

    .. image:: https://github.com/kayjan/bigtree/raw/master/assets/custom_tree.png

    Alternative way to define node and edge attributes (using callable function)

    >>> def get_node_attribute(node: Node):
    ...     if node.is_leaf:
    ...         return {"shape": "square"}
    ...     return {"shape": "circle"}
    >>>
    >>>
    >>> root = CustomNode("a")
    >>> b = CustomNode("b", parent=root)
    >>> c = CustomNode("c", parent=root)
    >>> d = CustomNode("d", parent=b)
    >>> e = CustomNode("e", parent=b)
    >>> graph = tree_to_dot(root, node_colour="gold", node_attr=get_node_attribute)
    >>> graph.write_png("assets/custom_tree_callable.png")

    .. image:: https://github.com/kayjan/bigtree/raw/master/assets/custom_tree_callable.png

    Args:
        tree (Node/List[Node]): tree or list of trees to be exported
        directed (bool): indicator whether graph should be directed or undirected, defaults to True
        rankdir (str): layout direction, defaults to 'TB' (top to bottom), can be 'BT' (bottom to top),
            'LR' (left to right), 'RL' (right to left)
        bg_colour (str): background color of image, defaults to None
        node_colour (str): fill colour of nodes, defaults to None
        node_shape (str): shape of nodes, defaults to None
            Possible node_shape include "circle", "square", "diamond", "triangle"
        edge_colour (str): colour of edges, defaults to None
        node_attr (str | Callable): If string type, it refers to ``Node`` attribute for node style.
            If callable type, it takes in the node itself and returns the node style.
            This overrides `node_colour` and `node_shape` and defaults to None.
            Possible node styles include {"style": "filled", "fillcolor": "gold", "shape": "diamond"}
        edge_attr (str | Callable): If stirng type, it refers to ``Node`` attribute for edge style.
            If callable type, it takes in the node itself and returns the edge style.
            This overrides `edge_colour`, and defaults to None.
            Possible edge styles include {"style": "bold", "label": "edge label", "color": "black"}

    Returns:
        (pydot.Dot)
    """
    # Get style
    graph_style = dict(bgcolor=bg_colour) if bg_colour else dict()
    node_style = dict(style="filled", fillcolor=node_colour) if node_colour else dict()
    if node_shape:
        node_style["shape"] = node_shape
    edge_style = dict(color=edge_colour) if edge_colour else dict()

    tree = tree.copy()
    _graph = (
        pydot.Dot(graph_type="digraph", strict=True, rankdir=rankdir, **graph_style)
        if directed
        else pydot.Dot(graph_type="graph", strict=True, rankdir=rankdir, **graph_style)
    )

    if not isinstance(tree, list):
        tree = [tree]

    for _tree in tree:
        if not isinstance(_tree, Node):
            raise TypeError("Tree should be of type `Node`, or inherit from `Node`")

        name_dict: Dict[str, List[str]] = collections.defaultdict(list)

        def recursive_create_node_and_edges(
            parent_name: Optional[str], child_node: T
        ) -> None:
            _node_style = node_style.copy()
            _edge_style = edge_style.copy()

            child_label = child_node.node_name
            if child_node.path_name not in name_dict[child_label]:  # pragma: no cover
                name_dict[child_label].append(child_node.path_name)
            child_name = child_label + str(
                name_dict[child_label].index(child_node.path_name)
            )
            if node_attr:
                if isinstance(node_attr, str) and child_node.get_attr(node_attr):
                    _node_style.update(child_node.get_attr(node_attr))
                elif isinstance(node_attr, Callable):  # type: ignore
                    _node_style.update(node_attr(child_node))  # type: ignore
            if edge_attr:
                if isinstance(edge_attr, str) and child_node.get_attr(edge_attr):
                    _edge_style.update(child_node.get_attr(edge_attr))
                elif isinstance(edge_attr, Callable):  # type: ignore
                    _edge_style.update(edge_attr(child_node))  # type: ignore
            node = pydot.Node(name=child_name, label=child_label, **_node_style)
            _graph.add_node(node)
            if parent_name is not None:
                edge = pydot.Edge(parent_name, child_name, **_edge_style)
                _graph.add_edge(edge)
            for child in child_node.children:
                if child:
                    recursive_create_node_and_edges(child_name, child)

        recursive_create_node_and_edges(None, _tree.root)
    return _graph


@optional_dependencies_image("Pillow")
def tree_to_pillow(
    tree: T,
    width: int = 0,
    height: int = 0,
    start_pos: Tuple[int, int] = (10, 10),
    font_family: str = "",
    font_size: int = 12,
    font_colour: Union[Tuple[int, int, int], str] = "black",
    bg_colour: Union[Tuple[int, int, int], str] = "white",
    **kwargs: Any,
) -> Image.Image:
    """Export tree to image (JPG, PNG).
    Image will be similar format as `print_tree`, accepts additional keyword arguments as input to `yield_tree`

    >>> from bigtree import Node, tree_to_pillow
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> pillow_image = tree_to_pillow(root)

    Export to image (PNG, JPG) file, etc.

    >>> pillow_image.save("tree_pillow.png")
    >>> pillow_image.save("tree_pillow.jpg")

    Args:
        tree (Node): tree to be exported
        width (int): width of image, optional as width of image is calculated automatically
        height (int): height of image, optional as height of image is calculated automatically
        start_pos (Tuple[int, int]): start position of text, (x-offset, y-offset), defaults to (10, 10)
        font_family (str): file path of font family, requires .ttf file, defaults to DejaVuSans
        font_size (int): font size, defaults to 12
        font_colour (Union[Tuple[int, int, int], str]): font colour, accepts tuple of RGB values or string, defaults to black
        bg_colour (Union[Tuple[int, int, int], str]): background of image, accepts tuple of RGB values or string, defaults to white

    Returns:
        (PIL.Image.Image)
    """
    # Initialize font
    if not font_family:
        dejavusans_url = "https://github.com/kayjan/bigtree/raw/master/assets/DejaVuSans.ttf?raw=true"
        font_family = urlopen(dejavusans_url)
    try:
        font = ImageFont.truetype(font_family, font_size)
    except OSError:
        raise ValueError(
            f"Font file {font_family} is not found, set `font_family` parameter to point to a valid .ttf file."
        )

    # Initialize text
    image_text = []
    for branch, stem, node in yield_tree(tree, **kwargs):
        image_text.append(f"{branch}{stem}{node.node_name}\n")

    # Calculate image dimension from text, otherwise override with argument
    def get_list_of_text_dimensions(
        text_list: List[str],
    ) -> List[Tuple[int, int, int, int]]:
        """Get list dimensions

        Args:
            text_list (List[str]): list of texts

        Returns:
            (List[Tuple[int, int, int, int]]): list of (left, top, right, bottom) bounding box
        """
        _image = Image.new("RGB", (0, 0))
        _draw = ImageDraw.Draw(_image)
        return [_draw.textbbox((0, 0), text_line, font=font) for text_line in text_list]

    text_dimensions = get_list_of_text_dimensions(image_text)
    text_height = sum(
        [text_dimension[3] + text_dimension[1] for text_dimension in text_dimensions]
    )
    text_width = max(
        [text_dimension[2] + text_dimension[0] for text_dimension in text_dimensions]
    )
    image_text_str = "".join(image_text)
    width = max(width, text_width + 2 * start_pos[0])
    height = max(height, text_height + 2 * start_pos[1])

    # Initialize and draw image
    image = Image.new("RGB", (width, height), bg_colour)
    image_draw = ImageDraw.Draw(image)
    image_draw.text(start_pos, image_text_str, font=font, fill=font_colour)
    return image


def tree_to_mermaid(
    tree: T,
    title: str = "",
    rankdir: str = "TB",
    line_shape: str = "basis",
    node_colour: str = "",
    node_border_colour: str = "",
    node_border_width: float = 1,
    node_shape: str = "rounded_edge",
    node_shape_attr: Callable[[T], str] | str = "",
    edge_arrow: str = "normal",
    edge_arrow_attr: Callable[[T], str] | str = "",
    edge_label: str = "",
    node_attr: Callable[[T], str] | str = "",
    **kwargs: Any,
) -> str:
    r"""Export tree to mermaid Markdown text. Accepts additional keyword arguments as input to `yield_tree`

    Parameters for customizations that applies to entire flowchart include
        - Title, `title`
        - Layout direction, `rankdir`
        - Line shape or curvature, `line_shape`
        - Fill colour of nodes, `node_colour`
        - Border colour of nodes, `node_border_colour`
        - Border width of nodes, `node_border_width`
        - Node shape, `node_shape`
        - Edge arrow style, `edge_arrow`

    Parameters for customizations that apply to customized nodes
        - Fill colour of nodes, fill under `node_attr`
        - Border colour of nodes, stroke under `node_attr`
        - Border width of nodes, stroke-width under `node_attr`
        - Node shape, `node_shape_attr`
        - Edge arrow style, `edge_arrow_attr`
        - Edge label, `edge_label`

    **Accepted Parameter Values**

    Possible `rankdir`
        - `TB`: top-to-bottom
        - `BT`: bottom-to-top
        - `LR`: left-to-right
        - `RL`: right-to-left

    Possible `line_shape`
        - `basis`
        - `bumpX`: used in LR or RL direction
        - `bumpY`
        - `cardinal`: undirected
        - `catmullRom`: undirected
        - `linear`:
        - `monotoneX`: used in LR or RL direction
        - `monotoneY`
        - `natural`
        - `step`: used in LR or RL direction
        - `stepAfter`
        - `stepBefore`: used in LR or RL direction

    Possible `node_shape`
        - `rounded_edge`: rectangular with rounded edges
        - `stadium`: (_) shape, rectangular with rounded ends
        - `subroutine`: ||_|| shape, rectangular with additional line at the ends
        - `cylindrical`: database node
        - `circle`: circular
        - `asymmetric`: >_| shape
        - `rhombus`: decision node
        - `hexagon`: <_> shape
        - `parallelogram`: /_/ shape
        - `parallelogram_alt`: \\_\\ shape, inverted parallelogram
        - `trapezoid`: /_\\ shape
        - `trapezoid_alt`: \\_/ shape, inverted trapezoid
        - `double_circle`

    Possible `edge_arrow`
        - `normal`: directed arrow, shaded arrowhead
        - `bold`: bold directed arrow
        - `dotted`: dotted directed arrow
        - `open`: line, undirected arrow
        - `bold_open`: bold line
        - `dotted_open`: dotted line
        - `invisible`: no line
        - `circle`: directed arrow with filled circle arrowhead
        - `cross`: directed arrow with cross arrowhead
        - `double_normal`: bidirectional directed arrow
        - `double_circle`: bidirectional directed arrow with filled circle arrowhead
        - `double_cross`: bidirectional directed arrow with cross arrowhead

    Refer to mermaid `documentation`_ for more information.
    Paste the output into any markdown file renderer to view the flowchart, alternatively visit the
    mermaid playground `here`_.

    .. note:: Advanced mermaid flowchart functionalities such as subgraphs and interactions (script, click) are not supported.

    .. _documentation: http://mermaid.js.org/syntax/flowchart.html
    .. _here: https://mermaid.live/

    >>> from bigtree import tree_to_mermaid
    >>> root = Node("a", node_shape="rhombus")
    >>> b = Node("b", edge_arrow="bold", edge_label="Child 1", parent=root)
    >>> c = Node("c", edge_arrow="dotted", edge_label="Child 2", parent=root)
    >>> d = Node("d", node_style="fill:yellow, stroke:black", parent=b)
    >>> e = Node("e", parent=b)
    >>> graph = tree_to_mermaid(root)
    >>> print(graph)
    ```mermaid
    %%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
    flowchart TB
    0("a") --> 0-0("b")
    0-0 --> 0-0-0("d")
    0-0 --> 0-0-1("e")
    0("a") --> 0-1("c")
    classDef default stroke-width:1
    ```

    **Customize node shape, edge label, edge arrow, and custom node attributes**

    >>> graph = tree_to_mermaid(root, node_shape_attr="node_shape", edge_label="edge_label", edge_arrow_attr="edge_arrow", node_attr="node_style")
    >>> print(graph)
    ```mermaid
    %%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
    flowchart TB
    0{"a"} ==>|Child 1| 0-0("b")
    0-0:::class0-0-0 --> 0-0-0("d")
    0-0 --> 0-0-1("e")
    0{"a"} -.->|Child 2| 0-1("c")
    classDef default stroke-width:1
    classDef class0-0-0 fill:yellow, stroke:black
    ```

    Args:
        tree (Node): tree to be exported
        title (str): title, defaults to None
        rankdir (str): layout direction, defaults to 'TB' (top to bottom), can be 'BT' (bottom to top),
            'LR' (left to right), 'RL' (right to left)
        line_shape (str): line shape or curvature, defaults to 'basis'
        node_colour (str): fill colour of nodes, can be colour name or hexcode, defaults to None
        node_border_colour (str): border colour of nodes, can be colour name or hexcode, defaults to None
        node_border_width (float): width of node border, defaults to 1
        node_shape (str): node shape, sets the shape of every node, defaults to 'rounded_edge'
        node_shape_attr (str | Callable): If string type, it refers to ``Node`` attribute for node shape.
            If callable type, it takes in the node itself and returns the node shape.
            This sets the shape of custom nodes, and overrides default `node_shape`, defaults to None
        edge_arrow (str): edge arrow style from parent to itself, sets the arrow style of every edge, defaults to 'normal'
        edge_arrow_attr (str | Callable): If string type, it refers to ``Node`` attribute for edge arrow style.
            If callable type, it takes in the node itself and returns the edge arrow style.
            This sets the edge arrow style of custom nodes from parent to itself, and overrides default `edge_arrow`, defaults to None
        edge_label (str): ``Node`` attribute for edge label from parent to itself, defaults to None
        node_attr (str | Callable): If string type, it refers to ``Node`` attribute for node style.
            If callable type, it takes in the node itself and returns the node style.
            This overrides `node_colour`, `node_border_colour`, and `node_border_width`, defaults to None

    Returns:
        (str)
    """
    from bigtree.tree.helper import clone_tree

    rankdirs = MermaidConstants.RANK_DIR
    line_shapes = MermaidConstants.LINE_SHAPES
    node_shapes = MermaidConstants.NODE_SHAPES
    edge_arrows = MermaidConstants.EDGE_ARROWS

    # Assertions
    assert_str_in_list("rankdir", rankdir, rankdirs)
    assert_key_in_dict("node_shape", node_shape, node_shapes)
    assert_str_in_list("line_shape", line_shape, line_shapes)
    assert_key_in_dict("edge_arrow", edge_arrow, edge_arrows)

    mermaid_template = """```mermaid\n{title}{line_style}\nflowchart {rankdir}\n{flows}\n{styles}\n```"""
    flowchart_template = "{from_node_ref}{from_node_name}{flow_style} {arrow}{arrow_label} {to_node_ref}{to_node_name}"
    style_template = "classDef {style_name} {style}"

    # Content
    title = f"---\ntitle: {title}\n---" if title else ""
    line_style = f"%%{{ init: {{ 'flowchart': {{ 'curve': '{line_shape}' }} }} }}%%"
    styles = []
    flows = []

    def _construct_style(
        _style_name: str,
        _node_colour: str,
        _node_border_colour: str,
        _node_border_width: float,
    ) -> str:
        style = []
        if _node_colour:
            style.append(f"fill:{_node_colour}")
        if _node_border_colour:
            style.append(f"stroke:{_node_border_colour}")
        if _node_border_width:
            style.append(f"stroke-width:{_node_border_width}")
        if not style:
            raise ValueError("Unable to construct style!")
        return style_template.format(style_name=_style_name, style=",".join(style))

    default_style = _construct_style(
        "default", node_colour, node_border_colour, node_border_width
    )
    styles.append(default_style)

    class MermaidNode(Node):
        @property
        def mermaid_name(self) -> str:
            """Reference name for MermaidNode, must be unique for each node

            Returns:
                (str)
            """
            if self.is_root:
                return "0"
            return f"{self.parent.mermaid_name}-{self.parent.children.index(self)}"

    def get_attr(
        _node: MermaidNode,
        attr_parameter: str | Callable[[MermaidNode], str],
        default_parameter: str,
    ) -> str:
        """Get custom attribute if available, otherwise return default parameter

        Args:
            _node (MermaidNode): node to get custom attribute, can be accessed as node attribute or a callable that takes in the node
            attr_parameter (str | Callable): custom attribute parameter
            default_parameter (str): default parameter if there is no attr_parameter

        Returns:
            (str)
        """
        _choice = default_parameter
        if attr_parameter:
            if isinstance(attr_parameter, str):
                _choice = _node.get_attr(attr_parameter, default_parameter)
            else:
                _choice = attr_parameter(_node)
        return _choice

    tree_mermaid = clone_tree(tree, MermaidNode)
    for _, _, node in yield_tree(tree_mermaid, **kwargs):
        if not node.is_root:
            # Get custom style (node_shape_attr)
            _parent_node_name = ""
            if node.parent.is_root:
                _parent_node_shape_choice = get_attr(
                    node.parent, node_shape_attr, node_shape  # type: ignore
                )
                _parent_node_shape = node_shapes[_parent_node_shape_choice]
                _parent_node_name = _parent_node_shape.format(label=node.parent.name)
            _node_shape_choice = get_attr(node, node_shape_attr, node_shape)  # type: ignore
            _node_shape = node_shapes[_node_shape_choice]
            _node_name = _node_shape.format(label=node.name)

            # Get custom style (edge_arrow_attr, edge_label)
            _arrow_choice = get_attr(node, edge_arrow_attr, edge_arrow)  # type: ignore
            _arrow = edge_arrows[_arrow_choice]
            _arrow_label = (
                f"|{node.get_attr(edge_label)}|" if node.get_attr(edge_label) else ""
            )

            # Get custom style (node_attr)
            _flow_style = get_attr(node, node_attr, "")  # type: ignore
            if _flow_style:
                _flow_style_class = f"""class{node.get_attr("mermaid_name")}"""
                styles.append(
                    style_template.format(
                        style_name=_flow_style_class, style=_flow_style
                    )
                )
                _flow_style = f":::{_flow_style_class}"

            flows.append(
                flowchart_template.format(
                    from_node_ref=node.parent.get_attr("mermaid_name"),
                    from_node_name=_parent_node_name,
                    flow_style=_flow_style,
                    arrow=_arrow,
                    arrow_label=_arrow_label,
                    to_node_ref=node.get_attr("mermaid_name"),
                    to_node_name=_node_name,
                )
            )

    return mermaid_template.format(
        title=title,
        line_style=line_style,
        rankdir=rankdir,
        flows="\n".join(flows),
        styles="\n".join(styles),
    )
