from __future__ import annotations

import re
from collections import OrderedDict, defaultdict
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

from bigtree.node.node import Node
from bigtree.tree.search import find_child_by_name, find_name
from bigtree.utils.assertions import (
    assert_dataframe_no_duplicate_attribute,
    assert_dataframe_no_duplicate_children,
    assert_dataframe_not_empty,
    assert_length_not_empty,
    filter_attributes,
    isnull,
)
from bigtree.utils.constants import NewickCharacter, NewickState
from bigtree.utils.exceptions import (
    DuplicatedNodeError,
    TreeError,
    optional_dependencies_pandas,
)

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

try:
    import polars as pl
except ImportError:  # pragma: no cover
    pl = None

__all__ = [
    "add_path_to_tree",
    "add_dict_to_tree_by_path",
    "add_dict_to_tree_by_name",
    "add_dataframe_to_tree_by_path",
    "add_dataframe_to_tree_by_name",
    "add_polars_to_tree_by_path",
    "add_polars_to_tree_by_name",
    "str_to_tree",
    "list_to_tree",
    "list_to_tree_by_relation",
    "dict_to_tree",
    "nested_dict_to_tree",
    "dataframe_to_tree",
    "dataframe_to_tree_by_relation",
    "polars_to_tree",
    "polars_to_tree_by_relation",
    "newick_to_tree",
]

T = TypeVar("T", bound=Node)


def add_path_to_tree(
    tree: T,
    path: str,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_attrs: Dict[str, Any] = {},
) -> T:
    """Add nodes and attributes to existing tree *in-place*, return node of path added.
    Adds to existing tree from list of path strings.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").
    - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc., and should not start with another root node.

    All attributes in `node_attrs` will be added to the tree, including attributes with null values.

    Examples:
        >>> from bigtree import add_path_to_tree, Node
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
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True
        node_attrs (Dict[str, Any]): attributes to add to node, key: attribute name, value: attribute value, optional

    Returns:
        (Node)
    """
    assert_length_not_empty(path, "Path", "path")

    root_node = tree.root
    tree_sep = root_node.sep
    node_type = root_node.__class__
    branch = path.lstrip(sep).rstrip(sep).split(sep)
    if branch[0] != root_node.node_name:
        raise TreeError(
            f"Path does not have same root node, expected {root_node.node_name}, received {branch[0]}\n"
            f"Check your input paths or verify that path separator `sep` is set correctly"
        )

    # Grow tree
    node = root_node
    parent_node = root_node
    for idx in range(1, len(branch)):
        node_name = branch[idx]
        node_path = tree_sep.join(branch[: idx + 1])
        if not duplicate_name_allowed:
            node = find_name(root_node, node_name)
            if node and not node.path_name.endswith(node_path):
                raise DuplicatedNodeError(
                    f"Node {node_name} already exists, try setting `duplicate_name_allowed` to True "
                    f"to allow `Node` with same node name"
                )
        else:
            node = find_child_by_name(parent_node, node_name)
        if not node:
            if idx == len(branch) - 1:
                node = node_type(node_name, **node_attrs)
            else:
                node = node_type(node_name)
            node.parent = parent_node
        parent_node = node
    node.set_attrs(node_attrs)
    return node


def add_dict_to_tree_by_path(
    tree: T,
    path_attrs: Dict[str, Dict[str, Any]],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    Adds to existing tree from nested dictionary, ``key``: path, ``value``: dict of attribute name and attribute value.

    All attributes in `path_attrs` will be added to the tree, including attributes with null values.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").
    - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
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
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True

    Returns:
        (Node)
    """
    assert_length_not_empty(path_attrs, "Dictionary", "path_attrs")

    root_node = tree.root

    for path, node_attrs in path_attrs.items():
        add_path_to_tree(
            root_node,
            path,
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_dict_to_tree_by_name(tree: T, name_attrs: Dict[str, Dict[str, Any]]) -> T:
    """Add attributes to existing tree *in-place*.
    Adds to existing tree from nested dictionary, ``key``: name, ``value``: dict of attribute name and attribute value.

    All attributes in `name_attrs` will be added to the tree, including attributes with null values.

    Input dictionary keys that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing the same name.

    Examples:
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

    Returns:
        (Node)
    """
    from bigtree.tree.search import findall

    assert_length_not_empty(name_attrs, "Dictionary", "name_attrs")

    attr_dict_names = set(name_attrs.keys())

    for node in findall(tree, lambda _node: _node.node_name in attr_dict_names):
        node_attrs = filter_attributes(
            name_attrs[node.node_name], omit_keys=["name"], omit_null_values=False
        )
        node.set_attrs(node_attrs)

    return tree


def add_dataframe_to_tree_by_path(
    tree: T,
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    Adds to existing tree from pandas DataFrame.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").
    - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
        >>> import pandas as pd
        >>> from bigtree import add_dataframe_to_tree_by_path, Node
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
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols].copy()
    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    assert_dataframe_no_duplicate_attribute(data, "path", path_col, attribute_cols)

    root_node = tree.root
    for row in data.to_dict(orient="index").values():
        node_attrs = filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_dataframe_to_tree_by_name(
    tree: T,
    data: pd.DataFrame,
    name_col: str = "",
    attribute_cols: List[str] = [],
) -> T:
    """Add attributes to existing tree *in-place*.
    Adds to existing tree from pandas DataFrame.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree.
    If columns are not specified, the first column will be taken as name column and all other columns as attributes.

    Input data node names that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing same name.

    Examples:
        >>> import pandas as pd
        >>> from bigtree import add_dataframe_to_tree_by_name, Node
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
            if not set, it will take all columns of data except `path_col`

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not name_col:
        name_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(name_col)

    assert_dataframe_no_duplicate_attribute(data, "name", name_col, attribute_cols)

    # Get attribute dict, remove null attributes
    name_attrs = (
        data.drop_duplicates(name_col)
        .set_index(name_col)[attribute_cols]
        .to_dict(orient="index")
    )
    name_attrs = {
        k1: {k2: v2 for k2, v2 in v1.items() if not isnull(v2)}
        for k1, v1 in name_attrs.items()
    }

    return add_dict_to_tree_by_name(tree, name_attrs)


def add_polars_to_tree_by_path(
    tree: T,
    data: pl.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree.
    Adds to existing tree from polars DataFrame.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").
    - Path separator `sep` is for the input `path` and can differ from existing tree.

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
        >>> import polars as pl
        >>> from bigtree import add_polars_to_tree_by_path, Node
        >>> root = Node("a")
        >>> path_data = pl.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     schema=["PATH", "age"]
        ... )
        >>> root = add_polars_to_tree_by_path(root, path_data)
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
        data (pl.DataFrame): data containing node path and attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator for input `path_col`
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols]
    data = data.with_columns(
        [data[path_col].str.strip_chars_start(sep).str.strip_chars_end(sep)]
    )
    assert_dataframe_no_duplicate_attribute(data, "path", path_col, attribute_cols)

    root_node = tree.root
    for row_kwargs in data.to_dicts():
        node_attrs = filter_attributes(
            row_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row_kwargs[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_polars_to_tree_by_name(
    tree: T,
    data: pl.DataFrame,
    name_col: str = "",
    attribute_cols: List[str] = [],
) -> T:
    """Add attributes to existing tree *in-place*.
    Adds to existing tree from polars DataFrame.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree.
    If columns are not specified, the first column will be taken as name column and all other columns as attributes.

    Input data node names that are not existing node names will be ignored.
    Note that if multiple nodes have the same name, attributes will be added to all nodes sharing same name.

    Examples:
        >>> import polars as pl
        >>> from bigtree import add_polars_to_tree_by_name, Node
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> name_data = pl.DataFrame([
        ...     ["a", 90],
        ...     ["b", 65],
        ... ],
        ...     schema=["NAME", "age"]
        ... )
        >>> root = add_polars_to_tree_by_name(root, name_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]

    Args:
        tree (Node): existing tree
        data (pl.DataFrame): data containing node name and attribute information
        name_col (str): column of data containing `name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): column(s) of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not name_col:
        name_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(name_col)

    assert_dataframe_no_duplicate_attribute(data, "name", name_col, attribute_cols)

    # Get attribute dict, remove null attributes
    name_attrs = dict(
        data.unique(subset=[name_col])
        .select([name_col] + attribute_cols)
        .rows_by_key(key=name_col, named=True)
    )
    name_attrs = {
        k1: {k2: v2 for k2, v2 in v1[0].items() if not isnull(v2)}
        for k1, v1 in name_attrs.items()
    }

    return add_dict_to_tree_by_name(tree, name_attrs)


def str_to_tree(
    tree_string: str,
    tree_prefix_list: List[str] = [],
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    r"""Construct tree from tree string

    Examples:
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
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    tree_string = tree_string.strip("\n")
    assert_length_not_empty(tree_string, "Tree string", "tree_string")
    tree_list = tree_string.split("\n")
    root_node = node_type(tree_list[0])

    # Infer prefix length
    prefix_length = None
    cur_parent = root_node
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

    return root_node


def list_to_tree(
    paths: List[str],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from list of path strings.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
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
        paths (List[str]): list containing path strings
        sep (str): path separator for input `paths` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_length_not_empty(paths, "Path list", "paths")

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
    return root_node


@optional_dependencies_pandas
def list_to_tree_by_relation(
    relations: List[Tuple[str, str]],
    allow_duplicates: bool = False,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from list of tuple containing parent-child names.

    Root node is inferred when parent is empty, or when name appears as parent but not as child.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated.
    Error will be thrown if names of intermediate nodes are repeated as there will be confusion.
    This error can be ignored by setting `allow_duplicates` to be True.

    Examples:
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
        relations (List[Tuple[str, str]]): list containing tuple containing parent-child names
        allow_duplicates (bool): allow duplicate intermediate nodes such that child node will
            be tagged to multiple parent nodes, defaults to False
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_length_not_empty(relations, "Path list", "relations")

    relation_data = pd.DataFrame(relations, columns=["parent", "child"])
    return dataframe_to_tree_by_relation(
        relation_data,
        child_col="child",
        parent_col="parent",
        allow_duplicates=allow_duplicates,
        node_type=node_type,
    )


def dict_to_tree(
    path_attrs: Dict[str, Any],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from nested dictionary using path,
    ``key``: path, ``value``: dict of attribute name and attribute value.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    All attributes in `path_attrs` will be added to the tree, including attributes with null values.

    Examples:
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
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_length_not_empty(path_attrs, "Dictionary", "path_attrs")

    # Initial tree
    root_name = list(path_attrs.keys())[0].lstrip(sep).rstrip(sep).split(sep)[0]
    root_node_attrs = dict(
        path_attrs.get(root_name, {})
        or path_attrs.get(sep + root_name, {})
        or path_attrs.get(root_name + sep, {})
        or path_attrs.get(sep + root_name + sep, {})
    )
    root_node_attrs = filter_attributes(
        root_node_attrs, omit_keys=["name"], omit_null_values=False
    )
    root_node = node_type(
        name=root_name,
        sep=sep,
        **root_node_attrs,
    )

    # Convert dictionary to dataframe
    for node_path, node_attrs in path_attrs.items():
        node_attrs = filter_attributes(
            node_attrs, omit_keys=["name"], omit_null_values=False
        )
        add_path_to_tree(
            root_node,
            node_path,
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def nested_dict_to_tree(
    node_attrs: Dict[str, Any],
    name_key: str = "name",
    child_key: str = "children",
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from nested recursive dictionary.

    - ``key``: `name_key`, `child_key`, or any attributes key.
    - ``value`` of `name_key` (str): node name.
    - ``value`` of `child_key` (List[Dict[str, Any]]): list of dict containing `name_key` and `child_key` (recursive).

    Examples:
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
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_length_not_empty(node_attrs, "Dictionary", "node_attrs")

    def _recursive_add_child(
        child_dict: Dict[str, Any], parent_node: Optional[T] = None
    ) -> T:
        """Recursively add child to tree, given child attributes and parent node.

        Args:
            child_dict (Dict[str, Any]): child to be added to tree, from dictionary
            parent_node (Node): parent node to be assigned to child node, defaults to None

        Returns:
            (Node)
        """
        child_dict = child_dict.copy()
        node_name = child_dict.pop(name_key)
        node_children = child_dict.pop(child_key, [])
        if not isinstance(node_children, List):
            raise TypeError(
                f"child_key {child_key} should be List type, received {node_children}"
            )
        node = node_type(node_name, parent=parent_node, **child_dict)
        for _child in node_children:
            _recursive_add_child(_child, parent_node=node)
        return node

    root_node = _recursive_add_child(node_attrs)
    return root_node


def dataframe_to_tree(
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from pandas DataFrame using path, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
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
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols].copy()
    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    assert_dataframe_no_duplicate_attribute(data, "path", path_col, attribute_cols)

    root_name = data[path_col].values[0].split(sep)[0]
    root_node_data = data[data[path_col] == root_name]
    if len(root_node_data):
        root_node_kwargs = list(
            root_node_data[attribute_cols].to_dict(orient="index").values()
        )[0]
        root_node_kwargs = filter_attributes(
            root_node_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)

    for row in data.to_dict(orient="index").values():
        node_attrs = filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    root_node.sep = sep
    return root_node


def dataframe_to_tree_by_relation(
    data: pd.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    allow_duplicates: bool = False,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from pandas DataFrame using parent and child names, return root of tree.

    Root node is inferred when parent name is empty, or when name appears in parent column but not in child column.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated.
    Error will be thrown if names of intermediate nodes are repeated as there will be confusion.
    This error can be ignored by setting `allow_duplicates` to be True.

    `child_col` and `parent_col` specify columns for child name and parent name to construct tree.
    `attribute_cols` specify columns for node attribute for child name.
    If columns are not specified, `child_col` takes first column, `parent_col` takes second column, and all other
    columns are `attribute_cols`.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    Examples:
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
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not child_col:
        child_col = data.columns[0]
    if not parent_col:
        parent_col = data.columns[1]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)

    data = data[[child_col, parent_col] + attribute_cols].copy()
    if not allow_duplicates:
        assert_dataframe_no_duplicate_children(data, child_col, parent_col)

    # Infer root node
    root_names = set(data[data[parent_col].isnull()][child_col])
    root_names.update(set(data[parent_col]) - set(data[child_col]) - {None})
    if len(root_names) != 1:
        raise ValueError(
            f"Unable to determine root node\n"
            f"Possible root nodes: {sorted(list(root_names), key=lambda v: (isinstance(v, str), v))}"
        )
    root_name = list(root_names)[0]

    def _retrieve_attr(_row: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve node attributes from dictionary, remove parent and child column from dictionary.

        Args:
            _row (Dict[str, Any]): node attributes

        Returns:
            (Dict[str, Any])
        """
        node_attrs = filter_attributes(
            _row, omit_keys=[child_col, parent_col], omit_null_values=True
        )
        node_attrs["name"] = _row[child_col]
        return node_attrs

    def _recursive_add_child(parent_node: T) -> None:
        """Recursive add child to tree, given current node.

        Args:
            parent_node (Node): parent node
        """
        child_rows = data[data[parent_col] == parent_node.node_name]

        for row in child_rows.to_dict(orient="index").values():
            child_node = node_type(**_retrieve_attr(row))
            child_node.parent = parent_node
            _recursive_add_child(child_node)

    # Create root node attributes
    root_row = data[data[child_col] == root_name]
    if len(root_row):
        row = list(root_row.to_dict(orient="index").values())[0]
        root_node = node_type(**_retrieve_attr(row))
    else:
        root_node = node_type(root_name)
    _recursive_add_child(root_node)
    return root_node


def polars_to_tree(
    data: pl.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from polars DataFrame using path, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree.
    If columns are not specified, `path_col` takes first column and all other columns are `attribute_cols`.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/".

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node.

    Examples:
        >>> import polars as pl
        >>> from bigtree import polars_to_tree
        >>> path_data = pl.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     schema=["PATH", "age"]
        ... )
        >>> root = polars_to_tree(path_data)
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
        data (pl.DataFrame): data containing path and node attribute information
        path_col (str): column of data containing `path_name` information,
            if not set, it will take the first column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `path_col`
        sep (str): path separator of input `path_col` and created tree, defaults to `/`
        duplicate_name_allowed (bool): indicator if nodes with duplicate ``Node`` name is allowed, defaults to True
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols]
    data = data.with_columns(
        [data[path_col].str.strip_chars_start(sep).str.strip_chars_end(sep)]
    )
    assert_dataframe_no_duplicate_attribute(data, "path", path_col, attribute_cols)

    root_name = data[path_col][0].split(sep)[0]
    root_node_data = data.filter(data[path_col] == root_name)
    if len(root_node_data):
        root_node_kwargs_list = root_node_data[attribute_cols].to_dicts()
        root_node_kwargs = root_node_kwargs_list[0] if root_node_kwargs_list else {}
        root_node_kwargs = filter_attributes(
            root_node_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)

    for row in data.to_dicts():
        node_attrs = filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    root_node.sep = sep
    return root_node


def polars_to_tree_by_relation(
    data: pl.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    allow_duplicates: bool = False,
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from polars DataFrame using parent and child names, return root of tree.

    Root node is inferred when parent name is empty, or when name appears in parent column but not in child column.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated.
    Error will be thrown if names of intermediate nodes are repeated as there will be confusion.
    This error can be ignored by setting `allow_duplicates` to be True.

    `child_col` and `parent_col` specify columns for child name and parent name to construct tree.
    `attribute_cols` specify columns for node attribute for child name.
    If columns are not specified, `child_col` takes first column, `parent_col` takes second column, and all other
    columns are `attribute_cols`.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    Examples:
        >>> import polars as pl
        >>> from bigtree import polars_to_tree_by_relation
        >>> relation_data = pl.DataFrame([
        ...     ["a", None, 90],
        ...     ["b", "a", 65],
        ...     ["c", "a", 60],
        ...     ["d", "b", 40],
        ...     ["e", "b", 35],
        ...     ["f", "c", 38],
        ...     ["g", "e", 10],
        ...     ["h", "e", 6],
        ... ],
        ...     schema=["child", "parent", "age"]
        ... )
        >>> root = polars_to_tree_by_relation(relation_data)
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
        data (pl.DataFrame): data containing path and node attribute information
        child_col (str): column of data containing child name information, defaults to None
            if not set, it will take the first column of data
        parent_col (str): column of data containing parent name information, defaults to None
            if not set, it will take the second column of data
        attribute_cols (List[str]): columns of data containing node attribute information,
            if not set, it will take all columns of data except `child_col` and `parent_col`
        allow_duplicates (bool): allow duplicate intermediate nodes such that child node will
            be tagged to multiple parent nodes, defaults to False
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_dataframe_not_empty(data)

    if not child_col:
        child_col = data.columns[0]
    if not parent_col:
        parent_col = data.columns[1]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)

    data = data[[child_col, parent_col] + attribute_cols]
    if not allow_duplicates:
        assert_dataframe_no_duplicate_children(data, child_col, parent_col)

    # Infer root node
    root_names = set(data.filter(data[parent_col].is_null())[child_col])
    root_names.update(set(data[parent_col]) - set(data[child_col]) - {None})
    if len(root_names) != 1:
        raise ValueError(
            f"Unable to determine root node\n"
            f"Possible root nodes: {sorted(list(root_names), key=lambda v: (isinstance(v, str), v))}"
        )
    root_name = list(root_names)[0]

    def _retrieve_attr(_row: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve node attributes from dictionary, remove parent and child column from dictionary.

        Args:
            _row (Dict[str, Any]): node attributes

        Returns:
            (Dict[str, Any])
        """
        node_attrs = filter_attributes(
            _row, omit_keys=[child_col, parent_col], omit_null_values=True
        )
        node_attrs["name"] = _row[child_col]
        return node_attrs

    def _recursive_add_child(parent_node: T) -> None:
        """Recursive add child to tree, given current node.

        Args:
            parent_node (Node): parent node
        """
        child_rows = data.filter(data[parent_col] == parent_node.node_name)

        for row_kwargs in child_rows.to_dicts():
            child_node = node_type(**_retrieve_attr(row_kwargs))
            child_node.parent = parent_node
            _recursive_add_child(child_node)

    # Create root node attributes
    root_row = data.filter(data[child_col] == root_name)
    if len(root_row):
        root_row_kwargs_list = root_row.to_dicts()
        root_row_kwargs = root_row_kwargs_list[0] if root_row_kwargs_list else {}
        root_node = node_type(**_retrieve_attr(root_row_kwargs))
    else:
        root_node = node_type(root_name)
    _recursive_add_child(root_node)
    return root_node


def newick_to_tree(
    tree_string: str,
    length_attr: str = "length",
    attr_prefix: str = "&&NHX:",
    node_type: Type[T] = Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from Newick notation, return root of tree.

    In the Newick Notation (or New Hampshire Notation)

    - Tree is represented in round brackets i.e., `(child1,child2,child3)parent`.
    - If there are nested trees, they will be in nested round brackets i.e., `((grandchild1)child1,(grandchild2,grandchild3)child2)parent`.
    - If there is length attribute, they will be beside the name i.e., `(child1:0.5,child2:0.1)parent`.
    - If there are other attributes, attributes are represented in square brackets i.e., `(child1:0.5[S:human],child2:0.1[S:human])parent[S:parent]`.

    Variations supported

    - Support special characters (`[`, `]`, `(`, `)`, `:`, `,`) in node name, attribute name, and attribute values if
        they are enclosed in single quotes i.e., '(name:!)'.
    - If there are no node names, it will be auto-filled with convention `nodeN` with N representing a number.

    Examples:
        >>> from bigtree import newick_to_tree
        >>> root = newick_to_tree("((d,e)b,c)a")
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> root = newick_to_tree("((d:40,e:35)b:65,c:60)a", length_attr="age")
        >>> root.show(attr_list=["age"])
        a
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        └── c [age=60]

        >>> root = newick_to_tree(
        ...     "((d:40[&&NHX:species=human],e:35[&&NHX:species=human])b:65[&&NHX:species=human],c:60[&&NHX:species=human])a[&&NHX:species=human]",
        ...     length_attr="age",
        ... )
        >>> root.show(all_attrs=True)
        a [species=human]
        ├── b [age=65, species=human]
        │   ├── d [age=40, species=human]
        │   └── e [age=35, species=human]
        └── c [age=60, species=human]

    Args:
        tree_string (str): Newick notation to construct tree
        length_attr (str): attribute name to store node length, optional, defaults to 'length'
        attr_prefix (str): prefix before all attributes, within square bracket, used to detect attributes, defaults to "&&NHX:"
        node_type (Type[Node]): node type of tree to be created, defaults to ``Node``

    Returns:
        (Node)
    """
    assert_length_not_empty(tree_string, "Tree string", "tree_string")

    # Store results (for tracking)
    depth_nodes: Dict[int, List[T]] = defaultdict(list)
    unlabelled_node_counter: int = 0
    current_depth: int = 1
    tree_string_idx: int = 0

    # Store states (for assertions and checks)
    current_state: NewickState = NewickState.PARSE_STRING
    current_node: Optional[T] = None
    cumulative_string: str = ""
    cumulative_string_value: str = ""

    def _create_node(
        _new_node: Optional[T],
        _cumulative_string: str,
        _unlabelled_node_counter: int,
        _depth_nodes: Dict[int, List[T]],
        _current_depth: int,
    ) -> Tuple[T, int]:
        """Create node at checkpoint.

        Args:
            _new_node (Optional[Node]): existing node (to add length attribute), or nothing (to create a node)
            _cumulative_string (str): cumulative string, contains either node name or length attribute
            _unlabelled_node_counter (int): number of unlabelled nodes, updates and returns counter
            _depth_nodes (Dict[int, List[Node]]): list of nodes at each depth
            _current_depth (int): depth of current node or node to be created

        Returns:
            (Tuple[Node, int])
        """
        if not _new_node:
            if not _cumulative_string:
                _cumulative_string = f"node{_unlabelled_node_counter}"
                _unlabelled_node_counter += 1
            _new_node = node_type(_cumulative_string)
            _depth_nodes[_current_depth].append(_new_node)
        elif _cumulative_string:
            _new_node.set_attrs(
                {
                    length_attr: (
                        int(_cumulative_string)
                        if _cumulative_string.isdigit()
                        else float(_cumulative_string)
                    )
                }
            )

        if len(_depth_nodes[_current_depth + 1]):
            _new_node.children = depth_nodes[_current_depth + 1]  # type: ignore
            del _depth_nodes[_current_depth + 1]
        return _new_node, _unlabelled_node_counter

    def _raise_value_error(tree_idx: int) -> None:
        """Raise value error.

        Raises:
            ValueError
        """
        raise ValueError(
            f"String not properly closed, check `tree_string` at index {tree_idx}"
        )

    while tree_string_idx < len(tree_string):
        character = tree_string[tree_string_idx]
        if character == NewickCharacter.OPEN_BRACKET:
            # Check and/or change state
            state_title = "Node creation start"
            if current_state not in [NewickState.PARSE_STRING]:
                _raise_value_error(tree_string_idx)
            # Logic
            current_depth += 1
            if current_node:
                _raise_value_error(tree_string_idx)
            if cumulative_string:
                _raise_value_error(tree_string_idx)
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character in [
            NewickCharacter.CLOSE_BRACKET,
            NewickCharacter.ATTR_START,
            NewickCharacter.NODE_SEP,
        ]:
            # Check and/or change state
            state_title = "Node creation end / Node attribute start"
            if current_state not in [
                NewickState.PARSE_STRING,
                NewickState.PARSE_ATTRIBUTE_NAME,
            ]:
                _raise_value_error(tree_string_idx)
            # Logic
            if character == NewickCharacter.ATTR_START:
                current_state = NewickState.PARSE_ATTRIBUTE_NAME
                if tree_string[tree_string_idx + 1 :].startswith(  # noqa: E203
                    attr_prefix
                ):
                    tree_string_idx += len(attr_prefix)
            current_node, unlabelled_node_counter = _create_node(
                current_node,
                cumulative_string,
                unlabelled_node_counter,
                depth_nodes,
                current_depth,
            )
            if character == NewickCharacter.CLOSE_BRACKET:
                current_depth -= 1
                current_node = None
            if character == NewickCharacter.NODE_SEP:
                current_node = None
            cumulative_string = ""
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character == NewickCharacter.ATTR_END:
            # Check and/or change state
            state_title = "Node attribute end"
            if current_state not in [NewickState.PARSE_ATTRIBUTE_VALUE]:
                _raise_value_error(tree_string_idx)
            current_state = NewickState.PARSE_STRING
            # Logic
            assert current_node, f"{state_title}, should have current_node"
            current_node.set_attrs({cumulative_string: cumulative_string_value})
            cumulative_string = ""
            cumulative_string_value = ""
            tree_string_idx += 1
            continue

        if character == NewickCharacter.ATTR_KEY_VALUE:
            # Check and/or change state
            state_title = "Node attribute creation"
            if current_state not in [NewickState.PARSE_ATTRIBUTE_NAME]:
                _raise_value_error(tree_string_idx)
            current_state = NewickState.PARSE_ATTRIBUTE_VALUE
            # Logic
            assert current_node, f"{state_title}, should have current_node"
            if not cumulative_string:
                _raise_value_error(tree_string_idx)
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character == NewickCharacter.ATTR_QUOTE:
            # Logic
            quote_end_idx = tree_string.find(
                NewickCharacter.ATTR_QUOTE, tree_string_idx + 1
            )
            if quote_end_idx == -1:
                _raise_value_error(tree_string_idx)
            if current_state in [
                NewickState.PARSE_STRING,
                NewickState.PARSE_ATTRIBUTE_NAME,
            ]:
                if cumulative_string:
                    _raise_value_error(tree_string_idx)
                cumulative_string = tree_string[
                    tree_string_idx + 1 : quote_end_idx  # noqa: E203
                ]
            else:
                if cumulative_string_value:
                    _raise_value_error(tree_string_idx)
                cumulative_string_value = tree_string[
                    tree_string_idx + 1 : quote_end_idx  # noqa: E203
                ]
            tree_string_idx = quote_end_idx + 1
            continue

        if character == NewickCharacter.SEP:
            # Check and/or change state
            state_title = "Node length creation / Node attribute creation"
            if current_state not in [
                NewickState.PARSE_STRING,
                NewickState.PARSE_ATTRIBUTE_VALUE,
            ]:
                _raise_value_error(tree_string_idx)
            # Logic
            if current_state == NewickState.PARSE_STRING:
                if current_node:
                    _raise_value_error(tree_string_idx)
                current_node, unlabelled_node_counter = _create_node(
                    current_node,
                    cumulative_string,
                    unlabelled_node_counter,
                    depth_nodes,
                    current_depth,
                )
                cumulative_string = ""
                assert (
                    not cumulative_string_value
                ), f"{state_title}, should not have cumulative_string_value"
                tree_string_idx += 1
                continue
            else:
                current_state = NewickState.PARSE_ATTRIBUTE_NAME
                assert current_node, f"{state_title}, should not have current_node"
                current_node.set_attrs({cumulative_string: cumulative_string_value})
                cumulative_string = ""
                cumulative_string_value = ""
                tree_string_idx += 1
                continue

        if current_state == NewickState.PARSE_ATTRIBUTE_VALUE:
            cumulative_string_value += character
        else:
            cumulative_string += character
        tree_string_idx += 1

    if current_depth != 1:
        _raise_value_error(tree_string_idx)

    # Final root node
    if len(depth_nodes[current_depth]):
        current_node = depth_nodes[current_depth][0]
    current_node, unlabelled_node_counter = _create_node(
        current_node,
        cumulative_string,
        unlabelled_node_counter,
        depth_nodes,
        current_depth,
    )
    return current_node
