from typing import Any, Callable, Iterable, Tuple, TypeVar

from bigtree.node.basenode import BaseNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import SearchError
from bigtree.utils.iterators import preorder_iter

__all__ = [
    "findall",
    "find",
    "find_name",
    "find_names",
    "find_full_path",
    "find_path",
    "find_paths",
    "find_attr",
    "find_attrs",
    "find_children",
    "find_child",
    "find_child_by_name",
]


T = TypeVar("T", bound=BaseNode)


def findall(
    tree: T,
    condition: Callable[[T], bool],
    max_depth: int = 0,
    min_count: int = 0,
    max_count: int = 0,
) -> Tuple[T, ...]:
    """
    Search tree for nodes matching condition (callable function).

    >>> from bigtree import Node, findall
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> findall(root, lambda node: node.age > 62)
    (Node(/a, age=90), Node(/a/b, age=65))

    Args:
        tree (BaseNode): tree to search
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None
        min_count (int): checks for minimum number of occurrence,
            raise SearchError if number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrence,
            raise SearchError if number of results do not meet min_count, defaults to None

    Returns:
        (Tuple[BaseNode, ...])
    """
    result = tuple(preorder_iter(tree, filter_condition=condition, max_depth=max_depth))
    if min_count and len(result) < min_count:
        raise SearchError(
            f"Expected more than {min_count} element(s), found {len(result)} elements\n{result}"
        )
    if max_count and len(result) > max_count:
        raise SearchError(
            f"Expected less than {max_count} element(s), found {len(result)} elements\n{result}"
        )
    return result


def find(tree: T, condition: Callable[[T], bool], max_depth: int = 0) -> T:
    """
    Search tree for *single node* matching condition (callable function).

    >>> from bigtree import Node, find
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find(root, lambda node: node.age == 65)
    Node(/a/b, age=65)
    >>> find(root, lambda node: node.age > 5)
    Traceback (most recent call last):
        ...
    bigtree.utils.exceptions.SearchError: Expected less than 1 element(s), found 4 elements
    (Node(/a, age=90), Node(/a/b, age=65), Node(/a/c, age=60), Node(/a/c/d, age=40))

    Args:
        tree (BaseNode): tree to search
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None

    Returns:
        (BaseNode)
    """
    result = findall(tree, condition, max_depth, max_count=1)
    if result:
        return result[0]


def find_name(tree: Node, name: str, max_depth: int = 0) -> Node:
    """
    Search tree for single node matching name attribute.

    >>> from bigtree import Node, find_name
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_name(root, "c")
    Node(/a/c, age=60)

    Args:
        tree (Node): tree to search
        name (str): value to match for name attribute
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None

    Returns:
        (Node)
    """
    return find(tree, lambda node: node.node_name == name, max_depth)


def find_names(tree: Node, name: str, max_depth: int = 0) -> Iterable[Node]:
    """
    Search tree for multiple node(s) matching name attribute.

    >>> from bigtree import Node, find_names
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("b", age=40, parent=c)
    >>> find_names(root, "c")
    (Node(/a/c, age=60),)
    >>> find_names(root, "b")
    (Node(/a/b, age=65), Node(/a/c/b, age=40))

    Args:
        tree (Node): tree to search
        name (str): value to match for name attribute
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None

    Returns:
        (Iterable[Node])
    """
    return findall(tree, lambda node: node.node_name == name, max_depth)


def find_full_path(tree: Node, path_name: str) -> Node:
    """
    Search tree for single node matching path attribute.
      - Path name can be with or without leading tree path separator symbol.
      - Path name must be full path, works similar to `find_path` but faster.

    >>> from bigtree import Node, find_full_path
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_full_path(root, "/a/c/d")
    Node(/a/c/d, age=40)

    Args:
        tree (Node): tree to search
        path_name (str): value to match (full path) of path_name attribute

    Returns:
        (Node)
    """
    path_name = path_name.rstrip(tree.sep).lstrip(tree.sep)
    path_list = path_name.split(tree.sep)
    if path_list[0] != tree.root.node_name:
        raise ValueError(
            f"Path {path_name} does not match the root node name {tree.root.node_name}"
        )
    parent_node = tree.root
    child_node = parent_node
    for child_name in path_list[1:]:
        child_node = find_child_by_name(parent_node, child_name)
        if not child_node:
            break
        parent_node = child_node
    return child_node


def find_path(tree: Node, path_name: str) -> Node:
    """
    Search tree for single node matching path attribute.
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be full path or partial path (trailing part of path) or node name.

    >>> from bigtree import Node, find_path
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_path(root, "c")
    Node(/a/c, age=60)
    >>> find_path(root, "/c")
    Node(/a/c, age=60)

    Args:
        tree (Node): tree to search
        path_name (str): value to match (full path) or trailing part (partial path) of path_name attribute

    Returns:
        (Node)
    """
    path_name = path_name.rstrip(tree.sep)
    return find(tree, lambda node: node.path_name.endswith(path_name))


def find_paths(tree: Node, path_name: str) -> Tuple[Node, ...]:
    """
    Search tree for multiple nodes matching path attribute.
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be partial path (trailing part of path) or node name.

    >>> from bigtree import Node, find_paths
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("c", age=40, parent=c)
    >>> find_paths(root, "/a/c")
    (Node(/a/c, age=60),)
    >>> find_paths(root, "/c")
    (Node(/a/c, age=60), Node(/a/c/c, age=40))

    Args:
        tree (Node): tree to search
        path_name (str): value to match (full path) or trailing part (partial path) of path_name attribute

    Returns:
        (Tuple[Node, ...])
    """
    path_name = path_name.rstrip(tree.sep)
    return findall(tree, lambda node: node.path_name.endswith(path_name))


def find_attr(
    tree: BaseNode, attr_name: str, attr_value: Any, max_depth: int = 0
) -> BaseNode:
    """
    Search tree for single node matching custom attribute.

    >>> from bigtree import Node, find_attr
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_attr(root, "age", 65)
    Node(/a/b, age=65)

    Args:
        tree (BaseNode): tree to search
        attr_name (str): attribute name to perform matching
        attr_value (Any): value to match for attr_name attribute
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None

    Returns:
        (BaseNode)
    """
    return find(
        tree,
        lambda node: bool(node.get_attr(attr_name) == attr_value),
        max_depth,
    )


def find_attrs(
    tree: BaseNode, attr_name: str, attr_value: Any, max_depth: int = 0
) -> Tuple[BaseNode, ...]:
    """
    Search tree for node(s) matching custom attribute.

    >>> from bigtree import Node, find_attrs
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=65, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_attrs(root, "age", 65)
    (Node(/a/b, age=65), Node(/a/c, age=65))

    Args:
        tree (BaseNode): tree to search
        attr_name (str): attribute name to perform matching
        attr_value (Any): value to match for attr_name attribute
        max_depth (int): maximum depth to search for, based on `depth` attribute, defaults to None

    Returns:
        (Tuple[BaseNode, ...])
    """
    return findall(
        tree,
        lambda node: bool(node.get_attr(attr_name) == attr_value),
        max_depth,
    )


def find_children(
    tree: T,
    condition: Callable[[T], bool],
    min_count: int = 0,
    max_count: int = 0,
) -> Tuple[T, ...]:
    """
    Search children for nodes matching condition (callable function).

    >>> from bigtree import Node, find_children
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_children(root, lambda node: node.age > 30)
    (Node(/a/b, age=65), Node(/a/c, age=60))

    Args:
        tree (BaseNode): tree to search for its children
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`
        min_count (int): checks for minimum number of occurrence,
            raise SearchError if number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrence,
            raise SearchError if number of results do not meet min_count, defaults to None

    Returns:
        (BaseNode)
    """
    result = tuple([node for node in tree.children if node and condition(node)])
    if min_count and len(result) < min_count:
        raise SearchError(
            f"Expected more than {min_count} element(s), found {len(result)} elements\n{result}"
        )
    if max_count and len(result) > max_count:
        raise SearchError(
            f"Expected less than {max_count} element(s), found {len(result)} elements\n{result}"
        )
    return result


def find_child(
    tree: T,
    condition: Callable[[T], bool],
) -> T:
    """
    Search children for *single node* matching condition (callable function).

    >>> from bigtree import Node, find_child
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_child(root, lambda node: node.age > 62)
    Node(/a/b, age=65)

    Args:
        tree (BaseNode): tree to search for its child
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`

    Returns:
        (BaseNode)
    """
    result = find_children(tree, condition, max_count=1)
    if result:
        return result[0]


def find_child_by_name(tree: Node, name: str) -> Node:
    """
    Search tree for single node matching name attribute.

    >>> from bigtree import Node, find_child_by_name
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65, parent=root)
    >>> c = Node("c", age=60, parent=root)
    >>> d = Node("d", age=40, parent=c)
    >>> find_child_by_name(root, "c")
    Node(/a/c, age=60)
    >>> find_child_by_name(c, "d")
    Node(/a/c/d, age=40)

    Args:
        tree (Node): tree to search, parent node
        name (str): value to match for name attribute, child node

    Returns:
        (Node)
    """
    return find_child(tree, lambda node: node.node_name == name)
