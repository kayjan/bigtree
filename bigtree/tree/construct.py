from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

from bigtree.node.node import Node
from bigtree.tree.export import tree_to_dataframe
from bigtree.tree.search import find_child_by_name, find_name
from bigtree.utils.exceptions import (
    DuplicatedNodeError,
    TreeError,
    optional_dependencies_pandas,
)

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

__all__ = [
    "add_path_to_tree",
    "add_dict_to_tree_by_path",
    "add_dict_to_tree_by_name",
    "add_dataframe_to_tree_by_path",
    "add_dataframe_to_tree_by_name",
    "str_to_tree",
    "list_to_tree",
    "list_to_tree_by_relation",
    "dict_to_tree",
    "nested_dict_to_tree",
    "dataframe_to_tree",
    "dataframe_to_tree_by_relation",
]


def add_path_to_tree(
    tree: Node,
    path: str,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_attrs: Dict[str, Any] = {},
) -> Node:
    """Add nodes and attributes to existing tree *in-place*, return node of added path.
    Adds to existing tree from list of path strings.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc., and should not start with another root node.

    >>> from bigtree import add_path_to_tree
    >>> root = Node("a")
    >>> add_path_to_tree(root, "a/b/c")
    Node(/a/b/c, )
    >>> root.show()
    a
    └── b
        └── c

    Args:
        tree (Node): existing tree
        path (str): path to be added to tree
        sep (str): path separator for input `path`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True
        node_attrs (Dict[str, Any]): attributes to add to node, key: attribute name, value: attribute value, optional

    Returns:
        (Node)
    """
    if not len(path):
        raise ValueError("Path is empty, check `path`")

    tree_root = tree.root
    tree_sep = tree_root.sep
    node_type = tree_root.__class__
    branch = path.lstrip(sep).rstrip(sep).split(sep)
    if branch[0] != tree_root.node_name:
        raise TreeError(
            f"Path does not have same root node, expected {tree_root.node_name}, received {branch[0]}\n"
            f"Check your input paths or verify that path separator `sep` is set correctly"
        )

    # Grow tree
    node = tree_root
    parent_node = tree_root
    for idx in range(1, len(branch)):
        node_name = branch[idx]
        node_path = tree_sep.join(branch[: idx + 1])
        if not duplicate_name_allowed:
            node = find_name(tree_root, node_name)
            if node and not node.path_name.endswith(node_path):
                raise DuplicatedNodeError(
                    f"Node {node_name} already exists, try setting `duplicate_name_allowed` to True "
                    f"to allow `Node` with same node name"
                )
        else:
            node = find_child_by_name(parent_node, node_name)
        if not node:
            if idx == len(branch) - 1:
                node_name = node_attrs.pop("name", branch[idx])
                node = node_type(node_name, **node_attrs)
            else:
                node = node_type(branch[idx])
            node.parent = parent_node
        parent_node = node
    node.set_attrs(node_attrs)
    return node


def add_dict_to_tree_by_path(
    tree: Node,
    path_attrs: Dict[str, Dict[str, Any]],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> Node:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    Adds to existing tree from nested dictionary, ``key``: path, ``value``: dict of attribute name and attribute value.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import Node, add_dict_to_tree_by_path
    >>> root = Node("a")
    >>> path_dict = {
    ...     "a": {"age": 90},
    ...     "a/b": {"age": 65},
    ...     "a/c": {"age": 60},
    ...     "a/b/d": {"age": 40},
    ...     "a/b/e": {"age": 35},
    ...     "a/c/f": {"age": 38},
    ...     "a/b/e/g": {"age": 10},
    ...     "a/b/e/h": {"age": 6},
    ... }
    >>> root = add_dict_to_tree_by_path(root, path_dict)
    >>> root.show()
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    Args:
        tree (Node): existing tree
        path_attrs (Dict[str, Dict[str, Any]]): dictionary containing node path and attribute information,
            key: node path, value: dict of node attribute name and attribute value
        sep (str): path separator for input `path_attrs`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True

    Returns:
        (Node)
    """
    if not len(path_attrs):
        raise ValueError("Dictionary does not contain any data, check `path_attrs`")

    tree_root = tree.root

    for k, v in path_attrs.items():
        add_path_to_tree(
            tree_root,
            k,
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=v,
        )
    return tree_root


@optional_dependencies_pandas
def add_dict_to_tree_by_name(
    tree: Node, name_attrs: Dict[str, Dict[str, Any]], join_type: str = "left"
) -> Node:
    """Add attributes to tree, return *new* root of tree.
    Adds to existing tree from nested dictionary, ``key``: name, ``value``: dict of attribute name and attribute value.

    Function can return all existing tree nodes or only tree nodes that are in the input dictionary keys depending on join type.
    Input dictionary keys that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing the same name.

    >>> from bigtree import Node, add_dict_to_tree_by_name
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> name_dict = {
    ...     "a": {"age": 90},
    ...     "b": {"age": 65},
    ... }
    >>> root = add_dict_to_tree_by_name(root, name_dict)
    >>> root.show(attr_list=["age"])
    a [age=90]
    └── b [age=65]

    Args:
        tree (Node): existing tree
        name_attrs (Dict[str, Dict[str, Any]]): dictionary containing node name and attribute information,
            key: node name, value: dict of node attribute name and attribute value
        join_type (str): join type with attribute, default of 'left' takes existing tree nodes,
            if join_type is set to 'inner' it will only take tree nodes that are in `path_attrs` key and drop others

    Returns:
        (Node)
    """
    if join_type not in ["inner", "left"]:
        raise ValueError("`join_type` must be one of 'inner' or 'left'")

    if not len(name_attrs):
        raise ValueError("Dictionary does not contain any data, check `name_attrs`")

    # Convert dictionary to dataframe
    data = pd.DataFrame(name_attrs).T.rename_axis("NAME").reset_index()
    return add_dataframe_to_tree_by_name(tree, data=data, join_type=join_type)


def add_dataframe_to_tree_by_path(
    tree: Node,
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> Node:
    """Add nodes and attributes to tree *in-place*, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`

    Path in path column should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path in path column can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> import pandas as pd
    >>> from bigtree import add_dataframe_to_tree_by_path
    >>> root = Node("a")
    >>> path_data = pd.DataFrame([
    ...     ["a", 90],
    ...     ["a/b", 65],
    ...     ["a/c", 60],
    ...     ["a/b/d", 40],
    ...     ["a/b/e", 35],
    ...     ["a/c/f", 38],
    ...     ["a/b/e/g", 10],
    ...     ["a/b/e/h", 6],
    ... ],
    ...     columns=["PATH", "age"]
    ... )
    >>> root = add_dataframe_to_tree_by_path(root, path_data)
    >>> root.show(attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   ├── d [age=40]
    │   └── e [age=35]
    │       ├── g [age=10]
    │       └── h [age=6]
    └── c [age=60]
        └── f [age=38]

    Args:
        tree (Node): existing tree
        data (pd.DataFrame): data containing node path and attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator for input `path_col`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True

    Returns:
        (Node)
    """
    data = data.copy()

    if not len(data.columns):
        raise ValueError("Data does not contain any columns, check `data`")
    if not len(data):
        raise ValueError("Data does not contain any rows, check `data`")

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    tree_root = tree.root
    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    data2 = data.copy()[[path_col] + attribute_cols].astype(str).drop_duplicates()
    _duplicate_check = (
        data2[path_col]
        .value_counts()
        .to_frame("counts")
        .rename_axis(path_col)
        .reset_index()
    )
    _duplicate_check = _duplicate_check[_duplicate_check["counts"] > 1]
    if len(_duplicate_check):
        raise ValueError(
            f"There exists duplicate path with different attributes\nCheck {_duplicate_check}"
        )

    for row in data.to_dict(orient="index").values():
        node_attrs = row.copy()
        del node_attrs[path_col]
        node_attrs = {k: v for k, v in node_attrs.items() if v is not None}
        add_path_to_tree(
            tree_root,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return tree_root


@optional_dependencies_pandas
def add_dataframe_to_tree_by_name(
    tree: Node,
    data: pd.DataFrame,
    name_col: str = "",
    attribute_cols: List[str] = [],
    join_type: str = "left",
) -> Node:
    """Add attributes to tree, return *new* root of tree.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree.
    If columns are not specified, the first column will be taken as name column and all other columns as attributes.

    Function can return all existing tree nodes or only tree nodes that are in the input data node names.
    Input data node names that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing same name.

    >>> import pandas as pd
    >>> from bigtree import add_dataframe_to_tree_by_name
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> name_data = pd.DataFrame([
    ...     ["a", 90],
    ...     ["b", 65],
    ... ],
    ...     columns=["NAME", "age"]
    ... )
    >>> root = add_dataframe_to_tree_by_name(root, name_data)
    >>> root.show(attr_list=["age"])
    a [age=90]
    └── b [age=65]

    Args:
        tree (Node): existing tree
        data (pd.DataFrame): data containing node name and attribute information
        name_col (str): column of data containing `name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): column(s) of data containing node attribute information,
            if not set, it will take all columns of data except path_col
        join_type (str): join type with attribute, default of 'left' takes existing tree nodes,
            if join_type is set to 'inner' it will only take tree nodes with attributes and drop the other nodes

    Returns:
        (Node)
    """
    data = data.copy()

    if join_type not in ["inner", "left"]:
        raise ValueError("`join_type` must be one of 'inner' or 'left'")

    if not len(data.columns):
        raise ValueError("Data does not contain any columns, check `data`")
    if not len(data):
        raise ValueError("Data does not contain any rows, check `data`")

    if not name_col:
        name_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(name_col)

    # Attribute data
    path_col = "PATH"
    data2 = data.copy()[[name_col] + attribute_cols].astype(str).drop_duplicates()
    _duplicate_check = (
        data2[name_col]
        .value_counts()
        .to_frame("counts")
        .rename_axis(name_col)
        .reset_index()
    )
    _duplicate_check = _duplicate_check[_duplicate_check["counts"] > 1]
    if len(_duplicate_check):
        raise ValueError(
            f"There exists duplicate name with different attributes\nCheck {_duplicate_check}"
        )

    # Tree data
    tree_root = tree.root
    sep = tree_root.sep
    node_type = tree_root.__class__
    data_tree = tree_to_dataframe(
        tree_root, name_col=name_col, path_col=path_col, all_attrs=True
    )
    common_cols = list(set(data_tree.columns).intersection(attribute_cols))
    data_tree = data_tree.drop(columns=common_cols)

    # Attribute data
    data_tree_attrs = pd.merge(data_tree, data, on=name_col, how=join_type)
    data_tree_attrs = data_tree_attrs.drop(columns=name_col)

    return dataframe_to_tree(
        data_tree_attrs, path_col=path_col, sep=sep, node_type=node_type
    )


def str_to_tree(
    tree_string: str,
    tree_prefix_list: List[str] = [],
    node_type: Type[Node] = Node,
) -> Node:
    r"""Construct tree from tree string

    >>> from bigtree import str_to_tree
    >>> tree_str = 'a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f'
    >>> root = str_to_tree(tree_str, tree_prefix_list=["├──", "└──"])
    >>> root.show()
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    Args:
        tree_string (str): String to construct tree
        tree_prefix_list (List[str]): List of prefix to mark the end of tree branch/stem and start of node name, optional.
            If not specified, it will infer unicode characters and whitespace as prefix.
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    tree_string = tree_string.strip("\n")
    if not len(tree_string):
        raise ValueError("Tree string does not contain any data, check `tree_string`")
    tree_list = tree_string.split("\n")
    tree_root = node_type(tree_list[0])

    # Infer prefix length
    prefix_length = None
    cur_parent = tree_root
    for node_str in tree_list[1:]:
        if len(tree_prefix_list):
            node_name = re.split("|".join(tree_prefix_list), node_str)[-1].lstrip()
        else:
            node_name = node_str.encode("ascii", "ignore").decode("ascii").lstrip()

        # Find node parent
        if not prefix_length:
            prefix_length = node_str.index(node_name)
            if not prefix_length:
                raise ValueError(
                    f"Invalid prefix, prefix should be unicode character or whitespace, "
                    f"otherwise specify one or more prefixes in `tree_prefix_list`, check: {node_str}"
                )
        node_prefix_length = node_str.index(node_name)
        if node_prefix_length % prefix_length:
            raise ValueError(
                f"Tree string have different prefix length, check branch: {node_str}"
            )
        while cur_parent.depth > node_prefix_length / prefix_length:
            cur_parent = cur_parent.parent

        # Link node
        child_node = node_type(node_name)
        child_node.parent = cur_parent
        cur_parent = child_node

    return tree_root


def list_to_tree(
    paths: Iterable[str],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from list of path strings.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import list_to_tree
    >>> path_list = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
    >>> root = list_to_tree(path_list)
    >>> root.show()
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    Args:
        paths (Iterable[str]): list containing path strings
        sep (str): path separator for input `paths` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not paths:
        raise ValueError("Path list does not contain any data, check `paths`")

    # Remove duplicates
    paths = list(OrderedDict.fromkeys(paths))

    # Construct root node
    root_name = paths[0].lstrip(sep).split(sep)[0]
    root_node = node_type(root_name)
    root_node.sep = sep

    for path in paths:
        add_path_to_tree(
            root_node, path, sep=sep, duplicate_name_allowed=duplicate_name_allowed
        )
    root_node.sep = sep
    return root_node


@optional_dependencies_pandas
def list_to_tree_by_relation(
    relations: Iterable[Tuple[str, str]],
    allow_duplicates: bool = False,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from list of tuple containing parent-child names.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated.
    Error will be thrown if names of intermediate nodes are repeated as there will be confusion.
    This error can be ignored by setting `allow_duplicates` to be True.

    >>> from bigtree import list_to_tree_by_relation
    >>> relations_list = [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "f"), ("e", "g"), ("e", "h")]
    >>> root = list_to_tree_by_relation(relations_list)
    >>> root.show()
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    Args:
        relations (Iterable[Tuple[str, str]]): list containing tuple containing parent-child names
        allow_duplicates (bool): allow duplicate intermediate nodes such that child node will
            be tagged to multiple parent nodes, defaults to False
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not relations:
        raise ValueError("Path list does not contain any data, check `relations`")

    relation_data = pd.DataFrame(relations, columns=["parent", "child"])
    return dataframe_to_tree_by_relation(
        relation_data,
        child_col="child",
        parent_col="parent",
        allow_duplicates=allow_duplicates,
        node_type=node_type,
    )


@optional_dependencies_pandas
def dict_to_tree(
    path_attrs: Dict[str, Any],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from nested dictionary using path,
    ``key``: path, ``value``: dict of attribute name and attribute value.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import dict_to_tree
    >>> path_dict = {
    ...     "a": {"age": 90},
    ...     "a/b": {"age": 65},
    ...     "a/c": {"age": 60},
    ...     "a/b/d": {"age": 40},
    ...     "a/b/e": {"age": 35},
    ...     "a/c/f": {"age": 38},
    ...     "a/b/e/g": {"age": 10},
    ...     "a/b/e/h": {"age": 6},
    ... }
    >>> root = dict_to_tree(path_dict)
    >>> root.show(attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   ├── d [age=40]
    │   └── e [age=35]
    │       ├── g [age=10]
    │       └── h [age=6]
    └── c [age=60]
        └── f [age=38]

    Args:
        path_attrs (Dict[str, Any]): dictionary containing path and node attribute information,
            key: path, value: dict of tree attribute and attribute value
        sep (str): path separator of input `path_attrs` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not len(path_attrs):
        raise ValueError("Dictionary does not contain any data, check `path_attrs`")

    # Convert dictionary to dataframe
    data = pd.DataFrame(path_attrs).T.rename_axis("PATH").reset_index()
    return dataframe_to_tree(
        data,
        sep=sep,
        duplicate_name_allowed=duplicate_name_allowed,
        node_type=node_type,
    )


def nested_dict_to_tree(
    node_attrs: Dict[str, Any],
    name_key: str = "name",
    child_key: str = "children",
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from nested recursive dictionary.
      - ``key``: `name_key`, `child_key`, or any attributes key.
      - ``value`` of `name_key` (str): node name.
      - ``value`` of `child_key` (List[Dict[str, Any]]): list of dict containing `name_key` and `child_key` (recursive).

    >>> from bigtree import nested_dict_to_tree
    >>> path_dict = {
    ...     "name": "a",
    ...     "age": 90,
    ...     "children": [
    ...         {"name": "b",
    ...          "age": 65,
    ...          "children": [
    ...              {"name": "d", "age": 40},
    ...              {"name": "e", "age": 35, "children": [
    ...                  {"name": "g", "age": 10},
    ...              ]},
    ...          ]},
    ...     ],
    ... }
    >>> root = nested_dict_to_tree(path_dict)
    >>> root.show(attr_list=["age"])
    a [age=90]
    └── b [age=65]
        ├── d [age=40]
        └── e [age=35]
            └── g [age=10]

    Args:
        node_attrs (Dict[str, Any]): dictionary containing node, children, and node attribute information,
            key: `name_key` and `child_key`
            value of `name_key` (str): node name
            value of `child_key` (List[Dict[str, Any]]): list of dict containing `name_key` and `child_key` (recursive)
        name_key (str): key of node name, value is type str
        child_key (str): key of child list, value is type list
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not node_attrs:
        raise ValueError("Dictionary does not contain any data, check `node_attrs`")

    def recursive_add_child(
        child_dict: Dict[str, Any], parent_node: Optional[Node] = None
    ) -> Node:
        child_dict = child_dict.copy()
        node_name = child_dict.pop(name_key)
        node_children = child_dict.pop(child_key, [])
        if not isinstance(node_children, List):
            raise TypeError(
                f"child_key {child_key} should be List type, received {node_children}"
            )
        node = node_type(node_name, parent=parent_node, **child_dict)
        for _child in node_children:
            recursive_add_child(_child, parent_node=node)
        return node

    root_node = recursive_add_child(node_attrs)
    return root_node


def dataframe_to_tree(
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from pandas DataFrame using path, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`.

    Path in path column can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    Path in path column should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> import pandas as pd
    >>> from bigtree import dataframe_to_tree
    >>> path_data = pd.DataFrame([
    ...     ["a", 90],
    ...     ["a/b", 65],
    ...     ["a/c", 60],
    ...     ["a/b/d", 40],
    ...     ["a/b/e", 35],
    ...     ["a/c/f", 38],
    ...     ["a/b/e/g", 10],
    ...     ["a/b/e/h", 6],
    ... ],
    ...     columns=["PATH", "age"]
    ... )
    >>> root = dataframe_to_tree(path_data)
    >>> root.show(attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   ├── d [age=40]
    │   └── e [age=35]
    │       ├── g [age=10]
    │       └── h [age=6]
    └── c [age=60]
        └── f [age=38]

    Args:
        data (pd.DataFrame): data containing path and node attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator of input `path_col` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicate `Node` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    data = data.copy()

    if not len(data.columns):
        raise ValueError("Data does not contain any columns, check `data`")
    if not len(data):
        raise ValueError("Data does not contain any rows, check `data`")

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    data2 = data.copy()[[path_col] + attribute_cols].astype(str).drop_duplicates()
    _duplicate_check = (
        data2[path_col]
        .value_counts()
        .to_frame("counts")
        .rename_axis(path_col)
        .reset_index()
    )
    _duplicate_check = _duplicate_check[_duplicate_check["counts"] > 1]
    if len(_duplicate_check):
        raise ValueError(
            f"There exists duplicate path with different attributes\nCheck {_duplicate_check}"
        )

    root_name = data[path_col].values[0].split(sep)[0]
    root_node_data = data[data[path_col] == root_name]
    if len(root_node_data):
        root_node_kwargs = list(
            root_node_data[attribute_cols].to_dict(orient="index").values()
        )[0]
        root_name = root_node_kwargs.pop("name", root_name)
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)
    add_dataframe_to_tree_by_path(
        root_node,
        data,
        path_col=path_col,
        attribute_cols=attribute_cols,
        sep=sep,
        duplicate_name_allowed=duplicate_name_allowed,
    )
    root_node.sep = sep
    return root_node


def dataframe_to_tree_by_relation(
    data: pd.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    allow_duplicates: bool = False,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from pandas DataFrame using parent and child names, return root of tree.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated.
    Error will be thrown if names of intermediate nodes are repeated as there will be confusion.
    This error can be ignored by setting `allow_duplicates` to be True.

    `child_col` and `parent_col` specify columns for child name and parent name to construct tree.
    `attribute_cols` specify columns for node attribute for child name
    If columns are not specified, `child_col` takes first column, `parent_col` takes second column, and all other
    columns are `attribute_cols`.

    >>> import pandas as pd
    >>> from bigtree import dataframe_to_tree_by_relation
    >>> relation_data = pd.DataFrame([
    ...     ["a", None, 90],
    ...     ["b", "a", 65],
    ...     ["c", "a", 60],
    ...     ["d", "b", 40],
    ...     ["e", "b", 35],
    ...     ["f", "c", 38],
    ...     ["g", "e", 10],
    ...     ["h", "e", 6],
    ... ],
    ...     columns=["child", "parent", "age"]
    ... )
    >>> root = dataframe_to_tree_by_relation(relation_data)
    >>> root.show(attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   ├── d [age=40]
    │   └── e [age=35]
    │       ├── g [age=10]
    │       └── h [age=6]
    └── c [age=60]
        └── f [age=38]

    Args:
        data (pd.DataFrame): data containing path and node attribute information
        child_col (str): column of data containing child name information, defaults to None
            if not set, it will take the first column of data
        parent_col (str): column of data containing parent name information, defaults to None
            if not set, it will take the second column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `child_col` and `parent_col`
        allow_duplicates (bool): allow duplicate intermediate nodes such that child node will
            be tagged to multiple parent nodes, defaults to False
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    data = data.copy()

    if not len(data.columns):
        raise ValueError("Data does not contain any columns, check `data`")
    if not len(data):
        raise ValueError("Data does not contain any rows, check `data`")

    if not child_col:
        child_col = data.columns[0]
    if not parent_col:
        parent_col = data.columns[1]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)

    data_check = data.copy()[[child_col, parent_col]].drop_duplicates()
    # Filter for child nodes that are parent of other nodes
    if not allow_duplicates:
        data_check = data_check[data_check[child_col].isin(data_check[parent_col])]
        _duplicate_check = (
            data_check[child_col]
            .value_counts()
            .to_frame("counts")
            .rename_axis(child_col)
            .reset_index()
        )
        _duplicate_check = _duplicate_check[_duplicate_check["counts"] > 1]
        if len(_duplicate_check):
            raise ValueError(
                f"There exists duplicate child with different parent where the child is also a parent node.\n"
                f"Duplicated node names should not happen, but can only exist in leaf nodes to avoid confusion.\n"
                f"Check {_duplicate_check}"
            )

    # If parent-child contains None -> root
    root_row = data[data[parent_col].isnull()]
    root_names = list(root_row[child_col])
    if not len(root_names):
        root_names = list(set(data[parent_col]) - set(data[child_col]))
    if len(root_names) != 1:
        raise ValueError(
            f"Unable to determine root node\nPossible root nodes: {root_names}"
        )
    root_name = root_names[0]
    root_node_data = data[data[child_col] == root_name]
    if len(root_node_data):
        root_node_kwargs = list(
            root_node_data[attribute_cols].to_dict(orient="index").values()
        )[0]
        root_name = root_node_kwargs.pop("name", root_name)
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)

    def retrieve_attr(_row: Dict[str, Any]) -> Dict[str, Any]:
        node_attrs = _row.copy()
        node_attrs["name"] = node_attrs[child_col]
        del node_attrs[child_col]
        del node_attrs[parent_col]
        _node_attrs = {k: v for k, v in node_attrs.items() if v is not None}
        return _node_attrs

    def recursive_create_child(parent_node: Node) -> None:
        child_rows = data[data[parent_col] == parent_node.node_name]

        for row in child_rows.to_dict(orient="index").values():
            child_node = node_type(**retrieve_attr(row))
            child_node.parent = parent_node
            recursive_create_child(child_node)

    # Create root node attributes
    if len(root_row):
        row = list(root_row.to_dict(orient="index").values())[0]
        root_node.set_attrs(retrieve_attr(row))
    recursive_create_child(root_node)
    return root_node
