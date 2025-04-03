from __future__ import annotations

from typing import Any, Dict, List, TypeVar

from bigtree.node import node

__all__ = [
    "tree_to_dict",
    "tree_to_nested_dict",
]

T = TypeVar("T", bound=node.Node)


def tree_to_dict(
    tree: T,
    name_key: str = "name",
    parent_key: str = "",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
    skip_depth: int = 0,
    leaf_only: bool = False,
) -> Dict[str, Any]:
    """Export tree to dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node path, and node attributes as a nested dictionary.

    Examples:
        >>> from bigtree import Node, tree_to_dict
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree_to_dict(root, name_key="name", parent_key="parent", attr_dict={"age": "person age"})
        {'/a': {'name': 'a', 'parent': None, 'person age': 90}, '/a/b': {'name': 'b', 'parent': 'a', 'person age': 65}, '/a/b/d': {'name': 'd', 'parent': 'b', 'person age': 40}, '/a/b/e': {'name': 'e', 'parent': 'b', 'person age': 35}, '/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

        For a subset of a tree

        >>> tree_to_dict(c, name_key="name", parent_key="parent", attr_dict={"age": "person age"})
        {'/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}}

    Args:
        tree: tree to be exported
        name_key: dictionary key for `node.node_name`
        parent_key: dictionary key for `node.parent.node_name`
        attr_dict: dictionary mapping node attributes to dictionary key, key: node attributes, value: corresponding
            dictionary key
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
                data_child: Dict[str, Any] = {}
                if name_key:
                    data_child[name_key] = _node.node_name
                if parent_key:
                    parent_name = None
                    if _node.parent:
                        parent_name = _node.parent.node_name
                    data_child[parent_key] = parent_name
                if all_attrs:
                    data_child.update(
                        dict(
                            _node.describe(
                                exclude_attributes=["name"], exclude_prefix="_"
                            )
                        )
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = _node.get_attr(k)
                data_dict[_node.path_name] = data_child
            for _child in _node.children:
                _recursive_append(_child)

    _recursive_append(tree)
    return data_dict


def tree_to_nested_dict(
    tree: T,
    name_key: str = "name",
    child_key: str = "children",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
    max_depth: int = 0,
) -> Dict[str, Any]:
    """Export tree to nested dictionary.

    All descendants from `tree` will be exported, `tree` can be the root node or child node of tree.

    Exported dictionary will have key as node attribute names, and children as a nested recursive dictionary.

    Examples:
        >>> from bigtree import Node, tree_to_nested_dict
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> tree_to_nested_dict(root, all_attrs=True)
        {'name': 'a', 'age': 90, 'children': [{'name': 'b', 'age': 65, 'children': [{'name': 'd', 'age': 40}, {'name': 'e', 'age': 35}]}, {'name': 'c', 'age': 60}]}

    Args:
        tree: tree to be exported
        name_key: dictionary key for `node.node_name`
        child_key: dictionary key for list of children
        attr_dict: dictionary mapping node attributes to dictionary key, key: node attributes, value: corresponding
            dictionary key
        all_attrs: indicator whether to retrieve all ``Node`` attributes, overrides `attr_dict`
        max_depth: maximum depth to export tree

    Returns:
        Dictionary containing tree information
    """
    data_dict: Dict[str, List[Dict[str, Any]]] = {}

    def _recursive_append(_node: T, parent_dict: Dict[str, Any]) -> None:
        """Recursively iterate through node and its children to export to nested dictionary.

        Args:
            _node: current node
            parent_dict: parent dictionary
        """
        if _node:
            if not max_depth or _node.depth <= max_depth:
                data_child = {name_key: _node.node_name}
                if all_attrs:
                    data_child.update(
                        dict(
                            _node.describe(
                                exclude_attributes=["name"], exclude_prefix="_"
                            )
                        )
                    )
                else:
                    for k, v in attr_dict.items():
                        data_child[v] = _node.get_attr(k)
                if child_key in parent_dict:
                    parent_dict[child_key].append(data_child)
                else:
                    parent_dict[child_key] = [data_child]

                for _child in _node.children:
                    _recursive_append(_child, data_child)

    _recursive_append(tree, data_dict)
    return data_dict[child_key][0]
