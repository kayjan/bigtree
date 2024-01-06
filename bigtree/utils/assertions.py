from typing import Any, Dict, List


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
