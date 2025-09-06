from __future__ import annotations

from typing import Any, Collection, Dict, Mapping, Optional, TypeVar, Union

from bigtree.node import dagnode, node

T = TypeVar("T", bound=Union[node.Node, dagnode.DAGNode])

__all__ = [
    "isnull",
    "filter_attributes",
    "assemble_attributes",
]


def isnull(value: Any) -> bool:
    """Check if value is null.

    Args:
        value: value to check

    Returns:
        Flag if value is null
    """
    import math

    if value is None or (isinstance(value, float) and math.isnan(value)):
        return True
    return False


def filter_attributes(
    node_attributes: Mapping[str, Any],
    omit_keys: Collection[str],
    omit_null_values: bool,
) -> Dict[str, Any]:
    """Filter node attributes to remove certain keys and/or values.

    Args:
        node_attributes: node attributes information
        omit_keys: keys to omit
        omit_null_values: indicator whether to omit values that are null

    Returns:
        Filtered node attributes
    """
    if omit_null_values:
        return {
            k: v
            for k, v in node_attributes.items()
            if not isnull(v) and k not in omit_keys
        }
    return {k: v for k, v in node_attributes.items() if k not in omit_keys}


def assemble_attributes(
    _node: T,
    attr_dict: Optional[Mapping[str, str]],
    all_attrs: bool,
    existing_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Assemble attributes of node into a dictionary.

    Args:
        _node: node
        attr_dict: node attributes mapped to dictionary key, key: node attributes, value: corresponding dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        existing_data: existing attributes, if any

    Returns:
        node attributes
    """
    data_attrs = existing_data or {}
    if all_attrs:
        data_attrs.update(
            dict(_node.describe(exclude_attributes=["name"], exclude_prefix="_"))
        )
    elif attr_dict:
        for k, v in attr_dict.items():
            data_attrs[v] = _node.get_attr(k)
    return data_attrs
