from __future__ import annotations

from typing import TypeVar

from bigtree.node import node
from bigtree.utils import common, exceptions

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
    path_col: str | None = "path",
    name_col: str | None = "name",
    parent_col: str | None = None,
    attr_dict: dict[str, str] | None = None,
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> pd.DataFrame:
    """Export tree to pandas DataFrame.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.to_dataframe(name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
             path name parent  person age
        0      /a    a   None          90
        1    /a/b    b      a          65
        2  /a/b/d    d      b          40
        3  /a/b/e    e      b          35
        4    /a/c    c      a          60

        For a subset of a tree.

        >>> b_tree = Tree(b)
        >>> b_tree.to_dataframe(name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
             path name parent  person age
        0    /a/b    b      a          65
        1  /a/b/d    d      b          40
        2  /a/b/e    e      b          35

    Args:
        tree: tree to be exported
        path_col: column name for `node.path_name`
        name_col: column name for `node.node_name`
        parent_col: column name for `node.parent.node_name`
        attr_dict: node attributes mapped to column name, key: node attributes, value: corresponding column in dataframe
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
                data_child = common.assemble_attributes(
                    _node,
                    attr_dict,
                    all_attrs,
                    path_col=path_col,
                    name_col=name_col,
                    parent_col=parent_col,
                )
                data_list.append(data_child)
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return pd.DataFrame(data_list)


@exceptions.optional_dependencies_polars
def tree_to_polars(
    tree: T,
    path_col: str | None = "path",
    name_col: str | None = "name",
    parent_col: str | None = None,
    attr_dict: dict[str, str] | None = None,
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> pl.DataFrame:
    """Export tree to polars DataFrame.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.to_polars(name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
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

        >>> b_tree = Tree(b)
        >>> b_tree.to_polars(name_col="name", parent_col="parent", path_col="path", attr_dict={"age": "person age"})
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
        attr_dict: node attributes mapped to column name, key: node attributes, value: corresponding column in dataframe
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
                data_child = common.assemble_attributes(
                    _node,
                    attr_dict,
                    all_attrs,
                    path_col=path_col,
                    name_col=name_col,
                    parent_col=parent_col,
                )
                data_list.append(data_child)
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return pl.DataFrame(data_list)
