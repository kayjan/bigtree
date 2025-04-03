from __future__ import annotations

from typing import Any, Dict, TypeVar

from bigtree.node import node
from bigtree.utils import exceptions

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

try:
    import polars as pl
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pl = MagicMock()


__all__ = [
    "tree_to_dataframe",
    "tree_to_polars",
]

T = TypeVar("T", bound=node.Node)


@exceptions.optional_dependencies_pandas
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

    Examples:
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
        tree: tree to be exported
        path_col: column name for `node.path_name`
        name_col: column name for `node.node_name`
        parent_col: column name for `node.parent.node_name`
        attr_dict: dictionary mapping node attributes to column name, key: node attributes, value: corresponding column
            in dataframe
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree
        skip_depth: number of initial depths to skip
        leaf_only: indicator to retrieve only information from leaf nodes

    Returns:
        pandas DataFrame containing tree information
    """
    data_list = []

    def _recursive_append(_node: T) -> None:
        """Recursively iterate through node and its children to export to dataframe.

        Args:
            _node: current node
        """
        if _node:
            if (
                (not max_depth or _node.depth <= max_depth)
                and (not skip_depth or _node.depth > skip_depth)
                and (not leaf_only or _node.is_leaf)
            ):
                data_child: Dict[str, Any] = {}
                if path_col:
                    data_child[path_col] = _node.path_name
                if name_col:
                    data_child[name_col] = _node.node_name
                if parent_col:
                    parent_name = None
                    if _node.parent:
                        parent_name = _node.parent.node_name
                    data_child[parent_col] = parent_name

                if all_attrs:
                    data_child.update(
                        _node.describe(exclude_attributes=["name"], exclude_prefix="_")
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = _node.get_attr(k)
                data_list.append(data_child)
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return pd.DataFrame(data_list)


@exceptions.optional_dependencies_polars
def tree_to_polars(
    tree: T,
    path_col: str = "path",
    name_col: str = "name",
    parent_col: str = "",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> pl.DataFrame:
    """Export tree to polars DataFrame.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Examples:
        >>> from bigtree import Node, tree_to_polars
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree_to_polars(root, name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
        shape: (5, 4)
        ┌────────┬──────┬────────┬────────────┐
        │ path   ┆ name ┆ parent ┆ person age │
        │ ---    ┆ ---  ┆ ---    ┆ ---        │
        │ str    ┆ str  ┆ str    ┆ i64        │
        ╞════════╪══════╪════════╪════════════╡
        │ /a     ┆ a    ┆ null   ┆ 90         │
        │ /a/b   ┆ b    ┆ a      ┆ 65         │
        │ /a/b/d ┆ d    ┆ b      ┆ 40         │
        │ /a/b/e ┆ e    ┆ b      ┆ 35         │
        │ /a/c   ┆ c    ┆ a      ┆ 60         │
        └────────┴──────┴────────┴────────────┘

        For a subset of a tree.

        >>> tree_to_polars(b, name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
        shape: (3, 4)
        ┌────────┬──────┬────────┬────────────┐
        │ path   ┆ name ┆ parent ┆ person age │
        │ ---    ┆ ---  ┆ ---    ┆ ---        │
        │ str    ┆ str  ┆ str    ┆ i64        │
        ╞════════╪══════╪════════╪════════════╡
        │ /a/b   ┆ b    ┆ a      ┆ 65         │
        │ /a/b/d ┆ d    ┆ b      ┆ 40         │
        │ /a/b/e ┆ e    ┆ b      ┆ 35         │
        └────────┴──────┴────────┴────────────┘

    Args:
        tree: tree to be exported
        path_col: column name for `node.path_name`
        name_col: column name for `node.node_name`
        parent_col: column name for `node.parent.node_name`
        attr_dict: dictionary mapping node attributes to column name, key: node attributes, value: corresponding column
            in dataframe
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree
        skip_depth: number of initial depths to skip
        leaf_only: indicator to retrieve only information from leaf nodes

    Returns:
        polars DataFrame containing tree information
    """
    data_list = []

    def _recursive_append(_node: T) -> None:
        """Recursively iterate through node and its children to export to dataframe.

        Args:
            _node: current node
        """
        if _node:
            if (
                (not max_depth or _node.depth <= max_depth)
                and (not skip_depth or _node.depth > skip_depth)
                and (not leaf_only or _node.is_leaf)
            ):
                data_child: Dict[str, Any] = {}
                if path_col:
                    data_child[path_col] = _node.path_name
                if name_col:
                    data_child[name_col] = _node.node_name
                if parent_col:
                    parent_name = None
                    if _node.parent:
                        parent_name = _node.parent.node_name
                    data_child[parent_col] = parent_name

                if all_attrs:
                    data_child.update(
                        _node.describe(exclude_attributes=["name"], exclude_prefix="_")
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = _node.get_attr(k)
                data_list.append(data_child)
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return pl.DataFrame(data_list)
