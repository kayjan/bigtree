from __future__ import annotations

from typing import Any, Dict, List, Tuple, Type

from bigtree.node.dagnode import DAGNode
from bigtree.utils.assertions import (
    assert_dataframe_no_duplicate_attribute,
    assert_dataframe_not_empty,
    assert_dictionary_not_empty,
    assert_length_not_empty,
    filter_attributes,
    isnull,
)
from bigtree.utils.exceptions import optional_dependencies_pandas

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

__all__ = ["list_to_dag", "dict_to_dag", "dataframe_to_dag"]


@optional_dependencies_pandas
def list_to_dag(
    relations: List[Tuple[str, str]],
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from list of tuples containing parent-child names.
    Note that node names must be unique.

    Examples:
        >>> from bigtree import list_to_dag, dag_iterator
        >>> relations_list = [("a", "c"), ("a", "d"), ("b", "c"), ("c", "d"), ("d", "e")]
        >>> dag = list_to_dag(relations_list)
        >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
        [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        relations (List[Tuple[str, str]]): list containing tuple of parent-child names
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to ``DAGNode``

    Returns:
        (DAGNode)
    """
    assert_length_not_empty(relations, "Input list", "relations")

    relation_data = pd.DataFrame(relations, columns=["parent", "child"])
    return dataframe_to_dag(
        relation_data, child_col="child", parent_col="parent", node_type=node_type
    )


@optional_dependencies_pandas
def dict_to_dag(
    relation_attrs: Dict[str, Any],
    parent_key: str = "parents",
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from nested dictionary, ``key``: child name, ``value``: dictionary of parent names, attribute
    name, and attribute value.
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
        relation_attrs (Dict[str, Any]): dictionary containing node, node parents, and node attribute information,
            key: child name, value: dictionary of parent names, node attribute, and attribute value
        parent_key (str): key of dictionary to retrieve list of parents name, defaults to 'parent'
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to ``DAGNode``

    Returns:
        (DAGNode)
    """
    assert_dictionary_not_empty(relation_attrs, "relation_attrs")

    # Convert dictionary to dataframe
    data = pd.DataFrame(relation_attrs).T.rename_axis("_tmp_child").reset_index()
    if parent_key not in data:
        raise ValueError(
            f"Parent key {parent_key} not in dictionary, check `relation_attrs` and `parent_key`"
        )

    data = data.explode(parent_key)
    return dataframe_to_dag(
        data,
        child_col="_tmp_child",
        parent_col=parent_key,
        node_type=node_type,
    )


@optional_dependencies_pandas
def dataframe_to_dag(
    data: pd.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from pandas DataFrame.
    Note that node names must be unique.

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
        data (pd.DataFrame): data containing path and node attribute information
        child_col (str): column of data containing child name information, defaults to ''
            if not set, it will take the first column of data
        parent_col (str): column of data containing parent name information, defaults to ''
            if not set, it will take the second column of data
        attribute_cols (List[str]): columns of data containing child node attribute information,
            if not set, it will take all columns of data except `child_col` and `parent_col`
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to ``DAGNode``

    Returns:
        (DAGNode)
    """
    assert_dataframe_not_empty(data)

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
    elif any([col not in data.columns for col in attribute_cols]):
        raise ValueError(
            f"One or more attribute column(s) not in data, check `attribute_cols`: {attribute_cols}"
        )

    data = data[[child_col, parent_col] + attribute_cols].copy()

    assert_dataframe_no_duplicate_attribute(
        data, "child name", child_col, attribute_cols
    )
    if sum(data[child_col].isnull()):
        raise ValueError(f"Child name cannot be empty, check column: {child_col}")

    node_dict: Dict[str, DAGNode] = dict()
    parent_node = DAGNode()

    for row in data.reset_index(drop=True).to_dict(orient="index").values():
        child_name = row[child_col]
        parent_name = row[parent_col]
        node_attrs = filter_attributes(
            row, omit_keys=["name", child_col, parent_col], omit_null_values=True
        )
        child_node = node_dict.get(child_name, node_type(child_name, **node_attrs))
        child_node.set_attrs(node_attrs)
        node_dict[child_name] = child_node

        if not isnull(parent_name):
            parent_node = node_dict.get(parent_name, node_type(parent_name))
            node_dict[parent_name] = parent_node
            child_node.parents = [parent_node]

    return parent_node
