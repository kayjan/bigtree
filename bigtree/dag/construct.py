from typing import List, Tuple, Type

import numpy as np
import pandas as pd

from bigtree.node.dagnode import DAGNode

__all__ = ["list_to_dag", "dict_to_dag", "dataframe_to_dag"]


def list_to_dag(
    relations: List[Tuple[str, str]],
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from list of tuple containing parent-child names.
    Note that node names must be unique.

    >>> from bigtree import list_to_dag, dag_iterator
    >>> relations_list = [("a", "c"), ("a", "d"), ("b", "c"), ("c", "d"), ("d", "e")]
    >>> dag = list_to_dag(relations_list)
    >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
    [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        relations (list): list containing tuple of parent-child names
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to DAGNode

    Returns:
        (DAGNode)
    """
    node_dict = dict()
    parent_node = None

    for parent_name, child_name in relations:
        parent_node = node_dict.get(parent_name)
        if not parent_node:
            parent_node = node_type(parent_name)

        child_node = node_dict.get(child_name)
        if not child_node:
            child_node = node_type(child_name)

        node_dict[parent_name] = parent_node
        node_dict[child_name] = child_node

        parent_node.children = [child_node]

    return parent_node


def dict_to_dag(
    relation_attrs: dict,
    parent_key: str = "parents",
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from nested dictionary, ``key``: child name, ``value``: dict of parent names, attribute name and
    attribute value.
    Note that node names must be unique.

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
        relation_attrs (dict): dictioning containing node, node parents, and node attribute information,
            key: child name, value: dict of parent names, node attribute and attribute value
        parent_key (str): key of dictionary to retrieve list of parents name, defaults to "parent"
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to DAGNode

    Returns:
        (DAGNode)
    """
    if not len(relation_attrs):
        raise ValueError("Dictionary does not contain any data, check `relation_attrs`")

    # Convert dictionary to dataframe
    data = pd.DataFrame(relation_attrs).T.rename_axis("_tmp_child").reset_index()
    assert (
        parent_key in data
    ), f"Parent key {parent_key} not in dictionary, check `relation_attrs` and `parent_key`"

    data = data.explode(parent_key)
    return dataframe_to_dag(
        data,
        child_col="_tmp_child",
        parent_col=parent_key,
        node_type=node_type,
    )


def dataframe_to_dag(
    data: pd.DataFrame,
    child_col: str = None,
    parent_col: str = None,
    attribute_cols: list = [],
    node_type: Type[DAGNode] = DAGNode,
) -> DAGNode:
    """Construct DAG from pandas DataFrame.
    Note that node names must be unique.

    `child_col` and `parent_col` specify columns for child name and parent name to construct DAG.
    `attribute_cols` specify columns for node attribute for child name
    If columns are not specified, `parent_col` takes first column, `child_col` takes second column, and all other
    columns are `attribute_cols`.

    >>> import pandas as pd
    >>> from bigtree import dataframe_to_dag, dag_iterator
    >>> path_data = pd.DataFrame([
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
    >>> dag = dataframe_to_dag(path_data)
    >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)]
    [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]

    Args:
        data (pandas.DataFrame): data containing path and node attribute information
        child_col (str): column of data containing child name information, defaults to None
            if not set, it will take the first column of data
        parent_col (str): column of data containing parent name information, defaults to None
            if not set, it will take the second column of data
        attribute_cols (list): columns of data containing child node attribute information,
            if not set, it will take all columns of data except `child_col` and `parent_col`
        node_type (Type[DAGNode]): node type of DAG to be created, defaults to DAGNode

    Returns:
        (DAGNode)
    """
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

    data_check = data.copy()[[child_col] + attribute_cols].drop_duplicates()
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
            f"There exists duplicate child name with different attributes\nCheck {_duplicate_check}"
        )
    if np.any(data[child_col].isnull()):
        raise ValueError(f"Child name cannot be empty, check {child_col}")

    node_dict = dict()
    parent_node = None

    for row in data.reset_index(drop=True).to_dict(orient="index").values():
        child_name = row[child_col]
        parent_name = row[parent_col]
        node_attrs = row.copy()
        del node_attrs[child_col]
        del node_attrs[parent_col]
        node_attrs = {k: v for k, v in node_attrs.items() if not pd.isnull(v)}
        child_node = node_dict.get(child_name)
        if not child_node:
            child_node = node_type(child_name)
        node_dict[child_name] = child_node
        child_node.set_attrs(node_attrs)

        if not pd.isnull(parent_name):
            parent_node = node_dict.get(parent_name)
            if not parent_node:
                parent_node = node_type(parent_name)
            node_dict[parent_name] = parent_node
            child_node.parents = [parent_node]

    return parent_node
