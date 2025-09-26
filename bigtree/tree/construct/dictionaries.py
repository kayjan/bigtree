from __future__ import annotations

from typing import Any, Mapping, TypeVar

from bigtree.node import node
from bigtree.tree.construct.strings import add_path_to_tree
from bigtree.utils import assertions, common

__all__ = [
    "add_dict_to_tree_by_path",
    "add_dict_to_tree_by_name",
    "dict_to_tree",
    "nested_dict_to_tree",
    "nested_dict_key_to_tree",
]

T = TypeVar("T", bound=node.Node)


def add_dict_to_tree_by_path(
    tree: T,
    path_attrs: Mapping[str, Mapping[str, Any]],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree. Adds to existing tree from nested dictionary,
    ``key``: path, ``value``: dict of attribute name and attribute value.

    All attributes in `path_attrs` will be added to the tree, including attributes with null values.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")
    - Path separator `sep` is for the input `path` and can differ from existing tree

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> from bigtree import Node, Tree
        >>> tree = Tree(Node("a"))
        >>> path_dict = {
        ...     "a": {"age": 90},
        ...     "a/b": {"age": 65},
        ...     "a/c": {"age": 60},
        ...     "a/b/d": {"age": 40},
        ...     "a/b/e": {"age": 35},
        ...     "a/c/f": {"age": 38},
        ...     "a/b/e/g": {"age": 10},
        ...     "a/b/e/h": {"age": 6},
        ... }
        >>> tree.add_dict_by_path(path_dict)
        >>> tree.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

    Args:
        tree: existing tree
        path_attrs: node path and attribute information, key: node path, value: dict of node attribute name and
            attribute value
        sep: path separator for input `path_attrs`
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed

    Returns:
        Node
    """
    assertions.assert_length_not_empty(path_attrs, "Dictionary", "path_attrs")

    root_node = tree.root

    for path, node_attrs in path_attrs.items():
        add_path_to_tree(
            root_node,
            path,
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_dict_to_tree_by_name(tree: T, name_attrs: Mapping[str, Mapping[str, Any]]) -> T:
    """Add attributes to existing tree *in-place*. Adds to existing tree from nested dictionary, ``key``: name,
    ``value``: dict of attribute name and attribute value.

    All attributes in `name_attrs` will be added to the tree, including attributes with null values.

    Input dictionary keys that are not existing node names will be ignored. Note that if multiple nodes have the same
    name, attributes will be added to all nodes sharing the same name.

    Examples:
        >>> from bigtree import Node, Tree
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> tree = Tree(root)
        >>> name_dict = {
        ...     "a": {"age": 90},
        ...     "b": {"age": 65},
        ... }
        >>> tree.add_dict_by_name(name_dict)
        >>> tree.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]

    Args:
        tree: existing tree
        name_attrs: node name and attribute information, key: node name, value: dict of node attribute name and
            attribute value

    Returns:
        Node
    """
    from bigtree.tree.search import findall

    assertions.assert_length_not_empty(name_attrs, "Dictionary", "name_attrs")

    attr_dict_names = set(name_attrs.keys())

    for _node in findall(tree, lambda _node1: _node1.node_name in attr_dict_names):
        node_attrs = common.filter_attributes(
            name_attrs[_node.node_name], omit_keys=["name"], omit_null_values=False
        )
        _node.set_attrs(node_attrs)

    return tree


def dict_to_tree(
    path_attrs: Mapping[str, Any],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from nested dictionary using path, ``key``: path, ``value``: dict of attribute name and attribute
    value.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    All attributes in `path_attrs` will be added to the tree, including attributes with null values.

    Examples:
        >>> from bigtree import Tree
        >>> path_dict = {
        ...     "a": {"age": 90},
        ...     "a/b": {"age": 65},
        ...     "a/c": {"age": 60},
        ...     "a/b/d": {"age": 40},
        ...     "a/b/e": {"age": 35},
        ...     "a/c/f": {"age": 38},
        ...     "a/b/e/g": {"age": 10},
        ...     "a/b/e/h": {"age": 6},
        ... }
        >>> tree = Tree.from_dict(path_dict)
        >>> tree.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        path_attrs: node path and attribute information, key: node path, value: dict of node attribute name and
            attribute value
        sep: path separator of input `path_attrs` and created tree
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length_not_empty(path_attrs, "Dictionary", "path_attrs")

    # Initial tree
    root_name = list(path_attrs.keys())[0].lstrip(sep).rstrip(sep).split(sep)[0]
    root_node_attrs = dict(
        path_attrs.get(root_name, {})
        or path_attrs.get(sep + root_name, {})
        or path_attrs.get(root_name + sep, {})
        or path_attrs.get(sep + root_name + sep, {})
    )
    root_node_attrs = common.filter_attributes(
        root_node_attrs, omit_keys=["name"], omit_null_values=False
    )
    root_node = node_type(
        name=root_name,
        sep=sep,
        **root_node_attrs,
    )

    # Convert dictionary to dataframe
    for node_path, node_attrs in path_attrs.items():
        node_attrs = common.filter_attributes(
            node_attrs, omit_keys=["name"], omit_null_values=False
        )
        add_path_to_tree(
            root_node,
            node_path,
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def nested_dict_to_tree(
    node_attrs: Mapping[str, Any],
    name_key: str = "name",
    child_key: str = "children",
    node_type: type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from nested recursive dictionary.

    - ``key``: `name_key`, `child_key`, or any attributes key
    - ``value`` of `name_key`: node name
    - ``value`` of `child_key`: list of dict containing `name_key` and `child_key` (recursive)

    Examples:
        >>> from bigtree import Tree
        >>> nested_dict = {
        ...     "name": "a",
        ...     "age": 90,
        ...     "children": [
        ...         {"name": "b",
        ...          "age": 65,
        ...          "children": [
        ...              {"name": "d", "age": 40},
        ...              {"name": "e", "age": 35, "children": [
        ...                  {"name": "g", "age": 10},
        ...              ]},
        ...          ]},
        ...     ],
        ... }
        >>> tree = Tree.from_nested_dict(nested_dict)
        >>> tree.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]
            ├── d [age=40]
            └── e [age=35]
                └── g [age=10]

    Args:
        node_attrs: node, children, and node attribute information,
            key: `name_key` and `child_key`
            value of `name_key` (str): node name
            value of `child_key` (list[Mapping[str, Any]]): list of dict containing `name_key` and `child_key` (recursive)
        name_key: key of node name, value is type str
        child_key: key of child list, value is type list
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length_not_empty(node_attrs, "Dictionary", "node_attrs")

    def _recursive_add_child(
        child_dict: Mapping[str, Any], parent_node: T | None = None
    ) -> T:
        """Recursively add child to tree, given child attributes and parent node.

        Args:
            child_dict: child to be added to tree, from dictionary
            parent_node: parent node to be assigned to child node

        Returns:
            Node
        """
        child_dict = dict(child_dict)
        node_name = child_dict.pop(name_key)
        node_children = child_dict.pop(child_key, [])
        if not isinstance(node_children, list):
            raise TypeError(
                f"child_key {child_key} should be List type, received {node_children}"
            )
        root = node_type(node_name, parent=parent_node, **child_dict)
        for _child in node_children:
            _recursive_add_child(_child, parent_node=root)
        return root

    root_node = _recursive_add_child(node_attrs)
    return root_node


def nested_dict_key_to_tree(
    node_attrs: Mapping[str, Mapping[str, Any]],
    child_key: str | None = "children",
    node_type: type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from nested recursive dictionary, where the keys are node names.

    If child_key is a string

    - ``key``: node name
    - ``value``: dict of node attributes and node children (recursive)

    Value dictionary

    - ``key`` that is not ``child_key`` has node attribute as value
    - ``key`` that is ``child_key`` has dictionary of node children as value (recursive)

    ---

    If child_key is None

    - ``key``: node name
    - ``value``: dict of node children (recursive), there are no node attributes

    Value dictionary consist of ``key`` that is node names of children

    Examples:
        >>> from bigtree import Tree
        >>> nested_dict = {
        ...     "a": {
        ...         "age": 90,
        ...         "children": {
        ...             "b": {
        ...                 "age": 65,
        ...                 "children": {
        ...                     "d": {"age": 40},
        ...                     "e": {
        ...                         "age": 35,
        ...                         "children": {"g": {"age": 10}},
        ...                     },
        ...                 },
        ...             },
        ...         },
        ...     }
        ... }
        >>> tree = Tree.from_nested_dict_key(nested_dict)
        >>> tree.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]
            ├── d [age=40]
            └── e [age=35]
                └── g [age=10]

        >>> from bigtree import nested_dict_key_to_tree
        >>> nested_dict = {
        ...     "a": {
        ...         "b": {
        ...             "d": {},
        ...             "e": {"g": {}},
        ...         },
        ...     }
        ... }
        >>> tree = Tree.from_nested_dict_key(nested_dict, child_key=None)
        >>> tree.show()
        a
        └── b
            ├── d
            └── e
                └── g

    Args:
        node_attrs: node, children, and node attribute information,
            key: node name
            value: dictionary of node attributes and node children
        child_key: key of child dict, value is type dict
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length(node_attrs, 1, "Dictionary", "node_attrs")

    def _recursive_add_child(
        child_name: str, child_dict: Mapping[str, Any], parent_node: T | None = None
    ) -> T:
        """Recursively add child to tree, given child attributes and parent node.

        Args:
            child_name: child name to be added to tree
            child_dict: child to be added to tree, from dictionary
            parent_node: parent node to be assigned to child node

        Returns:
            Node
        """
        if child_key:
            child_dict = dict(child_dict)
            node_children = child_dict.pop(child_key, {})
        else:
            node_children = child_dict
            child_dict = {}
        if not isinstance(node_children, Mapping):
            raise TypeError(
                f"child_key {child_key} should be Dict type, received {node_children}"
            )
        root = node_type(child_name, parent=parent_node, **child_dict)
        for _child_name in node_children:
            _recursive_add_child(
                _child_name, node_children[_child_name], parent_node=root
            )
        return root

    root_node_name = list(node_attrs.keys())[0]
    root_node = _recursive_add_child(root_node_name, node_attrs[root_node_name])
    return root_node
