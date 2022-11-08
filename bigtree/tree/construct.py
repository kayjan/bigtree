from collections import OrderedDict
from typing import List, Tuple, Type

import numpy as np
import pandas as pd

from bigtree.node.node import Node
from bigtree.tree.export import tree_to_dataframe
from bigtree.tree.search import find_children, find_name
from bigtree.utils.exceptions import DuplicatedNodeError, TreeError

__all__ = [
    "add_path_to_tree",
    "add_dict_to_tree_by_path",
    "add_dict_to_tree_by_name",
    "add_dataframe_to_tree_by_path",
    "add_dataframe_to_tree_by_name",
    "list_to_tree_tuples",
    "list_to_tree",
    "dict_to_tree",
    "nested_dict_to_tree",
    "dataframe_to_tree",
]


def add_path_to_tree(
    tree: Node,
    path: str,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_attrs: dict = {},
) -> Node:
    """Add nodes and attributes to existing tree *in-place*, return node of added path.
    Adds to existing tree from list of path strings.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path` and can be different from that of existing tree.

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import add_path_to_tree, print_tree
    >>> root = Node("a")
    >>> add_path_to_tree(root, "a/b/c")
    Node(/a/b/c, )
    >>> print_tree(root)
    a
    `-- b
        `-- c

    Args:
        tree (Node): existing tree
        path (str): path to be added to tree
        sep (str): path separator for input `path`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True
        node_attrs (dict): attributes to add to node, key: attribute name, value: attribute value, optional

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
            f"Error: Path does not have same root node, expected {tree_root.node_name}, received {branch[0]}\n"
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
            node = find_children(parent_node, node_name)
        if not node:
            node = node_type(branch[idx])
            node.parent = parent_node
        parent_node = node
    node.set_attrs(node_attrs)
    return node


def add_dict_to_tree_by_path(
    tree: Node,
    path_attrs: dict,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> Node:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    Adds to existing tree from nested dictionary, ``key``: path, ``value``: dict of attribute name and attribute value.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path` and can be different from that of existing tree.

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import Node, add_dict_to_tree_by_path, print_tree
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
    >>> print_tree(root)
    a
    |-- b
    |   |-- d
    |   `-- e
    |       |-- g
    |       `-- h
    `-- c
        `-- f

    Args:
        tree (Node): existing tree
        path_attrs (dict): dictioning containing node path and attribute information,
            key: node path, value: dict of node attribute name and attribute value
        sep (str): path separator for input `path_attrs`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True

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


def add_dict_to_tree_by_name(
    tree: Node, path_attrs: dict, join_type: str = "left"
) -> Node:
    """Add nodes and attributes to tree, return *new* root of tree.
    Adds to existing tree from nested dictionary, ``key``: name, ``value``: dict of attribute name and attribute value.

    Function can return all existing tree nodes or only tree nodes that are in the input dictionary keys.
    Input dictionary keys that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing same name.

    >>> from bigtree import Node, add_dict_to_tree_by_name, print_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> name_dict = {
    ...     "a": {"age": 90},
    ...     "b": {"age": 65},
    ... }
    >>> root = add_dict_to_tree_by_name(root, name_dict)
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    `-- b [age=65]

    Args:
        tree (Node): existing tree
        path_attrs (dict): dictioning containing node name and attribute information,
            key: node name, value: dict of node attribute name and attribute value
        join_type (str): join type with attribute, default of 'left' takes existing tree nodes,
            if join_type is set to 'inner' it will only take tree nodes that are in `path_attrs` key and drop others

    Returns:
        (Node)
    """
    if join_type not in ["inner", "left"]:
        raise ValueError("`join_type` must be one of 'inner' or 'left'")

    if not len(path_attrs):
        raise ValueError("Dictionary does not contain any data, check `path_attrs`")

    # Convert dictionary to dataframe
    data = pd.DataFrame(path_attrs).T.rename_axis("NAME").reset_index()
    return add_dataframe_to_tree_by_name(tree, data=data, join_type=join_type)


def add_dataframe_to_tree_by_path(
    tree: Node,
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: list = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> Node:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`

    Path in path column should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").
      - Path separator `sep` is for the input `path_col` and can be different from that of existing tree.

    Path in path column can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> import pandas as pd
    >>> from bigtree import add_dataframe_to_tree_by_path, print_tree
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
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    |-- b [age=65]
    |   |-- d [age=40]
    |   `-- e [age=35]
    |       |-- g [age=10]
    |       `-- h [age=6]
    `-- c [age=60]
        `-- f [age=38]

    Args:
        tree (Node): existing tree
        data (pandas.DataFrame): data containing node path and attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (list): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator for input `path_col`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True

    Returns:
        (Node)
    """
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
        node_attrs = {k: v for k, v in node_attrs.items() if not np.all(pd.isnull(v))}
        add_path_to_tree(
            tree_root,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return tree_root


def add_dataframe_to_tree_by_name(
    tree: Node,
    data: pd.DataFrame,
    name_col: str = "",
    attribute_cols: list = [],
    join_type: str = "left",
):
    """Add nodes and attributes to tree, return *new* root of tree.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree.
    If columns are not specified, the first column will be taken as name column and all other columns as attributes.

    Function can return all existing tree nodes or only tree nodes that are in the input data node names.
    Input data node names that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing same name.

    >>> import pandas as pd
    >>> from bigtree import add_dataframe_to_tree_by_name, print_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> name_data = pd.DataFrame([
    ...     ["a", 90],
    ...     ["b", 65],
    ... ],
    ...     columns=["NAME", "age"]
    ... )
    >>> root = add_dataframe_to_tree_by_name(root, name_data)
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    `-- b [age=65]

    Args:
        tree (Node): existing tree
        data (pandas.DataFrame): data containing node name and attribute information
        name_col (str): column of data containing `name` information,
            if not set, it will take the first column of data
        attribute_cols (list): column(s) of data containing node attribute information,
            if not set, it will take all columns of data except path_col
        join_type (str): join type with attribute, default of 'left' takes existing tree nodes,
            if join_type is set to 'inner' it will only take tree nodes with attributes and drop the other nodes

    Returns:
        (Node)
    """
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


def list_to_tree_tuples(
    relations: List[Tuple[str, str]],
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from list of tuple containing parent-child names.

    >>> from bigtree import list_to_tree_tuples, print_tree
    >>> relations_list = [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "f"), ("e", "g"), ("e", "h")]
    >>> root = list_to_tree_tuples(relations_list)
    >>> print_tree(root)
    a
    |-- b
    |   |-- d
    |   `-- e
    |       |-- g
    |       `-- h
    `-- c
        `-- f

    Args:
        relations (list): list containing tuple containing parent-child names
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not len(relations):
        raise ValueError("Path list does not contain any data, check `relations`")

    node_dict = {}
    for parent_name, child_name in relations:
        if not node_dict.get(child_name):
            node_dict[child_name] = node_type(child_name)
        child_node = node_dict[child_name]

        if parent_name:
            if not node_dict.get(parent_name):
                node_dict[parent_name] = node_type(parent_name)
            parent_node = node_dict[parent_name]
            child_node.parent = parent_node
    root = child_node.root
    return root


def list_to_tree(
    paths: list,
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

    >>> from bigtree import list_to_tree, print_tree
    >>> path_list = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    |-- b
    |   |-- d
    |   `-- e
    |       |-- g
    |       `-- h
    `-- c
        `-- f

    Args:
        paths (list): list containing path strings
        sep (str): path separator for input `paths` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
    if not len(paths):
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


def dict_to_tree(
    path_attrs: dict,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from nested dictionary, ``key``: path, ``value``: dict of attribute name and attribute value.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Path can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> from bigtree import dict_to_tree, print_tree
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
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    |-- b [age=65]
    |   |-- d [age=40]
    |   `-- e [age=35]
    |       |-- g [age=10]
    |       `-- h [age=6]
    `-- c [age=60]
        `-- f [age=38]

    Args:
        path_attrs (dict): dictioning containing path and node attribute information,
            key: path, value: dict of tree attribute and attribute value
        sep (str): path separator of input `path_attrs` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True
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
    node_attrs: dict,
    name_key: str = "name",
    child_key: str = "children",
    sep: str = "/",
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from nested recursive dictionary.
      - ``key``: `name_key`, `child_key`, or any attributes.
      - ``value`` of `name_key` (str): node name.
      - ``value`` of `child_key` (list): list of dict containing `name_key` and `child_key` (recursive).

    >>> from bigtree import nested_dict_to_tree, print_tree
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
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    `-- b [age=65]
        |-- d [age=40]
        `-- e [age=35]
            `-- g [age=10]

    Args:
        node_attrs (dict): dictioning containing node, children, and node attribute information,
            key: `name_key` and `child_key`
            value of `name_key` (str): node name
            value of `child_key` (list): list of dict containing `name_key` and `child_key` (recursive)
        name_key (str): key of node name, value is type str
        child_key (str): key of child list, value is type list
        sep (str): path separator of created tree, defaults to `/`
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """

    def recursive_add_child(child_dict, parent_node=None):
        child_dict = child_dict.copy()
        node_name = child_dict.pop(name_key)
        node_children = child_dict.pop(child_key, [])
        node = node_type(node_name, parent=parent_node, **child_dict)
        for _child in node_children:
            recursive_add_child(_child, parent_node=node)
        return node

    root_node = recursive_add_child(node_attrs)
    root_node.sep = sep
    return root_node


def dataframe_to_tree(
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: list = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[Node] = Node,
) -> Node:
    """Construct tree from pandas DataFrame, return root of tree.
    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`.

    Path in path column can start from root node `name`, or start with `sep`.
      - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    Path in path column should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    All paths should start from the same root node.
      - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    >>> import pandas as pd
    >>> from bigtree import dataframe_to_tree, print_tree
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
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    |-- b [age=65]
    |   |-- d [age=40]
    |   `-- e [age=35]
    |       |-- g [age=10]
    |       `-- h [age=6]
    `-- c [age=60]
        `-- f [age=38]

    Args:
        data (pandas.DataFrame): data containing path and node attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (list): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator of input `path_col` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicated `Node` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to Node

    Returns:
        (Node)
    """
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
    root_node = node_type(root_name)
    add_dataframe_to_tree_by_path(
        root_node,
        data,
        sep=sep,
        duplicate_name_allowed=duplicate_name_allowed,
    )
    root_node.sep = sep
    return root_node
