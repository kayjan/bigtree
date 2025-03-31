from __future__ import annotations

from typing import Any, Dict, List, Tuple, Type, TypeVar

from bigtree.node import dagnode
from bigtree.utils import assertions, exceptions

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

__all__ = ["list_to_dag", "dict_to_dag", "dataframe_to_dag"]

T = TypeVar("T", bound=dagnode.DAGNode)


def list_to_dag(
    relations: List[Tuple[str, str]],
    node_type: Type[T] = dagnode.DAGNode,  # type: ignore[assignment]
) -> T:
    """Construct DAG from list of tuples containing parent-child names. Note that node names must be unique.

    Examples:
        >>> from bigtree import list_to_dag, dag_iterator
        >>> relations_list = [("a", "c"), ("a", "d"), ("b", "c"), ("c", "d"), ("d", "e")]
        >>> dag = list_to_dag(relations_list)
        >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
        [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        relations: list containing tuple of parent-child names
        node_type: node type of DAG to be created

    Returns:
        DAG node
    """
    assertions.assert_length_not_empty(relations, "Input list", "relations")

    node_dict: Dict[str, T] = dict()
    parent_node: T = dagnode.DAGNode()  # type: ignore[assignment]

    for parent_name, child_name in relations:
        if parent_name not in node_dict:
            parent_node = node_type(parent_name)
            node_dict[parent_name] = parent_node
        else:
            parent_node = node_dict[parent_name]
        if child_name not in node_dict:
            child_node = node_type(child_name)
            node_dict[child_name] = child_node
        else:
            child_node = node_dict[child_name]

        child_node.parents = [parent_node]

    return parent_node


def dict_to_dag(
    relation_attrs: Dict[str, Any],
    parent_key: str = "parents",
    node_type: Type[T] = dagnode.DAGNode,  # type: ignore[assignment]
) -> T:
    """Construct DAG from nested dictionary, ``key``: child name, ``value``: dictionary of parent names and attributes.
    Note that node names must be unique.

    Examples:
        >>> from bigtree import dict_to_dag, dag_iterator
        >>> relation_dict = {
        ...     "a": {"step": 1},
        ...     "b": {"step": 1},
        ...     "c": {"parents": ["a", "b"], "step": 2},
        ...     "d": {"parents": ["a", "c"], "step": 2},
        ...     "e": {"parents": ["d"], "step": 3},
        ... }
        >>> dag = dict_to_dag(relation_dict, parent_key="parents")
        >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
        [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        relation_attrs: dictionary containing node, node parents, and node attribute information,
            key: child name, value: dictionary of parent names and attributes
        parent_key: key of dictionary to retrieve list of parents name
        node_type: node type of DAG to be created

    Returns:
        DAG node
    """
    assertions.assert_length_not_empty(relation_attrs, "Dictionary", "relation_attrs")

    node_dict: Dict[str, T] = dict()
    parent_node: T | None = None

    for child_name, node_attrs in relation_attrs.items():
        node_attrs = node_attrs.copy()
        parent_names: List[str] = []
        if parent_key in node_attrs:
            parent_names = node_attrs.pop(parent_key)
        assertions.assert_not_reserved_keywords(
            node_attrs, ["parent", "parents", "children"]
        )

        if child_name in node_dict:
            child_node = node_dict[child_name]
            child_node.set_attrs(node_attrs)
        else:
            child_node = node_type(child_name, **node_attrs)
            node_dict[child_name] = child_node

        for parent_name in parent_names:
            parent_node = node_dict.get(parent_name, node_type(parent_name))
            node_dict[parent_name] = parent_node
            child_node.parents = [parent_node]

    if parent_node is None:
        raise ValueError(
            f"Parent key {parent_key} not in dictionary, check `relation_attrs` and `parent_key`"
        )

    return parent_node


@exceptions.optional_dependencies_pandas
def dataframe_to_dag(
    data: pd.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    node_type: Type[T] = dagnode.DAGNode,  # type: ignore[assignment]
) -> T:
    """Construct DAG from pandas DataFrame. Note that node names must be unique.

    - `child_col` and `parent_col` specify columns for child name and parent name to construct DAG.
    - `attribute_cols` specify columns for node attribute for child name.
    - If columns are not specified, `child_col` takes first column, `parent_col` takes second column, and all other
        columns are `attribute_cols`.

    Only attributes in `attribute_cols` with non-null values will be added to the tree.

    Examples:
        >>> import pandas as pd
        >>> from bigtree import dataframe_to_dag, dag_iterator
        >>> relation_data = pd.DataFrame([
        ...     ["a", None, 1],
        ...     ["b", None, 1],
        ...     ["c", "a", 2],
        ...     ["c", "b", 2],
        ...     ["d", "a", 2],
        ...     ["d", "c", 2],
        ...     ["e", "d", 3],
        ... ],
        ...     columns=["child", "parent", "step"]
        ... )
        >>> dag = dataframe_to_dag(relation_data)
        >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
        [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        data: data containing path and node attribute information
        child_col: column of data containing child name information, if not set, it will take the first column of data
        parent_col: column of data containing parent name information, if not set, it will take the second column of data
        attribute_cols: columns of data containing child node attribute information, if not set, it will take all columns
            of data except `child_col` and `parent_col`
        node_type: node type of DAG to be created

    Returns:
        DAG node
    """
    assertions.assert_dataframe_not_empty(data)

    if not child_col:
        child_col = data.columns[0]
    elif child_col not in data.columns:
        raise ValueError(f"Child column not in data, check `child_col`: {child_col}")
    if not parent_col:
        parent_col = data.columns[1]
    elif parent_col not in data.columns:
        raise ValueError(f"Parent column not in data, check `parent_col`: {parent_col}")
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)
    assertions.assert_not_reserved_keywords(
        attribute_cols, ["parent", "parents", "children"]
    )

    data = data[[child_col, parent_col] + attribute_cols].copy()

    assertions.assert_dataframe_no_duplicate_attribute(
        data, "child name", child_col, attribute_cols
    )
    if sum(data[child_col].isnull()):
        raise ValueError(f"Child name cannot be empty, check column: {child_col}")

    node_dict: Dict[str, T] = dict()
    parent_node: T = dagnode.DAGNode()  # type: ignore[assignment]

    for row in data.reset_index(drop=True).to_dict(orient="index").values():
        child_name = row[child_col]
        parent_name = row[parent_col]
        node_attrs = assertions.filter_attributes(
            row, omit_keys=["name", child_col, parent_col], omit_null_values=True
        )
        child_node = node_dict.get(child_name, node_type(child_name, **node_attrs))
        child_node.set_attrs(node_attrs)
        node_dict[child_name] = child_node

        if not assertions.isnull(parent_name):
            parent_node = node_dict.get(parent_name, node_type(parent_name))
            node_dict[parent_name] = parent_node
            child_node.parents = [parent_node]

    return parent_node
