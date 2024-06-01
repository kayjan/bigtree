from typing import Any, Callable, Iterable, List, Tuple, TypeVar, Union

from bigtree.node.basenode import BaseNode
from bigtree.node.dagnode import DAGNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import SearchError
from bigtree.utils.iterators import preorder_iter

__all__ = [
    "findall",
    "find",
    "find_name",
    "find_names",
    "find_relative_path",
    "find_relative_paths",
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
NodeT = TypeVar("NodeT", bound=Node)
DAGNodeT = TypeVar("DAGNodeT", bound=DAGNode)


def __check_result_count(
    result: Tuple[Any, ...], min_count: int, max_count: int
) -> None:
    """Check result fulfil min_count and max_count requirements

    Args:
        result (Tuple[Any]): result of search
        min_count (int): checks for minimum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None
    """
    if min_count and len(result) < min_count:
        raise SearchError(
            f"Expected more than or equal to {min_count} element(s), found {len(result)} elements\n{result}"
        )
    if max_count and len(result) > max_count:
        raise SearchError(
            f"Expected less than or equal to {max_count} element(s), found {len(result)} elements\n{result}"
        )


def findall(
    tree: T,
    condition: Callable[[T], bool],
    max_depth: int = 0,
    min_count: int = 0,
    max_count: int = 0,
) -> Tuple[T, ...]:
    """
    Search tree for one or more nodes matching condition (callable function).

    Examples:
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
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None
        min_count (int): checks for minimum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None

    Returns:
        (Tuple[BaseNode, ...])
    """
    result = tuple(preorder_iter(tree, filter_condition=condition, max_depth=max_depth))
    __check_result_count(result, min_count, max_count)
    return result


def find(tree: T, condition: Callable[[T], bool], max_depth: int = 0) -> T:
    """
    Search tree for a single node matching condition (callable function).

    Examples:
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
        bigtree.utils.exceptions.SearchError: Expected less than or equal to 1 element(s), found 4 elements
        (Node(/a, age=90), Node(/a/b, age=65), Node(/a/c, age=60), Node(/a/c/d, age=40))

    Args:
        tree (BaseNode): tree to search
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None

    Returns:
        (BaseNode)
    """
    result = findall(tree, condition, max_depth, max_count=1)
    if result:
        return result[0]


def find_name(tree: NodeT, name: str, max_depth: int = 0) -> NodeT:
    """
    Search tree for a single node matching name attribute.

    Examples:
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
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None

    Returns:
        (Node)
    """
    return find(tree, lambda node: node.node_name == name, max_depth)


def find_names(tree: NodeT, name: str, max_depth: int = 0) -> Iterable[NodeT]:
    """
    Search tree for one or more nodes matching name attribute.

    Examples:
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
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None

    Returns:
        (Iterable[Node])
    """
    return findall(tree, lambda node: node.node_name == name, max_depth)


def find_relative_path(tree: NodeT, path_name: str) -> NodeT:
    r"""
    Search tree for a single node matching relative path attribute.

    - Supports unix folder expression for relative path, i.e., '../../node_name'
    - Supports wildcards, i.e., '\*/node_name'
    - If path name starts with leading separator symbol, it will start at root node.

    Examples:
        >>> from bigtree import Node, find_relative_path
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=c)
        >>> find_relative_path(d, "..")
        Node(/a/c, age=60)
        >>> find_relative_path(d, "../../b")
        Node(/a/b, age=65)
        >>> find_relative_path(d, "../../*")
        Traceback (most recent call last):
            ...
        bigtree.utils.exceptions.SearchError: Expected less than or equal to 1 element(s), found 2 elements
        (Node(/a/b, age=65), Node(/a/c, age=60))

    Args:
        tree (Node): tree to search
        path_name (str): value to match (relative path) of path_name attribute

    Returns:
        (Node)
    """
    result = find_relative_paths(tree, path_name, max_count=1)

    if result:
        return result[0]


def find_relative_paths(
    tree: NodeT,
    path_name: str,
    min_count: int = 0,
    max_count: int = 0,
) -> Tuple[NodeT, ...]:
    r"""
    Search tree for one or more nodes matching relative path attribute.

    - Supports unix folder expression for relative path, i.e., '../../node_name'
    - Supports wildcards, i.e., '\*/node_name'
    - If path name starts with leading separator symbol, it will start at root node.

    Examples:
        >>> from bigtree import Node, find_relative_paths
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=c)
        >>> find_relative_paths(d, "..")
        (Node(/a/c, age=60),)
        >>> find_relative_paths(d, "../../b")
        (Node(/a/b, age=65),)
        >>> find_relative_paths(d, "../../*")
        (Node(/a/b, age=65), Node(/a/c, age=60))

    Args:
        tree (Node): tree to search
        path_name (str): value to match (relative path) of path_name attribute
        min_count (int): checks for minimum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None

    Returns:
        (Tuple[Node, ...])
    """
    sep = tree.sep
    if path_name.startswith(sep):
        resolved_node = find_full_path(tree, path_name)
        return (resolved_node,)
    path_name = path_name.rstrip(sep).lstrip(sep)
    path_list = path_name.split(sep)
    wildcard_indicator = "*" in path_name
    resolved_nodes: List[NodeT] = []

    def resolve(node: NodeT, path_idx: int) -> None:
        """Resolve node based on path name

        Args:
            node (Node): current node
            path_idx (int): current index in path_list
        """
        if path_idx == len(path_list):
            resolved_nodes.append(node)
        else:
            path_component = path_list[path_idx]
            if path_component == ".":
                resolve(node, path_idx + 1)
            elif path_component == "..":
                if node.is_root:
                    raise SearchError("Invalid path name. Path goes beyond root node.")
                resolve(node.parent, path_idx + 1)
            elif path_component == "*":
                for child in node.children:
                    resolve(child, path_idx + 1)
            else:
                node = find_child_by_name(node, path_component)
                if not node:
                    if not wildcard_indicator:
                        raise SearchError(
                            f"Invalid path name. Node {path_component} cannot be found."
                        )
                else:
                    resolve(node, path_idx + 1)

    resolve(tree, 0)
    result = tuple(resolved_nodes)
    __check_result_count(result, min_count, max_count)
    return result


def find_full_path(tree: NodeT, path_name: str) -> NodeT:
    """
    Search tree for a single node matching path attribute.

    - Path name can be with or without leading tree path separator symbol.
    - Path name must be full path, works similar to `find_path` but faster.

    Examples:
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
    sep = tree.sep
    path_list = path_name.rstrip(sep).lstrip(sep).split(sep)
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


def find_path(tree: NodeT, path_name: str) -> NodeT:
    """
    Search tree for a single node matching path attribute.

    - Path name can be with or without leading tree path separator symbol.
    - Path name can be full path or partial path (trailing part of path) or node name.

    Examples:
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


def find_paths(tree: NodeT, path_name: str) -> Iterable[NodeT]:
    """
    Search tree for one or more nodes matching path attribute.

    - Path name can be with or without leading tree path separator symbol.
    - Path name can be partial path (trailing part of path) or node name.

    Examples:
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
        (Iterable[Node])
    """
    path_name = path_name.rstrip(tree.sep)
    return findall(tree, lambda node: node.path_name.endswith(path_name))


def find_attr(
    tree: BaseNode, attr_name: str, attr_value: Any, max_depth: int = 0
) -> BaseNode:
    """
    Search tree for a single node matching custom attribute.

    Examples:
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
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None

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
) -> Iterable[BaseNode]:
    """
    Search tree for one or more nodes matching custom attribute.

    Examples:
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
        max_depth (int): maximum depth to search for, based on the `depth` attribute, defaults to None

    Returns:
        (Iterable[BaseNode])
    """
    return findall(
        tree,
        lambda node: bool(node.get_attr(attr_name) == attr_value),
        max_depth,
    )


def find_children(
    tree: Union[T, DAGNodeT],
    condition: Callable[[Union[T, DAGNodeT]], bool],
    min_count: int = 0,
    max_count: int = 0,
) -> Tuple[Union[T, DAGNodeT], ...]:
    """
    Search children for one or more nodes matching condition (callable function).

    Examples:
        >>> from bigtree import Node, find_children
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=c)
        >>> find_children(root, lambda node: node.age > 30)
        (Node(/a/b, age=65), Node(/a/c, age=60))

    Args:
        tree (BaseNode/DAGNode): tree to search for its children
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`
        min_count (int): checks for minimum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None
        max_count (int): checks for maximum number of occurrences,
            raise SearchError if the number of results do not meet min_count, defaults to None

    Returns:
        (Tuple[Union[BaseNode, DAGNode], ...])
    """
    result = tuple([node for node in tree.children if node and condition(node)])
    __check_result_count(result, min_count, max_count)
    return result


def find_child(
    tree: Union[T, DAGNodeT],
    condition: Callable[[Union[T, DAGNodeT]], bool],
) -> Union[T, DAGNodeT]:
    """
    Search children for a single node matching condition (callable function).

    Examples:
        >>> from bigtree import Node, find_child
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=c)
        >>> find_child(root, lambda node: node.age > 62)
        Node(/a/b, age=65)

    Args:
        tree (BaseNode/DAGNode): tree to search for its child
        condition (Callable): function that takes in node as argument, returns node if condition evaluates to `True`

    Returns:
        (BaseNode/DAGNode)
    """
    result = find_children(tree, condition, max_count=1)
    if result:
        return result[0]


def find_child_by_name(
    tree: Union[NodeT, DAGNodeT], name: str
) -> Union[NodeT, DAGNodeT]:
    """
    Search tree for a single node matching name attribute.

    Examples:
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
        tree (Node/DAGNode): tree to search, parent node
        name (str): value to match for name attribute, child node

    Returns:
        (Node/DAGNode)
    """
    return find_child(tree, lambda node: node.node_name == name)
