from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Sized, Type, Union

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

try:
    import polars as pl
except ImportError:  # pragma: no cover
    pl = None


if TYPE_CHECKING:
    from bigtree.node.basenode import BaseNode
    from bigtree.node.dagnode import DAGNode
    from bigtree.node.node import Node


__all__ = [
    "assert_style_in_dict",
    "assert_str_in_list",
    "assert_key_in_dict",
    "assert_length_not_empty",
    "assert_dataframe_not_empty",
    "assert_dataframe_no_duplicate_attribute",
    "assert_dataframe_no_duplicate_children",
    "assert_tree_type",
    "isnull",
    "filter_attributes",
]


def assert_style_in_dict(
    parameter: Any,
    accepted_parameters: Dict[str, Any],
) -> None:
    """Raise ValueError is parameter is not in list of accepted parameters

    Args:
        parameter (Any): argument input for parameter
        accepted_parameters (List[Any]): list of accepted parameters
    """
    if parameter not in accepted_parameters:
        raise ValueError(
            f"Choose one of {accepted_parameters.keys()} style, alternatively you can define own style"
        )


def assert_str_in_list(
    parameter_name: str,
    parameter: Any,
    accepted_parameters: List[Any],
) -> None:
    """Raise ValueError is parameter is not in list of accepted parameters

    Args:
        parameter_name (str): parameter name for error message
        parameter (Any): argument input for parameter
        accepted_parameters (List[Any]): list of accepted parameters
    """
    if parameter not in accepted_parameters:
        raise ValueError(
            f"Invalid input, check `{parameter_name}` should be one of {accepted_parameters}"
        )


def assert_key_not_in_dict_or_df(
    parameter_dict: Union[Dict[str, Any], pd.DataFrame],
    not_accepted_parameters: List[str],
) -> None:
    """Raise ValueError is parameter is in key of dictionary

    Args:
        parameter_dict (Dict[str, Any]/pd.DataFrame): argument input for parameter
        not_accepted_parameters (List[str]): list of not accepted parameters
    """
    for parameter in parameter_dict:
        if parameter in not_accepted_parameters:
            raise ValueError(
                f"Invalid input, check `{parameter}` is not a valid key as it is a reserved keyword"
            )


def assert_key_in_dict(
    parameter_name: str,
    parameter: Any,
    accepted_parameters: Dict[Any, Any],
) -> None:
    """Raise ValueError is parameter is not in key of dictionary

    Args:
        parameter_name (str): parameter name for error message
        parameter (Any): argument input for parameter
        accepted_parameters (Dict[Any]): dictionary of accepted parameters
    """
    if parameter not in accepted_parameters:
        raise ValueError(
            f"Invalid input, check `{parameter_name}` should be one of {accepted_parameters.keys()}"
        )


def assert_length_not_empty(data: Sized, argument_name: str, argument: str) -> None:
    """Raise ValueError if data does not have length

    Args:
        data (Sized): data to check
        argument_name: argument name for data, for error message
        argument (str): argument for data, for error message
    """
    if not len(data):
        raise ValueError(
            f"{argument_name} does not contain any data, check `{argument}`"
        )


def assert_dataframe_not_empty(data: pd.DataFrame) -> None:
    """Raise ValueError is dataframe is empty

    Args:
        data (pd.DataFrame): dataframe to check
    """
    if not len(data.columns):
        raise ValueError("Data does not contain any columns, check `data`")
    if not len(data):
        raise ValueError("Data does not contain any rows, check `data`")


def assert_dataframe_no_duplicate_attribute(
    data: Union[pd.DataFrame, pl.DataFrame],
    id_type: str,
    id_col: str,
    attribute_cols: List[str],
) -> None:
    """Raise ValueError is dataframe contains different attributes for same path

    Args:
        data (Union[pd.DataFrame, pl.DataFrame]): dataframe to check
        id_type (str): type of uniqueness to check for, for error message
        id_col (str): column of data that is unique, can be name or path
        attribute_cols (List[str]): columns of data containing node attribute information,
    """
    if pd and isinstance(data, pd.DataFrame):
        data_check = data[[id_col] + attribute_cols].astype(str).drop_duplicates()
        duplicate_check = (
            data_check[id_col]
            .value_counts()
            .to_frame("count")
            .rename_axis(id_col)
            .reset_index()
        )
        duplicate_check = duplicate_check[duplicate_check["count"] > 1]
    else:
        data_check = data.unique(subset=[id_col] + attribute_cols)
        duplicate_check = data_check[id_col].value_counts()
        duplicate_check = duplicate_check.filter(duplicate_check["count"] > 1)
    if len(duplicate_check):
        raise ValueError(
            f"There exists duplicate {id_type} with different attributes\nCheck {duplicate_check}"
        )


def assert_dataframe_no_duplicate_children(
    data: Union[pd.DataFrame, pl.DataFrame],
    child_col: str,
    parent_col: str,
) -> None:
    """Raise ValueError is dataframe contains different duplicated parent tagged to different grandparents

    Args:
        data (Union[pd.DataFrame, pl.DataFrame]): dataframe to check
        child_col (str): column of data containing child name information
        parent_col (str): column of data containing parent name information
    """
    # Filter for child nodes that are parent of other nodes
    if pd and isinstance(data, pd.DataFrame):
        data_check = data[[child_col, parent_col]].drop_duplicates()
        data_check = data_check[data_check[child_col].isin(data_check[parent_col])]
        duplicate_check = (
            data_check[child_col]
            .value_counts()
            .to_frame("count")
            .rename_axis(child_col)
            .reset_index()
        )
        duplicate_check = duplicate_check[duplicate_check["count"] > 1]
    else:
        data_check = data.unique(subset=[child_col, parent_col])
        data_check = data_check.filter(
            data_check[child_col].is_in(data_check[parent_col])
        )
        duplicate_check = data_check[child_col].value_counts()
        duplicate_check = duplicate_check.filter(duplicate_check["count"] > 1)
    if len(duplicate_check):
        raise ValueError(
            f"There exists duplicate child with different parent where the child is also a parent node.\n"
            f"Duplicated node names should not happen, but can only exist in leaf nodes to avoid confusion.\n"
            f"Check {duplicate_check}"
        )


def assert_tree_type(
    tree: Union[BaseNode, Node, DAGNode],
    tree_type: Union[Type[BaseNode], Type[Node], Type[DAGNode]],
    tree_type_name: str,
) -> None:
    """Raise TypeError is tree is not of `tree_type`

    Args:
        tree (Union["BaseNode", "Node", "DAGNode"]): tree to check
        tree_type: tree type to assert for
        tree_type_name (str): tree type name
    """
    if not isinstance(tree, tree_type):
        raise TypeError(
            f"Tree should be of type `{tree_type_name}`, or inherit from `{tree_type_name}`"
        )


def isnull(value: Any) -> bool:
    """Check if value is null

    Args:
        value (Any): value to check

    Returns:
        (bool)
    """
    import math

    if value is None or (isinstance(value, float) and math.isnan(value)):
        return True
    return False


def filter_attributes(
    node_attributes: Dict[str, Any],
    omit_keys: List[str],
    omit_null_values: bool,
) -> Dict[str, Any]:
    """Filter node attributes to remove certain keys and/or values

    Args:
        node_attributes (Dict[str, Any]): node attribute dictionary
        omit_keys (List[str]): list of keys to omit
        omit_null_values (bool): indicator whether to omit values that are null

    Returns:
        (Dict[str, Any])
    """
    if omit_null_values:
        return {
            k: v
            for k, v in node_attributes.items()
            if not isnull(v) and k not in omit_keys
        }
    return {k: v for k, v in node_attributes.items() if k not in omit_keys}
