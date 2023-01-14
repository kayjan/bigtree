import collections
from typing import Any, Dict, List, Tuple, Union

import pandas as pd

from bigtree.node.node import Node
from bigtree.tree.search import find_path
from bigtree.utils.iterators import preorder_iter

__all__ = [
    "print_tree",
    "yield_tree",
    "tree_to_dict",
    "tree_to_nested_dict",
    "tree_to_dataframe",
    "tree_to_dot",
    "tree_to_pillow",
]


available_styles = {
    "ansi": ("|   ", "|-- ", "`-- "),
    "ascii": ("|   ", "|-- ", "+-- "),
    "const": ("\u2502   ", "\u251c\u2500\u2500 ", "\u2514\u2500\u2500 "),
    "const_bold": ("\u2503   ", "\u2523\u2501\u2501 ", "\u2517\u2501\u2501 "),
    "rounded": ("\u2502   ", "\u251c\u2500\u2500 ", "\u2570\u2500\u2500 "),
    "double": ("\u2551   ", "\u2560\u2550\u2550 ", "\u255a\u2550\u2550 "),
    "custom": ("", "", ""),
}


def print_tree(
    tree: Node,
    node_name_or_path: str = "",
    max_depth: int = None,
    attr_list: List[str] = None,
    all_attrs: bool = False,
    attr_omit_null: bool = True,
    attr_bracket: List[str] = ["[", "]"],
    style: str = "const",
    custom_style: List[str] = [],
):
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
        attr_list (list): list of node attributes to print, optional
        all_attrs (bool): indicator to show all attributes, overrides `attr_list`
        attr_omit_null (bool): indicator whether to omit showing of null attributes, defaults to True
        attr_bracket (List[str]): open and close bracket for `all_attrs` or `attr_list`
        style (str): style of print, defaults to abstract style
        custom_style (List[str]): style of stem, branch and final stem, used when `style` is set to 'custom'
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
                    ]
            attr_str = ", ".join(attr_str_list)
            if attr_str:
                attr_str = f" {attr_bracket_open}{attr_str}{attr_bracket_close}"
        node_str = f"{_node.node_name}{attr_str}"
        print(f"{pre_str}{fill_str}{node_str}")


def yield_tree(
    tree: Node,
    node_name_or_path: str = "",
    max_depth: int = None,
    style: str = "const",
    custom_style: List[str] = [],
):
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
        custom_style (List[str]): style of stem, branch and final stem, used when `style` is set to 'custom'
    """
    if style not in available_styles.keys():
        raise ValueError(
            f"Choose one of {available_styles.keys()} style, use `custom` to define own style"
        )

    tree = tree.copy()
    if node_name_or_path:
        tree = find_path(tree, node_name_or_path)
    if not tree.is_root:
        tree.parent = None

    # Set style
    if style == "custom":
        if len(custom_style) != 3:
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
    tree: Node,
    name_key: str = "name",
    parent_key: str = "",
    attr_dict: dict = {},
    all_attrs: bool = False,
    max_depth: int = None,
    skip_depth: int = None,
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
        attr_dict (dict): dictionary mapping node attributes to dictionary key,
            key: node attributes, value: corresponding dictionary key, optional
        all_attrs (bool): indicator whether to retrieve all `Node` attributes
        max_depth (int): maximum depth to export tree, optional
        skip_depth (int): number of initial depth to skip, optional
        leaf_only (bool): indicator to retrieve only information from leaf nodes

    Returns:
        (dict)
    """
    tree = tree.copy()
    data_dict = {}

    def recursive_append(node):
        if node:
            if (
                (not max_depth or node.depth <= max_depth)
                and (not skip_depth or node.depth > skip_depth)
                and (not leaf_only or node.is_leaf)
            ):
                data_child = {}
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
    tree: Node,
    name_key: str = "name",
    child_key: str = "children",
    attr_dict: dict = {},
    all_attrs: bool = False,
    max_depth: int = None,
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
        attr_dict (dict): dictionary mapping node attributes to dictionary key,
            key: node attributes, value: corresponding dictionary key, optional
        all_attrs (bool): indicator whether to retrieve all `Node` attributes
        max_depth (int): maximum depth to export tree, optional

    Returns:
        (dict)
    """
    tree = tree.copy()
    data_dict = {}

    def recursive_append(node, parent_dict):
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


def tree_to_dataframe(
    tree: Node,
    path_col: str = "path",
    name_col: str = "name",
    parent_col: str = "",
    attr_dict: dict = {},
    all_attrs: bool = False,
    max_depth: int = None,
    skip_depth: int = None,
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
        path_col (str): column name for `node.path_name`, optional
        name_col (str): column name for `node.node_name`, defaults to 'name'
        parent_col (str): column name for `node.parent.node_name`, optional
        attr_dict (dict): dictionary mapping node attributes to column name,
            key: node attributes, value: corresponding column in dataframe, optional
        all_attrs (bool): indicator whether to retrieve all `Node` attributes
        max_depth (int): maximum depth to export tree, optional
        skip_depth (int): number of initial depth to skip, optional
        leaf_only (bool): indicator to retrieve only information from leaf nodes

    Returns:
        (pd.DataFrame)
    """
    tree = tree.copy()
    data_list = []

    def recursive_append(node):
        if node:
            if (
                (not max_depth or node.depth <= max_depth)
                and (not skip_depth or node.depth > skip_depth)
                and (not leaf_only or node.is_leaf)
            ):
                data_child = {}
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


def tree_to_dot(
    tree: Union[Node, List[Node]],
    directed: bool = True,
    rankdir: str = "TB",
    bg_colour: str = None,
    node_colour: str = None,
    edge_colour: str = None,
    node_attr: str = None,
    edge_attr: str = None,
):
    r"""Export tree or list of trees to image.
    Posible node attributes include style, fillcolor, shape.

    >>> from bigtree import Node, tree_to_dot
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=b)
    >>> e = Node("e", age=35, parent=b)
    >>> graph = tree_to_dot(root)

    Export to image, dot file, etc.

    >>> graph.write_png("tree.png")
    >>> graph.write_dot("tree.dot")

    Export to string

    >>> graph.to_string()
    'strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\nc0 [label=c];\na0 -> c0;\n}\n'

    Defining node and edge attributes

    >>> class CustomNode(Node):
    ...     def __init__(self, name, node_shape="", edge_label="", **kwargs):
    ...         super().__init__(name, **kwargs)
    ...         self.node_shape = node_shape
    ...         self.edge_label = edge_label
    ...
    ...     @property
    ...     def edge_attr(self):
    ...         return {"label": self.edge_label}
    ...
    ...     @property
    ...     def node_attr(self):
    ...         return {"shape": self.node_shape}
    >>>
    >>>
    >>> root = CustomNode("a", node_shape="circle")
    >>> b = CustomNode("b", node_shape="diamond", edge_label="child", parent=root)
    >>> c = CustomNode("c", node_shape="diamond", edge_label="child", parent=root)
    >>> d = CustomNode("d", node_shape="square", edge_label="child", parent=b)
    >>> e = CustomNode("e", node_shape="square", edge_label="child", parent=b)
    >>> graph = tree_to_dot(root, node_colour="gold", node_attr="node_attr", edge_attr="edge_attr")
    >>> graph.write_png("assets/custom_tree.png")

    .. image:: https://github.com/kayjan/bigtree/raw/master/assets/custom_tree.png

    Args:
        tree (Node/List[Node]): tree or list of trees to be exported
        directed (bool): indicator whether graph should be directed or undirected, defaults to True
        rankdir (str): set direction of graph layout, defaults to 'TB' (top to bottom), can be 'BT' (bottom to top),
            'LR' (left to right), 'RL' (right to left)
        bg_colour (str): background color of image, defaults to None
        node_colour (str): fill colour of nodes, defaults to None
        edge_colour (str): colour of edges, defaults to None
        node_attr (str): `Node` attribute for node style, overrides node_colour, defaults to None.
            Possible node style (attribute value) include {"style": "filled", "fillcolor": "gold", "shape": "diamond"}
        edge_attr (str): `Node` attribute for edge style, overrides edge_colour, defaults to None.
            Possible edge style (attribute value) include {"style": "bold", "label": "edge label", "color": "black"}

    Returns:
        (pydot.Dot)
    """
    try:
        import pydot
    except ImportError:  # pragma: no cover
        raise ImportError(
            "pydot not available. Please perform a\n\npip install 'bigtree[image]'\n\nto install required dependencies"
        )

    # Get style
    if bg_colour:
        graph_style = dict(bgcolor=bg_colour)
    else:
        graph_style = dict()

    if node_colour:
        node_style = dict(style="filled", fillcolor=node_colour)
    else:
        node_style = dict()

    if edge_colour:
        edge_style = dict(color=edge_colour)
    else:
        edge_style = dict()

    tree = tree.copy()

    if directed:
        _graph = pydot.Dot(
            graph_type="digraph", strict=True, rankdir=rankdir, **graph_style
        )
    else:
        _graph = pydot.Dot(
            graph_type="graph", strict=True, rankdir=rankdir, **graph_style
        )

    if not isinstance(tree, list):
        tree = [tree]

    for _tree in tree:
        if not isinstance(_tree, Node):
            raise ValueError("Tree should be of type `Node`, or inherit from `Node`")

        name_dict = collections.defaultdict(list)

        def recursive_create_node_and_edges(parent_name, child_node):
            _node_style = node_style.copy()
            _edge_style = edge_style.copy()

            child_label = child_node.node_name
            if child_node.path_name not in name_dict[child_label]:  # pragma: no cover
                name_dict[child_label].append(child_node.path_name)
            child_name = child_label + str(
                name_dict[child_label].index(child_node.path_name)
            )
            if node_attr and child_node.get_attr(node_attr):
                _node_style.update(child_node.get_attr(node_attr))
            if edge_attr:
                _edge_style.update(child_node.get_attr(edge_attr))
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


def tree_to_pillow(
    tree: Node,
    width: int = 0,
    height: int = 0,
    start_pos: Tuple[float, float] = (10, 10),
    font_family: str = "assets/DejaVuSans.ttf",
    font_size: int = 12,
    font_colour: Union[Tuple[float, float, float], str] = "black",
    bg_colour: Union[Tuple[float, float, float], str] = "white",
    **kwargs,
):
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
        start_pos (Tuple[float, float]): start position of text, (x-offset, y-offset), defaults to (10, 10)
        font_family (str): file path of font family, requires .ttf file, defaults to DejaVuSans
        font_size (int): font size, defaults to 12
        font_colour (Union[List[int], str]): font colour, accepts tuple of RGB values or string, defaults to black
        bg_colour (Union[List[int], str]): background of image, accepts tuple of RGB values or string, defaults to white

    Returns:
        (PIL.Image.Image)
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:  # pragma: no cover
        raise ImportError(
            "Pillow not available. Please perform a\n\npip install 'bigtree[image]'\n\nto install required dependencies"
        )

    # Initialize font
    font = ImageFont.truetype(font_family, font_size)

    # Initialize text
    image_text = []
    for branch, stem, node in yield_tree(tree, **kwargs):
        image_text.append(f"{branch}{stem}{node.node_name}\n")

    # Calculate image dimension from text, otherwise override with argument
    def get_list_of_text_dimensions(text_list):
        """Get list dimensions

        Args:
            text_list (List[str]): list of texts

        Returns:
            (List[Iterable[int]]): list of (left, top, right, bottom) bounding box
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
    image_text = "".join(image_text)
    width = max(width, text_width + 2 * start_pos[0])
    height = max(height, text_height + 2 * start_pos[1])

    # Initialize and draw image
    image = Image.new("RGB", (width, height), bg_colour)
    image_draw = ImageDraw.Draw(image)
    image_draw.text(start_pos, image_text, font=font, fill=font_colour)
    return image
