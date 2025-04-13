from typing import Iterable, List, TypeVar

from bigtree.node import basenode
from bigtree.utils import exceptions

__all__ = [
    "get_common_ancestors",
    "get_path",
]

T = TypeVar("T", bound=basenode.BaseNode)


def get_common_ancestors(nodes: List[T]) -> List[T]:
    """Get common ancestors between different branches of the same tree.

    Args:
        nodes: branches belonging to the same tree

    Returns:
        Common ancestors between the different branches of the same tree
    """
    root = nodes[0].root
    common_ancestors = [nodes[0]] + list(nodes[0].ancestors)
    for _node in nodes:
        if not isinstance(_node, basenode.BaseNode):
            raise TypeError(
                f"Expect node to be BaseNode type, received input type {type(_node)}"
            )
        if root != _node.root:
            raise exceptions.TreeError(
                f"Nodes are not from the same tree. Check {root} and {_node}"
            )
        ancestors = set([_node] + list(_node.ancestors))
        common_ancestors = [_node for _node in common_ancestors if _node in ancestors]
    return common_ancestors


def get_path(from_node: T, to_node: T) -> Iterable[T]:
    """Get path from origin node to destination node from the same tree. Path is inclusive of origin and destination
    nodes.

    Examples:
        >>> from bigtree import Node, get_path, print_tree
        >>> a = Node(name="a")
        >>> b = Node(name="b", parent=a)
        >>> c = Node(name="c", parent=a)
        >>> d = Node(name="d", parent=b)
        >>> e = Node(name="e", parent=b)
        >>> f = Node(name="f", parent=c)
        >>> g = Node(name="g", parent=e)
        >>> h = Node(name="h", parent=e)
        >>> print_tree(a)
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f
        >>> get_path(d, d)
        [Node(/a/b/d, )]
        >>> get_path(d, g)
        [Node(/a/b/d, ), Node(/a/b, ), Node(/a/b/e, ), Node(/a/b/e/g, )]
        >>> get_path(d, f)
        [Node(/a/b/d, ), Node(/a/b, ), Node(/a, ), Node(/a/c, ), Node(/a/c/f, )]

    Args:
        from_node: start point of path, node to travel from
        to_node: end point of path, node to travel to

    Returns:
        Path from origin to destination node from the same tree
    """
    common_ancestors = get_common_ancestors([from_node, to_node])
    min_common_ancestor = common_ancestors[0]
    from_path = [from_node] + list(from_node.ancestors)
    to_path = ([to_node] + list(to_node.ancestors))[::-1]
    from_min_index = from_path.index(min_common_ancestor)
    to_min_index = to_path.index(min_common_ancestor)
    return from_path[:from_min_index] + to_path[to_min_index:]
