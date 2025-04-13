from typing import List, Optional, TypeVar

from bigtree.node import dagnode
from bigtree.utils import exceptions

__all__ = [
    "get_path_dag",
]

T = TypeVar("T", bound=dagnode.DAGNode)


def get_path_dag(from_node: T, to_node: T) -> List[List[T]]:
    """Get path from origin node to destination node. Path is inclusive of origin and destination nodes.

    Examples:
        >>> from bigtree import DAGNode, get_path_dag
        >>> a = DAGNode("a")
        >>> b = DAGNode("b")
        >>> c = DAGNode("c")
        >>> d = DAGNode("d")
        >>> a >> c
        >>> b >> c
        >>> c >> d
        >>> a >> d
        >>> get_path_dag(a, c)
        [[DAGNode(a, ), DAGNode(c, )]]
        >>> get_path_dag(a, d)
        [[DAGNode(a, ), DAGNode(c, ), DAGNode(d, )], [DAGNode(a, ), DAGNode(d, )]]
        >>> get_path_dag(a, b)
        Traceback (most recent call last):
            ...
        bigtree.utils.exceptions.exceptions.TreeError: It is not possible to go to DAGNode(b, )

    Args:
        from_node: start point of path, node to travel from
        to_node: end point of path, node to travel to

    Returns:
        Possible paths from origin to destination node from the same DAG
    """
    if not isinstance(from_node, dagnode.DAGNode):
        raise TypeError(
            f"Expect node to be DAGNode type, received input type {type(from_node)}"
        )
    if not isinstance(to_node, dagnode.DAGNode):
        raise TypeError(
            f"Expect node to be DAGNode type, received input type {type(to_node)}"
        )
    if from_node == to_node:
        return [[from_node]]
    if to_node not in from_node.descendants:
        raise exceptions.TreeError(f"It is not possible to go to {to_node}")

    paths: List[List[T]] = []

    def _recursive_path(_node: T, _path: List[T]) -> Optional[List[T]]:
        """Get path to specified node.

        Args:
            _node: current node
            _path: current path, from start node to current node, excluding current node

        Returns:
            Path from current node to destination node
        """
        if _node:  # pragma: no cover
            _path.append(_node)
            if _node == to_node:
                return _path
            for _child in _node.children:
                ans = _recursive_path(_child, _path.copy())
                if ans:
                    paths.append(ans)
        return None

    _recursive_path(from_node, [])
    return paths
