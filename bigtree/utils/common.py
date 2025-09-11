from __future__ import annotations

from typing import Any, Collection, Mapping, TypeVar, Union

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
) -> dict[str, Any]:
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
    attr_dict: Mapping[str, str] | None,
    all_attrs: bool,
    path_col: str | None = None,
    name_col: str | None = None,
    parent_col: str | tuple[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble attributes of node into a dictionary.

    Args:
        _node: node
        attr_dict: node attributes mapped to dictionary key, key: node attributes, value: corresponding dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        path_col: column name for `_node.path_name`, if present
        name_col: column name for `_node.node_name`, if present
        parent_col: if Node, column name for `_node.parent.node_name`. If DAGNode, tuple of column name and value for
            `_node.parent.node_name`.

    Returns:
        node attributes
    """
    data_attrs = {}

    # Main attributes
    if path_col:
        assert isinstance(_node, node.Node)
        data_attrs[path_col] = _node.path_name
    if name_col:
        data_attrs[name_col] = _node.node_name
    if parent_col:
        if isinstance(_node, node.Node):
            assert isinstance(parent_col, str)
            parent_name = None
            if _node.parent:
                parent_name = _node.parent.node_name
            data_attrs[parent_col] = parent_name
        else:
            assert isinstance(parent_col, tuple)
            data_attrs[parent_col[0]] = parent_col[1]

    # Other attributes
    if all_attrs:
        data_attrs.update(
            dict(_node.describe(exclude_attributes=["name"], exclude_prefix="_"))
        )
    elif attr_dict:
        for k, v in attr_dict.items():
            data_attrs[v] = _node.get_attr(k)

    return data_attrs
