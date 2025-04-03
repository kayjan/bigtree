from typing import Any, Callable, Iterable, List, Tuple, TypeVar, Union

from bigtree.node import basenode, dagnode, node
from bigtree.utils import exceptions, iterators

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


T = TypeVar("T", bound=basenode.BaseNode)
NodeT = TypeVar("NodeT", bound=node.Node)
DAGNodeT = TypeVar("DAGNodeT", bound=dagnode.DAGNode)


def __check_result_count(
    result: Tuple[Any, ...], min_count: int, max_count: int
) -> None:
    """Check result fulfil min_count and max_count requirements.

    Args:
        result: result of search
        min_count: checks for minimum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count
        max_count: checks for maximum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count
    """
    if min_count and len(result) < min_count:
        raise exceptions.SearchError(
            f"Expected more than or equal to {min_count} element(s), found {len(result)} elements\n{result}"
        )
    if max_count and len(result) > max_count:
        raise exceptions.SearchError(
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
        tree: tree to search
        condition: function that takes in node as argument, returns node if condition evaluates to `True`
        max_depth: maximum depth to search for, based on the `depth` attribute
        min_count: checks for minimum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count
        max_count: checks for maximum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count

    Returns:
        Search results
    """
    result = tuple(
        iterators.preorder_iter(tree, filter_condition=condition, max_depth=max_depth)
    )
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
        bigtree.utils.exceptions.exceptions.SearchError: Expected less than or equal to 1 element(s), found 4 elements
        (Node(/a, age=90), Node(/a/b, age=65), Node(/a/c, age=60), Node(/a/c/d, age=40))

    Args:
        tree: tree to search
        condition: function that takes in node as argument, returns node if condition evaluates to `True`
        max_depth: maximum depth to search for, based on the `depth` attribute

    Returns:
        Search result
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
        tree: tree to search
        name: value to match for name attribute
        max_depth: maximum depth to search for, based on the `depth` attribute

    Returns:
        Search result
    """
    return find(tree, lambda _node: _node.node_name == name, max_depth)


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
        tree: tree to search
        name: value to match for name attribute
        max_depth: maximum depth to search for, based on the `depth` attribute

    Returns:
        Search results
    """
    return findall(tree, lambda _node: _node.node_name == name, max_depth)


def find_relative_path(tree: NodeT, path_name: str) -> NodeT:
    r"""
    Search tree for a single node matching relative path attribute.

    - Supports unix folder expression for relative path, i.e., '../../node_name'
    - Supports wildcards, i.e., '\*/node_name'
    - If path name starts with leading separator symbol, it will start at root node

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
        bigtree.utils.exceptions.exceptions.SearchError: Expected less than or equal to 1 element(s), found 2 elements
        (Node(/a/b, age=65), Node(/a/c, age=60))

    Args:
        tree: tree to search
        path_name: value to match (relative path) of path_name attribute

    Returns:
        Search result
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
    - If path name starts with leading separator symbol, it will start at root node

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
        tree: tree to search
        path_name: value to match (relative path) of path_name attribute
        min_count: checks for minimum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count
        max_count: checks for maximum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count

    Returns:
        Search results
    """
    sep = tree.sep
    if path_name.startswith(sep):
        path_list = path_name.rstrip(sep).lstrip(sep).split(sep)
        if path_list[0] not in (tree.root.node_name, "..", ".", "*"):
            raise ValueError(
                f"Path {path_name} does not match the root node name {tree.root.node_name}"
            )
        if path_list[0] == tree.root.node_name:
            path_list[0] = "."
        result = find_relative_paths(tree.root, sep.join(path_list))
        return result
    path_name = path_name.rstrip(sep).lstrip(sep)
    path_list = path_name.split(sep)
    wildcard_indicator = "*" in path_name
    resolved_nodes: List[NodeT] = []

    def resolve(_node: NodeT, path_idx: int) -> None:
        """Resolve node based on path name.

        Args:
            _node: current node
            path_idx: current index in path_list
        """
        if path_idx == len(path_list):
            resolved_nodes.append(_node)
        else:
            path_component = path_list[path_idx]
            if path_component == ".":
                resolve(_node, path_idx + 1)
            elif path_component == "..":
                if _node.is_root:
                    raise exceptions.SearchError(
                        "Invalid path name. Path goes beyond root node."
                    )
                resolve(_node.parent, path_idx + 1)
            elif path_component == "*":
                for child in _node.children:
                    resolve(child, path_idx + 1)
            else:
                child_node = find_child_by_name(_node, path_component)
                if not child_node:
                    if not wildcard_indicator:
                        raise exceptions.SearchError(
                            f"Invalid path name. Node {path_component} cannot be found."
                        )
                else:
                    resolve(child_node, path_idx + 1)

    resolve(tree, 0)
    result = tuple(resolved_nodes)
    __check_result_count(result, min_count, max_count)
    return result


def find_full_path(tree: NodeT, path_name: str) -> NodeT:
    """
    Search tree for a single node matching path attribute.

    - Path name can be with or without leading tree path separator symbol
    - Path name must be full path, works similar to `find_path` but faster

    Examples:
        >>> from bigtree import Node, find_full_path
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=c)
        >>> find_full_path(root, "/a/c/d")
        Node(/a/c/d, age=40)

    Args:
        tree: tree to search
        path_name: value to match (full path) of path_name attribute

    Returns:
        Search result
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

    - Path name can be with or without leading tree path separator symbol
    - Path name can be full path or partial path (trailing part of path) or node name

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
        tree: tree to search
        path_name: value to match (full path) or trailing part (partial path) of path_name attribute

    Returns:
        Search result
    """
    path_name = path_name.rstrip(tree.sep)
    return find(tree, lambda _node: _node.path_name.endswith(path_name))


def find_paths(tree: NodeT, path_name: str) -> Iterable[NodeT]:
    """
    Search tree for one or more nodes matching path attribute.

    - Path name can be with or without leading tree path separator symbol
    - Path name can be partial path (trailing part of path) or node name

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
        tree: tree to search
        path_name: value to match (full path) or trailing part (partial path) of path_name attribute

    Returns:
        Search results
    """
    path_name = path_name.rstrip(tree.sep)
    return findall(tree, lambda _node: _node.path_name.endswith(path_name))


def find_attr(
    tree: basenode.BaseNode, attr_name: str, attr_value: Any, max_depth: int = 0
) -> basenode.BaseNode:
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
        tree: tree to search
        attr_name: attribute name to perform matching
        attr_value: value to match for attr_name attribute
        max_depth: maximum depth to search for, based on the `depth` attribute

    Returns:
        Search result
    """
    return find(
        tree,
        lambda _node: bool(_node.get_attr(attr_name) == attr_value),
        max_depth,
    )


def find_attrs(
    tree: basenode.BaseNode, attr_name: str, attr_value: Any, max_depth: int = 0
) -> Iterable[basenode.BaseNode]:
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
        tree: tree to search
        attr_name: attribute name to perform matching
        attr_value: value to match for attr_name attribute
        max_depth: maximum depth to search for, based on the `depth` attribute

    Returns:
        Search results
    """
    return findall(
        tree,
        lambda _node: bool(_node.get_attr(attr_name) == attr_value),
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
        tree: tree to search for its children
        condition: function that takes in node as argument, returns node if condition evaluates to `True`
        min_count: checks for minimum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count
        max_count: checks for maximum number of occurrences, raise exceptions.SearchError if the number of results do
            not meet min_count

    Returns:
        Search results
    """
    result = tuple([_node for _node in tree.children if _node and condition(_node)])
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
        tree: tree to search for its child
        condition: function that takes in node as argument, returns node if condition evaluates to `True`

    Returns:
        Search result
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
        tree: tree to search, parent node
        name: value to match for name attribute, child node

    Returns:
        Search result
    """
    return find_child(tree, lambda _node: _node.node_name == name)
