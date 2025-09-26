from __future__ import annotations

from typing import Any, TypeVar

from bigtree.node import node
from bigtree.utils import common

__all__ = [
    "tree_to_dict",
    "tree_to_nested_dict",
    "tree_to_nested_dict_key",
]

T = TypeVar("T", bound=node.Node)


def tree_to_dict(
    tree: T,
    name_key: str | None = "name",
    parent_key: str | None = None,
    attr_dict: dict[str, str] | None = None,
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> dict[str, Any]:
    """Export tree to dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node path, and node attributes as a nested dictionary.

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.to_dict(name_key="name", parent_key="parent", attr_dict={"age": "person age"})
        {'/a': {'name': 'a', 'parent': None, 'person age': 90}, '/a/b': {'name': 'b', 'parent': 'a', 'person age': 65}, '/a/b/d': {'name': 'd', 'parent': 'b', 'person age': 40}, '/a/b/e': {'name': 'e', 'parent': 'b', 'person age': 35}, '/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

        For a subset of a tree

        >>> c_tree = Tree(c)
        >>> c_tree.to_dict(name_key="name", parent_key="parent", attr_dict={"age": "person age"})
        {'/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

    Args:
        tree: tree to be exported
        name_key: dictionary key for `node.node_name`
        parent_key: dictionary key for `node.parent.node_name`
        attr_dict: node attributes mapped to dictionary key, key: node attributes, value: corresponding dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree
        skip_depth: number of initial depths to skip
        leaf_only: indicator to retrieve only information from leaf nodes

    Returns:
        Dictionary containing tree information
    """
    data_dict = {}

    def _recursive_append(_node: T) -> None:
        """Recursively iterate through node and its children to export to dictionary.

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
                    name_col=name_key,
                    parent_col=parent_key,
                )
                data_dict[_node.path_name] = data_child
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return data_dict


def tree_to_nested_dict(
    tree: T,
    name_key: str = "name",
    child_key: str = "children",
    attr_dict: dict[str, str] | None = None,
    all_attrs: bool = False,
    max_depth: int = 0,
) -> dict[str, Any]:
    """Export tree to nested dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node attribute names, and children as a nested recursive dictionary.

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.to_nested_dict(all_attrs=True)
        {'name': 'a', 'age': 90, 'children': [{'name': 'b', 'age': 65, 'children': [{'name': 'd', 'age': 40}, {'name': 'e', 'age': 35}]}, {'name': 'c', 'age': 60}]}

    Args:
        tree: tree to be exported
        name_key: dictionary key for `node.node_name`
        child_key: dictionary key for list of children
        attr_dict: node attributes mapped to dictionary key, key: node attributes, value: corresponding dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree

    Returns:
        Dictionary containing tree information
    """
    data_dict: dict[str, list[dict[str, Any]]] = {}

    def _recursive_append(_node: T, parent_dict: dict[str, Any]) -> None:
        """Recursively iterate through node and its children to export to nested dictionary.

        Args:
            _node: current node
            parent_dict: parent dictionary
        """
        if _node:
            if not max_depth or _node.depth <= max_depth:
                data_child = common.assemble_attributes(
                    _node, attr_dict, all_attrs, name_col=name_key
                )
                if child_key in parent_dict:
                    parent_dict[child_key].append(data_child)
                else:
                    parent_dict[child_key] = [data_child]

                for _child in _node.children:
                    _recursive_append(_child, data_child)

    _recursive_append(tree, data_dict)
    return data_dict[child_key][0]


def tree_to_nested_dict_key(
    tree: T,
    child_key: str | None = "children",
    attr_dict: dict[str, str] | None = None,
    all_attrs: bool = False,
    max_depth: int = 0,
) -> dict[str, Any]:
    """Export tree to nested dictionary, where the keys are node names.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node names, and children as node attributes and nested recursive dictionary.
    If child_key is None, the children key is nested recursive dictionary of node names (there will be no attributes).

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree = Tree(root)
        >>> tree.to_nested_dict_key(all_attrs=True)
        {'a': {'age': 90, 'children': {'b': {'age': 65, 'children': {'d': {'age': 40}, 'e': {'age': 35}}}, 'c': {'age': 60}}}}

        >>> tree.to_nested_dict_key(child_key=None)
        {'a': {'b': {'d': {}, 'e': {}}, 'c': {}}}

    Args:
        tree: tree to be exported
        child_key: dictionary key for children
        attr_dict: node attributes mapped to dictionary key, key: node attributes, value: corresponding dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree

    Returns:
        Dictionary containing tree information
    """
    data_dict: dict[str, dict[str, Any]] = {}

    def _recursive_append(_node: T, parent_dict: dict[str, Any]) -> None:
        """Recursively iterate through node and its children to export to nested dictionary.

        Args:
            _node: current node
            parent_dict: parent dictionary
        """
        if child_key is None:
            if attr_dict or all_attrs:
                raise ValueError(
                    "If child_key is None, no node attributes can be exported"
                )

        if _node:
            if not max_depth or _node.depth <= max_depth:
                data_child = common.assemble_attributes(_node, attr_dict, all_attrs)
                if child_key:
                    if child_key in parent_dict:
                        parent_dict[child_key][_node.node_name] = data_child
                    else:
                        parent_dict[child_key] = {_node.node_name: data_child}
                else:
                    parent_dict[_node.node_name] = data_child

                for _child in _node.children:
                    _recursive_append(_child, data_child)

    _recursive_append(tree, data_dict)
    return data_dict[child_key] if child_key else data_dict
