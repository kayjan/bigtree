import collections
from typing import Any, Dict, List

import pandas as pd

from bigtree.node.node import Node
from bigtree.tree.search import find_name
from bigtree.utils.iterators import preorder_iter

__all__ = [
    "print_tree",
    "yield_tree",
    "tree_to_dict",
    "tree_to_nested_dict",
    "tree_to_dataframe",
    "tree_to_dot",
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
    node_name: str = "",
    max_depth: int = None,
    all_attrs: bool = False,
    attr_list: List[str] = None,
    attr_bracket_open: str = "[",
    attr_bracket_close: str = "]",
    style: str = "ansi",
    style_stem: str = "",
    style_branch: str = "",
    style_stem_final: str = "",
):
    """Print tree to console, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to choose which attributes to show or show all attributes, using `attr_name_filter` and `all_attrs`
    - Able to customize open and close brackets if attributes are shown
    - Able to customize style, to choose from `ansi`, `ascii`, `const`, `rounded`, `double`, and `custom` style
        - Default style is `ansi` style
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
    |-- b
    |   |-- d
    |   `-- e
    `-- c

    **Printing Sub-tree**

    >>> print_tree(root, node_name="b")
    b
    |-- d
    `-- e

    >>> print_tree(root, max_depth=2)
    a
    |-- b
    `-- c

    **Printing Attributes**

    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    |-- b [age=65]
    |   |-- d [age=40]
    |   `-- e [age=35]
    `-- c [age=60]

    >>> print_tree(root, attr_list=["age"], attr_bracket_open="*(", attr_bracket_close=")")
    a *(age=90)
    |-- b *(age=65)
    |   |-- d *(age=40)
    |   `-- e *(age=35)
    `-- c *(age=60)

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
        node_name (str): node to print from, becomes the root node of printing
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        all_attrs (bool): indicator to show all attributes, overrides `attr_list`
        attr_list (list): list of node attributes to print, optional
        attr_bracket_open (str): open bracket for `attr_list`
        attr_bracket_close (str): close bracket for `attr_list`
        style (str): style of print, defaults to abstract style
        style_stem (str): style of stem, used when `style` is set to 'custom'
        style_branch (str): style of branch, used when `style` is set to 'custom'
        style_stem_final (str): style of final stem, used when `style` is set to 'custom'
    """
    for pre_str, fill_str, _node in yield_tree(
        tree=tree,
        node_name=node_name,
        max_depth=max_depth,
        style=style,
        style_stem=style_stem,
        style_branch=style_branch,
        style_stem_final=style_stem_final,
    ):
        # Get node_str (node name and attributes)
        attr_str = ""
        if all_attrs:
            attrs = _node.describe(exclude_attributes=["name"], exclude_prefix="_")
            if len(attrs):
                attr_str = ", ".join([f"{k}={v}" for k, v in attrs])
                attr_str = f" {attr_bracket_open}{attr_str}{attr_bracket_close}"
        elif attr_list:
            attr_str = ", ".join(
                [f"{attr_name}={_node.get_attr(attr_name)}" for attr_name in attr_list]
            )
            attr_str = f" {attr_bracket_open}{attr_str}{attr_bracket_close}"
        node_str = f"{_node.node_name}{attr_str}"
        print(f"{pre_str}{fill_str}{node_str}")


def yield_tree(
    tree: Node,
    node_name: str = "",
    max_depth: int = None,
    style: str = "ansi",
    style_stem: str = "",
    style_branch: str = "",
    style_stem_final: str = "",
):
    """Generator method for customizing printing of tree, starting from `tree`.

    - Able to select which node to print from, resulting in a subtree, using `node_name`
    - Able to customize for maximum depth to print, using `max_depth`
    - Able to customize style, to choose from `ansi`, `ascii`, `const`, `rounded`, `double`, and `custom` style
        - Default style is `ansi` style
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
    |-- b
    |   |-- d
    |   `-- e
    `-- c

    **Printing Sub-tree**

    >>> for branch, stem, node in yield_tree(root, node_name="b"):
    ...     print(f"{branch}{stem}{node.node_name}")
    b
    |-- d
    `-- e

    >>> for branch, stem, node in yield_tree(root, max_depth=2):
    ...     print(f"{branch}{stem}{node.node_name}")
    a
    |-- b
    `-- c

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
        node_name (str): node to print from, becomes the root node of printing, optional
        max_depth (int): maximum depth of tree to print, based on `depth` attribute, optional
        style (str): style of print, defaults to abstract style
        style_stem (str): style of stem, used when `style` is set to 'custom'
        style_branch (str): style of branch, used when `style` is set to 'custom'
        style_stem_final (str): style of final stem, used when `style` is set to 'custom'
    """
    if style not in available_styles.keys():
        raise ValueError(
            f"Choose one of {available_styles.keys()} style, use `custom` to define own style"
        )

    tree = tree.copy()
    if node_name:
        tree = find_name(tree, node_name)
    tree.parent = None

    # Set style
    if style != "custom":
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
                    dict(node.describe(exclude_attributes=["name"], exclude_prefix="_"))
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
        if not max_depth or node.depth <= max_depth:
            data_child = {name_key: node.node_name}
            if all_attrs:
                data_child.update(
                    dict(node.describe(exclude_attributes=["name"], exclude_prefix="_"))
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
    tree: Node,
    directed: bool = True,
    rankdir: str = "TB",
    bgcolor: str = None,
    node_colour: str = None,
    edge_colour: str = None,
    node_attr: str = None,
):
    r"""Export tree to image.
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

    Args:
        tree (Node): tree to be exported
        directed (bool): indicator whether graph should be directed or undirected, defaults to True
        rankdir (str): set direction of graph layout, defaults to 'TB', can be 'BT, 'LR', 'RL'
        bgcolor (str): background color of image, defaults to None
        node_colour (str): fill colour of nodes, defaults to None
        edge_colour (str): colour of edges, defaults to None
        node_attr (str): node attribute for style, overrides node_colour, defaults to None

    Returns:
        (pydot.Dot)
    """
    try:
        import pydot
    except ImportError:  # pragma: no cover
        raise ImportError(
            "pydot not available. Please perform a\n\npip install 'bigtree[image]'\n\nto install required dependencies"
        )

    if not isinstance(tree, Node):
        raise ValueError("Tree should be of type `Node`, or inherit from `Node`")

    # Get style
    if bgcolor:
        graph_style = dict(bgcolor=bgcolor)
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

    name_dict = collections.defaultdict(list)

    def recursive_create_node_and_edges(parent_name, child_node):
        child_label = child_node.node_name
        if child_node.path_name not in name_dict[child_label]:  # pragma: no cover
            name_dict[child_label].append(child_node.path_name)
        child_name = child_label + str(
            name_dict[child_label].index(child_node.path_name)
        )
        if node_attr and child_node.get_attr(node_attr):
            node_style.update(child_node.get_attr(node_attr))
        node = pydot.Node(name=child_name, label=child_label, **node_style)
        _graph.add_node(node)
        if parent_name is not None:
            edge = pydot.Edge(parent_name, child_name, **edge_style)
            _graph.add_edge(edge)
        for child in child_node.children:
            recursive_create_node_and_edges(child_name, child)

    recursive_create_node_and_edges(None, tree.root)
    return _graph
