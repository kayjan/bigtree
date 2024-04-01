from __future__ import annotations

import math
from typing import Any, Dict, List, Union

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None


def assert_style_in_dict(
    parameter: Any,
    accepted_parameters: Dict[str, Any],
) -> None:
    """Raise ValueError is parameter is not in list of accepted parameters

    Args:
        parameter (Any): argument input for parameter
        accepted_parameters (List[Any]): list of accepted parameters
    """
    if parameter not in accepted_parameters and parameter != "custom":
        raise ValueError(
            f"Choose one of {accepted_parameters.keys()} style, use `custom` to define own style"
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


def assert_length_not_empty(
    data: Union[str, List[Any]], argument_name: str, argument: str
) -> None:
    """Raise ValueError if data (str, list, or iterable) does not have length

    Args:
        data (str/List[Any]): data to check
        argument_name: argument name for data, for error message
        argument (str): argument for data, for error message
    """
    if not len(data):
        raise ValueError(
            f"{argument_name} does not contain any data, check `{argument}`"
        )


def assert_dictionary_not_empty(data_dict: Dict[Any, Any], argument: str) -> None:
    """Raise ValueError is dictionary is empty

    Args:
        data_dict (Dict[Any, Any]): dictionary to check
        argument (str): argument for dictionary, for error message
    """
    if not len(data_dict):
        raise ValueError(f"Dictionary does not contain any data, check `{argument}`")


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
    data: pd.DataFrame, id_type: str, id_col: str, attribute_cols: List[str]
) -> None:
    """Raise ValueError is dataframe contains different attributes for same path

    Args:
        data (pd.DataFrame): dataframe to check
        id_type (str): type of uniqueness to check for, for error message
        id_col (str): column of data that is unique, can be name or path
        attribute_cols (List[str]): columns of data containing node attribute information,
    """
    data_check = data[[id_col] + attribute_cols].astype(str).drop_duplicates()
    duplicate_check = (
        data_check[id_col]
        .value_counts()
        .to_frame("counts")
        .rename_axis(id_col)
        .reset_index()
    )
    duplicate_check = duplicate_check[duplicate_check["counts"] > 1]
    if len(duplicate_check):
        raise ValueError(
            f"There exists duplicate {id_type} with different attributes\nCheck {duplicate_check}"
        )


def assert_dataframe_no_duplicate_children(
    data: pd.DataFrame,
    child_col: str,
    parent_col: str,
) -> None:
    """Raise ValueError is dataframe contains different duplicated parent tagged to different grandparents

    Args:
        data (pd.DataFrame): dataframe to check
        child_col (str): column of data containing child name information
        parent_col (str): column of data containing parent name information
    """
    # Filter for child nodes that are parent of other nodes
    data_check = data[[child_col, parent_col]].drop_duplicates()
    data_check = data_check[data_check[child_col].isin(data_check[parent_col])]

    duplicate_check = (
        data_check[child_col]
        .value_counts()
        .to_frame("counts")
        .rename_axis(child_col)
        .reset_index()
    )
    duplicate_check = duplicate_check[duplicate_check["counts"] > 1]
    if len(duplicate_check):
        raise ValueError(
            f"There exists duplicate child with different parent where the child is also a parent node.\n"
            f"Duplicated node names should not happen, but can only exist in leaf nodes to avoid confusion.\n"
            f"Check {duplicate_check}"
        )


def isnull(value: Any) -> bool:
    """Check if value is null

    Args:
        value (Any): value to check

    Returns:
        (bool)
    """
    if not value or (isinstance(value, float) and math.isnan(value)):
        return True
    return False
